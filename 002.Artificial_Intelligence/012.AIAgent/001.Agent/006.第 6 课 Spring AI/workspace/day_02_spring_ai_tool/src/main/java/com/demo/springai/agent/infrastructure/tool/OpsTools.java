package com.demo.springai.agent.infrastructure.tool;

import com.demo.springai.agent.infrastructure.ssh.LinuxSshExecutor;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.ai.tool.annotation.Tool;
import org.springframework.ai.tool.annotation.ToolParam;
import org.springframework.stereotype.Component;

/**
 *
 * 运维 Tool：通过 SSH 连接配置的 Linux（默认 192.168.100.231）执行只读排查命令。
 * 【这里注册了4个工具】，模型会根据实际情况决定调用哪个工具
 * 4 个 Tool 都通过 defaultTools(opsTools) 注册给模型。
 */
@Component
public class OpsTools {

    private static final Logger log = LoggerFactory.getLogger(OpsTools.class);

    private final LinuxSshExecutor sshExecutor;

    public OpsTools(LinuxSshExecutor sshExecutor) {
        this.sshExecutor = sshExecutor;
    }

    @Tool(description = """
            查询已配置 Linux 主机的磁盘使用情况（执行 df -h）。
            当前目标主机在配置中指定，hostId 填 linux-231 即可。
            """)
    public String queryDiskUsage(
            @ToolParam(description = "主机标识，填 linux-231") String hostId) {
        log.info("[Tool 调用] queryDiskUsage, hostId={}, target={}", hostId, sshExecutor.getTargetDescription());
        return sshExecutor.runReadOnlyCommand("df -h");
    }

    @Tool(description = """
            查询已配置 Linux 主机内存占用最高的进程 Top3（只读 ps 命令）。
            当前目标：配置中的 Linux 服务器。
            """)
    public String queryTopMemoryProcesses(
            @ToolParam(description = "主机标识，填 linux-231") String hostId) {
        log.info("[Tool 调用] queryTopMemoryProcesses, hostId={}", hostId);
        return sshExecutor.runReadOnlyCommand("ps aux --sort=-%mem | head -n 4");
    }

    @Tool(description = "查询已配置 Linux 主机内存与 swap 使用情况（free -h）")
    public String queryMemoryUsage(
            @ToolParam(description = "主机标识，填 linux-231") String hostId) {
        log.info("[Tool 调用] queryMemoryUsage, hostId={}", hostId);
        return sshExecutor.runReadOnlyCommand("free -h");
    }

    @Tool(description = "查看 /var/log 下各子目录占用空间，辅助定位磁盘满是否由日志引起")
    public String queryVarLogDiskUsage(
            @ToolParam(description = "主机标识，填 linux-231") String hostId) {
        log.info("[Tool 调用] queryVarLogDiskUsage, hostId={}", hostId);
        return sshExecutor.runReadOnlyCommand("du -sh /var/log/* 2>/dev/null | sort -hr | head -n 5");
    }
}
