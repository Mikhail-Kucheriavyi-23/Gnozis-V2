from gnosis.core import Candidate, State
from gnosis.instances.clone import clone_state
from gnosis.instances.fork import fork_instance
from gnosis.instances.instance import Instance, InstanceStatus
from gnosis.instances.lineage import ancestry_chain, descendants, lineage_record


def make_root() -> Instance:
    initial = State(elements={"a": 1}, version=0)
    return Instance.create_root(owner_id="user-1", initial_state=initial)


def test_create_root_has_no_parent_and_generation_zero():
    root = make_root()
    assert root.parent_instance_id is None
    assert root.generation == 0
    assert root.status == InstanceStatus.ACTIVE


def test_clone_state_produces_independent_container():
    original = State(elements={"a": 1}, version=0)
    cloned = clone_state(original)
    assert cloned.elements == original.elements
    assert cloned is not original
    assert cloned.elements is not original.elements
    # content-identical states hash identically (deterministic id)
    assert cloned.state_id == original.state_id


def test_fork_creates_independent_instance_with_incremented_generation():
    root = make_root()
    child = fork_instance(root)
    assert child.parent_instance_id == root.instance_id
    assert child.generation == root.generation + 1
    assert child.instance_id != root.instance_id
    # same content at fork time
    assert child.engine.state.state_id == root.engine.state.state_id


def test_fork_isolation_child_mutation_never_touches_parent_state():
    """SECURITY/ISOLATION TEST (spec 42 analogue for Instances): mutating the
    forked child's Core State must never affect the parent's Core State."""
    root = make_root()
    child = fork_instance(root)

    parent_state_before = root.engine.state
    proposed = child.engine.state.with_elements({"only_in_child": True})
    candidate = Candidate(
        parent_state_id=child.engine.state.state_id, proposed_state=proposed, origin="test"
    )
    record = child.engine.step(candidate)

    assert record.accepted
    assert "only_in_child" in child.engine.state.elements
    # parent completely unaffected
    assert root.engine.state is parent_state_before
    assert "only_in_child" not in root.engine.state.elements


def test_fork_isolation_budgets_are_independent():
    root = make_root()
    child = fork_instance(root)
    proposed = child.engine.state.with_elements({"x": 1})
    candidate = Candidate(
        parent_state_id=child.engine.state.state_id, proposed_state=proposed, origin="test"
    )
    child.engine.step(candidate)
    assert child.engine.budget.spent == 1
    assert root.engine.budget.spent == 0  # untouched


def test_fork_defaults_owner_to_parent_owner():
    root = make_root()
    child = fork_instance(root)
    assert child.owner_id == root.owner_id


def test_fork_can_be_assigned_different_owner():
    root = make_root()
    child = fork_instance(root, owner_id="user-2")
    assert child.owner_id == "user-2"


def test_ancestry_chain_and_descendants():
    root = make_root()
    child = fork_instance(root)
    grandchild = fork_instance(child)

    registry = {
        root.instance_id: root,
        child.instance_id: child,
        grandchild.instance_id: grandchild,
    }

    chain = ancestry_chain(grandchild.instance_id, registry)
    assert chain == [grandchild.instance_id, child.instance_id, root.instance_id]

    desc = descendants(root.instance_id, registry)
    assert set(desc) == {child.instance_id, grandchild.instance_id}


def test_lineage_record_captures_expected_fields():
    root = make_root()
    child = fork_instance(root)
    rec = lineage_record(child)
    assert rec.instance_id == child.instance_id
    assert rec.parent_instance_id == root.instance_id
    assert rec.generation == 1
