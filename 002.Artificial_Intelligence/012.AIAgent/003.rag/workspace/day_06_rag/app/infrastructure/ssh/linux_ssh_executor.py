# -*- coding: utf-8 -*-
"""按连接管理中的 label 解析 SSH 配置后执行只读命令。"""
from __future__ import annotations

from collections.abc import Callable

import paramiko

ALLOWED = {
    "df -h",
    "free -h",
    "ps aux --sort=-%mem | head -n 4",
    "du -sh /var/log/* 2>/dev/null | sort -hr | head -n 5",
    "who",
}


class LinuxSshExecutor:
    def __init__(self, resolve_cfg: Callable[[str], dict]) -> None:
        # resolve_cfg(label) -> ssh 参数字典（host/port/username/password/...）
        self._resolve = resolve_cfg

    def get_target_description(self, host_id: str) -> str:
        try:
            cfg = self._resolve(host_id)
            return f"{cfg.get('host_label', host_id)} ({cfg.get('host', '?')})"
        except Exception:
            return host_id

    def run_read_only_command(self, command: str, host_id: str) -> str:
        try:
            cfg = self._resolve(host_id)
        except Exception as e:
            return f"解析连接失败: {e}"

        if not cfg.get("enabled", True):
            return f"连接 {host_id} 未启用（config 中 enabled=false）"
        password = cfg.get("password")
        if not password:
            return f"连接 {host_id} 未配置 password"

        cmd = command.strip()
        if cmd not in ALLOWED:
            return f"不允许执行的命令: {command}"

        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        try:
            client.connect(
                hostname=cfg["host"],
                port=int(cfg.get("port", 22)),
                username=cfg["username"],
                password=password,
                timeout=20,
            )
            _, stdout, stderr = client.exec_command(cmd, timeout=25)
            out = stdout.read().decode("utf-8", errors="replace").strip()
            err = stderr.read().decode("utf-8", errors="replace").strip()
            code = stdout.channel.recv_exit_status()
            parts = [
                f"主机 {self.get_target_description(host_id)}",
                f"命令: {cmd}",
                f"exit={code}",
            ]
            if out:
                parts.extend(["--- stdout ---", out])
            if err:
                parts.extend(["--- stderr ---", err])
            return "\n".join(parts)
        except Exception as e:
            return f"SSH 执行失败: {e}"
        finally:
            client.close()
