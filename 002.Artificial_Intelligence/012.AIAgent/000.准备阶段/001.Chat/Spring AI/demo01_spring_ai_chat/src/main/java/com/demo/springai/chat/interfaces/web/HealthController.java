package com.demo.springai.chat.interfaces.web;

import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RestController;

import java.util.Map;

/**
 * 健康检查，对标 LangChain demo01_langchain_chat 的 /api/health。
 */
@RestController
public class HealthController {

    @GetMapping("/api/health")
    public Map<String, String> health() {
        return Map.of(
                "status", "ok",
                "framework", "Spring Boot + Spring AI ChatClient",
                "page", "http://localhost:8102/"
        );
    }
}
