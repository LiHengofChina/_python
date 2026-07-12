from __future__ import annotations

import base64
import shlex
import subprocess
import sys
from pathlib import Path

import paramiko
import yaml
from langchain_core.tools import tool

BASE_DIR = Path(__file__).resolve().parent
CONFIG_PATH = BASE_DIR / "config.local.yml"

MODULES: dict[str, tuple[str, list[str]]] = {
    "basic": ("mysql_inspect_basic.py", ["check"]),
    "connection": ("mysql_inspect_connection.py", ["scan", "--threshold", "300"]),
    "performance": ("mysql_inspect_performance.py", ["audit"]),
    "architecture": ("mysql_inspect_architecture.py", ["check"]),
    "security": ("mysql_inspect_security.py", ["scan"]),
    "report": ("mysql_inspect_report.py", ["generate", "--report-type", "MySQL学习巡检", "--time-range", "24h"]),
}

_REMOTE_PYMYSQL_OK = False


def _load_config() -> dict:
    if not CONFIG_PATH.exists():
        return {}
    return yaml.safe_load(CONFIG_PATH.read_text(encoding="utf-8")) or {}


def _use_ssh_exec(cfg: dict) -> bool:
    mysql = cfg.get("mysql", {})
    if "use_ssh_exec" in mysql:
        return bool(mysql["use_ssh_exec"])
    return bool(cfg.get("ssh", {}).get("enabled"))


def _ssh_client(ssh_cfg: dict) -> paramiko.SSHClient:
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    client.connect(
        hostname=ssh_cfg["host"],
        port=int(ssh_cfg.get("port", 22)),
        username=ssh_cfg["username"],
        password=ssh_cfg.get("password"),
        timeout=15,
    )
    transport = client.get_transport()
    if transport:
        transport.set_keepalive(10)
    return client


def _ensure_remote_pymysql(ssh_cfg: dict) -> None:
    global _REMOTE_PYMYSQL_OK
    if _REMOTE_PYMYSQL_OK:
        return
    client = _ssh_client(ssh_cfg)
    try:
        _, stdout, _ = client.exec_command("python3 -c 'import pymysql'", timeout=30)
        if stdout.channel.recv_exit_status() == 0:
            _REMOTE_PYMYSQL_OK = True
            return
        _, stdout, _ = client.exec_command("pip3 install pymysql -q", timeout=180)
        stdout.read()
        stdout.channel.recv_exit_status()
        _REMOTE_PYMYSQL_OK = True
    finally:
        client.close()


def _deploy_remote_script(client: paramiko.SSHClient, script_name: str, body: str) -> str:
    b64 = base64.b64encode(body.encode("utf-8")).decode("ascii")
    remote_py = f"/tmp/{script_name}"
    remote_b64 = f"{remote_py}.b64"
    client.exec_command(f"rm -f {shlex.quote(remote_b64)}", timeout=15)
    # ponytail: 大块 heredoc/SFTP 会被网络掐断；改成分块 echo，每块短命令
    for i in range(0, len(b64), 400):
        chunk = b64[i : i + 400]
        _, stdout, _ = client.exec_command(
            f"printf %s {shlex.quote(chunk)} >> {shlex.quote(remote_b64)}",
            timeout=30,
        )
        stdout.channel.recv_exit_status()
    _, stdout, _ = client.exec_command(
        f"base64 -d {shlex.quote(remote_b64)} > {shlex.quote(remote_py)}",
        timeout=30,
    )
    stdout.channel.recv_exit_status()
    return remote_py


def _run_remote(scripts_dir: Path, script_name: str, fixed_args: list[str], mysql: dict, report_host: str) -> str:
    cfg = _load_config()
    ssh = cfg.get("ssh", {})
    _ensure_remote_pymysql(ssh)

    pwd = str(mysql.get("password", ""))
    tail = [
        *fixed_args,
        "--host", "127.0.0.1",
        "--port", str(mysql.get("port", 3306)),
        "--user", str(mysql["user"]),
        f"--password={pwd}",
    ]
    if script_name == "mysql_inspect_report.py":
        tail.extend(["--host", report_host])
    tail_s = " ".join(shlex.quote(a) for a in tail)
    script_body = (scripts_dir / script_name).read_text(encoding="utf-8")

    client = _ssh_client(ssh)
    try:
        remote_py = _deploy_remote_script(client, script_name, script_body)
        _, stdout, stderr = client.exec_command(
            f"python3 {shlex.quote(remote_py)} {tail_s}",
            timeout=120,
        )
        out = stdout.read().decode("utf-8", errors="replace").strip()
        err = stderr.read().decode("utf-8", errors="replace").strip()
        code = stdout.channel.recv_exit_status()
        merged = out or err or "(无输出)"
        if code != 0:
            return f"exit={code}\n{merged}".strip()
        return merged
    finally:
        client.close()


def _run_local(skill_dir: Path, script_name: str, fixed_args: list[str], mysql: dict, report_host: str, key: str) -> str:
    pwd = str(mysql.get("password", ""))
    script = skill_dir / "scripts" / "mysql_inspect" / script_name
    conn_args = [
        "--host", report_host,
        "--port", str(mysql.get("port", 3306)),
        "--user", str(mysql["user"]),
        f"--password={pwd}",
    ]
    cmd = [sys.executable, str(script), *fixed_args, *conn_args]
    if key == "report":
        cmd.extend(["--host", report_host])
    proc = subprocess.run(
        cmd, cwd=skill_dir, capture_output=True, text=True,
        timeout=120, encoding="utf-8", errors="replace",
    )
    merged = (proc.stdout or proc.stderr or "(无输出)").strip()
    if proc.returncode != 0:
        return f"exit={proc.returncode}\n{merged}".strip()
    return merged


def make_mysql_inspect_run(skill_dir: Path):
    scripts_dir = skill_dir / "scripts" / "mysql_inspect"

    @tool
    def mysql_inspect_run(inspect_module: str) -> str:
        """运行 MySQL 巡检子模块。inspect_module: basic|connection|performance|architecture|security|report。"""
        key = inspect_module.strip().lower()
        if key not in MODULES:
            return f"无效 inspect_module。可选: {', '.join(MODULES)}"

        script_name, fixed_args = MODULES[key]
        if not (scripts_dir / script_name).exists():
            return f"未找到脚本: {script_name}"

        cfg = _load_config()
        mysql = cfg.get("mysql", {})
        report_host = str(mysql.get("host", ""))

        try:
            if _use_ssh_exec(cfg):
                return _run_remote(scripts_dir, script_name, fixed_args, mysql, report_host)
            return _run_local(skill_dir, script_name, fixed_args, mysql, report_host, key)
        except subprocess.TimeoutExpired:
            return f"{key} 巡检超时（120s）"
        except Exception as exc:
            return f"巡检异常: {exc}"

    return mysql_inspect_run


def tools_for_skill(meta: dict, skill_dir: Path) -> list:
    names = [n.strip() for n in str(meta.get("tools", "")).split(",") if n.strip()]
    registry = {"mysql_inspect_run": make_mysql_inspect_run(skill_dir)}
    return [registry[n] for n in names if n in registry]
