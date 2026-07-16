package com.demo.springai.orchestration.interfaces.web;

import com.demo.springai.orchestration.application.OpsOrchestrationService;
import com.demo.springai.orchestration.application.OrchestrationStreamCallbacks;
import com.demo.springai.orchestration.interfaces.web.dto.ChatRequest;
import com.fasterxml.jackson.databind.ObjectMapper;
import org.springframework.http.MediaType;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RestController;
import org.springframework.web.servlet.mvc.method.annotation.SseEmitter;

import java.io.IOException;
import java.util.LinkedHashMap;
import java.util.Map;

/**
 * ChatGPT 风格：POST 发消息，SSE 逐步推送编排步骤 + 最终回答。
 */
@RestController
@RequestMapping("/api")
public class OrchestrationChatController {

    private static final long SSE_TIMEOUT_MS = 0L;

    private final OpsOrchestrationService opsOrchestrationService;
    private final ObjectMapper objectMapper;

    public OrchestrationChatController(
            OpsOrchestrationService opsOrchestrationService,
            ObjectMapper objectMapper) {
        this.opsOrchestrationService = opsOrchestrationService;
        this.objectMapper = objectMapper;
    }

    @PostMapping(value = "/chat", produces = MediaType.TEXT_EVENT_STREAM_VALUE)
    public SseEmitter chat(@RequestBody ChatRequest request) {
        String question = request.prompt() == null ? "" : request.prompt().strip();
        if (question.isEmpty()) {
            question = "你好";
        }

        SseEmitter emitter = new SseEmitter(SSE_TIMEOUT_MS);
        String finalQuestion = question;

        Thread worker = new Thread(() -> runOrchestration(emitter, finalQuestion), "orchestration-sse");
        worker.start();

        return emitter;
    }

    private void runOrchestration(SseEmitter emitter, String question) {
        try {
            safeSend(emitter, "start", Map.of("question", question));

            opsOrchestrationService.runStreaming(question, new OrchestrationStreamCallbacks() {
                @Override
                public void onStep(int order, String name, String output) {
                    Map<String, Object> payload = new LinkedHashMap<>();
                    payload.put("order", order);
                    payload.put("name", name);
                    payload.put("output", output);
                    safeSend(emitter, "step", payload);
                }

                @Override
                public void onComplete(String answer) {
                    safeSend(emitter, "answer", Map.of("content", answer));
                    safeSend(emitter, "done", "[DONE]");
                    emitter.complete();
                }
            });
        } catch (Exception e) {
            safeSend(emitter, "error", Map.of("message", e.getMessage()));
            emitter.completeWithError(e);
        }
    }

    private void safeSend(SseEmitter emitter, String eventName, Object data) {
        try {
            String json = data instanceof String s ? s : objectMapper.writeValueAsString(data);
            emitter.send(SseEmitter.event().name(eventName).data(json));
        } catch (IOException e) {
            emitter.completeWithError(e);
        }
    }
}
