from pathlib import Path

import yaml


def load_skill(skill_md: Path) -> dict:
    text = skill_md.read_text(encoding="utf-8")
    if not text.startswith("---"):
        return {"meta": {}, "body": text.strip()}
    _, front, body = text.split("---", 2)
    meta = yaml.safe_load(front) or {}
    return {"meta": meta, "body": body.strip()}


def skill_to_system_prompt(skill: dict) -> str:
    meta = skill["meta"]
    header = (
        f"你正在执行 Skill：{meta.get('name', 'unknown')}\n"
        f"可用 Tool：{meta.get('tools', '')}\n"
        "请严格按下面 SOP 执行；需要数据时调用 Tool；危险操作只给方案，末尾写「需人工审批」。\n"
    )
    return header + "\n" + skill["body"]
