package com.demo.springai.memory.infrastructure.gateway;

import com.demo.springai.memory.domain.gateway.MemoryChatGateway;
import org.springframework.ai.chat.client.ChatClient;
import org.springframework.ai.chat.memory.ChatMemory;
import org.springframework.beans.factory.annotation.Qualifier;
import org.springframework.stereotype.Component;

@Component
public class OllamaMemoryChatGateway implements MemoryChatGateway {

    private static final String SYSTEM_PROMPT = """
            你是银行运维助手，支持多轮对话。
            请结合上下文回答；若用户之前说过自己的名字或偏好，要记住并引用。
            """;

    private final ChatClient memoryChatClient;

    public OllamaMemoryChatGateway(@Qualifier("memoryChatClient") ChatClient memoryChatClient) {
        this.memoryChatClient = memoryChatClient;
    }

    @Override
    public String chat(String conversationId, String userMessage) {
        return memoryChatClient
                .prompt()
                .system(SYSTEM_PROMPT)
                .user(userMessage)
                .advisors(a -> a.param(ChatMemory.CONVERSATION_ID, conversationId))
                .call()
                .content();
    }
}
