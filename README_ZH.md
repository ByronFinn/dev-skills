<!-- markdownlint-disable MD033 MD041 -->

<h1 align="center">🛠️ Engineering Skills</h1>

<p align="center">
  <em>软件工程工作流中可复用的 AI 代理技能——从构思到发布。</em>
</p>

<p align="center">
  <a href="https://skills.sh/ByronFinn/dev-skills"><img src="https://skills.sh/b/ByronFinn/dev-skills" alt="skills.sh"></a>
  <a href="LICENSE"><img src="https://img.shields.io/badge/License-MIT-yellow.svg" alt="License: MIT"></a>
  <a href="https://github.com/ByronFinn/dev-skills"><img src="https://img.shields.io/badge/GitHub-ByronFinn/dev--skills-181717?logo=github" alt="GitHub"></a>
</p>

<p align="center">
  <a href="README.md">🇬🇧 English</a>
</p>

---

**Engineering Skills**（发布名为 `ByronFinn/dev-skills`）是一套**基于 Markdown 的指令集**，专供 AI 编码代理（如通过 [skills.sh](https://skills.sh) 集成的 Claude Code）加载使用。  
不含应用代码、无需构建步骤、没有运行时——**技能文档本身就是产品**。

## 🤔 为什么存在

AI 编码代理功能强大但缺乏一致性：跳过规划、忘记领域上下文、混淆测试设计与实现、丢失决策轨迹。本项目通过**结构化的技能文档**强制执行工程纪律：

| 原则 | 命令 | 强制什么 |
|---|---|---|
| **先思后码** | `/think` | 充分构思再动手 |
| **先挑战再实现** | `/grill` | 用领域模型挑战方案 |
| **先测试再实现** | `/tdd` | 红-绿-重构，独立视角 |
| **先评审再合并** | `/review` | 并行三方评审 |
| **先定位根因再修复** | `/debug` | 系统化调试，可复现反馈闭环 |
| **先调研再承诺** | `/research` | 从权威信源捕获最佳实践并持久化 |

---

## 📋 目录

- [快速开始](#-快速开始)
- [技能总览](#-技能总览)
- [工作流程](#-工作流程)
- [路由](#-路由)
- [设计原则](#-设计原则)
- [核心概念](#-核心概念)
- [子代理架构](#-子代理架构)
- [项目结构](#-项目结构)
- [环境要求](#-环境要求)
- [贡献指南](#-贡献指南)
- [许可证](#-许可证)

---

## 🚀 快速开始

```bash
# 将全部技能安装到你的项目中（一次性）
npx skills@latest add ByronFinn/dev-skills

# 为你的仓库配置技能行为（一次性）
/setup-project

# 开始构建一个功能
/think
```

就是这么简单。每个技能通过**斜杠命令**触发，完成后自动停止——技能不会自动串联。由你来决定何时进入下一步。

---

## 🧰 技能总览

> **11 项技能**覆盖完整的工程生命周期：规划 → 调研 → 验证 → 分解 → 实现 → 评审 → 调试 → 维护 → 写作。

| 技能 | 命令 | 输入 → 输出 | 描述 |
|---|---|---|---|
| **setup-project** | `/setup-project` | 仓库状态 → `docs/agents/` 配置 | 一次性初始化：议题追踪器、分诊标签、领域文档布局、仓库映射。项目结构变化后可重新运行。 |
| **think** | `/think` | 模糊想法 → PRD (`docs/prd/`) | 发散构思 → 收敛为决策完备的方案。每次一个问题，附推荐答案。 |
| **research** | `/research` | 技术栈×主题问题 → 不可变记录 + INDEX | 基于权威信源（官方文档、源码、规范）调研。持久化为版本化、不可变的记录，可在会话间复用。 |
| **have-a-try** | `/have-a-try` | 设计问题 → 答案（原型→删除） | 构建一次性原型来回答一个设计问题。LOGIC 模式（终端应用）或 UI 模式（变体切换器）。完成后删除。 |
| **grill** | `/grill` | PRD → 验证后的 PRD + CONTEXT.md + ADRs | 以"对抗性视角"审读 PRD，提取每一个未决问题、假设和模糊术语，逐一解决至穷尽。 |
| **story** | `/story` | PRD 或描述 → 垂直切片 Issue | 将方案拆分为可独立执行的问题（贯穿所有层的 tracer bullet）。按依赖顺序发布。 |
| **tdd** | `/tdd` | Issue / PRD → GREEN 代码 + 测试 | 子代理编排的 TDD：测试子代理 → 人工审核门禁 → 开发子代理。每个验收标准一个周期。 |
| **review** | `/review` | Diff → 合并的三方评审报告 | 并行子代理：测试评审 ∥ 代码评审 ∥ 影响评审。合并报告并以矛盾高亮供人工裁决。 |
| **debug** | `/debug` | 报错/崩溃/回归 → 修复 + 回归测试 | 六阶段系统循环：复现 → 假设 → 埋点 → 修复 → 测试 → 清理。支持二分定位和范围扫描模式。 |
| **improve-architecture** | `/improve-architecture` | 代码库 + PRDs + ADRs → 报告 | 扫描设计债务、ADR 合规性和深化机会。按阻塞/高/中优先级划分并附范围估算。 |
| **write** | `/write` | 草稿 → 润色后文稿 | 去除 AI 腔调、润色、重写。支持中英文。发布说明、宣发/社交文案、本地化、文档审校。 |

---

## 🔄 工作流程

技能可组合成标准的工程工作流。每个技能**产出后即停止**——由你触发下一步。

### 新功能——完整流程

```
/setup-project → /think → /grill → /story → /tdd → /review → 🚀 merge/release
                        ↗                        ↗
              /research (INDEX 未命中)    /have-a-try (设计疑问)
```

### 常用流程

| 场景 | 流程 | 何时使用 |
|---|---|---|
| **新功能** | `/think` → `/grill` → `/story` → `/tdd` → `/review` | 从模糊想法到评审通过的完整流程 |
| **直接拆分** | `/story` → `/tdd` → `/review` | 已有明确方案，跳过构思环节 |
| **缺陷修复** | `/debug` → `/review` (可选) | 报错、崩溃、回归——先定位根因 |
| **技术调研** | `/research` → `/think` (消费 INDEX) | 持久化最佳实践知识供复用 |
| **架构健康检查** | `/improve-architecture` → `/grill` → `/story` → `/tdd` | 定期设计债务扫描 |

### 流程示意图

```
                    ┌─────────────────────────────────────────────────────┐
                    │                    新功能完整流程                     │
                    └─────────────────────────────────────────────────────┘

  ┌──────────┐    ┌──────────┐    ┌──────────┐    ┌──────────┐    ┌──────────┐
  │  /think  │───▶│ /research│───▶│ /grill   │───▶│ /story   │───▶│  /tdd    │
  │  构思    │    │  调研    │    │  挑战    │    │  拆分    │    │  实现    │
  │  idea→PRD│    │  rec→INDEX│   │  PRD→valid│   │  →Issues │   │  →GREEN  │
  └──────────┘    └──────────┘    └──────────┘    └──────────┘    └──────────┘
       │               ▲               │                              ▲
       │               │               │                              │
       │     ┌─────────┴─────────┐     │                              │
       │     │ /think Step 5     │     │                              │
       │     │ 查询研究索引      │     │                              │
       │     └───────────────────┘     │                              │
       │                               │                              │
       │     ┌───────────────────┐     │                              │
       └────▶│  /have-a-try      │     │                              │
             │  (设计疑问)        │◀────┘                              │
             └───────────────────┘                                    │
                                                                      │
               ┌──────────┐                                           │
               │ /debug   │◀──────────────────────────────────────────┘
               │ 调试     │
               └──────────┘

  ┌──────────┐    ┌──────────┐    ┌──────────┐
  │/setup-   │    │/review   │    │/improve- │
  │project   │    │          │    │architecture│
  │初始化配置│    │  评审    │    │ 架构改进  │
  └──────────┘    └──────────┘    └──────────┘

  ┌──────────┐
  │  /write  │
  │  写作    │
  └──────────┘
```

---

## 🧭 路由

按**工作对象**路由——你手头有什么决定了该用哪个技能：

| 你的情况 | 使用 |
|---|---|
| 🆕 新项目需要配置 | `/setup-project` |
| 💡 模糊想法、需求不明确 | `/think` |
| 🔬 技术实现方案的权威调研 | `/research` |
| 🧪 需要跑代码验证的设计疑问 | `/have-a-try` |
| 🔥 需要挑战方案 | `/grill` |
| 📋 需要将方案拆解为任务 | `/story` |
| ✅ 已确认的待实现需求 | `/tdd` |
| 🐛 报错、崩溃、回归问题 | `/debug` |
| 👀 已完成的工作 / diff 需要评审 | `/review` |
| 🏗️ 架构健康检查 / 设计债务 | `/improve-architecture` |
| ✍️ 写作润色 / 去 AI 腔 | `/write` |

> **完整消歧规则**详见 [`skills/RESOLVER.md`](skills/RESOLVER.md)，涵盖 Bug vs TDD、Grill vs Review、Think vs Research 等边界情况。

---

## 🎯 设计原则

### 🧩 独立可组合

每个技能**可独立运行**——不硬性依赖前置技能。缺失先决条件时优雅降级而非报错。当串联使用时，技能通过 **PRD 追踪链**读取先前产出：

```
Created by → (Prototyped by) → Grilled by → Sliced by → Implemented by → Reviewed by
                                                    ↑                    ↑
                                              Debugged by        Arch reviewed by
```

[入口协议](skills/rules/entry-protocol.md) 标准化了这个启动过程：定位领域文档 → 检查上游产物 → 无论是否存在都继续执行。

### 🧠 子代理编排

TDD 和 Review 技能使用**子代理模式**——每个子代理在行动前独立从磁盘重新读取所有共享上下文，**不共享内存或缓存理解**（[ADR 0001](docs/adr/0001-sub-agent-orchestration-pattern.md)）：

- **TDD**：测试子代理（设计场景 → 写测试）→ 人工审核门禁 → 开发子代理（实现 → 重构）
- **Review**：测试评审 ∥ 代码评审 ∥ 影响评审 → 合并报告，矛盾高亮

这是一个通过 Markdown 指令级隔离实现的**逻辑概念**——无需运行时调度器。

### 📊 证据优于断言

技能强制要求运行命令并粘贴输出。"应该能用"永远不是可接受的证据。每个结论必须引用验证命令或明确的运行时检查。

### 🎯 最小变更

只修复被要求的内容，不多做。修复一个模式实例后，grep 查找同类问题。范围蔓延会被标记，而非默默吸收。

### 🔒 不可变研究记录

研究记录是**不可变的**——一旦写入即被冻结，记录该主版本的最佳实践。新主版本发布时创建新记录；旧记录永不编辑（[ADR 0004](docs/adr/0004-research-record-immutability.md)）。

---

## 📖 核心概念

<details>
<summary><b>📄 PRD（产品需求文档）</b></summary>

**格式**：[`skills/think/PRD-FORMAT.md`](skills/think/PRD-FORMAT.md) · **位置**：`docs/prd/<feature>.md`

核心产物。由 `/think` 或 `/story` 创建，`/grill` 验证，`/tdd` 实现，`/review` 验证。包含目标、需求、验收标准、技术方案，以及追踪每个接触过它的技能的**追踪**部分。

</details>

<details>
<summary><b>📖 CONTEXT.md（领域术语表）</b></summary>

**格式**：[`skills/grill/CONTEXT-FORMAT.md`](skills/grill/CONTEXT-FORMAT.md) · **位置**：仓库根目录

项目的统一语言。纯术语定义——不含实现细节。由 `/grill` 创建和维护。消费技能使用其词汇进行命名、测试设计和文档编写。

</details>

<details>
<summary><b>📝 ADR（架构决策记录）</b></summary>

**格式**：[`skills/grill/ADR-FORMAT.md`](skills/grill/ADR-FORMAT.md) · **位置**：`docs/adr/<NNNN>-<title>.md`

记录难以逆转的、出人意料的、涉及真实权衡的决策。由 `/grill` 谨慎创建——仅在三个条件全部满足时。由 `/improve-architecture` 和 `/review` 检查合规性。

</details>

<details>
<summary><b>🚦 人工审核门禁</b></summary>

**格式**：Full / Fast / Batch 模式（[ADR 0003](docs/adr/0003-gate-modes-full-fast-batch.md)）· **位于**：`/tdd` 技能内部

在下一阶段开始前需要人工批准的阻塞性检查点。**Full** 模式（默认）有两个关口：**场景评审关口**（测试设计质量）→ **测试代码评审关口**（代码质量+保真度）。**Fast** 模式合并为一个关口。**Batch** 模式将 2-3 个同质标准分组。

</details>

<details>
<summary><b>🔬 研究记录</b></summary>

**格式**：[`skills/research/RESEARCH-FORMAT.md`](skills/research/RESEARCH-FORMAT.md) · **位置**：`docs/research/<stack>-<topic>-<major>.md`

持久化记录某个**技术栈 × 主题 × 主版本**组合的最佳实践。包含 **TL;DR** 总结、发现、边界条件和仅限于权威信源的 `## Sources` 章节。根据 ADR 0004 不可变。

</details>

<details>
<summary><b>📊 研究索引</b></summary>

**格式**：[`skills/research/INDEX-FORMAT.md`](skills/research/INDEX-FORMAT.md) · **位置**：`docs/research/INDEX.md`

知识库的可搜索入口。两种视图：**按技术栈**（按栈分组）和**按主题**（跨栈对比）。下游技能（特别是 `/think` 第 5 步）首先查询 INDEX；仅在未命中时才开展新的调研。

</details>

---

## 🏗️ 子代理架构

两个技能（TDD 和 Review）使用高级的**子代理编排模式**。每个子代理是独立的执行阶段，从磁盘重新读取所有共享上下文，彼此之间不共享内存或状态。

### TDD 流程

```
 ┌───────────── 验收标准周期（每个标准一个）─────────────────────────────┐
 │                                                                           │
 │  ┌──────────────┐     ┌──────────────┐     ┌──────────────┐              │
 │  │ 测试子代理    │────▶│ 场景评审门禁  │────▶│ 测试子代理    │              │
 │  │ (设计场景)    │     │ (人工审批)    │     │ (写测试代码   │──────┐       │
 │  │              │     │              │     │  RED)        │      │       │
 │  └──────────────┘     └──────────────┘     └──────────────┘      │       │
 │                                                                    │       │
 │  ┌──────────────┐     ┌──────────────┐                            │       │
 │  │ 开发子代理    │◀────│ 测试代码门禁  │◀───────────────────────────┘       │
 │  │ (实现: GREEN) │     │ (人工审批)    │                                    │
 │  └──────────────┘     └──────────────┘                                    │
 │                                                                           │
 └───────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
                       ┌──────────────────────┐
                       │  统一重构阶段          │
                       │  (全部周期完成)        │
                       └──────────────────────┘
```

**门禁模式**（[ADR 0003](docs/adr/0003-gate-modes-full-fast-batch.md)）：
- **Full**（默认）：每个标准 2 个门禁——场景 + 测试代码
- **Fast**：1 个门禁（场景内联到代码评审）
- **Batch**：每 2-3 个同质标准 1 个门禁

### 评审流程

```
                           ┌──────────────────────┐
                    ┌─────▶│  测试评审              │
                    │      │  子代理                │
                    │      │  (测试质量、边界覆盖)    │
                    │      └──────────────────────┘
                    │
 ┌──────────┐      │      ┌──────────────────────┐     ┌──────────┐
 │编排器     │─────┼─────▶│  代码评审              │────▶│  合并     │
 │(SKILL.md)│      │      │  子代理                │     │  报告     │
 │          │      │      │  (实现、安全、性能)      │     │  (矛盾    │
 │          │      │      │                       │     │  高亮)   │
 └──────────┘      │      └──────────────────────┘     └──────────┘
                    │
                    │      ┌──────────────────────┐
                    └─────▶│  影响评审              │
                           │  子代理                │
                           │  (回归风险、         │
                           │   发布策略、兼容性)    │
                           └──────────────────────┘
```

---

## 📁 项目结构

```
dev-skills/
├── AGENTS.md                      # 工作空间指令
├── README.md                      # 英文版
├── README_ZH.md                   # ← 你在此处
├── CHANGELOG.md                   # 版本历史
├── CONTEXT.md                     # 领域模型（自举示例）
├── LICENSE                        # MIT
│
├── docs/
│   ├── prd/                       # 本项目的 PRD
│   ├── adr/                       # 架构决策记录
│   └── agents/                    # 技能配置
│       ├── domain.md              # 领域文档路径
│       ├── issue-tracker.md       # 议题追踪器配置
│       ├── triage-labels.md       # 分诊标签词汇表
│       ├── language.md            # 文档语言配置
│       └── repo-map.md            # 多仓库结构
│
├── skills/                        # ← 全部技能在此
│   ├── RESOLVER.md                # 路由表与消歧
│   ├── rules/
│   │   ├── anti-patterns.md       # 跨技能行为约束
│   │   └── entry-protocol.md      # 共享启动序列
│   │
│   ├── setup-project/             # 初始化技能
│   ├── think/                     # 构思技能
│   ├── research/                  # 技术调研技能
│   ├── have-a-try/                # 原型验证技能
│   ├── grill/                     # 方案挑战技能
│   ├── story/                     # 任务拆分技能
│   ├── tdd/                       # TDD 实现技能
│   ├── review/                    # 代码评审技能
│   ├── debug/                     # 调试技能
│   ├── improve-architecture/      # 架构改进技能
│   └── write/                     # 写作润色技能
│       └── references/            # 语言特定模式
```

每个技能目录遵循一致的结构：

| 文件 | 用途 |
|---|---|
| `SKILL.md` | 入口——YAML 前置元数据、产出契约、流程摘要、注意事项、输出模板 |
| `REFERENCE.md` | 详细步骤、检查清单、示例、子代理章节 |
| `*-FORMAT.md` | 双语格式模板（如适用） |

---

## 🔧 环境要求

- 支持 [skills.sh](https://skills.sh) 技能加载的 AI 编码代理（如 Claude Code）
- Git 仓库（`review`、`debug` 等基于 diff 的技能需要）
- 可选：`gh` CLI（用于 `story` 和 `review` 中的 GitHub 议题追踪器集成）

---

## 🤝 贡献指南

详情请参阅 [AGENTS.md](AGENTS.md) 了解项目约定、文件结构规则和语言指南。

添加或修改技能时：

1. **遵循现有结构**：`SKILL.md`（入口）→ `REFERENCE.md`（详情）→ `*-FORMAT.md`（模板）
2. **保持 `SKILL.md` 简洁**；深度细节移至 `REFERENCE.md`
3. **更新路由**——添加或修改技能时更新 [`skills/RESOLVER.md`](skills/RESOLVER.md)
4. **遵守共享规则**——用 [`anti-patterns.md`](skills/rules/anti-patterns.md) 的规则检视自己的输出
5. **使用入口协议**——引用 [`rules/entry-protocol.md`](skills/rules/entry-protocol.md) 而非重复上下文读取指令。参见 [anti-pattern #36](skills/rules/anti-patterns.md#L42)
6. **更新 CHANGELOG**——在 [`CHANGELOG.md`](CHANGELOG.md) 中记录变更

本项目**自举使用**自身技能——所有文档（PRD、ADR、CONTEXT.md）按照项目[语言配置](docs/agents/language.md)使用简体中文书写。

---

## 📄 许可证

[MIT](LICENSE) © 2026 ByronFinn

---

<p align="center">
  <sub>用技能构建，由技能驱动。🤖</sub>
</p>
