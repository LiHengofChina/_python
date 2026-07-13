# -*- coding: utf-8 -*-
"""连接档案 SQLite 仓储（连接管理）。"""
from __future__ import annotations

import sqlite3
from pathlib import Path

import yaml

from app.domain.model import ConnectionProfile


class ConnectionStore:
    def __init__(self, db_path: Path) -> None:
        self.db_path = db_path
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self._init_schema()

    def _connect(self) -> sqlite3.Connection:
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn

    def _init_schema(self) -> None:
        with self._connect() as conn:
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS connection_profile (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    label TEXT NOT NULL UNIQUE,
                    type TEXT NOT NULL,
                    config_yaml TEXT NOT NULL,
                    created_at TEXT NOT NULL DEFAULT (datetime('now','localtime')),
                    updated_at TEXT NOT NULL DEFAULT (datetime('now','localtime'))
                )
                """
            )

    def seed_from_ssh_config(self, ssh_cfg: dict) -> ConnectionProfile | None:
        """库为空且 config 有 ssh 时，导入一条，方便 Demo 开箱即用。"""
        if self.list_all():
            return None
        if not ssh_cfg or not ssh_cfg.get("host"):
            return None
        label = str(ssh_cfg.get("host_label") or "linux-231")
        payload = {
            "enabled": bool(ssh_cfg.get("enabled", True)),
            "host": ssh_cfg.get("host"),
            "port": int(ssh_cfg.get("port", 22)),
            "username": ssh_cfg.get("username", "root"),
            "password": ssh_cfg.get("password", ""),
        }
        return self.create(
            label=label,
            type_="linux",
            config_yaml=yaml.safe_dump(payload, allow_unicode=True, sort_keys=False),
        )

    def create(self, label: str, type_: str, config_yaml: str) -> ConnectionProfile:
        self._validate_yaml(config_yaml)
        with self._connect() as conn:
            try:
                cur = conn.execute(
                    "INSERT INTO connection_profile(label, type, config_yaml) VALUES (?, ?, ?)",
                    (label.strip(), type_.strip().lower(), config_yaml.strip()),
                )
            except sqlite3.IntegrityError as e:
                raise ValueError(f"label 已存在: {label}") from e
            row = conn.execute(
                "SELECT * FROM connection_profile WHERE id = ?", (int(cur.lastrowid),)
            ).fetchone()
        return self._row(row)

    def update(
        self, conn_id: int, label: str, type_: str, config_yaml: str
    ) -> ConnectionProfile:
        self._validate_yaml(config_yaml)
        with self._connect() as conn:
            exists = conn.execute(
                "SELECT id FROM connection_profile WHERE id = ?", (conn_id,)
            ).fetchone()
            if not exists:
                raise ValueError(f"连接不存在: {conn_id}")
            try:
                conn.execute(
                    """
                    UPDATE connection_profile
                    SET label = ?, type = ?, config_yaml = ?,
                        updated_at = datetime('now','localtime')
                    WHERE id = ?
                    """,
                    (label.strip(), type_.strip().lower(), config_yaml.strip(), conn_id),
                )
            except sqlite3.IntegrityError as e:
                raise ValueError(f"label 已存在: {label}") from e
            row = conn.execute(
                "SELECT * FROM connection_profile WHERE id = ?", (conn_id,)
            ).fetchone()
        return self._row(row)

    def delete(self, conn_id: int) -> None:
        with self._connect() as conn:
            cur = conn.execute(
                "DELETE FROM connection_profile WHERE id = ?", (conn_id,)
            )
            if cur.rowcount == 0:
                raise ValueError(f"连接不存在: {conn_id}")

    def list_all(self) -> list[ConnectionProfile]:
        with self._connect() as conn:
            rows = conn.execute(
                "SELECT * FROM connection_profile ORDER BY id DESC"
            ).fetchall()
        return [self._row(r) for r in rows]

    def get(self, conn_id: int) -> ConnectionProfile | None:
        with self._connect() as conn:
            row = conn.execute(
                "SELECT * FROM connection_profile WHERE id = ?", (conn_id,)
            ).fetchone()
        return self._row(row) if row else None

    def get_by_label(self, label: str) -> ConnectionProfile | None:
        with self._connect() as conn:
            row = conn.execute(
                "SELECT * FROM connection_profile WHERE label = ?", (label.strip(),)
            ).fetchone()
        return self._row(row) if row else None

    def resolve_linux_ssh(self, label: str) -> dict:
        """按 label 解析 linux 连接，供 SSH Tool 使用。"""
        key = (label or "").strip()
        profile = self.get_by_label(key)
        # ponytail: 小模型常把「linux-231机器」收成「linux-231」；仅当唯一前缀/包含匹配时兜底
        if profile is None and key:
            candidates = [
                p
                for p in self.list_all()
                if p.type == "linux"
                and (p.label == key or p.label.startswith(key) or key in p.label)
            ]
            if len(candidates) == 1:
                profile = candidates[0]
                print(f"[Conn] label 模糊匹配: {key!r} -> {profile.label!r}")
        if profile is None:
            available = [p.label for p in self.list_all()]
            raise ValueError(
                f"未找到连接 label={key!r}。可用 label: {available}"
            )
        if profile.type != "linux":
            raise ValueError(f"连接 {profile.label} 类型是 {profile.type}，不是 linux")
        data = yaml.safe_load(profile.config_yaml) or {}
        if not isinstance(data, dict):
            raise ValueError(f"连接 {profile.label} 的 config_yaml 必须是对象")
        data = dict(data)
        data["host_label"] = profile.label
        data.setdefault("enabled", True)
        return data

    @staticmethod
    def _validate_yaml(text: str) -> None:
        try:
            obj = yaml.safe_load(text)
        except yaml.YAMLError as e:
            raise ValueError(f"YAML 格式错误: {e}") from e
        if not isinstance(obj, dict):
            raise ValueError("config_yaml 必须是键值对象，例如 host/port/username")

    @staticmethod
    def _row(row: sqlite3.Row) -> ConnectionProfile:
        return ConnectionProfile(
            id=int(row["id"]),
            label=str(row["label"]),
            type=str(row["type"]),
            config_yaml=str(row["config_yaml"]),
            created_at=str(row["created_at"]),
            updated_at=str(row["updated_at"]),
        )
