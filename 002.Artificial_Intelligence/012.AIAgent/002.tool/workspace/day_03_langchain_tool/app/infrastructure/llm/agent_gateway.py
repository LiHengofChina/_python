# -*- coding: utf-8 -*-
"""带 Tool 的 Agent 网关：LangGraph create_react_agent（对标 Spring defaultTools）。"""
from __future__ import annotations

from langchain_core.messages import AIMessage, HumanMessage, SystemMessage
from langchain_ollama import ChatOllama
from langgraph.prebuilt import create_react_agent

from app.infrastructure.config import load_config
from app.infrastructure.ssh import LinuxSshExecutor
from app.infrastructure.tool import build_ops_tools


class OllamaAgentChatGateway:
    def __init__(self, cfg: dict | None = None) -> None:
        cfg = cfg or load_config()
        ora = cfg.get("ollama", {})
        self._llm = ChatOllama(
            base_url=ora.get("base_url", "http://127.0.0.1:11434"),
            model=ora.get("model", "qwen2.5:7b"),
            temperature=float(ora.get("temperature", 0.2)),
            client_kwargs={"trust_env": False},
        )
        ssh = LinuxSshExecutor(cfg.get("ssh", {}))
        tools = build_ops_tools(ssh)
        self._agent = create_react_agent(self._llm, tools)

    def chat_with_tools(self, system_prompt: str, user_message: str) -> str:
        result = self._agent.invoke(
            {
                "messages": [
                    SystemMessage(content=system_prompt),
                    HumanMessage(content=user_message),
                ]
            }
        )
        messages = result.get("messages") or []
        for msg in reversed(messages):
            if isinstance(msg, AIMessage) and msg.content and not msg.tool_calls:
                return str(msg.content)
        return str(messages[-1].content) if messages else "(无输出)"

    def chat_messages_with_tools(
        self, system_prompt: str, history: list[tuple[str, str]]
    ) -> str:
        """history: [(role, content), ...] 含本轮 user。"""
        msgs: list = [SystemMessage(content=system_prompt)]
        for role, content in history:
            if role == "assistant":
                msgs.append(AIMessage(content=content))
            elif role == "user":
                msgs.append(HumanMessage(content=content))
        result = self._agent.invoke({"messages": msgs})
        messages = result.get("messages") or []
        for msg in reversed(messages):
            if isinstance(msg, AIMessage) and msg.content and not msg.tool_calls:
                return str(msg.content)
        return str(messages[-1].content) if messages else "(无输出)"
