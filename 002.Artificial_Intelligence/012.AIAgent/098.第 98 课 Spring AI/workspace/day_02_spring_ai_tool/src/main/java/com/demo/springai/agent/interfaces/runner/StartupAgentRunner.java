package com.demo.springai.agent.interfaces.runner;

import com.demo.springai.agent.application.AgentChatApplicationService;
import com.demo.springai.agent.domain.model.AgentChatReply;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.boot.CommandLineRunner;
import org.springframework.stereotype.Component;

@Component
public class StartupAgentRunner implements CommandLineRunner {

    private final AgentChatApplicationService agentChatApplicationService;

    @Value("${demo.agent.startup-enabled:true}")
    private boolean startupEnabled;

    @Value("${demo.agent.startup-question:用一句话介绍什么是 Spring AI}")
    private String startupQuestion;

    public StartupAgentRunner(AgentChatApplicationService agentChatApplicationService) {
        this.agentChatApplicationService = agentChatApplicationService;
    }

    @Override
    public void run(String... args) {
        if (!startupEnabled) {
            return;
        }
        System.out.println("\n====== Spring AI Chat 启动示例 ======");
        System.out.println("问题：" + startupQuestion);
        try {
            AgentChatReply reply = agentChatApplicationService.troubleshoot(startupQuestion);
            System.out.println("回答：" + reply.answer());
        } catch (Exception e) {
            System.err.println("调用失败：" + e.getMessage());
        }
        System.out.println("====================================\n");
    }
}
