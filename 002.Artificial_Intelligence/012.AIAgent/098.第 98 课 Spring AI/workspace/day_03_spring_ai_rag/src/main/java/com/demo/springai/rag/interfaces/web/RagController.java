package com.demo.springai.rag.interfaces.web;

import com.demo.springai.rag.application.RagApplicationService;
import com.demo.springai.rag.domain.model.RagReply;
import org.springframework.ai.document.Document;
import org.springframework.ai.vectorstore.SearchRequest;
import org.springframework.ai.vectorstore.VectorStore;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.RequestMapping;
import org.springframework.web.bind.annotation.RequestParam;
import org.springframework.web.bind.annotation.RestController;

import java.util.List;
import java.util.Map;
import java.util.stream.Collectors;

@RestController
@RequestMapping("/api/rag")
public class RagController {

    private final RagApplicationService ragApplicationService;
    private final VectorStore vectorStore;
    private final int topK;

    public RagController(
            RagApplicationService ragApplicationService,
            VectorStore vectorStore,
            @Value("${demo.rag.top-k:3}") int topK) {
        this.ragApplicationService = ragApplicationService;
        this.vectorStore = vectorStore;
        this.topK = topK;
    }

    /**
     * RAG 问答：检索 + 生成。
     * 示例：GET http://localhost:8101/api/rag/ask?q=磁盘满了怎么办
     */
    @GetMapping("/ask")
    public Map<String, String> ask(@RequestParam("q") String question) {
        RagReply reply = ragApplicationService.ask(question);
        return Map.of("question", reply.question(), "answer", reply.answer());
    }

    /**
     * 仅检索（不调用大模型），方便观察 RAG 检索到了哪些块。
     */
    @GetMapping("/search")
    public Map<String, Object> search(@RequestParam("q") String question) {
        List<Document> docs = vectorStore.similaritySearch(
                SearchRequest.builder().query(question).topK(topK).build());
        List<String> snippets = docs.stream()
                .map(d -> d.getText().replace("\n", " ").substring(0, Math.min(120, d.getText().length())))
                .collect(Collectors.toList());
        return Map.of("question", question, "topK", topK, "chunks", snippets);
    }
}
