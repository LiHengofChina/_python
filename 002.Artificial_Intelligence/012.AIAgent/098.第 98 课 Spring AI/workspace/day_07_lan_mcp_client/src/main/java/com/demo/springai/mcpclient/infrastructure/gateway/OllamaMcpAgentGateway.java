package com.demo.springai.mcpclient.infrastructure.gateway;

import com.demo.springai.mcpclient.domain.gateway.McpAgentGateway;
import org.springframework.ai.chat.client.ChatClient;
import org.springframework.ai.tool.ToolCallbackProvider;
import org.springframework.stereotype.Component;

@Component
public class OllamaMcpAgentGateway implements McpAgentGateway {

    private final ChatClient chatClient;

    public OllamaMcpAgentGateway(
            ChatClient.Builder chatClientBuilder,
            ToolCallbackProvider mcpToolCallbackProvider) {
        this.chatClient = chatClientBuilder
                .defaultToolCallbacks(mcpToolCallbackProvider)
                .build();
    }

    @Override
    public String chatWithMcpTools(String systemPrompt, String userMessage) {
        return chatClient
                .prompt()
                .system(systemPrompt)
                .user(userMessage)
                .call()
                .content();
    }
}
