# Gnozis-V2 — AI Agent Roles and Authority

## Operating principle

Gnozis is built and tested through multiple AI systems working against the same canonical project artifacts. Access to project data is broader than authority to modify the canonical architecture.

**Repository/Drive access does not by itself grant write authority.**

The human project owner authorizes substantive changes. AI agents implement, test, audit, challenge, and report within explicitly assigned scope.

## Roles

### ChatGPT — Architecture / Integration / Final Gate

- maintains Ψ-Core invariants and architectural direction;
- defines bounded tasks and acceptance criteria;
- reconciles independent findings;
- decides whether a phase is accepted, rejected, or returned for correction;
- synchronizes project context and status.

### Claude — Primary Implementer

- implements explicitly assigned engineering phases;
- writes and runs tests available in its environment;
- documents implementation and limitations;
- performs corrective passes after independent findings;
- does not self-certify final acceptance.

### Manus — Independent Reviewer / Adversarial Engineer

- reads the actual source or artifact;
- reproduces tests where possible;
- searches for hidden coupling, missing invariants, security defects, and unsupported claims;
- may perform an explicitly assigned corrective pass;
- does not grant final project acceptance.

### Gemini / Other Connected AI Systems

Depending on explicit assignment, a connected AI may act as:

- implementation contributor;
- independent auditor;
- adversarial tester;
- research/comparison source;
- runtime observer.

Its output is evidence or a proposal, not automatic architectural authority.

## Phase authority

Before each major phase, record:

```text
Primary implementer:
Independent reviewer:
ChatGPT final gate:
External audit required: yes/no
Allowed files/scope:
Forbidden changes:
```

The same AI should not both implement and independently certify a phase unless explicitly accepted as an exception by the project owner and documented as such.

## Access model

```text
GitHub / Google Drive access
          ↓
     observation
          ↓
 explicit task scope
          ↓
 implementation
          ↓
 independent verification
          ↓
 ChatGPT final gate
```

An agent with read access can inspect the whole relevant project without receiving permission to modify it.

An agent with write capability may modify only the files and architectural scope authorized by its current task.

## Evidence hierarchy

When reports conflict:

1. pinned source code;
2. reproducible runtime behavior and real tests/CI;
3. accepted project invariants/contracts;
4. independent audit evidence;
5. AI reports and design proposals.

A textual claim such as `PASS`, `implemented`, or `ready` is never sufficient evidence by itself.

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

No connected AI system may silently redefine these through an implementation convenience.

## Development strategy

The project intentionally builds the core while exercising it in real runtime conditions. Failures and observations from actual use are fed back into the next bounded engineering task.

The normal loop is:

```text
Build → Execute → Test → Attack → Correct → Re-test → Gate → Record → Build next
```

Runtime observations may reveal missing requirements or invariants, but they become architectural requirements only after explicit review and documentation.

## Future autonomy boundary

This multi-agent workflow is an engineering precursor to the intended Gnozis multi-agent architecture. It does **not** mean Gnozis is currently autonomous.

Before autonomous self-modification is enabled, the project must independently verify identity, capabilities, authorization, bounded operations, proof/invariants, rollback, durable auditability, recovery, and human override.
