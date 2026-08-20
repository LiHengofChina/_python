# -*- coding: utf-8 -*-
from __future__ import annotations

from app.domain.gateway import LlmChatGateway
from app.domain.model import ChatReply


class ChatApplicationService:
    """应用层：编排对话用例（对标 ChatApplicationService）。"""

    def __init__(self, gateway: LlmChatGateway) -> None:
        self._gateway = gateway

    def chat(self, question: str) -> ChatReply:
        return ChatReply(question=question, answer=self._gateway.chat(question))

    def chat_with_system(self, system_prompt: str, question: str) -> ChatReply:
        return ChatReply(
            question=question,
            answer=self._gateway.chat_with_system(system_prompt, question),
        )
