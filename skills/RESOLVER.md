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

**Note on sub-agent orchestration:** `/tdd` now internally runs Acceptance Criterion Cycles — a 5-step loop per criterion (Test Sub-Agent designs scenarios → Scenario Review Gate → Test Sub-Agent writes tests (RED) → Test Code Review Gate → Develop Sub-Agent implements (GREEN)), followed by a unified Refactor phase after all cycles. `/review` now internally dispatches three parallel sub-agents (Test Review, Code Review, Impact Review), each independently re-reading all shared context, then merges their reports for human adjudication.

## Disambiguation

**Bug/test failure conflict (`debug` vs `tdd`):**
- Root cause unknown, failing test unexplained, regression, crash, or anomaly → `/debug`.
- Root cause known and user wants test-first implementation of accepted behavior → `/tdd`.
- During `/debug`, Phase 5 may use TDD discipline locally; do not switch the main skill unless user asks.
- Note: `/tdd` now uses sub-agent orchestration (Test Sub-Agent → Human Review Gates → Develop Sub-Agent per acceptance criterion). If the user only wants a quick fix without the full cycle structure, `/debug` is more appropriate.

**“审查” conflict (`grill` vs `review`):**
- PRD, plan, approach, terminology, domain model, ADR, “方案是否合理” → `/grill`.
- Diff, changed files, staged work, completed task, verification, merge/release readiness → `/review`.
- Note: `/review` now runs three parallel perspectives (Test Review, Code Review, Impact Review). It covers implementation quality and change impact, not plan design.

**Impact Review vs improve-architecture:**
- Local change impact, regression risk for current diff, compatibility and release strategy → `/review` (Impact Review sub-agent).
- Global architecture health, design debt scan, periodic code health check → `/improve-architecture`.

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
| `think` | — | — | `CONTEXT.md`, `docs/adr/`, existing PRDs | PRD-FORMAT.md | Creates PRD if user opts in |
| `grill` | `domain.md` | PRD (`docs/prd/PRD-NNNN-<title>.md`) | `CONTEXT.md`, `docs/adr/` | CONTEXT-FORMAT.md, ADR-FORMAT.md | Creates `CONTEXT.md` and ADRs lazily |
| `story` | `domain.md`, `repo-map.md`, `issue-tracker.md`, `triage-labels.md` | — | `CONTEXT.md`, PRD | STORY-FORMAT.md (Issue body), minimal PRD | Creates minimal PRD if none exists |
| `tdd` | `domain.md`, `repo-map.md` | — | `issue-tracker.md`, PRD, `CONTEXT.md`, ADRs | Issue body = STORY-FORMAT.md | — |
| `review` | `domain.md`, `repo-map.md` | Code changes (staged or unstaged) | PRD, `CONTEXT.md`, ADRs, CI configs | Issue body = STORY-FORMAT.md | Updates local docs when verified |
| `debug` | `domain.md`, `repo-map.md` | Reproducible error or symptom | `CONTEXT.md`, ADRs | — | — |
| `improve-architecture` | `domain.md`, `repo-map.md` | — | `CONTEXT.md`, `docs/adr/`, `docs/prd/*.md` | — | — |
| `write` | `domain.md` | Text to edit | Project style references, existing releases, `CONTEXT.md` | — | — |

**Config column**: Files under `docs/agents/`. `domain.md` tells consumer skills where domain docs live. `repo-map.md` tells them about multi-repo structure. Both are optional — skills fall back to default paths if missing.

**Format Contract column**: The output format expected by downstream skills. "Issue body = STORY-FORMAT.md" means issues created by the skill use the Story Format body.

**Config maintenance:** `/setup-project` creates `docs/agents/` configuration that consumer skills read. When project structure changes (repos added/removed, issue tracker switched, domain docs reorganized), re-run `/setup-project` — it reads existing config, detects drift, and updates only what changed. Consumer skills may suggest running `/setup-project` if they detect missing or stale config.

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

> **Note:** In `tdd/` and `review/`, REFERENCE.md now contains sub-agent instruction chapters describing each sub-agent’s responsibilities, checklists, and independence constraints.

```
skills/
├── setup-project/
│   ├── SKILL.md
│   └── REFERENCE.md
├── think/
│   ├── SKILL.md
│   ├── REFERENCE.md
│   └── PRD-FORMAT.md
├── grill/
│   ├── SKILL.md
│   ├── REFERENCE.md
│   ├── CONTEXT-FORMAT.md
│   └── ADR-FORMAT.md
├── story/
│   ├── SKILL.md
│   ├── REFERENCE.md
│   └── STORY-FORMAT.md
├── tdd/
│   ├── SKILL.md
│   └── REFERENCE.md
├── review/
│   ├── SKILL.md
│   └── REFERENCE.md
├── debug/
│   ├── SKILL.md
│   └── REFERENCE.md
├── improve-architecture/
│   ├── SKILL.md
│   └── REFERENCE.md
├── write/
│   ├── SKILL.md
│   ├── REFERENCE.md
│   └── references/
│       ├── write-en.md
│       ├── write-zh.md
│       ├── write-zh-prose.md
│       ├── write-zh-bilingual.md
│       ├── write-zh-release-notes.md
│       └── write-product-localization.md
├── RESOLVER.md
├── rules/
│   ├── anti-patterns.md
│   └── entry-protocol.md
```
