import json
from empathetic.pipeline import ReviewPipeline
from empathetic.models import InputPayload, ConfigSettings

def test_pipeline_mock():
    cfg = ConfigSettings(self_critique_passes=0, enable_diff=True)
    payload = InputPayload(
        code_snippet="def f():\n    return 1",
        review_comments=["Inefficient"]
    )
    pipe = ReviewPipeline(cfg)
    out, md, issues = pipe.run(payload)
    assert out.comments
    assert "Empathetic Code Review Report" in md