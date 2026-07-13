day_04_connection_manager — 连接管理 + Tool Agent
从 day_03_langchain_tool 复制并增强

命名：用「连接管理」而不是「主机管理」
  —— 可覆盖 linux / mysql / oracle / ftp 等，表结构：
  id + label + type + config_yaml

布局：
  左：菜单树（连接管理 / 聊天，后续可加 RAG 资料等）
  右：按菜单切换整页内容（各自独立页面，不再左右各占一半功能）

目录拆分：
  app/application/connection|session|chat     三套用例分包
  app/interfaces/web/connection|session|chat  三套 API 路由分包
  app/interfaces/web/app.py                   只负责挂载
  app/interfaces/web/container.py             组装服务

Tool：
  host_id = 连接的 label
  SSH 参数从 SQLite 解析，不再只靠 config.local.yml（yml 仅作首次种子）

API：
  GET/POST   /api/connections
  PUT/DELETE /api/connections/{id}
  会话与 /api/chat 同 day_03

步骤：
  1) pip install -r requirements.txt
  2) python main.py
  3) 浏览器 http://127.0.0.1:8101/
  4) 连接管理维护 label，聊天页提问排查
