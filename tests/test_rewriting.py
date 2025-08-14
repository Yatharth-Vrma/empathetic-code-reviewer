from empathetic.rewriting import parse_transformation

def test_parse_transformation_basic():
    raw = '{"comments":[{"original":"c","severity":"low","principle":"readability","positive_rephrasing":"Good","why":"This improves readability.","suggested_code":"x=1","resources":[],"notes_internal":""}],"summary":{"overall_tone_observation":"ok","key_principles_distribution":{"readability":1},"encouraging_overview":"Nice","next_learning_steps":["Review naming"]},"analytics":{"avg_positive_length":1,"avg_why_length":4,"resource_link_count":0,"positivity_score":1}}'
    out = parse_transformation(raw, ["c"])
    assert out.comments[0].original == "c"