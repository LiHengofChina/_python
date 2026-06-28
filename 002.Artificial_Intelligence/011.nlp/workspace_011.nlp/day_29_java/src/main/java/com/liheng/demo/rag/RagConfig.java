package com.liheng.demo.rag;

/**
 * RAG Demo 全局配置。
 */
public final class RagConfig {

    /** classpath 下运维手册路径 */
    public static final String DOC_CLASSPATH = "data/ops_manual.txt";

    /** 固定长度切块：每块字符数（无章节标题时使用） */
    public static final int CHUNK_SIZE = 200;

    /** 切块重叠字符数 */
    public static final int CHUNK_OVERLAP = 40;

    /** 检索返回前 K 个最相关块 */
    public static final int TOP_K = 2;

    private RagConfig() {
    }
}
