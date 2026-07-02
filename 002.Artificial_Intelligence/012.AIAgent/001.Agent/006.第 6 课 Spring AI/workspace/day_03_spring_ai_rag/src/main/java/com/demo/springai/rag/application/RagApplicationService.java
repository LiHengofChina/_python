package com.demo.springai.rag.application;

import com.demo.springai.rag.domain.gateway.RagChatGateway;
import com.demo.springai.rag.domain.model.RagReply;
import org.springframework.stereotype.Service;

@Service
public class RagApplicationService {

    private final RagChatGateway ragChatGateway;

    public RagApplicationService(RagChatGateway ragChatGateway) {
        this.ragChatGateway = ragChatGateway;
    }

    public RagReply ask(String question) {
        return ragChatGateway.ask(question);
    }
}
