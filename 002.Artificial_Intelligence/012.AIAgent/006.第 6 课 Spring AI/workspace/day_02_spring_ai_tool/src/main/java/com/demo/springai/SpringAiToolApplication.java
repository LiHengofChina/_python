package com.demo.springai;

import org.springframework.boot.SpringApplication;
import org.springframework.boot.autoconfigure.SpringBootApplication;

/**
 * 阶段 4 · Spring AI 第 2 课：Tool Demo。
 *
 * <p>在 Chat 基础上，让大模型可调用 Java 方法（模拟运维排查工具）。
 */
@SpringBootApplication
public class SpringAiToolApplication {

    public static void main(String[] args) {
        SpringApplication.run(SpringAiToolApplication.class, args);
    }
}
