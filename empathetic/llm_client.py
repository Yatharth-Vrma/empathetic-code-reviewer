from __future__ import annotations
import os, json, logging
try:
    import google.generativeai as genai  # type: ignore
except ImportError:  # pragma: no cover - optional dependency
    genai = None  # type: ignore

logger = logging.getLogger(__name__)

class LLMClient:
    """Thin wrapper around Gemini API with a deterministic mock fallback.

    If the google.generativeai package or GEMINI_API_KEY is missing we fall back to
    a mock that returns a minimal valid JSON structure + trailing markdown header
    so downstream parsing & formatting paths remain exercised in tests.
    """
    def __init__(self, model_name: str, temperature: float):
        self.model_name = model_name
        self.temperature = temperature
        self._model = None
        api_key = os.environ.get("GEMINI_API_KEY")
        if genai and api_key:
            try:
                genai.configure(api_key=api_key)
                self._model = genai.GenerativeModel(model_name)  # type: ignore[attr-defined]
            except Exception as e:  # pragma: no cover - network / auth issues
                logger.warning("Gemini initialization failed (%s); using mock.", e)
        else:
            logger.warning("Gemini not initialized (missing package or API key) – using mock responses.")

    def generate(self, system_prompt: str, user_prompt: str) -> str:
        if not self._model:
            return self._mock(system_prompt, user_prompt)
        response = self._model.generate_content(  # type: ignore[call-arg]
            [system_prompt, user_prompt],
            generation_config={"temperature": self.temperature}
        )
        try:
            return response.text  # type: ignore[return-value]
        except AttributeError:  # pragma: no cover - defensive
            logger.error("Model response missing text; returning mock fallback.")
            return self._mock(system_prompt, user_prompt)

    def _mock(self, system_prompt: str, user_prompt: str) -> str:
        sample = {
            "comments": [{
                "original": "Sample comment",
                "severity": "low",
                "principle": "readability",
                "positive_rephrasing": "Nice foundation—clarifying this could help future maintainers.",
                "why": "This improves readability by making the intent explicit.",
                "suggested_code": "# example",
                "resources": [],
                "notes_internal": ""
            }],
            "summary": {
                "overall_tone_observation": "Neutral overall tone.",
                "key_principles_distribution": {"readability": 1},
                "encouraging_overview": "Solid base to iterate.",
                "next_learning_steps": ["Review naming conventions for clarity."]
            },
            "analytics": {
                "avg_positive_length": 7.0,
                "avg_why_length": 9.0,
                "resource_link_count": 0,
                "positivity_score": 1.0
            }
        }
        return json.dumps(sample) + "\n# Empathetic Code Review Report\n(Mock Markdown)"

__all__ = ["LLMClient"]