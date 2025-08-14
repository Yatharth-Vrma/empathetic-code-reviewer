from empathetic.diff_utils import unified_diff

def test_diff_basic():
    orig = "x=1\ny=2"
    new = "x=1\ny=3"
    d = unified_diff(orig, new)
    assert "-y=2" in d and "+y=3" in d