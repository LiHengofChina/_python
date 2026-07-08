package com.demo.springai.orchestration.interfaces.runner;

import org.springframework.ai.chat.client.ChatClient;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.boot.CommandLineRunner;
import org.springframework.core.annotation.Order;
import org.springframework.stereotype.Component;

@Component
@Order(2)
public class StartupOrchestrationRunner implements CommandLineRunner {

    private final ChatClient chatClient;

    @Value("${demo.orchestration.startup-enabled:true}")
    private boolean startupEnabled;

    @Value("${demo.orchestration.startup-question:用一句话介绍什么是 Spring AI}")
    private String startupQuestion;

    public StartupOrchestrationRunner(ChatClient.Builder chatClientBuilder) {
        this.chatClient = chatClientBuilder.build();
    }

    @Override
    public void run(String... args) {
        if (!startupEnabled) {
            return;
        }
        System.out.println("\n====== Spring AI 编排 启动示例 ======");
        System.out.println("问题：" + startupQuestion);
        try {
            String answer = chatClient.prompt().user(startupQuestion).call().content();
            System.out.println("回答：" + answer);
        } catch (Exception e) {
            System.err.println("调用失败：" + e.getMessage());
        }
        System.out.println("====================================\n");
    }
}
