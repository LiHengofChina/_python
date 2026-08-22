package com.demo.springai.session.domain.gateway;

import java.util.List;

/**
 * 领域网关：与大模型对话（支持多轮消息列表）。
 */
public interface LlmChatGateway {

    String chat(String userMessage);

    String chatWithSystemRole(String systemPrompt, String userMessage);

    /** messages: [role, content]，role = user|assistant|system */
    String chatMessages(List<String[]> messages);
}
