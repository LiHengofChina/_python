package com.demo.springai.mcpclient.interfaces.web;

import org.springframework.ai.tool.ToolCallback;
import org.springframework.ai.tool.ToolCallbackProvider;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;

import java.util.Arrays;
import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;
import java.util.stream.Collectors;

/**
 * 查看当前 MCP Client 自动发现的所有 Tool（来自所有已连接的 MCP Server）。
 */
@RestController
@RequestMapping("/api/mcp-agent")
public class McpToolsInfoController {

    private final ToolCallbackProvider mcpToolCallbackProvider;

    @Value("${demo.mcp-client.filesystem-enabled:false}")
    private boolean filesystemEnabled;

    public McpToolsInfoController(ToolCallbackProvider mcpToolCallbackProvider) {
        this.mcpToolCallbackProvider = mcpToolCallbackProvider;
    }

    @GetMapping("/tools")
    public Map<String, Object> listTools() {
        List<Map<String, String>> tools = Arrays.stream(mcpToolCallbackProvider.getToolCallbacks())
                .map(this::toToolInfo)
                .collect(Collectors.toList());

        Map<String, Object> body = new LinkedHashMap<>();
        body.put("toolCount", tools.size());
        body.put("tools", tools);
        body.put("connections", buildConnectionHint());
        return body;
    }

    private Map<String, String> toToolInfo(ToolCallback callback) {
        var def = callback.getToolDefinition();
        Map<String, String> info = new LinkedHashMap<>();
        info.put("name", def.name());
        info.put("description", def.description());
        return info;
    }

    private List<String> buildConnectionHint() {
        if (filesystemEnabled) {
            return List.of(
                    "ops-server (SSE) → http://127.0.0.1:8104",
                    "filesystem (STDIO) → @modelcontextprotocol/server-filesystem");
        }
        return List.of("ops-server (SSE) → http://127.0.0.1:8104");
    }
}
