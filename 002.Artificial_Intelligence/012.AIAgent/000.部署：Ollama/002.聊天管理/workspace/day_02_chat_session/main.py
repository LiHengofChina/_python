# -*- coding: utf-8 -*-
"""
day_02 聊天管理（会话）— 在 day_01 Chat 上增加 SQLite 会话/消息

用法：
  pip install -r requirements.txt
  python main.py
  浏览器打开 http://127.0.0.1:8102/
"""
from __future__ import annotations

import uvicorn

from app.infrastructure.config import load_config


def main() -> None:
    cfg = load_config()
    server = cfg.get("server", {})
    host = server.get("host", "127.0.0.1")
    port = int(server.get("port", 8102))
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
