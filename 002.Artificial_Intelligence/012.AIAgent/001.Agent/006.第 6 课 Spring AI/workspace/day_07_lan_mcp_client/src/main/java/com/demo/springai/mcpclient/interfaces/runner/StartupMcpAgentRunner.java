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

    @Value("${demo.mcp-client.startup-question:查一下 linux-231 磁盘使用情况}")
    private String startupQuestion;

    @Value("${demo.mcp-client.ops-server-url:http://127.0.0.1:8104}")
    private String opsServerUrl;

    @Value("${demo.mcp-client.filesystem-url:http://127.0.0.1:8106/sse}")
    private String filesystemUrl;

    public StartupMcpAgentRunner(McpAgentApplicationService mcpAgentApplicationService) {
        this.mcpAgentApplicationService = mcpAgentApplicationService;
    }

    @Override
    public void run(String... args) {
        if (!startupEnabled) {
            return;
        }
        System.out.println("\n====== Day07 局域网 MCP Client ======");
        System.out.println("模式：只走 SSE（不用 stdio/npx）");
        System.out.println("Day07-01 自研 → " + opsServerUrl);
        System.out.println("Day07-02 开源 → " + filesystemUrl);
        System.out.println("查看 Tool：GET http://localhost:8107/api/mcp-agent/tools");
        System.out.println("问题：" + startupQuestion);
        try {
            McpAgentReply reply = mcpAgentApplicationService.troubleshoot(startupQuestion);
            System.out.println("回答：" + reply.answer());
        } catch (Exception e) {
            System.err.println("调用失败：" + e.getMessage());
            System.err.println("请确认：1) server_01 已启动(8104)  2) server_02 supergateway(8106)  3) Ollama 已启动");
        }
        System.out.println("=====================================\n");
    }
}
