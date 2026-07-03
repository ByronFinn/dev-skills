# Architecture Review — Judgment Calls (C2/C3)

> **日期**: 2026-07-04 · **执行者**: `/improve-architecture` · **范围**: C2 (TDD Full/Fast default) 和 C3 (CONTEXT.md external vocabulary)

本文件记录 architecture review 中两项**判断题**（非 bug、有真实权衡）的处置。这两项无客观正确答案，按 anti-pattern #28 不由 assistant 代决——记录判定依据和当前选择，供 `/grill` 或后续维护者复核。

---

## C3 — CONTEXT.md 是否收录 agentskills.io 规范术语

**问题**：CONTEXT.md 当前收录的全是 skill 系统**内部机制**术语（Sub-Agent、Human Review Gate、Research Record 等）。审计初判建议补一个 External Vocabulary 段，收录 Skill / SKILL.md / progressive disclosure / `description` 字段等与 Anthropic 规范对接的术语。

**判定**：**不补，保持 CONTEXT.md 纯净。** 理由：

1. **违反契约**。`grill/CONTEXT-FORMAT.md:5` 定义 CONTEXT.md 为"领域术语表，无实现细节"，`grill/SKILL.md:56` 的反模式明确写"CONTEXT.md gained implementation details → It is a glossary, nothing more"。Skill/SKILL.md/progressive disclosure 是**实现规范术语**，不是项目领域语言——把它们塞进 CONTEXT.md 会破坏 grill 自己的契约。
2. **正确归属**。agentskills.io 规范术语的事实源是 [agentskills.io/specification](https://agentskills.io/specification) 和 [Anthropic 官方文档](https://docs.claude.com/en/docs/claude-code/skills)，本地副本会过时。AGENTS.md:74 已经在 SKILL.md 文件契约处链接到 spec——这正是规范术语该出现的位置（项目级文档，不是领域 glossary）。
3. **dogfood 边缘情况自洽**。本项目"产品"= 技能系统本身，所以 CONTEXT.md 收录 Sub-Agent 等内部术语是合理的——这些**是**该项目的领域语言。但 agentskills.io 术语是**外部规范**，性质不同。

**结论**：C3 不修。CONTEXT.md 保持"项目领域语言 glossary"的纯净契约；规范术语归属 AGENTS.md + 外部 spec 链接。

**复核提示**：若未来项目的"产品"边界扩展（例如 dev-skills 开始直接教授 skill 编写方法论），届时重新评估。

---

## C2 — TDD Full/Fast 默认值姿态

**问题**：TDD 默认 Full 模式（每条 AC 2 个人类门，5 条 AC = 10 次阻塞）。这与 Anthropic《Building Effective Agents》"先简单，复杂再升级"的建议有张力。项目 ADR-0003 把"默认最严格、用户主动降级"作为**有意决策**，但风险是用户因不知道有 Fast 而全程被卡。

**两个选项**：

| 选项 | 含义 | 代价 |
|---|---|---|
| **保持现状** | 默认 Full，用户必须主动喊 Fast | 用户可能因不知有 Fast 而承受不必要的 10 次门 |
| **主动 offer** | 每个 cycle 开头问一句"这条 Full 还是 Fast？" | 改变用户可见交互；每 cycle 多一次确认；可能被视为过度打断 |

**判定**：**这是产品姿态选择，需用户拍板。** assistant 不代决，理由（anti-pattern #28）：
- 改变 TDD skill 的默认交互行为属于"影响用户可见行为"的改动
- 两个选项都有真实成本，无技术正确答案
- ADR-0003 是 Accepted 状态的有意决策，推翻它需要新 ADR 或用户明确指令

**建议提交 `/grill` 决策**：若用户重视此问题，应在 `/grill` 中以 ADR-0005 的形式正式记录新姿态（或确认维持 ADR-0003）。本审计不预设结论。

**复核提示**：当前实现（`tdd/SKILL.md` Gate Modes 段 + ADR-0003）在两种姿态下都不需要代码改动——纯指令层，姿态切换只需改默认措辞。

---

## 总结

- **C3 已进入终态**：判定为不修，理由记录于此。
- **C2 需用户决策**：两个选项已明确呈递，无第三路径。用户选择后即可一行改动落地（改 `tdd/SKILL.md` Gate Modes 段的默认措辞）。
