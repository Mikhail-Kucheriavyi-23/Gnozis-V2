"""Cumulative analysis of previously persisted reflection evidence.

This layer is deliberately read-only. It turns prior reflection reports into
new evidence about persistence, recurrence and unresolved proposals; it does
not activate rules or modify Core.
"""

from __future__ import annotations

from collections import Counter
from dataclasses import dataclass
from typing import Any, Iterable, Mapping


@dataclass(frozen=True)
class ReflectionHistorySummary:
    report_count: int
    finding_count: int
    proposal_count: int
    unresolved_proposal_count: int
    counterexample_statuses: tuple[tuple[str, int], ...]
    recurring_finding_ids: tuple[str, ...]


@dataclass(frozen=True)
class HistoricalFinding:
    finding_id: str
    occurrences: int
    latest_claim: str
    proposal_statuses: tuple[str, ...]


def _payload(report: Mapping[str, Any]) -> Mapping[str, Any]:
    value = report.get("payload", report)
    return value if isinstance(value, Mapping) else {}


def summarize_reflection_history(
    reports: Iterable[Mapping[str, Any]],
) -> ReflectionHistorySummary:
    reports = tuple(reports)
    finding_counts: Counter[str] = Counter()
    proposal_count = 0
    unresolved = 0
    finding_claims: dict[str, str] = {}
    proposal_statuses: dict[str, list[str]] = {}
    counterexample_statuses: Counter[str] = Counter()

    for stored in reports:
        payload = _payload(stored)
        findings = payload.get("findings", ())
        proposals = payload.get("proposals", ())
        results = payload.get("counterexample_results", ())

        for finding in findings if isinstance(findings, list) else ():
            if not isinstance(finding, Mapping):
                continue
            finding_id = str(finding.get("finding_id", ""))
            if not finding_id:
                continue
            finding_counts[finding_id] += 1
            finding_claims[finding_id] = str(finding.get("claim", ""))

        for proposal in proposals if isinstance(proposals, list) else ():
            if not isinstance(proposal, Mapping):
                continue
            proposal_count += 1
            proposal_id = str(proposal.get("proposal_id", ""))
            status = str(proposal.get("status", "PROPOSED"))
            if proposal_id:
                proposal_statuses.setdefault(proposal_id, []).append(status)
            if status not in {"ACCEPTED", "REJECTED", "SUPERSEDED"}:
                unresolved += 1

        for result in results if isinstance(results, list) else ():
            if not isinstance(result, Mapping):
                continue
            counterexample_statuses[str(result.get("status", "UNKNOWN"))] += 1

    recurring = tuple(sorted(fid for fid, count in finding_counts.items() if count > 1))
    return ReflectionHistorySummary(
        report_count=len(reports),
        finding_count=sum(finding_counts.values()),
        proposal_count=proposal_count,
        unresolved_proposal_count=unresolved,
        counterexample_statuses=tuple(sorted(counterexample_statuses.items())),
        recurring_finding_ids=recurring,
    )


def unresolved_findings(
    reports: Iterable[Mapping[str, Any]],
) -> tuple[HistoricalFinding, ...]:
    """Return recurring findings whose proposals have not reached a terminal status."""
    reports = tuple(reports)
    findings: dict[str, int] = Counter()
    claims: dict[str, str] = {}
    statuses: dict[str, list[str]] = {}

    for stored in reports:
        payload = _payload(stored)
        for finding in payload.get("findings", ()) if isinstance(payload.get("findings", ()), list) else ():
            if isinstance(finding, Mapping):
                fid = str(finding.get("finding_id", ""))
                if fid:
                    findings[fid] += 1
                    claims[fid] = str(finding.get("claim", ""))
        for proposal in payload.get("proposals", ()) if isinstance(payload.get("proposals", ()), list) else ():
            if isinstance(proposal, Mapping):
                fid = str(proposal.get("finding_id", ""))
                if fid:
                    statuses.setdefault(fid, []).append(str(proposal.get("status", "PROPOSED")))

    result = []
    terminal = {"ACCEPTED", "REJECTED", "SUPERSEDED"}
    for fid in sorted(findings):
        current = tuple(statuses.get(fid, ()))
        if findings[fid] > 1 and not current or current and current[-1] not in terminal:
            result.append(HistoricalFinding(fid, findings[fid], claims.get(fid, ""), current))
    return tuple(result)
