from __future__ import annotations
from pydantic import BaseModel, Field, validator
from typing import List, Literal, Optional, Dict

Principle = Literal["readability","performance","naming","style","maintainability","complexity","correctness","pythonic_convention","other"]
Severity = Literal["low","medium","high"]
DeveloperLevel = Literal["junior","mid","senior"]

class InputPayload(BaseModel):
    code_snippet: str
    review_comments: List[str]

    @validator("review_comments")
    def strip_empty(cls, v: List[str]) -> List[str]:
        return [c.strip() for c in v if c and c.strip()]

class CommentTransformed(BaseModel):
    original: str
    severity: Severity
    principle: Principle
    positive_rephrasing: str
    why: str
    suggested_code: str
    resources: List[str] = Field(default_factory=list)
    notes_internal: Optional[str] = ""

class Summary(BaseModel):
    overall_tone_observation: str
    key_principles_distribution: Dict[str, int]
    encouraging_overview: str
    next_learning_steps: List[str]

class Analytics(BaseModel):
    avg_positive_length: float
    avg_why_length: float
    resource_link_count: int
    positivity_score: float

class TransformationOutput(BaseModel):
    comments: List[CommentTransformed]
    summary: Summary
    analytics: Optional[Analytics] = None

class ConfigSettings(BaseModel):
    persona: str = "mentor"
    warmth: float = 0.85
    formality: float = 0.4
    pedagogy_depth: float = 0.75
    developer_level: DeveloperLevel = "mid"
    max_resources: int = 3
    self_critique_passes: int = 1
    enable_diff: bool = False
    emit_json: bool = False
    model_name: str = "gemini-1.5-pro"
    temperature: float = 0.4
    retry_attempts: int = 1