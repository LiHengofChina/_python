package com.liheng.demo.rag;

import java.io.BufferedReader;
import java.io.IOException;
import java.io.InputStream;
import java.io.InputStreamReader;
import java.nio.charset.StandardCharsets;
import java.util.stream.Collectors;

/**
 * 【步骤 ①】从 classpath 加载原始文档。
 */
public final class DocumentLoader {

    private DocumentLoader() {
    }

    public static String loadFromClasspath(String classpathLocation) throws IOException {
        InputStream in = DocumentLoader.class.getClassLoader().getResourceAsStream(classpathLocation);
        if (in == null) {
            throw new IOException("找不到资源文件: " + classpathLocation);
        }
        try (BufferedReader reader = new BufferedReader(new InputStreamReader(in, StandardCharsets.UTF_8))) {
            return reader.lines().collect(Collectors.joining("\n"));
        }
    }
}
