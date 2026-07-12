# -*- coding: utf-8 -*-
"""通过 SSH 在目标 Linux 上执行预定义只读命令（禁止任意 shell）。"""
from __future__ import annotations

import paramiko

ALLOWED = {
    "df -h",
    "free -h",
    "ps aux --sort=-%mem | head -n 4",
    "du -sh /var/log/* 2>/dev/null | sort -hr | head -n 5",
}


class LinuxSshExecutor:
    def __init__(self, ssh_cfg: dict) -> None:
        self._cfg = ssh_cfg or {}

    def get_target_description(self) -> str:
        label = self._cfg.get("host_label", "linux")
        host = self._cfg.get("host", "?")
        return f"{label} ({host})"

    def run_read_only_command(self, command: str) -> str:
        if not self._cfg.get("enabled"):
            return "SSH 未启用，请在 config.local.yml 设置 ssh.enabled=true"
        password = self._cfg.get("password")
        if not password:
            return "SSH 密码未配置，请在 config.local.yml 设置 ssh.password"

        cmd = command.strip()
        if cmd not in ALLOWED:
            return f"不允许执行的命令: {command}"

        client = paramiko.SSHClient()
        client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
        try:
            client.connect(
                hostname=self._cfg["host"],
                port=int(self._cfg.get("port", 22)),
                username=self._cfg["username"],
                password=password,
                timeout=20,
            )
            _, stdout, stderr = client.exec_command(cmd, timeout=25)
            out = stdout.read().decode("utf-8", errors="replace").strip()
            err = stderr.read().decode("utf-8", errors="replace").strip()
            code = stdout.channel.recv_exit_status()
            parts = [
                f"主机 {self.get_target_description()}",
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
