package com.demo.springai.session.interfaces.web;

import com.demo.springai.session.application.ChatApplicationService;
import com.demo.springai.session.application.SessionApplicationService;
import com.demo.springai.session.domain.model.ChatMessage;
import com.demo.springai.session.domain.model.ChatReply;
import com.demo.springai.session.domain.model.ChatSession;
import com.demo.springai.session.infrastructure.persistence.ChatStore;
import org.springframework.http.HttpStatus;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PathVariable;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RestController;
import org.springframework.web.server.ResponseStatusException;

import java.util.LinkedHashMap;
import java.util.List;
import java.util.Map;

/**
 * REST：会话 CRUD + 聊天（对标 Python demo_002）。
 */
@RestController
public class SessionChatController {

    private final SessionApplicationService sessionService;
    private final ChatApplicationService chatService;

    public SessionChatController(
            SessionApplicationService sessionService,
            ChatApplicationService chatService) {
        this.sessionService = sessionService;
        this.chatService = chatService;
    }

    @GetMapping("/api/health")
    public Map<String, Object> health() {
        Map<String, Object> m = new LinkedHashMap<>();
        m.put("status", "ok");
        m.put("framework", "Spring Boot + Spring AI + SQLite 会话");
        m.put("user_id", ChatStore.FIXED_USER_ID);
        m.put("page", "http://localhost:8102/");
        return m;
    }

    @GetMapping("/api/sessions")
    public List<Map<String, Object>> listSessions() {
        return sessionService.listSessions().stream().map(this::sessionDto).toList();
    }

    @PostMapping("/api/sessions")
    public Map<String, Object> createSession(@RequestBody(required = false) SessionCreateRequest body) {
        String title = body == null || body.title() == null || body.title().isBlank()
                ? "新对话"
                : body.title().trim();
        return sessionDto(sessionService.createSession(title));
    }

    @GetMapping("/api/sessions/{sessionId}/messages")
    public List<Map<String, Object>> listMessages(@PathVariable long sessionId) {
        try {
            return sessionService.listMessages(sessionId).stream().map(this::messageDto).toList();
        } catch (IllegalArgumentException e) {
            throw new ResponseStatusException(HttpStatus.NOT_FOUND, e.getMessage(), e);
        }
    }

    @PostMapping("/api/chat")
    public Map<String, Object> chat(@RequestBody ChatRequest body) {
        if (body == null || body.question() == null || body.question().isBlank()) {
            throw new ResponseStatusException(HttpStatus.BAD_REQUEST, "question 不能为空");
        }
        try {
            ChatReply reply;
            Map<String, Object> out = new LinkedHashMap<>();
            if (body.sessionId() == null) {
                reply = chatService.chat(body.question().trim());
                out.put("question", reply.question());
                out.put("answer", reply.answer());
                out.put("session_id", null);
            } else {
                reply = chatService.chatInSession(body.sessionId(), body.question().trim());
                out.put("question", reply.question());
                out.put("answer", reply.answer());
                out.put("session_id", body.sessionId());
            }
            return out;
        } catch (IllegalArgumentException e) {
            throw new ResponseStatusException(HttpStatus.NOT_FOUND, e.getMessage(), e);
        } catch (Exception e) {
            throw new ResponseStatusException(
                    HttpStatus.BAD_GATEWAY, "调用 Ollama 失败: " + e.getMessage(), e);
        }
    }

    private Map<String, Object> sessionDto(ChatSession s) {
        Map<String, Object> m = new LinkedHashMap<>();
        m.put("id", s.id());
        m.put("user_id", s.userId());
        m.put("title", s.title());
        m.put("created_at", s.createdAt());
        return m;
    }

    private Map<String, Object> messageDto(ChatMessage msg) {
        Map<String, Object> m = new LinkedHashMap<>();
        m.put("id", msg.id());
        m.put("session_id", msg.sessionId());
        m.put("role", msg.role());
        m.put("content", msg.content());
        m.put("created_at", msg.createdAt());
        return m;
    }
}
