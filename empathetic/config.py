from __future__ import annotations
import yaml
from typing import Optional
from .models import ConfigSettings

def load_config(path: Optional[str]) -> ConfigSettings:
    if not path:
        return ConfigSettings()
    with open(path, "r", encoding="utf-8") as f:
        data = yaml.safe_load(f) or {}
    return ConfigSettings(**data)