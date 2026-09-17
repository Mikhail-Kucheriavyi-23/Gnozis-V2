"""Atomic persistence boundary for an evidence-gated Core promotion."""
from __future__ import annotations

import hashlib
import sqlite3

from .materialization import CoreVersionDescriptor
from .promotion import PromotionCandidate
from .recursive import ReEvaluationResult
from gnosis.core.types import State
from gnosis.storage.database import transaction
from gnosis.storage.repositories import (
    StorageCorruptionError,
    append_audit,
    canonical_json,
    load_instance,
    save_state,
    utc_now,
)


class PromotionPersistenceError(ValueError):
    """Raised when an atomic promotion cannot be persisted safely."""


def _evidence_digest(candidate: PromotionCandidate, reevaluation: ReEvaluationResult) -> str:
    payload = {
        "candidate_model_id": candidate.model_id,
        "candidate_evidence": {
            "model_id": candidate.evidence.model_id,
            "passed": candidate.evidence.passed,
            "score": candidate.evidence.score,
            "reasons": tuple(candidate.evidence.reasons),
        },
        "rounds": [
            {
                "model_id": item.model_id,
                "passed": item.passed,
                "score": item.score,
                "reasons": tuple(item.reasons),
            }
            for item in reevaluation.rounds
        ],
    }
    return hashlib.sha256(canonical_json(payload).encode("utf-8")).hexdigest()


def _promotion_id(
    instance_id: str,
    descriptor: CoreVersionDescriptor,
    evidence_digest: str,
) -> str:
    raw = canonical_json(
        {
            "instance_id": instance_id,
            "version_id": descriptor.version_id,
            "parent_state_id": descriptor.parent_state_id,
            "proposed_state_id": descriptor.proposed_state_id,
            "candidate_model_id": descriptor.candidate_model_id,
            "evidence_digest": evidence_digest,
        }
    )
    return hashlib.sha256(raw.encode("utf-8")).hexdigest()


def persist_promotion(
    conn: sqlite3.Connection,
    *,
    instance_id: str,
    current_state: State,
    proposed_state: State,
    candidate: PromotionCandidate,
    reevaluation: ReEvaluationResult,
    descriptor: CoreVersionDescriptor,
    actor: str,
    failure_at: str | None = None,
) -> str:
    """Atomically persist a validated Core_n -> Core_(n+1) promotion.

    The authoritative instance head is updated only inside the same
    transaction that writes the proposed state, promotion provenance and
    append-only audit event. Any exception rolls the entire operation back.
    """
    if not candidate.can_promote:
        raise PromotionPersistenceError("promotion candidate is not eligible")
    if not reevaluation.stable:
        raise PromotionPersistenceError("promotion candidate is not stable")
    if not descriptor.ready:
        raise PromotionPersistenceError("promotion descriptor is not ready")
    if descriptor.parent_state_id != current_state.state_id:
        raise PromotionPersistenceError("descriptor parent does not match current state")
    if descriptor.proposed_state_id != proposed_state.state_id:
        raise PromotionPersistenceError("descriptor proposed state does not match proposed state")
    if descriptor.candidate_model_id != candidate.model_id:
        raise PromotionPersistenceError("descriptor model mismatch")
    if descriptor.evidence_rounds != len(reevaluation.rounds):
        raise PromotionPersistenceError("evidence round count mismatch")
    if proposed_state.state_id == current_state.state_id:
        raise PromotionPersistenceError("promotion must change Core state")

    evidence_digest = _evidence_digest(candidate, reevaluation)
    promotion_id = _promotion_id(instance_id, descriptor, evidence_digest)

    def inject(point: str) -> None:
        if failure_at == point:
            raise RuntimeError(f"injected promotion failure at {point}")

    with transaction(conn):
        inject("after_begin")
        instance = load_instance(conn, instance_id)
        if instance.engine.state.state_id != current_state.state_id:
            raise PromotionPersistenceError("stale canonical Core head")

        existing = conn.execute(
            "SELECT promotion_id,proposed_state_id FROM promotions WHERE instance_id=? AND parent_state_id=?",
            (instance_id, current_state.state_id),
        ).fetchone()
        if existing is not None:
            if existing[0] == promotion_id and existing[1] == proposed_state.state_id:
                return promotion_id
            raise PromotionPersistenceError("a different promotion already exists for this parent state")

        save_state(conn, proposed_state, created_at=utc_now())
        inject("after_state")
        conn.execute(
            "INSERT INTO promotions(promotion_id,instance_id,parent_state_id,proposed_state_id,hypothesis_id,model_id,descriptor_version_id,evidence_digest,evidence_rounds,created_at) VALUES(?,?,?,?,?,?,?,?,?,?)",
            (
                promotion_id,
                instance_id,
                current_state.state_id,
                proposed_state.state_id,
                candidate.hypothesis_id,
                candidate.model_id,
                descriptor.version_id,
                evidence_digest,
                len(reevaluation.rounds),
                utc_now(),
            ),
        )
        inject("after_promotion")
        append_audit(
            conn,
            actor=actor,
            action="core.promote",
            resource=instance_id,
            result="accepted",
            event_key=f"promotion:{promotion_id}",
        )
        inject("after_audit")
        conn.execute(
            "UPDATE instances SET current_state_id=? WHERE instance_id=? AND current_state_id=?",
            (proposed_state.state_id, instance_id, current_state.state_id),
        )
        if conn.execute("SELECT changes()").fetchone()[0] != 1:
            raise StorageCorruptionError("promotion head update affected unexpected row count")
        inject("after_head")
        inject("before_commit")

    return promotion_id
