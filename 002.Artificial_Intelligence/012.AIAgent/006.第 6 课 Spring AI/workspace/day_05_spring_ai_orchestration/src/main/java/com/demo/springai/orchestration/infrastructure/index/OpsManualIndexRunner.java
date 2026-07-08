package com.demo.springai.orchestration.infrastructure.index;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.ai.document.Document;
import org.springframework.ai.reader.TextReader;
import org.springframework.ai.transformer.splitter.TokenTextSplitter;
import org.springframework.ai.vectorstore.VectorStore;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.boot.CommandLineRunner;
import org.springframework.core.annotation.Order;
import org.springframework.core.io.Resource;
import org.springframework.stereotype.Component;

import java.util.List;

@Component
@Order(1)
public class OpsManualIndexRunner implements CommandLineRunner {

    private static final Logger log = LoggerFactory.getLogger(OpsManualIndexRunner.class);

    private final VectorStore vectorStore;

    @Value("${demo.orchestration.rag.manual-path}")
    private Resource manualResource;

    public OpsManualIndexRunner(VectorStore vectorStore) {
        this.vectorStore = vectorStore;
    }

    @Override
    public void run(String... args) {
        log.info("RAG 索引开始：{}", manualResource.getFilename());
        TextReader reader = new TextReader(manualResource);
        reader.getCustomMetadata().put("source", "ops_manual");
        List<Document> chunks = new TokenTextSplitter().apply(reader.read());
        vectorStore.add(chunks);
        log.info("RAG 索引完成：切块 {} 段", chunks.size());
    }
}
