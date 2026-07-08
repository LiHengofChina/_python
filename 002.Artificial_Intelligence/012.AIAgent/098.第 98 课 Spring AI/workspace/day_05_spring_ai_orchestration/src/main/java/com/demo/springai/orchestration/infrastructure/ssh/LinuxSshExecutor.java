package com.demo.springai.orchestration.infrastructure.ssh;

import net.schmizz.sshj.SSHClient;
import net.schmizz.sshj.connection.channel.direct.Session;
import net.schmizz.sshj.transport.verification.PromiscuousVerifier;
import org.springframework.stereotype.Component;

import java.io.ByteArrayOutputStream;
import java.io.IOException;
import java.nio.charset.StandardCharsets;
import java.util.concurrent.TimeUnit;

@Component
public class LinuxSshExecutor {

    private final OpsSshProperties properties;

    public LinuxSshExecutor(OpsSshProperties properties) {
        this.properties = properties;
    }

    public String getTargetDescription() {
        return properties.getHostLabel() + " (" + properties.getHost() + ")";
    }

    public String runReadOnlyCommand(String command) {
        if (!properties.isEnabled()) {
            return "SSH 未启用";
        }
        if (properties.getPassword() == null || properties.getPassword().isBlank()) {
            return "SSH 密码未配置";
        }
        validateReadOnlyCommand(command);

        try (SSHClient ssh = new SSHClient()) {
            ssh.addHostKeyVerifier(new PromiscuousVerifier());
            ssh.connect(properties.getHost(), properties.getPort());
            ssh.authPassword(properties.getUsername(), properties.getPassword());

            try (Session session = ssh.startSession()) {
                Session.Command cmd = session.exec(command);
                ByteArrayOutputStream stdout = new ByteArrayOutputStream();
                ByteArrayOutputStream stderr = new ByteArrayOutputStream();
                cmd.join(25, TimeUnit.SECONDS);
                stdout.writeBytes(cmd.getInputStream().readAllBytes());
                stderr.writeBytes(cmd.getErrorStream().readAllBytes());

                String out = stdout.toString(StandardCharsets.UTF_8).strip();
                String err = stderr.toString(StandardCharsets.UTF_8).strip();
                int exit = cmd.getExitStatus() == null ? -1 : cmd.getExitStatus();

                StringBuilder result = new StringBuilder();
                result.append("主机 ").append(getTargetDescription()).append("\n");
                result.append("命令: ").append(command).append("\n");
                result.append("exit=").append(exit).append("\n");
                if (!out.isEmpty()) {
                    result.append("--- stdout ---\n").append(out).append("\n");
                }
                if (!err.isEmpty()) {
                    result.append("--- stderr ---\n").append(err).append("\n");
                }
                return result.toString().strip();
            }
        } catch (IOException e) {
            return "SSH 执行失败: " + e.getMessage();
        }
    }

    private void validateReadOnlyCommand(String command) {
        String normalized = command.trim();
        boolean allowed = normalized.equals("df -h")
                || normalized.equals("free -h")
                || normalized.equals("ps aux --sort=-%mem | head -n 4")
                || normalized.equals("du -sh /var/log/* 2>/dev/null | sort -hr | head -n 5");
        if (!allowed) {
            throw new IllegalArgumentException("不允许执行的命令: " + command);
        }
    }
}
