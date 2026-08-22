package com.demo.springai.chat.interfaces.web;

import com.demo.springai.chat.application.ChatApplicationService;
import com.demo.springai.chat.domain.model.ChatReply;
import org.springframework.http.HttpStatus;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;
import org.springframework.web.server.ResponseStatusException;

import java.util.Map;

/**
 * 接口层：HTTP 适配器。
 *
 * <p>示例：
 * <ul>
 *   <li>浏览器页面：{@code http://localhost:8102/}</li>
 *   <li>{@code POST /api/chat} body {@code {"question":"磁盘满了怎么办"}}</li>
 *   <li>{@code GET /api/chat?q=磁盘满了怎么办}</li>
 * </ul>
 */
@RestController
@RequestMapping("/api/chat")
public class ChatController {

    private final ChatApplicationService chatApplicationService;

    public ChatController(ChatApplicationService chatApplicationService) {
        this.chatApplicationService = chatApplicationService;
    }

    @GetMapping
    public Map<String, String> chatGet(@RequestParam("q") String question) {
        return doChat(question);
    }

    @PostMapping
    public Map<String, String> chatPost(@RequestBody ChatRequest body) {
        if (body == null || body.question() == null || body.question().isBlank()) {
            throw new ResponseStatusException(HttpStatus.BAD_REQUEST, "question 不能为空");
        }
        return doChat(body.question().trim());
    }

    @GetMapping("/ops")
    public Map<String, String> chatOps(@RequestParam("q") String question) {
        String system = "你是银行运维助手，回答要简洁、可执行，涉及生产操作要提醒人工审批。";
        try {
            ChatReply reply = chatApplicationService.chatWithSystemRole(system, question);
            return Map.of("question", reply.question(), "answer", reply.answer());
        } catch (Exception e) {
            throw new ResponseStatusException(HttpStatus.BAD_GATEWAY, "调用 Ollama 失败: " + e.getMessage(), e);
        }
    }

    private Map<String, String> doChat(String question) {
        try {
            ChatReply reply = chatApplicationService.chat(question);
            return Map.of("question", reply.question(), "answer", reply.answer());
        } catch (Exception e) {
            throw new ResponseStatusException(HttpStatus.BAD_GATEWAY, "调用 Ollama 失败: " + e.getMessage(), e);
        }
    }
}
