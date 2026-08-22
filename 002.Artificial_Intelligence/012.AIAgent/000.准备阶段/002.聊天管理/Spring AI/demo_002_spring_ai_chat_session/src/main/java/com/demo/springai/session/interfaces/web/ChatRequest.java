package com.demo.springai.session.interfaces.web;

import com.fasterxml.jackson.annotation.JsonProperty;

/**
 * 聊天请求。session_id 与 Python 前端字段对齐。
 */
public record ChatRequest(
        String question,
        @JsonProperty("session_id") Long sessionId
) {
}
