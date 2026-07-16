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

@RestController
@RequestMapping("/api/mcp-agent")
public class McpToolsInfoController {

    private final ToolCallbackProvider mcpToolCallbackProvider;

    @Value("${demo.mcp-client.ops-server-url:http://127.0.0.1:8104}")
    private String opsServerUrl;

    @Value("${demo.mcp-client.filesystem-url:http://127.0.0.1:8106/sse}")
    private String filesystemUrl;

    public McpToolsInfoController(ToolCallbackProvider mcpToolCallbackProvider) {
        this.mcpToolCallbackProvider = mcpToolCallbackProvider;
    }

    @GetMapping("/tools")
    public Map<String, Object> listTools() {
        List<Map<String, String>> tools = Arrays.stream(mcpToolCallbackProvider.getToolCallbacks())
                .map(this::toToolInfo)
                .collect(Collectors.toList());

        Map<String, Object> body = new LinkedHashMap<>();
        body.put("mode", "lan-sse");
        body.put("toolCount", tools.size());
        body.put("tools", tools);
        body.put("connections", List.of(
                "Day07-01 自研 JAR → " + opsServerUrl,
                "Day07-02 开源 supergateway → " + filesystemUrl));
        return body;
    }

    private Map<String, String> toToolInfo(ToolCallback callback) {
        var def = callback.getToolDefinition();
        Map<String, String> info = new LinkedHashMap<>();
        info.put("name", def.name());
        info.put("description", def.description());
        return info;
    }
}
