# Reproducible Self-Diagnostic Corpus

This directory contains deterministic evidence corpora generated from real Ψ-Core execution for reflection experiments.

## Rules

- Corpus files must be generated from executable Core runs, never hand-authored as findings.
- The corpus is evidence, not a claim that any rule is defective.
- Diagnostic output remains read-only.
- Each corpus records provenance: source commit, scenario identifier, transition count, and generation method.
- Controlled scenarios must be explicitly labeled as experiments and must not be presented as production history.

## Diagnostic #0001

The first corpus is a controlled integration experiment. It validates:

```text
Core execution
  -> TransitionRecord
  -> SQLite persistence
  -> recovery
  -> Self-Diagnostic
  -> diagnostic artifact
```

The controlled scenario is deliberately repeated so the reflection layer has sufficient evidence to form a finding. Its conclusions require independent review.
