# -*- coding: utf-8 -*-
from __future__ import annotations

from app.application.session import SessionApplicationService
from app.domain.model import AgentChatReply, ChatReply
from app.infrastructure.llm import OllamaAgentChatGateway

OPS_SYSTEM_PROMPT = """你是银行运维助手。排查问题时必须先调用可用工具获取事实，再给出结论和建议。
host_id 必须使用系统提示里「当前可用连接」的 label，原样填写，不要改写、不要加「机器」等后缀。
涉及重启、删除、变更等生产操作，必须提醒需要人工审批。"""


class AgentChatApplicationService:
    """应用层：带 Tool 的运维排查。"""

    def __init__(self, agent_gateway: OllamaAgentChatGateway) -> None:
        self._agent = agent_gateway

    def troubleshoot(self, question: str) -> AgentChatReply:
        answer = self._agent.chat_with_tools(OPS_SYSTEM_PROMPT, question)
        return AgentChatReply(question=question, answer=answer)


class ChatApplicationService:
    """应用层：对话 + 会话内带 Tool 的多轮对话。"""

    def __init__(
        self,
        agent_gateway: OllamaAgentChatGateway,
        session_service: SessionApplicationService,
    ) -> None:
        self._agent = agent_gateway
        self._sessions = session_service

    def chat(self, question: str) -> ChatReply:
        answer = self._agent.chat_with_tools(OPS_SYSTEM_PROMPT, question)
        return ChatReply(question=question, answer=answer)

    def chat_in_session(self, session_id: int, question: str) -> ChatReply:
        self._sessions.get_session(session_id)
        history = self._sessions.list_messages(session_id)
        recent = history[-20:]
        payload = [(m.role, m.content) for m in recent]
        payload.append(("user", question))

        answer = self._agent.chat_messages_with_tools(OPS_SYSTEM_PROMPT, payload)

        self._sessions.add_message(session_id, "user", question)
        self._sessions.add_message(session_id, "assistant", answer)
        return ChatReply(question=question, answer=answer)
