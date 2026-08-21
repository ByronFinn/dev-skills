# 工作流设计审计与修复（Workflow Design Audit）

> **日期**: 2026-07-05 · **执行者**: 全仓工作流设计审计（用户发起）· **范围**: `skills/**`（12 个 skill 全量）+ `rules/` + `RESOLVER.md` + `docs/agents/` + AGENTS.md
> **方法**: 逐文件通读 + 分区子代理深审（tdd/review/implement、think/grill、story/research、debug/ia/have-a-try/setup、write）+ 全仓引用扫描脚本复核。所有 P1 结论均经一手验证（脚本 + 逐字比对）。

## TL;DR

- 架构骨架（分层结构、PRD Traceability 契约、子代理独立纪律、research 不可变记录、幂等 setup）是健全的；问题集中在**跨技能接缝**与**规则复述漂移**。
- 修复 **4 处 P1**（跨技能契约断裂 / 永不触发的触发器 / 双文件互相矛盾 / 双路由表冲突）、**12 处 P2**（冗余与漂移）、**约 15 处 P3**（编号、格式、缺失要素）。
- 反模式主表从 38 条瘦身至 **25 条，全部有 consumer 引用**；13 条零引用规则移入 Archive 段（编号冻结，不重编号）。

## P1（逻辑断裂，已修复）

| # | 位置 | 问题 | 修复 |
|---|---|---|---|
| 1 | `review/SKILL.md` + `review/REFERENCE.md` Ch1 | diff 采集只定义 staged/unstaged；`/implement` 每 seam 提交后再派 `/review`，工作树干净 → 三个子代理收到空 diff。主管线最后一环断裂 | Ch1 Step 1 增加 B 分支：干净树时用 `git diff $(git merge-base <default> HEAD)..HEAD` 或 PR diff；Prerequisites 改为 "staged/unstaged **or** committed on branch"；空 diff 时停下询问 |
| 2 | `debug/REFERENCE.md` Stage 1 | Stage 1 只生成 1-2 个假设，升级条件却是 "3 hypotheses fail"（永不触发）；Stage 2 无假设耗尽出口，Handoff 模板无锚点 | 升级条件改为 "quick validation fails (hypotheses refuted / none explains all symptoms)"；Phase 4 增加 "3 falsified hypotheses → emit Handoff"；SKILL Handoff 标题锚定 Phase 4 |
| 3 | `think/REFERENCE.md` Step 5 | Research Steps 无条件开始研究，未提 INDEX —— 与 SKILL.md Step 5 的 "query INDEX first" 直接矛盾 | REFERENCE 增加 INDEX gate（权威表指向 SKILL.md），research steps 限定 "only on an INDEX miss" |
| 4 | `write/SKILL.md` Modes 表 ↔ `write/REFERENCE.md` Pre-flight | Release Notes 无条件路由到中文目录；英文 release notes 两表冲突 | 两表统一：中文 → write-zh-release-notes.md；英文 → write-en.md（新增 §Release Notes & Social Posts 英文镜像章节） |

## P2（冗余与漂移，已修复）

1. **tdd Gate Modes 三重复述** → SKILL.md §Gate Modes 为唯一权威；:87 的复述缩为一行指针；REFERENCE Ch6 #10 删除（连同与 SKILL Gotchas 重复的 5 条 + 编号跳跃 5→8，重排为 1-7）。
2. **Runtime Note 两技能近逐字重复** → 新建 `rules/sub-agent-runtime.md`（单一权威，链 ADR-0001）；tdd/review SKILL.md 改为链接。
3. **review/REFERENCE Ch3/Ch4 内部 "Extra Context Re-Read" 各重复两遍**（复制粘贴事故）→ 删章首副本，统一放章尾。
4. **anti-patterns 38 条中 16 条零引用** → 13 条移入 Archive 段（编号冻结）；主表 25 条全部有引用；RESOLVER 补 #30 引用（结构性约定）。#1 补 entry-protocol 引用。
5. **write 中文路径加载 998 行**（prose 卡内容 ~100% 被 721 行大目录覆盖）→ REFERENCE 增加 Loading Policy：轻 polish 只加载 42 行快卡，深改写/长文才加载大目录；混合中英文自动补双语 spacing 块。
6. **research Tier-1/slug 规则三处复述** → SKILL 保留一句原则，完整规则指向 RESEARCH-FORMAT.md（§信源分级标准 / §文件位置与命名）单一权威。
7. **setup-project 技能名单漏 implement（REFERENCE 再漏 have-a-try）** → 两处补全为 12 个。
8. **本仓库 domain.md 实例仍是模板占位符**（指向不存在的 PRD/研究文件）→ 填入真实文件名（PRD-0000/0001、ADR 0001-0004、注明无 docs/research/）。
9. **管线图漂移** → improve-architecture "story → tdd → review" 修正为 "story → implement → review"、"Bug fix: debug" 补 "(optional) review"；have-a-try 自我定位从 "/think 与 /tdd 之间" 修正为 "/think 与 /grill 之间"（与 RESOLVER 一致）。
10. **improve-architecture 阈值两份**（§3.2 表 + Extended Examples 复述）→ 示例改为引用 §3.2 行，不再复述数字。
11. **RESOLVER 四表冗余** → Phase 表删 Description 列（只留触发词→技能）；Skill Inventory 删 Core Role 列（与 Work Object 表重复，注明"复述即漂移"）。
12. **PRD-FORMAT 字段表的 "Child Issues" 幽灵字段** → 更正为 "Sliced into"（PRD 无独立 Child Issues 字段）；review/SKILL Step 6 同步改措辞。

## P3（编号/格式/缺失要素，已修复）

- 编号错位：think gotcha "Step 9→Step 10"；RESOLVER "Step 9a→Step 10a"；story SKILL/REFERENCE 整体错位一格（SKILL 补 Step 0 Read Project Configuration，两文件 0-9 对齐，连带修正 REFERENCE 内 4 处旧编号与 entry-protocol 的引用）；implement gotcha 的 "Step 3a-3f" 标签加 "REFERENCE §" 前缀；setup-project gotcha "Step 4→Step 3-4"。
- 格式：review/SKILL 输出模板制表符 + 未闭合代码围栏（CommonMark）→ 去除；"confirm.Extract" / ".See" 缺空格。
- tdd REFERENCE 章节五要素补齐：Ch2 增 Pre-Gate Self-Check（子代理工作清单）；Ch5 增 Phase-Specific Context（重读清单 + 独立性）；Deep Module 定义收敛到 Ch5 单一权威（消除 Ch1↔Ch5 循环指针）。
- write：SKILL.md Modes 表列出不存在的 "Bilingual Review" procedure（整段重写时移除）；write-zh-prose.md Long-form 指针 SKILL→REFERENCE；Document Review 步骤 5 补快照处置补救；write-en.md 的 "--" 改写；英文镜像章节去 em-dash（该目录原本零 em-dash）。
- have-a-try：Pick a Branch 增加 "两分支皆不适配 → 建议 /research 或 /think" 出口；#13 引用错位修正。
- grill：ADR 3 条件改为指向 ADR-FORMAT.md §创建条件（消除中英双份）；缺失父 Issue 警告消息去硬编码中文（改为按 language.md 输出）。
- setup-project：Step 6 写入顺序定为 "docs/agents 先、AGENTS.md 后"（中断安全）。
- implement/REFERENCE 3b：硬编码 `skills/tdd/` 路径改相对引用；"Code Review Gate"→"Test Code Review Gate" 对齐。
- entry-protocol：CONTEXT.md 默认路径补多上下文分支（根 CONTEXT-MAP.md 存在时读各上下文 CONTEXT.md）。
- review/REFERENCE：General Recovery Steps 改为链接 anti-pattern #36 + 增量（对齐 tdd 做法）；合并报告模板完整版定稿于 Ch5（消除 SKILL↔REFERENCE 循环指针），含 Reviewed-range 字段。

## 做得好（保持）

- PRD Traceability 七字段在模板与全部下游写入方之间精确一致；STORY-FORMAT 的 Meta 契约同样完整。
- PRD Conflict Check 单一权威（think/REFERENCE）+ 四处干净回链，是 #38 的模范执行。
- implement→tdd 委托边界（显式 override）与 debug 的反馈回路分类学。

## 验证

- 引用扫描（修正版正则）：主表 25 条全部被引用、0 悬挂、0 "已归档仍被引用"。
- story SKILL/REFERENCE 步骤数 10=10 对齐；tdd Ch6 编号 1-7 连续。
- write-en.md em-dash 计数回落为 0（除规则本身）。
