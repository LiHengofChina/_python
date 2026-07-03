package com.demo.springai.orchestration.infrastructure.llm;

import com.demo.springai.orchestration.domain.model.OpsIntent;
import org.springframework.ai.chat.client.ChatClient;
import org.springframework.stereotype.Component;

@Component
public class IntentAnalyzer {

    private final ChatClient chatClient;

    public IntentAnalyzer(ChatClient.Builder chatClientBuilder) {
        this.chatClient = chatClientBuilder.build();
    }

    public OpsIntent analyze(String question) {
        String raw = chatClient.prompt()
                .system("""
                        你是运维工单分类器。根据用户问题，只输出一个英文标签，不要解释。
                        可选标签：DISK、MEMORY、MYSQL、NGINX、UNKNOWN
                        - 磁盘、空间、df、/var/log → DISK
                        - 内存、OOM、swap、free → MEMORY
                        - MySQL、连接数、Too many connections → MYSQL
                        - Nginx、502、网关 → NGINX
                        """)
                .user(question)
                .call()
                .content();

        return parseIntent(raw);
    }

    private OpsIntent parseIntent(String raw) {
        if (raw == null) {
            return OpsIntent.UNKNOWN;
        }
        String upper = raw.strip().toUpperCase();
        for (OpsIntent intent : OpsIntent.values()) {
            if (upper.contains(intent.name())) {
                return intent;
            }
        }
        return OpsIntent.UNKNOWN;
    }
}
