# -*- coding: utf-8 -*-
from __future__ import annotations

from pathlib import Path

from fastapi import FastAPI, HTTPException
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles
from pydantic import BaseModel, Field

from app.application.chat_service import ChatApplicationService
from app.infrastructure.config import load_config
from app.infrastructure.ollama_gateway import OllamaChatGateway

STATIC_DIR = Path(__file__).resolve().parent / "static"

_cfg = load_config()
_service = ChatApplicationService(OllamaChatGateway(_cfg))

app = FastAPI(title="day01-langchain-chat", version="0.1.0")
app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")


class ChatRequest(BaseModel):
    question: str = Field(..., min_length=1, description="用户问题")


class ChatResponse(BaseModel):
    question: str
    answer: str


@app.get("/")
def index() -> FileResponse:
    return FileResponse(STATIC_DIR / "index.html")


@app.get("/api/health")
def health() -> dict:
    ora = _cfg.get("ollama", {})
    return {
        "status": "ok",
        "framework": "FastAPI + LangChain ChatOllama",
        "model": ora.get("model"),
        "base_url": ora.get("base_url"),
    }


@app.get("/api/chat")
def chat_get(q: str) -> ChatResponse:
    """对标 Spring AI：GET /api/chat?q=..."""
    return _do_chat(q)


@app.post("/api/chat")
def chat_post(body: ChatRequest) -> ChatResponse:
    """浏览器页面用 POST。"""
    return _do_chat(body.question)


@app.get("/api/chat/ops")
def chat_ops(q: str) -> ChatResponse:
    system = "你是银行运维助手，回答要简洁、可执行，涉及生产操作要提醒人工审批。"
    try:
        reply = _service.chat_with_system(system, q)
        return ChatResponse(question=reply.question, answer=reply.answer)
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"调用 Ollama 失败: {e}") from e


def _do_chat(question: str) -> ChatResponse:
    try:
        reply = _service.chat(question)
        return ChatResponse(question=reply.question, answer=reply.answer)
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"调用 Ollama 失败: {e}") from e
