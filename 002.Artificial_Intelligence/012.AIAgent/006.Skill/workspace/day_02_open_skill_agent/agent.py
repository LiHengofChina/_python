from pathlib import Path

import yaml
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_ollama import ChatOllama
from langgraph.prebuilt import create_react_agent

from ops_tools import tools_for_skill
from skill_loader import load_skill_package, skill_to_system_prompt

BASE_DIR = Path(__file__).resolve().parent
CONFIG_PATH = BASE_DIR / "config.local.yml"
SKILL_DIR = BASE_DIR.parents[1] / "skills" / "openocta" / "mysql_inspect"


def _load_model() -> str:
    if CONFIG_PATH.exists():
        cfg = yaml.safe_load(CONFIG_PATH.read_text(encoding="utf-8")) or {}
        return cfg.get("ollama", {}).get("model", "qwen2.5:7b")
    return "qwen2.5:7b"


def build_skill_agent(skill_dir: Path | None = None):
    path = skill_dir or SKILL_DIR
    skill = load_skill_package(path)
    system = skill_to_system_prompt(skill)
    tools = tools_for_skill(skill["meta"], path)
    if not tools:
        raise ValueError(f"Skill 未声明 tools，请检查 adapter.yaml: {path}")

    llm = ChatOllama(
        model=_load_model(),
        temperature=0,
        client_kwargs={"trust_env": False},
    )
    agent = create_react_agent(llm, tools)
    return agent, system, skill


def run(question: str, skill_dir: Path | None = None) -> tuple:
    agent, system, skill = build_skill_agent(skill_dir)
    result = agent.invoke(
        {
            "messages": [
                SystemMessage(content=system),
                HumanMessage(content=question),
            ]
        }
    )
    return skill, result["messages"]
