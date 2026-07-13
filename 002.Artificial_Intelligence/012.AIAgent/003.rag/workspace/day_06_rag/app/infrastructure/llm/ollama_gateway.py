# -*- coding: utf-8 -*-
"""基础设施：LangChain ChatOllama（支持多轮消息）。"""
from __future__ import annotations

from langchain_core.messages import AIMessage, BaseMessage, HumanMessage, SystemMessage
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
        return self.chat_messages([("user", user_message)])

    def chat_with_system(self, system_prompt: str, user_message: str) -> str:
        return self.chat_messages(
            [("system", system_prompt), ("user", user_message)]
        )

    def chat_messages(self, messages: list[tuple[str, str]]) -> str:
        """messages: [(role, content), ...] role = user|assistant|system"""
        lc_msgs: list[BaseMessage] = []
        for role, content in messages:
            if role == "system":
                lc_msgs.append(SystemMessage(content=content))
            elif role == "assistant":
                lc_msgs.append(AIMessage(content=content))
            else:
                lc_msgs.append(HumanMessage(content=content))
        resp = self._llm.invoke(lc_msgs)
        return str(resp.content)
