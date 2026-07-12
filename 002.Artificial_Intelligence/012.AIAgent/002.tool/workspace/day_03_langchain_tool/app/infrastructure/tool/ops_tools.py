# -*- coding: utf-8 -*-
"""运维 Tool：对标 Spring AI OpsTools（4 个只读 SSH 工具）。"""
from __future__ import annotations

from langchain_core.tools import tool

from app.infrastructure.ssh import LinuxSshExecutor


def build_ops_tools(ssh: LinuxSshExecutor) -> list:
    @tool
    def query_disk_usage(host_id: str) -> str:
        """查询已配置 Linux 主机的磁盘使用情况（执行 df -h）。hostId 填 linux-231。"""
        print(f"[Tool] query_disk_usage host_id={host_id} target={ssh.get_target_description()}")
        return ssh.run_read_only_command("df -h")

    @tool
    def query_top_memory_processes(host_id: str) -> str:
        """查询已配置 Linux 主机内存占用最高的进程 Top3（只读 ps）。"""
        print(f"[Tool] query_top_memory_processes host_id={host_id}")
        return ssh.run_read_only_command("ps aux --sort=-%mem | head -n 4")

    @tool
    def query_memory_usage(host_id: str) -> str:
        """查询已配置 Linux 主机内存与 swap 使用情况（free -h）。"""
        print(f"[Tool] query_memory_usage host_id={host_id}")
        return ssh.run_read_only_command("free -h")

    @tool
    def query_var_log_disk_usage(host_id: str) -> str:
        """查看 /var/log 下各子目录占用空间，辅助定位磁盘满是否由日志引起。"""
        print(f"[Tool] query_var_log_disk_usage host_id={host_id}")
        return ssh.run_read_only_command(
            "du -sh /var/log/* 2>/dev/null | sort -hr | head -n 5"
        )

    return [
        query_disk_usage,
        query_top_memory_processes,
        query_memory_usage,
        query_var_log_disk_usage,
    ]
