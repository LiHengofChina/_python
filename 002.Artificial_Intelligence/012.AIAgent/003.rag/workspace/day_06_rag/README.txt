day_06_rag — 文档管理 + Chroma RAG + Tool + SSE
从 day_05_sse_chat 复制并增强

对照 Java：
  day_03_spring_ai_rag / day_04_spring_ai_rag_tool
  → 聊天前检索向量库，把【参考资料】拼进 System Prompt，再调 LLM/Tool

功能：
  1) 左侧「文档管理」：上传/删除/列表 .txt
  2) 点「同步索引」：切块 → Embedding(nomic-embed-text) → Chroma
  3) 状态：pending / indexing / ready / failed
  4) 聊天 SSE：Retrieving knowledge… → Thinking… → Tool… → Answer

目录：
  data/uploads/   原始 txt
  data/chroma/    Chroma 持久化
  data/samples/ops_manual.txt  示例手册（可上传）

步骤：
  1) pip install -r requirements.txt
  2) ollama pull nomic-embed-text
  3) 停掉占用 8101 的旧进程，python main.py
  4) 文档管理上传 samples/ops_manual.txt → 同步索引
  5) 聊天问：磁盘使用率超过 85% 怎么办？
