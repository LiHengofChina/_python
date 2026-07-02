package com.demo.springai.agent.infrastructure.config;

import com.demo.springai.agent.infrastructure.ssh.OpsSshProperties;
import org.springframework.boot.context.properties.EnableConfigurationProperties;
import org.springframework.context.annotation.Configuration;

@Configuration
@EnableConfigurationProperties(OpsSshProperties.class)
public class OpsInfrastructureConfig {
}
