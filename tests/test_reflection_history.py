from gnosis.reflection.history import summarize_reflection_history, unresolved_findings


def _report(index, status="PROPOSED"):
    return {
        "report_id": f"reflection:{index}",
        "payload": {
            "findings": [{
                "finding_id": "finding:A",
                "claim": "recurring rejection",
            }],
            "proposals": [{
                "proposal_id": "proposal:A",
                "finding_id": "finding:A",
                "status": status,
            }],
            "counterexample_results": [{"status": "INCONCLUSIVE"}],
        },
    }


def test_summary_detects_recurrence_and_unresolved_proposal():
    summary = summarize_reflection_history((_report(1), _report(2)))
    assert summary.report_count == 2
    assert summary.finding_count == 2
    assert summary.proposal_count == 2
    assert summary.unresolved_proposal_count == 2
    assert summary.recurring_finding_ids == ("finding:A",)
    assert summary.counterexample_statuses == (("INCONCLUSIVE", 2),)


def test_terminal_proposal_removes_finding_from_unresolved_set():
    result = unresolved_findings((_report(1, "ACCEPTED"), _report(2, "ACCEPTED")))
    assert result == ()


def test_unresolved_findings_are_deterministic():
    result = unresolved_findings((_report(2), _report(1)))
    assert len(result) == 1
    assert result[0].finding_id == "finding:A"
    assert result[0].occurrences == 2
