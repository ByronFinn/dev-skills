# 0001 - Sub-Agent Orchestration Pattern for Multi-Phase Skills

Date: 2026-06-12

## Status

Accepted

## Context

dev-skills is a pure Markdown instruction set — there is no runtime, no build step, and no agent scheduler. Skills describe workflows that AI coding agents follow. Currently, TDD and Review skills each execute as a single agent context. This creates cognitive coupling: the same agent that writes tests also implements the code, and the same review context evaluates everything from test quality to release readiness.

The user identified that independent execution perspectives (separate agents for testing vs development, separate review perspectives) would surface more issues and improve quality. The challenge is: how do you achieve agent independence in a system that only produces Markdown files?

## Decision

We adopt a **sub-agent orchestration pattern** within existing skill directories:

- `/tdd` and `/review` commands remain unchanged for the user
- Each skill's SKILL.md becomes an **orchestrator** that describes the sequencing of sub-agents
- Each skill's REFERENCE.md contains **independent instruction chapters** for each sub-agent
- Each sub-agent chapter specifies: context re-read checklist, independent responsibilities, checklists, output templates, and independence constraints
- Sub-agents do not share internal state or cached understanding — each re-reads all shared context (PRD, Story, Issues, CONTEXT.md, ADRs) from disk before acting

The key insight: "sub-agent" is a logical concept implemented through instruction-level isolation in Markdown. The AI agent reading the skill instructions follows each sub-agent chapter as if starting fresh.

## Consequences

### Positive

* Test design and implementation are truly independent perspectives reading the same requirements
* Review covers three distinct dimensions (test quality, code quality, impact) without one perspective biasing another
* User commands don't change — no learning curve
* Each sub-agent chapter is self-contained and can be read/understood independently
* PRD ambiguities are naturally surfaced when two independent interpretations diverge

### Negative

* Skill files become longer and more complex internally
* Each sub-agent re-reading context adds implicit overhead (though this is agent behavior, not runtime cost)
* The "independence" guarantee depends on the AI agent faithfully following the instruction to re-read from disk
* Debugging workflow issues requires understanding the orchestrator + sub-agent pattern

## Alternatives Considered

* **Separate top-level skill directories** (e.g., `write-test/`, `develop/`, `test-review/`): Cleaner separation but forces users to learn new commands (`/write-test`, `/develop`) and manually sequence them. Breaks the existing workflow pipeline.
* **Single agent with perspective switching**: Agent switches "hats" within one context. Simpler but doesn't achieve true independence — the agent still carries cached understanding from the previous phase.
* **Runtime orchestration layer**: Build an actual scheduler that manages agent sessions. Far beyond dev-skills' scope as a Markdown-only project.

## References

* CONTEXT.md — Sub-Agent, Orchestrator, Acceptance Criterion Cycle definitions
* anti-patterns.md #37 (Skill-to-skill state drift) — existing cross-skill re-read rule
