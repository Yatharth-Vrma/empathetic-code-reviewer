from __future__ import annotations
from .models import TransformationOutput

__all__ = ["heuristic_issues"]

def heuristic_issues(out: TransformationOutput) -> list[str]:
    issues: list[str] = []
    if not out.comments:
        issues.append("No comments produced")
    for c in out.comments:
        if len(c.why.split()) < 3:
            issues.append(f"Why too short for comment: {c.original[:30]}")
    return issues