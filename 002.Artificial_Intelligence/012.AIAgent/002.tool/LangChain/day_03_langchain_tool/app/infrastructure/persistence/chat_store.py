# -*- coding: utf-8 -*-
"""SQLite 会话/消息仓储。Demo 固定 user_id=1。"""
from __future__ import annotations

import sqlite3
from pathlib import Path

from app.domain.model import ChatMessage, ChatSession

FIXED_USER_ID = 1


class ChatStore:
    def __init__(self, db_path: Path) -> None:
        self.db_path = db_path
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self._init_schema()

    def _connect(self) -> sqlite3.Connection:
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn

    def _init_schema(self) -> None:
        with self._connect() as conn:
            conn.executescript(
                """
                CREATE TABLE IF NOT EXISTS chat_session (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    user_id INTEGER NOT NULL,
                    title TEXT NOT NULL,
                    created_at TEXT NOT NULL DEFAULT (datetime('now','localtime'))
                );
                CREATE TABLE IF NOT EXISTS chat_message (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    session_id INTEGER NOT NULL,
                    role TEXT NOT NULL,
                    content TEXT NOT NULL,
                    created_at TEXT NOT NULL DEFAULT (datetime('now','localtime')),
                    FOREIGN KEY(session_id) REFERENCES chat_session(id)
                );
                """
            )

    def create_session(self, title: str = "新对话", user_id: int = FIXED_USER_ID) -> ChatSession:
        with self._connect() as conn:
            cur = conn.execute(
                "INSERT INTO chat_session(user_id, title) VALUES (?, ?)",
                (user_id, title),
            )
            sid = int(cur.lastrowid)
            row = conn.execute("SELECT * FROM chat_session WHERE id = ?", (sid,)).fetchone()
        return self._session(row)

    def list_sessions(self, user_id: int = FIXED_USER_ID) -> list[ChatSession]:
        with self._connect() as conn:
            rows = conn.execute(
                "SELECT * FROM chat_session WHERE user_id = ? ORDER BY id DESC",
                (user_id,),
            ).fetchall()
        return [self._session(r) for r in rows]

    def get_session(self, session_id: int, user_id: int = FIXED_USER_ID) -> ChatSession | None:
        with self._connect() as conn:
            row = conn.execute(
                "SELECT * FROM chat_session WHERE id = ? AND user_id = ?",
                (session_id, user_id),
            ).fetchone()
        return self._session(row) if row else None

    def list_messages(self, session_id: int) -> list[ChatMessage]:
        with self._connect() as conn:
            rows = conn.execute(
                "SELECT * FROM chat_message WHERE session_id = ? ORDER BY id ASC",
                (session_id,),
            ).fetchall()
        return [self._message(r) for r in rows]

    def add_message(self, session_id: int, role: str, content: str) -> ChatMessage:
        with self._connect() as conn:
            cur = conn.execute(
                "INSERT INTO chat_message(session_id, role, content) VALUES (?, ?, ?)",
                (session_id, role, content),
            )
            mid = int(cur.lastrowid)
            # ponytail: 首条用户消息时用前 20 字更新标题，避免全叫「新对话」
            if role == "user":
                title_row = conn.execute(
                    "SELECT COUNT(*) AS c FROM chat_message WHERE session_id = ?",
                    (session_id,),
                ).fetchone()
                if int(title_row["c"]) == 1:
                    conn.execute(
                        "UPDATE chat_session SET title = ? WHERE id = ?",
                        (content.strip()[:20] or "新对话", session_id),
                    )
            row = conn.execute("SELECT * FROM chat_message WHERE id = ?", (mid,)).fetchone()
        return self._message(row)

    @staticmethod
    def _session(row: sqlite3.Row) -> ChatSession:
        return ChatSession(
            id=int(row["id"]),
            user_id=int(row["user_id"]),
            title=str(row["title"]),
            created_at=str(row["created_at"]),
        )

    @staticmethod
    def _message(row: sqlite3.Row) -> ChatMessage:
        return ChatMessage(
            id=int(row["id"]),
            session_id=int(row["session_id"]),
            role=str(row["role"]),
            content=str(row["content"]),
            created_at=str(row["created_at"]),
        )
