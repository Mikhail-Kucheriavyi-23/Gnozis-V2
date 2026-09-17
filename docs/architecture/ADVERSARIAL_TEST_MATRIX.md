# Persistence Adversarial Test Matrix

**Status:** proposed acceptance suite

**Required test record:** each test should capture precondition, operation, expected DB state, expected domain state, expected audit chain, and expected recovery result.

## Test result vocabulary

- `PASS`: operation obeys the contract.
- `REJECT`: invalid input is refused without an unsafe partial commit.
- `FAIL_CLOSED`: corruption or ambiguity prevents evolution/recovery.
- `IDEMPOTENT`: exact replay produces the same durable result without a second semantic event.

## Matrix

| ID | Class | Precondition | Operation | Expected DB state | Domain/audit/recovery expectation |
|---|---|---|---|---|---|
| A-01 | Fresh | Empty DB | Initialize schema | One valid schema version | `EMPTY_INITIALIZED` |
| A-02 | Constraints | Schema ready | Insert orphan relation | No row committed | `REJECT`; no domain change |
| A-03 | Constraints | Schema ready | Insert orphan candidate | No row committed | `REJECT` |
| A-04 | State | Valid nested State | Save/load round-trip | Canonical rows retained | Same IDs and deep-frozen object |
| A-05 | State tamper | Saved state | Change payload directly | DB physically altered only by adversary | Load `FAIL_CLOSED` on hash mismatch |
| A-06 | Relation tamper | Saved relation | Change endpoint/value | Hash or endpoint check fails | No State reconstruction |
| A-07 | Candidate accepted | Root exists | Persist accepted candidate | State, candidate, transition, audit, head all present | New head after restart |
| A-08 | Candidate rejected | Root exists | Persist rejected candidate | Candidate, rejected transition, audit present; head unchanged | Recovery returns old head |
| A-09 | Root atomicity | Empty DB | Fail after state insert | No visible root or orphan state | Prior empty state recovered |
| A-10 | Accepted atomicity | Root exists | Fail after candidate insert | No partial accepted operation | Old head recovered |
| A-11 | Accepted atomicity | Root exists | Fail after transition insert | No transition/head mismatch | `RECOVERED` old state or `FAIL_CLOSED`, never guessed |
| A-12 | Accepted atomicity | Root exists | Fail after audit insert before commit | No visible event/head advance | Old head and chain recovered |
| A-13 | Commit crash | Root exists | Kill process around commit | SQLite all-or-nothing result | Reopen verifies one valid outcome |
| A-14 | Restart | Committed transition | Close/reopen | All rows durable | Exact current state and valid chain |
| A-15 | Final corruption | Valid chain | Alter final payload/hash | Corrupt row detectable | `CORRUPT_FAIL_CLOSED` |
| A-16 | Middle corruption | 3+ events | Alter middle event | Later rows remain physically present | Full-chain verification fails; no skip |
| A-17 | Previous-link tamper | 2+ events | Alter `prev_hash` | Row may be physically altered | Chain fails |
| A-18 | Sequence tamper | 2+ events | Swap/change sequence | Unique/order/hash checks fail | Chain fails |
| A-19 | Delete final | 2+ events and current head depends on final | Delete final event | Direct deletion rejected or inconsistency visible | Fail closed; no silent rollback |
| A-20 | Insert middle | 2+ events | Insert event with intermediate sequence | Unique/FK/chain policy rejects or verification fails | No accepted recovery |
| A-21 | Update audit | Existing event | `UPDATE audit_events` | Trigger/API rejects | Original chain remains valid |
| A-22 | Delete audit | Existing event | `DELETE audit_events` | Trigger/API rejects | Original chain remains valid |
| A-23 | Duplicate event | Existing event | Reinsert exact event | No second semantic event | `IDEMPOTENT` or explicit `REJECT` |
| A-24 | Payload substitution | Existing event | Replace actor/result/resource | Hash mismatch | `FAIL_CLOSED` |
| A-25 | Duplicate state | Existing state ID | Insert same ID with different payload | PK/identity check rejects | Original state unchanged |
| A-26 | Duplicate candidate | Existing candidate ID | Replay exact candidate | No duplicate semantic transition | Idempotent or reject |
| A-27 | Stale head | Root advanced | Commit candidate with old parent | No new head | `REJECT`; audit policy documented |
| A-28 | No-op transition | Root exists | Persist version-only/no-content change | Transition rejected before accepted persistence | Core meaningful-change invariant preserved |
| A-29 | Rejected-to-head | Rejected candidate | Restart | Head points to prior state | Proposed state never becomes current |
| A-30 | Fork | Parent exists | Create child | Parent and child rows/head atomic | Parent unchanged; child generation valid |
| A-31 | Fork crash | Parent exists | Fail during child creation | No incomplete child | Parent recovery unchanged |
| A-32 | Fork isolation | Parent and child | Advance child | Only child head changes | State/budget isolation preserved |
| A-33 | Lineage cycle | Existing instances | Attempt self/ancestor parent | Constraint/repository rejects | Recovery remains valid |
| A-34 | Generation mismatch | Parent exists | Insert wrong child generation | Constraint/recovery check rejects | No valid child returned |
| A-35 | Multiple instances | Two roots | Interleave commits | Global audit sequence remains strict | Both heads recover independently |
| A-36 | Concurrent same head | One root, two writers | Commit both candidates | One wins; one stale/rejected | No lost update; chain valid |
| A-37 | Concurrent different heads | Two roots | Commit concurrently | Serialized safe result initially acceptable | No cross-instance contamination |
| A-38 | Foreign keys off | Connection created | Attempt orphan insert | Test must detect pragma failure | Implementation must refuse unsafe connection |
| A-39 | Unsupported status | Valid DB | Inject unknown status | Load rejects | No silent coercion |
| A-40 | Malformed JSON | Valid DB | Corrupt serialized payload | Load fails | `CORRUPT_FAIL_CLOSED` |
| A-41 | Missing current head | Instance exists | Remove/head-break state reference | FK or recovery detects | No timestamp-based fallback |
| A-42 | Missing audit event | Head/transition exists | Delete referenced event | Continuity fails | Fail closed unless transaction proof establishes never-committed operation |
| A-43 | Secret input | Sentinel secret supplied | Persist candidate/provenance | Secret rejected/redacted | Secret absent from every table and log |
| A-44 | Core isolation | Existing Core suite | Install/use storage adapter | Core behavior unchanged | Existing suite passes; no Core SQL dependency |
| A-45 | Serialization determinism | Equivalent mapping order | Save equivalent states | Same canonical payload/hash | IDs equal where logical content equal |
| A-46 | Relation duplicate | Same relation twice | Save state | Policy rejects or deterministic duplicate semantics | No accidental graph mutation |
| A-47 | Read snapshot | Active writer | Read multi-table head | One committed snapshot | No mixed-version domain object |
| A-48 | Rollback recovery | Forced exception | Reopen DB | No partial operation | Prior chain/head valid |
| A-49 | Schema mismatch | Older/newer DB | Open with incompatible code | Startup refuses | `SCHEMA_INCOMPATIBLE` |
| A-50 | Audit resource mismatch | Event points to wrong resource | Verify chain/domain links | Hash may be valid but semantic validation fails | `FAIL_CLOSED` |

## Required per-test evidence

Every failure-injection or tamper test must record:

1. database rows before the operation;
2. exact operation and failure injection point;
3. database rows after the operation;
4. current instance head;
5. transition and candidate counts;
6. last verified audit sequence/hash;
7. reconstructed domain result;
8. recovery status and error category.

A test that only asserts an exception is insufficient. The test must prove that no unsafe partial state became authoritative.

## Minimum implementation gate

The Persistence phase is not ready for Final Gate if any of these remain untested:

- accepted commit atomicity;
- rejected candidate atomicity;
- restart recovery;
- final and middle audit corruption;
- append-only bypass attempts;
- duplicate/idempotency behavior;
- fork and multiple-instance isolation;
- current-head consistency;
- secret exclusion;
- unchanged Core test suite.
