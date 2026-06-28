package com.demo;

import com.liheng.demo.rag.*;

import java.util.List;

/**
 *
 *
 */
public final class RagDemo {

    private static final String SEP = "=".repeat(70);

    private RagDemo() {
    }

    public static void main(String[] args) throws Exception {
        System.out.println(SEP);
        System.out.println("day_29_java — Java RAG Demo（检索增强生成）");
        System.out.println(SEP);

        // ① 加载文档
        String text = DocumentLoader.loadFromClasspath(RagConfig.DOC_CLASSPATH);
        System.out.println("[1] 已加载文档：ops_manual.txt，共 " + text.length() + " 字符");

        // ② 切块
        List<String> chunks = Chunker.buildChunks(text, RagConfig.CHUNK_SIZE, RagConfig.CHUNK_OVERLAP);
        System.out.println("[2] 切块完成，共 " + chunks.size() + " 块");
        for (int i = 0; i < chunks.size(); i++) {
            String preview = chunks.get(i).replace("\n", " ");
            if (preview.length() > 60) {
                preview = preview.substring(0, 60) + "...";
            }
            System.out.println("    块" + i + ": " + preview);
        }

        // ③ 向量化入库
        SimpleVectorStore store = new SimpleVectorStore();
        store.addDocuments(chunks);
        System.out.println("[3] 已向量化入库：" + store.chunkCount() + " 块，特征维度 " + store.featureDimension());

        // 演示问题（与 Python Demo 相同）
        List<String> questions = List.of(
                "磁盘使用率超过 85% 应该怎么处理？",
                "Nginx 返回 502 怎么排查？",
                "数据库连接数过多怎么办？"
        );

        for (String question : questions) {
            ragAnswer(question, store);
        }

        System.out.println(SEP);
        System.out.println("Demo 结束。对照代码理解：切块 → 向量库 → 检索 → Prompt → Mock 生成。");
        System.out.println(SEP);
    }

    private static void ragAnswer(String question, SimpleVectorStore store) {
        System.out.println();
        System.out.println(SEP);
        System.out.println("用户问题：" + question);
        System.out.println(SEP);

        // ④ 检索
        List<SearchResult> retrieved = store.search(question, RagConfig.TOP_K);
        System.out.println("\n[4] 检索 Top-" + RagConfig.TOP_K + "：");
        for (int i = 0; i < retrieved.size(); i++) {
            SearchResult r = retrieved.get(i);
            String preview = r.text().replace("\n", " ");
            if (preview.length() > 50) {
                preview = preview.substring(0, 50) + "...";
            }
            System.out.printf("    Top%d | 块%d | 相似度 %.4f | %s%n",
                    i + 1, r.chunkIndex(), r.score(), preview);
        }

        // ⑤ 拼 Prompt + Mock 生成
        String prompt = RagPromptBuilder.build(question, retrieved);
        System.out.println("\n[5] 已拼装 Prompt（长度 " + prompt.length() + " 字符）");
        System.out.println("-".repeat(40) + " Prompt 预览 " + "-".repeat(40));
        String preview = prompt.length() > 800 ? prompt.substring(0, 800) + "..." : prompt;
        System.out.println(preview);
        System.out.println("-".repeat(88));

        System.out.println("\n[5] Mock 生成（未调用大模型）...");
        String answer = MockAnswerGenerator.generate(question, retrieved);
        System.out.println("\n【最终回答】");
        System.out.println(answer);
    }
}
