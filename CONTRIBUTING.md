# Contributing

## Development Setup
```bash
python -m venv .venv
source .venv/bin/activate
pip install -e .[dev]
pre-commit install  # if you add a config later
```

## Running Tests
```bash
pytest -q
```

## CLI Usage (Dev)
```bash
empathetic run --input examples/sample_input.json --output report.md --emit-json --enable-diff
```
Add `GEMINI_API_KEY` via export or `.env`. Install dotenv extra if you want auto-loading.

## Code Style
- Ruff for lint/format
- Mypy for typing
- Target Python 3.11+

## Commit Guidelines
- Conventional commits encouraged (feat:, fix:, docs:, refactor:, test:, chore:).

## Adding Principles
Update:
- style_guidelines.py
- PROMPT_ENGINEERING.md taxonomy section
- tests if new principle needs coverage

## Pull Request Checklist
- [ ] Tests pass
- [ ] Added/updated docs
- [ ] No banned phrases in prompt templates
- [ ] Coverage not decreased
- [ ] CLI still works with and without GEMINI_API_KEY