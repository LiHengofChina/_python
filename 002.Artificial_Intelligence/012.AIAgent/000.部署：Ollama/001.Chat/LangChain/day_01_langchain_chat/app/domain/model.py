# -*- coding: utf-8 -*-
from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class ChatReply:
    question: str
    answer: str
