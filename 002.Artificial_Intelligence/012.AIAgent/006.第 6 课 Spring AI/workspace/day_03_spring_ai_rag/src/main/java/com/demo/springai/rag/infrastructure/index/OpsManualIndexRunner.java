package com.demo.springai.rag.infrastructure.index;

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

/**
 * 启动时：加载运维手册 → 切块 → Embedding → 写入向量库。
 *
 * <p>对应 Python day_29 的步骤 ①②③。
 */
@Component
@Order(1)
public class OpsManualIndexRunner implements CommandLineRunner {

    private static final Logger log = LoggerFactory.getLogger(OpsManualIndexRunner.class);

    private final VectorStore vectorStore;

    @Value("${demo.rag.manual-path}")
    private Resource manualResource;

    public OpsManualIndexRunner(VectorStore vectorStore) {
        this.vectorStore = vectorStore;
    }

    @Override
    public void run(String... args) {
        log.info("RAG 索引开始：{}", manualResource.getFilename());
        TextReader reader = new TextReader(manualResource);
        reader.getCustomMetadata().put("source", "ops_manual");

        List<Document> documents = reader.read();
        TokenTextSplitter splitter = new TokenTextSplitter();
        List<Document> chunks = splitter.apply(documents);

        vectorStore.add(chunks);
        log.info("RAG 索引完成：原文 {} 段，切块 {} 段", documents.size(), chunks.size());
    }
}
