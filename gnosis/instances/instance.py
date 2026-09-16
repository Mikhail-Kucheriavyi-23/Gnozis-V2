from __future__ import annotations

import uuid
from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum

from gnosis.core import Budget, Engine, State


class InstanceStatus(str, Enum):
    ACTIVE = "active"
    STOPPED = "stopped"
    ARCHIVED = "archived"


def _new_id() -> str:
    # NOTE: a UUID here is a record-keeping identifier only. It is NOT a
    # cryptographic proof of identity (spec section 26 explicitly warns
    # against treating a bare UUID as identity proof) — that is Phase 5.
    return str(uuid.uuid4())


def _now() -> str:
    return datetime.now(timezone.utc).isoformat()


@dataclass
class Instance:
    """An autonomous Gnozis Instance: its own protected Core + Engine.

    Instances do NOT share Engine objects, State objects, or budgets with
    each other — that is what "autonomous relative to other Instances"
    (spec section 12) means structurally in this slice.
    """

    instance_id: str
    owner_id: str
    engine: Engine
    parent_instance_id: str | None = None
    generation: int = 0
    status: InstanceStatus = InstanceStatus.ACTIVE
    created_at: str = field(default_factory=_now)

    @classmethod
    def create_root(cls, owner_id: str, initial_state: State, budget: Budget | None = None) -> "Instance":
        """Create a brand-new, generation-0 Instance (spec section 49, step 1+3)."""
        engine = Engine(state=initial_state, budget=budget or Budget())
        return cls(
            instance_id=_new_id(),
            owner_id=owner_id,
            engine=engine,
            parent_instance_id=None,
            generation=0,
        )
