package com.demo.springai.mcpclient.domain.gateway;

public interface McpAgentGateway {

    String chatWithMcpTools(String systemPrompt, String userMessage);
}
