# -*- coding: utf-8 -*-
from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class DocumentRecord:
    id: int
    filename: str
    stored_name: str
    status: str  # pending | indexing | ready | failed
    chunk_count: int
    error_message: str
    created_at: str
    updated_at: str
