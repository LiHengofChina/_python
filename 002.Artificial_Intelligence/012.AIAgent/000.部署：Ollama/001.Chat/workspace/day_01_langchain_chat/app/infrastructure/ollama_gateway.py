# -*- coding: utf-8 -*-
"""基础设施：LangChain ChatOllama（对标 OllamaChatGateway）。"""
from __future__ import annotations

from langchain_core.messages import HumanMessage, SystemMessage
from langchain_ollama import ChatOllama

from app.infrastructure.config import load_config


class OllamaChatGateway:
    def __init__(self, cfg: dict | None = None) -> None:
        cfg = cfg or load_config()
        ora = cfg.get("ollama", {})
        self._llm = ChatOllama(
            base_url=ora.get("base_url", "http://127.0.0.1:11434"),
            model=ora.get("model", "qwen2.5:7b"),
            temperature=float(ora.get("temperature", 0.3)),
            client_kwargs={"trust_env": False},
        )

    def chat(self, user_message: str) -> str:
        resp = self._llm.invoke([HumanMessage(content=user_message)])
        return str(resp.content)

    def chat_with_system(self, system_prompt: str, user_message: str) -> str:
        resp = self._llm.invoke(
            [
                SystemMessage(content=system_prompt),
                HumanMessage(content=user_message),
            ]
        )
        return str(resp.content)
