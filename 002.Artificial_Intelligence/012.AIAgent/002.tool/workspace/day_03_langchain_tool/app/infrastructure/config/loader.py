# -*- coding: utf-8 -*-
from __future__ import annotations

from pathlib import Path

import yaml

# app/infrastructure/config/loader.py → 上溯 3 层到项目根
BASE_DIR = Path(__file__).resolve().parents[3]
CONFIG_PATH = BASE_DIR / "config.local.yml"


def load_config() -> dict:
    if not CONFIG_PATH.exists():
        example = BASE_DIR / "config.example.yml"
        raise FileNotFoundError(
            f"缺少 {CONFIG_PATH.name}，请先复制 {example.name} 为 config.local.yml"
        )
    return yaml.safe_load(CONFIG_PATH.read_text(encoding="utf-8")) or {}
