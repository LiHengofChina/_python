package com.demo.springai.agent.infrastructure.gateway;

import com.demo.springai.agent.domain.gateway.AgentChatGateway;
import com.demo.springai.agent.infrastructure.tool.OpsTools;
import org.springframework.ai.chat.client.ChatClient;
import org.springframework.stereotype.Component;

/**
 * 通过 Spring AI ChatClient 注册 Tool，由模型决定是否调用。
 */
@Component
public class OllamaAgentChatGateway implements AgentChatGateway {

    private final ChatClient chatClient;

    public OllamaAgentChatGateway(ChatClient.Builder chatClientBuilder, OpsTools opsTools) {
        // defaultTools：把 OpsTools 里带 @Tool 的方法注册给模型
        this.chatClient = chatClientBuilder.defaultTools(opsTools).build();
    }

    @Override
    public String chatWithTools(String systemPrompt, String userMessage) {
        return chatClient
                .prompt()
                .system(systemPrompt)
                .user(userMessage)
                .call()
                .content();
    }
}
