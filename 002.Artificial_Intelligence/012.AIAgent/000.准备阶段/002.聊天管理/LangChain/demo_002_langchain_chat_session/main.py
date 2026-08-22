# -*- coding: utf-8 -*-
"""
demo_002_langchain_chat_session — 会话管理（SQLite）
对标 Spring AI demo_002_spring_ai_chat_session

用法：
  pip install -r requirements.txt
  python main.py
  浏览器打开 http://127.0.0.1:8101/
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
    print("FastAPI + LangChain + SQLite 会话管理")
    print("=== 固定用户 user_id=1 ===")
    print(f"=== 浏览器访问 http://{host}:{port}/ ===")
    uvicorn.run(
        "app.interfaces.web.app:app",
        host=host,
        port=port,
        reload=False,
    )


if __name__ == "__main__":
    main()
