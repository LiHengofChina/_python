# -*- coding: utf-8 -*-
import sys

from agent import run

DEFAULT_QUESTION = "Oracle 有一条 SQL 很慢，帮我按官方 Skill 流程定位原因"


def main() -> None:
    question = sys.argv[1] if len(sys.argv) > 1 else DEFAULT_QUESTION
    skill, messages = run(question)

    print("=== 框架 ===")
    print("LangChain + LangGraph")
    print("\n=== 开源 Skill ===")
    print(skill["meta"].get("name"), "← ../../skills/oracle/db/SKILL.md")
    print("来源: oracle/skills · db 域")
    print("\n=== 用户问题 ===")
    print(question)
    print("\n=== Agent 执行 ===\n")
    for msg in messages:
        content = getattr(msg, "content", "")
        if content:
            print(f"[{type(msg).__name__}]\n{content}\n")


if __name__ == "__main__":
    main()
