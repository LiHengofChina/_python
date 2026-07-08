package com.demo.springai.memory.application;

import com.demo.springai.memory.domain.gateway.MemoryChatGateway;
import com.demo.springai.memory.domain.model.MemoryChatReply;
import org.springframework.ai.chat.memory.ChatMemory;
import org.springframework.ai.chat.messages.Message;
import org.springframework.stereotype.Service;

import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;
import java.util.stream.Collectors;

@Service
public class MemoryChatApplicationService {

    private final MemoryChatGateway memoryChatGateway;
    private final ChatMemory chatMemory;

    public MemoryChatApplicationService(MemoryChatGateway memoryChatGateway, ChatMemory chatMemory) {
        this.memoryChatGateway = memoryChatGateway;
        this.chatMemory = chatMemory;
    }

    public MemoryChatReply chat(String conversationId, String question) {
        String answer = memoryChatGateway.chat(conversationId, question);
        return new MemoryChatReply(conversationId, question, answer);
    }

    public List<Map<String, String>> listHistory(String conversationId) {
        return chatMemory.get(conversationId).stream()
                .map(this::toHistoryItem)
                .collect(Collectors.toList());
    }

    private Map<String, String> toHistoryItem(Message message) {
        Map<String, String> item = new LinkedHashMap<>();
        item.put("type", message.getMessageType().name());
        item.put("content", message.getText());
        return item;
    }
}
