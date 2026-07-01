package com.demo.springai.chat.infrastructure.gateway;

import com.demo.springai.chat.domain.gateway.LlmChatGateway;
import org.springframework.ai.chat.client.ChatClient;
import org.springframework.stereotype.Component;

/**
 * 基础设施层：通过 Spring AI + Ollama 实现 {@link LlmChatGateway}。
 *
 * <p>LLM 调用细节（ChatClient、HTTP）封装在此，不泄漏到应用层/接口层。
 */
@Component
public class OllamaChatGateway implements LlmChatGateway {

    private final ChatClient chatClient;

    public OllamaChatGateway(ChatClient.Builder chatClientBuilder) {
        this.chatClient = chatClientBuilder.build();
    }

    @Override
    public String chat(String userMessage) {
        return chatClient
                .prompt()
                .user(userMessage)
                .call()
                .content();
    }

    @Override
    public String chatWithSystemRole(String systemPrompt, String userMessage) {
        return chatClient
                .prompt()
                .system(systemPrompt)
                .user(userMessage)
                .call()
                .content();
    }
}
