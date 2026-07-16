# -*- coding: utf-8 -*-
"""领域端口：LLM 网关接口（对标 Java LlmChatGateway）。"""
from __future__ import annotations

from typing import Protocol


class LlmChatGateway(Protocol):
    def chat(self, user_message: str) -> str: ...

    def chat_with_system(self, system_prompt: str, user_message: str) -> str: ...

    def chat_messages(self, messages: list[tuple[str, str]]) -> str: ...
