day_02_chat_session — 聊天/会话管理 Demo
从 001.Chat/day_01 复制后增加：会话列表、消息落库、多轮上下文

聊天记录存哪？
  Demo：SQLite 文件 data/chat.db（也是数据库，零安装）
  生产：一般用 MySQL / PostgreSQL 等，不推荐长期只靠纯文本文件

目录：
  app/domain/                 模型（Session / Message）
  app/application/
    session_service.py        会话/消息用例（不调 LLM）
    chat_service.py           对话用例（调 LLM，会话内对话委托 Session）
  app/infrastructure/
    config/                   读 config.local.yml
    llm/                      OllamaChatGateway
    persistence/              SQLite ChatStore（会话/消息）
  app/interfaces/web/         API + 左侧会话列表页面
  data/chat.db                运行后自动生成

固定用户：user_id=1

步骤：
  1) pip install -r requirements.txt
  2) python main.py
  3) 浏览器 http://127.0.0.1:8102/
  4) 新建会话 → 提问 → 同会话再追问（模型能看到历史）

API：
  GET/POST /api/sessions
  GET  /api/sessions/{id}/messages
  POST /api/chat  {"question":"...","session_id":1}
