# -*- coding: utf-8 -*-
"""Chroma 向量库：切块入库 + 检索（对照 Spring AI QuestionAnswerAdvisor）。"""
from __future__ import annotations

from pathlib import Path
from typing import Any

from langchain_chroma import Chroma
from langchain_core.documents import Document
from langchain_ollama import OllamaEmbeddings
from langchain_text_splitters import RecursiveCharacterTextSplitter


class ChromaRagStore:
    def __init__(
        self,
        persist_dir: Path,
        *,
        base_url: str = "http://127.0.0.1:11434",
        embed_model: str = "nomic-embed-text",
        chunk_size: int = 500,
        chunk_overlap: int = 50,
        top_k: int = 3,
        collection_name: str = "ops_docs",
    ) -> None:
        self.persist_dir = persist_dir
        self.persist_dir.mkdir(parents=True, exist_ok=True)
        self.top_k = top_k
        self._splitter = RecursiveCharacterTextSplitter(
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
            separators=["\n\n", "\n", "。", "；", " ", ""],
        )
        self._embeddings = OllamaEmbeddings(
            base_url=base_url,
            model=embed_model,
            # ponytail: Windows 代理环境偶发干扰本机 Ollama
            client_kwargs={"trust_env": False},
        )
        self._vs = Chroma(
            collection_name=collection_name,
            embedding_function=self._embeddings,
            persist_directory=str(self.persist_dir),
        )

    def index_text(self, doc_id: int, filename: str, text: str) -> int:
        """按 doc_id 重建该文档向量，返回 chunk 数。"""
        self.delete_doc(doc_id)
        text = (text or "").strip()
        if not text:
            return 0
        chunks = self._splitter.split_text(text)
        docs = [
            Document(
                page_content=chunk,
                metadata={
                    "doc_id": str(doc_id),
                    "filename": filename,
                    "chunk_index": i,
                },
            )
            for i, chunk in enumerate(chunks)
        ]
        ids = [f"doc{doc_id}_chunk{i}" for i in range(len(docs))]
        self._vs.add_documents(docs, ids=ids)
        return len(docs)

    def delete_doc(self, doc_id: int) -> None:
        # ponytail: Chroma where 过滤删除；空库时忽略
        try:
            self._vs.delete(where={"doc_id": str(doc_id)})
        except Exception:
            pass

    def search(self, query: str, top_k: int | None = None) -> list[dict[str, Any]]:
        k = top_k or self.top_k
        if not (query or "").strip():
            return []
        try:
            pairs = self._vs.similarity_search_with_score(query, k=k)
        except Exception:
            return []
        hits: list[dict[str, Any]] = []
        for doc, score in pairs:
            hits.append(
                {
                    "content": doc.page_content,
                    "filename": str(doc.metadata.get("filename") or ""),
                    "doc_id": doc.metadata.get("doc_id"),
                    "score": float(score),
                }
            )
        return hits

    @staticmethod
    def format_context(hits: list[dict[str, Any]]) -> str:
        if not hits:
            return ""
        parts = []
        for i, h in enumerate(hits, 1):
            src = h.get("filename") or "unknown"
            parts.append(f"[{i}] 来源:{src}\n{h.get('content') or ''}")
        return "\n\n".join(parts)
