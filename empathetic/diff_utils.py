from __future__ import annotations
import difflib

__all__ = ["unified_diff"]

def unified_diff(original: str, suggested: str) -> str:
    """Return a unified diff string between original and suggested code.

    Provides minimal context for readability. Lines are split preserving
    newline semantics via splitlines().
    """
    orig_lines = original.splitlines()
    new_lines = suggested.splitlines()
    diff = difflib.unified_diff(orig_lines, new_lines, lineterm="")
    return "\n".join(diff)