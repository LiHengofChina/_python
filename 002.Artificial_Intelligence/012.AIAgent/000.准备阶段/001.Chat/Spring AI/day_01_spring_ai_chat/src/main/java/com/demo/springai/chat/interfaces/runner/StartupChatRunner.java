package com.demo.springai.chat.interfaces.runner;

import com.demo.springai.chat.application.ChatApplicationService;
import com.demo.springai.chat.domain.model.ChatReply;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.boot.CommandLineRunner;
import org.springframework.stereotype.Component;

/**
 * 【启动时的检测】
 * 接口层：启动时执行一次示例对话，验证 Ollama 连通。
 */
@Component
public class StartupChatRunner implements CommandLineRunner {

    private final ChatApplicationService chatApplicationService;

    @Value("${demo.chat.startup-enabled:true}")
    private boolean startupEnabled;

    @Value("${demo.chat.startup-question:你好}")
    private String startupQuestion;

    public StartupChatRunner(ChatApplicationService chatApplicationService) {
        this.chatApplicationService = chatApplicationService;
    }

    @Override
    public void run(String... args) {
        if (!startupEnabled) {
            return;
        }
        System.out.println("\n====== Spring AI Chat 启动示例 ======");
        System.out.println("问题：" + startupQuestion);
        try {
            ChatReply reply = chatApplicationService.chat(startupQuestion);
            System.out.println("回答：" + reply.answer());
        } catch (Exception e) {
            System.err.println("调用 Ollama 失败，请确认：");
            System.err.println("  1) Ollama 已启动");
            System.err.println("  2) 已执行 ollama pull qwen2.5:7b");
            System.err.println("  3) application.yml 中 base-url / model 正确");
            System.err.println("错误：" + e.getMessage());
        }
        System.out.println("====================================\n");
    }
}
