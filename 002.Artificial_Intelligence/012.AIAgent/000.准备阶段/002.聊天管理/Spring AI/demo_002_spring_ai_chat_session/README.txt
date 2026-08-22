demo_002_spring_ai_chat_session — 聊天/会话管理（对标 LangChain demo_002）

功能：
  会话列表 / 新建 / 切换
  消息落库 SQLite（data/chat.db）
  同会话多轮：历史拼进 Spring AI ChatClient

端口：Python 8101 · Java 8102（与 Chat 相同约定，同一时间只跑一个 Demo）
固定用户：user_id=1

步骤：
  1) Ollama 已启动，已 pull qwen2.5:7b
  2) IDEA Open → Spring AI/demo_002_spring_ai_chat_session
  3) 运行 SpringAiChatSessionApplication
  4) 浏览器 http://localhost:8102/

API：
  GET/POST /api/sessions
  GET  /api/sessions/{id}/messages
  POST /api/chat  {"question":"...","session_id":1}
  GET  /api/health
