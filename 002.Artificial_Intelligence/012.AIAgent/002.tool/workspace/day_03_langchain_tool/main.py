# -*- coding: utf-8 -*-
"""
day_03 LangChain Tool — 对标 Spring AI day_02_spring_ai_tool

用法：
  pip install -r requirements.txt
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
    print("FastAPI + LangChain Tool Agent + SQLite 会话")
    print("=== 对标 Spring AI day_02 Tool ===")
    print(f"=== 浏览器访问 http://{host}:{port}/ ===")
    uvicorn.run(
        "app.interfaces.web.app:app",
        host=host,
        port=port,
        reload=False,
    )


if __name__ == "__main__":
    main()
