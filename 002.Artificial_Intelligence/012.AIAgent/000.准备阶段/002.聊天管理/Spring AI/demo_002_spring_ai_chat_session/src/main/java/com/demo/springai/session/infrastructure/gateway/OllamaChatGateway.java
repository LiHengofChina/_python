package com.demo.springai.session.infrastructure.gateway;

import com.demo.springai.session.domain.gateway.LlmChatGateway;
import org.springframework.ai.chat.client.ChatClient;
import org.springframework.ai.chat.messages.AssistantMessage;
import org.springframework.ai.chat.messages.Message;
import org.springframework.ai.chat.messages.SystemMessage;
import org.springframework.ai.chat.messages.UserMessage;
import org.springframework.stereotype.Component;

import java.util.ArrayList;
import java.util.List;

/**
 * Spring AI + Ollama 实现多轮对话。
 */
@Component
public class OllamaChatGateway implements LlmChatGateway {

    private final ChatClient chatClient;

    public OllamaChatGateway(ChatClient.Builder chatClientBuilder) {
        this.chatClient = chatClientBuilder.build();
    }

    @Override
    public String chat(String userMessage) {
        return chatMessages(List.<String[]>of(new String[]{"user", userMessage}));
    }

    @Override
    public String chatWithSystemRole(String systemPrompt, String userMessage) {
        return chatMessages(List.<String[]>of(
                new String[]{"system", systemPrompt},
                new String[]{"user", userMessage}
        ));
    }

    @Override
    public String chatMessages(List<String[]> messages) {
        List<Message> lc = new ArrayList<>();
        for (String[] m : messages) {
            String role = m[0];
            String content = m[1];
            if ("system".equals(role)) {
                lc.add(new SystemMessage(content));
            } else if ("assistant".equals(role)) {
                lc.add(new AssistantMessage(content));
            } else {
                lc.add(new UserMessage(content));
            }
        }
        return chatClient.prompt().messages(lc).call().content();
    }
}
