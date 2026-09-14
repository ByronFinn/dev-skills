# ponytail 技能集迁移分析报告与方案

> 对象：`/Users/baifan/Projects/ByronFinn/ponytail/skills`（6 个） → 迁移融合进本仓库 `dev-skills/skills/`
> 本文档为**分析与迁移方案**，未改动任何技能文件。落地需逐项逐批批准。

---

## 一、被迁移对象全景

`ponytail/skills/` 下有 6 个 SKILL.md（无 REFERENCE、无 FORMAT 文件，均为单文件技能）。按行为类型分三类：

### A. 常驻模式（persistent mode）——非按需技能

| 技能 | 本质 | 核心内容 |
|---|---|---|
| `ponytail` | **持续激活的"懒惰资深工程师"模式** | YAGNI 阶梯、强度分级（lite/full/ultra）、延迟简化的 `ponytail:` 注释约定、根因优先修复、输出格式（代码先行 ≤3 行）、"什么时候不该懒"豁免清单。Debounced到 `off` 前一直生效。 |

### B. 一次性命令类（one-shot）——按需触发、纯报告不改动

| 技能 | 输入 | 输出 |
|---|---|---|
| `ponytail-review` | diff / 改动 | 按行给过度工程发现：`L<行>: <tag> <cut>, <replacement>.`，tags = delete / stdlib / native / yagni / shrink，结尾 `net: -<N> lines possible.` |
| `ponytail-audit` | 整个代码库 | 同 tags，仓库级扫描，排序（最大削减在前），结尾 `net: -<N> lines, -<M> deps possible.` |
| `ponytail-debt` | 全库 `ponytail:` 注释 | 汇聚为债务台账，标识 `no-trigger` 腐化风险行 |
| `ponytail-gain` | 基准数据 | 固定 ASCII 记分板（5 任务 3 模型的中位数），诚实边界：绝不报"此仓省 N 行" |
| `ponytail-help` | 命令卡片 | 全部模式/技能的速查卡 |

### C. 关键机制（贯穿 A 和 B）

- **阶梯（the ladder）**：① 需要存在吗(YAGNI) → ② 仓库里已有？复用 → ③ stdlib 能做？ → ④ 原生平台功能覆盖？ → ⑤ 已装依赖解决？ → ⑥ 能一行？一行 → ⑦ 最小可行代码。**理解问题在前，爬阶梯在后。**
- **根因优先修复**：一处共享护栏 < 每处调用加补丁；先 grep 所有 caller 再改。
- **`ponytail:` 注释约定**：把刻意的简化标记成 `ponytail: <天花板>, <升级路径>`，让"迟延"不沦为"永不"。
- **不只懒**：输入验证/防数据丢失的错误处理/安全/无障碍/显式要求的东西**绝不高阶简化**；非平凡逻辑留一个 `assert` 自检或一个小测试。

---

## 2. ponytail ↔ dev-skills 叠加与差异分析

### 2.1 与现有技能的边界（重叠处）

#### 与 `review` 重叠
- `review` 是**三视角平行审查**（Test ∥ Code ∥ Impact），关注**正确性、安全、性能、变更影响**，属于 full-stack 完成质检。
- `ponytail-review` 只查**过度工程/复杂度**，并显式把"正确性漏洞、安全洞、性能"划出界外。
- **结论**：两者互补不冲突。`ponytail-review` 是 `review` 的一个**可选子视角**（瘦身视角），应作为独立互补技能而不是并入 `review`。

#### 与 `improve-architecture` 重叠
- `improve-architecture` 走**域语言/ADR 对齐 + 设计债**，产出"架构改进报告 + 优先级 + 努力度估算"。
- `ponytail-audit` 走**纯机械可削减量**（删/简/stdlib 替换），产出"每行一个发现 + net 行数"。不涉及域建模，不看 PRD/ADR。
- **结论**：`ponytail-audit` 是**代码级瘦身审计**（bottom-up），`improve-architecture` 是**设计与债务评估**（top-down）。可并存，边界写入 RESOLVER。

#### 与全局规则 `rules/anti-patterns.md` 的关系
- 现有规则**#8（过早抽象）、#31（补偿性复杂度）** 与 ponytail 理念同源，但都是负面清单（什么不能做）。
- ponytail 是**正面可操作法则**（爬阶梯、标记天花板、根因 = bug fix），于是成为这些反模式的"怎么做到"的操作补充。可作为**引用关系**而不是重复拷贝（见反模式 #38：别抄共享规则）。

### 2.2 架构性差异：模式模型不兼容
- dev-skills 现有技能**全部是按需触发的一次性流程**（有 outcome contract / done-when / process），不持久激活。
- ponytail 是**常驻模式**（默认激活，直到 `off`；带强度分级）。
- 迁移必须明确决策这一点，否则会在本仓库引入第一个"常驻 skill"，需要显式书面约定（见 §3.2）。

### 2.3 需要裁剪/本土化的点
- **命令前缀**：ponytail 用 `/ponytail-*` 与 `@ponytail`。dev-skills 用 `/skill` 目录名。应统一为 `/ponytail`、`/ponytail-review` 等（与本仓库 slash 风格对齐）。
- **外部平台差异化**：ponytail-help 里 "Claude Code/Codex/OpenCode" 的触发方式差异、`/plugin`、环境变量 `PONYTAIL_DEFAULT_MODE`、配置文件 `~/.config/ponytail/` —— 这些**平台特定内容**属反模式 #19（公共技能表面泄漏），仅迁移观念，不迁移平台专属机制。
- **中文触发词**：本仓库 RESOLVER 触发词是英中双语，ponytail 目前只有英文触发词，需补中文（懒、简单、yagni、精简、去重、过度工程、重建 等）。
- **README/CHANGELOG/惯用输出**：本仓库技能在 SKILL.md 末尾有 **Output 模板 + Gotchas 表 + Workflow Position**；ponytail 是紧凑叙述。落地时按本仓库模板重排（反模式 #30 别前置过程）。

---

## 3. 已确认的落地范围（你的选择）

你已选定：

1. **当前只加最小核心 skill**（即上面 A 类的 `ponytail` 常驻模式技能），`review / audit / debt / gain / help` 五个命令类技能**后续再谈**（建议第二步）。
2. **模式模型**：保持常驻模式语义（lite/full/ultra + 开关），作为本仓库**第一个持久模式技能**引入。
3. **本步动作**：先产出本文档（分析 + 迁移方案），**不写实际技能文件**。逐级批准后再落地。

---

## 4. 迁移方案（含未来批次规划）

### 批次 1（本次，最小核心）：新增 `ponytail` 常驻模式技能

- 目录：`skills/ponytail/SKILL.md`（+ 视需要 REFERENCE.md）
- SKILL.md 结构按本仓库惯例重排：
  - YAML frontmatter：`name: ponytail`，`description`（英文为主，含 `ponytail` 常量激活关键词 + 中文触发词 + 使用场景）。
  - `## Events/Settings` 说明这是持久模式，并指出**这是本仓库唯一常驻技能**，与其他按需技能不做流程链。
  - **Outcome Contract / Persistent Contract**：定义"激活期间每个响应都遵守的约束"，而非一次性产出的 done-when。
  - **响应契约**：代码先行 ≤3 行、`[code] → skipped: X, add when Y` 输出格式。
  - **Ladder**（原 7 条富含完整，中文解释）。
  - **Rules**（原 9 条：无未请求抽象、删 > 增、最少数文件、两个 stdlib 取正确一个、标记真实切角等）。
  - **Intensity** 表格（lite/full/ultra）。
  - **When NOT to be lazy** 豁免表（不改验证/安全/数据/可访问/显式请求）。
  - **根因修复** = 最小钩子（不是症状）。
  - **ponytail: 注释** 负载债约定（与未来 `ponytail-debt` 供衔接）。
  - **测试**：非平凡逻辑给 assert 自检/小测试。
  - **Gotchas 表**（本仓库惯例）。
- 平台专属 / plugin / env / 路径内容**不迁移**（反模式 #19）。
- 与 `anti-patterns.md` 的引用关系写明：`#8 过早抽象 / #31 补偿式复杂度` 的操作落地即本技能。

### 批次 2（后续，待审批）：一次性瘦身与债务技能

- 前议三点：
  - `ponytail-review` 与 `review` 的边界（复杂度回调子集，不并入）
  - `ponytail-audit` 是 `improve-architecture` 的互补（bottom-up 代码瘦身 vs top-down 架构评估），可独立或作为 improve-architecture 的可选 pass。
  - `ponytail-debt` 依赖批次 1 的 `ponytail:` 注释；需先有核心技能产生这些注释才有意义。
  - `ponytail-gain` 的"固定分数板 + 诚实守界"可保留但需按本仓库写风格重排。
  - `ponytail-help` 收编进 README/RESOLVER，不单独做。

### 4.3 融合配套（无论批次，都要改）

- `skills/RESOLVER.md`：加 `ponytail` 的触发词、与 review/improve-architecture 的别歧规则、技能清单一行。
- `AGENTS.md`：Repository Structure 加目录行，工作流图加可选 `ponytail` 常驻模式的说明。
- `README.md` / `README_ZH.md`：加新的命令说明。
- `CHANGELOG.md`：记录新增。

---

## 5. 关键决策点（落地需你批准）

1. **常驻模式是否接受**：引入本仓库首个持久模式技能后，`disable-model-invocation` / 默认激活程度（full？）怎么定。建议：默认不高亮显式调用也无碍，但需明确定义"何时算过期激活"以防污染非编码任务（ponytail 自己说别用在非编码）。
2. **`ponytail:` 注释命名**：是否随 `-comment` 约定 in 到本仓库语言规范（AGENTS 用英文注释，但可接受）保持一致。
3. **纯度**：本次只做原始核心的"忠实改编"（保 ladder/制度/开关），并把"平台专项、`/bin` 差异化"剔除。
4. **命名唯一性**：本仓库是否已有 `ponytail` 相关名称冲突（已核查：无）。

---

## 6. 不一致风险（提示，不阻断）

- 现有技能的 `disable-model-invocation` 机制在 AGENTS.md 提到但技能集未实际使用，可借 ponytail 常驻模式时首次落地用法。
- ponytail 假设"一个 lazy 模式常驻"，与本仓库"按任务触发"哲学不同，README 措辞需先发而避免造成误解。

---

## 7. 下一步

确认本方案，分批（批次1→批次2）执行；每批次执行后再合并 RESOLVER/AGENTS/README 配套改动。执行会让本仓库的审查技能多一个"复杂度视角"，并引入第一个常驻技能。