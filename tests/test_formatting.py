from empathetic.formatting import render_markdown
from empathetic.models import TransformationOutput, CommentTransformed, Summary, Analytics

def test_markdown_render():
    out = TransformationOutput(
        comments=[
            CommentTransformed(
                original="Bad name",
                severity="low",
                principle="naming",
                positive_rephrasing="Great start—improve the variable name.",
                why="This improves readability by clarifying intent.",
                suggested_code="user = item",
                resources=["https://peps.python.org/pep-0008/#naming-conventions"],
                notes_internal=""
            )
        ],
        summary=Summary(
            overall_tone_observation="Neutral",
            key_principles_distribution={"naming":1},
            encouraging_overview="Solid foundation!",
            next_learning_steps=["Review naming conventions"]
        ),
        analytics=None
    )
    md = render_markdown(out, "print('hi')", diffs=None)
    assert "Empathetic Code Review Report" in md
    assert "Bad name" in md