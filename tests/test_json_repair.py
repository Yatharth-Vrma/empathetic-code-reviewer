from empathetic.json_repair import attempt_repair

def test_attempt_repair_valid():
    raw = "noise {\"a\":1,} trailing stuff"
    repaired = attempt_repair(raw)
    assert repaired == '{"a":1}'

def test_attempt_repair_failure():
    try:
        attempt_repair("no braces here")
    except ValueError:
        assert True
    else:
        assert False, "Expected ValueError"