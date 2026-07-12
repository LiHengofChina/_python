# -*- coding: utf-8 -*-
import sys

from agent import run

DEFAULT_QUESTION = "linux-231 磁盘满了，帮我排查一下"


def main() -> None:
    question = sys.argv[1] if len(sys.argv) > 1 else DEFAULT_QUESTION
    skill, messages = run(question)

    print("=== 框架 ===")
    print("LangChain + LangGraph")
    print("\n=== 加载的 Skill ===")
    print(skill["meta"]["name"], "← ../../skills/disk_alert/SKILL.md")
    print("\n=== 用户问题 ===")
    print(question)
    print("\n=== Agent 执行 ===\n")
    for msg in messages:
        content = getattr(msg, "content", "")
        if content:
            print(f"[{type(msg).__name__}]\n{content}\n")


if __name__ == "__main__":
    main()
