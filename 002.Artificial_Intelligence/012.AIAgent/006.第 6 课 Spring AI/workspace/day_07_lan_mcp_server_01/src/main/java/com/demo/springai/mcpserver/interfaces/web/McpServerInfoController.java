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
        body.put("role", "Day07-01 自研 MCP Server");
        body.put("description", "SSH 运维 Tool，外网 mvn package → 内网 java -jar");
        body.put("deploy", "deploy/start-jar.bat 或 java -jar day07-lan-mcp-server-01-1.0.0.jar");
        body.put("sseEndpoint", "/sse");
        body.put("messageEndpoint", "/mcp/message");
        body.put("nextStep", "Agent：day_07_lan_mcp_client，sse.ops-server.url → http://内网IP:8104");
        return body;
    }
}
