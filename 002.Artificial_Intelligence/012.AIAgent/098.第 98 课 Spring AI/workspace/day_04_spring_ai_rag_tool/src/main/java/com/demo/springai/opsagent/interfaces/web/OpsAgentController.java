package com.demo.springai.opsagent.interfaces.web;

import com.demo.springai.opsagent.application.OpsAgentApplicationService;
import com.demo.springai.opsagent.domain.model.OpsAgentReply;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

import java.util.Map;

/**
 * RAG + Tool 合体排查接口。
 *
 * <p>示例：{@code GET http://localhost:8102/api/ops-agent/troubleshoot?q=linux-231磁盘快满了，请按手册排查}
 */
@RestController
@RequestMapping("/api/ops-agent")
public class OpsAgentController {

    private final OpsAgentApplicationService opsAgentApplicationService;

    public OpsAgentController(OpsAgentApplicationService opsAgentApplicationService) {
        this.opsAgentApplicationService = opsAgentApplicationService;
    }

    @GetMapping("/troubleshoot")
    public Map<String, String> troubleshoot(@RequestParam("q") String question) {
        OpsAgentReply reply = opsAgentApplicationService.troubleshoot(question);
        return Map.of("question", reply.question(), "answer", reply.answer());
    }
}
