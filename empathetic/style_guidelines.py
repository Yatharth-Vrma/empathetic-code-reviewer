from __future__ import annotations

STYLE_LINKS = {
    "naming": ["https://peps.python.org/pep-0008/#naming-conventions"],
    "pythonic_convention": ["https://peps.python.org/pep-0008/"],
    "performance": ["https://wiki.python.org/moin/TimeComplexity"],
    "readability": ["https://peps.python.org/pep-0008/#code-lay-out"],
    "maintainability": ["https://refactoring.guru/"],
}

__all__ = ["get_links_for_principle"]

def get_links_for_principle(principle: str) -> list[str]:
    return STYLE_LINKS.get(principle, [])