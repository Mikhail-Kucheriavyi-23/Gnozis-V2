# Gnozis-V2 — AI Context

## CONTEXT-SYNC ADDENDUM — AI TASK-BLOCK OPERATING PROTOCOL

This addendum formalizes how AI agents must operate on the existing roadmap and task queue. It does not authorize removal of the final self-evolution gate.

### Operating contour

```text
Audit
  ↓
Task Registry
  ↓
Dependency Graph
  ↓
Priority Selection
  ↓
Implementation
  ↓
Test
  ↓
Adversarial Check
  ↓
Correction
  ↓
Re-test
  ↓
Gate
  ↓
Evidence Record
  ↓
Next Task
```

### Task Block contract

Every executable task must be representable as a self-contained contract containing:

- `TASK-ID`
- `BLOCK`
- `STATUS`
- `PRIORITY`
- `DEPENDS_ON`
- `OBJECTIVE`
- `SCOPE`
- `DO_NOT_CHANGE`
- `REQUIRED_TESTS`
- `ACCEPTANCE`
- `AUDIT`
- `NEXT`

An agent must select one primary task at a time. Dependencies are mandatory; priority never bypasses them. Directly necessary corrective work is allowed only when required to complete the selected task.

### Agent selection rule

On every new work session an agent must:

1. Read the complete `AI_CONTEXT.md`.
2. Reconcile the current `main` HEAD.
3. Inspect the implementation and relevant tests.
4. Build the currently applicable dependency view.
5. Select exactly one highest-priority `READY` task whose dependencies are satisfied.
6. Implement only that task plus directly necessary corrections.
7. Execute relevant tests/runtime verification.
8. Record actual evidence.
9. Mark `DONE` only when evidence exists; otherwise use `IN_PROGRESS` or `BLOCKED`.
10. Stop and hand off rather than autonomously selecting an unrelated later capability.

### Self-evolution preparation rule

The final self-evolution gate remains closed until the required evidence chain is operational. Preparation must proceed first through Core invariants, persistence/recovery, append-only audit evidence, candidate generation and testing, sandbox execution, shadow evaluation, invariant delta, governance/evidence thresholds, security, quarantine and recovery.

The intended chain is:

```text
Candidate
  ↓
Generate
  ↓
Test
  ↓
Sandbox execution
  ↓
Observed evidence
  ↓
Shadow evaluation
  ↓
Invariant delta
  ↓
Governance / evidence gate
  ↓
Promotion candidate
  ↓
ONLY THEN canonical mutation
```

No task may bypass this gate merely because a later capability is technically possible.

### Evidence rule

A written test is not a PASS until it has actually executed in a real runtime or CI environment. A claimed audit, artifact, GitHub Actions run, or self-evolution result is not evidence unless the corresponding execution/result is inspected.

### Immediate planning objective

The next planning-level objective is to maintain a single authoritative Task Registry plus its dependency graph and deterministic selection rules. Existing task IDs and statuses remain authoritative unless explicitly changed with implementation evidence.

This addendum supplements the existing repository context; it does not replace the repository's existing architectural history, task queue, invariants, or safety rules.