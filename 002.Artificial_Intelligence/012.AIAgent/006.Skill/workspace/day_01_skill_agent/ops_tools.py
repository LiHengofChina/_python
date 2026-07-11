from __future__ import annotations

from pathlib import Path

import paramiko
import yaml
from langchain_core.tools import tool

BASE_DIR = Path(__file__).resolve().parent
MANUAL_PATH = BASE_DIR / "data" / "ops_manual.txt"
CONFIG_PATH = BASE_DIR / "config.local.yml"


def _load_config() -> dict:
    if not CONFIG_PATH.exists():
        return {}
    return yaml.safe_load(CONFIG_PATH.read_text(encoding="utf-8")) or {}


def _ssh_run(command: str) -> str:
    cfg = _load_config().get("ssh", {})
    if not cfg.get("enabled"):
        return "SSH 未启用：请复制 config.example.yml 为 config.local.yml 并配置密码"

    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    try:
        client.connect(
            hostname=cfg["host"],
            port=int(cfg.get("port", 22)),
            username=cfg["username"],
            password=cfg.get("password"),
            timeout=15,
        )
        _, stdout, stderr = client.exec_command(command, timeout=60)
        out = stdout.read().decode("utf-8", errors="replace").strip()
        err = stderr.read().decode("utf-8", errors="replace").strip()
        if err and not out:
            return err
        return out or "(无输出)"
    except Exception as exc:
        return f"SSH 执行失败: {exc}"
    finally:
        client.close()


@tool
def ssh_exec(command: str) -> str:
    """在 linux-231 (192.168.100.231) 执行只读 shell 命令，如 df -h、du -sh /var/log/*。"""
    blocked = ("rm ", "reboot", "shutdown", "mkfs", "dd ")
    if any(k in command.lower() for k in blocked):
        return "危险命令已拦截，仅输出方案，需人工审批后再执行"
    return _ssh_run(command)


@tool
def rag_search(query: str) -> str:
    """检索运维手册 ops_manual.txt，查磁盘告警、日志清理等标准处理方式。"""
    text = MANUAL_PATH.read_text(encoding="utf-8")
    sections = [s.strip() for s in text.split("\n## ") if s.strip()]
    hits = [s for s in sections if any(k in s.lower() for k in query.lower().split())]
    return "\n\n## ".join((hits or sections[:1])[:2])


ALL_TOOLS = {"ssh_exec": ssh_exec, "rag_search": rag_search}


def tools_for_skill(meta: dict) -> list:
    names = [n.strip() for n in str(meta.get("tools", "")).split(",") if n.strip()]
    return [ALL_TOOLS[n] for n in names if n in ALL_TOOLS]
