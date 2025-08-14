from __future__ import annotations
import json
import typer
from pathlib import Path
from rich.console import Console
from .models import InputPayload
from .config import load_config
from .pipeline import ReviewPipeline
from .logging_config import setup_logging

app = typer.Typer()
console = Console()


def main_run(
    input_path: Path,
    output_path: Path,
    persona: str = "mentor",
    developer_level: str = "mid",
    enable_diff: bool = False,
    emit_json: bool = False,
    self_critique_passes: int = 1,
    config: Path | None = None,
    model_name: str = "gemini-1.5-pro",
    temperature: float = 0.4,
):
    setup_logging()
    cfg = load_config(str(config) if config else None)
    cfg.persona = persona
    cfg.developer_level = developer_level  # type: ignore
    cfg.enable_diff = enable_diff
    cfg.emit_json = emit_json
    cfg.self_critique_passes = self_critique_passes
    cfg.model_name = model_name
    cfg.temperature = temperature

    payload = InputPayload(**json.loads(input_path.read_text(encoding="utf-8")))
    pipeline = ReviewPipeline(cfg)
    output_obj, markdown, issues = pipeline.run(payload)

    output_path.write_text(markdown, encoding="utf-8")
    console.print(f"[green]Markdown report written to {output_path}[/green]")

    if emit_json:
        meta = output_path.with_suffix(".metadata.json")
        meta.write_text(json.dumps(output_obj.dict(), indent=2, ensure_ascii=False), encoding="utf-8")
        console.print(f"[blue]Metadata JSON written to {meta}[/blue]")

    if issues:
        console.print("[yellow]Heuristic issues detected:[/yellow]")
        for i in issues:
            console.print(f" - {i}")

    return output_obj


@app.command()
def run(
    input: Path = typer.Option(..., "--input", exists=True),
    output: Path = typer.Option(..., "--output"),
    persona: str = typer.Option("mentor"),
    developer_level: str = typer.Option("mid"),
    enable_diff: bool = typer.Option(False),
    emit_json: bool = typer.Option(False),
    self_critique_passes: int = typer.Option(1),
    config: Path | None = typer.Option(None, "--config"),
    model_name: str = typer.Option("gemini-1.5-pro"),
    temperature: float = typer.Option(0.4),
):
    main_run(
        input_path=input,
        output_path=output,
        persona=persona,
        developer_level=developer_level,
        enable_diff=enable_diff,
        emit_json=emit_json,
        self_critique_passes=self_critique_passes,
        config=config,
        model_name=model_name,
        temperature=temperature,
    )


@app.command()
def batch(
    batch_dir: Path = typer.Option(..., "--batch-dir", exists=True, file_okay=False),
    out_dir: Path = typer.Option(..., "--out-dir"),
    persona: str = typer.Option("mentor"),
    developer_level: str = typer.Option("mid"),
    enable_diff: bool = typer.Option(False),
    emit_json: bool = typer.Option(False),
    self_critique_passes: int = typer.Option(1),
    config: Path | None = typer.Option(None, "--config"),
    model_name: str = typer.Option("gemini-1.5-pro"),
    temperature: float = typer.Option(0.4),
):
    out_dir.mkdir(parents=True, exist_ok=True)
    for f in batch_dir.glob("*.json"):
        out_file = out_dir / f"{f.stem}.md"
        main_run(
            input_path=f,
            output_path=out_file,
            persona=persona,
            developer_level=developer_level,
            enable_diff=enable_diff,
            emit_json=emit_json,
            self_critique_passes=self_critique_passes,
            config=config,
            model_name=model_name,
            temperature=temperature,
        )

if __name__ == "__main__":  # pragma: no cover
    app()