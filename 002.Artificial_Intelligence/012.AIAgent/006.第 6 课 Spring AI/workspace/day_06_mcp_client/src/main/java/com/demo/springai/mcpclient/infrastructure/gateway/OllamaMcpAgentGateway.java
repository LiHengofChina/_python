package com.demo.springai.mcpclient.infrastructure.gateway;

import com.demo.springai.mcpclient.domain.gateway.McpAgentGateway;
import org.springframework.ai.chat.client.ChatClient;
import org.springframework.ai.tool.ToolCallbackProvider;
import org.springframework.stereotype.Component;

/**
 * 通过 MCP Client 自动发现的 Tool 调用远程 MCP Server。
 *
 * <p>对比 day_02：day_02 用 defaultTools(opsTools) 本地注册；
 * 本课用 defaultToolCallbacks(mcpTools) 从 MCP Server 拉取 Tool 列表。
 */
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
