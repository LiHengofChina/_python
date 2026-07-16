package com.demo.springai.orchestration.infrastructure.llm;

import com.demo.springai.orchestration.domain.model.OrchestrationContext;
import org.springframework.ai.chat.client.ChatClient;
import org.springframework.stereotype.Component;

/**
 * 多轮推理：先出初稿，再基于初稿复核补全。
 */
@Component
public class OpsSynthesizer {

    private final ChatClient chatClient;

    public OpsSynthesizer(ChatClient.Builder chatClientBuilder) {
        this.chatClient = chatClientBuilder.build();
    }

    public String draft(OrchestrationContext ctx) {
        return chatClient.prompt()
                .system("你是银行运维助手。结合手册摘录与现场数据写排查初稿，条目清晰。")
                .user(buildUserPrompt(ctx, false))
                .call()
                .content();
    }

    public String refine(OrchestrationContext ctx) {
        return chatClient.prompt()
                .system("""
                        你是银行运维专家。请复核下面的初稿：
                        1. 是否覆盖手册中的关键步骤
                        2. 是否与现场数据一致
                        3. 涉及重启/删除/变更必须标注「需人工审批」
                        输出最终建议（可直接执行的行动清单）。
                        """)
                .user(buildUserPrompt(ctx, true))
                .call()
                .content();
    }

    private String buildUserPrompt(OrchestrationContext ctx, boolean includeDraft) {
        StringBuilder sb = new StringBuilder();
        sb.append("【用户问题】\n").append(ctx.getQuestion()).append("\n\n");
        sb.append("【意图】\n").append(ctx.getIntent()).append("\n\n");
        sb.append("【手册摘录】\n").append(ctx.getManualExcerpt()).append("\n\n");
        sb.append("【现场数据】\n").append(ctx.getToolOutputs()).append("\n");
        if (includeDraft) {
            sb.append("\n【初稿】\n").append(ctx.getDraftAnswer()).append("\n");
        }
        return sb.toString();
    }
}
