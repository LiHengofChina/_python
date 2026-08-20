day_01_langchain_chat — FastAPI Web 聊天（对标 Spring AI day_01）

目录（轻量 DDD，对标 Java 分层）：
  app/domain/           领域模型 + 端口（gateway Protocol）
  app/application/      用例编排 ChatApplicationService
  app/infrastructure/   OllamaChatGateway、读配置
  app/interfaces/web/   FastAPI 路由 + static/ 简单聊天页
  main.py               启动 uvicorn
  config.local.yml      端口 / 模型

前后端：
  现阶段同仓，不拆两个仓库。
  后端：FastAPI（/api/chat）
  前端：app/interfaces/web/static/index.html（浏览器页面）
  以后前端变复杂再拆 Vue/React 独立项目。

步骤：
  1) Ollama 已启动，已 pull qwen2.5:7b
  2) pip install -r requirements.txt
  3) python main.py
  4) 浏览器打开 http://127.0.0.1:8101/

API（对标 Spring）：
  GET  /api/chat?q=你好
  POST /api/chat   {"question":"你好"}
  GET  /api/chat/ops?q=磁盘满了怎么办
  GET  /api/health
