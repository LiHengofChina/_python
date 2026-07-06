package com.demo.springai.memory.interfaces.runner;

import com.demo.springai.memory.application.MemoryChatApplicationService;
import com.demo.springai.memory.domain.model.MemoryChatReply;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.boot.CommandLineRunner;
import org.springframework.stereotype.Component;

@Component
public class StartupMemoryRunner implements CommandLineRunner {

    private final MemoryChatApplicationService memoryChatApplicationService;

    @Value("${demo.memory.startup-enabled:true}")
    private boolean startupEnabled;

    @Value("${demo.memory.startup-conversation-id:demo-startup}")
    private String conversationId;

    public StartupMemoryRunner(MemoryChatApplicationService memoryChatApplicationService) {
        this.memoryChatApplicationService = memoryChatApplicationService;
    }

    @Override
    public void run(String... args) {
        if (!startupEnabled) {
            return;
        }
        System.out.println("\n====== Day08 Memory 多轮对话示例 ======");
        System.out.println("会话 ID：" + conversationId);
        try {
            String q1 = "我叫运维小张，请记住我的名字。";
            MemoryChatReply r1 = memoryChatApplicationService.chat(conversationId, q1);
            System.out.println("第1轮问：" + q1);
            System.out.println("第1轮答：" + r1.answer());

            String q2 = "我刚才说我叫什么？只回答名字。";
            MemoryChatReply r2 = memoryChatApplicationService.chat(conversationId, q2);
            System.out.println("第2轮问：" + q2);
            System.out.println("第2轮答：" + r2.answer());

            System.out.println("查看历史：GET http://localhost:8108/api/memory/history?cid=" + conversationId);
            System.out.println("聊天页：http://localhost:8108/");
        } catch (Exception e) {
            System.err.println("调用失败：" + e.getMessage());
            System.err.println("请确认 Ollama 已启动");
        }
        System.out.println("=====================================\n");
    }
}
