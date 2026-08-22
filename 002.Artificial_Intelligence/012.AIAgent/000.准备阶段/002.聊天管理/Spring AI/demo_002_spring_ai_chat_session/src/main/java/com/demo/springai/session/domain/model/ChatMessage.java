package com.demo.springai.session.domain.model;

/**
 * 会话内一条消息。role = user | assistant | system
 */
public record ChatMessage(long id, long sessionId, String role, String content, String createdAt) {
}
