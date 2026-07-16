package com.demo.springai.memory.interfaces.web;

import com.demo.springai.memory.application.MemoryChatApplicationService;
import com.demo.springai.memory.domain.model.MemoryChatReply;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

import java.util.List;
import java.util.Map;

/**
 * 多轮对话：同一 {@code cid} 下，模型能记住前几轮内容。
 *
 * <p>示例（同一 cid 连问两次）：
 * <ul>
 *   <li>{@code GET /api/memory/chat?q=我叫运维小张，请记住&cid=user-001}</li>
 *   <li>{@code GET /api/memory/chat?q=我刚才说我叫什么&cid=user-001}</li>
 * </ul>
 */
@RestController
@RequestMapping("/api/memory")
public class MemoryChatController {

    private final MemoryChatApplicationService memoryChatApplicationService;

    public MemoryChatController(MemoryChatApplicationService memoryChatApplicationService) {
        this.memoryChatApplicationService = memoryChatApplicationService;
    }

    @GetMapping("/chat")
    public Map<String, String> chat(
            @RequestParam("q") String question,
            @RequestParam("cid") String conversationId) {
        MemoryChatReply reply = memoryChatApplicationService.chat(conversationId, question);
        return Map.of(
                "conversationId", reply.conversationId(),
                "question", reply.question(),
                "answer", reply.answer());
    }

    @GetMapping("/history")
    public Map<String, Object> history(@RequestParam("cid") String conversationId) {
        List<Map<String, String>> messages = memoryChatApplicationService.listHistory(conversationId);
        return Map.of(
                "conversationId", conversationId,
                "messageCount", messages.size(),
                "messages", messages);
    }
}
