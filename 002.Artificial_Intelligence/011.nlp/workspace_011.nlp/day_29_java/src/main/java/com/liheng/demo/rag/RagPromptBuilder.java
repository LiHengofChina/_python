package com.liheng.demo.rag;

import java.util.List;

/**
 * 【步骤 ⑤ 前半】拼装 RAG Prompt：参考资料 + 用户问题。
 */
public final class RagPromptBuilder {

    private RagPromptBuilder() {
    }

    public static String build(String question, List<SearchResult> retrieved) {
        StringBuilder context = new StringBuilder();
        for (int i = 0; i < retrieved.size(); i++) {
            SearchResult result = retrieved.get(i);
            context.append("--- 资料").append(i + 1)
                    .append("（块").append(result.chunkIndex())
                    .append("，相似度 ").append(String.format("%.4f", result.score()))
                    .append("）---\n")
                    .append(result.text())
                    .append("\n\n");
        }

        return "你是银行运维助手。请严格根据以下参考资料回答问题。\n"
                + "若资料中没有相关内容，请明确回答「资料中未找到，无法确定」。\n\n"
                + "【参考资料】\n"
                + context
                + "【用户问题】\n"
                + question + "\n\n"
                + "【回答】\n";
    }
}
