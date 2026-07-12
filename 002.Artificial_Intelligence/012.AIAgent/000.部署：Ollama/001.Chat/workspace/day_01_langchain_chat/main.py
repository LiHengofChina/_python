# -*- coding: utf-8 -*-
"""
day_01 LangChain Chat — 对标 Spring AI day_01_spring_ai_chat

用法：
  pip install -r requirements.txt
  # 确认 Ollama 已启动，且已 pull 模型：ollama pull qwen2.5:7b
  python main.py
  python main.py "你好，用一句话介绍 Ollama"
"""
from __future__ import annotations

import sys

from chat import chat, load_config


def main() -> None:
    cfg = load_config()
    question = (
        sys.argv[1]
        if len(sys.argv) > 1
        else cfg.get("demo", {}).get("question", "你好")
    )
    ora = cfg.get("ollama", {})

    print("=== 框架 ===")
    print("LangChain + ChatOllama")
    print("\n=== Ollama ===")
    print(f"base_url: {ora.get('base_url')}")
    print(f"model:    {ora.get('model')}")
    print("\n=== 用户问题 ===")
    print(question)
    print("\n=== 模型回答 ===")
    try:
        answer = chat(question)
        print(answer)
    except Exception as e:
        print("调用 Ollama 失败，请确认：")
        print("  1) Ollama 已启动")
        print(f"  2) 已执行 ollama pull {ora.get('model', 'qwen2.5:7b')}")
        print("  3) config.local.yml 中 base_url / model 正确")
        print(f"错误：{e}")
        raise SystemExit(1) from e


if __name__ == "__main__":
    main()
