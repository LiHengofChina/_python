# -*- coding: utf-8 -*-
"""
day_06 RAG（文档管理 + Chroma + Tool + SSE）
复制自 day_05；聊天前先检索知识库，再把资料拼进 Prompt。

用法：
  pip install -r requirements.txt
  ollama pull nomic-embed-text   # 若尚未拉取
  python main.py
  浏览器 http://127.0.0.1:8101/
"""
from __future__ import annotations

import uvicorn

from app.infrastructure.config import load_config


def main() -> None:
    cfg = load_config()
    server = cfg.get("server", {})
    host = server.get("host", "127.0.0.1")
    port = int(server.get("port", 8101))
    print("=== 框架 ===")
    print("FastAPI + 文档管理 + Chroma RAG + Tool Agent + SSE")
    print("=== 聊天：先 RAG 检索，再调模型/工具 ===")
    print(f"=== 浏览器访问 http://{host}:{port}/ ===")
    uvicorn.run(
        "app.interfaces.web.app:app",
        host=host,
        port=port,
        reload=False,
    )


if __name__ == "__main__":
    main()
