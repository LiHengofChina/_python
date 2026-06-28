package com.liheng.demo.rag;

import java.util.ArrayList;
import java.util.List;
import java.util.Locale;
import java.util.regex.Matcher;
import java.util.regex.Pattern;

/**
 * 简易中文分词：提取英文/数字词 + 连续汉字（与 Python Demo 中 jieba 作用类似，便于 TF-IDF）。
 *
 * <p>学习阶段够用；生产 RAG 一般用 Embedding API，不依赖这种分词。
 */
public final class TextTokenizer {

    /** 匹配：英文数字词 或 单个汉字 */
    private static final Pattern TOKEN_PATTERN =
            Pattern.compile("[a-zA-Z0-9_]+|[\\u4e00-\\u9fa5]");

    private TextTokenizer() {
    }

    public static List<String> tokenize(String text) {
        List<String> tokens = new ArrayList<>();
        Matcher matcher = TOKEN_PATTERN.matcher(text.toLowerCase(Locale.ROOT));
        while (matcher.find()) {
            tokens.add(matcher.group());
        }
        return tokens;
    }
}
