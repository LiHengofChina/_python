package com.demo.springai.rag.interfaces.runner;

import com.demo.springai.rag.application.RagApplicationService;
import com.demo.springai.rag.domain.model.RagReply;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.boot.CommandLineRunner;
import org.springframework.core.annotation.Order;
import org.springframework.stereotype.Component;

/**
 * 在文档索引完成后执行一次 RAG 示例问答。
 */
@Component
@Order(2)
public class StartupRagRunner implements CommandLineRunner {

    private final RagApplicationService ragApplicationService;

    @Value("${demo.rag.startup-enabled:true}")
    private boolean startupEnabled;

    @Value("${demo.rag.startup-question:用一句话介绍什么是 Spring AI}")
    private String startupQuestion;

    public StartupRagRunner(RagApplicationService ragApplicationService) {
        this.ragApplicationService = ragApplicationService;
    }

    @Override
    public void run(String... args) {
        if (!startupEnabled) {
            return;
        }
        System.out.println("\n====== Spring AI RAG 启动示例 ======");
        System.out.println("问题：" + startupQuestion);
        try {
            RagReply reply = ragApplicationService.ask(startupQuestion);
            System.out.println("回答：" + reply.answer());
        } catch (Exception e) {
            System.err.println("RAG 调用失败：" + e.getMessage());
            System.err.println("请确认已执行：ollama pull nomic-embed-text");
        }
        System.out.println("====================================\n");
    }
}
