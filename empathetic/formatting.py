from __future__ import annotations
from typing import Dict, Optional
from .models import TransformationOutput

__all__ = ["render_markdown"]

def render_markdown(output: TransformationOutput, code_snippet: str, diffs: Optional[Dict[str,str]] = None) -> str:
    lines = ["# Empathetic Code Review Report", "", "## Original Code", "```python", code_snippet, "```"]
    lines.append("\n## Transformed Comments")
    for c in output.comments:
        lines.append(f"### Original: {c.original}")
        lines.append(f"*Severity:* {c.severity} | *Principle:* {c.principle}")
        lines.append(f"**Positive Rephrasing:** {c.positive_rephrasing}")
        lines.append(f"**Why:** {c.why}")
        if c.suggested_code.strip():
            lines.append("**Suggested Improvement:**")
            lines.append("```python")
            lines.append(c.suggested_code)
            lines.append("```")
        if diffs and c.original in diffs and diffs[c.original].strip():
            lines.append("**Diff:**")
            lines.append("```diff")
            lines.append(diffs[c.original])
            lines.append("```")
        if c.resources:
            lines.append("**Resources:**")
            for r in c.resources:
                lines.append(f"- {r}")
        lines.append("")
    s = output.summary
    lines.append("## Summary")
    lines.append(f"**Tone:** {s.overall_tone_observation}")
    lines.append("**Principles Distribution:**")
    for k,v in s.key_principles_distribution.items():
        lines.append(f"- {k}: {v}")
    lines.append(f"**Encouraging Overview:** {s.encouraging_overview}")
    if s.next_learning_steps:
        lines.append("**Next Steps:**")
        for step in s.next_learning_steps:
            lines.append(f"- {step}")
    return "\n".join(lines) + "\n"