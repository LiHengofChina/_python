package com.demo.springai.agent.domain.gateway;

/**
 * 带 Tool 能力的对话网关（领域端口）。
 */
public interface AgentChatGateway {

    /**
     * 模型可根据问题自动选择并调用已注册的 Tool，再生成最终回答。
     */
    String chatWithTools(String systemPrompt, String userMessage);
}
