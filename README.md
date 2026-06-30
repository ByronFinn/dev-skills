# Engineering Skills

[![skills.sh](https://skills.sh/b/ByronFinn/dev-skills)](https://skills.sh/ByronFinn/dev-skills)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

Reusable agent skills for software engineering workflows — from idea to release.

Skills are Markdown-based instruction sets loaded by AI coding agents (e.g., Claude Code via [skills.sh](https://skills.sh)). No application code, no build step, no runtime — the **skill documents themselves are the product**.

## Quick Start

```bash
# Install all skills into your project
npx skills@latest add ByronFinn/dev-skills

# In your repo, configure skill behavior (one-time)
/setup-project

# Start building a feature
/think
```

That's it. Each skill is triggered by a slash command and stops when done — skills never auto-chain. You decide when to move to the next step.

## Why This Exists

AI coding agents are powerful but inconsistent. They skip planning, forget domain context, mix test design with implementation, and lose track of decisions. This project solves that with **structured skill documents** that enforce engineering discipline:

- **Think before code** — brainstorm and converge before writing anything
- **Challenge before implement** — stress-test plans against domain model
- **Test before implement** — red-green-refactor with independent sub-agent perspectives
- **Review before merge** — parallel three-perspective review with contradiction surfacing
- **Root cause before fix** — systematic debugging with reproducible feedback loops

## Skills

| Skill | Command | Input | Output | Description |
|-------|---------|-------|--------|-------------|
| **setup-project** | `/setup-project` | Repo state | `docs/agents/` config | One-time scaffold: issue tracker, triage labels, domain doc layout. Re-runnable when project structure changes. |
| **think** | `/think` | Rough idea or feature description | PRD (`docs/prd/`) | Brainstorm → converge to decision-complete plan. Research-first for technical choices. |
| **grill** | `/grill` | Existing PRD | Validated PRD + CONTEXT.md + ADRs | Challenge every open decision. Sharpen terminology. Walk the design tree until shared understanding. |
| **story** | `/story` | PRD or direct description | Vertical-slice Issues | Break plan into independently executable issues (tracer bullets). HITL/AFK typing. |
| **tdd** | `/tdd` | Issue, PRD, or description | Code + tests (GREEN) | Sub-agent orchestrated red-green-refactor. Per-criterion cycles with two-stage human review gates. Gate Modes: Full / Fast / Batch. |
| **review** | `/review` | Code changes (diff) | Merged three-perspective report | Parallel Test Review ∥ Code Review ∥ Impact Review. Contradictions surfaced for human adjudication. Integration Review for multi-slice features. |
| **debug** | `/debug` | Error, crash, regression | Root cause + fix + regression test | Systematic 6-phase loop. Feedback loop first, then hypothesize-instrument-fix. Environment diff, bisect, and scope scan modes. |
| **improve-architecture** | `/improve-architecture` | Codebase + PRDs + ADRs | Architecture improvement report | Scan for design debt, ADR compliance, deepening opportunities. Blocking/High/Medium priority with scope estimates. |
| **write** | `/write` | Prose, draft, or doc to review | Edited prose (no change list) | Strip AI tone, polish, rewrite. Release notes, launch/social copy, localization, document review. |

## Workflow

Skills compose into standard engineering workflows. Each skill **stops** after its output — you trigger the next step.

### New Feature (full pipeline)

```
/setup-project → /think → /grill → /story → /tdd → /review → merge/release
```

### Direct Implementation (clear plan, skip brainstorming)

```
/story → /tdd → /review → merge/release
```

### Bug Fix

```
/debug → /review (optional)
```

### Architecture Health Check (periodic)

```
/improve-architecture → /grill (if decisions) → /story (if approved) → /tdd
```

### Routing

Route by your **work object**, not workflow phase:

| You have / want to do | Skill |
|---|---|
| New project, need configuration | `setup-project` |
| Rough idea, unclear requirements | `think` |
| PRD/plan to challenge | `grill` |
| Plan to break into tickets | `story` |
| Accepted issue to implement | `tdd` |
| Error, crash, regression | `debug` |
| Completed work / diff to review | `review` |
| Architecture health / design debt | `improve-architecture` |
| Prose editing / polish / de-AI / release notes / localization | `write` |

Full disambiguation rules: [`skills/RESOLVER.md`](skills/RESOLVER.md)

## Design Principles

### Standalone + Composable

Every skill works **on its own** — no hard dependencies on prior skills. Missing prerequisites trigger graceful degradation, not errors. When chained, skills read prior outputs through the **PRD Traceability chain**:

```
Created by → Grilled by → Sliced by → Implemented by → Reviewed by
                                ↑                    ↑
                          Debugged by        Arch reviewed by
```

The [`Entry Protocol`](skills/rules/entry-protocol.md) standardizes this bootstrap: locate domain docs → check upstream artifacts → proceed with or without them.

### Sub-Agent Orchestration

TDD and Review skills use a **sub-agent pattern** — each sub-agent independently re-reads all shared context from disk before acting, with no shared memory or cached understanding ([ADR-0001](docs/adr/0001-sub-agent-orchestration-pattern.md)):

- **TDD**: Test Sub-Agent (design scenarios → write tests) → Human Review Gates → Develop Sub-Agent (implement → refactor)
- **Review**: Test Review ∥ Code Review ∥ Impact Review → merge with contradiction highlighting

This is a logical concept implemented through instruction-level isolation in Markdown — no runtime scheduler needed.

### Evidence Over Claims

Skills enforce the discipline of running commands and pasting output. "Should work" is never acceptable evidence. Every conclusion must cite a verification command or explicit runtime check.

### Minimal Change

Fix what was asked, nothing more. After fixing one instance of a pattern, grep for siblings. Scope creep is flagged, not silently absorbed.

## Shared Rules

| File | Purpose |
|------|---------|
| [`skills/rules/anti-patterns.md`](skills/rules/anti-patterns.md) | Cross-skill behavioral constraints (41 rules, always apply). Covers everything from "read before acting" to "sub-agent state independence" to "session recovery". |
| [`skills/rules/entry-protocol.md`](skills/rules/entry-protocol.md) | Shared bootstrap sequence all skills apply before starting — locate domain docs, check upstream artifacts, ensure standalone/composable execution. |

## Key Concepts

<details>
<summary><b>PRD (Product Requirements Document)</b></summary>

Format: [`skills/think/PRD-FORMAT.md`](skills/think/PRD-FORMAT.md) · Location: `docs/prd/<feature>.md`

The central artifact. Created by `/think` or `/story`, validated by `/grill`, implemented by `/tdd`, verified by `/review`. Contains goal, requirements, acceptance criteria, technical approach, and a Traceability section tracking every skill that touched it.

</details>

<details>
<summary><b>CONTEXT.md (Domain Glossary)</b></summary>

Format: [`skills/grill/CONTEXT-FORMAT.md`](skills/grill/CONTEXT-FORMAT.md) · Location: repo root

Ubiquitous language for the project. Pure terminology definitions — no implementation details. Created and maintained by `/grill`. Consumer skills use its vocabulary for naming, test design, and documentation.

</details>

<details>
<summary><b>ADR (Architecture Decision Record)</b></summary>

Format: [`skills/grill/ADR-FORMAT.md`](skills/grill/ADR-FORMAT.md) · Location: `docs/adr/<NNNN>-<title>.md`

Records hard-to-reverse, surprising, real-trade-off decisions. Created sparingly by `/grill` — only when all three conditions are met. Checked for compliance by `/improve-architecture` and `/review`.

</details>

<details>
<summary><b>Human Review Gate</b></summary>

Blocking checkpoint in `/tdd` where a human must approve before the next phase begins. Two stages per acceptance criterion (default Full mode): **Scenario Review Gate** (test design quality) and **Test Code Review Gate** (code quality + fidelity). See [ADR-0002](docs/adr/0002-two-stage-human-review-gate.md). Fast and Batch modes available for experienced users.

</details>

## Repository Structure

The canonical structure tree lives in [`AGENTS.md`](AGENTS.md#repository-structure) (kept current there so it drifts in one place, not three). In short: each skill is a directory under `skills/` with a `SKILL.md` entry point and (optionally) a `REFERENCE.md` for detail and `*-FORMAT.md` templates; shared rules and the routing table sit alongside.

Every skill follows the same internal structure:

| File | Purpose |
|------|---------|
| `SKILL.md` | Entry point — YAML front matter, outcome contract, process summary, gotchas, output template |
| `REFERENCE.md` | Detailed steps, checklists, examples, sub-agent chapters |

## Project Documentation

This project dogfoods its own skills:

- [CONTEXT.md](CONTEXT.md) — domain model (demonstrates `/grill` output)
- [CHANGELOG.md](CHANGELOG.md) — version history
- [docs/prd/](docs/prd/) — PRDs for the project itself
- [docs/adr/](docs/adr/) — Architecture Decision Records

## Requirements

- An AI coding agent that supports [skills.sh](https://skills.sh) skill loading (e.g., Claude Code)
- Git repository (for diff-based skills like `review` and `debug`)
- Optional: `gh` CLI (for GitHub issue tracker integration in `story` and `review`)

## Contributing

See [AGENTS.md](AGENTS.md) for project conventions, file structure rules, and language guidelines.

When adding or modifying skills:
1. Follow existing structure: `SKILL.md` (entry) → `REFERENCE.md` (detail) → `*-FORMAT.md` (templates)
2. Keep `SKILL.md` concise; move deep detail to `REFERENCE.md`
3. Update `RESOLVER.md` routing when adding/changing skills
4. Run `anti-patterns.md` rules against your own output
5. Reference `entry-protocol.md` for shared bootstrap — don't duplicate context-read instructions
6. Update `CHANGELOG.md` with your changes

## License

[MIT](LICENSE)
