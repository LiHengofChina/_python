day_03_langchain_tool — Python Tool Demo
对标：098 / day_02_spring_ai_tool
复制自：002.聊天管理 / day_02_chat_session，再增加 SSH Tool

对照：
  Spring @Tool OpsTools          ↔  LangChain @tool build_ops_tools
  ChatClient.defaultTools(...)   ↔  LangGraph create_react_agent(llm, tools)
  LinuxSshExecutor               ↔  infrastructure/ssh/LinuxSshExecutor
  GET /api/agent/troubleshoot    ↔  同路径

目录要点：
  app/infrastructure/tool/     4 个运维 Tool（磁盘/内存/进程/日志目录）
  app/infrastructure/ssh/      只读命令白名单 + paramiko
  app/infrastructure/llm/      OllamaAgentChatGateway（带 Tool）
  app/application/             Session + Chat/Agent 用例
  端口：8101（同时只跑一个 Demo）

步骤：
  1) 确认 Ollama 与 192.168.100.231 SSH 可达
  2) 编辑 config.local.yml 的 ssh.password
  3) pip install -r requirements.txt
  4) python main.py
  5) 浏览器 http://127.0.0.1:8101/
     或 GET /api/agent/troubleshoot?q=linux-231磁盘满了帮我排查
