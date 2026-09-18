from gnosis.reflection.memory_evidence import project_evolution_memory
from gnosis.storage.evolution_memory import EvolutionMemoryRecord


def test_memory_projects_to_read_only_reflection_evidence():
    r=EvolutionMemoryRecord("m","i","c","t","s",None,"rejected",("e1",),"2026-09-18T00:00:00+00:00")
    out=project_evolution_memory((r,))
    assert out[0].memory_id == "m"
    assert out[0].outcome == "rejected"
    assert out[0].evidence == ("e1",)


def test_memory_projection_is_bounded():
    records=tuple(EvolutionMemoryRecord(str(i),"i","c","t","s",None,"inconclusive",(),"2026-09-18T00:00:00+00:00") for i in range(5))
    assert len(project_evolution_memory(records, limit=2)) == 2


def test_cumulative_reflection_reads_instance_scoped_evolution_memory():
    from gnosis.core import State
    from gnosis.instances.instance import Instance
    from gnosis.reflection.runtime import reflect_with_history
    from gnosis.storage import append_evolution_memory, connect, save_instance
    conn=connect(); instance=Instance.create_root("u", State(elements={"a":1})); save_instance(conn, instance)
    result=reflect_with_history(instance.engine, conn, instance_id=instance.instance_id)
    assert result.evolution_evidence == ()
