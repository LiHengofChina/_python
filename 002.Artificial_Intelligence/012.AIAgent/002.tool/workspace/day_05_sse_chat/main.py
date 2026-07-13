# -*- coding: utf-8 -*-
"""
day_05 SSE 聊天（Cursor 风格过程展示）
复制自 day_04；聊天走 /api/chat/stream，推送 Thinking / Tool 进度。

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
    print("FastAPI + 连接管理 + LangChain Tool Agent + SSE")
    print("=== 聊天：POST /api/chat/stream ===")
    print(f"=== 浏览器访问 http://{host}:{port}/ ===")
    uvicorn.run(
        "app.interfaces.web.app:app",
        host=host,
        port=port,
        reload=False,
    )


if __name__ == "__main__":
    main()
