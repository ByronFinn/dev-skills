# Skills Resolver

Skill routing table. Claude Code auto-matches via each SKILL.md's `description`. This doc is a human-readable central index and conflict resolver.

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
| Design doubt easier to resolve by *running* code than reasoning on paper — state machine edges, data-model expressiveness, “does this logic feel right?” (→ LOGIC) | `have-a-try` | Build a throwaway terminal prototype that answers one logic/state question. Sits between `/think` and `/grill`. |
| Design doubt about what a page should *look like* — “try a few layouts”, “see a few options” (→ UI) | `have-a-try` | Build several radically different UI variants on one route, switchable via `?variant=`. |
| Existing PRD/plan/terminology/domain model/ADR questions, “challenge this plan”, “is this design sound?” | `grill` | Stress-test plan against domain language and decision records. |
| Completed PRD or clear feature description needing tickets, issue breakdown, implementation tasks, vertical slices | `story` | Convert plan into executable Issues. Accepts PRD or direct description. |
| Accepted issue, known behavior to implement, explicit TDD/red-green-refactor request | `tdd` | Sub-agent orchestration: Test Sub-Agent → Human Review Gates → Develop Sub-Agent. One acceptance criterion per cycle. |
| Error, crash, failing test, regression, anomalous behavior, “used to work” | `debug` | Unknown root cause must be diagnosed before fixing. |
| Diff, staged/unstaged changes, completed work, merge readiness, release readiness | `review` | Parallel three-perspective sub-agent review: Test Review ∥ Code Review ∥ Impact Review. |
| Periodic health check, design debt scan, architecture review, proactive cleanup candidates | `improve-architecture` | Produce architecture improvement report and deepening opportunities. |
| Prose editing, polish, remove AI tone, rewrite, proofread, release notes, tweet, document review, localization copy | `write` | Rewrite and polish prose in Chinese or English; remove AI-like wording; review product localization. |

## Route by Workflow Phase

### Project Setup (First time)

| Trigger | Skill | Description |
|---------|-------|-------------|
| setup / 初始化 / 配置技能 / issue tracker setup / new project | `setup-project` | Scaffold `docs/agents/` configuration and AGENTS.md block |

### New Feature Development (Pre-build)

| Trigger | Skill | Description |
|---------|-------|-------------|
| brainstorm / 构思 / 方案 / 出方案 / 深入分析 / 怎么设计 | `think` | Diverge on possibilities, converge to concrete plan, generate initial PRD and issue |
| research / 调研 / 最佳实践 / best practice / 技术选型 / tech evaluation / 选哪个库 / 官方文档 / how does X work in version Y / 权威信源 | `research` | Investigate a stack×topic×major against authoritative sources; persist immutable record + INDEX row. Sits beside think — think consumes INDEX at Step 5, or research runs standalone |
| prototype / 原型 / 试一下 / spike / 验证设计 / 看看效果 / 跑起来看看 / 状态机对不对 / 数据模型能表达吗 | `have-a-try` | Build a throwaway prototype to answer one design question (LOGIC terminal app or UI variants). Optional branch between `/think` and `/grill` — write disposable code, capture the verdict, delete the shell |
| 挑战方案 / grill / 细化方案 / 深挖计划 / 术语审查 | `grill` | Challenge plan against domain model, sharpen terminology, update CONTEXT.md, ADRs, issue |
| 分解 / story / 拆分 / Issues / 任务 / 子任务 | `story` | Break plan into executable Issues (accepts PRD or direct description), update PRD child issues, sync issue tracker |
| TDD / 测试优先 / 实现已确认行为 / red-green-refactor | `tdd` | Test-driven development, red-green-refactor loop, one vertical slice at a time |

### Completion & Finish (Post-build)

| Trigger | Skill | Description |
|---------|-------|-------------|
| 代码审查 / review / check / 把关 / 发布前 / 完成 / 验收 | `review` | Code review, verification, documentation sync, issue sync/release follow-through when explicitly authorized |

### Bug Fix (Diagnostic)

| Trigger | Skill | Description |
|---------|-------|-------------|
| 调试 / debug / 排查 / 报错 / 崩溃 / 不工作 / 回归 / 以前是好的 / 测试失败 | `debug` | Root cause analysis and systematic fix, quick locate then 6-phase loop |

### Architecture Improvement (Maintenance)

| Trigger | Skill | Description |
|---------|-------|-------------|
| 架构 / improve-architecture / 重构候选 / 清理 / 债务 / 架构审查 | `improve-architecture` | Periodic architecture review, scan PRDs for alignment, find design debt and deepening opportunities |

### Writing & Editing (Cross-phase)

| Trigger | Skill | Description |
|---------|-------|-------------|
| 润色 / 改稿 / 去AI味 / rewrite / polish / proofread / 帮我写 | `write` | Rewrite prose, remove AI tone, preserve author voice |
| 审稿 / review document / check this document / 本地化文案 | `write` | Document review with privacy scan, tone check, bilingual validation |
| release notes / changelog / 发版 / tweet / 推文 / 社交发文 | `write` | Generate release notes from commits, draft social posts |

## Common Sequences

Skills don't auto-chain by default. Each skill stops and waits for user's next step.

**Project setup (first time):**
```
/setup-project → skills configured → /think (start feature work)
```

**New feature complete workflow:**
```
/think → user approves → /grill → /story → /tdd → /review → merge/release
```
`/think` Step 5 queries `docs/research/INDEX.md` first; on a hit it reuses the TL;DR, on a miss it may suggest `/research` to persist a durable record before committing to an approach.

**Technical investigation (standalone or embedded):**
```
/research <stack> <topic>-<major>   →  immutable record + INDEX row  →  /think (queries INDEX) or /grill (records ADR citing the research)
```
`/research` runs standalone to build the knowledge base, OR is effectively triggered inside `/think` Step 5 when a technical choice needs grounding. Records are immutable (ADR-0004); a new major creates a new file, never edits the old.

**New feature with a design doubt worth prototyping:**
```
/think → /have-a-try (when a design question is cheaper to run than reason about) → /grill → /story → /tdd → /review
```
`/have-a-try` is an optional branch, not a required step. Use it only when the question is concrete enough to resolve by running code (state machine edges, data-model cases, what a page should look like). It writes disposable code; the validated verdict flows into the PRD/ADR, then the prototype shell is deleted or absorbed.

**Bug fix workflow:**
```
/debug → root cause known → fix/regression test → /review (optional)
```

**Test-first implementation workflow:**
```
/tdd → /review
```

**Direct breakdown (user has a clear plan):**
```
/story → /tdd → /review → merge/release
```

**Periodic maintenance:**
```
/improve-architecture → review report → /grill (if terminology/ADR decisions) → /story (if approved improvements) → /tdd (optional)
```

**Note on sub-agent orchestration:** `/tdd` now internally runs Acceptance Criterion Cycles — a 5-step loop per criterion (Test Sub-Agent designs scenarios → Scenario Review Gate → Test Sub-Agent writes tests (RED) → Code Review Gate → Develop Sub-Agent implements (GREEN)), followed by a unified Refactor phase after all cycles. `/review` now internally dispatches three parallel sub-agents (Test Review, Code Review, Impact Review), each independently re-reading all shared context, then merges their reports for human adjudication.

## Disambiguation

**Bug/test failure conflict (`debug` vs `tdd`):**
- Root cause unknown, failing test unexplained, regression, crash, or anomaly → `/debug`.
- Root cause known and user wants test-first implementation of accepted behavior → `/tdd`.
- During `/debug`, Phase 5 may use TDD discipline locally; do not switch the main skill unless user asks.
- Note: `/tdd` now uses sub-agent orchestration (Test Sub-Agent → Human Review Gates → Develop Sub-Agent per acceptance criterion). If the user only wants a quick fix without the full cycle structure, `/debug` is more appropriate.

**"验证一下 / try it" conflict (`have-a-try` vs `think` vs `tdd`):**
- Vague idea, multiple paths, not sure *what* to build → `/think` (pure conversation, no code, produces a PRD).
- Concrete design question that's cheaper to resolve by *running* code than reasoning on paper (state machine edge, data-model case, what a page looks like) → `/have-a-try` (disposable prototype; LOGIC terminal app or UI variants).
- Accepted behavior with known requirements, want a proper test-first implementation → `/tdd` (red-green-refactor with human review gates — the opposite of "skip the polish").
- Rule of thumb: `/think` doesn't write code; `/have-a-try` writes disposable code; `/tdd` writes production code with tests. If the user says "试一下" but the design isn't clear yet, suggest `/think` first.

**“审查” conflict (`grill` vs `review`):**
- PRD, plan, approach, terminology, domain model, ADR, “方案是否合理” → `/grill`.
- Diff, changed files, staged work, completed task, verification, merge/release readiness → `/review`.
- Note: `/review` now runs three parallel perspectives (Test Review, Code Review, Impact Review). It covers implementation quality and change impact, not plan design.

**Impact Review vs improve-architecture:**
- Local change impact, regression risk for current diff, compatibility and release strategy → `/review` (Impact Review sub-agent).
- Global architecture health, design debt scan, periodic code health check → `/improve-architecture`.

**“调研 / research” conflict (`research` vs `think` vs `have-a-try`):**
- Vague idea, multiple paths, not sure *what* to build → `/think` (converge to a PRD; it queries INDEX at Step 5 but doesn't itself persist research).
- Concrete technical question against a specific stack+version, want to capture the best practice durably for reuse → `/research` (authoritative-source investigation → immutable record + INDEX).
- Design doubt cheaper to resolve by *running* code than reasoning (state machine edge, what a page looks like) → `/have-a-try` (disposable prototype).
- Rule of thumb: `/think` decides *what* to build (no durable technical record); `/research` decides *how* a specific tech behaves (durable, sourced record); `/have-a-try` validates a design guess (disposable code). `/think` Step 5 internally consumes `/research` output via INDEX — you don't have to run `/research` manually first.

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

| Skill | Format Files | Core Role | Updates |
|-------|-------------|-----------|---------|
| `setup-project` | — | Scaffold or update per-repo skill configuration (idempotent — safe to re-run) | `docs/agents/*.md` + AGENTS.md block |
| `think` | PRD-FORMAT.md | Diverge → converge to initial PRD | PRD + parent issue (required, Step 9a) |
| `research` | RESEARCH-FORMAT.md<br>INDEX-FORMAT.md | Investigate stack×topic×major against authoritative sources → immutable record + INDEX | `docs/research/<stack>-<topic>-<major>.md` + INDEX.md row (lazy-created) |
| `have-a-try` | — | Build a throwaway prototype to answer one design question (LOGIC terminal app or UI variants) | Validated verdict (PRD `Prototyped by` / ADR / commit / NOTES.md); prototype deleted or core absorbed |
| `grill` | CONTEXT-FORMAT.md<br>ADR-FORMAT.md | Challenge plan + update domain knowledge | PRD + CONTEXT.md + ADRs + parent issue synced (if created by /think) |
| `story` | STORY-FORMAT.md | Vertical slices to Issues (accepts PRD or direct description) | PRD (created or updated) + Child Issues + issues if confirmed |
| `tdd` | — | Sub-agent orchestration: Test Sub-Agent → Human Review Gates → Develop Sub-Agent | Code + tests (via Acceptance Criterion Cycles) |
| `review` | — | Parallel three-perspective review: Test Review ∥ Code Review ∥ Impact Review | Merged report + local docs + remote updates only when explicitly authorized |
| `debug` | — | Root cause → 6-phase fix | Root cause report + code fix |
| `improve-architecture` | — | Periodic architecture review | Architecture report |
| `write` | — | Prose editing: rewrite, de-AI, review, release notes, localization | Edited prose only (no change list) |

> **Format Files column**: "—" means the skill's output format is embedded in REFERENCE.md rather than in a separate *-FORMAT.md file. Skills with named format files (PRD-FORMAT.md, STORY-FORMAT.md, etc.) use them as bilingual templates shared with the user.

## Prerequisites Matrix

Each skill may depend on files or configuration produced by earlier skills. Missing prerequisites are handled gracefully — the skill either works without them (with reduced precision) or suggests running a prerequisite skill first.

| Skill | Config (always read first) | Required | Optional (enhances output if present) | Format Contract | Auto-created by |
|-------|---------------------------|----------|---------------------------------------|----------------|-----------------|
| `setup-project` | — | Git repo | — | — | — (this is the foundation) |
| `think` | — | — | `CONTEXT.md`, `docs/adr/`, existing PRDs, `docs/research/INDEX.md` | PRD-FORMAT.md | Creates PRD if user opts in |
| `research` | `domain.md` | A concrete stack×topic×major question | `CONTEXT.md`, `docs/adr/`, `docs/research/INDEX.md` (for dedup) | RESEARCH-FORMAT.md, INDEX-FORMAT.md | Creates `docs/research/` + INDEX lazily on first record |
| `have-a-try` | `domain.md` | A concrete design question | `CONTEXT.md`, `docs/adr/`, PRD | — | — |
| `grill` | `domain.md` | PRD (`docs/prd/PRD-NNNN-<title>.md`) | `CONTEXT.md`, `docs/adr/` | CONTEXT-FORMAT.md, ADR-FORMAT.md | Creates `CONTEXT.md` and ADRs lazily |
| `story` | `domain.md`, `repo-map.md`, `issue-tracker.md`, `triage-labels.md` | — | `CONTEXT.md`, PRD | STORY-FORMAT.md (Issue body), minimal PRD | Creates minimal PRD if none exists |
| `tdd` | `domain.md`, `repo-map.md` | — | `issue-tracker.md`, PRD, `CONTEXT.md`, ADRs | Issue body = STORY-FORMAT.md | — |
| `review` | `domain.md`, `repo-map.md` | Code changes (staged or unstaged) | PRD, `CONTEXT.md`, ADRs, CI configs | Issue body = STORY-FORMAT.md | Updates local docs when verified |
| `debug` | `domain.md`, `repo-map.md` | Reproducible error or symptom | `CONTEXT.md`, ADRs | — | — |
| `improve-architecture` | `domain.md`, `repo-map.md` | — | `CONTEXT.md`, `docs/adr/`, `docs/prd/*.md` | — | — |
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

Key anti-patterns for sub-agent skills:
- **#37 Skill-to-skill state drift** — re-read latest shared files when entering a skill
- **#38 Sub-agent state leakage** — each sub-agent independently re-reads all shared context from disk; no shared memory, no cached understanding

## Project Structure

> **Note:** In `tdd/` and `review/`, REFERENCE.md contains sub-agent instruction chapters describing each sub-agent's responsibilities, checklists, and independence constraints.

The canonical directory tree lives in `AGENTS.md` (Repository Structure section) so it drifts in one place, not across files. See there for the authoritative layout.
