package com.demo.springai.mcpserver.infrastructure.config;

import com.demo.springai.mcpserver.infrastructure.ssh.OpsSshProperties;
import com.demo.springai.mcpserver.infrastructure.tool.OpsMcpTools;
import org.springframework.ai.tool.ToolCallbackProvider;
import org.springframework.ai.tool.method.MethodToolCallbackProvider;
import org.springframework.boot.context.properties.EnableConfigurationProperties;
import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

/**
 * 把 @Tool 方法注册为 MCP Tool（供 MCP Client 远程发现与调用）。
 *
 * <p>对比 day_02：day_02 用 defaultTools() 直接绑进 ChatClient；
 * 本课把同一批 Tool 通过 MCP 协议暴露出去。
 */
@Configuration
@EnableConfigurationProperties(OpsSshProperties.class)
public class McpServerConfig {

    @Bean
    public ToolCallbackProvider opsMcpToolProvider(OpsMcpTools opsMcpTools) {
        return MethodToolCallbackProvider.builder()
                .toolObjects(opsMcpTools)
                .build();
    }
}
