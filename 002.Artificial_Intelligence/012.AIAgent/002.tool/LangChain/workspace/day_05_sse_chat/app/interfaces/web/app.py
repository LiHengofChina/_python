# -*- coding: utf-8 -*-
"""FastAPI 入口：挂载静态页 + 各业务路由。"""
from __future__ import annotations

from pathlib import Path

from fastapi import FastAPI
from fastapi.responses import FileResponse
from fastapi.staticfiles import StaticFiles

from app.infrastructure.persistence import FIXED_USER_ID
from app.interfaces.web import chat as chat_api
from app.interfaces.web import connection as connection_api
from app.interfaces.web import session as session_api
from app.interfaces.web.container import container

STATIC_DIR = Path(__file__).resolve().parent / "static"

app = FastAPI(title="day04-connection-manager", version="0.4.0")
app.mount("/static", StaticFiles(directory=str(STATIC_DIR)), name="static")
app.include_router(connection_api.router)
app.include_router(session_api.router)
app.include_router(chat_api.router)


@app.get("/")
def index() -> FileResponse:
    return FileResponse(STATIC_DIR / "index.html")


@app.get("/api/health")
def health() -> dict:
    ora = container.cfg.get("ollama", {})
    return {
        "status": "ok",
        "framework": "FastAPI + 连接管理 + Tool Agent",
        "model": ora.get("model"),
        "user_id": FIXED_USER_ID,
        "connections": len(container.connection_service.list_connections()),
        "db_path": str(container.db_path),
    }
