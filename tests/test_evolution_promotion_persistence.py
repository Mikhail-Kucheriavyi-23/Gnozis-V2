import pytest

from gnosis.core import State
from gnosis.evolution.evaluator import ModelEvidence
from gnosis.evolution.materialization import CoreVersionDescriptor
from gnosis.evolution.promotion import PromotionCandidate
from gnosis.evolution.promotion_persistence import (
    PromotionPersistenceError,
    persist_promotion,
)
from gnosis.evolution.recursive import ReEvaluationResult
from gnosis.evolution.hypothesis import EvolutionHypothesis
from gnosis.instances.instance import Instance
from gnosis.storage.database import connect
from gnosis.storage.repositories import save_instance, save_state
from gnosis.reflection.invariant_delta import InvariantDelta


def fixture():
    current = State(elements={"a": 1}, version=0)
    proposed = current.with_elements({"b": 2})
    hypothesis = EvolutionHypothesis(
        hypothesis_id="h1",
        target="core",
        rationale="validated improvement",
        expected_effects=("b added",),
        constraints=("bounded",),
    )
    evidence = ModelEvidence("h1:model:1", True, 1.0, ("stable",))
    candidate = PromotionCandidate(
        hypothesis_id="h1",
        model_id=evidence.model_id,
        evidence=evidence,
        invariant_delta=InvariantDelta(
            preserved=("state-valid",),
            violated=(),
            improved=(),
            unknown=(),
            active_violations={},
            shadow_violations={},
        ),
    )
    reevaluation = ReEvaluationResult(
        rounds=tuple(ModelEvidence("h1:model:1", True, 1.0, ("stable",)) for _ in range(3)),
        stable=True,
    )
    descriptor = CoreVersionDescriptor(
        version_id=f"{current.state_id}->{proposed.state_id}",
        parent_state_id=current.state_id,
        proposed_state_id=proposed.state_id,
        candidate_model_id="h1:model:1",
        evidence_rounds=3,
    )
    return current, proposed, candidate, reevaluation, descriptor


def test_promotion_updates_head_and_writes_provenance_atomically():
    conn = connect()
    current, proposed, candidate, reevaluation, descriptor = fixture()
    instance = Instance.create_root("owner", current)
    save_instance(conn, instance)

    promotion_id = persist_promotion(
        conn,
        instance_id=instance.instance_id,
        current_state=current,
        proposed_state=proposed,
        candidate=candidate,
        reevaluation=reevaluation,
        descriptor=descriptor,
        actor="promotion-test",
    )

    row = conn.execute(
        "SELECT proposed_state_id,model_id,evidence_rounds FROM promotions WHERE promotion_id=?",
        (promotion_id,),
    ).fetchone()
    head = conn.execute(
        "SELECT current_state_id FROM instances WHERE instance_id=?",
        (instance.instance_id,),
    ).fetchone()
    audit = conn.execute(
        "SELECT action,result FROM audit_events WHERE event_id=?",
        (f"promotion:{promotion_id}",),
    ).fetchone()

    assert tuple(row) == (proposed.state_id, candidate.model_id, 3)
    assert head[0] == proposed.state_id
    assert tuple(audit) == ("core.promote", "accepted")


def test_failure_rolls_back_state_promotion_audit_and_head():
    conn = connect()
    current, proposed, candidate, reevaluation, descriptor = fixture()
    instance = Instance.create_root("owner", current)
    save_instance(conn, instance)

    with pytest.raises(RuntimeError, match="after_audit"):
        persist_promotion(
            conn,
            instance_id=instance.instance_id,
            current_state=current,
            proposed_state=proposed,
            candidate=candidate,
            reevaluation=reevaluation,
            descriptor=descriptor,
            actor="promotion-test",
            failure_at="after_audit",
        )

    assert conn.execute("SELECT 1 FROM states WHERE state_id=?", (proposed.state_id,)).fetchone() is None
    assert conn.execute("SELECT 1 FROM promotions").fetchone() is None
    assert conn.execute("SELECT 1 FROM audit_events WHERE action='core.promote'").fetchone() is None
    assert conn.execute(
        "SELECT current_state_id FROM instances WHERE instance_id=?", (instance.instance_id,)
    ).fetchone()[0] == current.state_id


def test_stale_parent_is_rejected_without_write():
    conn = connect()
    current, proposed, candidate, reevaluation, descriptor = fixture()
    instance = Instance.create_root("owner", current)
    save_instance(conn, instance)
    advanced = current.with_elements({"already": True})
    save_state(conn, advanced)
    conn.execute(
        "UPDATE instances SET current_state_id=? WHERE instance_id=?",
        (advanced.state_id, instance.instance_id),
    )

    with pytest.raises(PromotionPersistenceError, match="stale canonical Core head"):
        persist_promotion(
            conn,
            instance_id=instance.instance_id,
            current_state=current,
            proposed_state=proposed,
            candidate=candidate,
            reevaluation=reevaluation,
            descriptor=descriptor,
            actor="promotion-test",
        )

    assert conn.execute("SELECT COUNT(*) FROM promotions").fetchone()[0] == 0
