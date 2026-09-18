import sqlite3
import pytest
from gnosis.core import Candidate, State
from gnosis.instances.instance import Instance
from gnosis.storage import append_evolution_memory, connect, load_evolution_memory, save_instance


def test_evolution_memory_round_trip_and_digest():
    conn=connect(); instance=Instance.create_root("u", State(elements={"a":1})); save_instance(conn,instance)
    proposed=instance.engine.state.with_elements({"b":2}); candidate=Candidate(instance.engine.state.state_id,proposed,"reflection:endogenous")
    record=instance.engine.step(candidate)
    from gnosis.storage.repositories import persist_transition
    persist_transition(conn,instance,candidate,record,actor="test")
    tid=conn.execute("SELECT transition_id FROM transitions WHERE candidate_id=?",(candidate.candidate_id,)).fetchone()[0]
    mem=append_evolution_memory(conn,instance_id=instance.instance_id,candidate_id=candidate.candidate_id,transition_id=tid,state_id=proposed.state_id,proposal_id="proposal:1",outcome="accepted",evidence=("finding:1","observation:1"))
    loaded=load_evolution_memory(conn,instance.instance_id)
    assert loaded==(mem,)
    assert mem.digest==mem.memory_id


def test_evolution_memory_is_append_only():
    conn=connect(); instance=Instance.create_root("u", State(elements={"a":1})); save_instance(conn,instance)
    proposed=instance.engine.state.with_elements({"b":2}); candidate=Candidate(instance.engine.state.state_id,proposed,"test")
    record=instance.engine.step(candidate)
    from gnosis.storage.repositories import persist_transition
    persist_transition(conn,instance,candidate,record,actor="test")
    tid=conn.execute("SELECT transition_id FROM transitions WHERE candidate_id=?",(candidate.candidate_id,)).fetchone()[0]
    append_evolution_memory(conn,instance_id=instance.instance_id,candidate_id=candidate.candidate_id,transition_id=tid,state_id=proposed.state_id,proposal_id=None,outcome="rejected",evidence=("rejected",))
    with pytest.raises(sqlite3.DatabaseError): conn.execute("DELETE FROM evolution_memory")
    with pytest.raises(sqlite3.DatabaseError): conn.execute("UPDATE evolution_memory SET outcome='accepted'")


def test_evolution_memory_rejects_unknown_outcome():
    conn=connect()
    with pytest.raises(ValueError): append_evolution_memory(conn,instance_id="i",candidate_id="c",transition_id="t",state_id="s",proposal_id=None,outcome="accepted-ish",evidence=())
