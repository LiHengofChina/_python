from __future__ import annotations

import re
import shlex
import threading
from pathlib import Path

import paramiko
import yaml
from langchain_core.tools import tool

BASE_DIR = Path(__file__).resolve().parent
CONFIG_PATH = BASE_DIR / "config.local.yml"
DEFAULT_IC_DIR = BASE_DIR / "instantclient" / "instantclient_19_26"
READONLY_BLOCK = re.compile(
    r"\b(insert|update|delete|merge|drop|truncate|alter|create|grant|revoke|shutdown)\b",
    re.I,
)
_THICK_READY = False
_THICK_LOCK = threading.Lock()
_CONN_LOCK = threading.Lock()  # ponytail: 串行化连接，避免 11g + thick 并发触发 ORA-28547


def _load_config() -> dict:
    if not CONFIG_PATH.exists():
        return {}
    return yaml.safe_load(CONFIG_PATH.read_text(encoding="utf-8")) or {}


def _ensure_thick(ora: dict) -> None:
    global _THICK_READY
    if _THICK_READY:
        return
    with _THICK_LOCK:
        if _THICK_READY:
            return
        ic_path = Path(ora.get("instant_client_dir") or DEFAULT_IC_DIR)
        if not ic_path.is_absolute():
            ic_path = BASE_DIR / ic_path
        if not (ic_path / "oci.dll").exists():
            return
        import oracledb

        oracledb.init_oracle_client(lib_dir=str(ic_path))
        _THICK_READY = True


def init_oracle_if_configured() -> None:
    """Agent 启动时预初始化 thick 模式，避免 Tool 并发首次 init。"""
    ora = _load_config().get("oracle", {})
    if ora.get("enabled"):
        _ensure_thick(ora)


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
    return client


def make_oracle_skill_read(skill_dir: Path):
    @tool
    def oracle_skill_read(skill_path: str) -> str:
        """读取 Oracle db 子技能文档。示例：performance/explain-plan.md、monitoring/alert-log.md"""
        rel = skill_path.strip().replace("\\", "/").lstrip("/")
        if rel.startswith("db/"):
            rel = rel[3:]
        target = (skill_dir / rel).resolve()
        if not str(target).startswith(str(skill_dir.resolve())):
            return "路径非法"
        if not target.exists():
            parent = skill_dir / Path(rel).parent
            if parent.is_dir():
                names = sorted(p.name for p in parent.glob("*.md"))
                return f"未找到 {rel}。同目录可选: {', '.join(names[:20])}"
            return f"未找到: {rel}"
        text = target.read_text(encoding="utf-8")
        return text[:12000] + ("\n...(截断)" if len(text) > 12000 else "")

    return oracle_skill_read


def make_oracle_sql_run():
    @tool
    def oracle_sql_run(sql: str) -> str:
        """在 Oracle 上执行只读 SQL（SELECT / 数据字典）。需 config.local.yml 配置 oracle。"""
        cfg = _load_config()
        ora = cfg.get("oracle", {})
        ssh = cfg.get("ssh", {})
        if not ora.get("enabled"):
            return "Oracle 未启用：请在 config.local.yml 设置 oracle.enabled=true"
        if READONLY_BLOCK.search(sql):
            return "危险 SQL 已拦截，仅输出方案，需人工审批后再执行"

        user = ora["user"]
        pwd = ora["password"]
        service = ora.get("service", "ORCL")
        host = ora.get("host", "127.0.0.1")
        port = int(ora.get("port", 1521))
        connect = f"{user}/{pwd}@//{host}:{port}/{service}"
        script = (
            "set heading on feedback off pagesize 200 linesize 200 trimspool on\n"
            f"{sql.strip().rstrip(';')};\n"
            "exit\n"
        )

        if ora.get("use_ssh_exec") and ssh.get("enabled"):
            cmd = f"sqlplus -S -L {shlex.quote(connect)} <<'EOSQL'\n{script}EOSQL"
            client = _ssh_client(ssh)
            try:
                _, stdout, stderr = client.exec_command(cmd, timeout=90)
                out = stdout.read().decode("utf-8", errors="replace").strip()
                err = stderr.read().decode("utf-8", errors="replace").strip()
                code = stdout.channel.recv_exit_status()
                merged = out or err or "(无输出)"
                if code != 0:
                    return f"exit={code}\n{merged}".strip()
                return merged
            finally:
                client.close()

        try:
            import oracledb
        except ImportError:
            return "未安装 oracledb，请 pip install oracledb"

        _ensure_thick(ora)
        try:
            with _CONN_LOCK:
                with oracledb.connect(
                    user=user, password=pwd, host=host, port=port, service_name=service
                ) as conn:
                    with conn.cursor() as cur:
                        cur.execute(sql.strip().rstrip(";"))
                        if cur.description:
                            cols = [d[0] for d in cur.description]
                            rows = cur.fetchmany(50)
                            lines = [f"connected_user={user}", "\t".join(cols)]
                            if rows:
                                lines.extend("\t".join(str(c) for c in r) for r in rows)
                            else:
                                lines.append(
                                    f"(0 rows) 当前以 {user} 登录；查本用户表请用 user_tables，"
                                    "查其他 schema 需对应账号或 DBA 权限"
                                )
                            return "\n".join(lines)
                        return "OK"
        except Exception as exc:
            return f"Oracle 执行失败: {exc}"

    return oracle_sql_run


def tools_for_skill(meta: dict, skill_dir: Path) -> list:
    names = [n.strip() for n in str(meta.get("tools", "")).split(",") if n.strip()]
    registry = {
        "oracle_skill_read": make_oracle_skill_read(skill_dir),
        "oracle_sql_run": make_oracle_sql_run(),
    }
    return [registry[n] for n in names if n in registry]
