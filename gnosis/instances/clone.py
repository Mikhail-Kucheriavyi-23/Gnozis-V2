"""
Clone (spec section 10): Clone(Psi) -> Psi'.

Clone operates on a STATE, producing an independent copy with no shared
mutable memory. Because `State` is an immutable, frozen dataclass with
copied-in containers (see core/types.py State.__post_init__), the "clone"
is already structurally independent — but this function exists explicitly
so callers never rely on Python object identity/aliasing by accident, and
so intent is visible in the codebase per spec section 10's requirement to
"strictly distinguish" Clone from Fork/Instance.

STATUS: IMPLEMENTED
"""

from __future__ import annotations

from gnosis.core import Relation, State


def clone_state(state: State) -> State:
    """Return an independent State with identical content but guaranteed
    to share no mutable container with the original."""
    cloned_elements = {k: v for k, v in state.elements.items()}
    cloned_relations = tuple(
        Relation(
            source=r.source,
            target=r.target,
            relation_type=r.relation_type,
            value=r.value,
        )
        for r in state.relations
    )
    return State(elements=cloned_elements, relations=cloned_relations, version=state.version)
