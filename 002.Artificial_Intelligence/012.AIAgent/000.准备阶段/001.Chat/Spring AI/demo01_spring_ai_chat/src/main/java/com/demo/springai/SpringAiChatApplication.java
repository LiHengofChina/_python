package com.demo.springai;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;

/**
 * Chat demo01_spring_ai_chat 启动类。
 *
 * <p>分层：interfaces → application → domain ← infrastructure
 * <p>浏览器页面：{@code http://localhost:8102/}
 *
 * <p>前置：Ollama 已启动，并已 {@code ollama pull qwen2.5:7b}
 */
@SpringBootApplication
public class SpringAiChatApplication {

    public static void main(String[] args) {
        SpringApplication.run(SpringAiChatApplication.class, args);
    }

}
