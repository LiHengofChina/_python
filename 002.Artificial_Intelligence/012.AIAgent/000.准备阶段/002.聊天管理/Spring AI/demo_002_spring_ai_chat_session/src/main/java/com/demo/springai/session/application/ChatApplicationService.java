package com.demo.springai.session.application;

import com.demo.springai.session.domain.gateway.LlmChatGateway;
import com.demo.springai.session.domain.model.ChatMessage;
import com.demo.springai.session.domain.model.ChatReply;
import org.springframework.stereotype.Service;

import java.util.ArrayList;
import java.util.List;

/**
 * 应用层：对话用例（调 LLM；会话内对话委托 Session）。
 */
@Service
public class ChatApplicationService {

    private final LlmChatGateway llmChatGateway;
    private final SessionApplicationService sessionService;

    public ChatApplicationService(
            LlmChatGateway llmChatGateway,
            SessionApplicationService sessionService) {
        this.llmChatGateway = llmChatGateway;
        this.sessionService = sessionService;
    }

    public ChatReply chat(String question) {
        return new ChatReply(question, llmChatGateway.chat(question));
    }

    public ChatReply chatInSession(long sessionId, String question) {
        sessionService.getSession(sessionId);

        List<ChatMessage> history = sessionService.listMessages(sessionId);
        // 只带最近 20 条，避免上下文过长
        int from = Math.max(0, history.size() - 20);
        List<String[]> payload = new ArrayList<>();
        for (ChatMessage m : history.subList(from, history.size())) {
            payload.add(new String[]{m.role(), m.content()});
        }
        payload.add(new String[]{"user", question});

        String answer = llmChatGateway.chatMessages(payload);

        sessionService.addMessage(sessionId, "user", question);
        sessionService.addMessage(sessionId, "assistant", answer);
        return new ChatReply(question, answer);
    }
}
