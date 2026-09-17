# Gnozis-V2 — AI Context

## Canonical repository

- Canonical development repository: `Mikhail-Kucheriavyi-23/Gnozis-V2`
- Legacy `Gnozis` remains an archival research source and historical provenance.
- `AI_CONTEXT.md` is the operational handoff document for participating AI systems.
- `docs/AI_HANDOFF_PROTOCOL.md` is the canonical continuation/recovery protocol for replacing or adding AI agents at any project stage.

## Current verified repository baseline

- Branch: `main`
- Current documentation baseline after handoff-protocol addition: `8a8f0c1f22942bc6e5df21386525f4b753824499`.
- Ψ-Core remains the source of truth for state/evolution semantics.
- `gnosis/storage/` is implemented in the current `main`; older context claiming that it is missing is obsolete.
- Persistence is accepted in `main` following the project's independent verification gate.
- Current implementation must always be checked against source, tests and CI rather than inferred from historical documentation.

## Current implementation state

- Ψ-Core: `IMPLEMENTED`.
- Instance/lineage: `PARTIAL`; durable persistence is now present, while cryptographic Identity is future scope.
- Persistence: `IMPLEMENTED / ACCEPTED` in the canonical repository; implementation and verification evidence remain separately traceable.
- Append-only audit storage: `IMPLEMENTED` at the storage layer; broader phase-level verification remains subject to the recorded gates.
- Memory: `NOT ACCEPTED` and not merged into `main`.
- Identity and cryptography: `MISSING`.
- Agents and federation: `MISSING` as Gnozis runtime architecture.
- User/world bridge: `MISSING`.
- Endogenous generation: `PARTIAL` / `THEORETICAL` boundary; current generation remains caller-supplied.

## Persistence source of truth

The current storage layer contains:

```text
gnosis/storage/database.py
gnosis/storage/repositories.py
gnosis/storage/__init__.py
```

The database layer currently defines `SCHEMA_VERSION = 3`, enables SQLite foreign keys, uses `BEGIN IMMEDIATE` transaction boundaries, persists states/candidates/instances/transitions, and defines append-only `audit_events` with SQLite update/delete guards.

Persistence is accepted in canonical `main`. Do not restart or duplicate the Persistence implementation because of stale historical documents.

## Multi-agent project governance — FIXED WORKING MODEL

Gnozis is developed through multiple AI systems working against the same canonical project artifacts. Access to project data is broader than authority to modify the canonical architecture.

**GitHub / Google Drive access does not by itself grant architectural authority.**

### Mandatory phase chain

```text
access
  ↓
explicit task
  ↓
bounded implementation
  ↓
independent verification
  ↓
correction
  ↓
re-verification
  ↓
ChatGPT integration gate
  ↓
context/status update
```

### ChatGPT — architecture / integration / final gate

- maintains architectural direction and Ψ-Core invariants;
- defines bounded tasks, acceptance criteria and forbidden changes;
- reconciles Claude/Manus/auditor findings;
- performs the integration/final gate under the project owner's authorization;
- synchronizes canonical context and status.

### Claude — primary implementation engineer

- implements explicitly assigned bounded engineering phases;
- adds and runs tests available in its environment;
- documents implementation and limitations;
- performs corrective passes after independent findings;
- does not self-certify final acceptance.

### Manus — independent reviewer / adversarial engineer

- reads actual source or artifacts;
- reproduces tests where possible;
- searches for hidden coupling, missing invariants, security defects and unsupported claims;
- may perform an explicitly assigned corrective pass;
- does not grant final project acceptance.

### Gemini / other connected AI systems

Depending on explicit assignment, a connected AI may act as implementation contributor, auditor, adversarial tester, research/comparison source, or runtime observer. Its output is evidence or a proposal, not automatic architectural authority.

## Phase authority

Before each substantive phase, record:

```text
Primary implementer:
Independent reviewer:
ChatGPT final gate:
External audit required: yes/no
Allowed files/scope:
Forbidden changes:
```

The same AI should not implement and independently certify the same phase unless an explicit exception is documented by the project owner.

## Evidence hierarchy

When reports conflict:

1. actual current source code;
2. reproducible runtime behavior and real tests/CI;
3. accepted project invariants/contracts;
4. independent audit evidence;
5. AI reports and design proposals.

A textual `PASS`, `implemented`, `complete`, or `ready` claim is never sufficient evidence by itself.

Every CI claim must identify the exact tested commit SHA. Implementation state and verification state must remain separate.

## Core protection

The following require explicit task scope and final review:

- `gnosis/core/*`;
- persistence semantics;
- Identity and capability boundaries;
- security/encryption boundaries;
- Memory/Core boundary;
- Bridge/Core boundary;
- federation/trust semantics;
- self-modification/evolution rules.

No connected AI may silently redefine these through implementation convenience. No AI model belongs inside Ψ-Core.

## Runtime → architecture feedback

The project intentionally builds the core while exercising it in real runtime conditions. Runtime observations may reveal missing requirements, invariants or useful interfaces. They become canonical architectural requirements only after explicit review and documentation.

The engineering loop is:

```text
Build → Execute → Test → Attack → Correct → Re-test → Gate → Record → Build next
```

This is an engineering strategy; it does not mean Gnozis is currently autonomous or federated.

## Current phase status

### Persistence

Persistence is already in canonical `main` and is accepted after independent verification. Do not restart or duplicate the Persistence implementation because of stale historical documents.

### Multi-agent strategy

`docs/MULTI_AGENT_BUILD_STRATEGY.md` and `AGENT_ROLES.md` define the current governance model. The strategy has been independently reviewed as `PASS WITH FINDINGS`; the principal documentation-drift finding is addressed by the current synchronization.

### Memory

Memory is **NOT ACCEPTED** and is not present in canonical `main`.

A separately delivered Claude Memory artifact was independently audited and found to require a corrective pass. The currently assigned corrective items are:

- H-01 — reject cross-owner/cross-instance supersession;
- H-03 — reject self/direct/indirect supersession cycles;
- H-04 — enforce provenance validation on the write path;
- M-01 — enforce root/version continuity;
- M-02 — enforce the retention state machine.

The corrective Memory artifact must remain outside `main` until the independent re-audit passes and ChatGPT performs the integration gate.

## Current mandatory sequence

```text
STATUS.md / AI_CONTEXT.md synchronization
        ↓
Manus read-only documentation audit
        ↓
Memory corrective pass
        ↓
Manus full Memory re-audit with real pytest
        ↓
ChatGPT integration gate
```

No Memory corrective implementation is part of the documentation synchronization step.

## Context recovery procedure

A new AI session must read, in order:

1. `AI_CONTEXT.md`;
2. `STATUS.md`;
3. `docs/AI_HANDOFF_PROTOCOL.md`;
4. relevant specification/schema documents;
5. relevant source files;
6. relevant tests;
7. latest CI status.

Then report:

- current branch;
- current HEAD;
- latest CI-tested commit;
- implementation state using `IMPLEMENTED / PARTIAL / MISSING / THEORETICAL`;
- verification qualifiers separately;
- any mismatch between current HEAD and tested commit.

Never assume an earlier AI report is proof of implementation.

## Status vocabulary

Use these as primary implementation states:

- `IMPLEMENTED` — implementation exists and required evidence supports the claim;
- `PARTIAL` — some implementation exists but required behavior is incomplete;
- `MISSING` — specified but not implemented;
- `THEORETICAL` — design/research only.

Use verification qualifiers separately, for example `VERIFIED_BY_TESTS`, `VERIFIED_BY_CI`, `UNVERIFIED`, or `BLOCKED`.

## Open evolution boundary

As Gnozis approaches autonomous/self-directed evolution, the governance model must be revisited. Future autonomous modification requires independent verification of identity, capabilities, authorization, bounded operations, proof/invariants, rollback, durable auditability, recovery, conflict resolution and human override.

No claim of autonomous self-development should be made until those mechanisms are implemented and independently verified.
