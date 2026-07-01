package com.demo.springai.chat.domain.gateway;

/**
 *
 * 【在 DDD 里，Gateway（网关） 表示：领域层要用的外部能力，由基础设施层去实现。】
 *
 * 领域网关（端口）：与大模型对话的能力抽象。
 *
 * <p>领域层只定义「需要什么」，不关心 Ollama / Spring AI 如何实现。
 */
public interface LlmChatGateway {

    /** 普通对话：仅用户消息 */
    String chat(String userMessage);

    /** 带系统角色（System Prompt）的对话 */
    String chatWithSystemRole(String systemPrompt, String userMessage);
}
