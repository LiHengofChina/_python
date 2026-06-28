package com.liheng.demo.rag;

import java.util.List;

/**
 * 【步骤 ⑤ 后半】Mock 生成：不调用大模型，只展示检索结果（与 Python Demo 默认模式一致）。
 */
public final class MockAnswerGenerator {

    private MockAnswerGenerator() {
    }

    public static String generate(String question, List<SearchResult> retrieved) {
        StringBuilder answer = new StringBuilder();
        answer.append("【Mock 模式】未调用大模型，以下为根据检索资料整理的要点：\n");
        answer.append("您的问题：").append(question).append("\n\n");
        answer.append("检索到的相关内容：\n");

        for (int i = 0; i < retrieved.size(); i++) {
            SearchResult result = retrieved.get(i);
            answer.append("  (").append(i + 1).append(") 相似度 ")
                    .append(String.format("%.4f", result.score())).append("：\n");
            String[] lines = result.text().split("\n");
            int lineLimit = Math.min(5, lines.length);
            for (int j = 0; j < lineLimit; j++) {
                String line = lines[j].strip();
                if (!line.isEmpty()) {
                    answer.append("      ").append(line).append("\n");
                }
            }
            answer.append("\n");
        }

        answer.append("提示：接入 Spring AI / Ollama 后，可将本 Prompt 发给真实 LLM 生成自然语言回答。");
        return answer.toString();
    }
}
