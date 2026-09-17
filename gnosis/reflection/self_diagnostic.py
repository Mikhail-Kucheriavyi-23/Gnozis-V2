"""Read-only diagnostic surface for asking Core what it can justify changing."""
from __future__ import annotations

from dataclasses import dataclass
from typing import Sequence

from gnosis.core.types import TransitionRecord

from .analyzer import ReflectionAnalyzer
from .causal import CausalCandidate, attribute_finding, refine_proposal_target


@dataclass(frozen=True)
class SelfDiagnostic:
    report: object
    causal_candidates: tuple[CausalCandidate, ...]
    refined_proposals: tuple[object, ...]
    limitations: tuple[str, ...]


def diagnose(transitions: Sequence[TransitionRecord], minimum_repetitions: int = 2) -> SelfDiagnostic:
    report = ReflectionAnalyzer(transitions).analyze(minimum_repetitions=minimum_repetitions)
    causal = tuple(attribute_finding(f, transitions) for f in report.findings)
    by_finding = {c.finding_id: c for c in causal}
    proposals = tuple(
        refine_proposal_target(p, by_finding[p.finding_id])
        for p in report.proposals
        if p.finding_id in by_finding
    )
    limitations = (
        "Recorded Test rule provenance is evidence of rule application, not proof of deeper causality.",
        "The diagnostic cannot propose a source-code patch or activate a rule.",
        "Missing provenance remains UNSPECIFIED rather than inferred.",
    )
    return SelfDiagnostic(report, causal, proposals, limitations)
