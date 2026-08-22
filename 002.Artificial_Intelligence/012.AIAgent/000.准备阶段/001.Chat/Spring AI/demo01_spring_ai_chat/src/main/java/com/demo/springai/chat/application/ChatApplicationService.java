package com.demo.springai.chat.application;

import com.demo.springai.chat.domain.gateway.LlmChatGateway;
import com.demo.springai.chat.domain.model.ChatReply;
import org.springframework.stereotype.Service;

/**
 * 应用层：编排对话用例，不含 HTTP 与 ChatClient 细节。
 */
@Service
public class ChatApplicationService {

    private final LlmChatGateway llmChatGateway;

    public ChatApplicationService(LlmChatGateway llmChatGateway) {
        this.llmChatGateway = llmChatGateway;
    }

    public ChatReply chat(String question) {
        String answer = llmChatGateway.chat(question);
        return new ChatReply(question, answer);
    }

    public ChatReply chatWithSystemRole(String systemPrompt, String question) {
        String answer = llmChatGateway.chatWithSystemRole(systemPrompt, question);
        return new ChatReply(question, answer);
    }
}
