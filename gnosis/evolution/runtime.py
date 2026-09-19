"""Minimal bounded runtime orchestration for endogenous capability experiments.

This module composes existing evolution primitives without activating or mutating
canonical Core state. It is intentionally a vertical slice:
history -> gap -> capability -> candidate -> sandbox -> evaluation -> evidence.
"""
from __future__ import annotations

import sqlite3
from dataclasses import dataclass
from typing import Any, Callable, Mapping, Sequence

from gnosis.core.types import Candidate, State, TransitionRecord
from gnosis.core.verification import TestFn
from .capability import CapabilityHypothesis, CapabilitySynthesizer
from .evaluator import ComparativeEvaluation, EvaluationResult, EvidenceSufficiency, Outcome, ReplicatedEvidence, assess_evidence_sufficiency, assess_replicated_evidence, evaluate_observation, evaluate_outcomes
from .gap import GapDetector, GapHypothesis, history_from_persisted_transitions
from .provenance import EvidenceProvenance, build_provenance
from .sandbox import ObservationFn, SandboxBudget, SandboxResult, run_sandbox
from .transaction import EvolutionTransactionResult, persist_evolution_transaction
from gnosis.reflection.shadow import ShadowEvaluation, evaluate_shadow
from .selection import SelectionResult, select_for_review


@dataclass(frozen=True)
class RuntimeSliceResult:
    """Complete result of one bounded, non-authoritative evolution experiment."""

    gap: GapHypothesis
    capability: CapabilityHypothesis
    candidate: Candidate
    sandbox: SandboxResult
    evaluation: EvaluationResult
    provenance: EvidenceProvenance
    transaction: EvolutionTransactionResult
    shadow: ShadowEvaluation | None = None
    comparison: ComparativeEvaluation | None = None
    sufficiency: EvidenceSufficiency | ReplicatedEvidence | None = None
    selection: SelectionResult | None = None


def capability_candidate(state: State, capability: CapabilityHypothesis) -> Candidate:
    """Encode a capability hypothesis as an uncommitted Core Candidate.

    The returned proposed state is only the sandbox candidate. This function
    never calls Engine.step(), persists Core state, or grants authority.
    """
    proposed_state = state.with_elements(
        {
            "__gnozis_capability__": {
                "capability_id": capability.capability_id,
                "source_gap_id": capability.source_gap_id,
                "mechanism": capability.mechanism,
                "expected_effects": capability.expected_effects,
                "resource_bound": capability.resource_bound,
                "available_operations": capability.available_operations,
                "test_strategy": capability.test_strategy,
            }
        }
    )
    return Candidate(
        parent_state_id=state.state_id,
        proposed_state=proposed_state,
        origin="evolution:capability-hypothesis",
    )


def _default_observer(state: State, candidate: Candidate) -> Mapping[str, Any]:
    """Observe only the bounded candidate representation.

    This deliberately proves execution/evidence plumbing, not capability
    usefulness. A richer evaluator can be supplied by the caller.
    """
    capability = candidate.proposed_state.elements.get("__gnozis_capability__")
    return {
        "parent_state_id": state.state_id,
        "candidate_id": candidate.candidate_id,
        "capability": capability,
    }


def run_bounded_candidate(
    *,
    conn: sqlite3.Connection,
    state: State,
    candidate: Candidate,
    transitions: Sequence[TransitionRecord],
    observe: ObservationFn | None = None,
    sandbox_budget: SandboxBudget = SandboxBudget(),
    predicate: str = "observations_present",
    minimum_repetitions: int = 2,
    baseline_outcomes: tuple[Outcome, ...] | None = None,
    candidate_outcomes: tuple[Outcome, ...] | None = None,
    minimum_delta: float = 0.0,
) -> RuntimeSliceResult:
    """Run a supplied Candidate through the common bounded evidence path.

    This shared boundary is non-authoritative and never mutates canonical Core state.
    """
    from gnosis.reflection.persistence import ensure_reflection_schema
    ensure_reflection_schema(conn)
    sandbox = run_sandbox(state, candidate, observe or _default_observer, budget=sandbox_budget)
    evaluation = evaluate_observation(
        sandbox.execution.observations,
        evidence_digest=sandbox.execution.evidence_digest,
        predicate=predicate,
    ) if sandbox.accepted_for_evaluation else EvaluationResult(
        "REJECTED",
        (f"sandbox execution status: {sandbox.execution.status}",),
        sandbox.execution.evidence_digest,
    )
    comparison = None
    sufficiency = None
    selection = None
    if baseline_outcomes is not None or candidate_outcomes is not None:
        if not baseline_outcomes or not candidate_outcomes:
            raise ValueError("baseline_outcomes and candidate_outcomes must be supplied together")
        comparison = evaluate_outcomes(
            baseline=baseline_outcomes[0], candidate=candidate_outcomes[0],
            minimum_delta=minimum_delta,
        )
        sufficiency = assess_replicated_evidence(
            baselines=baseline_outcomes, candidates=candidate_outcomes,
            minimum_repetitions=minimum_repetitions, minimum_delta=minimum_delta,
        )
        selection = select_for_review(
            candidate_id=candidate.candidate_id,
            comparison=comparison,
            sufficiency=sufficiency,
        )
    provenance = build_provenance(
        candidate_id=candidate.candidate_id,
        parent_state_id=state.state_id,
        parent_state_digest=state.content_id,
        proposed_state_digest=candidate.proposed_state.content_id,
        proposed_state_content_id=candidate.proposed_state.content_id,
        candidate_binding_digest=candidate.binding_digest(state.content_id),
        observations=sandbox.execution.observations,
        evidence_digest=sandbox.execution.evidence_digest,
        evaluation_status=evaluation.status,
        shadow_status="NOT_RUN",
        invariant_status="UNCHANGED",
        governance_decision="REVIEW",
    )
    transaction = persist_evolution_transaction(
        conn, provenance, event_type="BOUNDED_RUNTIME_EVIDENCE",
        payload={
            "gap_id": "external-candidate",
            "capability_id": "external-candidate",
            "candidate_id": candidate.candidate_id,
            "sandbox_status": sandbox.execution.status,
            "evaluation_status": evaluation.status,
            "comparison_status": comparison.status if comparison else "NOT_RUN",
            "sufficiency_status": sufficiency.status if sufficiency else "NOT_RUN",
            "selection_status": selection.status if selection else "NOT_RUN",
            "activation": False,
        },
    )
    return RuntimeSliceResult(
        gap=GapHypothesis(source_records=(), gap_id="external-candidate", tension="external", rationale=("external candidate",)),
        capability=CapabilityHypothesis(capability_id="external-candidate", source_gap_id="external-candidate", mechanism="external", expected_effects=(), resource_bound=1, available_operations=(), test_strategy="external"),
        candidate=candidate, sandbox=sandbox, evaluation=evaluation,
        provenance=provenance, transaction=transaction,
        comparison=comparison, sufficiency=sufficiency, selection=selection,
    )


def run_runtime_slice(
    *,
    conn: sqlite3.Connection,
    state: State,
    transitions: Sequence[TransitionRecord],
    observe: ObservationFn | None = None,
    available_operations: Sequence[str] = ("observe", "record"),
    resource_bound: int = 1,
    sandbox_budget: SandboxBudget = SandboxBudget(),
    predicate: str = "observations_present",
    minimum_repetitions: int = 2,
    active_test: TestFn | None = None,
    shadow_test: TestFn | None = None,
    baseline_outcome: Outcome | None = None,
    candidate_outcome: Outcome | None = None,
    baseline_outcomes: tuple[Outcome, ...] | None = None,
    candidate_outcomes: tuple[Outcome, ...] | None = None,
    minimum_delta: float = 0.0,
    min_confidence: float = 0.95,
) -> RuntimeSliceResult:
    """Execute one complete bounded evolution slice and persist its evidence.

    The canonical state supplied by the caller is never replaced or persisted
    by this function. Only candidate/evidence provenance is persisted.
    """
    from gnosis.reflection.persistence import ensure_reflection_schema

    ensure_reflection_schema(conn)
    history = history_from_persisted_transitions(transitions)
    gaps = GapDetector().detect(
        history=history,
        minimum_repetitions=minimum_repetitions,
    )
    if not gaps:
        raise ValueError("no repeated unresolved gap was detected")

    capability = CapabilitySynthesizer().synthesize(
        gaps[0],
        available_operations=available_operations,
        resource_bound=resource_bound,
    )[0]
    candidate = capability_candidate(state, capability)

    sandbox = run_sandbox(
        state,
        candidate,
        observe or _default_observer,
        budget=sandbox_budget,
    )

    evaluation = evaluate_observation(
        sandbox.execution.observations,
        evidence_digest=sandbox.execution.evidence_digest,
        predicate=predicate,
    ) if sandbox.accepted_for_evaluation else EvaluationResult(
        "REJECTED",
        (f"sandbox execution status: {sandbox.execution.status}",),
        sandbox.execution.evidence_digest,
    )

    shadow: ShadowEvaluation | None = None
    shadow_status = "NOT_RUN"
    if (active_test is None) != (shadow_test is None):
        raise ValueError("active_test and shadow_test must be supplied together")
    if active_test is not None and shadow_test is not None:
        shadow = evaluate_shadow((candidate,), active_test, shadow_test)
        shadow_status = shadow.status

    comparison: ComparativeEvaluation | None = None
    sufficiency: EvidenceSufficiency | None = None
    selection: SelectionResult | None = None
    repeated_mode = baseline_outcomes is not None or candidate_outcomes is not None
    if repeated_mode:
        if baseline_outcomes is None or candidate_outcomes is None:
            raise ValueError("baseline_outcomes and candidate_outcomes must be supplied together")
        if not baseline_outcomes or not candidate_outcomes:
            raise ValueError("repeated outcomes must not be empty")
        comparison = evaluate_outcomes(baseline=baseline_outcomes[0], candidate=candidate_outcomes[0], minimum_delta=minimum_delta)
        sufficiency = assess_replicated_evidence(
            baselines=baseline_outcomes, candidates=candidate_outcomes,
            minimum_repetitions=minimum_repetitions, minimum_delta=minimum_delta,
        )
    else:
        if (baseline_outcome is None) != (candidate_outcome is None):
            raise ValueError("baseline_outcome and candidate_outcome must be supplied together")
        if baseline_outcome is not None and candidate_outcome is not None:
            comparison = evaluate_outcomes(baseline=baseline_outcome, candidate=candidate_outcome, minimum_delta=minimum_delta)
            sufficiency = assess_evidence_sufficiency(
                baseline=baseline_outcome, candidate=candidate_outcome,
                minimum_delta=minimum_delta, min_confidence=min_confidence,
            )
    if comparison is not None and sufficiency is not None:
        selection = select_for_review(candidate_id=candidate.candidate_id, comparison=comparison, sufficiency=sufficiency)

    candidate_binding_digest = candidate.binding_digest(state.content_id)
    provenance = build_provenance(
        candidate_id=candidate.candidate_id,
        parent_state_id=state.state_id,
        parent_state_digest=state.content_id,
        proposed_state_digest=candidate.proposed_state.content_id,
        proposed_state_content_id=candidate.proposed_state.content_id,
        candidate_binding_digest=candidate_binding_digest,
        observations=sandbox.execution.observations,
        evidence_digest=sandbox.execution.evidence_digest,
        evaluation_status=evaluation.status,
        shadow_status=shadow_status,
        invariant_status="UNCHANGED",
        governance_decision="REVIEW",
    )
    transaction = persist_evolution_transaction(
        conn,
        provenance,
        event_type="BOUNDED_RUNTIME_EVIDENCE",
        payload={
            "gap_id": capability.source_gap_id,
            "capability_id": capability.capability_id,
            "candidate_id": candidate.candidate_id,
            "sandbox_status": sandbox.execution.status,
            "evaluation_status": evaluation.status,
            "comparison_status": comparison.status if comparison else "NOT_RUN",
            "sufficiency_status": sufficiency.status if sufficiency else "NOT_RUN",
            "selection_status": selection.status if selection else "NOT_RUN",
            "activation": False,
        },
    )
    return RuntimeSliceResult(
        gap=gaps[0],
        capability=capability,
        candidate=candidate,
        sandbox=sandbox,
        evaluation=evaluation,
        provenance=provenance,
        transaction=transaction,
        shadow=shadow,
        comparison=comparison,
        sufficiency=sufficiency,
        selection=selection,
    )
