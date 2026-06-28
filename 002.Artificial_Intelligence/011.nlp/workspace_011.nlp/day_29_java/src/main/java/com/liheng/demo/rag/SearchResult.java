package com.liheng.demo.rag;

/**
 * 单条检索结果：块下标、相似度分数、块文本。
 */
public record SearchResult(int chunkIndex, double score, String text) {
}
