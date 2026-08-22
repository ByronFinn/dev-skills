# Trigger Eval: description routing probes

Reusable probe harness for testing whether each skill's `description` routes real user phrasings correctly. Method from [agentskills.io: optimizing descriptions](https://agentskills.io/skill-creation/optimizing-descriptions) — should-trigger and near-miss queries — adapted to this repo: probes run as sub-agents that see **only a snapshot of the current catalog** (name + description, inline in the prompt), so results reflect the descriptions, not the harness's installed copy.

## How to run a round

1. Snapshot all `description` fields: `for f in skills/*/SKILL.md; do sed -n '/^---$/,/^---$/p' "$f"; done`
2. For each query below (or new ones), dispatch one sub-agent with:
   - the catalog snapshot inline (mark `disable-model-invocation` skills as `[user-invoked only]` — they must never be auto-selected);
   - the instruction: *decide which single skill, if any, to invoke based only on these descriptions; answer `SKILL: <name>` or `SKILL: NONE` plus a short justification*;
   - the user message, verbatim.
3. Score against the expected column. Known limitation: 1 run per query (agentskills.io recommends 3) — treat single failures as directional, re-run before acting on a boundary case.

Run a round whenever a `description` changes. Add every observed mis-route in the wild as a new query here.

## Query set (2026-08-22 round)

### Should-trigger

| ID | Query | Expected | Result |
|---|---|---|---|
| P1 | 帮我构思一下这个新功能该怎么做，需求还不太清楚，有好几种可能的做法 | think | ✅ think |
| P2 | 这个方案行不行？帮我把计划里的坑都找出来，一个一个过 | grill | ✅ grill |
| P3 | 计划定好了，把它拆成一批可执行的任务票，标好依赖关系 | story | ✅ story |
| P4 | 这个接口以前是好的，升级依赖之后就 404 了，帮我排查一下 | debug | ✅ debug |
| P5 | 这几个功能的改动都做完了，合并之前帮我把把关 | review | ✅ review |
| P6 | 这段发布文案帮我润色一下，读起来太像AI写的了 | write | ✅ write |

### Near-miss (should NOT trigger the lookalike skill)

| ID | Query | Expected | Result | Finding |
|---|---|---|---|---|
| N1 | 研究一下这个 bug 为什么只在生产环境出现，本地从来没复现过 | debug (not research — "研究" is not 技术调研) | ✅ debug | — |
| N2 | 帮我把 parseConfig 这个函数重构一下，嵌套太深了改平一点就行，别的别动 | NONE (single-function edit, not improve-architecture) | ✅ NONE | — |
| N3 | 帮我测一下这个函数的性能，看看一次调用耗时多少毫秒 | NONE (plain measurement, no decision at stake) | ❌ have-a-try | benchmark trigger over-captured → fixed: description now says "Not for plain one-off measurements or lookups with no decision at stake" |
| N4 | review this PRD draft for clarity and wording before I share it with the team — it's a bit rambling | write (not grill/review — prose wording) | ✅ write | — |
| N5 | think about how to name this boolean variable — should it be isEnabled or hasAccess? | NONE (not think's design-session) | ✅ NONE | — |
| N6 | 调研一下竞品都有哪些功能，然后我们再决定新版本要做什么 | think (product decision, not technical-stack research) | ❌ research | research boundary unclear → fixed: description now bounds to "technical stack/version question", deflects product/market/competitor analysis to think |

## 2026-08-22 round summary

10/12 clean. Two boundary mis-routes (N3, N6), both fixed by description micro-edits the same day. **Decision informed by this round:** the invocation model (11 model-invoked + 1 user-invoked) stays — routing accuracy does not justify restructuring. Re-run N3/N6 after the description fixes land upstream (installed copies refresh).
