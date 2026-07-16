# -*- coding: utf-8 -*-
"""文档 / 知识库管理 API。"""
from __future__ import annotations

from fastapi import APIRouter, File, HTTPException, UploadFile

from app.domain.document import DocumentRecord
from app.interfaces.web.container import container

router = APIRouter(prefix="/api/documents", tags=["文档管理"])


def _dto(d: DocumentRecord) -> dict:
    return {
        "id": d.id,
        "filename": d.filename,
        "status": d.status,
        "chunk_count": d.chunk_count,
        "error_message": d.error_message,
        "created_at": d.created_at,
        "updated_at": d.updated_at,
    }


@router.get("")
def list_documents() -> list[dict]:
    return [_dto(d) for d in container.document_service.list_documents()]


@router.post("")
async def upload_document(file: UploadFile = File(...)) -> dict:
    name = file.filename or "unnamed.txt"
    if not name.lower().endswith(".txt"):
        raise HTTPException(status_code=400, detail="目前只支持 .txt")
    content = await file.read()
    if not content:
        raise HTTPException(status_code=400, detail="空文件")
    try:
        doc = container.document_service.upload(name, content)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e)) from e
    return _dto(doc)


@router.delete("/{doc_id}")
def delete_document(doc_id: int) -> dict:
    try:
        container.document_service.delete(doc_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e)) from e
    return {"ok": True, "id": doc_id}


@router.post("/{doc_id}/index")
def index_document(doc_id: int) -> dict:
    try:
        doc = container.document_service.index_one(doc_id)
    except ValueError as e:
        raise HTTPException(status_code=404, detail=str(e)) from e
    return _dto(doc)


@router.post("/reindex")
def reindex_all() -> list[dict]:
    return [_dto(d) for d in container.document_service.reindex_all()]
