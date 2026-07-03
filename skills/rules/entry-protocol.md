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
| `docs/agents/language.md` | Language consumer skills should write human-facing output in (PRDs, ADRs, CONTEXT, Issues, comments) | Fall back to the user's input language; ask when unsure |

### Step 2: Identify Multi-Repo Scope

If `repo-map.md` exists, identify which repos are involved in the current task. Cross-repo tasks require reading domain docs from all relevant repos.

If `repo-map.md` is missing, treat the current repo as the only repo. If the task mentions files or modules outside this repo, ask the user.

### Step 3: Read Domain Context

Read domain docs at the paths discovered in Step 1 (or defaults if config missing):

| Document | Default path | Purpose |
|----------|-------------|---------|
| CONTEXT.md | `CONTEXT.md` at repo root | Domain glossary — terminology, concepts, relationships |
| PRDs | `docs/prd/PRD-NNNN-<title>.md` | Product requirements — what to build, acceptance criteria |
| ADRs | `docs/adr/*.md` | Architecture Decision Records — past technical decisions |
| Research INDEX | `docs/research/INDEX.md` | Searchable index of persisted technical research records (stack × topic × major). Query before re-searching; see `/research` skill |

**If any document is missing, proceed without it.** Missing context reduces precision but does not block execution. State what's missing so the user knows the limitation.

**Filing-consistency check.** While scanning for these docs, also flag misplaced files so the drift surfaces early. Report (do not auto-fix — moving files is a destructive op needing explicit authorization):

- PRD content found **outside** `docs/prd/` — e.g. `docs/adr/PRD-*.md`, `docs/prd-*.md` in the docs root, or `PRD-*.md` at repo root.
- ADR files carrying a `PRD-` prefix, or PRD files carrying no `PRD-` prefix.
- Research records found **outside** `docs/research/` — e.g. `<stack>-<topic>-<major>.md` at repo root or under `docs/`.
- **Number collisions** — two ADRs sharing the same `NNNN`, or two PRDs sharing the same `PRD-NNNN` (common when multiple sessions run concurrently). Scan the directory and report any duplicate numbers before creating a new file.
- **Research record collisions** — two records sharing the same `<stack>-<topic>-<major>` filename (a `/research` duplicate; see `/research` Step 2 dedup).

Report findings as a note in the skill output: *"Filing inconsistency found: <file> appears misplaced / <NNNN> is used by two files. Want me to relocate?"* Do not silently move or renumber.

### Step 3a: PRD Conflict Check (only for PRD-creating skills)

Applies **only** to skills about to create a new PRD file (`/think` Step 2, `/story` Step 3). Skills that only read an existing PRD — and all non-PRD skills (`/write`, `/debug`, `/review`, etc.) — skip this entirely.

The full procedure lives with the primary PRD-creator: see [think/REFERENCE.md §PRD Conflict Check](../think/REFERENCE.md#prd-conflict-check-before-assigning-nnnn). It is owned there rather than in this shared protocol so that non-PRD skills don't carry PRD-management ceremony they never use. `/story` follows the same procedure when it creates a minimal PRD.

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
