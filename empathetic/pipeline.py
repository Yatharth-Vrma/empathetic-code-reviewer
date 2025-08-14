from __future__ import annotations
import json, logging
from typing import Tuple, Dict
from pathlib import Path
from .models import InputPayload, ConfigSettings, TransformationOutput
from .llm_client import LLMClient
from .rewriting import parse_transformation
from .postprocessors import enrich
from .formatting import render_markdown
from .evaluators import heuristic_issues
from .analytics import compute_analytics
from .diff_utils import unified_diff

logger = logging.getLogger(__name__)

# Robust path resolution (previously assumed CWD = project root)
_PROJECT_ROOT = Path(__file__).resolve().parent.parent
_PROMPT_FILE = _PROJECT_ROOT / "PROMPT_ENGINEERING.md"
try:
    PROMPT_DOC = _PROMPT_FILE.read_text(encoding="utf-8")
except FileNotFoundError:
    logger.warning("PROMPT_ENGINEERING.md not found at %s", _PROMPT_FILE)
    PROMPT_DOC = ""

def build_user_prompt(payload: InputPayload, cfg: ConfigSettings) -> str:
    return (
        f"Developer Level: {cfg.developer_level}\n"
        f"Persona: {cfg.persona}\n"
        f"Warmth: {cfg.warmth} Formality: {cfg.formality} PedagogyDepth: {cfg.pedagogy_depth}\n"
        f"RAW_COMMENTS: {json.dumps(payload.review_comments, ensure_ascii=False)}\n"
        f"CODE:\n{payload.code_snippet}\n"
        "Return JSON then Markdown per spec."
    )

SYSTEM_PROMPT = "Refer to full System Prompt in PROMPT_ENGINEERING.md. Follow schema rigidly."

class ReviewPipeline:
    def __init__(self, cfg: ConfigSettings):
        self.cfg = cfg
        self.llm = LLMClient(cfg.model_name, cfg.temperature)

    def _refine(self, current: TransformationOutput) -> TransformationOutput:
        prompt = json.dumps(current.dict(), ensure_ascii=False)
        user = f"{prompt}\nRefine per critique rules. Return JSON ONLY."
        raw = self.llm.generate("Self-Critique Mode", user)
        try:
            refined = parse_transformation(raw, [c.original for c in current.comments])
            return refined
        except Exception:
            logger.warning("Refinement failed; keeping previous.")
            return current

    def run(self, payload: InputPayload) -> Tuple[TransformationOutput, str, list[str]]:
        user_prompt = build_user_prompt(payload, self.cfg)
        raw = self.llm.generate(SYSTEM_PROMPT, user_prompt)

        try:
            output = parse_transformation(raw, payload.review_comments)
        except Exception as e:
            logger.error(f"Initial parse failed: {e}")
            raise

        for _ in range(self.cfg.self_critique_passes):
            output = self._refine(output)

        output = enrich(output, self.cfg.max_resources)
        output = compute_analytics(output)

        diffs: Dict[str,str] = {}
        if self.cfg.enable_diff:
            # Attempt mapping original code to suggestion (best effort)
            for c in output.comments:
                if c.suggested_code.strip():
                    diffs[c.original] = unified_diff(payload.code_snippet, c.suggested_code)

        issues = heuristic_issues(output)
        markdown = render_markdown(output, payload.code_snippet, diffs=diffs if self.cfg.enable_diff else None)
        return output, markdown, issues