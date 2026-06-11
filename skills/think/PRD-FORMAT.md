# PRD Format

## 用途

这是 `think` skill 生成的 PRD 文件格式模板。

## 文件位置

`docs/prd/<feature-name>.md`

## 模板

```markdown
# <Feature Name>

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

## Issue

#<issue-number>

## Child Issues

* (待 story 填充)
```

## 字段说明

| 字段 | 说明 |
|------|------|
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
| Issue | 对应的 Issue 编号 |
| Child Issues | 子 Issues 列表（由 story 填充）|
