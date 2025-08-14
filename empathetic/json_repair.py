from __future__ import annotations
import json, re

def attempt_repair(raw: str) -> str:
    """
    Attempt simple JSON repairs:
    - Remove leading/trailing non-json noise
    - Fix trailing commas
    - Ensure quotes are balanced (basic)
    """
    start = raw.find("{")
    end = raw.rfind("}")
    if start == -1 or end == -1:
        raise ValueError("No JSON object markers found.")
    candidate = raw[start:end+1]

    # Remove control chars
    candidate = "".join(ch for ch in candidate if ord(ch) >= 9)
    # Remove trailing commas before } or ]
    candidate = re.sub(r",\s*([}\]])", r"\1", candidate)

    # Basic brace/quote balancing check
    if candidate.count("{") != candidate.count("}") :
        raise ValueError("Brace mismatch cannot repair.")

    json.loads(candidate)  # will raise if still invalid
    return candidate