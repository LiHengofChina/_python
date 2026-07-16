# -*- coding: utf-8 -*-
"""连接管理 API。"""
from __future__ import annotations

from fastapi import APIRouter, HTTPException

from app.interfaces.web.container import container
from app.interfaces.web.schemas import ConnectionBody

router = APIRouter(prefix="/api/connections", tags=["连接管理"])


@router.get("")
def list_connections() -> list[dict]:
    return [
        {
            "id": c.id,
            "label": c.label,
            "type": c.type,
            "config_yaml": c.config_yaml,
            "created_at": c.created_at,
            "updated_at": c.updated_at,
        }
        for c in container.connection_service.list_connections()
    ]


@router.post("")
def create_connection(body: ConnectionBody) -> dict:
    try:
        c = container.connection_service.create(body.label, body.type, body.config_yaml)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e)) from e
    return {
        "id": c.id,
        "label": c.label,
        "type": c.type,
        "config_yaml": c.config_yaml,
        "created_at": c.created_at,
        "updated_at": c.updated_at,
    }


@router.put("/{conn_id}")
def update_connection(conn_id: int, body: ConnectionBody) -> dict:
    try:
        c = container.connection_service.update(
            conn_id, body.label, body.type, body.config_yaml
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e)) from e
    return {
        "id": c.id,
        "label": c.label,
        "type": c.type,
        "config_yaml": c.config_yaml,
        "created_at": c.created_at,
        "updated_at": c.updated_at,
    }


@router.delete("/{conn_id}")
def delete_connection(conn_id: int) -> dict:
    try:
        container.connection_service.delete(conn_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e)) from e
    return {"ok": True, "id": conn_id}
