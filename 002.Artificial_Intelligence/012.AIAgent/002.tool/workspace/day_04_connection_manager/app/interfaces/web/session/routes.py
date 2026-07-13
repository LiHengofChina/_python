# -*- coding: utf-8 -*-
"""会话管理 API。"""
from __future__ import annotations

from fastapi import APIRouter, HTTPException

from app.interfaces.web.container import container
from app.interfaces.web.schemas import SessionCreateRequest

router = APIRouter(prefix="/api/sessions", tags=["会话管理"])


@router.get("")
def list_sessions() -> list[dict]:
    return [
        {
            "id": s.id,
            "user_id": s.user_id,
            "title": s.title,
            "created_at": s.created_at,
        }
        for s in container.session_service.list_sessions()
    ]


@router.post("")
def create_session(body: SessionCreateRequest | None = None) -> dict:
    title = body.title if body else "新对话"
    s = container.session_service.create_session(title=title)
    return {
        "id": s.id,
        "user_id": s.user_id,
        "title": s.title,
        "created_at": s.created_at,
    }


@router.get("/{session_id}/messages")
def list_messages(session_id: int) -> list[dict]:
    try:
        msgs = container.session_service.list_messages(session_id)
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
