from empathetic.severity import classify_severity

def test_severity_high():
    assert classify_severity("This causes a crash") == "high"

def test_severity_medium():
    assert classify_severity("This is inefficient") == "medium"

def test_severity_low():
    assert classify_severity("Maybe style tweak") == "low"