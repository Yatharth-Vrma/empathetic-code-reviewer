from . import cli  # noqa: F401 ensures Typer app is discoverable

__all__ = ["cli", "run", "batch"]

# Re-export convenience functions if needed
try:
    run = cli.run  # type: ignore[attr-defined]
    batch = cli.batch  # type: ignore[attr-defined]
except AttributeError:  # pragma: no cover
    pass