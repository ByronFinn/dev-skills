# Research Record Format

## 用途

单条技术研究记录的格式模板。由 `research` skill 生成。每条记录回答「在某个 stack 的某个 major 版本下，某个 topic 的最佳实践是什么」，基于权威信源，且不可变（immutable）。

## 文件位置与命名

`docs/research/<stack>-<topic>-<major>.md`

### 命名规则（强制）

- **Fixed three-segment format with major**: `<stack>-<topic>-<major>.md`. The **major version is always part of the filename** — INDEX reads version from the filename, not by re-reading file contents. Examples: `react-concurrent-rendering-18.md`, `postgres-index-strategy-15.md`.
- **stack = leaf unit**: a single library/framework/language with its own version number and official source. **No composite slugs** (`react-nextjs` is wrong; decompose into `react` and `nextjs` as separate records).
- **Slug-casing**: lowercase + hyphens, **strip special characters and dots**:
  - `C++` → `cpp`
  - `Node.js` → `nodejs`
  - `PostgreSQL` → `postgres`
  - `.NET` → `dotnet`
  - `C#` → `csharp`
  - Applies to both stack and topic.
- **Topic granularity**: a topic must be answerable by a **single one-line verdict**. If the conclusion needs a branching matrix ("in case A choose X, in case B choose Y"), the topic is too broad and must be split.
- **Lives only in `docs/research/`**: never at the repo root, `docs/` root, `docs/prd/`, or `docs/adr/`.
- **Language**: follow the project config `docs/agents/language.md` (written by `/setup-project`). If unconfigured, fall back to the user's input language and ask the team's preference. See [Skill Entry Protocol](../rules/entry-protocol.md).

### 主版本与多版本共存

- **Different majors of the same stack+topic each occupy one file**: `react-concurrent-rendering-17.md` + `react-concurrent-rendering-18.md` + `react-concurrent-rendering-19.md` coexist.
- **Monorepo multi-major coexistence**: if the project uses React 17 (package A) and React 18 (package B) simultaneously, write one record per major — do not merge.
- **Minor/patch do not split files**: `18.2` and `18.3` share `-18.md` (the full-version difference is recorded in the record's `stack@version` field, not by splitting files).

## 记录生命周期状态

每条记录有一个固定纯文本 `Status` 字段（**不使用 emoji**，对齐 PRD/ADR 惯例），取值如下：

```
verified → stale → (re-researched: new -<newmajor>.md | deprecated)
```

| Status | Meaning | Set by |
|---|---|---|
| **verified** | Research complete, `stack@version` confirmed, conclusion valid for the current major | `research` skill (on write) |
| **stale** | The current project's major is higher than the record's major (major difference only). **Does not mean the record is wrong** — it faithfully documents the best practice of that major era. Marked by any skill reading INDEX when it detects a version mismatch | Any INDEX-reading skill (think/research/grill) |
| **deprecated** | Conclusion overturned or the stack itself abandoned. Requires explicit human marking | Human |

**Stale threshold**: **only a major difference triggers stale** (`18.2` vs `19.0` → stale; `18.2` vs `18.3` → no trigger). Exception: the record author may explicitly declare "sensitive to minor changes" in `## Boundary Conditions` (e.g. security libraries); then minor differences also trigger stale — the call belongs to the record author, not a global rule.

## 不可变性 (ADR-0004)

**A record is frozen the moment it is written.** This is the core cross-major constraint:

- **DO (new major arrives)** → create a new `-<newmajor>.md` file (e.g. `-18.md` → `-19.md`); the old record stays frozen.
- **DON'T (edit an old record to "update" it)** — even if the old conclusion no longer applies in the new major. The old record faithfully documents that major era's best practice and has historical traceability value.
- **Intra-major error correction**: if an error is found in an already-written record **within the same major**, do **not** silently rewrite the original. Instead, append a dated, sourced `## Correction` block explaining the fix. Immutability applies across majors; intra-major uses append, not rewrite.

## 模板

```markdown
# <Stack>: <Topic>

> **Stack**: <stack>@<full-version>  | **Major**: <major>  | **Verified**: <YYYY-MM-DD>  | **Status**: verified

## TL;DR

<2-3 lines: verdict + key trade-off. INDEX's "one-line verdict" is a further distillation of this. Downstream skills (e.g. /think Step 5) read only this by default to make a decision.>

## Question

<The specific question the research answers, in one sentence. Make stack + topic + target major explicit.>

## Approach

<The reasoning process: how the conclusion was reached. Which official docs/source sections were read, what was compared. Lets future readers reproduce your reasoning.>

## Findings

<Comparison matrix: options considered and their trade-offs.>

| Option | Pros | Cons | When to use |
|---|---|---|---|
| <option A> | ... | ... | ... |
| <option B> | ... | ... | ... |

## Verdict & Rationale

<Final conclusion + why this was chosen. Must be supported by at least one Tier 1 source.>

## Boundary Conditions

<Applicability boundaries: in which version range/scenarios it holds; when it does not apply. May declare "sensitive to minor changes" here as a stale exception.>

## Sources

<Mandatory field. Every verdict needs at least 1 Tier 1 source as primary evidence. All links must be directly accessible URLs pointing to the specific page, not a homepage.>

**Tier 1 (maintainer-authored, required)**
- [Official docs: specific page title](<direct-URL-to-specific-page>) — <point cited>
- [Official source: file/line](<direct-URL>) — <point cited>
- [Official spec/standard: section](<direct-URL>) — <point cited>

**Tier 2 (supplementary only, never sole evidence)**
- [Official changelog: version entry](<direct-URL>) — <point cited>
- [Accepted/Merged RFC: number](<direct-URL>) — <point cited>

<!-- Optional: intra-major error correction. Do not delete original text; append this block. -->
<!-- ## Correction (YYYY-MM-DD)
Based on <Tier 1 source URL>, corrects: <what was wrong, what is right>. Original text retained above for history. -->
```

## 字段说明

| Field | Description |
|---|---|
| Stack | `<stack>@<full-version>`, e.g. `react@18.2.0`. Full version (major.minor.patch). Use `unknown` when no dependency manifest is readable; stale checks are then skipped |
| Major | The major version number, e.g. `18`. Matches the filename suffix |
| Verified | Research completion date, YYYY-MM-DD |
| Status | Fixed plain-text enum: `verified \| stale \| deprecated`. **Carries no data, no emoji** |
| TL;DR | 2-3 行 verdict + trade-off，供下游 skill 只读这里即可决策 |
| Question | 一句话研究问题 |
| Approach | 推理过程，可复现 |
| Findings | 对比矩阵，多方案 trade-off |
| Verdict & Rationale | 最终结论，至少 1 个 Tier 1 信源支撑 |
| Boundary Conditions | 适用边界 + 可选的"对 minor 敏感"声明 |
| Sources | 强制：Tier 1 必收（至少 1 个），Tier 2 仅补充 |

## 信源分级标准（强制）

**Core rule: every verdict needs at least 1 Tier 1 source as primary evidence; Tier 2 only supplements, never solely supports a verdict.**

| Tier | Scope | Authority source |
|---|---|---|
| **Tier 1 (required, primary)** | Official documentation, official source code, official specifications/standards (ISO/W3C/ECMA-262 etc.) | Content **produced by the maintainers themselves** |
| **Tier 2 (supplementary only)** | Official changelogs, **Accepted/Merged only** official RFCs/proposals, maintainer-flagged (pinned/labeled) official comments in official repos | Official but non-normative, needs context |
| **Excluded** | Personal blogs, tutorial sites, unofficial translations, AI-generated content, Stack Overflow answers (unless they link to an official source), **community-maintained-but-not-official sites** (e.g. cppreference, community-maintained periods of redux.js.org), **unaccepted RFC drafts**, non-maintainer comments | Authority does not derive from the maintainers themselves |

## 示例

```markdown
# React: Concurrent Rendering

> **Stack**: react@18.2.0  | **Major**: 18  | **Verified**: 2026-06-30  | **Status**: verified

## TL;DR

For CPU-intensive rendering (large list filtering, chart re-computation), mark non-urgent updates with `useTransition` to avoid blocking the main thread; do not build a custom scheduler — React 18's concurrency model has priorities built in. `useDeferredValue` suits "deferred value" scenarios. Suspended data fetching has many edge cases; consider wrapping with React Query.

## Question

In React 18, when and how should concurrent rendering be used to avoid main-thread blocking?

## Approach

Read the official React docs sections on "Concurrency", "useTransition", and "useDeferredValue", cross-referenced the priority lane model in official source `packages/react-reconciler/src/ReactFiberLane.js`, and consulted the `createRoot` breaking change in the official React 18.0 changelog.

## Findings

| Option | Pros | Cons | When to use |
|---|---|---|---|
| useTransition | Official API, marks non-urgent updates, yields the main thread | Must wrap setState calls | Large list filtering, search, chart re-computation |
| useDeferredValue | Declarative, defers a value's propagation | Can only defer values, cannot control update triggers | Input debouncing, real-time charts |
| Custom scheduler | Full control | Conflicts with React's internal scheduling, hard to maintain | Almost never |

## Verdict & Rationale

Use `useTransition` (CPU-intensive) or `useDeferredValue` (deferred value) by default. Do not build a custom scheduler — React 18's concurrency model has priority lanes built in; a custom one would conflict with it.

## Boundary Conditions

Applies only to React 18+ (`createRoot`). React 17 and below have no concurrent rendering. Not sensitive to minor (18.0-18.2 behave identically).

## Sources

**Tier 1 (maintainer-authored, required)**
- [React official docs: Concurrency in React 18](https://react.dev/blog/2022/03/29/react-v18#concurrent-features) — concurrency feature overview
- [React official source: ReactFiberLane.js](https://github.com/facebook/react/blob/main/packages/react-reconciler/src/ReactFiberLane.js) — priority lane model

**Tier 2 (supplementary only, never sole evidence)**
- [React 18.0 official changelog](https://github.com/facebook/react/blob/main/CHANGELOG.md#1800-march-29-2022) — createRoot becomes default
```

## 反模式

| Anti-pattern | Correct approach |
|---|---|
| Cited a second-hand blog as decision evidence | At least 1 Tier 1 official source as primary evidence |
| Source URL points to a homepage, not the specific page | URL must point to the specific page proving the claim |
| Treated a community-maintained site (cppreference etc.) as official | Strictly follow "authority derives from the maintainers themselves" |
| Tier 2 source solely supports a verdict | Tier 2 only supplements; must pair with Tier 1 |
| Edited an old record to "update" for a new major | Create a new `-<newmajor>.md`; the old record stays frozen (ADR-0004) |
| Intra-major error silently rewritten | Append a dated, sourced `## Correction` block |
| Filename omits the major version | Major is always part of the filename |
| Composite stack slug (react-nextjs) | Decompose into leaf units, each its own record |
