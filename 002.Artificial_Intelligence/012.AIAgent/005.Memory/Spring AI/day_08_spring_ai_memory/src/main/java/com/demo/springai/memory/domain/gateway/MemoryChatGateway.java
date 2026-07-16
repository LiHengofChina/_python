package com.demo.springai.memory.domain.gateway;

public interface MemoryChatGateway {

    String chat(String conversationId, String userMessage);
}
