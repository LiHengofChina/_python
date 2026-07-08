package com.demo.springai.mcpserver.infrastructure.tool;

import com.demo.springai.mcpserver.infrastructure.ssh.LinuxSshExecutor;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.ai.tool.annotation.Tool;
import org.springframework.ai.tool.annotation.ToolParam;
import org.springframework.stereotype.Component;

@Component
public class OpsMcpTools {

    private static final Logger log = LoggerFactory.getLogger(OpsMcpTools.class);

    private final LinuxSshExecutor sshExecutor;

    public OpsMcpTools(LinuxSshExecutor sshExecutor) {
        this.sshExecutor = sshExecutor;
    }

    /**
     * 工具一：queryDiskUsage — 查磁盘（df -h）
     * @param hostId
     * @return
     */
    @Tool(description = "查询已配置 Linux 主机的磁盘使用情况（执行 df -h）。hostId 填 linux-231。")
    public String queryDiskUsage(
            @ToolParam(description = "主机标识，填 linux-231") String hostId) {
        log.info("[MCP Tool] queryDiskUsage, hostId={}", hostId);
        return sshExecutor.runReadOnlyCommand("df -h");
    }

    /**
     * 工具二：queryMemoryUsage — 查内存（free -h）
     * @param hostId
     * @return
     */
    @Tool(description = "查询已配置 Linux 主机内存占用最高的进程 Top3（只读 ps 命令）。")
    public String queryTopMemoryProcesses(
            @ToolParam(description = "主机标识，填 linux-231") String hostId) {
        log.info("[MCP Tool] queryTopMemoryProcesses, hostId={}", hostId);
        return sshExecutor.runReadOnlyCommand("ps aux --sort=-%mem | head -n 4");
    }

    /**
     * 工具三：queryTopMemoryProcesses — 查内存占用最高的进程
     * @param hostId
     * @return
     */
    @Tool(description = "查询已配置 Linux 主机内存与 swap 使用情况（free -h）。")
    public String queryMemoryUsage(
            @ToolParam(description = "主机标识，填 linux-231") String hostId) {
        log.info("[MCP Tool] queryMemoryUsage, hostId={}", hostId);
        return sshExecutor.runReadOnlyCommand("free -h");
    }

    /**
     * 工具四：queryVarLogDiskUsage — 查 /var/log 占用
     * @param hostId
     * @return
     */
    @Tool(description = "查看 /var/log 下各子目录占用空间，辅助定位磁盘满是否由日志引起。")
    public String queryVarLogDiskUsage(
            @ToolParam(description = "主机标识，填 linux-231") String hostId) {
        log.info("[MCP Tool] queryVarLogDiskUsage, hostId={}", hostId);
        return sshExecutor.runReadOnlyCommand("du -sh /var/log/* 2>/dev/null | sort -hr | head -n 5");
    }
}
