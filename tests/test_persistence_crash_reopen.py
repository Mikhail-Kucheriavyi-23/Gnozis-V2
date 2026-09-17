import pytest

from gnosis.core import Candidate, State
from gnosis.instances.instance import Instance
from gnosis.storage import connect, load_instance, persist_transition, save_instance, verify_durable_graph


CHECKPOINTS = [
    "before_begin",
    "after_begin",
    "after_candidate",
    "after_transition",
    "after_audit",
    "after_head",
    "before_commit",
]


def _prepare(path):
    conn = connect(path)
    instance = Instance.create_root("u", State(elements={"root": 0}))
    save_instance(conn, instance)
    proposed = instance.engine.state.with_elements({"next": 1})
    candidate = Candidate(instance.engine.state.state_id, proposed, "crash-test")
    record = instance.engine.step(candidate)
    return conn, instance, candidate, record, proposed


@pytest.mark.parametrize("point", CHECKPOINTS)
def test_crash_checkpoint_reopen_has_only_old_durable_state(tmp_path, point):
    path = tmp_path / f"{point}.sqlite"
    conn, instance, candidate, record, proposed = _prepare(path)
    with pytest.raises(RuntimeError, match="injected failure"):
        persist_transition(conn, instance, candidate, record, actor="u", failure_at=point)
    conn.close()

    reopened = connect(path)
    recovered = load_instance(reopened, instance.instance_id)
    assert recovered.engine.state.state_id == instance.engine.state.state_id
    assert recovered.engine.state.state_id != proposed.state_id
    assert reopened.execute("SELECT COUNT(*) FROM transitions").fetchone()[0] == 0
    assert reopened.execute("SELECT COUNT(*) FROM audit_events WHERE transition_id IS NOT NULL").fetchone()[0] == 0
    assert verify_durable_graph(reopened)[0] == 1


def test_after_commit_reopen_has_complete_new_state(tmp_path):
    path = tmp_path / "after-commit.sqlite"
    conn, instance, candidate, record, proposed = _prepare(path)
    with pytest.raises(RuntimeError, match="injected failure"):
        persist_transition(conn, instance, candidate, record, actor="u", failure_at="after_commit")
    conn.close()

    reopened = connect(path)
    recovered = load_instance(reopened, instance.instance_id)
    assert recovered.engine.state.state_id == proposed.state_id
    assert reopened.execute("SELECT COUNT(*) FROM transitions").fetchone()[0] == 1
    assert reopened.execute("SELECT COUNT(*) FROM audit_events WHERE transition_id IS NOT NULL").fetchone()[0] == 1
    assert verify_durable_graph(reopened)[0] == 2
