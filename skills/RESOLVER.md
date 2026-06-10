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
| Rough idea, unclear requirements, feasibility, design approach, “how should we build this?” | `think` | Convert ambiguity into a decision-complete PRD. |
| Existing PRD/plan/terminology/domain model/ADR questions, “challenge this plan”, “is this design sound?” | `grill` | Stress-test plan against domain language and decision records. |
| Completed PRD that needs tickets, issue breakdown, implementation tasks, vertical slices | `story` | Convert PRD requirements into executable Issues. |
| Accepted issue, known behavior to implement, explicit TDD/red-green-refactor request | `tdd` | Implement one vertical slice at a time through tests. |
| Error, crash, failing test, regression, anomalous behavior, “used to work” | `debug` | Unknown root cause must be diagnosed before fixing. |
| Diff, staged/unstaged changes, completed work, merge readiness, release readiness | `review` | Verify implementation, docs, artifacts, and release state with evidence. |
| Periodic health check, design debt scan, architecture review, proactive cleanup candidates | `improve-architecture` | Produce architecture improvement report and deepening opportunities. |

## Route by Workflow Phase

### New Feature Development (Pre-build)

| Trigger | Skill | Description |
|---------|-------|-------------|
| brainstorm / 构思 / 方案 / 出方案 / 深入分析 / 怎么设计 | `think` | Diverge on possibilities, converge to concrete plan, generate initial PRD and GitHub Issue |
| 挑战方案 / grill / 细化方案 / 深挖计划 / 术语审查 | `grill` | Challenge plan against domain model, sharpen terminology, update CONTEXT.md, ADRs, GitHub Issue |
| 分解 / story / 拆分 / Issues / 任务 / 子任务 | `story` | Break PRD into executable Issues (vertical slices), update PRD child issues, sync GitHub |
| TDD / 测试优先 / 实现已确认行为 / red-green-refactor | `tdd` | Test-driven development, red-green-refactor loop, one vertical slice at a time |

### Completion & Finish (Post-build)

| Trigger | Skill | Description |
|---------|-------|-------------|
| 代码审查 / review / check / 把关 / 发布前 / 完成 / 验收 | `review` | Code review, verification, documentation sync, GitHub/release follow-through when explicitly authorized |

### Bug Fix (Diagnostic)

| Trigger | Skill | Description |
|---------|-------|-------------|
| 调试 / debug / 排查 / 报错 / 崩溃 / 不工作 / 回归 / 以前是好的 / 测试失败 | `debug` | Root cause analysis and systematic fix, quick locate then 6-phase loop |

### Architecture Improvement (Maintenance)

| Trigger | Skill | Description |
|---------|-------|-------------|
| 架构 / improve-architecture / 重构候选 / 清理 / 债务 / 架构审查 | `improve-architecture` | Periodic architecture review, scan PRDs for alignment, find design debt and deepening opportunities |

## Common Sequences

Skills don't auto-chain by default. Each skill stops and waits for user's next step.

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

**Periodic maintenance:**
```
/improve-architecture → review report → /grill (if terminology/ADR decisions) → /story (if approved improvements) → /tdd (optional)
```

## Disambiguation

**Bug/test failure conflict (`debug` vs `tdd`):**
- Root cause unknown, failing test unexplained, regression, crash, or anomaly → `/debug`.
- Root cause known and user wants test-first implementation of accepted behavior → `/tdd`.
- During `/debug`, Phase 5 may use TDD discipline locally; do not switch the main skill unless user asks.

**“审查” conflict (`grill` vs `review`):**
- PRD, plan, approach, terminology, domain model, ADR, “方案是否合理” → `/grill`.
- Diff, changed files, staged work, completed task, verification, merge/release readiness → `/review`.

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
| `think` | PRD-FORMAT.md | Diverge → converge to initial PRD | PRD + GitHub Issue if explicitly confirmed |
| `grill` | CONTEXT-FORMAT.md<br>ADR-FORMAT.md | Challenge plan + update domain knowledge | PRD + CONTEXT.md + ADRs + GitHub Issue if confirmed |
| `story` | STORY-FORMAT.md | Vertical slices to Issues | PRD Child Issues + GitHub Issues if confirmed |
| `tdd` | — | Red-green-refactor loop | Code + tests |
| `review` | — | Code review + evidence + authorized finish work | Report + local docs + remote updates only when explicitly authorized |
| `debug` | — | Root cause → 6-phase fix | Root cause report + code fix |
| `improve-architecture` | — | Periodic architecture review | Architecture report |

## Shared Rules

Cross-skill behavioral constraints live in `rules/anti-patterns.md`. Skills should reference this file directly when applying global rules; it is a shared reference, not a standalone workflow skill.

## Project Structure

```
skills/
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
├── RESOLVER.md
└── rules/
    └── anti-patterns.md
```
