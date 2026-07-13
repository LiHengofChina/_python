# -*- coding: utf-8 -*-
"""运维 Tool：host_id = 连接管理中的 label。"""
from __future__ import annotations

from langchain_core.tools import tool

from app.infrastructure.ssh import LinuxSshExecutor


def build_ops_tools(ssh: LinuxSshExecutor) -> list:
    @tool
    def query_disk_usage(host_id: str) -> str:
        """查询 Linux 主机磁盘使用情况（df -h）。host_id 填连接管理中的 label，如 linux-231。"""
        print(f"[Tool] query_disk_usage host_id={host_id}")
        return ssh.run_read_only_command("df -h", host_id)

    @tool
    def query_top_memory_processes(host_id: str) -> str:
        """查询 Linux 主机内存占用最高进程 Top3。host_id 填连接管理中的 label。"""
        print(f"[Tool] query_top_memory_processes host_id={host_id}")
        return ssh.run_read_only_command("ps aux --sort=-%mem | head -n 4", host_id)

    @tool
    def query_memory_usage(host_id: str) -> str:
        """查询 Linux 主机内存与 swap（free -h）。host_id 填连接管理中的 label。"""
        print(f"[Tool] query_memory_usage host_id={host_id}")
        return ssh.run_read_only_command("free -h", host_id)

    @tool
    def query_var_log_disk_usage(host_id: str) -> str:
        """查看 /var/log 子目录占用。host_id 填连接管理中的 label。"""
        print(f"[Tool] query_var_log_disk_usage host_id={host_id}")
        return ssh.run_read_only_command(
            "du -sh /var/log/* 2>/dev/null | sort -hr | head -n 5", host_id
        )

    @tool
    def query_logged_in_users(host_id: str) -> str:
        """查询 Linux 主机当前有哪些用户已登录（who）。host_id 填连接管理中的 label。"""
        print(f"[Tool] query_logged_in_users host_id={host_id}")
        return ssh.run_read_only_command("who", host_id)

    return [
        query_disk_usage,
        query_top_memory_processes,
        query_memory_usage,
        query_var_log_disk_usage,
        query_logged_in_users,
    ]
