# -*- coding: utf-8 -*-
"""聊天 / Agent API。"""
from __future__ import annotations

from fastapi import APIRouter, HTTPException

from app.interfaces.web.container import container
from app.interfaces.web.schemas import ChatRequest, ChatResponse

router = APIRouter(tags=["聊天服务"])


@router.post("/api/chat", response_model=ChatResponse)
def chat_post(body: ChatRequest) -> ChatResponse:
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


@router.get("/api/agent/troubleshoot")
def troubleshoot(q: str) -> dict:
    try:
        reply = container.agent_service.troubleshoot(q)
        return {"question": reply.question, "answer": reply.answer}
    except Exception as e:
        raise HTTPException(status_code=502, detail=f"排查失败: {e}") from e
