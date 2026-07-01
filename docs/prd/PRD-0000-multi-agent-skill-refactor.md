# Multi-Agent Skill Refactor

> **Status**: In Progress | **PRD**: PRD-0000 | **Created**: 2026-06-12 | **Last updated**: 2026-06-24

## Goal

重构 TDD 和 Review skill，引入 sub-agent 编排模式：`/tdd` 和 `/review` 命令保持不变，但内部驱动独立的 sub-agent 执行，各自重新读取 PRD/Story 上下文，避免认知耦合。同时引入两阶段 Human Review Gate（场景设计审查 + 测试代码审查），以提升质量保障和问题发现能力。

## What I already know

* 当前 TDD skill 是单一 agent 执行 red-green-refactor 循环，测试编写和实现在同一个上下文中完成
* Review skill 已独立存在，但当前是单一视角的审查
* 用户核心诉求：Test 和 Develop 应各自独立为 sub-agent，共享 PRD/Story 但不共享内部状态
* 用户核心诉求：测试编写和边界情况的限定需要人类审查（两阶段 Human Review Gate）
* 用户核心诉求：Review 也应使用独立 sub-agent（test-review / code-review / impact-review 并行）
* dev-skills 是 Markdown 指令集，"独立 sub-agent" 通过在 skill 文件中描述独立的 sub-agent 指令段来实现

## Assumptions (resolved)

* ~~"独立 sub-agent" 在 dev-skills 语境中 = 独立的 SKILL.md + REFERENCE.md~~ → Sub-agent 指令嵌入在各 skill 的 REFERENCE.md 中作为独立章节，不新建顶层目录
* 人类审查关卡是同步阻塞点 — 两阶段阻塞：场景审查 + 代码审查
* 每个 Issue（来自 /story）的每个验收标准是一个独立的 Acceptance Criterion Cycle
* Refactor 阶段归 Develop Sub-Agent，在所有 cycle 完成后统一执行
* 理解分歧是特性而非缺陷 — 通过回退策略（停止 + 人类决策）自然处理

## Open Questions

* Debug skill 的 Phase 5（Fix + regression test）是否也需要类似的 agent 拆分？（推迟到下一迭代）

## Requirements

### TDD Skill 重构（sub-agent 编排）

* `/tdd` 命令保持不变，SKILL.md 描述整体编排流程（orchestrator）
* 每个 Issue 的每个验收标准执行一个 **Acceptance Criterion Cycle**：
  1. **Test Sub-Agent（场景设计阶段）**：独立读取 PRD/Story/Issue/CONTEXT.md/ADRs，设计测试场景表（场景、输入、预期输出、边界条件）
  2. **Scenario Review Gate**：人类审查场景设计的完备性、边界覆盖、合理性
  3. **Test Sub-Agent（测试代码阶段）**：根据批准的场景编写测试代码（RED）
  4. **Test Code Review Gate**：人类审查测试代码质量、命名、场景忠实度、public interface 使用
  5. **Develop Sub-Agent**：独立重新读取 PRD/Story/Issue + 审查通过的测试，实现代码使测试 GREEN
* 所有 cycle 完成后，Develop Sub-Agent 执行统一 **Refactor** 阶段（提取重复、深化模块、应用 SOLID）
* Develop Sub-Agent 发现测试设计问题时：停止工作，报告具体问题，由人类决定是否回退，不自行修改测试
* 每个 sub-agent 的指令作为 REFERENCE.md 中的独立章节

### Review Skill 重构（sub-agent 并行）

* `/review` 命令保持不变，SKILL.md 描述并行编排流程
* **Test Review Sub-Agent**：审查测试质量、边界覆盖度、测试设计合理性
* **Code Review Sub-Agent**：审查实现质量、安全、性能、代码规范
* **Impact Review Sub-Agent**：全链路影响分析 — 变更影响范围、回归风险、兼容性、架构健康（局部视角）、技术债务、发布策略（feature flag、灰度、回滚方案）
* 三个 sub-agent 并行执行，结果拼接为综合报告，矛盾项标注由人类裁决
* 每个 sub-agent 独立重新读取上下文，不共享内部状态
* Issue sync / release follow-through 归 Orchestrator 执行（需当前 turn 人类授权）

### 共通约束

* 每个 sub-agent 必须独立重新读取所有共享上下文（PRD、Story、Issue、CONTEXT.md、ADRs）
* 禁止 sub-agent 之间共享内部状态或缓存理解
* 更新 RESOLVER.md 反映新的内部结构
* 更新 AGENTS.md 反映目录结构
* 新增 anti-pattern #38：sub-agent 独立性约束

### 边界明确

* Impact Review Sub-Agent vs improve-architecture skill：
  - Impact Review = **本次变更**对架构的影响（局部、每次 review）
  - improve-architecture = **整个系统**的架构健康检查（全局、定期）
  - Impact Review 中引导：如需全局架构检查，运行 `/improve-architecture`

## Acceptance Criteria

* [ ] TDD SKILL.md 包含 sub-agent 编排流程描述（orchestrator）
* [ ] TDD REFERENCE.md 包含 Test Sub-Agent（场景设计 + 测试代码）和 Develop Sub-Agent 的独立指令章节
* [ ] 两阶段 Human Review Gate 在 TDD 流程中有明确的位置、交互模板和审查清单
* [ ] Acceptance Criterion Cycle 流程（5 步循环）在 REFERENCE.md 中有完整描述
* [ ] Review SKILL.md 包含并行 sub-agent 编排流程描述
* [ ] Review REFERENCE.md 包含 Test/Code/Impact Review Sub-Agent 的独立指令章节
* [ ] 三个 Review Sub-Agent 各自有独立的审查清单、输出模板和独立性约束
* [ ] Review 报告合并逻辑（拼接 + 矛盾标注）在 REFERENCE.md 中描述
* [ ] RESOLVER.md 已更新（skill 路由、工作流、歧义消解）
* [ ] AGENTS.md 项目结构已更新
* [ ] anti-patterns.md 新增 #38 sub-agent 独立性约束
* [ ] 原 TDD 核心原则（垂直切片、行为测试、public interface、Refactor）在新结构中保留

## Definition of Done

* 所有 skill 文件遵循现有结构约定（SKILL.md entry + REFERENCE.md detail）
* 语言约定保持一致（English primary, Chinese supplementary in format files）
* anti-patterns.md 规则编号连续（#38 新增）、格式一致
* 不引入新的 skill 间的循环依赖
* 目录结构不变（tdd/ 和 review/ 保持），内部文件重构

## Out of Scope

* runtime/编排层的自动化（dev-skills 只产出 Markdown 指令，不控制 agent 调度）
* grill / think / improve-architecture 的 agent 拆分（本次聚焦 TDD 和 Review）
* debug skill 的拆分（可后续考虑）
* 新增顶层 skill 目录

## Technical Approach

保持现有 tdd/ 和 review/ 目录结构不变，重构 SKILL.md 和 REFERENCE.md 内容：

```
skills/
├── tdd/
│   ├── SKILL.md          # 编排入口：描述 per-acceptance-criterion 的 5 步循环
│   └── REFERENCE.md      # 包含 Test Sub-Agent（场景设计+代码）和 Develop Sub-Agent 的独立指令章节
├── review/
│   ├── SKILL.md          # 编排入口：描述并行 Test/Code/Impact Review + 报告合并
│   └── REFERENCE.md      # 包含三个 Review Sub-Agent 的独立指令章节 + Orchestrator 合并逻辑
```

每个 sub-agent 指令章节包含：
- 上下文读取清单（必须独立重新读取的文件列表）
- 独立职责描述
- 检查清单
- 输出模板
- 独立性约束

## Technical Notes

* 当前 tdd/ 目录结构：SKILL.md (104行) + REFERENCE.md (189行)
* 当前 review/ 目录结构：SKILL.md (110行) + REFERENCE.md (203行)
* RESOLVER.md 188行，包含路由表、工作流、歧义消解
* anti-patterns.md 当前 37 条规则，新增 #38

## Decision (ADR-lite)

**Context**: TDD 和 Review skill 中单一 agent 混合多个职责，导致认知耦合和盲区
**Decision**: 保持 /tdd 和 /review 命令不变，内部引入 sub-agent 编排模式。每个验收标准执行 5 步循环（Test 场景设计→场景审查→Test 代码→代码审查→Develop 实现）。Review 三个 Sub-Agent 并行运行，报告拼接+矛盾标注。
**Consequences**: 用户无需学习新命令；两阶段 Human Review Gate 增加人类交互但提高测试质量；理解分歧作为 PRD 歧义的检测信号

## ADRs

* [0001 - Sub-Agent Orchestration Pattern](docs/adr/0001-sub-agent-orchestration-pattern.md)
* [0002 - Two-Stage Human Review Gate](docs/adr/0002-two-stage-human-review-gate.md) — Superseded by 0003 (Full mode 保留其决策)
* [0003 - Gate Modes (Full / Fast / Batch)](docs/adr/0003-gate-modes-full-fast-batch.md)

## Traceability

- **Created by**: `/think`
- **Grilled by**: `/grill` (2026-06-12) — sub-agent 编排模式、两阶段审查门、Acceptance Criterion Cycle 术语确定
- **Sliced by**: `/story` → Child Issues below
- **Implemented by**: `/tdd` + `/review` — TDD/Review skill 重构为 sub-agent 编排(#2-#5)
- **Arch reviewed by**: `/improve-architecture` (2026-06-17) — 发现 ADR 0002 被 Gate Modes 违反(B1,已由 ADR 0003 解决)、Traceability 链路断裂(H1)、CONTEXT.md 概念漂移(H2)；(2026-06-24) — 修复 ADR 0003 在 tdd/REFERENCE.md 的残留漂移、补齐 PRD-0000 命名前缀与状态行
- **Reviewed by**: `/review` (2026-06-17) — grill/think/tdd/review skill 优化落地

## Child Issues

* #1 — Add anti-pattern #38: sub-agent independence constraint (AFK)
* #2 — Refactor TDD SKILL.md as sub-agent orchestrator (HITL)
* #3 — Refactor Review SKILL.md as parallel sub-agent orchestrator (HITL)
* #4 — Write TDD REFERENCE.md sub-agent instruction chapters (HITL, blocked by #2)
* #5 — Write Review REFERENCE.md sub-agent instruction chapters (HITL, blocked by #3)
* #6 — Update RESOLVER.md for sub-agent skill structure (HITL, blocked by #2, #3)
* #7 — Update AGENTS.md project structure and workflow (HITL, blocked by #2, #3)
