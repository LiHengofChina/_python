# -*- coding: utf-8 -*-
"""组装应用服务，供接口层注入。"""
from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from app.application.chat import AgentChatApplicationService, ChatApplicationService
from app.application.connection import ConnectionApplicationService
from app.application.document import DocumentApplicationService
from app.application.session import SessionApplicationService
from app.infrastructure.config import BASE_DIR, load_config
from app.infrastructure.llm import OllamaAgentChatGateway
from app.infrastructure.persistence import ChatStore, ConnectionStore
from app.infrastructure.persistence.document_store import DocumentStore
from app.infrastructure.rag import ChromaRagStore


@dataclass
class AppContainer:
    cfg: dict
    db_path: Path
    connection_service: ConnectionApplicationService
    session_service: SessionApplicationService
    chat_service: ChatApplicationService
    agent_service: AgentChatApplicationService
    document_service: DocumentApplicationService
    rag_store: ChromaRagStore


def build_container() -> AppContainer:
    cfg = load_config()
    db_path = BASE_DIR / cfg.get("chat", {}).get("db_path", "data/app.db")
    upload_dir = BASE_DIR / cfg.get("rag", {}).get("upload_dir", "data/uploads")
    chroma_dir = BASE_DIR / cfg.get("rag", {}).get("chroma_dir", "data/chroma")

    chat_store = ChatStore(db_path)
    conn_store = ConnectionStore(db_path)
    conn_store.seed_from_ssh_config(cfg.get("ssh", {}))
    doc_store = DocumentStore(db_path, upload_dir)

    ora = cfg.get("ollama", {})
    rag_cfg = cfg.get("rag", {})
    rag_store = ChromaRagStore(
        chroma_dir,
        base_url=ora.get("base_url", "http://127.0.0.1:11434"),
        embed_model=ora.get("embed_model", "nomic-embed-text"),
        chunk_size=int(rag_cfg.get("chunk_size", 500)),
        chunk_overlap=int(rag_cfg.get("chunk_overlap", 50)),
        top_k=int(rag_cfg.get("top_k", 3)),
    )

    session_service = SessionApplicationService(chat_store)
    connection_service = ConnectionApplicationService(conn_store)
    document_service = DocumentApplicationService(doc_store, rag_store)
    agent_gateway = OllamaAgentChatGateway(conn_store, cfg, rag_store=rag_store)
    chat_service = ChatApplicationService(agent_gateway, session_service)
    agent_service = AgentChatApplicationService(agent_gateway)

    return AppContainer(
        cfg=cfg,
        db_path=db_path,
        connection_service=connection_service,
        session_service=session_service,
        chat_service=chat_service,
        agent_service=agent_service,
        document_service=document_service,
        rag_store=rag_store,
    )


container = build_container()
