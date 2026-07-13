# -*- coding: utf-8 -*-
"""文档元数据（SQLite）+ 磁盘上的 txt 文件。"""
from __future__ import annotations

import sqlite3
from pathlib import Path

from app.domain.document import DocumentRecord


class DocumentStore:
    def __init__(self, db_path: Path, upload_dir: Path) -> None:
        self.db_path = db_path
        self.upload_dir = upload_dir
        self.db_path.parent.mkdir(parents=True, exist_ok=True)
        self.upload_dir.mkdir(parents=True, exist_ok=True)
        self._init_schema()

    def _connect(self) -> sqlite3.Connection:
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn

    def _init_schema(self) -> None:
        with self._connect() as conn:
            conn.execute(
                """
                CREATE TABLE IF NOT EXISTS rag_document (
                    id INTEGER PRIMARY KEY AUTOINCREMENT,
                    filename TEXT NOT NULL,
                    stored_name TEXT NOT NULL,
                    status TEXT NOT NULL DEFAULT 'pending',
                    chunk_count INTEGER NOT NULL DEFAULT 0,
                    error_message TEXT NOT NULL DEFAULT '',
                    created_at TEXT NOT NULL DEFAULT (datetime('now','localtime')),
                    updated_at TEXT NOT NULL DEFAULT (datetime('now','localtime'))
                )
                """
            )

    def list_all(self) -> list[DocumentRecord]:
        with self._connect() as conn:
            rows = conn.execute(
                "SELECT * FROM rag_document ORDER BY id DESC"
            ).fetchall()
        return [self._row(r) for r in rows]

    def get(self, doc_id: int) -> DocumentRecord | None:
        with self._connect() as conn:
            row = conn.execute(
                "SELECT * FROM rag_document WHERE id = ?", (doc_id,)
            ).fetchone()
        return self._row(row) if row else None

    def add(self, filename: str, content: bytes) -> DocumentRecord:
        safe = Path(filename).name
        if not safe.lower().endswith(".txt"):
            raise ValueError("目前只支持 .txt 文件")
        with self._connect() as conn:
            cur = conn.execute(
                "INSERT INTO rag_document(filename, stored_name, status) VALUES (?, '', 'pending')",
                (safe,),
            )
            doc_id = int(cur.lastrowid)
            stored = f"{doc_id}_{safe}"
            path = self.upload_dir / stored
            path.write_bytes(content)
            conn.execute(
                "UPDATE rag_document SET stored_name = ?, updated_at = datetime('now','localtime') WHERE id = ?",
                (stored, doc_id),
            )
            row = conn.execute(
                "SELECT * FROM rag_document WHERE id = ?", (doc_id,)
            ).fetchone()
        return self._row(row)

    def delete(self, doc_id: int) -> bool:
        doc = self.get(doc_id)
        if not doc:
            return False
        path = self.upload_dir / doc.stored_name
        if path.exists():
            path.unlink()
        with self._connect() as conn:
            conn.execute("DELETE FROM rag_document WHERE id = ?", (doc_id,))
        return True

    def set_status(
        self,
        doc_id: int,
        status: str,
        *,
        chunk_count: int | None = None,
        error_message: str = "",
    ) -> DocumentRecord:
        with self._connect() as conn:
            if chunk_count is None:
                conn.execute(
                    """
                    UPDATE rag_document
                    SET status = ?, error_message = ?, updated_at = datetime('now','localtime')
                    WHERE id = ?
                    """,
                    (status, error_message, doc_id),
                )
            else:
                conn.execute(
                    """
                    UPDATE rag_document
                    SET status = ?, chunk_count = ?, error_message = ?,
                        updated_at = datetime('now','localtime')
                    WHERE id = ?
                    """,
                    (status, chunk_count, error_message, doc_id),
                )
            row = conn.execute(
                "SELECT * FROM rag_document WHERE id = ?", (doc_id,)
            ).fetchone()
        return self._row(row)

    def file_path(self, doc: DocumentRecord) -> Path:
        return self.upload_dir / doc.stored_name

    @staticmethod
    def _row(row: sqlite3.Row) -> DocumentRecord:
        return DocumentRecord(
            id=int(row["id"]),
            filename=str(row["filename"]),
            stored_name=str(row["stored_name"]),
            status=str(row["status"]),
            chunk_count=int(row["chunk_count"]),
            error_message=str(row["error_message"] or ""),
            created_at=str(row["created_at"]),
            updated_at=str(row["updated_at"]),
        )
