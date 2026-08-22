package com.demo.springai.session.application;

import com.demo.springai.session.domain.model.ChatMessage;
import com.demo.springai.session.domain.model.ChatSession;
import com.demo.springai.session.infrastructure.persistence.ChatStore;
import org.springframework.stereotype.Service;

import java.util.List;

/**
 * 应用层：会话/消息管理（不调用 LLM）。
 */
@Service
public class SessionApplicationService {

    private final ChatStore store;

    public SessionApplicationService(ChatStore store) {
        this.store = store;
    }

    public ChatSession createSession(String title) {
        return store.createSession(title);
    }

    public List<ChatSession> listSessions() {
        return store.listSessions();
    }

    public ChatSession getSession(long sessionId) {
        return store.getSession(sessionId)
                .orElseThrow(() -> new IllegalArgumentException("会话不存在: " + sessionId));
    }

    public List<ChatMessage> listMessages(long sessionId) {
        getSession(sessionId);
        return store.listMessages(sessionId);
    }

    public ChatMessage addMessage(long sessionId, String role, String content) {
        getSession(sessionId);
        return store.addMessage(sessionId, role, content);
    }
}
