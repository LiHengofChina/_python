# -*- coding: utf-8 -*-
from __future__ import annotations

import json
from collections.abc import Iterator
from typing import Any

from app.application.session import SessionApplicationService
from app.domain.model import AgentChatReply, ChatReply
from app.infrastructure.llm import OllamaAgentChatGateway

OPS_SYSTEM_PROMPT = """你是银行运维助手。排查问题时必须先调用可用工具获取事实，再给出结论和建议。
host_id 必须使用系统提示里「当前可用连接」的 label，原样填写，不要改写、不要加「机器」等后缀。
涉及重启、删除、变更等生产操作，必须提醒需要人工审批。"""


class AgentChatApplicationService:
    """应用层：带 Tool 的运维排查。"""

    def __init__(self, agent_gateway: OllamaAgentChatGateway) -> None:
        self._agent = agent_gateway

    def troubleshoot(self, question: str) -> AgentChatReply:
        answer = self._agent.chat_with_tools(OPS_SYSTEM_PROMPT, question)
        return AgentChatReply(question=question, answer=answer)


class ChatApplicationService:
    """应用层：对话 + 会话内带 Tool 的多轮对话（支持 SSE 事件流）。"""

    def __init__(
        self,
        agent_gateway: OllamaAgentChatGateway,
        session_service: SessionApplicationService,
    ) -> None:
        self._agent = agent_gateway
        self._sessions = session_service

    def chat(self, question: str) -> ChatReply:
        answer = self._agent.chat_with_tools(OPS_SYSTEM_PROMPT, question)
        return ChatReply(question=question, answer=answer)

    def chat_in_session(self, session_id: int, question: str) -> ChatReply:
        answer = ""
        for ev in self.iter_chat_in_session(session_id, question):
            if ev.get("type") == "answer":
                answer = str(ev.get("content") or "")
        return ChatReply(question=question, answer=answer)

    def iter_chat_in_session(
        self, session_id: int, question: str
    ) -> Iterator[dict[str, Any]]:
        self._sessions.get_session(session_id)
        yield {"type": "status", "message": "Loading session…"}

        history = self._sessions.list_messages(session_id)
        # ponytail: trace 只给人看，不喂模型
        recent = [m for m in history if m.role in ("user", "assistant")][-20:]
        payload = [(m.role, m.content) for m in recent]
        payload.append(("user", question))

        answer = ""
        trace: list[dict[str, Any]] = []
        try:
            for ev in self._agent.iter_chat_messages_with_tools(
                OPS_SYSTEM_PROMPT, payload
            ):
                if ev.get("type") == "answer":
                    answer = str(ev.get("content") or "")
                elif ev.get("type") in ("status", "tool_start", "tool_end"):
                    trace.append(ev)
                yield ev
        except Exception as e:
            yield {"type": "error", "message": str(e)}
            return

        self._sessions.add_message(session_id, "user", question)
        if trace:
            self._sessions.add_message(
                session_id, "trace", json.dumps(trace, ensure_ascii=False)
            )
        self._sessions.add_message(session_id, "assistant", answer or "(无输出)")
        yield {
            "type": "done",
            "session_id": session_id,
            "message": "Done",
        }
