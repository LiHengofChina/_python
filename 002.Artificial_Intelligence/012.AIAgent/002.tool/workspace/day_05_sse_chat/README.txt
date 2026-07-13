day_05_sse_chat — SSE 流式聊天（Cursor 风格过程展示）
从 day_04_connection_manager 复制并增强

相对 day_04 的变化：
  聊天默认走 POST /api/chat/stream（SSE）
  页面实时展示 Thinking / Tool 过程（完成后折叠为 Thought briefly）
  过程事件落库为 role=trace（JSON），刷新可还原；不喂给模型

事件类型（data: JSON）：
  status / tool_start / tool_end / answer / done / error

保留：
  POST /api/chat 普通 HTTP（兼容）
  连接管理 / 会话 / Tool 逻辑同 day_04

步骤：
  1) pip install -r requirements.txt
  2) 先停掉占用 8101 的旧进程，再 python main.py
  3) 浏览器 http://127.0.0.1:8101/
  4) 连接管理维护 label → 聊天页提问，观察过程卡片
