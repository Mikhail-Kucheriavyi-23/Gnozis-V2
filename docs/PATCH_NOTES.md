# PATCH NOTES — audit defect remediation

Scope: fixes ONLY the defects confirmed by `AUDIT.md`. No new phase
(Agent/Memory/Federation/Bridge) was started; the `Ψ=(X,R)` model and the
single `Engine`/`Instance` contracts are unchanged except where a defect
required a new invariant/method. See `logs/audit/PHASE_PATCH_AUDIT.md` for
the full test execution log and final verdict.

## Defect #1 — shallow frozen state (v33 recidive #8) → FIXED

**Before:** `frozen=True` blocked reassigning `State.elements`, but the
dict/list/set *contents* were fully mutable in place — `state.elements['x']
= 1` succeeded silently, nested dicts could be mutated through the
accessor, `with_elements`/`with_relations` shared live nested references
across "versions", and `Relation.value` held a live reference to whatever
mutable object the caller passed in.

**After:** `gnosis/core/types.py::deep_freeze()` recursively converts every
dict → `MappingProxyType` (over a freshly-built dict), every list/tuple →
tuple, every set → frozenset, applied in `State.__post_init__` and
`Relation.__post_init__`. All six adversarial scenarios from the audit
(A–F) now raise `TypeError` or otherwise leave the original object
untouched. See `tests/test_immutability_adversarial.py`.

## Defect #2 — identity/no-op transition accepted as evolution (v33 recidive #3) → FIXED

**Before:** `check_monotonic_version` only compared `version` (an int).
A candidate with byte-identical `elements`/`relations` but `version + 1`
passed every invariant and was committed as if real evolution occurred.

**After:** `State.content_id` (new property) hashes `elements` + a
*sorted* list of relation ids, deliberately excluding `version` and
independent of relation ordering. `invariants.py::check_meaningful_change`
rejects any candidate whose `content_id` matches the current state's
`content_id`, added to `DEFAULT_INVARIANTS`. See
`tests/test_meaningful_change.py`, including the canonical-ordering case
(dict key order / relation order differences do not create false
"evolution").

## Defect #3 — Test(candidate)→bool not enforced (v33 recidive #6/#7) → FIXED

**Before:** `TestResult.passed: bool` was a type hint only.
`TestResult(passed="yes")` constructed without error and was used truthily
downstream.

**After:** `TestResult.__post_init__` raises `TypeError` unless
`isinstance(passed, bool)` — specifically `isinstance`, not a value check,
so `1`/`0` (type `int`) are correctly rejected despite `bool` being an
`int` subclass. See `tests/test_test_result_contract.py`.

## Defect #5 — Select stage missing from runtime → FIXED (minimal)

**Before:** `Engine` had no method accepting more than one `Candidate`;
the documented "Generate → Test → Select → Evolve" cycle had no Select in
code, only in prose.

**After:** `gnosis/core/select.py::select()` runs Test on every candidate
in a list, discards failures, and deterministically chooses the passing
candidate with the lexicographically smallest `candidate_id` (documented
explicitly as a minimal, temporary, non-scoring rule — the master spec
does not define a real selection criterion yet). `Engine.step_select()`
wires this into the same verify()-gated commit path as `step()`. No
global state, no external model, no scoring heuristic. See
`tests/test_select.py`, including a full `Ψ0 → Generate → Test → Select →
Evolve → Ψ1` vertical-slice test.

## Defect #6 — "endogenous generator" documentation mismatch → FIXED (docs only)

**Before:** `evolution.py` called `GenerateFn` an "endogenous generator
hook" while `run(generate_fn)` actually receives the generator from the
caller on every invocation — exactly the "External Controller → tells Core
what to evolve" pattern spec section 3 prohibits.

**After:** Docstrings in `evolution.py` (module-level and on `GenerateFn`)
now state plainly that Generate is caller-supplied, not endogenous, in
this slice, and that building a real internal generator is Phase 9 scope.
No behavior changed — this was a documentation-only correction, per PATCH
section 6 ("не делать сейчас поспешную архитектурную переделку").

## Defect #7 — invariant-failure semantics left implicit → FIXED (docs only, Variant A confirmed)

**Decision recorded explicitly** in `invariants.py` module docstring:
candidate-local invariant failure is Variant A (reject this candidate,
Engine continues) — not a hard stop. Explicitly distinguished from three
things that remain unimplemented and must not be conflated with this: (a)
corruption of the current authoritative state, (b) a security/capability
failure, (c) an unrecoverable engine failure. No behavior changed.

## Defect #8 — StopReason enum overclaims coverage → FIXED (docs only)

**Before:** all 10 `StopReason` values sat in one flat enum with no
indication that 8 of them are never raised anywhere in the code.

**After:** the enum itself is now split into two commented groups —
`IMPLEMENTED NOW` (`BUDGET_EXHAUSTED`, `INVALID_STATE`) and `RESERVED /
FUTURE` (the other 8) — so the source of truth carries the honesty, not
just STATUS.md. No fake trigger paths were added to "cover" the enum
(explicitly prohibited by PATCH section 8).

## Defect #9 — `logs/` is a decorative placeholder → FIXED (docs only)

**Before:** three empty directories with no indication they were
non-functional.

**After:** `logs/README.md` states plainly that nothing writes to these
directories yet, that `Engine.history` is in-memory only, and that this is
not a persistent or audit-complete logging system. No logging
infrastructure was built (explicitly out of scope per PATCH section 9).

## Defect #10 — forward stubs overclaim ("fixed contract") → FIXED (docs only)

**Before:** `Agent = None` etc. were described as a "fixed contract to
implement against."

**After:** same `None` assignments, but the docstring now calls them
"reserved names, not type contracts" and explicitly notes this
overclaiming was the audit finding being corrected. No Agent/Capability
architecture was added (explicitly out of scope per PATCH sections 10/14).

## Explicitly NOT done in this PATCH (per PATCH section 14)

No OpenRouter, Bot, LLM dependency, Internet Bridge, User Bridge, Memory,
Database implementation, Federation, cryptographic subsystem, Agent
runtime, gas VM, or self-modification engine were added. The `Ψ=(X,R)`
model is unchanged. No second State model or alternate evolution engine
was created.
