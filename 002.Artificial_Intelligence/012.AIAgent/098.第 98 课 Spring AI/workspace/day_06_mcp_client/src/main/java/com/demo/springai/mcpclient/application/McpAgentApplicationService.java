package com.demo.springai.mcpclient.application;

import com.demo.springai.mcpclient.domain.gateway.McpAgentGateway;
import com.demo.springai.mcpclient.domain.model.McpAgentReply;
import org.springframework.stereotype.Service;

@Service
public class McpAgentApplicationService {

    private static final String OPS_SYSTEM_PROMPT = """
            你是银行运维助手。排查问题时必须通过 MCP 工具获取现场数据，再给出结论。
            工具由远程 MCP Server 提供（与 day_02 本地 Tool 能力相同，但走 MCP 协议）。
            涉及重启、删除、变更等生产操作，必须提醒需要人工审批。
            """;

    private final McpAgentGateway mcpAgentGateway;

    public McpAgentApplicationService(McpAgentGateway mcpAgentGateway) {
        this.mcpAgentGateway = mcpAgentGateway;
    }

    public McpAgentReply troubleshoot(String question) {
        String answer = mcpAgentGateway.chatWithMcpTools(OPS_SYSTEM_PROMPT, question);
        return new McpAgentReply(question, answer);
    }
}
