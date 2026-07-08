package com.demo.springai.mcpclient.interfaces.web;

import com.demo.springai.mcpclient.application.McpAgentApplicationService;
import com.demo.springai.mcpclient.domain.model.McpAgentReply;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

import java.util.Map;

/**
 * Day07 局域网 Agent 排查接口。
 *
 * <p>先启动 8104（自研 JAR）和 8106（supergateway），再访问本接口。
 * 示例：{@code GET http://localhost:8107/api/mcp-agent/troubleshoot?q=linux-231磁盘快满了}
 */
@RestController
@RequestMapping("/api/mcp-agent")
public class McpAgentController {

    private final McpAgentApplicationService mcpAgentApplicationService;

    public McpAgentController(McpAgentApplicationService mcpAgentApplicationService) {
        this.mcpAgentApplicationService = mcpAgentApplicationService;
    }

    @GetMapping("/troubleshoot")
    public Map<String, String> troubleshoot(@RequestParam("q") String question) {
        McpAgentReply reply = mcpAgentApplicationService.troubleshoot(question);
        return Map.of("question", reply.question(), "answer", reply.answer());
    }
}
