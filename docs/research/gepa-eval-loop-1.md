# gepa: Evaluation-Driven Prompt/Skill Optimization Loop

> **Stack**: gepa@0.1.4 (per DSPy 2.6-era release notes; paper v2 2026-02-14)  | **Major**: 1  | **Verified**: 2026-09-14  | **Status**: verified

## TL;DR

Optimize skills/prompts with a GEPA-style loop: run a small dual-sided eval, collect **per-sample (score + textual feedback)** — "Actionable Side Information", the text analogue of a gradient — reflect on failing traces, make one targeted mutation, accept only if the held-out score improves, and keep a Pareto pool of candidates selected by validation (never by last-iteration). Dataset: start small (2–3 behavioral cases; ≥20 trigger queries, half near-misses), 60/40 train/holdout, judge noise handled by repeat runs/majority vote. Stop on a pre-declared eval budget or when feedback is consistently empty. Trade-off: more reflection calls than scalar-reward loops, but reportedly 12–35× fewer rollouts than RL to better final quality.

## Question

How should a GEPA-style evaluation-and-optimization loop be designed (loop structure, feedback granularity, dataset, judge calibration, anti-overfitting, stopping) for iteratively improving a Markdown skill set?

## Approach

Read the GEPA paper (arXiv 2507.19457, ICLR 2026 Oral, v2 2026-02-14), the official gepa-ai/gepa repository README (five-step loop, input contract, budget semantics), DSPy's official GEPA overview and getting-started guide (metric-with-feedback contract, valset semantics, stopping), agentskills.io's optimizing-descriptions and evaluating-skills guides (trigger + output eval recipes), OpenAI's evals guide, Anthropic's develop-tests page and "Demystifying evals for AI agents" engineering post (task/dataset design, pass^k, judge calibration), and promptfoo/LangSmith/Braintrust docs (assertion design, CI gates, dataset splits). Cross-checked only practices stated by ≥2 independent official sources.

## Findings

| Dimension | Convergent practice | Sources |
|---|---|---|
| Loop | eval → per-sample trace/critique → reflect (diagnose why) → targeted mutation → accept iff improved; Pareto pool; select final by held-out score | GEPA paper+repo, DSPy, agentskills.io, Anthropic, LangSmith, Braintrust |
| Feedback granularity | textual per-sample critique ≫ scalar ("optimizers know *that* it failed, not *why*"; DSPy metric returns `Prediction(score, feedback)`; concrete evidence required for PASS) | GEPA repo, DSPy, agentskills.io, Anthropic |
| Dataset size | 2–3 output-eval cases to start; "as few as 3 examples" workable for GEPA; ≥20 test cases (Anthropic); 20 trigger queries (8–10 should + 8–10 should-not) | agentskills.io ×2, GEPA repo, Anthropic ×2, LangSmith (10–20) |
| Dual-sided design | positives AND negatives/near-misses — "One-sided evals create one-sided optimization" | agentskills.io, Anthropic eng |
| Splits | train/holdout ~60/40; guide edits only by train failures; select by holdout; keep final fresh-query check | agentskills.io, DSPy, LangSmith |
| Judge noise | 3 runs/query → trigger-rate threshold 0.5; 2–5 samples + majority vote; grader temperature 0; track stddev | agentskills.io, Anthropic, promptfoo |
| Judge calibration | human-verify a labeled set (≥20 balanced), alignment score = % agreement, few-shot the judge prompt, "Unknown" escape hatch | LangSmith, Anthropic eng |
| Assertions | deterministic checks first, LLM-judge only for judgment calls; grade outcomes not paths; resist reward hacking | promptfoo, agentskills.io, Anthropic eng |
| Regression gate | evals run in CI, non-zero exit blocks merge; regression suite grows from real failures | promptfoo, Braintrust, LangSmith, Anthropic |
| Stopping | fixed metric-call budget (GEPA `max_metric_calls`, ~100–500 evals); "five iterations is usually enough" for trigger tuning; stop when "feedback is consistently empty, or you're no longer seeing meaningful improvement" | GEPA/DSPy, agentskills.io |
| Headline numbers | GEPA beats GRPO by 6% avg (up to 20%) with up to 35× fewer rollouts; beats MIPROv2 by >10% (+12% AIME-2025) | GEPA paper |

## Verdict & Rationale

Adopt for dev-skills: a deterministic-first static+workflow suite run every iteration (cheap regression gate, non-zero exit), each failing check emitting (id, location, textual feedback) — never a bare score; a trigger eval with ≥20 queries (60/40 split, near-miss-weighted) run at checkpoints via fresh-context subagents that see only the catalog; a multi-turn behavioral eval for interviewing skills (one-question-per-message rate, adaptivity, tree completeness, no code-answerable asks) with scripted user answers and a rubric judge; iteration log recording every candidate's per-level scores so the final pick is the best-holdout candidate, not the last one. Rationale: every element is stated by the GEPA/DSPy primary sources and ≥1 independent official eval guide (Tier 1); the repo already has check-docs.py as a seed regression gate and trigger-eval.md as a manual probe harness to grow from.

## Boundary Conditions

GEPA numbers were measured on prompt-optimization benchmarks (HotpotQA, AIME, etc.), not Markdown skill repos — the loop structure transfers, the speedup numbers do not. Subagent-based trigger/behavior evals inherit judge noise; treat single failures as directional (existing repo practice) and use majority-of-3 only for final-round decisions. The textual-feedback requirement is the load-bearing part; a scalar-only harness forfeits the mechanism. Re-verify if gepa package semantics change (integration moving from `gepa` package into DSPy core).

## Sources

**Tier 1 (maintainer-authored, required)**
- [GEPA paper (arXiv 2507.19457, ICLR 2026 Oral)](https://arxiv.org/abs/2507.19457) — reflect/mutate/combine loop; Pareto frontier; textual feedback thesis; headline numbers
- [gepa-ai/gepa repository README](https://github.com/gepa-ai/gepa) — five-step loop; Actionable Side Information; works with as few as 3 examples; budget stopping
- [DSPy docs: GEPA overview](https://dspy.ai/api/optimizers/GEPA/overview/) — metric returns (score, feedback); trainset/valset roles; Pareto selection returns best-validation candidate
- [DSPy docs: GEPA optimization guide](https://dspy.ai/getting-started/gepa-optimization/) — smallest-representative valset; reflection_lm sizing; stopping modes
- [agentskills.io: Optimizing skill descriptions](https://agentskills.io/skill-creation/optimizing-descriptions) — 20-query recipe, near-misses, 60/40, 3-run trigger rate, 5-iteration stopping
- [agentskills.io: Evaluating skill output quality](https://agentskills.io/skill-creation/evaluating-skills) — with/without baseline, concrete evidence, blind A/B, lean iteration, stopping on empty feedback
- [Anthropic docs: Define success criteria and build evaluations](https://platform.claude.com/docs/en/test-and-evaluate/develop-tests) — ≥20 test cases; 2–5 samples majority vote; rubric grading options
- [Anthropic engineering: Demystifying evals for AI agents](https://www.anthropic.com/engineering/demystifying-evals-for-ai-agents) — dual-sided datasets; pass^k; judge calibration; outcome grading
- [OpenAI: Evals guide](https://platform.openai.com/docs/guides/evals) — grader types; thresholds before running; iteration flow

**Tier 2 (supplementary only, never sole evidence)**
- [promptfoo: CI/CD](https://www.promptfoo.dev/docs/integrations/ci-cd/) and [model-graded assertions](https://www.promptfoo.dev/docs/configuration/expected-outputs/model-graded/) — temperature-0 graders; threshold gates blocking merges
- [LangSmith: Evaluation concepts](https://docs.langchain.com/langsmith/evaluation-concepts) and [improving judge feedback](https://docs.langchain.com/langsmith/improve-judge-evaluator-feedback) — 10–20 seed examples; judge alignment score; train/val/test splits
- [Braintrust: Evals guide](https://www.braintrust.dev/docs/guides/evals) — data/task/scorer triad; playground→experiment→CI→production loop
