package com.demo.springai.chat.interfaces.web;

import com.demo.springai.chat.application.ChatApplicationService;
import com.demo.springai.chat.domain.model.ChatReply;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

import java.util.Map;

/**
 * 接口层（用户接口）：HTTP 适配器。
 *
 * <p>示例：
 * <ul>
 *   <li>{@code GET http://localhost:8099/api/chat?q=磁盘满了怎么办}</li>
 *   <li>{@code GET http://localhost:8099/api/chat/ops?q=Nginx502怎么排查}</li>
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
    public Map<String, String> chat(@RequestParam("q") String question) {
        ChatReply reply = chatApplicationService.chat(question);
        return Map.of("question", reply.question(), "answer", reply.answer());
    }

    @GetMapping("/ops")
    public Map<String, String> chatOps(@RequestParam("q") String question) {
        String system = "你是银行运维助手，回答要简洁、可执行，涉及生产操作要提醒人工审批。";
        ChatReply reply = chatApplicationService.chatWithSystemRole(system, question);
        return Map.of("question", reply.question(), "answer", reply.answer());
    }
}
