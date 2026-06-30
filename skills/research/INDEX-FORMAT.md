# Research INDEX Format

## 用途

研究知识库的索引与入口文件。位于 `docs/research/INDEX.md`。下游 skill（尤其 `/think` Step 5 的 research-first）**先查这里**：命中则复用 TL;DR，未命中才启动新研究。

## File Location

`docs/research/INDEX.md`

**Lazy creation**: created only when the first research record is produced; never scaffolded as an empty file (mirrors the `docs/prd/` and `docs/adr/` convention).

## Dual-View Structure

INDEX provides two views over **the same set of records**, serving two query types:

1. **By Stack** — grouped per stack; answers "what research exists for this stack". One row per record.
2. **By Topic** — cross-stack comparison; answers "how does this topic behave across different stacks". Multiple stacks of the same topic listed side by side.

Both views point to the same `<stack>-<topic>-<major>.md` files; content is not duplicated.

## Template

```markdown
# Research Index

> Entry point for every research record. Query here first; reuse the TL;DR on a hit, start new research only on a miss.
> Status values: verified (validated) | stale (current project major is higher; suggest re-research) | deprecated (abandoned).

## By Stack

### react

| Topic | Major | Version | Verdict | File | Status |
|---|---|---|---|---|---|
| concurrent-rendering | 18 | react@18.2.0 | useTransition is enough; do not build a custom scheduler | [react-concurrent-rendering-18.md](react-concurrent-rendering-18.md) | verified |
| suspense-data-fetching | 18 | react@18.2.0 → 19 | Many edge cases; consider wrapping with React Query | [react-suspense-data-fetching-18.md](react-suspense-data-fetching-18.md) | stale |

### postgres

| Topic | Major | Version | Verdict | File | Status |
|---|---|---|---|---|---|
| index-strategy | 15 | postgres@15.4 | Partial indexes + BRIN save 60% space vs B-tree | [postgres-index-strategy-15.md](postgres-index-strategy-15.md) | verified |

## By Topic

> Cross-stack comparison of the same topic. Single-stack topics are kept too (listed when ≥1), so a future new stack immediately sees the existing baseline.

| Topic | Stacks | See |
|---|---|---|
| concurrent-rendering | react@18 | [react-concurrent-rendering-18.md](react-concurrent-rendering-18.md) |
| data-fetching | react@18 | [react-suspense-data-fetching-18.md](react-suspense-data-fetching-18.md) |
| index-strategy | postgres@15 | [postgres-index-strategy-15.md](postgres-index-strategy-15.md) |
```

## 字段说明

| Field | Description |
|---|---|
| Topic | Research slug (kebab-case), without the stack prefix |
| Major | Major version number, matching the filename suffix |
| Version | Version column. **verified/deprecated rows**: a single studied version (e.g. `react@18.2.0`). **stale rows**: `studied-version → current-major` (e.g. `react@18.2.0 → 19`), showing version drift at a glance |
| Verdict | A one-line conclusion; a further distillation of the record file's TL;DR |
| File | Relative link to the record file |
| Status | **Fixed plain-text enum**: `verified \| stale \| deprecated`. **Carries no data, no emoji** (mirrors PRD's `Status: Draft` and ADR's `Status: Accepted` conventions) |

## Status Field Rules (mandatory)

**The Status column is always a pure enum token and carries no data.** All version information belongs in the Version column.

| Status | When set | Set by |
|---|---|---|
| `verified` | When the research record is written | `research` skill |
| `stale` | When any INDEX-reading skill finds the current project major is higher than the record's major | Any INDEX-reading skill (think/research/grill) — collaborative marking |
| `deprecated` | When the conclusion is overturned or the stack is abandoned | Explicit human marking |

### Full format of a stale row

When a row is marked stale, **edit both fields** (never embed data in Status):

- `Status` column → `stale` (pure token, no data)
- `Version` column → change from a single value to `studied-version → current-major`

Example:
```
| suspense-data-fetching | 18 | react@18.2.0 → 19 | Many edge cases... | react-suspense-data-fetching-18.md | stale |
```

The re-research hint is written at the end of the verdict or in a note below the table, in the format: `→ suggest /research react suspense-data-fetching-19`. **Do not auto-trigger re-research** — that is the user's explicit call.

## By Topic View Rules

- **Single-stack topics are listed too** (listed when ≥1 stack has researched it). Value: when a future new stack researches the same topic, the existing baseline is immediately visible.
- **Topics with 0 stacks researched do not appear** (no record to index).
- `Stacks` column format: `<stack>@<major>`, multiple stacks space-separated: `react@18 vue3@3`.

## 更新规则

1. **Immediate update** — the `research` skill updates both INDEX views immediately when producing a new record (mirrors PRD/ADR's "file on creation"; no batching).
2. **Collaborative stale marking** — any skill reading INDEX marks stale immediately on detecting a version mismatch; do not wait for the next `/research`.
3. **Do not delete stale rows** — stale records have historical value (immutability principle, ADR-0004); keep and mark them.
4. **Re-research produces a new row** — when the user explicitly runs `/research <stack> <topic>-<newmajor>`, a new record file is created and a new INDEX row added; the old row stays stale, not deleted.

## Anti-patterns

| Anti-pattern | Correct approach |
|---|---|
| Status column carries data (e.g. `stale (v19)`) | Status is a pure enum; version info belongs in the Version column |
| Using emoji for status (check/warning/cross symbols) | Plain-text enum (verified/stale/deprecated), mirroring PRD/ADR conventions |
| Deleting the old record on a stale row | Keep and mark stale (immutability, ADR-0004) |
| By Topic lists only topics with ≥2 stacks | Single-stack topics are listed too, preserving the comparison baseline |
| INDEX scaffolded empty ahead of time | Created only when the first record is produced |
