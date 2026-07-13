# -*- coding: utf-8 -*-
"""聊天 / Agent API（含 SSE 流式进度）。"""
from __future__ import annotations

import json

from fastapi import APIRouter, HTTPException
from fastapi.responses import StreamingResponse

from app.interfaces.web.container import container
from app.interfaces.web.schemas import ChatRequest, ChatResponse

router = APIRouter(tags=["聊天服务"])


def _sse(data: dict) -> str:
    return f"data: {json.dumps(data, ensure_ascii=False)}\n\n"


@router.post("/api/chat", response_model=ChatResponse)
def chat_post(body: ChatRequest) -> ChatResponse:
    """保留普通 HTTP，便于兼容；页面默认走 /api/chat/stream。"""
    try:
        if body.session_id is None:
            reply = container.chat_service.chat(body.question)
            return ChatResponse(question=reply.question, answer=reply.answer)
        reply = container.chat_service.chat_in_session(body.session_id, body.question)
        return ChatResponse(
            question=reply.question,
            answer=reply.answer,
            session_id=body.session_id,
        )
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e)) from e
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"Agent/Tool 调用失败: {e}") from e


@router.post("/api/chat/stream")
def chat_stream(body: ChatRequest) -> StreamingResponse:
    """SSE：推送 Thinking / Tool / Answer 进度（Cursor 风格过程展示）。"""
    if body.session_id is None:
        raise HTTPException(status_code=400, detail="SSE 聊天需要 session_id")

    session_id = body.session_id
    question = body.question

    def event_gen():
        try:
            yield _sse({"type": "status", "message": "Starting…"})
            for ev in container.chat_service.iter_chat_in_session(session_id, question):
                yield _sse(ev)
        except Exception as e:
            yield _sse({"type": "error", "message": str(e)})

    return StreamingResponse(
        event_gen(),
        media_type="text/event-stream",
        headers={
            "Cache-Control": "no-cache",
            "Connection": "keep-alive",
            "X-Accel-Buffering": "no",
        },
    )


@router.get("/api/agent/troubleshoot")
def troubleshoot(q: str) -> dict:
    try:
        reply = container.agent_service.troubleshoot(q)
        return {"question": reply.question, "answer": reply.answer}
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"排查失败: {e}") from e
