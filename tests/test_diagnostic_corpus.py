from pathlib import Path


def test_diagnostic_corpus_generator_exists_and_uses_persistence():
    source = Path("diagnostic_corpus/generate.py").read_text(encoding="utf-8")
    assert "persist_transition" in source
    assert "load_transition_records" in source
    assert "verify_durable_graph" in source
    assert "diagnose(recovered_history)" in source


def test_diagnostic_corpus_contract_is_four_transitions():
    source = Path("diagnostic_corpus/generate.py").read_text(encoding="utf-8")
    assert "assert len(recovered_history) == 4" in source
    assert "sum(not record.accepted for record in recovered_history) == 3" in source
    assert "sum(record.accepted for record in recovered_history) == 1" in source
    assert 'test-rule:diagnostic-policy' in source
