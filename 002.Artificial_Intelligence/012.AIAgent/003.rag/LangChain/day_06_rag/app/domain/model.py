# -*- coding: utf-8 -*-
from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class ChatReply:
    question: str
    answer: str


@dataclass(frozen=True)
class AgentChatReply:
    question: str
    answer: str


@dataclass(frozen=True)
class ChatSession:
    id: int
    user_id: int
    title: str
    created_at: str


@dataclass(frozen=True)
class ChatMessage:
    id: int
    session_id: int
    role: str
    content: str
    created_at: str


@dataclass(frozen=True)
class ConnectionProfile:
    """连接档案：linux / mysql / ftp / oracle 等，具体参数在 config_yaml。"""

    id: int
    label: str
    type: str
    config_yaml: str
    created_at: str
    updated_at: str
