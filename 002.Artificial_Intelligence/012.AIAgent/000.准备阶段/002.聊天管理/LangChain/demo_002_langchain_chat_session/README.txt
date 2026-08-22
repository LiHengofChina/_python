demo_002_langchain_chat_session — 聊天/会话管理（对标 Spring AI demo_002）
从 Chat demo01 增加：会话列表、消息落库、多轮上下文

聊天记录存哪？
  Demo：SQLite 文件 data/chat.db
  生产：一般用 MySQL / PostgreSQL

目录：
  app/domain/
  app/application/session_service.py + chat_service.py
  app/infrastructure/config|llm|persistence
  app/interfaces/web/   API + 左侧会话列表页面

固定用户：user_id=1
端口：Python 8101 · Java 8102（与 Chat 相同约定，同一时间只跑一个 Demo）

步骤：
  1) pip install -r requirements.txt
  2) python main.py
  3) 浏览器 http://127.0.0.1:8101/

API：
  GET/POST /api/sessions
  GET  /api/sessions/{id}/messages
  POST /api/chat  {"question":"...","session_id":1}
