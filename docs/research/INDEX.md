# Research Index

> Entry point for every research record. Query here first; reuse the TL;DR on a hit, start new research only on a miss.
> Status values: verified (validated) | stale (current project major is higher; suggest re-research) | deprecated (abandoned).

## By Stack

### agentskills

| Topic | Major | Version | Verdict | File | Status |
|---|---|---|---|---|---|
| skill-authoring | 1 | agentskills@unknown (2026-09 snapshot) | Spec mechanics + official authoring bar: name/description-only, <1024-char pushy description, SKILL.md <500 lines outcome-contract-first, conditional file refs, defaults-not-menus, two-track evaluation (20-query trigger + with/without output evals) | [agentskills-skill-authoring-1.md](agentskills-skill-authoring-1.md) | verified |

### agent-interviewing

| Topic | Major | Version | Verdict | File | Status |
|---|---|---|---|---|---|
| question-pacing | 1 | agent-interviewing@unknown | One question per message with recommended answer; next question derived from the last answer until the tree is exhausted — academically and community-supported, officially unmandated; adopted as dev-skills product decision | [agent-interviewing-question-pacing-1.md](agent-interviewing-question-pacing-1.md) | verified |

### gepa

| Topic | Major | Version | Verdict | File | Status |
|---|---|---|---|---|---|
| eval-loop | 1 | gepa@0.1.4 | GEPA loop: per-sample (score + textual feedback), dual-sided small datasets, 60/40 train/holdout, select best candidate by holdout under a fixed budget — not scalar pass rates, not last iteration | [gepa-eval-loop-1.md](gepa-eval-loop-1.md) | verified |

## By Topic

> Cross-stack comparison of the same topic. Single-stack topics are kept too (listed when ≥1), so a future new stack immediately sees the existing baseline.

| Topic | Stacks | See |
|---|---|---|
| skill-authoring | agentskills@1 | [agentskills-skill-authoring-1.md](agentskills-skill-authoring-1.md) |
| question-pacing | agent-interviewing@1 | [agent-interviewing-question-pacing-1.md](agent-interviewing-question-pacing-1.md) |
| eval-loop | gepa@1 | [gepa-eval-loop-1.md](gepa-eval-loop-1.md) |
