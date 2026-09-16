"""
Fork (spec section 10): Fork(G_i) -> G_j.

Produces a brand-new, independent Instance whose starting State is a clone
of the parent's CURRENT state at fork time, but whose Engine (state history,
budget) is entirely separate going forward. Fork does NOT mean shared Core
State (spec section 10: "Fork не означает общий Core State").

STATUS: IMPLEMENTED
"""

from __future__ import annotations

from gnosis.core import Budget, Engine

from .clone import clone_state
from .instance import Instance, InstanceStatus, _new_id, _now


def fork_instance(parent: Instance, owner_id: str | None = None, budget: Budget | None = None) -> Instance:
    """Create a new Instance forked from `parent`.

    `owner_id` defaults to the parent's owner (same user forking their own
    instance); pass an explicit owner_id to model a fork handed to a
    different user.
    """
    forked_state = clone_state(parent.engine.state)
    new_engine = Engine(state=forked_state, budget=budget or Budget())
    return Instance(
        instance_id=_new_id(),
        owner_id=owner_id if owner_id is not None else parent.owner_id,
        engine=new_engine,
        parent_instance_id=parent.instance_id,
        generation=parent.generation + 1,
        status=InstanceStatus.ACTIVE,
        created_at=_now(),
    )
