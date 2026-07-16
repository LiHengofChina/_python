package com.demo.springai.rag.infrastructure.gateway;

import com.demo.springai.rag.domain.gateway.RagChatGateway;
import com.demo.springai.rag.domain.model.RagReply;
import org.springframework.ai.chat.client.ChatClient;
import org.springframework.ai.chat.client.advisor.vectorstore.QuestionAnswerAdvisor;
import org.springframework.ai.vectorstore.SearchRequest;
import org.springframework.ai.vectorstore.VectorStore;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Component;

/**
 * RAG 实现：QuestionAnswerAdvisor 自动检索向量库并拼进 Prompt。
 */
@Component
public class OllamaRagChatGateway implements RagChatGateway {

    private final ChatClient chatClient;

    public OllamaRagChatGateway(
            ChatClient.Builder chatClientBuilder,
            VectorStore vectorStore,
            @Value("${demo.rag.top-k:3}") int topK,
            @Value("${demo.rag.similarity-threshold:0.5}") double similarityThreshold) {

        var advisor = QuestionAnswerAdvisor.builder(vectorStore)
                .searchRequest(SearchRequest.builder()
                        .topK(topK)
                        .similarityThreshold(similarityThreshold)
                        .build())
                .build();

        this.chatClient = chatClientBuilder
                .defaultAdvisors(advisor)
                .build();
    }

    @Override
    public RagReply ask(String question) {
        String answer = chatClient
                .prompt()
                .system("""
                        你是银行运维助手。请严格根据检索到的参考资料回答。
                        若资料中没有相关内容，请明确说「资料中未找到」。
                        """)
                .user(question)
                .call()
                .content();
        return new RagReply(question, answer);
    }
}
