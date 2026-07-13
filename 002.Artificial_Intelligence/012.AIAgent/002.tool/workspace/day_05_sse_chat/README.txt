day_05_sse_chat — SSE 流式聊天（Cursor 风格过程展示）
从 day_04_connection_manager 复制并增强

相对 day_04 的变化：
  聊天默认走 POST /api/chat/stream（SSE）
  页面实时展示 Thinking / Calling model / Tool 开始与结束 / Answer
  发送按钮变为「进行中」，不再只是灰掉干等

事件类型（data: JSON）：
  status     — 进度文案（Thinking… / Calling model…）
  tool_start — 开始跑工具（name + args）
  tool_end   — 工具结束（preview）
  answer     — 最终回复
  done       — 会话已落库
  error      — 失败

保留：
  POST /api/chat 普通 HTTP（兼容）
  连接管理 / 会话 / Tool 逻辑同 day_04

步骤：
  1) pip install -r requirements.txt
  2) 先停掉占用 8101 的旧进程，再 python main.py
  3) 浏览器 http://127.0.0.1:8101/
  4) 连接管理维护 label → 聊天页提问，观察左侧过程卡片
