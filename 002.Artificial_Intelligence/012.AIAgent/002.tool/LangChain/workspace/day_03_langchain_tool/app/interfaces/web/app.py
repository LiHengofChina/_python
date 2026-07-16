# -*- coding: utf-8 -*-
from __future__ import annotations

from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field

from app.application.chat_service import AgentChatApplicationService, ChatApplicationService
from app.application.session_service import SessionApplicationService
from app.infrastructure.config import BASE_DIR, load_config
from app.infrastructure.llm import OllamaAgentChatGateway
from app.infrastructure.persistence import FIXED_USER_ID, ChatStore

STATIC_DIR = Path(__file__).resolve().parent / "static"

_cfg = load_config()
_db_path = BASE_DIR / _cfg.get("chat", {}).get("db_path", "data/chat.db")
_store = ChatStore(_db_path)
_session_service = SessionApplicationService(_store)
_agent_gateway = OllamaAgentChatGateway(_cfg)
_chat_service = ChatApplicationService(_agent_gateway, _session_service)
_agent_service = AgentChatApplicationService(_agent_gateway)

app = FastAPI(title="day03-langchain-tool", version="0.3.0")
app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")


class ChatRequest(BaseModel):
    question: str = Field(..., min_length=1)
    session_id: int | None = Field(default=None)


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
    ssh = _cfg.get("ssh", {})
    return {
        "status": "ok",
        "framework": "FastAPI + LangChain Tool Agent",
        "model": ora.get("model"),
        "user_id": FIXED_USER_ID,
        "ssh_enabled": bool(ssh.get("enabled")),
        "ssh_host": ssh.get("host"),
        "db_path": str(_db_path),
    }


@app.get("/api/sessions")
def list_sessions() -> list[dict]:
    return [
        {
            "id": s.id,
            "user_id": s.user_id,
            "title": s.title,
            "created_at": s.created_at,
        }
        for s in _session_service.list_sessions()
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
        raise HTTPException(status_code=502, detail=f"Agent/Tool 调用失败: {e}") from e


@app.get("/api/agent/troubleshoot")
def troubleshoot(q: str) -> dict:
    """对标 Spring：GET /api/agent/troubleshoot?q=..."""
    try:
        reply = _agent_service.troubleshoot(q)
        return {"question": reply.question, "answer": reply.answer}
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"排查失败: {e}") from e


@app.post("/api/agent/troubleshoot")
def troubleshoot_post(body: ChatRequest) -> ChatResponse:
    try:
        reply = _agent_service.troubleshoot(body.question)
        return ChatResponse(question=reply.question, answer=reply.answer)
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"排查失败: {e}") from e
