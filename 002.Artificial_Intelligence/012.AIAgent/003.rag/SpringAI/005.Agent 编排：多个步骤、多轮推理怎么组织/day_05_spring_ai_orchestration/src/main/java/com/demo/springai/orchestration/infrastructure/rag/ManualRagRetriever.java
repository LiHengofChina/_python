package com.demo.springai.orchestration.infrastructure.rag;

import org.springframework.ai.document.Document;
import org.springframework.ai.vectorstore.SearchRequest;
import org.springframework.ai.vectorstore.VectorStore;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.stereotype.Component;

import java.util.List;
import java.util.stream.Collectors;

@Component
public class ManualRagRetriever {

    private final VectorStore vectorStore;
    private final int topK;

    public ManualRagRetriever(
            VectorStore vectorStore,
            @Value("${demo.orchestration.rag.top-k:3}") int topK) {
        this.vectorStore = vectorStore;
        this.topK = topK;
    }

    public String retrieve(String question) {
        List<Document> docs = vectorStore.similaritySearch(
                SearchRequest.builder().query(question).topK(topK).build());
        if (docs.isEmpty()) {
            return "（未检索到相关手册段落）";
        }
        return docs.stream()
                .map(Document::getText)
                .collect(Collectors.joining("\n---\n"));
    }
}
