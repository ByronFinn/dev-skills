# Skills Resolver

Skill routing table. Claude Code auto-matches via each SKILL.md's `description`. This doc is a human-readable central index.

## Route by Workflow Phase

### New Feature Development (Pre-build)

| Trigger | Skill | Description |
|---------|-------|-------------|
| brainstorm / 构思 / 方案 / 出方案 / 深入分析 / 怎么设计 | `think` | Diverge on possibilities, converge to concrete plan, generate initial PRD and GitHub Issue |
| 挑战 / grill / 细化 / 审查 / 深挖 | `grill` | Challenge plan against domain model, sharpen terminology, update CONTEXT.md, ADRs, GitHub Issue |
| 分解 / story / 拆分 / Issues / 任务 / 子任务 | `story` | Break PRD into executable Issues (vertical slices), update PRD child issues, sync GitHub |
| TDD / 测试 / 实现 / red-green-refactor | `tdd` | Test-driven development, red-green-refactor loop, one vertical slice at a time |

### Completion & Finish (Post-build)

| Trigger | Skill | Description |
|---------|-------|-------------|
| 审查 / review / check / 把关 / 发布前 / 完成 | `review` | Code review, update local files (PRD/docs), sync remote (Issues/releases), release follow-through |

### Bug Fix (Diagnostic)

| Trigger | Skill | Description |
|---------|-------|-------------|
| 调试 / debug / 排查 / 报错 / 崩溃 / 不工作 / 回归 / 以前是好的 | `debug` | Root cause analysis and systematic fix, quick locate then 6-phase loop |

### Architecture Improvement (Maintenance)

| Trigger | Skill | Description |
|---------|-------|-------------|
| 架构 / improve-architecture / 重构 / 清理 / 债务 / 架构审查 | `improve-architecture` | Periodic (every 2-4 weeks) architecture review, scan PRDs for alignment, find design debt and deepening opportunities |

## Common Sequences

Skills don't auto-chain by default. Each skill stops and waits for user's next step.

**New feature complete workflow:**
```
/think → user approves → /grill → /story → /tdd → /review → merge/release
```

**Bug fix workflow:**
```
/debug → fix → /review (optional)
```

**Periodic maintenance:**
```
/improve-architecture → review report → /story (if improvements) → /tdd (optional)
```

## Disambiguation

When multiple skills could match:

1. **Most specific first** — more specific skill wins
2. **Phase order** — Pre-build → Post-build → Diagnostic → Maintenance
3. **User intent** — judge by explicit user intent

**Special cases:**
- "判断一下" + error/anomaly → `/debug` (diagnose problem)
- "判断一下" + is it worth it → `/think` evaluation mode (value judgment)
- 继续优化 + error → `/debug`
- 继续优化 + no error → `/improve-architecture`

## Skill Inventory

| Skill | Format Files | Triggers (EN/CN) | Core Role | Updates |
|-------|-------------|------------------|-----------|---------|
| `think` | PRD-FORMAT.md | brainstorm/构思/方案 | Diverge → converge to initial PRD | PRD + GitHub Issue |
| `grill` | CONTEXT-FORMAT.md<br>ADR-FORMAT.md | 挑战/grill/细化/审查 | Challenge plan + update domain knowledge | PRD + CONTEXT.md + ADRs + GitHub Issue |
| `story` | STORY-FORMAT.md | 分解/story/拆分/Issues | Vertical slices to Issues | PRD Child Issues + GitHub Issues |
| `tdd` | - | TDD/测试/实现 | Red-green-refactor loop | Code + tests |
| `review` | - | 审查/review/check/把关 | Code review + doc sync + release | PRD + docs + GitHub Issues + Release |
| `debug` | - | 调试/debug/排查/修复 | Root cause → 6-phase fix | Root cause report + code fix |
| `improve-architecture` | - | 架构/improve-architecture/重构 | Periodic architecture review | Architecture report |

## Project Structure

```
skills/
├── think/
│   ├── SKILL.md
│   └── PRD-FORMAT.md
├── grill/
│   ├── SKILL.md
│   ├── CONTEXT-FORMAT.md
│   └── ADR-FORMAT.md
├── story/
│   ├── SKILL.md
│   └── STORY-FORMAT.md
├── tdd/
│   └── SKILL.md
├── review/
│   └── SKILL.md
├── debug/
│   └── SKILL.md
├── improve-architecture/
│   └── SKILL.md
├── RESOLVER.md
└── rules/
    └── anti-patterns.md
```
