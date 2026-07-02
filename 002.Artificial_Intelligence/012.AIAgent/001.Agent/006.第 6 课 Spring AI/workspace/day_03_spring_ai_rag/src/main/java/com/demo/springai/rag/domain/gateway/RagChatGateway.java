package com.demo.springai.rag.domain.gateway;

import com.demo.springai.rag.domain.model.RagReply;

public interface RagChatGateway {

    RagReply ask(String question);
}
