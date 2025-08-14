from __future__ import annotations
import json
from typing import List
from .models import TransformationOutput
from .severity import classify_severity
from .json_repair import attempt_repair

__all__ = ["parse_transformation", "extract_json_block"]

def extract_json_block(text: str) -> str:
    start = text.find("{")
    end = text.rfind("}")
    if start == -1 or end == -1:
        raise ValueError("No JSON braces found.")
    return text[start:end+1]

def parse_transformation(raw: str, originals: List[str]) -> TransformationOutput:
    """Parse raw model output into schema, attempting repair if needed.

    Steps:
      1. Extract outermost JSON braces heuristic.
      2. Attempt direct json.loads.
      3. On failure, run lightweight repair (balanced braces, commas) then parse.
      4. Ensure severity present for each comment via heuristic classifier.
    """
    try:
        json_block = extract_json_block(raw)
        data = json.loads(json_block)
    except Exception:
        repaired = attempt_repair(raw)
        data = json.loads(repaired)

    comments = data.get("comments", [])
    for i, c in enumerate(comments):
        if "severity" not in c or c.get("severity") not in ("low", "medium", "high"):
            if i < len(originals):
                c["severity"] = classify_severity(originals[i])
            else:  # pragma: no cover - defensive
                c["severity"] = "low"
    data["comments"] = comments
    return TransformationOutput(**data)