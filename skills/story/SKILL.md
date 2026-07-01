---
name: story
description: "Break a plan into executable Issues using vertical slices. Accepts an existing PRD or a direct feature description. Use when user wants to convert a plan to Issues, create implementation tickets, or breakdown work."
when_to_use: "breakdown,story,拆分,Issues,tasks,subtasks,decompose"
dispatch_intent: "Convert plan to Issues, create implementation tickets"
---

# Story: Break Plan Into Issues

🥷 Vertical slices, each issue is end-to-end.

Break plan into independently actionable issues using vertical slices (tracer bullets). Accepts an existing PRD or a direct feature description.

## Outcome Contract

- **Outcome**: Set of Issues, each executable independently, covering the full plan
- **Done when**: All issues created with dependencies mapped; PRD created or updated with child issues
- **Evidence**: Created Issues with proper acceptance criteria, PRD (created or updated) with child issue links
- **Output**: Issue count list, PRD created/updated, next step to `/tdd`

## Prerequisites

- **Input**: an existing PRD at `docs/prd/PRD-NNNN-<title>.md`, or a direct feature description from the user
- Apply the [Skill Entry Protocol](../rules/entry-protocol.md) to locate domain docs and issue tracker config
- `docs/agents/issue-tracker.md` — read for issue creation convention
- `docs/agents/triage-labels.md` — read for label mapping
- If tracker files are not found, ask the user which issue tracker they use (GitHub / GitLab / Local / Other), then create the files with matching convention. Or suggest running `/setup-project` for full interactive setup.

## Process Summary

**Step 0**: Determine input source — locate existing PRD, or capture feature description from user

**Step 1**: Extract requirements — from PRD or from user description + codebase exploration

**Step 2**: Ensure PRD exists — if not, create a minimal PRD capturing the requirements

**Step 3**: Explore codebase (optional) — understand current state, use domain glossary, respect ADRs

**Step 4**: Draft vertical slices — each is a thin vertical slice through all layers (schema, API, UI, tests)

**Step 5**: Present to user — show title, type (HITL/AFK), blocked-by, user stories

**Step 6**: Publish issues in dependency order (blockers first). Issue title format: `[PRD-NNNN] <slice-description> — <core-behavior>`. Issue body includes a `Meta` section (PRD reference, Type, Siblings).

**Step 7**: Update PRD with child issues; set `Status` to `Sliced` in the PRD metadata line. Update the `## Traceability` `Sliced into` field with the child issues list (number, title, type, status).

**Step 8**: Sync Issue (if parent exists). Update the parent Issue body, append child issues list.

**Slice Types:**
- **HITL**: Human-in-the-loop — requires human judgment (architecture, design, UX). Agent pauses at decision points for input.
- **AFK**: Away-from-keyboard — implementable end-to-end without human interaction.

See [REFERENCE.md](REFERENCE.md) for issue template, input handling, and example.

## Gotchas

| What happened | Rule |
|---|---|
| Horizontal slicing (all schema, then all API) | Use vertical slices through all layers |
| Slices too thick | Prefer many thin slices over few thick ones |
| Dependencies wrong | Publish in dependency order (blockers first) |
| PRD/parent issue not updated | Step 7/8: Update PRD and sync Issue |
| Input too vague for slicing | Suggest `/think` — do not run a full brainstorming session yourself |
| Same topic got two PRDs (e.g. PRD-0001 + PRD-0002) | Step 3 (Ensure PRD Exists): run Entry Protocol Step 3a conflict check before creating |

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
- docs/prd/PRD-NNNN-<title>.md — child issues updated (Status → Sliced)

Next: Run /tdd to start implementing first issue.
```

## Example

```
PRD: User subscription (PRD-0003-subscription)

Proposed:
1. Create subscription data model (AFK) — schema + API + tests
2. Payment flow integration (AFK, blocked by #1) — gateway + webhooks + tests
3. Management UI (HITL, blocked by #2) — design review + components + E2E

User: granularity looks right, proceed → [Create 3 issues, Update PRD]
```
