# Gnozis-V2 — AI Context

## CANONICAL BASELINE — HEAD PIN

- Canonical repository: `Mikhail-Kucheriavyi-23/Gnozis-V2`
- Canonical branch: `main`
- Verified current main HEAD at this checkpoint: `950915871c1ccdd3512dc816b8814912a60faf22`.
- Previous pinned baseline `a990a11e81c5a693ed3b2ac45f115954cad5ad5f` is historical.
- All architectural statements in this document refer to current `main` or explicitly marked historical commits/branches.
- If another agent reports an older commit (for example `47a7e548...`), treat it as historical until reconciled against current `main`.
- Before architectural changes, reconcile the current `main` HEAD if the working context may be stale.

## Canonical repository and scope

- Canonical development repository: `Mikhail-Kucheriavyi-23/Gnozis-V2`
- `AI_CONTEXT.md` is the operational handoff document and must remain synchronized with verified source/runtime state.
- Current scope: SINGLE OWNER / SINGLE ACCOUNT / SINGLE PROJECT.
- Multi-user, federation, tenant and public-network runtime are future strategy only.
- Current work is repository modification, testing, persistence, reflection, autonomous evolution architecture and architecture validation. Do not design the public/federated product yet.

## Why the architecture is being built this way

The original Gnozis direction is not merely an application that executes fixed rules. The long-term objective is a system that can observe its own operation, accumulate evidence, detect limitations in its own rules, formulate falsifiable proposals for rule changes, build and test alternative architectural models in an internal sandbox, and autonomously promote a sufficiently justified evolution into its next Core version.

Autonomous self-modification is intentional. The safety property is not "a human must press the button"; it is that canonical mutation is downstream of a reproducible recursive evidence loop. A model must be hypothesized, bounded, executed in isolation, evaluated against evidence and Core invariants, compared with alternatives, and only then become eligible for promotion.

The intended recursive contour is:

```text
Core_n
  ↓
observable evidence
  ↓
persistence / recovery
  ↓
self-diagnostic reflection
  ↓
versioned RuleProposal
  ↓
EvolutionHypothesis
  ↓
bounded EvolutionSandbox
  ↓
ModelGenerator
  ↓
Sandbox execution
  ↓
Shadow Evaluation
  ↓
Invariant Delta
  ↓
Governance / evidence threshold
  ↓
PromotionCandidate
  ↓
Core_(n+1)
  ↓
Reflection again
```

No single stage is allowed to substitute for the complete evidence chain.

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
11. **Shadow Adapter** — a proposal can be translated into an explicit shadow assessment contract without activating or mutating Core.
12. **Invariant Delta** — shadow and active evidence can be compared against the existing Core invariant surface; missing evidence is represented as `unknown` rather than fabricated failure.
13. **Persistent Invariant Delta** — invariant-delta evidence is persisted through the existing reflection SQLite persistence rather than creating a second storage system.
14. **Governance Decision** — a read-only decision layer classifies evidence as `BLOCK`, `HOLD`, `REVIEW` or `NO_CHANGE`.
15. **Authority Boundary** — the previous AuthorityRequest is provenance/approval metadata, not the definition of the autonomous evolution mechanism. It must not be interpreted as a mandatory human-operated activation gate.
16. **Authority provenance persistence** — AuthorityRequest lineage can be persisted and recovered.
17. **Autonomous Evolution Sandbox — current branch work** — the `evolution-sandbox` branch introduced bounded `EvolutionHypothesis`, `SandboxModel`, `SandboxExperiment`, `ModelEvidence`, `SandboxEvaluation`, and deterministic bounded `ModelGenerator` contracts. This branch is experimental until explicitly promoted into `main` after runtime verification.

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
- Shadow evaluation, invariant delta, governance classification and persistence layers exist in the current development line.
- **R1 RuleRegistry/analyzer tests have been added but are NOT considered verified until a real runtime/CI execution is inspected.**
- **A real GitHub Actions Self-Diagnostic run has NOT been verified.** Never claim `SELF-DIAGNOSTIC-0001` exists or CI passed without inspecting an actual run and artifact.
- **Evolution sandbox contracts currently exist on the `evolution-sandbox` branch, not as verified canonical `main` behavior.** The branch contains bounded hypothesis/model generation and evaluator contracts. Runtime execution has not yet been verified.
- Autonomous promotion into canonical Core is intentionally NOT yet implemented. The intended target is evidence-threshold-based promotion, not mandatory manual approval.

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

L3  Validation / Governance
    Shadow Adapter
    Shadow Evaluation
    Invariant Delta
    GovernanceDecision
    persistent provenance

L4  Autonomous Evolution — experimental
    EvolutionHypothesis
      ↓
    EvolutionSandbox
      ↓
    ModelGenerator
      ↓
    Sandbox Execution
      ↓
    ModelEvidence
      ↓
    SandboxEvaluation
      ↓
    PromotionCandidate

L5  Recursive promotion — NOT YET IMPLEMENTED
    evidence threshold
      ↓
    canonical Core_(n+1)
      ↓
    Reflection(Core_(n+1))
```

## Current next engineering gate

Do NOT jump directly to canonical self-modification.

The next concrete gate is:

```text
Evolution Model
    ↓
real sandbox execution
    ↓
real observations/evidence
    ↓
existing ShadowEvaluation
    ↓
existing InvariantDelta
    ↓
existing Governance
    ↓
PromotionCandidate
```

The sandbox must produce evidence from actual execution rather than accepting a caller-supplied score as proof. Only after that contract is runtime-verified should a promotion mechanism be designed.

## Context integrity rule

If the chat history and repository disagree, the repository HEAD and verified runtime evidence take precedence. Never reconstruct current architecture from memory alone. Update this file whenever a major architectural gate is completed or a canonical HEAD changes materially.
