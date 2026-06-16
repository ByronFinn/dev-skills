# Skill Entry Protocol

Shared bootstrap sequence for all skills. Each skill references this protocol instead of repeating the full instructions.

## Purpose

Every skill needs to locate domain docs, identify multi-repo scope, and check for upstream artifacts before starting work. This protocol standardizes that bootstrap. It ensures skills can run **standalone** (graceful degradation when prerequisites are missing) and **composable** (correctly reads prior skill outputs when chained).

## Protocol

When entering any skill, perform this read sequence **before** starting skill-specific work:

### Step 1: Read Project Config

Read config files under `docs/agents/` (created by `setup-project`). If the directory doesn't exist, skip to defaults.

| File | What it tells you | If missing |
|------|-------------------|------------|
| `docs/agents/domain.md` | Actual paths for CONTEXT.md, PRDs, ADRs (may differ from defaults in multi-repo/monorepo) | Use default paths (Step 3) |
| `docs/agents/repo-map.md` | Multi-repo structure — which repos exist, which owns the issue tracker | Treat as single-repo |
| `docs/agents/issue-tracker.md` | Issue tracker type and CLI conventions | Ask user which tracker they use |
| `docs/agents/triage-labels.md` | Label vocabulary mapping | Use canonical defaults |

### Step 2: Identify Multi-Repo Scope

If `repo-map.md` exists, identify which repos are involved in the current task. Cross-repo tasks require reading domain docs from all relevant repos.

If `repo-map.md` is missing, treat the current repo as the only repo. If the task mentions files or modules outside this repo, ask the user.

### Step 3: Read Domain Context

Read domain docs at the paths discovered in Step 1 (or defaults if config missing):

| Document | Default path | Purpose |
|----------|-------------|---------|
| CONTEXT.md | `CONTEXT.md` at repo root | Domain glossary — terminology, concepts, relationships |
| PRDs | `docs/prd/<feature>.md` | Product requirements — what to build, acceptance criteria |
| ADRs | `docs/adr/*.md` | Architecture Decision Records — past technical decisions |

**If any document is missing, proceed without it.** Missing context reduces precision but does not block execution. State what's missing so the user knows the limitation.

### Step 4: Check Upstream Artifacts (Composability)

If the skill consumes another skill's output, verify upstream quality:

| Signal | Meaning | Action |
|--------|---------|--------|
| PRD Traceability shows `Created by: /story (minimal PRD)` | Requirements may not be decision-complete — no `/think` session | Confirm acceptance criteria with user before proceeding |
| PRD has `Open Questions` or `TODO` markers | `/grill` may not have resolved all decisions | Note: "PRD has unresolved items" — proceed but flag uncertainty |
| PRD `Grilled by` field is empty | Plan not validated against domain model | Proceed but note plan is unvalidated |

These are notes, not blockers. Record them in the skill's output.

## Standalone vs Composable

**Standalone (no prior skill ran):** The skill works with whatever context exists. If no PRD, no CONTEXT.md, no ADRs — the skill derives what it can from the codebase and user input. It does not refuse to start.

**Composable (prior skills ran):** The skill reads prior outputs via the Traceability chain in PRD files. Each PRD's `## Traceability` section records which skills touched it, enabling the current skill to verify completeness.

## Reference

Skills should reference this protocol as:
```
Apply the [Skill Entry Protocol](../rules/entry-protocol.md) before proceeding.
```
