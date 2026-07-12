# -*- coding: utf-8 -*-
from __future__ import annotations

from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field

from app.application.chat_service import ChatApplicationService
from app.application.session_service import SessionApplicationService
from app.infrastructure.config import BASE_DIR, load_config
from app.infrastructure.llm import OllamaChatGateway
from app.infrastructure.persistence import FIXED_USER_ID, ChatStore

STATIC_DIR = Path(__file__).resolve().parent / "static"

_cfg = load_config()
_db_path = BASE_DIR / _cfg.get("chat", {}).get("db_path", "data/chat.db")
_store = ChatStore(_db_path)
_session_service = SessionApplicationService(_store)
_chat_service = ChatApplicationService(OllamaChatGateway(_cfg), _session_service)

app = FastAPI(title="day02-chat-session", version="0.2.0")
app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")


class ChatRequest(BaseModel):
    question: str = Field(..., min_length=1)
    session_id: int | None = Field(default=None, description="会话 ID；不传则无历史单轮")


class SessionCreateRequest(BaseModel):
    title: str = "新对话"


class ChatResponse(BaseModel):
    question: str
    answer: str
    session_id: int | None = None


@app.get("/")
def index() -> FileResponse:
    return FileResponse(STATIC_DIR / "index.html")


@app.get("/api/health")
def health() -> dict:
    ora = _cfg.get("ollama", {})
    return {
        "status": "ok",
        "framework": "FastAPI + LangChain + SQLite 会话",
        "model": ora.get("model"),
        "user_id": FIXED_USER_ID,
        "db_path": str(_db_path),
    }


@app.get("/api/sessions")
def list_sessions() -> list[dict]:
    sessions = _session_service.list_sessions()
    return [
        {
            "id": s.id,
            "user_id": s.user_id,
            "title": s.title,
            "created_at": s.created_at,
        }
        for s in sessions
    ]


@app.post("/api/sessions")
def create_session(body: SessionCreateRequest | None = None) -> dict:
    title = body.title if body else "新对话"
    s = _session_service.create_session(title=title)
    return {
        "id": s.id,
        "user_id": s.user_id,
        "title": s.title,
        "created_at": s.created_at,
    }


@app.get("/api/sessions/{session_id}/messages")
def list_messages(session_id: int) -> list[dict]:
    try:
        msgs = _session_service.list_messages(session_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e)) from e
    return [
        {
            "id": m.id,
            "session_id": m.session_id,
            "role": m.role,
            "content": m.content,
            "created_at": m.created_at,
        }
        for m in msgs
    ]


@app.post("/api/chat")
def chat_post(body: ChatRequest) -> ChatResponse:
    try:
        if body.session_id is None:
            reply = _chat_service.chat(body.question)
            return ChatResponse(question=reply.question, answer=reply.answer)
        reply = _chat_service.chat_in_session(body.session_id, body.question)
        return ChatResponse(
            question=reply.question,
            answer=reply.answer,
            session_id=body.session_id,
        )
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e)) from e
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"调用 Ollama 失败: {e}") from e
