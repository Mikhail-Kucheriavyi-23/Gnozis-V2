"""
Phase 3: Instance / Clone / Fork / Lineage (spec sections 10-12).

An Instance wraps an independent Engine (its own State, Budget, history).
Clone and Fork are distinct operations (spec section 10):

    Clone(Psi) -> Psi'      # clone a STATE, not memory-shared
    Fork(G_i) -> G_j        # produce a new INDEPENDENT Instance

Neither operation shares Core State or memory between the two sides after
the operation completes — each Instance is autonomous (spec section 12).

STATUS: IMPLEMENTED (Instance, clone_state, fork_instance, lineage-of a
        given instance map). No persistence (storage/database.py) yet —
        everything here is in-process only; see STATUS.md.
STATUS: MISSING (cryptographic Identity per instance — Phase 5; Capability
        enforcement on who may fork/clone — Phase 5/8)
"""
