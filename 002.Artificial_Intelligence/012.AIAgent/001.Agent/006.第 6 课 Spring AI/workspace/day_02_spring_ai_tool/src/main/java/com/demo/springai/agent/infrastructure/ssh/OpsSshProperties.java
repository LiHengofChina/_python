package com.demo.springai.agent.infrastructure.ssh;

import org.springframework.boot.context.properties.ConfigurationProperties;

/**
 * Linux SSH 连接配置（密码建议放 application-local.yml，勿提交 Git）。
 */
@ConfigurationProperties(prefix = "demo.ops.ssh")
public class OpsSshProperties {

    /** 是否启用真实 SSH（false 时 Tool 返回提示，不连机器） */
    private boolean enabled = true;

    private String host = "192.168.100.231";

    private int port = 22;

    private String username = "root";

    private String password = "";

    /** 展示用主机标识，供 Tool 描述与日志 */
    private String hostLabel = "linux-231";

    public boolean isEnabled() {
        return enabled;
    }

    public void setEnabled(boolean enabled) {
        this.enabled = enabled;
    }

    public String getHost() {
        return host;
    }

    public void setHost(String host) {
        this.host = host;
    }

    public int getPort() {
        return port;
    }

    public void setPort(int port) {
        this.port = port;
    }

    public String getUsername() {
        return username;
    }

    public void setUsername(String username) {
        this.username = username;
    }

    public String getPassword() {
        return password;
    }

    public void setPassword(String password) {
        this.password = password;
    }

    public String getHostLabel() {
        return hostLabel;
    }

    public void setHostLabel(String hostLabel) {
        this.hostLabel = hostLabel;
    }
}
