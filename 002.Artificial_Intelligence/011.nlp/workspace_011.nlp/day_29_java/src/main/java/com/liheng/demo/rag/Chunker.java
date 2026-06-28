package com.liheng.demo.rag;

import java.util.ArrayList;
import java.util.List;
import java.util.regex.Pattern;

/**
 * 【步骤 ②】文档切块（Chunking）。
 */
public final class Chunker {

    private static final Pattern SECTION_SPLIT = Pattern.compile("\n(?=## )");

    private Chunker() {
    }

    /**
     * 优先按 Markdown 二级标题（##）切块；无标题则按固定长度滑动窗口切。
     */
    public static List<String> buildChunks(String text, int chunkSize, int overlap) {
        if (text.contains("## ")) {
            return splitBySections(text);
        }
        return splitByFixedSize(text, chunkSize, overlap);
    }

    private static List<String> splitBySections(String text) {
        String[] parts = SECTION_SPLIT.split(text.strip());
        List<String> chunks = new ArrayList<>();
        for (String part : parts) {
            if (!part.isBlank()) {
                chunks.add(part.strip());
            }
        }
        return chunks;
    }

    private static List<String> splitByFixedSize(String text, int chunkSize, int overlap) {
        List<String> chunks = new ArrayList<>();
        int start = 0;
        int length = text.length();
        while (start < length) {
            int end = Math.min(start + chunkSize, length);
            String piece = text.substring(start, end).strip();
            if (!piece.isEmpty()) {
                chunks.add(piece);
            }
            if (end >= length) {
                break;
            }
            start += chunkSize - overlap;
        }
        return chunks;
    }
}
