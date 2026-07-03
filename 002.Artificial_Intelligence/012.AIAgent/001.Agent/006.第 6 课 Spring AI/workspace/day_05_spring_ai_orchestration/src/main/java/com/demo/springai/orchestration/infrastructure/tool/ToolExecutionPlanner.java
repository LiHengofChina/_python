package com.demo.springai.orchestration.infrastructure.tool;

import com.demo.springai.orchestration.domain.model.OpsIntent;
import com.demo.springai.orchestration.infrastructure.ssh.LinuxSshExecutor;
import org.springframework.stereotype.Component;

import java.util.ArrayList;
import java.util.List;

/**
 * 编排器决定执行哪些命令（非模型随意调 Tool）。
 */
@Component
public class ToolExecutionPlanner {

    private final LinuxSshExecutor sshExecutor;

    public ToolExecutionPlanner(LinuxSshExecutor sshExecutor) {
        this.sshExecutor = sshExecutor;
    }

    public String execute(OpsIntent intent) {
        List<String> commands = planCommands(intent);
        StringBuilder sb = new StringBuilder();
        for (String command : commands) {
            sb.append(sshExecutor.runReadOnlyCommand(command)).append("\n\n");
        }
        return sb.toString().strip();
    }

    private List<String> planCommands(OpsIntent intent) {
        List<String> commands = new ArrayList<>();
        switch (intent) {
            case DISK -> {
                commands.add("df -h");
                commands.add("du -sh /var/log/* 2>/dev/null | sort -hr | head -n 5");
            }
            case MEMORY -> {
                commands.add("free -h");
                commands.add("ps aux --sort=-%mem | head -n 4");
            }
            case MYSQL, NGINX -> {
                commands.add("free -h");
                commands.add("ps aux --sort=-%mem | head -n 4");
            }
            default -> {
                commands.add("df -h");
                commands.add("free -h");
            }
        }
        return commands;
    }
}
