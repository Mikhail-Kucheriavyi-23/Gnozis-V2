# Gnozis-V2 — AI Context

## Canonical repository and scope

- Canonical development repository: `Mikhail-Kucheriavyi-23/Gnozis-V2`
- `AI_CONTEXT.md` is the operational handoff document and must remain synchronized with verified source/runtime state.
- Current scope: SINGLE OWNER / SINGLE ACCOUNT / SINGLE PROJECT.
- Multi-user, federation, tenant and public-network runtime are future strategy only.
- Current work is repository modification, testing, persistence, reflection and architecture validation. Do not design the public/federated product yet.

## Why the architecture is being built this way

The original Gnozis direction is not merely an application that executes fixed rules. The long-term objective is a system that can observe its own operation, accumulate evidence, detect limitations in its own rules, formulate falsifiable proposals for rule changes, test those proposals independently, and only much later permit governed evolution.

The project therefore deliberately separates:

```text
Ψ-Core execution
    ↓
observable evidence
    ↓
persistence / recovery
    ↓
self-diagnostic reflection
    ↓
versioned rule-change hypothesis
    ↓
shadow evaluation / invariant comparison
    ↓
governed evolution
```

The current implementation must NOT skip directly from diagnosis to self-editing.

## Historical architectural chain — DO NOT LOSE THIS

The work progressed through these gates. A later agent must not collapse them into one generic "reflection" feature:

1. **Ψ-Core authority** — Core remains the source of truth for state/evolution semantics. No second state model and no AI model inside Core.
2. **Persistence first** — durable SQLite storage and append-only audit evidence were introduced so runtime history survives process boundaries.
3. **Provenance** — `TransitionRecord.test_rule_id` was added so evidence can identify the exact rule that produced a transition. Missing provenance remains `test-rule:unspecified`; causality must never be guessed.
4. **Recovery** — diagnostic evidence must come from persisted/recovered transition history, not a fresh/empty Engine and not fabricated records.
5. **Self-Diagnostic** — Reflection was built as a read-only layer outside Core: evidence → observations → findings → causal candidates → counterexamples → RuleProposal.
6. **Reproducible diagnostic corpus** — `diagnostic_corpus/` was introduced to distinguish controlled executable experiments from production history. The corpus must be generated from actual Core execution and persistence, never hand-authored as findings.
7. **Executable diagnostic path** — `diagnostic_corpus/generate.py` was developed around the required SQLite round-trip: execution → `persist_transition()` → recovery/`load_transition_records()` → `diagnose(recovered_history)` → artifact.
8. **Diagnostic contract tests** — tests were added to verify the persistence path and the controlled scenario. These tests must be treated as unverified until actually executed by a real runtime/CI.
9. **Rule Registry R1** — a versioned, read-only `RuleRegistry`/`RuleMetadata` foundation was added so a proposal can refer to a concrete `rule_id + rule_version` instead of an unversioned abstract rule.
10. **Versioned RuleProposal** — proposals now represent a hypothesis such as `rule:v1 → proposed:v2`, with evidence references, counterexamples, expected effects, regression risks and validation requirements.
11. **Current gate** — R1 must be independently executed and verified before moving to Shadow Evaluation or any endogenous evolution mechanism.

## Current verified engineering state

- Ψ-Core remains authoritative for state/evolution semantics.
- Persistence and append-only audit storage exist in `main`.
- `TransitionRecord` carries `test_rule_id` provenance.
- Persistence preserves `test_rule_id` through SQLite round-trip.
- Backward-compatible persistence migration preserves older data with `test-rule:unspecified` when provenance did not exist.
- Reflection is a read-only layer outside Ψ-Core.
- Proposal lineage and diagnostic artifact serialization exist.
- Reproducible Self-Diagnostic workflow/corpus infrastructure exists.
- Versioned read-only `RuleRegistry`/`RuleMetadata` exists in `gnosis/reflection/rules.py`.
- Reflection observations carry `rule_id` + `rule_version`.
- Findings carry affected versioned rule references.
- RuleProposals carry `rule_id`, `current_version`, `proposed_version`, finding/counterexample references, expected effects, regression risks and test plan.
- **R1 RuleRegistry/analyzer tests have been added but are NOT yet considered verified until a real runtime/CI execution is inspected.**
- **A real GitHub Actions Self-Diagnostic run has NOT been verified.** Never claim `SELF-DIAGNOSTIC-0001` exists or CI passed without inspecting an actual run and artifact.

## Current architectural layers

```text
L0  Ψ-Core
    State / Engine / transition semantics

L1  Evidence
    TransitionRecord / provenance / persistence / recovery

L2  Reflection
    Observation
      ↓
    Finding
      ↓
    CausalCandidate
      ↓
    CounterexampleCandidate
      ↓
    versioned RuleProposal

L3  Governance / validation
    Shadow Evaluation
    invariant delta
    regression analysis
    acceptance/rejection of proposal hypothesis

L4  Endogenous evolution
    future only; forbidden until lower layers are independently verified
```

## Critical distinction: proposal is NOT modification

The intended architecture is:

```text
Rule v1
  ↓
evidence
  ↓
Finding
  ↓
Counterexample
  ↓
RuleProposal: v1 → v2
  ↓
independent validation
  ↓
ACCEPT / REJECT / INSUFFICIENT_EVIDENCE
```

`RuleProposal` is a hypothesis. It must not activate itself, edit Python source, mutate canonical Core, or silently replace a rule.

`RuleRegistry` is descriptive/version metadata only. It must not become a hidden activation mechanism.

## Self-Diagnostic controlled experiment

The controlled scenario intentionally uses repeated `policy:bad-element` rejections associated with:

```text
 test-rule:diagnostic-policy
```

followed by an accepted transition.

Expected experiment properties are:

```text
4 TransitionRecord total
3 rejected
1 accepted
SQLite round-trip
exact test_rule_id provenance
```

These are **experiment invariants**, not findings that the diagnostic policy is defective.

The intended chain is:

```text
real Core execution
  ↓
TransitionRecord
  ↓
persist_transition()
  ↓
SQLite
  ↓
load/recovery
  ↓
recovered TransitionRecord history
  ↓
diagnose(history)
  ↓
SELF-DIAGNOSTIC-0001
```

A fresh/empty Engine or fabricated transition list is not acceptable evidence.

## CI / execution status

The repository contains `.github/workflows/self-diagnostic.yml` with the intended diagnostic workflow and `workflow_dispatch`/push triggers.

However, previous connector checks returned zero workflow runs for relevant commits. This means CI execution has not been established as evidence. Do not infer failure of Gnozis architecture from absence of a run, and do not infer success from workflow source alone.

If CI remains unavailable, the next valid route is an independently executed runtime/pytest verification of the same executable diagnostic path. Do not bypass the diagnostic contract or fabricate a PASS.

## R1 Rule Registry contract

`RuleMetadata` should identify a concrete rule version and remain descriptive. The registry must support deterministic lookup of:

```text
(rule_id, rule_version)
```

and latest-version lookup without exposing an activation API.

The Reflection chain must preserve:

```text
TransitionRecord.test_rule_id
    ↓
RuleRegistry(rule_id, version)
    ↓
Finding
    ↓
Counterexample
    ↓
RuleProposal(current_version → proposed_version)
```

Do not weaken provenance by guessing a rule from surrounding context.

## Required R1 verification before Shadow Evaluation

Before implementing Shadow Evaluation, verify all of the following in real execution:

1. RuleRegistry can register/resolve a versioned rule metadata record.
2. Reflection can resolve `TransitionRecord.test_rule_id` to the correct rule/version.
3. Observation and Finding preserve that versioned reference.
4. RuleProposal contains current and proposed versions and evidence references.
5. Proposal creation does not mutate canonical Core.
6. Existing reflection tests remain valid.
7. Persistence/recovery does not lose provenance.
8. Diagnostic artifact serialization preserves the versioned proposal lineage.
9. No test is merely checking source text instead of executing the contract.

Only after these are verified should the project move to:

```text
Shadow Evaluation(v1, v2, same evidence)
        ↓
Invariant delta
        ↓
Regression analysis
        ↓
ShadowAssessment
```

## Protection rules

- Reflection cannot mutate canonical Core.
- RuleProposal cannot activate itself.
- RuleRegistry has no activation semantics.
- `NO_COUNTEREXAMPLE_FOUND` is not proof of correctness.
- No AI model belongs inside Ψ-Core.
- No second state model may be introduced.
- No global clock/selector/operator may be smuggled into Core.
- Autonomous self-modification remains forbidden until R1-R5 are independently verified.
- A diagnostic finding is not automatically a Core bug.

## Diagnostic review classification

When `SELF-DIAGNOSTIC-0001.json` becomes available, inspect:

- findings;
- evidence references;
- exact `test_rule_id` attribution;
- versioned rule metadata;
- causal candidates;
- counterexample results;
- RuleProposals;
- proposal lineage;
- limitations / `UNSPECIFIED` cases;
- possible diagnostic false positives.

Classify each finding as exactly one of:

```text
CORE BUG
ARCHITECTURAL GAP
MISSING INVARIANT
MISSING TEST
FALSE POSITIVE
INSUFFICIENT EVIDENCE
FUTURE FEATURE
```

Never implement a Core change merely because a diagnostic proposes it.

## Current immediate task

**Do NOT jump directly to Shadow Evaluation.** First restore and verify the complete R1 chain in runtime.

Recommended order:

```text
1. Read AI_CONTEXT.md
2. Read STATUS.md
3. Inspect current source, not old reports
4. Run R1 RuleRegistry/analyzer tests
5. Run diagnostic corpus integration test
6. Verify persistence/recovery
7. Verify actual diagnostic artifact if generated
8. Update AI_CONTEXT.md + STATUS.md with factual results
9. Only then design the smallest Shadow Evaluation step
```

If another AI agent reports that the project is "not yet ready" or proposes restarting architecture, compare its statement against this chain first. The current task is verification of the already-built chain, not restarting Gnozis from scratch.

## Scope and authority

Current scope remains one owner/account and one canonical repository. Claude/Manus may implement or audit bounded tasks. ChatGPT/project owner remains the architectural gate.

Evidence hierarchy:

1. current source;
2. reproducible runtime behavior and real tests/CI;
3. accepted invariants/contracts;
4. independent audit evidence;
5. AI reports/proposals.

Never claim PASS/implemented/complete from documentation alone.
