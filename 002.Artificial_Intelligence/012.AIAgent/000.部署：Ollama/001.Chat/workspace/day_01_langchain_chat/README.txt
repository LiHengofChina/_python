day_01_langchain_chat — LangChain + Ollama 纯聊天 Demo
位置：000.部署：Ollama / 001.Chat / workspace / day_01_langchain_chat
对标：098.第 98 课 Spring AI / workspace / day_01_spring_ai_chat

本课只用 LangChain（ChatOllama），不用 LangGraph / CrewAI。

对照关系：
  Spring AI ChatClient.prompt().user().call()
    ↔  LangChain ChatOllama.invoke([HumanMessage(...)])
  application.yml spring.ai.ollama.*
    ↔  config.local.yml ollama.*
  StartupChatRunner 启动示例
    ↔  python main.py [可选问题]

步骤：
  1) 本机 Ollama 已启动，且已 pull 模型（默认 qwen2.5:7b）
  2) copy config.example.yml → config.local.yml（已有则可跳过）
  3) pip install -r requirements.txt
  4) python main.py
  5) python main.py "你的问题"

可选：在代码里试 chat_with_system(system, user)，对标 Spring 的 chatWithSystemRole。
