# -*- coding: utf-8 -*-
"""对标 Spring AI 的 OllamaChatGateway：用 LangChain ChatOllama 调本地模型。"""
from __future__ import annotations

from pathlib import Path

import yaml
from langchain_core.messages import HumanMessage, SystemMessage
from langchain_ollama import ChatOllama

BASE_DIR = Path(__file__).resolve().parent
CONFIG_PATH = BASE_DIR / "config.local.yml"


def load_config() -> dict:
    if not CONFIG_PATH.exists():
        example = BASE_DIR / "config.example.yml"
        raise FileNotFoundError(
            f"缺少 {CONFIG_PATH.name}，请先复制 {example.name} 为 config.local.yml"
        )
    return yaml.safe_load(CONFIG_PATH.read_text(encoding="utf-8")) or {}


def build_llm(cfg: dict | None = None) -> ChatOllama:
    cfg = cfg or load_config()
    ora = cfg.get("ollama", {})
    return ChatOllama(
        base_url=ora.get("base_url", "http://127.0.0.1:11434"),
        model=ora.get("model", "qwen2.5:7b"),
        temperature=float(ora.get("temperature", 0.3)),
        client_kwargs={"trust_env": False},
    )


def chat(user_message: str, llm: ChatOllama | None = None) -> str:
    """纯用户消息对话。"""
    llm = llm or build_llm()
    resp = llm.invoke([HumanMessage(content=user_message)])
    return str(resp.content)


def chat_with_system(system_prompt: str, user_message: str, llm: ChatOllama | None = None) -> str:
    """带 system 角色的对话。"""
    llm = llm or build_llm()
    resp = llm.invoke(
        [
            SystemMessage(content=system_prompt),
            HumanMessage(content=user_message),
        ]
    )
    return str(resp.content)
