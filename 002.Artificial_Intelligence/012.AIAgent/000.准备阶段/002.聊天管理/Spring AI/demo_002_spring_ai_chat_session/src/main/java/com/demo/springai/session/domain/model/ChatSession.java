package com.demo.springai.session.domain.model;

/**
 * 会话档案。
 */
public record ChatSession(long id, long userId, String title, String createdAt) {
}
