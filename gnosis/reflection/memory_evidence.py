"""Read-only projection of durable evolution memory into Reflection evidence."""
from __future__ import annotations
from dataclasses import dataclass
from gnosis.storage.evolution_memory import EvolutionMemoryRecord

@dataclass(frozen=True)
class EvolutionEvidence:
    memory_id: str
    candidate_id: str
    transition_id: str
    outcome: str
    evidence: tuple[str, ...]


def project_evolution_memory(records: tuple[EvolutionMemoryRecord, ...], *, limit: int = 100) -> tuple[EvolutionEvidence, ...]:
    """Expose verified memory as evidence only; never creates authority or candidates."""
    if limit < 1:
        raise ValueError("limit must be >= 1")
    return tuple(EvolutionEvidence(r.memory_id, r.candidate_id, r.transition_id, r.outcome, r.evidence)
                 for r in records[:limit])
