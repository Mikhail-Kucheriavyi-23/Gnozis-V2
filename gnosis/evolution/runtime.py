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
from .capability import CapabilityHypothesis, CapabilitySynthesizer
from .evaluator import EvaluationResult, evaluate_observation
from .gap import GapDetector, GapHypothesis, history_from_persisted_transitions
from .provenance import EvidenceProvenance, build_provenance
from .sandbox import ObservationFn, SandboxBudget, SandboxResult, run_sandbox
from .transaction import EvolutionTransactionResult, persist_evolution_transaction


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
        shadow_status="NOT_RUN",
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
    )
