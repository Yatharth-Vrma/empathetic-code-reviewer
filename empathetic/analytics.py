from __future__ import annotations
from .models import TransformationOutput, Analytics

__all__ = ["compute_analytics"]

def compute_analytics(out: TransformationOutput) -> TransformationOutput:
    if not out.comments:
        out.analytics = Analytics(
            avg_positive_length=0,
            avg_why_length=0,
            resource_link_count=0,
            positivity_score=0.0
        )
        return out
    positives = [len(c.positive_rephrasing.split()) for c in out.comments]
    whys = [len(c.why.split()) for c in out.comments]
    resources = sum(len(c.resources) for c in out.comments)
    positivity = sum(1 for c in out.comments if c.positive_rephrasing) / len(out.comments)
    out.analytics = Analytics(
        avg_positive_length=sum(positives)/len(positives),
        avg_why_length=sum(whys)/len(whys),
        resource_link_count=resources,
        positivity_score=positivity,
    )
    return out