package com.demo.springai.agent.interfaces.web;

import com.demo.springai.agent.application.AgentChatApplicationService;
import com.demo.springai.agent.domain.model.AgentChatReply;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

import java.util.Map;

/**
 * 带 Tool 的 Agent 风格排查接口。
 *
 * <p>示例：{@code GET http://localhost:8100/api/agent/troubleshoot?q=请排查srv-01磁盘为什么满了}
 */
@RestController
@RequestMapping("/api/agent")
public class AgentChatController {

    private final AgentChatApplicationService agentChatApplicationService;

    public AgentChatController(AgentChatApplicationService agentChatApplicationService) {
        this.agentChatApplicationService = agentChatApplicationService;
    }

    @GetMapping("/troubleshoot")
    public Map<String, String> troubleshoot(@RequestParam("q") String question) {
        AgentChatReply reply = agentChatApplicationService.troubleshoot(question);
        return Map.of("question", reply.question(), "answer", reply.answer());
    }
}
