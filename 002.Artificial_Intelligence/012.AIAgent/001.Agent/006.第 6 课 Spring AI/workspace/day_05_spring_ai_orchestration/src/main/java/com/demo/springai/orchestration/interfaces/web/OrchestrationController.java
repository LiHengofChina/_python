package com.demo.springai.orchestration.interfaces.web;

import com.demo.springai.orchestration.application.OpsOrchestrationService;
import com.demo.springai.orchestration.domain.model.OrchestrationResult;
import com.demo.springai.orchestration.domain.model.OrchestrationStep;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;

/**
 * 编排接口：返回每一步的中间结果，便于观察 Agent 如何组织多步骤。
 *
 * <p>示例：{@code GET http://localhost:8103/api/orchestration/run?q=linux-231磁盘快满了}
 */
@RestController
@RequestMapping("/api/orchestration")
public class OrchestrationController {

    private final OpsOrchestrationService opsOrchestrationService;

    public OrchestrationController(OpsOrchestrationService opsOrchestrationService) {
        this.opsOrchestrationService = opsOrchestrationService;
    }

    @GetMapping("/run")
    public Map<String, Object> run(@RequestParam("q") String question) {
        OrchestrationResult result = opsOrchestrationService.run(question);
        List<Map<String, Object>> steps = result.steps().stream()
                .map(this::toStepMap)
                .toList();

        Map<String, Object> body = new LinkedHashMap<>();
        body.put("question", result.question());
        body.put("steps", steps);
        body.put("answer", result.answer());
        return body;
    }

    private Map<String, Object> toStepMap(OrchestrationStep step) {
        Map<String, Object> map = new LinkedHashMap<>();
        map.put("order", step.order());
        map.put("name", step.name());
        map.put("output", step.output());
        return map;
    }
}
