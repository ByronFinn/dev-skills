# Skills Optimization Campaign — Final Report (2026-09-14)

Owner-mandated campaign: optimize the skill set to full best-practice compliance under a GEPA-style evaluation loop (≥50 iterations, data-driven, no user questions mid-run). Framework: [skills-eval.md](../skills-eval.md). Evidence base: [docs/research/](../../research/) (3 records). All iteration logs: [iteration-NNN.json](.) + [scoreboard.csv](scoreboard.csv).

## Headline numbers

| Metric | Baseline (iter 0) | Final (iter 50) | Delta |
|---|---|---|---|
| Level S hard (static compliance) | 176/190 (92.6%) | **216/216 (100%)** | +40 checks-worth of compliance; check set also grew 190→216 |
| Level S soft | 23/24 | **74/74 (100%)** | check set grew 24→74 |
| Level W (workflow coherence) | 32/32 | **36/36 (100%)** | +4 new checks (README coverage, step-ref validity, INDEX consistency), all green |
| T-Live routing (sub-agent, fresh context) | — (12-query manual harness, last round 10/12) | **20/20 (train 12/12, holdout 8/8)** | +8 holdout queries; 0 mis-routes |
| B behavior: one-question-per-message | batch model by design (grill rounds; story 4-question batch) | **100% across 22 simulated turns (4 scenarios)** | doctrine inverted and held on unseen scenarios |
| B behavior: adaptivity (next question from last answer) | not required by old model | **100% of applicable turns** | |
| B behavior: code-answerable asked to user | 1 violation in train scenario | **0 across all scenarios** | |
| check-docs.py | pass | pass | invariant gate held throughout |

## What changed (by evidence source)

1. **Owner mandate → one-by-one doctrine** (research record `agent-interviewing-question-pacing-1`): grill reworked from round/frontier batches to one-question-per-message adaptive tree-walk; think given the same contract plus no-piggyback-riders and approval-purity rules; anti-patterns #3/#4 inverted (numbers frozen); story's two batch-question instructions converted; setup-project's batching reframed as destructive-op authorization with an explicit boundary.
2. **Behavior simulation traces → 3 behavioral fixes**: ADR-eligibility re-litigation at completion (grill, from G1 trace); piggyback riders on selection questions and approval submissions (think, from T1 traces t2/t4). All three re-verified post-fix (checkpoint 2) and held on holdout scenarios never seen by the fixes (checkpoint 3), including the honest-gate case: refusing to mark Grilled with nodes unresolved.
3. **Static suite → structural fixes**: TOCs for 4 reference files >300 lines; intent-first phrasing in 4 descriptions; grill's orphaned CONTEXT-FORMAT.md pointer; per-skill hard gates now enforce the whole authoring bar.
4. **Three parallel read-only audits → 37 findings**, all actionable ones fixed (iterations 8–11): SKILL↔REFERENCE contradictions (tdd Batch gate count vs ADR-0003, gate-mode offer timing, Sub-Agent Common scope; review Ch5 false cross-reference; implement "Dispatch /review" heading vs no-auto-chain), #38 restatements trimmed (runtime notes, session recovery, independence boilerplate), no-op instructions deleted (tdd Per-Cycle Checklist, review "Don't assume"), PRD-FORMAT phantom field + missing `Sliced by` field, RESOLVER row corrections, stale references (Step 10a/10, writing-skills probe-harness location, retired "frontier" term).

## Evaluation artifacts shipped

- `scripts/eval_skills.py` — deterministic harness (stdlib only), per-check textual feedback, JSON+CSV logging, non-zero exit as regression gate. Determinism verified (double-run identical).
- `scripts/evals/trigger-queries.json` — 20 queries, 60/40 train/holdout, near-miss weighted.
- `scripts/evals/behavior-scenarios.json` — 4 scenarios (train+holdout per interviewing skill) with mock repos, scripted adaptive answers, code-answerable traps.
- `docs/evals/skills-eval.md` — the framework spec (levels, splits, judge rubric incl. approval-submission exemption, decision rules, known limitations).
- Checkpoints 1–3 + trigger-final JSON; scoreboard.csv; this report.

## Known limitations (honest)

- T-Proxy (lexical) remains weak on CJK synonymy (e.g. 任务票→story) — documented as drift-detection only; T-Live is ground truth and is 20/20. Per the anti-overfitting rule, descriptions were NOT keyword-patched for proxy-only misses.
- T-Live/B are 1-run-per-query/probe (documented deviation from the 3-run recommendation); single failures directional; all verdicts carry quoted evidence for audit.
- B scenarios exercise the conversation contract, not filesystem side effects.
- Iterations after convergence (23–49) are hold-steady confirmation runs with no changes (feedback empty — GEPA's stopping condition); they were run to satisfy the owner's ≥50-iteration mandate and are labeled as such in the scoreboard.

## Verdict

All evaluation levels green at final state; every defect found by any level was fixed and its fix verified (same-scenario re-run and/or holdout generalization). The final state is the best-holdout candidate of the campaign, not merely the last one.
