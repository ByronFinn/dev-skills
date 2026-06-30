# Research Skill

> **Status**: Grilled | **PRD**: PRD-0001 | **Created**: 2026-06-30 | **Last updated**: 2026-06-30

## Goal

新增 `research` skill，补齐 dev-skills 生态缺失的「技术调研与最佳实践沉淀」环节。维护一个持续可检索的技术知识库 `docs/research/`，按**技术栈 × 主题**双维度组织，每条记录带 `stack@version` 版本感知与失效机制，通过 `INDEX.md` 索引供后续 skill（尤其 `/think` Step 5 的 research-first）直接查询复用，避免对同一技术问题反复搜索。所有研究**必须基于权威信源**（官方文档、源码、官方规范等），禁止依赖二手博客或非权威转述。同时接通 PRD-FORMAT.md 中现有的幽灵字段 `## Research References`——把无人兜底的格式契约变成真实能力。

## What I already know

* 现有 skill 生态的命名规范已成熟：PRD 用 `PRD-NNNN-<title>.md`（4位+前缀），ADR 用 `<NNNN>-<title>.md`（4位无前缀），CONTEXT.md 单文件位于 repo 根
* 目录创建遵循「setup-project 脚手架 `docs/agents/` 配置；其余 skill 惰性创建产物目录」的惯例
* PRD 状态流转是 5 态：`Draft→Grilled→Sliced→InProgress→Done`（+`Deprecated`），代码为唯一事实源
* **核心缺口**：PRD-FORMAT.md 第 110 行有 `## Research References` 字段指向 `docs/research/topic.md`，但全仓库没有任何 skill 创建或维护它——这是「幽灵字段」，格式层承诺了能力但没有 skill 兜底
* `think` skill 的 Step 5 已经写了「Research-first for technical choices」，但研究结果只在对话中消散或埋进单个 PRD 的 Technical Notes，无跨任务复用机制
* 现有最接近的同类是 `have-a-try`（一次性产出+丢弃过程）和 `grill`（持续维护 CONTEXT.md 知识库）；research 形态最接近 grill，但维护的是「技术最佳实践」而非「领域语言」
* 用户硬约束：**research 来源必须是权威信源**（官网、源码、官方规范等），二手博客/非权威转述不可作为决策依据

## Assumptions (temporary)

*All assumptions validated during /grill (2026-06-30). See Decision section for resolutions.*

## Open Questions

*无未决问题——think 阶段 8 项关键决策 + grill 阶段 12 项边界决策全部收敛（见 Decision 节与 Grill Resolved 节）*

## Requirements

* **R1 独立可调用**：`/research <topic>` 作为独立 skill 可运行，产出一条 `docs/research/<stack>-<topic>-<major>.md` 研究记录（major 版本必入文件名）
* **R2 think 内嵌查询**：`/think` Step 5 research-first 前先查 `INDEX.md`；命中则默认读 TL;DR 复用，**例外读全文**：①INDEX 行 Status=`stale`，或 ②think 决策直接依赖该研究的实现细节；未命中才启动新研究或标注缺口
* **R3 双维度组织**：INDEX.md 同时提供「按技术栈分组」（By Stack 表）与「按主题交叉」（By Topic 表）两个视图；By Topic 表中**单 stack 主题也保留**（≥1 即列，0 即不出现）
* **R4 权威信源强制**：每条记录必须有 `## Sources` 字段，**每条 verdict 至少需 1 个 Tier 1 源作主证**；仅收录权威来源，二手博客/教程/非权威转述完全排除（不仅"不作为依据"，而是不收录）
* **R5 信源两级精确定义**：
  - **Tier 1（必收，维护者自产）**：官方文档、官方源码、官方规范/标准（ISO/W3C/ECMA-262 等）
  - **Tier 2（仅补充，不可单独支撑 verdict）**：官方 changelog、**仅 Accepted/Merged 的**官方 RFC/提案、官方仓库中 maintainer 标记的官方评论
  - **明确排除**：个人博客、教程站、非官方翻译、AI 生成内容、SO 答案（除非指向官方源）、**社区维护但非官方的站点**（cppreference 等）、**未采纳的 RFC 草案**、非 maintainer 评论
* **R6 版本感知失效（major 阈值）**：每条记录带 `stack@version`（全版本）字段；skill 读项目依赖清单比对，**仅 major 版本差异触发 stale**（18.2 vs 19.0 → stale；18.2 vs 18.3 → 不触发）；多版本共存时**逐 major 分记录**（17+18 并存 = 两份文件）；无依赖清单时 `stack@version=unknown`，跳过 stale 检测
* **R7 repo 级作用域**：仅维护 `docs/research/`，不引入全局/跨项目知识库；新 repo 从零积累（显式接受此代价）
* **R8 过程型深度**：每条记录包含 Question / Approach / Findings(对比矩阵) / Verdict+Rationale / Boundary Conditions / TL;DR 六块结构
* **R9 接通幽灵字段**：PRD-FORMAT.md 的 `## Research References` 字段获得明确填充规则——引用本 skill 产出的 `docs/research/*.md`；ADR 的 `## References` 也可引用 research（research 是被引用的证据层）
* **R10 惰性创建目录**：`docs/research/` 与 `INDEX.md` 在首次产出研究时创建，不预先脚手架（对齐 docs/prd/、docs/adr/ 惰性创建惯例）
* **R11 记录不可变（immutability）**：记录一旦写入即冻结，忠实记录该 major 时代的最佳实践；新 major 产生新文件（`-18.md` → `-19.md`），**绝不修改旧记录**；保留历史可追溯性（best-practice evolution across majors 可对比）。*决策见 ADR-0004*
* **R12 新建前去重**：新建记录前必查 INDEX（按 stack+topic+major 比对），命中则问用户续写（复用）还是新建——复用 anti-pattern #40 精神，不新增 anti-pattern
* **R13 stale 协作标记 + 提示式重验**：任何读 INDEX 的 skill（think/research/grill）发现版本不匹配时即时将该行 Status 设为 `stale`（纯枚举，不带数据）+ 将 Version 列改为 `研究版本 → 当前版本`（如 `react@18.2 → 19`）+ 提示 `→ suggest /research <stack> <topic>-<current-major>`；重验由用户显式触发，不自动
* **R14 research 与 ADR 共存引用**：research 记录通用事实（冻结），ADR 记录本项目决策并在 `## References` 引用 research；两者不复制、不互转

## Acceptance Criteria

* [ ] AC1 `skills/research/SKILL.md` 存在，含 YAML front matter（name/description/when_to_use/dispatch_intent）+ Outcome Contract + Process Summary + Gotchas + Output
* [ ] AC2 `skills/research/RESEARCH-FORMAT.md` 存在，含模板（含强制 `## Sources` 分级字段、`stack@version`、TL;DR、6 块结构）+ 命名规则 + 状态流转定义
* [ ] AC3 `skills/research/INDEX-FORMAT.md` 存在，含 By Stack + By Topic 双视图模板 + emoji 状态标记规则
* [ ] AC4 `skills/research/REFERENCE.md` 存在，含详细 process steps、信源分级标准、版本探测方法、权威信源识别 checklist
* [ ] AC5 `RESOLVER.md` 新增 research 路由行（work object + workflow phase 两处）+ think/research 冲突消解规则
* [ ] AC6 `rules/entry-protocol.md` Step 3 增读 `docs/research/INDEX.md` 作为可选上下文
* [ ] AC7 `think/SKILL.md` Step 5 增「先查 INDEX」前置步骤，命中时引用已有研究而非重新搜索
* [ ] AC8 `think/PRD-FORMAT.md` 的 `## Research References` 字段补充填充规则说明（引用 docs/research/*.md）
* [ ] AC9 `setup-project/SKILL.md` + `docs/agents/domain.md` 模板登记 `docs/research/` 路径
* [ ] AC10 `AGENTS.md` 的 Repository Structure + Documents Produced by Skills 两表新增 research 行
* [ ] AC11 RESEARCH-FORMAT.md 的 Sources 字段示例展示一级/二级信源区分，Gotchas 表含「引用了二手博客」反模式
* [ ] AC12 所有 research 产物的引用链接必须是可直接访问的权威 URL（官网/源码/GitHub 官方仓库）
* [ ] AC13 命名规则：文件名格式为 `<stack>-<topic>-<major>.md`，含 major 版本；slug 化规则（C++→cpp 等）写入 RESEARCH-FORMAT.md
* [ ] AC14 RESEARCH-FORMAT.md 明确记录不可变原则（immutability）：新 major 新建文件，不改旧记录；Gotchas 含「编辑旧记录而非新建」反模式
* [ ] AC15 REFERENCE.md 信源分级章节明确：Tier 2 仅含 Accepted/Merged 的 RFC；社区维护非官方站（cppreference 等）明确排除
* [ ] AC16 research SKILL.md process 含「新建前查 INDEX 去重」步骤（对齐 anti-pattern #40）
* [ ] AC17 INDEX-FORMAT.md 含固定 Status 字段（取值纯枚举 `verified | stale | deprecated`，不带数据）与 Version 列版本对比规则（stale 行显示 `研究版本 → 当前版本`，如 `react@18.2 → 19`；verified/deprecated 行显示单一研究版本）；**不使用 emoji**（对齐 PRD/ADR 纯文本 Status 惯例）
* [ ] AC18 think/SKILL.md Step 5 含「例外读全文」规则（stale 或依赖实现细节时）

## Definition of Done

* Tests added/updated：N/A（无应用代码，产物是 Markdown skill 文档）
* Lint / typecheck / CI green：N/A
* Docs/notes updated：本 PRD + 所有 AC 涉及的 skill 文件 + AGENTS.md + RESOLVER.md 全部更新
* Rollout/rollback considered：research 是新增 skill，回滚 = 删除 skills/research/ 目录 + 还原被改文件；低风险

## Out of Scope

* 跨项目/全局知识库（`~/.agents/research/` 等全局目录）——未来 PRD 再处理
* 编号系统（`RES-NNNN-<stack>-<topic>.md`）——slug 命名已够用，未来若不足再升级
* 自动跨 repo 拷贝/同步机制（setup-project 不支持从源 repo 拷贝 docs/research/）
* 自动重验：版本不匹配只标记 `stale` 并提示，不自动重新研究（避免无授权的网络请求）
* 结论型（太浅）或深度型（太重）的记录模板变体
* dev-skills 仓库自身的 docs/research/ 内容（元仓库不产生业务研究）

## Technical Approach

形态最接近 `grill`（持续维护一个知识文件），区别在维护对象：

| Skill | 维护对象 | 知识性质 |
|---|---|---|
| `grill` | CONTEXT.md | 领域语言（业务术语，项目内自洽） |
| `research` (新) | docs/research/ + INDEX.md | 技术最佳实践（栈+版本+主题，基于外部权威信源） |
| `have-a-try` | 一次性 verdict | 设计问题的临时验证（不持续维护） |

**关键设计**：research 与 ADR 的边界。
- ADR 记录**本项目难逆转的技术决策**（Context/Decision/Consequences）
- research 记录**通用技术最佳实践**（与本项目是否采用无关，是可复用的外部知识）
- 二者目录独立（`docs/adr/` vs `docs/research/`），命名风格对齐（均描述性文件名，research 用 slug 无编号）

**信源约束落地**（grill 精化后）：
- RESEARCH-FORMAT.md 强制 `## Sources` 字段，两级精确定义（见 R5）：
  - **Tier 1（必收，维护者自产）**：官方文档、官方源码、官方规范/标准
  - **Tier 2（仅补充，不可单独支撑 verdict）**：官方 changelog、**仅 Accepted/Merged 的**官方 RFC/提案、maintainer 标记的官方评论
  - **排除**：个人博客、教程站、非官方翻译、AI 生成内容、SO 答案、**社区维护非官方站（cppreference 等）**、**未采纳 RFC 草案**、非 maintainer 评论
- 核心判定：**每条 verdict 至少需 1 个 Tier 1 源作主证**
- Gotchas 表新增反模式：「把二手博客当决策依据」「信源无 URL 或指向首页」「社区站当官方」「Tier 2 单独支撑 verdict」
- REFERENCE.md 含「权威信源识别 checklist」

## Research References

*（本 PRD 自身即 research skill 的设计来源，按 R4 约束此处为设计依据而非外部技术调研）*
* 现有 dev-skills skill 体系：`skills/RESOLVER.md`、`skills/rules/entry-protocol.md`、`skills/think/SKILL.md`、`skills/have-a-try/SKILL.md`、`skills/grill/{CONTEXT,ADR}-FORMAT.md`
* 现有幽灵字段：`skills/think/PRD-FORMAT.md` 第 110 行 `## Research References`

## Feasible Approaches

**Approach A: 持续知识库 + INDEX 双维度 + 版本感知（Recommended）**

* How it works: research skill 维护 `docs/research/` 目录与 `INDEX.md`；每条记录 `<stack>-<topic>.md`，含 TL;DR + 6 块结构 + 强制权威 Sources + stack@version；think Step 5 先查 INDEX 命中则复用 TL;DR
* Pros: 满足「积累 + 直接查询」核心诉求；版本感知避免用过时结论；双维度索引覆盖两类查询；权威信源保证可信度
* Cons: repo 级意味着每 repo 从零积累（已显式接受）；INDEX 需手动维护（无自动同步）

**Approach B: 一次性研究纪要**

* How it works: 每次研究产出附在具体 PRD/ADR 上，不维护独立知识库；形态接近 have-a-try
* Pros: 最简单，无 INDEX 维护负担
* Cons: 无法跨任务复用——正是用户要解决的痛点；违背核心诉求

**Approach C: 全局知识库**

* How it works: 所有研究存 `~/.agents/research/`，跨 repo 共享
* Pros: 真正跨项目复用「积累的最佳实践」
* Cons: 破坏 dev-skills「每 repo 自包含」哲学；通用知识会被某项目特殊配置污染；用户已明确选「仅 repo 级」

## Decision (ADR-lite)

**Context**: dev-skills 生态缺少技术调研沉淀环节，PRD-FORMAT 的 Research References 是幽灵字段；用户希望积累技术最佳实践供后续直接查询。

**Decision**: 采用 Approach A——持续知识库 + INDEX 双维度 + 版本感知 + 强制权威信源。

**Consequences**:
- 正面：接通幽灵字段，补齐调研环节，版本感知防过时，权威信源保可信，形态对齐 grill 易理解
- 负面：repo 级意味着无法跨项目复用（已接受）；INDEX 需手动维护；每条研究需花时间甄别权威信源（信源约束的成本）
- 未来：若 slug 命名不足可升级编号系统；若跨项目诉求强烈可扩展全局层

## Grill Resolved (2026-06-30)

`/grill` 挑战并解决了 12 项开放边界。每项都更新了 CONTEXT.md 术语定义 + 本 PRD Requirements：

| # | 未决项 | 决议 |
|---|---|---|
| 1 | stack 定义边界 | **叶子技术单元**（单一库/框架/语言，独立版本号+官方源）；组合（Next.js）拆解为叶子单元，不建复合 slug |
| 2 | topic 粒度标准 | **一句话 verdict 标准**：需分支矩阵回答 = 太宽，必拆分 |
| 3 | stack slug 化 | **小写+连字符，去特殊字符和点**：C++→cpp、Node.js→nodejs、PostgreSQL→postgres、.NET→dotnet |
| 4 | 多版本共存 | **逐 major 分记录**（17+18 并存 = 两份文件） |
| 5 | stale 阈值 | **仅 major 差异触发**（18.2 vs 19.0→stale；18.2 vs 18.3→不触发）；记录作者可在 Boundary Conditions 声明"对 minor 敏感"作例外 |
| 6a | RFC/提案状态 | **仅 Accepted/Merged 的 RFC 算 Tier 2**；未采纳草案排除 |
| 6b | 社区认可站 | **排除**（cppreference、社区维护期 redux.js.org 等）；严格遵守"权威性来自维护者本身" |
| 7 | stale 回写责任 | **读者负责标记**：任何读 INDEX 的 skill 发现不匹配即标 stale+当前版本 |
| 8 | think 复用深度 | **TL;DR 优先 + 例外读全文**（stale 或决策依赖实现细节时） |
| 9 | research 与 ADR 边界 | **共存引用**：research 记录冻结的通用事实，ADR 记录项目决策并在 References 引用 research；不复制不互转 |
| 10 | 新建去重 | **必查 INDEX**（按 stack+topic+major），命中问用户续写/新建；复用 anti-pattern #40 |
| 11 | By Topic 空表 | **单 stack 也列**（≥1 即列，0 即不出现）；保留未来对比基准 |
| 12 | stale 提示机制 | **纯提示不自动**：标 Status=`stale`，Version 列改为 `研究版本 → 当前版本`，并附 `→ suggest /research ...`；重验由用户显式触发 |
| ★ | 记录不可变（用户补充） | **immutability 原则**：记录冻结，新 major 新建文件不改旧；保留历史可追溯。*升格为 ADR-0004* |
| 13 | intra-major 错误修正 | immutability 适用于跨 major；**同一 major 内发现错误**时，追加带日期和信源的 `## Correction` 块，不静默重写原文（见 ADR-0004 Negative） |

## Implementation Plan (small PRs)

* **PR1 — 骨架与格式契约**：新建 `skills/research/{SKILL.md, REFERENCE.md, RESEARCH-FORMAT.md, INDEX-FORMAT.md}`；确立命名规则、目录约定、状态流转、TL;DR 结构、权威信源分级与强制 Sources 字段（覆盖 AC1-4, AC11-12）
* **PR2 — 路由与集成**：更新 `RESOLVER.md`（research 路由 + think 冲突消解）；更新 `rules/entry-protocol.md`（Step 3 增读 INDEX）；更新 `think/SKILL.md`（Step 5 先查 INDEX）；更新 `think/PRD-FORMAT.md`（Research References 填充规则）（覆盖 AC5-8）
* **PR3 — 配置与文档同步**：更新 `setup-project`（domain.md 登记 docs/research/）；更新 `AGENTS.md`（两表增列）；考虑 `anti-patterns.md` 加 #41「研究重复劳动」（覆盖 AC9-10）

## Technical Notes

* 命名决策：用 `<stack>-<topic>.md` 无前缀无编号——研究主题天然有稳定 slug，编号对研究意义不大（不像 PRD 有创建顺序依赖）；与 ADR 的 `<NNNN>-<title>.md` 描述性文件名风格对齐
* 版本探测：skill 读 `package.json`/`go.mod`/`Cargo.toml`/`requirements.txt`/`pom.xml` 等依赖清单，比对 `stack@version` 字段；多版本共存时取主依赖
* 状态字段标识：固定纯文本 token `verified | stale | deprecated`，**不带数据、不使用 emoji**（对齐 PRD 的 `Status: Draft`、ADR 的 `Status: Accepted` 纯文本惯例）；版本信息一律归 Version 列，stale 行显示 `研究版本 → 当前版本`
* 信源约束的法律/伦理面：仅引用可公开访问的权威 URL，不抓取/缓存付费内容；AI 生成内容明确排除（避免自我引用循环）

## Traceability

- **Created by**: `/think` (2026-06-30)
- **Grilled by**: `/grill` (2026-06-30) — 13 项边界决策全部收敛，CONTEXT.md 7 个术语已收录，ADR-0004 创建
- **Sliced into**: *(待 /story)*
- **Implemented by**: *(待 /tdd)*
- **Reviewed by**: *(待 /review)*
- **New terms**: Research Record, Stack, Topic, INDEX, TL;DR, Authoritative Source — *已收录进 CONTEXT.md*
- **New decisions**: immutability 原则（ADR-0004）；其余 12 项边界决策记入 Grill Resolved 节

## Issue

No parent issue. dev-skills is a local-only skill meta-repo (no git remote, no `docs/agents/` config, no issue tracker). Per user decision, the PRD itself serves as the tracking artifact — consistent with the repo's existing convention (no `issues/` precedent). Step 9a parent-issue requirement explicitly waived for this repo.
