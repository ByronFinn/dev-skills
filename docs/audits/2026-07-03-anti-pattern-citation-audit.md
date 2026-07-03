# Anti-Pattern Citation Audit

> **日期**: 2026-07-03 · **执行者**: `/improve-architecture` · **范围**: `skills/**/*.md`
> **方法**: 脚本扫描（限定 `anti-patterns.md` 主表 #1–#38，排除 Numbering History 段）+ 全仓 `anti-pattern #NN` 引用反向对照

## TL;DR

- 定义规则 **38 条**，被实际引用的只有 **11 条**（29%）；**27 条（71%）从未被任何 skill 引用**——是 always-loaded 路径上的死重。
- **0 条悬挂引用**（cited-but-undefined）——所有 `#NN` 都能在主表找到定义，编号一致性 OK。
- **1 处编号误指**已修复（`review/REFERENCE.md:560`：`#36` → `#34`）。

## 已修复

| 文件:行 | 原引用 | 修正为 | 原因 |
|---|---|---|---|
| `skills/review/REFERENCE.md:560` | `anti-pattern #36` | `anti-pattern #34` | 上下文是"Re-read shared context from disk"（state drift 的反制，#34），不是 session recovery（#36）。违反了项目自己的 #21「fix one instance, check siblings」——renumber 后没做全仓 citation 扫描 |

## 被引用的 11 条规则（保留）

| # | 引用次数 | 规则 | 引用位置 |
|---|---|---|---|
| 3 | 2 | Serial interrogation | grill/SKILL.md, grill/REFERENCE.md |
| 8 | 1 | Premature abstraction | tdd/REFERENCE.md |
| 13 | 2 | Unsolicited file creation | have-a-try/SKILL.md |
| 15 | 1 | Attribution leak | review/REFERENCE.md |
| 16 | 1 | Implicit authorization escalation | setup-project/REFERENCE.md |
| 19 | 2 | Public skill surface leakage | have-a-try/SKILL.md |
| 29 | 1 | Weak success contract | have-a-try/SKILL.md |
| 34 | 3 | Skill-to-skill state drift | review/SKILL.md ×2, review/REFERENCE.md |
| 35 | 5 | Sub-agent state leakage | tdd/SKILL.md, tdd/REFERENCE.md ×3, review/SKILL.md |
| 36 | 2 | Session recovery | tdd/REFERENCE.md, review/REFERENCE.md |
| 37 | 3 | Silent PRD duplicate | research/SKILL.md ×2, research/REFERENCE.md |

**观察**：引用高度集中在两类——sub-agent 体系（#34/#35/#36/#37，共 13 次）和少数通用 gotcha（#8/#13/#19/#29，共 6 次）。

## 从未被引用的 27 条规则（候选瘦身）

`#1, #2, #4, #5, #6, #7, #9, #10, #11, #12, #14, #17, #18, #20, #21, #22, #23, #24, #25, #26, #27, #28, #30, #31, #32, #33, #38`

**分类建议**（供 `/grill` 决策）：

### A. 可合并进现有高频规则的（重复精神）
- `#1 Act before reading` ≈ 已隐含在每个 skill 的 "Apply Entry Protocol" 里
- `#21 Fix one instance, ignore siblings` —— 本次审计就触犯了它，应保留为高频
- `#38 Restate shared rules` —— 与"shared rules live once in rules/"是同一原则的元表述

### B. 真正通用、应在某个 skill 显式引用的（补引用而非删除）
- `#6 Claim without evidence` —— review/debug/improve-architecture 都该引
- `#17 Declare ready without verifying the artifact` —— review 的核心，却没引
- `#27 External content as trusted instruction` —— research 的核心，却没引
- `#32 Fix without instrumentation` —— debug 的核心，却没引

### C. 可移入 archive 的（场景稀有或已被更具体的 skill gotcha 覆盖）
- `#7 Over-format`, `#25 Scorecard without contract`, `#26 Review request as worktree authorization`, `#31 Compensatory complexity`

## 建议的下一步

1. **立即**：本报告已修复的 1 处编号（已完成）。
2. **短期（B 类）**：在 review/debug/research/improve-architecture 的 SKILL.md 显式引用各自"本该引用"的规则（#6/#17/#27/#32），让通用规则真正进入消费链路。
3. **中期（瘦身）**：把 C 类移到 `rules/anti-patterns-archive.md`，主文件目标 ≤ 20 条、每条都有 consumer。这本身就是项目推崇的 "deep modules" 原则。
4. **流程**：在 `anti-patterns.md` 顶部加一条元规则——"新增规则前，先确认有 consumer skill 会在指令里引用它；否则不进主表。"

## 复现脚本

```bash
python3 - <<'PY'
from pathlib import Path
import re
from collections import defaultdict
root=Path('skills')
ap=(root/'rules/anti-patterns.md').read_text().split('## Usage')[0]
defined={int(m.group(1)): m.group(2).strip()
         for line in ap.splitlines()
         for m in [re.match(r'^\|\s*(\d{1,3})\s*\|([^|]+)\|', line)] if m and m.group(1).isdigit() and 1<=int(m.group(1))<=45}
cites=defaultdict(list)
cite_re=re.compile(r'anti-pattern(?:s\.md)?\s+#?(\d+)', re.IGNORECASE)
for f in sorted(root.glob('**/*.md')):
    if f.name=='anti-patterns.md': continue
    for i,line in enumerate(f.read_text().splitlines(),1):
        for m in cite_re.finditer(line): cites[int(m.group(1))].append((str(f),i))
print('UNCITED:', sorted(n for n in defined if n not in cites))
print('DANGLING:', sorted(n for n in cites if n not in defined))
PY
```
