package com.demo.springai.opsagent.interfaces.runner;

import com.demo.springai.opsagent.application.OpsAgentApplicationService;
import com.demo.springai.opsagent.domain.model.OpsAgentReply;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.boot.CommandLineRunner;
import org.springframework.core.annotation.Order;
import org.springframework.stereotype.Component;

@Component
@Order(2)
public class StartupOpsAgentRunner implements CommandLineRunner {

    private final OpsAgentApplicationService opsAgentApplicationService;

    @Value("${demo.ops-agent.startup-enabled:true}")
    private boolean startupEnabled;

    @Value("${demo.ops-agent.startup-question:用一句话介绍什么是 Spring AI}")
    private String startupQuestion;

    public StartupOpsAgentRunner(OpsAgentApplicationService opsAgentApplicationService) {
        this.opsAgentApplicationService = opsAgentApplicationService;
    }

    @Override
    public void run(String... args) {
        if (!startupEnabled) {
            return;
        }
        System.out.println("\n====== Spring AI RAG+Tool 启动示例 ======");
        System.out.println("问题：" + startupQuestion);
        try {
            OpsAgentReply reply = opsAgentApplicationService.troubleshoot(startupQuestion);
            System.out.println("回答：" + reply.answer());
        } catch (Exception e) {
            System.err.println("调用失败：" + e.getMessage());
            System.err.println("请确认 Ollama 已启动，且已 pull qwen2.5:7b 与 nomic-embed-text");
        }
        System.out.println("====================================\n");
    }
}
