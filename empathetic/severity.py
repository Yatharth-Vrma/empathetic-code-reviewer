from __future__ import annotations
from typing import Literal

__all__ = ["classify_severity"]

def classify_severity(comment: str) -> Literal["low","medium","high"]:
    lowered = comment.lower()
    if any(k in lowered for k in ["crash","security","exploit","data loss","incorrect","bug"]):
        return "high"
    if any(k in lowered for k in ["inefficient","slow","complex","confusing","bad"]):
        return "medium"
    return "low"