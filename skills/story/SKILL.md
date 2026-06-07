---
name: story
description: "Break PRD into executable Issues. Use vertical slices (tracer bullets) to decompose plan into end-to-end tasks. Use when user wants to convert PRD to Issues, create implementation tickets, or breakdown work."
when_to_use: "breakdown,story,拆分,Issues,tasks,subtasks,decompose"
dispatch_intent: "Convert PRD to Issues, create implementation tickets"
---

# Story: Break PRD Into Issues

🥷 Vertical slices, each issue is end-to-end.

Break plan into independently actionable issues using vertical slices (tracer bullets).

## Outcome Contract

- **Outcome**: Set of GitHub Issues, each executable independently, covering full PRD
- **Done when**: All issues created with dependencies mapped, PRD updated with child issues
- **Evidence**: Created GitHub Issues with proper acceptance criteria, updated PRD with child issue links
- **Output**: Issue count list, updated PRD, next step to `/tdd`

## Prerequisites

- PRD file must exist (completed by `think` and `grill`)
- Issue tracker and triage label vocabulary should be configured

## Process Summary

**Step 1**: Read PRD at `docs/prd/<feature-name>.md`

**Step 2**: Explore codebase (optional) — understand current state, use domain glossary, respect ADRs

**Step 3**: Draft vertical slices — each is a thin vertical slice through all layers (schema, API, UI, tests)

**Step 4**: Present to user — show title, type (HITL/AFK), blocked-by, user stories

**Step 5**: Publish issues in dependency order (blockers first)

**Step 6**: Update PRD with child issues

**Step 7**: Sync GitHub Issue (if parent exists)

**Slice Types:**
- **HITL**: Human-in-the-loop (architecture decisions, design reviews)
- **AFK**: Away-from-keyboard (implementable without human interaction)

See [REFERENCE.md](REFERENCE.md) for issue template and example.

Shared behavioral constraints: apply [../rules/anti-patterns.md](../rules/anti-patterns.md) when a global anti-pattern is relevant.

## Gotchas

| What happened | Rule |
|---|---|
| Horizontal slicing (all schema, then all API) | Use vertical slices through all layers |
| Slices too thick | Prefer many thin slices over few thick ones |
| Dependencies wrong | Publish in dependency order (blockers first) |
| PRD/parent issue not updated | Step 6/7: Update PRD and sync GitHub Issue |

## Vertical Slice Rules

- Each slice traces one narrow but **complete** path through every layer
- Completed slice is demonstrable or verifiable on its own
- Prefer many thin slices over few thick ones
- Avoid file paths or code snippets — they become stale

## Output

```
Story complete.

Created issues:
* #<issue-1> — <title> (AFK)
* #<issue-2> — <title> (HITL, blocked by #1)

Updated files:
- docs/prd/<name>.md — child issues updated

Next: Run /tdd to start implementing first issue.
```

## Example

```
PRD: User subscription functionality

Proposed:
1. Create subscription data model (AFK) — schema + API + tests
2. Payment flow integration (AFK, blocked by #1) — gateway + webhooks + tests
3. Management UI (HITL, blocked by #2) — design review + components + E2E

User: granularity looks right, proceed

[Create 3 issues]
[Update PRD]
```
