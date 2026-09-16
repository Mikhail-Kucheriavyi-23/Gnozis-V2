# THREAT MODEL — GNOSIS 2.0

Status: DRAFT (Phase 0 deliverable). Covers actors and unauthorized actions
that the architecture must structurally prevent. This is not a formal
security audit — it is the enumeration that invariants/tests in Phase 1+
are checked against.

## Actors

| Actor | Description | Trust level |
|---|---|---|
| Core | The verified state-transition engine itself | Fully trusted by definition — but has no privileged bypass; even Core's own generator goes through `verify()` |
| Human User | Owns one or more Instances/Agents | Untrusted for direct state mutation; trusted only via Capabilities it holds |
| Human Agent | A User's agent identity inside the system | Same as User, scoped by Capability |
| Gnozis Agent | An agent formed from a verified Instance (Phase 5/6) | Untrusted beyond its granted Capabilities |
| External Agent | Any agent outside this Instance (another Gnozis instance, another AI, a human via Bridge) | Least trusted; reaches Core only via Bridge + Capability check |
| Memory subsystem | Persistent storage layer (Phase 4) | Trusted for read/write of its own records; MUST NOT have a path to mutate Core directly |
| Bridge | External interface (Phase 8) | Trusted to enforce Capability checks; MUST NOT expose Core mutation to the outside world |

## Unauthorized actions that MUST be structurally impossible

These map directly to the security tests in spec section 42 and to
`tests/test_evolution.py`.

1. **Any actor mutates `State` without going through `Candidate → Test → Verify → Commit`.**
   - Status: IMPLEMENTED & TESTED. `Engine.state` is only ever reassigned
     inside `Engine.step()`, and only after `verify()` returns `passed=True`.
     There is no setter, no public field write path, nothing else in the
     codebase touches `Engine.state`.
2. **A rejected Candidate partially or fully mutates Core state.**
   - Status: IMPLEMENTED & TESTED (`test_rejected_candidate_never_mutates_core_state`).
3. **Budget goes negative / an actor runs unbounded operations.**
   - Status: IMPLEMENTED & TESTED (`test_budget_cannot_go_negative`).
4. **A Candidate claims a stale or forged parent state and gets applied anyway.**
   - Status: IMPLEMENTED & TESTED (`test_candidate_from_stale_parent_is_rejected`,
     `check_state_integrity`).
5. **User or External Agent bypasses Capability checks.** — NOT YET
   APPLICABLE: no Capability system exists yet (Phase 5/8). Flagged as
   MISSING, not silently assumed safe.
6. **Memory subsystem is given a mutation path into Core.** — NOT YET
   APPLICABLE: no Memory subsystem exists yet (Phase 4). The architecture
   in `docs/ARCHITECTURE.md`-to-be must keep Memory reads/writes isolated
   from `Engine.state` when it's built.
7. **Invalid or forged cryptographic identity is accepted.** — NOT YET
   APPLICABLE: no Identity layer exists yet (Phase 5).
8. **Revoked identity or capability is still honored.** — NOT YET
   APPLICABLE: same as above.
9. **Replay of an old, already-committed Candidate/Message.** — NOT YET
   APPLICABLE: no Message/Federation layer exists yet (Phase 7).
10. **External world data (Bridge/Internet) flows directly into Core state without passing through Candidate/Test/Verify.**
    - Status: STRUCTURALLY IMPOSSIBLE TODAY because no Bridge exists yet — but
      this is a "not applicable," not a proof. When Phase 8 is built, Bridge
      output MUST be wrapped as a `Candidate` like any other proposal; this
      requirement is recorded here so it isn't forgotten when Bridge is added.

## What this threat model does NOT cover yet

Everything gated on Phase 3+ (Instance isolation across clones/forks,
cross-Instance Federation trust, Agent lifecycle attacks, Bridge-specific
attacks like SSRF/data exfiltration via External Agent). Each of those
phases must extend this document before being marked IMPLEMENTED — a
threat model written in advance of the code it covers, per spec section 50
("не добавлять функциональность, если неизвестно ... как действие
ограничивается").
