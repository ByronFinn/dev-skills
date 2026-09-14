# Skills Eval: GEPA-style evaluation and optimization framework

Evaluation framework for the dev-skills skill set — both **single-skill quality** and **whole-workflow coherence**. Method grounded in [docs/research/gepa-eval-loop-1.md](../research/gepa-eval-loop-1.md) (GEPA loop: per-sample score + textual feedback, Pareto candidates selected by holdout, budget-bounded), [docs/research/agentskills-skill-authoring-1.md](../research/agentskills-skill-authoring-1.md) (what to check), and [docs/research/agent-interviewing-question-pacing-1.md](../research/agent-interviewing-question-pacing-1.md) (interview behavior to check). The older probe harness lives on in Level T-Live: [trigger-eval.md](trigger-eval.md).

## The loop (GEPA adapted to a Markdown repo)

```
candidate (skill files on disk)
   → run eval levels (S, W every iteration; T-Live, B at checkpoints)
   → collect per-check failures WITH textual feedback          ← Actionable Side Information
   → reflect: diagnose the general category, never keyword-patch
   → mutate: one targeted edit batch per iteration
   → accept iff hard-check score does not regress (holdout decides T/B ties)
   → log docs/evals/results/iteration-NN.json + scoreboard.csv row
```

Selection rule: the **final** state is the best-holdout candidate across the run, not the last iteration. Stopping: eval budget declared in advance (this run: ≥50 iterations by owner mandate) or feedback consistently empty.

## Levels

| Level | What | How | Cadence | Gate |
|---|---|---|---|---|
| **S — Static compliance** | Per-skill structure vs the authoring bar: frontmatter, description, outcome-contract-first, gotchas/output sections, line budgets, TOC, sub-agent REFERENCE chapters, one-by-one interview rules (think/grill), no batch-question language | `scripts/eval_skills.py --level s` (deterministic, stdlib only) | every iteration | exit 1 on any hard fail |
| **W — Workflow coherence** | Cross-skill graph: handoff targets exist, entry-protocol referenced, RESOLVER inventory complete, Traceability producer/consumer pairs, plus everything `scripts/check-docs.py` checks | `scripts/eval_skills.py --level w` (deterministic + subprocess) | every iteration | exit 1 on any fail |
| **T — Trigger routing** | Does the catalog route real phrasings to the right skill? **T-Proxy** (deterministic lexical-overlap, catches keyword drift) every iteration; **T-Live** (fresh subagent sees only name+description snapshot, picks one skill or NONE) at checkpoints | proxy: `--level t`; live: protocol below, results filed in `results/` | proxy every iteration; live at checkpoints | train/holdout accuracy reported separately |
| **B — Behavior simulation** | Do the interviewing skills actually behave one-by-one? Turn-by-turn subagent simulation with scripted user answers + rubric judge | manual protocol below, results filed in `results/` | checkpoints (baseline / mid / final) | per-turn rubric, majority where noisy |

## Datasets and the overfitting guard

- **Trigger queries**: `scripts/evals/trigger-queries.json` — ≥20 queries, half should-trigger, half near-miss/NONE, mixed 中文/English, casual phrasings. Split **60/40 train/holdout**. Edits to `description` fields are guided by **train failures only**; holdout accuracy is the headline number. Never add a failing query's keywords to a description — fix the boundary description instead (agentskills.io rule).
- **Behavior scenarios**: `scripts/evals/behavior-scenarios.json` — per interviewing skill: one **train** scenario (drives fixes) + one **holdout** scenario (only reported). Each scenario embeds a mock repo (PRD + CONTEXT.md + code snippet), a scripted answer per expected turn, ground-truth open items, and code-answerable items the agent must resolve itself (never ask).
- **Static checks**: the check list itself is the dataset; a check that passes 3 consecutive full rounds without ever failing moves to "stable" in the scoreboard notes (saturation awareness) but stays in the suite as a regression gate.

## Metrics

Per iteration the harness writes `docs/evals/results/iteration-NN.json` (per-check results **with textual feedback strings** — the load-bearing part) and appends to `docs/evals/results/scoreboard.csv`:

```
iteration, S_hard_pass, S_hard_total, S_soft_pass, S_soft_total, W_pass, W_total,
T_proxy_train, T_proxy_holdout, notes
```

Checkpoints add `checkpoint-<name>.json` with T-Live and B results (per-turn rubric verdicts + judge evidence quotes).

## T-Live protocol (checkpoint)

1. Snapshot catalog: all `name` + `description` from `skills/*/SKILL.md`, marking `disable-model-invocation` units `[user-invoked only]`.
2. One subagent per query (fresh context): show the catalog inline, give the user message verbatim, ask for `SKILL: <name>` or `SKILL: NONE` + one-line justification. The subagent must not see the repo, file paths, or expected answers.
3. Score vs expected. Single-run failures are directional (documented judge-noise limitation; majority-of-3 reserved for final-round boundary calls).

## B protocol (checkpoint)

Per scenario, per turn:

1. **Actor subagent** (fresh context): receives the skill's SKILL.md + REFERENCE.md verbatim, the scenario's mock repo, and the transcript so far — but never future scripted answers. Instruction: *produce only your next single message to the user.*
2. Advance the transcript: the next scripted user answer is appended only if the actor's question matches the expected focus (else the generic scripted fallback answer is used — a batch-questioner thereby strands questions, which the judge flags).
3. **Judge subagent** (fresh context, rubric fixed): given turn message + transcript + scenario ground truth, return JSON: `{"exactly_one_question": bool, "recommended_answer_present": bool, "adaptive": bool|null, "asks_code_answerable": bool, "completion_correct": bool|null, "evidence": "..."}`. Rubric notes: a numbered inventory the agent extracts as its own work plan is not a batch of questions; on **approval submissions**, `recommended_answer_present` is N/A — the submitted plan is itself the recommendation (checkpoint-2 decision); post-approval action lists ("after approval I will X") are not asks.
4. Scenario score = fraction of rubric points across turns; report per skill: one-question rate, adaptivity rate, no-code-ask rate, completion correctness.

## Decision rules

- A `description` change requires a T round (proxy always; live at checkpoint) — existing rule from [trigger-eval.md](trigger-eval.md), now enforced by the scoreboard.
- An interview-rule change (think/grill) requires a B checkpoint before finalization.
- Any hard S/W failure blocks "done" — re-run until clean (regression gate).
- Fixed iteration budget per optimization campaign is declared up front; candidates are compared on holdout, and the best-holdout state is the one that ships.

## Known limitations

- T-Proxy is lexical and gameable; it exists to catch drift between checkpoints, not to replace T-Live.
- T-Live/B judges are model-based: single failures directional; rubric evidence quotes recorded so verdicts are auditable.
- B scenarios embed mock repos inline; they exercise the conversation contract (pacing, adaptivity, gating), not filesystem side effects.
