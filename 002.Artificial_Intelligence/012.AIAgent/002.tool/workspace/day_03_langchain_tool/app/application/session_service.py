# -*- coding: utf-8 -*-
from __future__ import annotations

from app.domain.model import ChatMessage, ChatSession
from app.infrastructure.persistence import FIXED_USER_ID, ChatStore


class SessionApplicationService:
    """应用层：会话/消息管理（不调用 LLM）。"""

    def __init__(self, store: ChatStore) -> None:
        self._store = store

    def create_session(self, title: str = "新对话") -> ChatSession:
        return self._store.create_session(title=title, user_id=FIXED_USER_ID)

    def list_sessions(self) -> list[ChatSession]:
        return self._store.list_sessions(user_id=FIXED_USER_ID)

    def get_session(self, session_id: int) -> ChatSession:
        session = self._store.get_session(session_id, user_id=FIXED_USER_ID)
        if session is None:
            raise ValueError(f"会话不存在: {session_id}")
        return session

    def list_messages(self, session_id: int) -> list[ChatMessage]:
        self.get_session(session_id)
        return self._store.list_messages(session_id)

    def add_message(self, session_id: int, role: str, content: str) -> ChatMessage:
        self.get_session(session_id)
        return self._store.add_message(session_id, role, content)
