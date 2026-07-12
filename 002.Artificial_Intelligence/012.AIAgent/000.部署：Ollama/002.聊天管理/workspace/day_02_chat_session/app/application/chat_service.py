# -*- coding: utf-8 -*-
from __future__ import annotations

from app.application.session_service import SessionApplicationService
from app.domain.gateway import LlmChatGateway
from app.domain.model import ChatReply


class ChatApplicationService:
    """应用层：对话用例（调 LLM；会话内对话会委托 Session 服务）。"""

    def __init__(
        self,
        gateway: LlmChatGateway,
        session_service: SessionApplicationService,
    ) -> None:
        self._gateway = gateway
        self._sessions = session_service

    def chat(self, question: str) -> ChatReply:
        return ChatReply(question=question, answer=self._gateway.chat(question))

    def chat_with_system(self, system_prompt: str, question: str) -> ChatReply:
        return ChatReply(
            question=question,
            answer=self._gateway.chat_with_system(system_prompt, question),
        )

    def chat_in_session(self, session_id: int, question: str) -> ChatReply:
        self._sessions.get_session(session_id)

        history = self._sessions.list_messages(session_id)
        # ponytail: 只带最近 20 条，避免上下文过长撑爆 7B
        recent = history[-20:]
        payload = [(m.role, m.content) for m in recent]
        payload.append(("user", question))

        answer = self._gateway.chat_messages(payload)

        self._sessions.add_message(session_id, "user", question)
        self._sessions.add_message(session_id, "assistant", answer)
        return ChatReply(question=question, answer=answer)
