# Trigger Eval: description routing probes

Probe protocol for testing whether each skill's `description` routes real user phrasings correctly. Method from [agentskills.io: optimizing descriptions](https://agentskills.io/skill-creation/optimizing-descriptions) — should-trigger and near-miss queries. This file is the **protocol + round log**; the query set itself now lives as data in [`scripts/evals/trigger-queries.json`](../../scripts/evals/trigger-queries.json) (20 queries, **60/40 train/holdout** split) and is driven by the harness in [`scripts/eval_skills.py`](../../scripts/eval_skills.py) (Level T-Proxy, deterministic, every iteration) and the Level T-Live protocol in [`skills-eval.md`](skills-eval.md) (fresh sub-agent per query, checkpoints).

## How to run a round

1. Snapshot all `description` fields: `for f in skills/*/SKILL.md; do sed -n '/^---$/,/^---$/p' "$f"; done`
2. For each query in `scripts/evals/trigger-queries.json`, dispatch one sub-agent with:
   - the catalog snapshot inline, verbatim (mark `disable-model-invocation` skills as `[user-invoked only]` — they must never be auto-selected);
   - the instruction: *decide which single skill, if any, to invoke based only on these descriptions; answer `SKILL: <name>` or `SKILL: NONE` plus a short justification*;
   - the user message, verbatim.
3. Score against the expected field. Known limitation: 1 run per query (agentskills.io recommends 3) — treat single failures as directional, re-run before acting on a boundary case.
4. Guide description edits with **train** failures only; **holdout** accuracy is the headline. Never copy a failing query's keywords into a description (overfitting rule).

Run a round whenever a `description` changes. Add every observed mis-route in the wild as a new query in the JSON (extend the holdout first, then rebalance splits).

## Round log

### 2026-08-22 (12 queries, pre-split) — 10/12 clean

Two boundary mis-routes, both fixed by description micro-edits the same day: N3 (have-a-try over-capturing plain measurements → description now says "Not for plain one-off measurements or lookups with no decision at stake") and N6 (research capturing product/competitor 调研 → description bounded to "technical stack/version question"). Decision informed by the round: the invocation model (11 model-invoked + 2 user-invoked units) stays.

### 2026-09-14 (20 queries, 12 train / 8 holdout) — 20/20 clean

Train 12/12, holdout 8/8 (`checkpoint-1.json`). Routing layer unchanged in substance since the 2026-08-22 fixes; four descriptions gained intent-first phrasing ("Use when/for…") during the same campaign without disturbing routing. The `rules` bundle remains `disable-model-invocation` — never model-loaded, competes for no route.

### Query set history

The original 12 queries (P1–P6, N1–N6) live on as the train split; 8 holdout queries (H1–H8) were added 2026-09-14 when the set moved to JSON. T-Proxy (lexical, IDF-weighted) runs every harness iteration and is drift-detection only — its known weakness is CJK phrasing with no lexical overlap (e.g. 任务票 for story); T-Live is the ground truth.

