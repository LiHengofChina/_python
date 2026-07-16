# -*- coding: utf-8 -*-
"""带 Tool 的 Agent 网关：ChatOllama.bind_tools + 手动循环。

ponytail: qwen2.5:7b 有时把工具调用写成 JSON 文本而不是 tool_calls；
若检测到这种「假调用」，解析后仍执行真实 Tool，避免只回 JSON 说明书。
"""
from __future__ import annotations

import json
import re
import uuid
from typing import Any

from langchain_core.messages import AIMessage, HumanMessage, SystemMessage, ToolMessage
from langchain_core.tools import BaseTool
from langchain_ollama import ChatOllama

from app.infrastructure.config import load_config
from app.infrastructure.ssh import LinuxSshExecutor
from app.infrastructure.tool import build_ops_tools

# 匹配模型把工具写成文本的几种常见样子
_JSON_BLOCK = re.compile(r"```(?:json)?\s*(\{.*?\})\s*```", re.S)
_NAME_ARGS = re.compile(
    r'\{\s*"name"\s*:\s*"([^"]+)"\s*,\s*"arguments"\s*:\s*(\{.*?\})\s*\}',
    re.S,
)

TOOL_SYSTEM_EXTRA = """
调用工具时，必须使用系统提供的函数调用（function/tool calling），不要把工具调用写成 JSON 文本或代码块给用户看。
拿到工具返回的真实数据后，再用中文简洁总结。host_id 固定填 linux-231。
""".strip()


class OllamaAgentChatGateway:
    def __init__(self, cfg: dict | None = None) -> None:
        cfg = cfg or load_config()
        ora = cfg.get("ollama", {})
        self._llm = ChatOllama(
            base_url=ora.get("base_url", "http://127.0.0.1:11434"),
            model=ora.get("model", "qwen2.5:7b"),
            temperature=float(ora.get("temperature", 0.1)),
            client_kwargs={"trust_env": False},
        )
        ssh = LinuxSshExecutor(cfg.get("ssh", {}))
        self._tools: list[BaseTool] = build_ops_tools(ssh)
        self._tool_map = {t.name: t for t in self._tools}
        self._bound = self._llm.bind_tools(self._tools)

    def chat_with_tools(self, system_prompt: str, user_message: str) -> str:
        messages: list[Any] = [
            SystemMessage(content=f"{system_prompt}\n\n{TOOL_SYSTEM_EXTRA}"),
            HumanMessage(content=user_message),
        ]
        return self._run_loop(messages)

    def chat_messages_with_tools(
        self, system_prompt: str, history: list[tuple[str, str]]
    ) -> str:
        messages: list[Any] = [
            SystemMessage(content=f"{system_prompt}\n\n{TOOL_SYSTEM_EXTRA}")
        ]
        for role, content in history:
            if role == "assistant":
                messages.append(AIMessage(content=content))
            elif role == "user":
                messages.append(HumanMessage(content=content))
        return self._run_loop(messages)

    def _run_loop(self, messages: list[Any], max_rounds: int = 6) -> str:
        for _ in range(max_rounds):
            ai: AIMessage = self._bound.invoke(messages)
            messages.append(ai)

            calls = list(ai.tool_calls or [])
            if not calls:
                # 模型把工具写成了文本 JSON → 兜底解析并当真工具跑
                calls = self._parse_text_tool_calls(str(ai.content or ""))
                if calls:
                    print(f"[Tool-Fallback] 从文本解析到 {len(calls)} 个工具调用")
                    # 换成带 tool_calls 的 AIMessage，方便后续 ToolMessage 对齐
                    ai_fixed = AIMessage(content="", tool_calls=calls)
                    messages[-1] = ai_fixed

            if not calls:
                text = str(ai.content or "").strip()
                # 若仍是「请等待工具返回」这类空转，再逼一次
                if self._looks_like_fake_tool_plan(text):
                    messages.append(
                        HumanMessage(
                            content="不要输出 JSON。请直接发起真正的工具调用（function call）。"
                        )
                    )
                    continue
                return text or "(无输出)"

            for call in calls:
                name = call["name"]
                args = call.get("args") or {}
                call_id = call.get("id") or str(uuid.uuid4())
                print(f"[Tool] {name} args={args}")
                tool = self._tool_map.get(name)
                if tool is None:
                    result = f"未知工具: {name}"
                else:
                    try:
                        result = tool.invoke(args)
                    except Exception as e:
                        result = f"工具执行失败: {e}"
                messages.append(
                    ToolMessage(content=str(result), tool_call_id=call_id, name=name)
                )

        return "工具调用轮次过多，已停止。请缩小问题再试。"

    def _parse_text_tool_calls(self, text: str) -> list[dict]:
        if not text:
            return []
        found: list[dict] = []
        blobs: list[str] = _JSON_BLOCK.findall(text)
        if not blobs:
            blobs = [m.group(0) for m in _NAME_ARGS.finditer(text)]

        for blob in blobs:
            try:
                obj = json.loads(blob)
            except json.JSONDecodeError:
                m = _NAME_ARGS.search(blob)
                if not m:
                    continue
                try:
                    obj = {"name": m.group(1), "arguments": json.loads(m.group(2))}
                except json.JSONDecodeError:
                    continue
            name = obj.get("name")
            args = obj.get("arguments") or obj.get("args") or {}
            if isinstance(args, str):
                try:
                    args = json.loads(args)
                except json.JSONDecodeError:
                    args = {"host_id": args}
            if name in self._tool_map and isinstance(args, dict):
                found.append(
                    {
                        "name": name,
                        "args": args,
                        "id": str(uuid.uuid4()),
                        "type": "tool_call",
                    }
                )
        # 去重（模型常重复贴同一段 JSON）
        uniq: list[dict] = []
        seen: set[tuple] = set()
        for c in found:
            key = (c["name"], json.dumps(c["args"], sort_keys=True, ensure_ascii=False))
            if key in seen:
                continue
            seen.add(key)
            uniq.append(c)
        return uniq

    @staticmethod
    def _looks_like_fake_tool_plan(text: str) -> bool:
        if not text:
            return False
        markers = ("请等待工具", "```json", '"name":', "arguments", "函数调用")
        return any(m in text for m in markers) and "exit=" not in text
