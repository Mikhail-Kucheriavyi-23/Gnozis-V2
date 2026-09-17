# Gnozis-V2 — AI Context

## Canonical repository

- Canonical development repository: `Mikhail-Kucheriavyi-23/Gnozis-V2`
- Legacy `Gnozis` remains an archival research source and historical provenance.
- `AI_CONTEXT.md` is the operational handoff document for participating AI systems.
- `docs/AI_HANDOFF_PROTOCOL.md` is the canonical continuation/recovery protocol for replacing or adding AI agents at any project stage.
- `docs/USER_ARCHITECTURE.md` is the canonical architecture document for user/task/context/capability continuity across connected terminals and products.

## Current verified repository baseline

- Branch: `main`.
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
- User-centered multi-terminal architecture: `DOCUMENTED / NOT IMPLEMENTED` — see `docs/USER_ARCHITECTURE.md`.
- Endogenous generation: `PARTIAL` / `THEORETICAL` boundary; current generation remains caller-supplied.

## Current working scope — SINGLE OWNER / SINGLE PROJECT

**This is the active scope of the present engineering phase.**

All architecture changes, repository modifications, integration work and testing are currently performed within the project owner's account and the single canonical repository `Gnozis-V2`. Multiple connected AI systems may participate as implementation, audit, research or review agents, but they operate against this one owner's project context.

The immediate practical experiment is:

```text
ONE OWNER / ONE ACCOUNT
│
├── ChatGPT
├── Claude
├── Manus
├── Gemini / other connected AI
├── GitHub
├── Google Drive / other connected tools
│
└──────────────→ Gnozis-V2
                  ↓
          Ψ-Core + Persistence
          + Audit + Reflection
          + future Evolution
```

The purpose of this phase is to prove that a project can retain durable context, state, provenance and work continuity when the user changes AI terminals or tools, and that several AI systems can cooperate without any one conversation being the canonical project memory.

**Do not implement multi-user, multi-tenant or federation infrastructure merely because it is described in the long-term architecture.** Those are future strategic layers.

Currently out of implementation scope:

- other user accounts;
- tenant isolation;
- cross-account identity;
- public user network;
- organization-wide permissions;
- inter-user federation;
- cross-account trust protocols;
- multi-tenant billing/access architecture;
- shared production workspace between independent account owners.

Future multi-user strategy may be designed later, after the single-owner architecture is implemented and tested. Its future existence must not contaminate the current Ψ-Core contracts.

## User-centered architecture — FIXED DESIGN DIRECTION

Gnozis is being built as a user-centered architecture in which continuity of work belongs to durable project/task context rather than to a particular AI terminal or product.

The canonical design document is `docs/USER_ARCHITECTURE.md`.

The target model is:

```text
USER
  ↓
TASK
  ↓
CONTEXT
  ↓
CAPABILITIES
  ↓
DATA / TOOLS / CONNECTORS
  ↓
CORE / EXECUTION
  ↓
VERIFIED RESULT
  ↓
PROVENANCE / MEMORY
```

Key architectural rules:

- any authorized connected terminal of the current owner should be able to reconstruct the relevant task/project context and continue work;
- conversational history is not the canonical source of project continuity;
- GitHub, Google Drive, AI terminals and other products are connectors/interfaces/capability providers, not automatic sources of truth;
- `Capability ≠ Authority` and `Resource access ≠ Architectural authority`;
- different user types (manager, programmer, engineer, physicist, researcher, analyst, etc.) are future users of the same architecture; specialization comes from task + context + data + authorized capabilities rather than separate Core engines;
- individuals may eventually cooperate without belonging to the same organization; this is future strategy, not current runtime implementation;
- shared task/context must not merge participant identities or permissions;
- notifications are entry points to durable tasks, not the canonical task state;
- results must remain distinguishable as verified facts, observations, calculations, proposals, or unresolved claims and retain provenance where applicable;
- task/context/capability layers must not introduce a second Ψ-Core state model or silently redefine Core semantics;
- this is an architectural target, not a claim that User/Task/Context/Capability runtime layers are already implemented.

The target continuity property is:

```text
Terminal A ─┐
Terminal B ─┼──→ shared canonical context/state ←── connectors
Terminal C ─┤
Terminal D ─┘
```

A terminal may disappear, reach a usage limit, or be replaced. The next terminal must recover from durable project artifacts and verified state rather than reconstructing the project from chat history.

## Self-reflective Core — ARCHITECTURAL DIRECTION

Gnozis is intended eventually to inspect its own execution history and identify possible deficiencies in its own rules. This is controlled reflection, not unrestricted self-modification.

### Layer model

```text
L0 Ψ-Core
    canonical State = Ψ=(X,R)
    transitions
    invariants

L1 Observation
    transition history
    audit events
    evidence
    provenance

L2 Reflection
    Rule Registry
    ReflectionObservation
    ReflectionPattern
    ReflectionFinding
    Counterexample
    RuleProposal

L3 Governance
    Shadow Rule evaluation
    independent verification
    acceptance
    activation
    rollback

L4 Endogenous Evolution
    future phase only
    autonomous generation remains disabled until L0-L3
    are independently implemented and independently verified.
```

### Core protection

- Reflection must not directly mutate canonical Core state.
- A `RuleProposal` is not a Core transition.
- A verified proposal is not automatically activated.
- Reflection may identify a possible deficiency; it must not treat its own hypothesis as truth merely because it generated it.
- No AI model belongs inside Ψ-Core.
- No second state model may be introduced for Reflection.

### Target self-reflection loop

```text
OBSERVE
   ↓
CLASSIFY
   ↓
HYPOTHESIZE
   ↓
CHALLENGE
   ↓
COLLECT EVIDENCE
   ↓
PROPOSE
   ↓
SHADOW TEST
   ↓
INDEPENDENT VERIFY
   ↓
GOVERN
   ↓
ADOPT
   ↓
OBSERVE AGAIN
```

Failure at a governance stage leads to rejection or quarantine, not forced activation.

### Rule lifecycle target

```text
PROPOSED
    ↓
ANALYZING
    ↓
SHADOW
    ↓
CHALLENGED
    ↓
VERIFICATION
    ↓
AUDITED
    ↓
ACCEPTED
    ↓
ACTIVE
```

Alternative outcomes include `REJECTED` and `QUARANTINED`. Acceptance and activation are separate states. Rule versions are retained for provenance and rollback.

### Planned reflection entities

`Rule`:

```text
rule_id
rule_version
rule_type
scope
implementation_ref
spec_ref
invariant_refs
provenance
status
```

`ReflectionObservation` records which rule/version was applied to which state/candidate/transition, the outcome, reason codes and evidence references.

`ReflectionFinding` groups reproducible observations into a candidate pattern and must identify falsification conditions. Frequency or confidence is not itself proof of correctness.

`CounterexampleCandidate` is an explicit attempt to refute a reflection hypothesis using historical, synthetic, boundary, mutation, cross-rule or external-evidence methods.

`RuleProposal` describes a proposed rule/version change, its evidence, expected effects, possible regressions and test plan. It cannot activate itself.

### Evidence chain target

```text
Observation
    ↓
Pattern
    ↓
Finding
    ↓
Hypothesis
    ↓
Counterexample challenge
    ↓
Rule Proposal
    ↓
Shadow evaluation
    ↓
Independent verification
    ↓
Governance
    ↓
Activation / rejection / quarantine
```

Every substantive reflection claim must be traceable to reproducible observations/evidence. `NO_COUNTEREXAMPLE_FOUND` does not mean `PROVEN_TRUE`.

## Current self-reflection status

The existing Core already provides the foundation: canonical Ψ-State, candidate/transition verification, explicit invariants, persistence and append-only audit history. Endogenous generation remains caller-supplied and is therefore not autonomous.

The following are architectural targets, not current implementation claims:

- Rule Registry: `MISSING`
- ReflectionObservation: `MISSING`
- ReflectionPattern/Finding: `MISSING`
- Counterexample engine: `MISSING`
- RuleProposal lifecycle: `MISSING`
- Shadow Core/rule evaluation: `MISSING`
- Rule governance/activation/rollback: `MISSING`
- Autonomous self-modification: `MISSING / FORBIDDEN FOR CURRENT PHASE`

## Reflection implementation roadmap

This roadmap is a sequence of bounded engineering phases. Do not collapse the phases into one uncontrolled self-modification implementation.

```text
R1 Core Reflection Foundation
    ↓
R2 Observation + Finding Engine
    ↓
R3 Counterexample Engine
    ↓
R4 Shadow Rule Evaluation
    ↓
R5 Governance / Activation / Rollback
    ↓
R6 Endogenous Rule Generation
    ↓
R7 Cooperative Self-Reflection Network (future multi-user strategy)
```

### R1 — Core Reflection Foundation

Create the read-only, provenance-preserving reflection data/contracts without changing existing Ψ-Core transition semantics.

Allowed:

1. Rule Registry and version metadata.
2. ReflectionObservation contract.
3. ReflectionFinding/Pattern contract.
4. Counterexample registration/challenge contracts.
5. RuleProposal contract and lifecycle metadata.
6. Provenance links to states, candidates, transitions and audit events.
7. Persistence for the new reflection artifacts.
8. Read-only reflection pipeline and tests.

Forbidden:

- autonomous Core modification;
- automatic rule activation;
- replacement or duplication of Ψ-State;
- second state model;
- autonomous endogenous generator;
- Shadow Core activation;
- changes to existing transition semantics unless separately authorized.

### R2 — Observation + Finding Engine

Connect real Core execution history to reflection observations. Detect repeated or unusual patterns without changing Core behavior.

Observation sources include transition records and audit events. Candidate patterns may include repeated rejection reasons, recurring state classes, conflicting outcomes, repeated failures or unusual transition patterns.

A pattern is not proof of a defect. Findings must state reproducibility and falsification conditions.

### R3 — Counterexample Engine

Actively try to refute Findings using reproducible historical replay, boundary cases, synthetic candidates, mutation, competing rules or other explicitly recorded challenge methods.

Possible results:

```text
REFUTED
SUPPORTED
INCONCLUSIVE
NOT_RUN
```

`NO_COUNTEREXAMPLE_FOUND` must never be treated as proof of truth.

### R4 — Shadow Rule Evaluation

Compare a proposed rule version with the active version over identical historical, boundary and adversarial inputs.

Shadow execution may observe and compare but cannot:

```text
commit canonical state
activate a rule
modify Rule Registry authority
bypass invariants
```

Compare outcomes, invariant deltas, behavioral deltas, resource deltas and evidence.

### R5 — Governance / Activation / Rollback

Introduce explicit governance decisions, atomic activation, monitoring and rollback. Rule versions remain available for provenance and restoration.

Acceptance and activation are distinct states. Rollback is a normal versioned operation, not an ad-hoc repair.

### R6 — Endogenous Rule Generation

Future phase only. Gnozis may eventually generate a candidate rule from accumulated evidence, but generation has no direct authority over canonical Core.

Required sequence:

```text
SELF-GENERATE
    ↓
Rule Candidate
    ↓
Counterexample
    ↓
Shadow
    ↓
Verification
    ↓
Governance
    ↓
Activation
```

R6 is prohibited until R1-R5 are implemented and independently verified.

### R7 — Cooperative Self-Reflection Network

Future strategy only. Multiple independent users/Gnozis instances/AI systems may eventually exchange evidence, hypotheses, counterexamples and proposals under explicit identity, capability and trust boundaries. This is not current implementation scope.

## Next bounded Core modernization phase

### CORE REFLECTION FOUNDATION — R1

Current intended phase:

```text
Primary implementer: Claude when available
Independent reviewer: Manus
Final gate: ChatGPT
External audit: as explicitly assigned
Scope: R1 only
```

Acceptance criteria:

```text
existing Core tests remain valid;
existing transition semantics remain unchanged;
Reflection cannot commit a transition;
all reflection claims have provenance;
new artifacts are persistable and auditable;
RuleProposal cannot activate itself;
current Ψ-Core invariants remain authoritative.
```

No phase may be assumed complete from documentation alone; source, tests, CI and independent verification remain authoritative.

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

### User architecture

`docs/USER_ARCHITECTURE.md` records the current architectural direction for user/task/context/capability continuity across connected terminals and products. It is **DOCUMENTED / NOT IMPLEMENTED**. No runtime User/Task/Context/Capability layer is claimed by this document alone.

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
4. `docs/USER_ARCHITECTURE.md`;
5. relevant specification/schema documents;
6. relevant source files;
7. relevant tests;
8. latest CI status.

Then report:

- current branch;
- current HEAD;
- latest CI-tested commit;
- implementation state using `IMPLEMENTED / PARTIAL / MISSING / THEORETICAL`;
- verification qualifiers separately;
- any mismatch between current HEAD and tested commit;
- current task and its durable context;
- capabilities available to the current terminal;
- allowed and forbidden scope.

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
