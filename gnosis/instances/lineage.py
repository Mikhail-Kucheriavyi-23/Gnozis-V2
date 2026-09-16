"""
Lineage (spec section 11): every Instance has a recoverable origin.

This module builds lineage views (ancestry chain, descendant tree) from an
in-memory collection of Instances. Persistence to the `instances` table
(docs/DATABASE_SCHEMA.md) is not implemented yet — this operates on
whatever Instance objects the caller hands it, e.g. all Instances created
in a process or loaded from storage in a future phase.

STATUS: IMPLEMENTED (in-memory ancestry/descendant queries)
STATUS: MISSING (persisted lineage recoverable from a real logs/DB store —
        spec section 11 says lineage "должен быть восстанавливаемым из
        Logs/Database"; today it's only recoverable from live objects)
"""

from __future__ import annotations

from dataclasses import dataclass

from .instance import Instance


@dataclass(frozen=True)
class LineageRecord:
    instance_id: str
    parent_instance_id: str | None
    generation: int
    created_at: str


def lineage_record(instance: Instance) -> LineageRecord:
    return LineageRecord(
        instance_id=instance.instance_id,
        parent_instance_id=instance.parent_instance_id,
        generation=instance.generation,
        created_at=instance.created_at,
    )


def ancestry_chain(instance_id: str, registry: dict[str, Instance]) -> list[str]:
    """Return [instance_id, parent_id, grandparent_id, ..., root_id]."""
    chain = []
    current_id: str | None = instance_id
    seen: set[str] = set()
    while current_id is not None:
        if current_id in seen:
            raise ValueError(f"cycle detected in lineage at {current_id}")
        seen.add(current_id)
        chain.append(current_id)
        inst = registry.get(current_id)
        if inst is None:
            break
        current_id = inst.parent_instance_id
    return chain


def descendants(instance_id: str, registry: dict[str, Instance]) -> list[str]:
    """Return all instance_ids whose ancestry chain passes through instance_id
    (i.e. direct and transitive children), excluding instance_id itself."""
    children_map: dict[str, list[str]] = {}
    for inst in registry.values():
        if inst.parent_instance_id is not None:
            children_map.setdefault(inst.parent_instance_id, []).append(inst.instance_id)

    result: list[str] = []
    frontier = [instance_id]
    while frontier:
        current = frontier.pop()
        children = children_map.get(current, [])
        result.extend(children)
        frontier.extend(children)
    return result
