"""Read-only Shadow -> Invariant Delta -> Governance evidence gate."""
from __future__ import annotations
from dataclasses import dataclass
from typing import Mapping, Sequence
from gnosis.core.invariants import InvariantCheck
from gnosis.core.types import Candidate, State
from .shadow import ShadowEvaluation, evaluate_shadow
from .invariant_delta import InvariantDelta, analyze_invariant_delta
from .governance import GovernanceDecision, evaluate_governance

@dataclass(frozen=True)
class ReflectionEvidenceGateResult:
    passed: bool
    shadow: ShadowEvaluation
    invariant_delta: InvariantDelta
    governance: GovernanceDecision
    reasons: tuple[str, ...] = ()

def run_reflection_evidence_gate(candidates: Sequence[Candidate], active_test, shadow_test, current_states: Mapping[str, State], invariants: Sequence[InvariantCheck]) -> ReflectionEvidenceGateResult:
    reasons=[]
    try:
        shadow=evaluate_shadow(candidates, active_test, shadow_test)
        delta=analyze_invariant_delta(shadow,candidates,current_states,invariants)
        governance=evaluate_governance(shadow,delta)
    except Exception as exc:
        empty=ShadowEvaluation((),0,0,0,0,0,"NO_INPUT")
        empty_delta=InvariantDelta((),(),(),(),{}, {})
        decision=GovernanceDecision("HOLD","NO_INPUT","INSUFFICIENT_EVIDENCE",(f"evidence generation failed: {type(exc).__name__}",))
        return ReflectionEvidenceGateResult(False,empty,empty_delta,decision,("evidence generation failed",))
    if governance.can_activate or governance.can_rollback:
        reasons.append("governance evidence must not grant authority")
    if governance.decision == "BLOCK" and not (shadow.regressions or delta.violated):
        reasons.append("BLOCK lacks blocking evidence")
    if governance.decision == "REVIEW" and shadow.status != "BEHAVIOR_CHANGED" and not delta.improved:
        reasons.append("REVIEW lacks behavioral or invariant improvement evidence")
    if governance.decision == "HOLD" and not (shadow.status == "NO_INPUT" or delta.status == "INSUFFICIENT_EVIDENCE"):
        reasons.append("HOLD lacks insufficient-evidence condition")
    return ReflectionEvidenceGateResult(not reasons,shadow,delta,governance,tuple(reasons))
