"""Deterministic evaluation of sandbox evidence."""
from __future__ import annotations
from dataclasses import dataclass
from typing import Any,Mapping
@dataclass(frozen=True)
class EvaluationResult:
    status:str; rationale:tuple[str,...]; evidence_digest:str
def evaluate_observation(observations:Mapping[str,Any],*,evidence_digest:str,predicate:str)->EvaluationResult:
    if not evidence_digest: return EvaluationResult("INSUFFICIENT_EVIDENCE",("missing evidence digest",),"")
    if not observations: return EvaluationResult("INSUFFICIENT_EVIDENCE",("sandbox produced no observations",),evidence_digest)
    if predicate!="observations_present": return EvaluationResult("REVIEW",("evidence requires an explicit evaluator implementation",),evidence_digest)
    return EvaluationResult("PASS",("sandbox observations are present and digest-linked",),evidence_digest)
