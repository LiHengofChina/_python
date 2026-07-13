# -*- coding: utf-8 -*-
"""文档管理：上传 / 删除 / 列表 / 切块入库。"""
from __future__ import annotations

from app.domain.document import DocumentRecord
from app.infrastructure.persistence.document_store import DocumentStore
from app.infrastructure.rag import ChromaRagStore


class DocumentApplicationService:
    def __init__(self, store: DocumentStore, rag: ChromaRagStore) -> None:
        self._store = store
        self._rag = rag

    def list_documents(self) -> list[DocumentRecord]:
        return self._store.list_all()

    def upload(self, filename: str, content: bytes) -> DocumentRecord:
        return self._store.add(filename, content)

    def delete(self, doc_id: int) -> None:
        doc = self._store.get(doc_id)
        if not doc:
            raise ValueError(f"文档不存在: {doc_id}")
        self._rag.delete_doc(doc_id)
        self._store.delete(doc_id)

    def index_one(self, doc_id: int) -> DocumentRecord:
        doc = self._store.get(doc_id)
        if not doc:
            raise ValueError(f"文档不存在: {doc_id}")
        self._store.set_status(doc_id, "indexing", error_message="")
        try:
            path = self._store.file_path(doc)
            text = path.read_text(encoding="utf-8")
            n = self._rag.index_text(doc.id, doc.filename, text)
            return self._store.set_status(doc_id, "ready", chunk_count=n, error_message="")
        except Exception as e:
            return self._store.set_status(
                doc_id, "failed", chunk_count=0, error_message=str(e)
            )

    def reindex_all(self) -> list[DocumentRecord]:
        return [self.index_one(d.id) for d in self._store.list_all()]
