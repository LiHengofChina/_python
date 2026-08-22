package com.demo.springai.chat.interfaces.web;

/**
 * 聊天请求体（浏览器页面 POST /api/chat 使用）。
 */
public record ChatRequest(String question) {
}
