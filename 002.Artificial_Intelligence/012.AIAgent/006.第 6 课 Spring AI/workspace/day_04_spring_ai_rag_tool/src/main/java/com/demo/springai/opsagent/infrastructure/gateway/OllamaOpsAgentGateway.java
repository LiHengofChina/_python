package com.demo.springai.opsagent.infrastructure.gateway;

import com.demo.springai.opsagent.domain.gateway.OpsAgentGateway;
import com.demo.springai.opsagent.infrastructure.tool.OpsTools;
import org.springframework.ai.chat.client.ChatClient;
import org.springframework.ai.chat.client.advisor.vectorstore.QuestionAnswerAdvisor;
import org.springframework.ai.vectorstore.SearchRequest;
import org.springframework.ai.vectorstore.VectorStore;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Component;

/**
 * RAG + Tool 合体：QuestionAnswerAdvisor 检索手册，defaultTools 拉现场数据。
 */
@Component
public class OllamaOpsAgentGateway implements OpsAgentGateway {

    private final ChatClient chatClient;

    public OllamaOpsAgentGateway(
            ChatClient.Builder chatClientBuilder,
            VectorStore vectorStore,
            OpsTools opsTools,
            @Value("${demo.ops-agent.rag.top-k:3}") int topK,
            @Value("${demo.ops-agent.rag.similarity-threshold:0.5}") double similarityThreshold) {

        //构建RAG检索对象
        var ragAdvisor = QuestionAnswerAdvisor.builder(vectorStore)
                .searchRequest(SearchRequest.builder()
                        .topK(topK)
                        .similarityThreshold(similarityThreshold)
                        .build())
                .build();

        this.chatClient = chatClientBuilder
                .defaultAdvisors(ragAdvisor)
                .defaultTools(opsTools)
                .build();
    }

    @Override
    public String troubleshoot(String systemPrompt, String userMessage) {
        return chatClient
                .prompt()
                .system(systemPrompt)
                .user(userMessage)
                .call()
                .content();
    }
}
