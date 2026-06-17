# PRD Format

## 用途

PRD 文件格式模板。由 `think` 或 `story`（无 PRD 时）生成和维护。

## 文件位置

`docs/prd/PRD-NNNN-<title>.md`

**命名规则**:

- **NNNN**：四位零填充序号（0000-9999）。由 `/think` 创建时自动分配：扫描 `docs/prd/` 下现有 `PRD-NNNN-*.md` 文件，取最大序号 +1。首次创建从 `0000` 开始。
- **title**：语义标题，使用 kebab-case（小写字母 + 连字符）。简明描述 PRD 主题，与 `# <Feature Name>` 标题对应。
- **语言**：跟随用户输入语言。不确定时询问用户。
- 示例：`PRD-0000-agent-runtime-evolution.md`、`PRD-0005-minio-storage-switch.md`

**为什么用编号**:
- 稳定短引用：Issue、commit、对话中 `PRD-0005` 比 `minio-storage-switch.md` 精确且不受改名影响
- 创建顺序可见：编号反映 PRD 创建的先后关系
- 状态追踪：结合 `## Status` 字段可快速建立实现全景表

## PRD 生命周期状态

PRD 在其生命周期内经历以下状态，每个状态的进入由可验证证据驱动：

```
Draft → Grilled → Sliced → InProgress → Done
  └─────────────────────────────────→ Deprecated
```

| 状态 | 进入条件 | 设置者 |
|------|---------|--------|
| **Draft** | PRD 文件创建，`Open Questions` 尚未全部解决 | `/think` |
| **Grilled** | 所有 Open Questions 已解决，Assumptions 已验证，Exhaustiveness Gate 通过 | `/grill` |
| **Sliced** | PRD 已拆分为 Issues，`Child Issues` 已填充 | `/story` |
| **InProgress** | 至少一个 Child Issue 开始实现 | `/tdd` 首次执行 |
| **Done** | 所有 Child Issues 关闭，所有 Acceptance Criteria 满足，代码已合并 | `/review` 或人工 |
| **Deprecated** | PRD 被放弃或替代（从任意前置状态可达） | 人工标记 |

**状态与代码的关系**: `Done` 判定**以代码为唯一事实源**——不依赖 Issue 关闭状态或口头确认，而是验证：
- 对应功能代码已合并到主分支
- 测试覆盖 Acceptance Criteria 并通过
- 无 `[TEMPORARY]` / `TODO(prd-NNNN)` 残留标记

**Status 字段格式**（放在 PRD 模板中 `# <Feature Name>` 之后的第一行）:

```markdown
> **Status**: Draft | **PRD**: PRD-NNNN | **Created**: YYYY-MM-DD | **Last updated**: YYYY-MM-DD
```

## 模板

```markdown
# <Feature Name>

> **Status**: Draft | **PRD**: PRD-NNNN | **Created**: YYYY-MM-DD | **Last updated**: YYYY-MM-DD

## Goal

<why + what in one paragraph>

## What I already know

* <facts from user message>
* <facts discovered from repo/docs>

## Assumptions (temporary)

* <assumptions to validate>

## Open Questions

* <ONLY Blocking / Preference questions; keep list short>

## Requirements

* <requirement 1>
* <requirement 2>

## Acceptance Criteria

* [ ] <testable criterion 1>
* [ ] <testable criterion 2>
* [ ] <testable criterion 3>

## Definition of Done

* Tests added/updated (unit/integration where appropriate)
* Lint / typecheck / CI green
* Docs/notes updated if behavior changes
* Rollout/rollback considered if risky

## Out of Scope

* <what we will not do in this task>

## Technical Approach

<key design + decisions>

## Research References

* [research topic](docs/research/topic.md) — <one-line takeaway>

## Feasible Approaches

**Approach A: <name>** (Recommended)

* How it works:
* Pros:
* Cons:

**Approach B: <name>**

* How it works:
* Pros:
* Cons:

## Decision (ADR-lite)

**Context**: Why this decision was needed
**Decision**: Which approach was chosen
**Consequences**: Trade-offs, risks, potential future improvements

## Implementation Plan (small PRs)

* PR1: <scaffolding + tests + minimal plumbing>
* PR2: <core behavior>
* PR3: <edge cases + docs + cleanup>

## Technical Notes

* <files inspected, constraints, links, references>
* <research notes summary if applicable>

## Traceability

- **Created by**: `/think` (or `/story` for minimal PRD)
- **Grilled by**: `/grill` (if run) — decision quality validated
- **Sliced into**:
  - #<issue-1> — [PRD-NNNN] <slice title> (AFK) — Done
  - #<issue-2> — [PRD-NNNN] <slice title> (HITL, blocked by #<issue-1>) — In Progress
  - #<issue-3> — [PRD-NNNN] <slice title> (AFK)
- **Implemented by**: `/tdd` (Issue reference)
- **Debugged by**: `/debug` (if bug fix touched this feature) — <bug summary + root cause>
- **Arch reviewed by**: `/improve-architecture` (if architecture review performed) — <finding summary>
- **Reviewed by**: `/review` (PR reference)
- **New terms**: <domain terms found during review, for CONTEXT.md>
- **New decisions**: <decisions made during implementation, for ADR>

## Issue

#<issue-number>（父 Issue，如有）
```

## 字段说明

| 字段 | 说明 |
|------|------|
| Status | PRD 生命周期状态（Draft / Grilled / Sliced / InProgress / Done / Deprecated） |
| PRD | PRD 编号（四位零填充，如 PRD-0000） |
| Goal | 一句话描述为什么和做什么 |
| What I already know | 已知事实（来自用户和代码库） |
| Assumptions | 需要验证的临时假设 |
| Open Questions | 仅阻塞/偏好问题 |
| Requirements | 功能需求列表 |
| Acceptance Criteria | 可测试的验收标准 |
| Definition of Done | 完成定义（团队质量标准） |
| Out of Scope | 明确不做的事情 |
| Technical Approach | 技术方案和关键决策 |
| Research References | 研究参考链接 |
| Feasible Approaches | 可行方法（2-3个选项）|
| Decision (ADR-lite) | 决策记录（轻量级ADR）|
| Implementation Plan | 实施计划（拆分成小PR）|
| Technical Notes | 技术笔记 |
| Traceability | 全链路追踪（各 skill 阶段自动填充）|
| Issue | 对应的 Issue 编号 |
| Child Issues | 子 Issues 列表（由 /story 自动填写，格式：`#<number> — <title> (type)`）|
