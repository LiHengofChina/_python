# -*- coding: utf-8 -*-
import sys

from agent import run

DEFAULT_QUESTION = "对 MySQL 做一次全维度健康巡检，给出巡检报告"


def main() -> None:
    question = sys.argv[1] if len(sys.argv) > 1 else DEFAULT_QUESTION
    skill, messages = run(question)

    print("=== 框架 ===")
    print("LangChain + LangGraph")
    print("\n=== 开源 Skill ===")
    print(skill["meta"].get("name"), "← ../../skills/openocta/mysql_inspect/SKILL.md")
    print("来源: openocta/openocta_skills · MySQL数据库巡检")
    print("\n=== 用户问题 ===")
    print(question)
    print("\n=== Agent 执行 ===\n")
    for msg in messages:
        content = getattr(msg, "content", "")
        if content:
            print(f"[{type(msg).__name__}]\n{content}\n")


if __name__ == "__main__":
    main()
