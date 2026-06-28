package com.liheng.demo.rag;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;

/**
 * 【步骤 ③ + ④】模拟向量库：TF-IDF 向量化 + 余弦相似度检索。
 *
 * <p>生产环境常用 Chroma、Milvus、PGVector + 神经网络 Embedding；
 * 本类用内存 TF-IDF 模拟「向量库 + 相似度查询」，与 Python Demo 思路一致。
 */
public class SimpleVectorStore {

    private List<String> chunks = new ArrayList<>();
    private List<Map<String, Double>> tfidfVectors = new ArrayList<>();
    private Map<String, Integer> vocabulary = new HashMap<>();

    /**
     * 入库：对所有文档块计算 TF-IDF 向量。
     */
    public void addDocuments(List<String> documentChunks) {
        this.chunks = new ArrayList<>(documentChunks);
        buildVocabulary(documentChunks);
        this.tfidfVectors = new ArrayList<>();
        for (String chunk : documentChunks) {
            tfidfVectors.add(computeTfidf(TextTokenizer.tokenize(chunk)));
        }
    }

    private void buildVocabulary(List<String> documentChunks) {
        vocabulary.clear();
        for (String chunk : documentChunks) {
            for (String token : TextTokenizer.tokenize(chunk)) {
                vocabulary.putIfAbsent(token, 1);
            }
        }
    }

    private Map<String, Double> computeTfidf(List<String> tokens) {
        Map<String, Integer> termFreq = new HashMap<>();
        for (String token : tokens) {
            termFreq.merge(token, 1, Integer::sum);
        }
        int totalTerms = tokens.size();
        Map<String, Double> tfidf = new HashMap<>();
        for (Map.Entry<String, Integer> entry : termFreq.entrySet()) {
            String term = entry.getKey();
            double tf = entry.getValue() / (double) totalTerms;
            int docCount = 0;
            for (String chunk : chunks) {
                if (TextTokenizer.tokenize(chunk).contains(term)) {
                    docCount++;
                }
            }
            double idf = Math.log((chunks.size() + 1.0) / (docCount + 1.0)) + 1.0;
            tfidf.put(term, tf * idf);
        }
        return tfidf;
    }

    private double cosineSimilarity(Map<String, Double> a, Map<String, Double> b) {
        double dot = 0.0;
        double normA = 0.0;
        double normB = 0.0;
        for (Map.Entry<String, Double> entry : a.entrySet()) {
            double va = entry.getValue();
            normA += va * va;
            Double vb = b.get(entry.getKey());
            if (vb != null) {
                dot += va * vb;
            }
        }
        for (double vb : b.values()) {
            normB += vb * vb;
        }
        if (normA == 0.0 || normB == 0.0) {
            return 0.0;
        }
        return dot / (Math.sqrt(normA) * Math.sqrt(normB));
    }

    /**
     * 检索 Top-K 最相似文档块。
     */
    public List<SearchResult> search(String query, int topK) {
        Map<String, Double> queryVector = computeTfidf(TextTokenizer.tokenize(query));
        List<SearchResult> ranked = new ArrayList<>();
        for (int i = 0; i < chunks.size(); i++) {
            double score = cosineSimilarity(queryVector, tfidfVectors.get(i));
            ranked.add(new SearchResult(i, score, chunks.get(i)));
        }
        ranked.sort((a, b) -> Double.compare(b.score(), a.score()));
        return ranked.subList(0, Math.min(topK, ranked.size()));
    }

    public int featureDimension() {
        return vocabulary.size();
    }

    public int chunkCount() {
        return chunks.size();
    }
}
