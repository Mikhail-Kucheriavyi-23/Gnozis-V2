# GNOSIS 2.0 — Phase 0/1/3 + Audit Patch

New project, built from scratch per `docs/MASTER_SPEC.md`. This is **not**
a refactor of GNOSIS v1 (UROBOROS Ψ-Core v33) — that repository is treated
only as research material, not as code to reuse.

## What's actually in this slice

Per spec section 53: *"Не заявлять implemented, если функциональность
только описана."* See `STATUS.md` for the full implemented/partial/missing
breakdown against all 53 spec sections, and `docs/PATCH_NOTES.md` +
`logs/audit/PHASE_PATCH_AUDIT.md` for the independent audit that was run
against this archive and the defects it found and fixed.

Implemented now:

- `Ψ = (X, R)` as `State` + `Relation`, **deep-frozen** (not just
  `frozen=True` — nested dict/list/set content cannot be mutated through
  any accessor; see `gnosis/core/types.py::deep_freeze`)
- `Candidate → Test → Select → Evolve` / `Commit` pipeline — both a
  single-candidate path (`Engine.step`) and a multi-candidate path with a
  real, deterministic Select stage (`Engine.step_select`,
  `gnosis/core/select.py`) — with **no** direct Candidate → Core mutation
  path
- Protected invariants: state integrity, transition validity, monotonic
  versioning, and **meaningful-change** (rejects identity/no-op
  transitions that only bump `version` without changing content) —
  `gnosis/core/invariants.py`
- `TestResult.passed` is a runtime-enforced `bool` (not just a type hint)
- Hard resource budget (default 20 atomic ops) with no negative overflow
- Hard stop conditions as a typed enum, explicitly split into
  IMPLEMENTED-NOW vs RESERVED (`StopReason` in `gnosis/core/types.py`)
- `Instance` / `clone_state` / `fork_instance` / lineage
  (`gnosis/instances/`), with isolation between forked instances tested
- 61 tests total, including adversarial regression tests for every defect
  the audit found (deep-mutation attempts, no-op transitions, non-bool
  Test results, Select determinism)
- GitHub Actions CI config (`.github/workflows/ci.yml`) — **note:** this
  has not actually been executed against this codebase in the sandbox
  these patches were built in (no network access to install real
  `pytest`); see `logs/audit/PHASE_PATCH_AUDIT.md` section B for exactly
  what was and wasn't run, and run it for real before trusting a CI badge.

Not implemented yet (see `STATUS.md`): Agents, Memory, Identity/crypto,
Capabilities, Federation, Bridge, persistence/database, real endogenous
generation, theorem-prover integration.

## Running the tests

```bash
pip install -e ".[dev]"
pytest -v
```

If you don't have network access to install `pytest`, note that the
authoring sandbox didn't either — see `logs/audit/PHASE_PATCH_AUDIT.md`
for how verification was done without it (an offline runner is not part
of this deliverable; it's not a substitute for running real pytest).

## Design principle

> "Сначала доказуемый фундамент, затем автономия."

This archive went through one full audit + patch cycle already (see
`AUDIT.md` at the repo root for the original findings, `docs/PATCH_NOTES.md`
for what was fixed, and `logs/audit/PHASE_PATCH_AUDIT.md` for the
re-verification). Per that audit's final answer, this slice is
**READY FOR PHASE 4** (Memory) — but should not skip ahead to
Agent/Federation/Bridge without similarly grounding those phases first.
