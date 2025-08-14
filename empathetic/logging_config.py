from __future__ import annotations
import logging, sys

__all__ = ["setup_logging"]

def setup_logging(level: str = "INFO") -> None:
    root = logging.getLogger()
    if root.handlers:
        return
    handler = logging.StreamHandler(sys.stdout)
    fmt = logging.Formatter("[%(levelname)s] %(name)s: %(message)s")
    handler.setFormatter(fmt)
    root.addHandler(handler)
    root.setLevel(level)