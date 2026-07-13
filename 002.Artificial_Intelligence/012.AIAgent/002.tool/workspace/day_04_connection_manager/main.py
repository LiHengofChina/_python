# -*- coding: utf-8 -*-
"""
day_04 连接管理 + Tool Agent
复制自 day_03，增加连接档案 CRUD；Tool 按 label 从 SQLite 取配置。

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
    print("FastAPI + 连接管理 + LangChain Tool Agent")
    print("=== 左：连接管理 / 右：会话+Agent ===")
    print(f"=== 浏览器访问 http://{host}:{port}/ ===")
    uvicorn.run(
        "app.interfaces.web.app:app",
        host=host,
        port=port,
        reload=False,
    )


if __name__ == "__main__":
    main()
