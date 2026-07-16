package com.demo.springai.mcpserver.interfaces.web;

import org.springframework.beans.factory.annotation.Value;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RestController;

import java.util.LinkedHashMap;
import java.util.Map;

@RestController
public class McpServerInfoController {

    @Value("${spring.ai.mcp.server.name:ops-mcp-server}")
    private String serverName;

    @GetMapping("/")
    public Map<String, Object> info() {
        Map<String, Object> body = new LinkedHashMap<>();
        body.put("name", serverName);
        body.put("role", "MCP Server");
        body.put("description", "把运维 SSH Tool 通过 MCP 协议暴露，供 Agent 客户端连接");
        body.put("sseEndpoint", "/sse");
        body.put("messageEndpoint", "/mcp/message");
        body.put("nextStep", "启动 day_06_mcp_client（8105），它会连本 Server 调用 Tool");
        return body;
    }
}
