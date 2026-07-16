package com.demo.springai.agent.application;

import com.demo.springai.agent.domain.gateway.AgentChatGateway;
import com.demo.springai.agent.domain.model.AgentChatReply;
import org.springframework.stereotype.Service;

@Service
public class AgentChatApplicationService {

    private static final String OPS_SYSTEM_PROMPT = """
            你是银行运维助手。排查问题时必须先调用可用工具获取事实，再给出结论和建议。
            涉及重启、删除、变更等生产操作，必须提醒需要人工审批。
            """;

    private final AgentChatGateway agentChatGateway;

    public AgentChatApplicationService(AgentChatGateway agentChatGateway) {
        this.agentChatGateway = agentChatGateway;
    }

    public AgentChatReply troubleshoot(String question) {
        String answer = agentChatGateway.chatWithTools(OPS_SYSTEM_PROMPT, question);
        return new AgentChatReply(question, answer);
    }
}
