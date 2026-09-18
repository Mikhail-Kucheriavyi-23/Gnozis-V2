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
