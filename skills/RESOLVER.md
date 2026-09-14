# Skills Resolver

Skill routing table for human reading and disambiguation.

> **Source of truth for routing is each skill's `description` field.** Per the [agentskills.io spec](https://agentskills.io/specification), loaders match on `name + description` — there is no central catalog at runtime. This file is a **derived index**: it restates the routing for humans and adds the disambiguation rules that `description` fields alone cannot express. When this file and a skill's `description` disagree, **the `description` wins** — fix this file, not the field.

## Routing Principle

Route by the user's **artifact/object of work** before routing by workflow phase. Phase order is only a fallback after the work object is clear.

Priority when multiple skills could match:

1. **Explicit skill name or slash command** — user says `/debug`, `use tdd`, etc.
2. **Work object / artifact** — error log, diff, PRD, issue, rough idea, architecture scan.
3. **Most specific intent** — choose the skill whose outcome contract best matches the requested result.
4. **Workflow phase** — only as final fallback.

## Route by Work Object

| User provides / asks about | Skill | Why |
|---|---|---|
| New project, configure skills, issue tracker setup, initialize workflow | `setup-project` | Scaffold `docs/agents/` configuration and AGENTS.md before skills can run. |
| Rough idea, unclear requirements, feasibility, design approach, “how should we build this?” | `think` | Convert ambiguity into a decision-complete PRD. |
| Technical investigation needing durable capture — “what’s the best practice for X in version Y”, stack/version-specific research, authoritative-source lookup to reuse later | `research` | Persist an immutable, versioned research record into `docs/research/` + INDEX, so the next task queries INDEX instead of re-searching. |
| A divergence to settle by running code — conflicting options or a contested claim; “which is faster”, “which option survives concern C” (→ BENCH/SPIKE) | `have-a-try` | Minimal comparative demo: shared-harness measurement or concern×option matrix — selects or eliminates. |
| “Does this logic / state model hold up?” — state machine edges, data-model expressiveness (→ LOGIC) | `have-a-try` | Interactive probe (TUI, or shareable HTML for non-developers) with guided scenarios — validates or kills the design. |
| “What should this page look like?” — “try a few layouts”, “see a few options” (→ UI) | `have-a-try` | Several radically different UI variants on one route, switchable via `?variant=` — user picks. |
| Any other divergence running code can settle (→ CUSTOM) | `have-a-try` | Synthesized minimal experiment per the four-question rules in its REFERENCE. |
| Existing PRD/plan/terminology/domain model/ADR questions, “challenge this plan”, “is this design sound?” | `grill` | Stress-test plan against domain language and decision records. |
| Completed PRD or clear feature description needing tickets, issue breakdown, implementation tasks, vertical slices | `story` | Convert plan into executable Issues. Accepts PRD or direct description. |
| Issues or PRD ready for implementation, "implement this", orchestrate /tdd at seams / 实现 / 编码实现 / 开发 / 开始写代码 | `implement` | Orchestrate /tdd at pre-agreed seams, implement non-TDD items directly, typecheck + test per item, dispatch /review, commit per seam. |
| Accepted issue, known behavior to implement, explicit TDD/red-green-refactor request | `tdd` | Sub-agent orchestration: Test Sub-Agent → Human Review Gates → Develop Sub-Agent. One acceptance criterion per cycle. |
| Error, crash, failing test, regression, anomalous behavior, “used to work” | `debug` | Unknown root cause must be diagnosed before fixing. |
| Diff, staged/unstaged changes, completed work, merge readiness, release readiness | `review` | Parallel three-perspective sub-agent review: Test Review ∥ Code Review ∥ Impact Review. |
| Periodic health check, design debt scan, architecture review, proactive cleanup candidates | `improve-architecture` | Produce architecture improvement report and deepening opportunities. |
| Prose editing, polish, remove AI tone, rewrite, proofread, release notes, tweet, document review, localization copy | `write` | Rewrite and polish prose in Chinese or English; remove AI-like wording; review product localization. |

## Route by Workflow Phase

Phase view of the same routing. Trigger words live in each skill's `description` (the runtime source of truth) and in the work-object table above — restating them here is how the lists drift apart. This section adds only the phase ordering.

| Phase | Skills (typical order) |
|---|---|
| Project setup (first time) | `setup-project` |
| New feature (pre-build) | `think` → `research` / `have-a-try` (evidence gathering) → `grill` |
| Build | `implement` → `tdd` (driven at seams) · `story` output feeds both |
| Completion (post-build) | `review` |
| Bug fix (diagnostic) | `debug` → `review` (optional) |
| Architecture health (maintenance) | `improve-architecture` |
| Writing & editing (cross-phase) | `write` |

## Common Sequences

Skills don't auto-chain by default: each skill stops and waits for the user to trigger the next step. One exception — an **orchestrator skill may internally drive a model-invoked sub-skill as part of its own documented process** (`/implement` calls the Skill tool with "tdd" per seam; tdd's gates still apply). Cross-skill handoffs at completion (e.g. implement suggesting `/review`) always stop for the user.

**Project setup (first time):**
```
/setup-project → skills configured → /think (start feature work)
```

**New feature complete workflow:**
```
/think → user approves → /grill → /story → /implement → /review → merge/release
```
`/implement` handles per-seam orchestration: delegates to `/tdd` where suitable, implements directly otherwise, runs typechecking and tests after each item, commits per seam, then dispatches `/review` at the end.

```
/implement → per-seam [/tdd|direct → typecheck → test → commit] → full test suite → /review
```

`/think` Step 5 queries `docs/research/INDEX.md` first; on a hit it reuses the TL;DR, on a miss it may suggest `/research` to persist a durable record before committing to an approach.

**Technical investigation (standalone or embedded):**
```
/research <stack> <topic>-<major>   →  immutable record + INDEX row  →  /think (queries INDEX) or /grill (records ADR citing the research)
```
`/research` runs standalone to build the knowledge base, OR is effectively triggered inside `/think` Step 5 when a technical choice needs grounding. Records are immutable (ADR-0004); a new major creates a new file, never edits the old.

**Direct breakdown (user has a clear plan):**
```
/story → /implement → /review → merge/release
```
The `/tdd → /review` path remains available for single-issue manual TDD.

**New feature with a divergence worth settling by experiment:**
```
/think → /have-a-try (settles divergences reasoning can't) → /grill → /story → /implement → /review
```
`/have-a-try` is an optional branch, not a required step — and it has **four entry points**. Evidence flows back to where the divergence was born:

- **After `/think`**: the converged PRD still holds A-vs-B options → minimal demo settles it; verdict → PRD `Prototyped by` + Open Question closed → `/grill`.
- **During `/grill`**: a challenged decision that reasoning and reading can't settle → park the item, `/have-a-try`, verdict → ADR → resume the checklist.
- **After `/research`**: docs narrowed the candidates → `/have-a-try` BENCH/SPIKE settles the final call by measurement.
- **During `/story`/`/implement`**: a local design doubt → mini try → verdict on the issue/commit → continue the seam.

It writes disposable code; the verdict (selection or elimination) plus evidence flows into the PRD/ADR/issue, then the demo shell is deleted, absorbed, or archived to a throwaway branch when the verdict is contested.

**Bug fix workflow:**
```
/debug → root cause known → fix/regression test → /review (optional)
```

**Test-first implementation workflow:**
```
/tdd → /review
```
Direct single-issue TDD without the `/implement` orchestration layer.

**Periodic maintenance:**
```
/improve-architecture → review report → /grill (if terminology/ADR decisions) → /story (if approved improvements) → /implement (optional)
```

**Note on sub-agent orchestration:** `/tdd` now internally runs Acceptance Criterion Cycles — a 5-step loop per criterion (Test Sub-Agent designs scenarios → Scenario Review Gate → Test Sub-Agent writes tests (RED) → Code Review Gate → Develop Sub-Agent implements (GREEN)), followed by a unified Refactor phase after all cycles. `/review` now internally dispatches three parallel sub-agents (Test Review, Code Review, Impact Review), each independently re-reading all shared context, then merges their reports for human adjudication.

## Disambiguation

**"实现 / implement" conflict (`implement` vs `tdd` vs `story`):**
- User has multiple issues/seams from `/story`, wants end-to-end orchestration (typecheck, test, commit, review) → `/implement`.
- User has one well-defined acceptance criterion and wants focused TDD (red-green-refactor with human review gates) → `/tdd`.
- User has an idea that still needs breaking into tickets → `/story`.
- Rule of thumb: `/story` splits the work, `/implement` orchestrates the execution, `/tdd` executes a single unit. If you have tickets, use `/implement`; if you have one ticket, use `/tdd`.

**Bug/test failure conflict (`debug` vs `tdd`):**
- Root cause unknown, failing test unexplained, regression, crash, or anomaly → `/debug`.
- Root cause known and user wants test-first implementation of accepted behavior → `/tdd`.
- During `/debug`, Phase 5 may use TDD discipline locally; do not switch the main skill unless user asks.
- Note: `/tdd` now uses sub-agent orchestration (Test Sub-Agent → Human Review Gates → Develop Sub-Agent per acceptance criterion). If the user only wants a quick fix without the full cycle structure, `/debug` is more appropriate.

**"验证一下 / try it" conflict (`have-a-try` vs `think` vs `tdd`):**
- Vague idea, multiple paths, not sure *what* to build → `/think` (pure conversation, no code, produces a PRD).
- A divergence — conflicting options or a contested claim — that's cheaper to settle by *running* code than by reasoning (state machine edge, what a page looks like, which option is faster, whether an option survives a concern) → `/have-a-try` (minimal demo on the contested point; LOGIC probe / UI variants / BENCH / SPIKE / synthesized — selects or eliminates).
- Accepted behavior with known requirements, want a proper test-first implementation → `/tdd` (red-green-refactor with human review gates — the opposite of "skip the polish").
- Rule of thumb: `/think` doesn't write code; `/have-a-try` writes disposable code; `/tdd` writes production code with tests. If the user says "试一下" but the divergence can't even be named yet, suggest `/think` first.

**“审查” conflict (`grill` vs `review`):**
- PRD, plan, approach, terminology, domain model, ADR, “方案是否合理” → `/grill`.
- Diff, changed files, staged work, completed task, verification, merge/release readiness → `/review`.
- Note: `/review` now runs three parallel perspectives (Test Review, Code Review, Impact Review). It covers implementation quality and change impact, not plan design.

**Impact Review vs improve-architecture:**
- Local change impact, regression risk for current diff, compatibility and release strategy → `/review` (Impact Review sub-agent).
- Global architecture health, design debt scan, periodic code health check → `/improve-architecture`.

**“调研 / research” conflict (`research` vs `think` vs `have-a-try`):**
- Vague idea, multiple paths, not sure *what* to build → `/think` (converge to a PRD; it queries INDEX at Step 5 but doesn't itself persist research). Product/market/competitor analysis ("调研一下竞品都有什么功能") also lands here — it feeds the *what-to-build* decision, not the technical knowledge base.
- Concrete technical question against a specific stack+version, want to capture the best practice durably for reuse → `/research` (authoritative-source investigation → immutable record + INDEX).
- A divergence to settle by *running* code on your machine / your load (which option is faster, whether an option survives a concern, state machine edge, what a page looks like) → `/have-a-try` (disposable demo; selects or eliminates).
- Rule of thumb: `/think` decides *what* to build (no durable technical record); `/research` decides *how* a specific tech behaves per documentation (durable, sourced record); `/have-a-try` decides between options by measurement/observation (disposable code; verdict + evidence fixed into PRD/ADR). Typical chain: `/research` narrows candidates by docs → `/have-a-try` BENCH/SPIKE settles the final call. `/think` Step 5 internally consumes `/research` output via INDEX — you don't have to run `/research` manually first.

**"拆分任务" conflict (`story` vs `think`):**
- User has a clear, specific plan in mind and wants it broken into issues → `/story`
- User has a rough idea, needs help figuring out what to build → `/think`
- User asks to "break this down" but description is vague or ambiguous → suggest `/think` first, then `/story`
- User provides a detailed spec document (not PRD format) → `/story` can parse it directly

**“判断一下” special cases:**
- + error/anomaly/test failure → `/debug`.
- + is it worth it / which approach → `/think` evaluation mode.
- + architecture/design debt without active bug → `/improve-architecture`.

**“继续优化” special cases:**
- + error/regression → `/debug`.
- + accepted implementation issue → `/tdd`.
- + broad architecture/code health → `/improve-architecture`.

## Skill Inventory

Format files and update targets per skill. (Role and routing: see "Route by Work Object" above — restating them here is how the table drifts.)

| Skill | Format Files | Updates |
|-------|-------------|---------|
| `rules` **(bundle, not routable)** | — | Carries `anti-patterns.md`, `entry-protocol.md`, `sub-agent-runtime.md`, `writing-skills.md`, `engineering-principles.md` into installed copies. `disable-model-invocation` — never route task work here; the other skills link into it (`../rules/<file>.md`) |
| `setup-project` | — | `docs/agents/*.md` + AGENTS.md block |
| `think` | PRD-FORMAT.md | PRD + parent issue (required, Step 10) |
| `research` | RESEARCH-FORMAT.md<br>INDEX-FORMAT.md | `docs/research/<stack>-<topic>-<major>.md` + INDEX.md row (lazy-created) |
| `have-a-try` | — | Verdict (selected or eliminated) + evidence (PRD `Prototyped by` / ADR / commit / NOTES.md; concern×option matrix for SPIKE, numbers + environment for BENCH); demo deleted, core absorbed, or archived to throwaway branch |
| `grill` | CONTEXT-FORMAT.md<br>ADR-FORMAT.md | PRD + CONTEXT.md + ADRs + parent issue synced (if created by /think) |
| `story` | STORY-FORMAT.md | PRD (created or updated) + child issues + issues if confirmed |
| `implement` | — | Code + commits + PRD and issue status updates |
| `tdd` | — | Code + tests (via Acceptance Criterion Cycles) |
| `review` | — | Merged report + local docs + remote updates only when explicitly authorized |
| `debug` | — | Root cause report + code fix |
| `improve-architecture` | — | Architecture report + PRD `Arch reviewed by` field (when findings link to a PRD) |
| `write` | — | Edited prose only (no change list) |

> **Format Files column**: "—" means the skill's output format is embedded in REFERENCE.md rather than in a separate *-FORMAT.md file. Skills with named format files (PRD-FORMAT.md, STORY-FORMAT.md, etc.) use them as bilingual templates shared with the user.

## Prerequisites Matrix

Each skill may depend on files or configuration produced by earlier skills. Missing prerequisites are handled gracefully — the skill either works without them (with reduced precision) or suggests running a prerequisite skill first.

| Skill | Config (always read first) | Required | Optional (enhances output if present) | Format Contract | Auto-created by |
|-------|---------------------------|----------|---------------------------------------|----------------|-----------------|
| `setup-project` | — | Git repo | — | — | — (this is the foundation) |
| `think` | `domain.md` | — | `CONTEXT.md`, `docs/adr/`, existing PRDs, `docs/research/INDEX.md` | PRD-FORMAT.md | Creates PRD if user opts in |
| `research` | `domain.md` | A concrete stack×topic×major question | `CONTEXT.md`, `docs/adr/`, `docs/research/INDEX.md` (for dedup) | RESEARCH-FORMAT.md, INDEX-FORMAT.md | Creates `docs/research/` + INDEX lazily on first record |
| `have-a-try` | `domain.md` | A divergence — conflicting options or a contested claim, settleable by running code | `CONTEXT.md`, `docs/adr/`, PRD | — | — |
| `grill` | `domain.md` | PRD (`docs/prd/PRD-NNNN-<title>.md`) | `CONTEXT.md`, `docs/adr/` | CONTEXT-FORMAT.md, ADR-FORMAT.md | Creates `CONTEXT.md` and ADRs lazily |
| `story` | `domain.md`, `repo-map.md`, `issue-tracker.md`, `triage-labels.md` | — | `CONTEXT.md`, PRD | STORY-FORMAT.md (Issue body), minimal PRD | Creates minimal PRD if none exists |
| `implement` | `domain.md`, `repo-map.md`, `issue-tracker.md` | Issues from `/story` or PRD with Acceptance Criteria | `CONTEXT.md`, ADRs, `docs/research/INDEX.md`, `triage-labels.md` | Issues from `/story`; expects `/tdd` output | PRD Status update (→ `In Progress`), issue status update (→ `Done`), commits |
| `tdd` | `domain.md`, `repo-map.md` | — | `issue-tracker.md`, PRD, `CONTEXT.md`, ADRs | Issue body = STORY-FORMAT.md | — |
| `review` | `domain.md`, `repo-map.md` | Code changes (staged or unstaged) | PRD, `CONTEXT.md`, ADRs, CI configs | Issue body = STORY-FORMAT.md | Updates local docs when verified |
| `debug` | `domain.md`, `repo-map.md` | Reproducible error or symptom | `CONTEXT.md`, ADRs | — | — |
| `improve-architecture` | `domain.md`, `repo-map.md` | — | `CONTEXT.md`, `docs/adr/`, `docs/prd/*.md`, `docs/audits/*.md` | — | — |
| `write` | `domain.md` | Text to edit | Project style references, existing releases, `CONTEXT.md` | — | — |

**Config column**: Files under `docs/agents/`. `domain.md` tells consumer skills where domain docs live. `repo-map.md` tells them about multi-repo structure. `language.md` tells them what language to write human-facing output in (PRDs, ADRs, CONTEXT, Issues). All are optional — skills fall back to default paths (and, for language, the user's input language) if missing.

**Format Contract column**: The output format expected by downstream skills. "Issue body = STORY-FORMAT.md" means issues created by the skill use the Story Format body.

**Config maintenance:** `/setup-project` creates `docs/agents/` configuration that consumer skills read. When project structure changes (repos added/removed, issue tracker switched, domain docs reorganized, doc language changed), re-run `/setup-project` — it reads existing config, detects drift, and updates only what changed. Consumer skills may suggest running `/setup-project` if they detect missing or stale config.

## Mid-Skill Switching

Users may switch skills at any time. Rules:

1. **Current skill stops immediately** — do not complete remaining steps of the previous skill.
2. **Intermediate artifacts are preserved** — partial PRDs, CONTEXT.md updates, and created issues remain on disk. The new skill reads the current state and decides what to use.
3. **Do not clean up** — the new skill may produce different files that supersede the old ones, or the user may return to the previous skill later.
4. **State what changed** — when entering a new skill after switching, briefly acknowledge the switch and state which prior artifacts you're building on.

## Shared Rules

Cross-skill behavioral constraints live in `rules/anti-patterns.md`. Skills should reference this file directly when applying global rules; it is a shared reference, not a standalone workflow skill.

The shared bootstrap sequence lives in `rules/entry-protocol.md`. All skills reference this protocol instead of duplicating context-read instructions. It ensures skills work standalone (graceful degradation) and composable (reads prior skill outputs via Traceability chain).

The shared engineering-principle catalog lives in `rules/engineering-principles.md` — the single definition of SOLID (SRP/OCP/LSP/ISP/DIP), DRY, KISS, YAGNI, LoD, composition over inheritance, explicit over implicit, fail fast, and immutability/purity, plus the gates that keep principle findings from becoming nitpicks (named consequence required; severity defaults to `minor`, and a principle tag never creates a blocker; scope stops at the diff) and the consumer/ownership map. Consuming skills: `review` (Code Review owns the diff-local principles, Impact Review owns DIP/OCP and cross-module coupling), `improve-architecture` (§3.2 owns the scan thresholds), `tdd` (Refactor phase, `refactor-safe` entries only), `implement` (direct implementation). Skills link to it and never restate definitions (#38).

Key anti-patterns for sub-agent skills:
- **#30 Procedural front-loading** (anti-pattern #30) — every SKILL.md opens with its outcome contract before any procedure; workflow detail stays in REFERENCE.md
- **#34 Skill-to-skill state drift** (anti-pattern #34) — re-read latest shared files when entering a skill
- **#35 Sub-agent state leakage** (anti-pattern #35) — each sub-agent independently re-reads all shared context from disk; no shared memory, no cached understanding

## Project Structure

> **Note:** In `tdd/` and `review/`, REFERENCE.md contains sub-agent instruction chapters describing each sub-agent's responsibilities, checklists, and independence constraints.

The canonical directory tree lives in `AGENTS.md` (Repository Structure section) so it drifts in one place, not across files. See there for the authoritative layout. The routing table and disambiguation rules in this file are the **human-readable reference**; the runtime source of truth for routing is each skill's `description` field (see the header note above). `AGENTS.md` and `README.md` carry only a pointer plus headline summaries, not a verbatim copy.
