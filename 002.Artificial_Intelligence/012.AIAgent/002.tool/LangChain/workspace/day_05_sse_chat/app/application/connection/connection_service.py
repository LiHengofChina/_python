# -*- coding: utf-8 -*-
from __future__ import annotations

from app.domain.model import ConnectionProfile
from app.infrastructure.persistence.connection_store import ConnectionStore


class ConnectionApplicationService:
    """应用层：连接档案 CRUD（连接管理）。"""

    def __init__(self, store: ConnectionStore) -> None:
        self._store = store

    def list_connections(self) -> list[ConnectionProfile]:
        return self._store.list_all()

    def get(self, conn_id: int) -> ConnectionProfile:
        row = self._store.get(conn_id)
        if row is None:
            raise ValueError(f"连接不存在: {conn_id}")
        return row

    def create(self, label: str, type_: str, config_yaml: str) -> ConnectionProfile:
        if not label.strip():
            raise ValueError("label 不能为空")
        if not type_.strip():
            raise ValueError("type 不能为空")
        return self._store.create(label, type_, config_yaml)

    def update(
        self, conn_id: int, label: str, type_: str, config_yaml: str
    ) -> ConnectionProfile:
        if not label.strip():
            raise ValueError("label 不能为空")
        return self._store.update(conn_id, label, type_, config_yaml)

    def delete(self, conn_id: int) -> None:
        self._store.delete(conn_id)

    def labels_hint(self) -> str:
        rows = self._store.list_all()
        if not rows:
            return "（暂无连接，请先在左侧连接管理新增）"
        return "、".join(f"{r.label}({r.type})" for r in rows)
