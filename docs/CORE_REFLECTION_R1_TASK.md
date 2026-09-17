# R1 — Core Reflection Foundation

## Purpose

Implement the first runtime layer for controlled self-reflection while preserving the existing Ψ-Core semantics exactly.

Current operating mode: **single owner / single account / single canonical project**.

## Role assignment

```text
Primary implementer: Claude when explicitly assigned
Independent reviewer: Manus when available
Final integration gate: ChatGPT
```

The implementer must not treat this document as evidence that the feature already exists.

## Mandatory pre-flight

Before editing:

1. inspect current `main` HEAD;
2. inspect `gnosis/core/*` and existing contracts;
3. inspect `gnosis/storage/*` and existing persistence schema;
4. inspect current tests;
5. inspect CI configuration and latest tested commit;
6. reconcile any difference between this document and actual source.

Source and reproducible evidence outrank this document.

## Allowed implementation scope

Implement only the minimum durable foundation for:

### Rule Registry

Versioned metadata for rules currently recognized by the reflection layer.

Minimum conceptual fields:

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

### ReflectionObservation

A provenance-linked record describing an observation of a rule applied to a state, candidate or transition.

Minimum conceptual information:

```text
observation_id
rule_id
rule_version
state_ref / candidate_ref / transition_ref
outcome
reason_codes
evidence_refs
provenance
created_at
```

### ReflectionFinding

A reproducible candidate pattern derived from observations.

Must include:

```text
finding_id
claim
observation_refs
affected_rule_refs
reproducibility
falsification_condition
status
provenance
```

A Finding is not proof of a defect.

### CounterexampleCandidate

A durable challenge record for attempting to falsify a Finding.

Minimum information:

```text
counterexample_id
finding_id
challenge_type
input/evidence references
result
provenance
```

Allowed results should distinguish at least:

```text
REFUTED
SUPPORTED
INCONCLUSIVE
NOT_RUN
```

### RuleProposal

A proposal for a future rule/version change.

Minimum information:

```text
proposal_id
rule_id
current_version
proposed_version
finding_refs
counterexample_refs
expected_effects
possible_regressions
test_plan
status
provenance
```

A RuleProposal has **no activation authority**.

## Persistence requirements

Use the existing storage architecture rather than creating a second database abstraction.

New reflection records must:

- be transactionally persisted;
- maintain foreign-key/provenance relationships where applicable;
- be auditable;
- not make historical records mutable merely for convenience;
- avoid unrelated schema changes.

If a schema migration is genuinely required, stop and surface it as an explicit scope decision rather than silently expanding R1.

## Core boundary

The implementation MUST NOT:

```text
change Ψ=(X,R) semantics
change Engine transition semantics
introduce a second State model
allow reflection to commit transitions
allow RuleProposal to activate itself
activate shadow rules
implement endogenous generation
modify Memory
implement Identity/authentication
implement encryption
implement Internet Bridge
implement multi-user/federation runtime
embed an AI model inside Core
```

## Read-only reflection interface

The first runtime interface should permit:

```text
observe
list observations
inspect finding
register challenge
create proposal
inspect provenance
```

It should not expose a direct mutation path into canonical Core state.

## Tests required

At minimum test:

1. rule registration/version uniqueness;
2. observation provenance;
3. finding references valid observations;
4. counterexample references valid findings;
5. proposal references valid evidence;
6. proposal cannot activate a rule;
7. reflection operations cannot mutate canonical Ψ-State;
8. append-only/audit guarantees for reflection records;
9. persistence survives reload;
10. existing Core test suite remains unchanged and passes.

Where an assertion cannot be demonstrated from actual runtime behavior, report it as unverified rather than inferring success.

## Acceptance gate

R1 is accepted only when all of the following are true:

```text
existing Core behavior unchanged
existing Core tests pass
new R1 tests pass
reflection records persist
provenance is traceable
reflection cannot commit Core transitions
RuleProposal cannot activate itself
no forbidden scope entered
independent review completed
ChatGPT final integration gate completed
```

## Handoff after implementation

The implementer must provide:

```text
HEAD commit SHA
files changed
schema changes (if any)
tests executed
CI-tested commit SHA
test results
known limitations
forbidden-scope confirmation
open findings
recommended next phase
```

Do not mark R1 `ACCEPTED` from a textual completion report alone.
