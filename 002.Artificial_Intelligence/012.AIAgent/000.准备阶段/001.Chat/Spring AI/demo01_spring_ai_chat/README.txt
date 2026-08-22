demo01_spring_ai_chat — Spring AI Chat（带浏览器页面，对标 LangChain demo01_langchain_chat）

目录：
  src/main/java/.../chat/
    domain/           领域模型 + 网关接口
    application/      ChatApplicationService
    infrastructure/   OllamaChatGateway
    interfaces/web/   REST + 健康检查
  src/main/resources/
    application.yml
    static/index.html   ← 浏览器聊天页

步骤：
  1) Ollama 已启动，已 pull qwen2.5:7b
  2) IDEA Open → 选 Spring AI/demo01_spring_ai_chat，运行 SpringAiChatApplication
  3) 浏览器打开 http://localhost:8102/

API：
  GET  /api/chat?q=你好
  POST /api/chat   {"question":"你好"}
  GET  /api/chat/ops?q=磁盘满了怎么办
  GET  /api/health
