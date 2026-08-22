# -*- coding: utf-8 -*-
from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class ChatReply:
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
    role: str  # user | assistant | system
    content: str
    created_at: str
