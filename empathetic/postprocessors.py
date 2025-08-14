from __future__ import annotations
from .models import TransformationOutput
from .style_guidelines import get_links_for_principle

BANNED = ["obviously","simply","just "," trivial","simply","just"]

def sanitize(text: str) -> str:
    out = text
    for b in BANNED:
        out = out.replace(b, "")
    return " ".join(out.split())

__all__ = ["enrich"]

def enrich(output: TransformationOutput, max_per: int) -> TransformationOutput:
    """Augment comments with style guideline links (up to max_per) and sanitize tone."""
    for c in output.comments:
        links = get_links_for_principle(c.principle)
        for l in links:
            if l not in c.resources and len(c.resources) < max_per:
                c.resources.append(l)
        c.positive_rephrasing = sanitize(c.positive_rephrasing)
        c.why = sanitize(c.why)
        c.resources = c.resources[:max_per]
    return output