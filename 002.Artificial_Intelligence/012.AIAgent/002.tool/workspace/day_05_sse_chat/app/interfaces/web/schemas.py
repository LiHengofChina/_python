# -*- coding: utf-8 -*-
from __future__ import annotations

from pydantic import BaseModel, Field


class ChatRequest(BaseModel):
    question: str = Field(..., min_length=1)
    session_id: int | None = Field(default=None)


class ChatResponse(BaseModel):
    question: str
    answer: str
    session_id: int | None = None


class SessionCreateRequest(BaseModel):
    title: str = "新对话"


class ConnectionBody(BaseModel):
    label: str = Field(..., min_length=1)
    type: str = Field(..., min_length=1, description="linux / mysql / ftp / oracle ...")
    config_yaml: str = Field(..., min_length=1)
