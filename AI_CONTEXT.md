# Gnozis-V2 — AI Context

## CANONICAL BASELINE — HEAD PIN

- Canonical repository: `Mikhail-Kucheriavyi-23/Gnozis-V2`
- Canonical branch: `main`
- Verified baseline commit at checkpoint: `a990a11e81c5a693ed3b2ac45f115954cad5ad5f`
- All architectural statements in this document refer to this baseline or later commits unless explicitly marked historical.
- If another agent reports an older commit (for example `47a7e548...`), treat it as historical until reconciled against current `main`.
- Before architectural changes, reconcile the current `main` HEAD if the working context may be stale.

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
