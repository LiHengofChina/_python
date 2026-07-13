# -*- coding: utf-8 -*-
"""组装应用服务，供接口层注入。"""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from app.application.chat import AgentChatApplicationService, ChatApplicationService
from app.application.connection import ConnectionApplicationService
from app.application.session import SessionApplicationService
from app.infrastructure.config import BASE_DIR, load_config
from app.infrastructure.llm import OllamaAgentChatGateway
from app.infrastructure.persistence import ChatStore, ConnectionStore


@dataclass
class AppContainer:
    cfg: dict
    db_path: Path
    connection_service: ConnectionApplicationService
    session_service: SessionApplicationService
    chat_service: ChatApplicationService
    agent_service: AgentChatApplicationService


def build_container() -> AppContainer:
    cfg = load_config()
    db_path = BASE_DIR / cfg.get("chat", {}).get("db_path", "data/app.db")
    chat_store = ChatStore(db_path)
    conn_store = ConnectionStore(db_path)
    conn_store.seed_from_ssh_config(cfg.get("ssh", {}))

    session_service = SessionApplicationService(chat_store)
    connection_service = ConnectionApplicationService(conn_store)
    agent_gateway = OllamaAgentChatGateway(conn_store, cfg)
    chat_service = ChatApplicationService(agent_gateway, session_service)
    agent_service = AgentChatApplicationService(agent_gateway)

    return AppContainer(
        cfg=cfg,
        db_path=db_path,
        connection_service=connection_service,
        session_service=session_service,
        chat_service=chat_service,
        agent_service=agent_service,
    )


container = build_container()
