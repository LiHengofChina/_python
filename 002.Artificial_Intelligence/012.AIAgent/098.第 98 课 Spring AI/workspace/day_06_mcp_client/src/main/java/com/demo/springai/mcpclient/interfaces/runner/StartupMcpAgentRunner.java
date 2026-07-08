package com.demo.springai.mcpclient.interfaces.runner;

import com.demo.springai.mcpclient.application.McpAgentApplicationService;
import com.demo.springai.mcpclient.domain.model.McpAgentReply;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.boot.CommandLineRunner;
import org.springframework.stereotype.Component;

@Component
public class StartupMcpAgentRunner implements CommandLineRunner {

    private final McpAgentApplicationService mcpAgentApplicationService;

    @Value("${demo.mcp-client.startup-enabled:true}")
    private boolean startupEnabled;

    @Value("${demo.mcp-client.startup-question:用一句话介绍什么是 Spring AI}")
    private String startupQuestion;

    @Value("${demo.mcp-client.filesystem-enabled:false}")
    private boolean filesystemEnabled;

    public StartupMcpAgentRunner(McpAgentApplicationService mcpAgentApplicationService) {
        this.mcpAgentApplicationService = mcpAgentApplicationService;
    }

    @Override
    public void run(String... args) {
        if (!startupEnabled) {
            return;
        }
        System.out.println("\n====== Spring AI MCP Client 启动示例 ======");
        System.out.println("MCP 连接：ops-server (8104)" +
                (filesystemEnabled ? " + filesystem（开源）" : ""));
        System.out.println("查看全部 Tool：GET http://localhost:8105/api/mcp-agent/tools");
        System.out.println("问题：" + startupQuestion);
        try {
            McpAgentReply reply = mcpAgentApplicationService.troubleshoot(startupQuestion);
            System.out.println("回答：" + reply.answer());
        } catch (Exception e) {
            System.err.println("调用失败：" + e.getMessage());
            System.err.println("请确认：1) MCP Server 已启动(8104)  2) Ollama 已启动");
        }
        System.out.println("==========================================\n");
    }
}
