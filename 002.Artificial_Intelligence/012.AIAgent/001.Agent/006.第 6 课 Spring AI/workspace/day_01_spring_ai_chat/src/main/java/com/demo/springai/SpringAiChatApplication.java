package com.demo.springai;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;

/**
 * 阶段 4 · Spring AI 第 1 课：Chat Demo 启动类。
 *
 * <p>chat 模块采用 DDD 分层：
 * interfaces → application → domain ← infrastructure
 *
 * <p>前置条件：
 * <ol>
 *   <li>本机已安装并启动 Ollama（默认端口 11434）</li>
 *   <li>已拉取模型：{@code ollama pull qwen2.5:7b}</li>
 * </ol>
 */
@SpringBootApplication
public class SpringAiChatApplication {

    public static void main(String[] args) {
        SpringApplication.run(SpringAiChatApplication.class, args);
    }

}
