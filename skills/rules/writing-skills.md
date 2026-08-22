# Writing Skills: Shared Authoring Discipline

Rules for writing and editing any document an agent consumes — `SKILL.md`, `REFERENCE.md`, `*FORMAT.md`, `description` fields. Apply when creating or changing a skill. Distilled from mattpocock/skills' `writing-for-agents`, the [agentskills.io spec](https://agentskills.io/specification), and this repo's own audits.

## The two loads

Every line you add spends one of two budgets:

- **Context load** — always-loaded material (`description` sits in every session; SKILL.md loads on trigger). Paid by the agent, on every turn.
- **Cognitive load** — the human's memory of which skills exist and when to reach for each. Paid by the user.

Neither is free; the design job is spending each where it earns. A `description` trigger list helps routing (spends context) but spares the user from typing slash commands (saves cognitive). A user-invoked skill (`disable-model-invocation: true`) pays zero context but full cognitive load. Test for model-invocation: *could the model usefully reach for this autonomously, or must another skill call it?* If neither, make it user-invoked. Reuse alone is not the test.

## Description fields

The `description` carries the entire triggering burden (spec: progressive disclosure loads `name + description` first). Per [optimizing descriptions](https://agentskills.io/skill-creation/optimizing-descriptions):

- **Imperative, intent-first**: "Use when the user wants…", describe the user's goal, not the skill's internals.
- **Front-load the leading word**; one trigger per branch — synonyms renaming one case are one branch written twice, collapse them.
- **Pushy beats terse**: list contexts where it applies even if the user doesn't name the domain; but stay under ~1024 chars.
- **Test with near-misses**: 8–10 should-trigger + 8–10 near-miss queries (share keywords but need a different skill, or need none). A negative example that shares no vocabulary tests nothing. The probe harness and query sets live in `docs/evals/` — run a probe round when changing any description.

Trigger words may be Chinese or English; route matching needs both (see RESOLVER.md).

## Information hierarchy

Three tiers, ranked by how immediately the agent needs the material:

1. **In-file steps** (SKILL.md process sections) — what the agent does, in order.
2. **In-file reference** (Gotchas tables, rules) — consulted on demand.
3. **Disclosed reference** (REFERENCE.md, `*FORMAT.md`, `references/`) — loaded only via a pointer.

The disclosure test: **inline what every branch needs; push behind a pointer what only some branches reach.** Push too little and SKILL.md bloats past ~140 lines; push too much and you hide material the agent actually needs. Keep each meaning in **one source of truth** — cross-skill rules live once in `rules/` and are linked, never restated (anti-pattern #38). Co-locate a concept's definition, rules, and caveats under one heading.

## Structure contract

Every SKILL.md opens with its **Outcome Contract** before any procedure (anti-pattern #30), then process, Gotchas table, output template. Every step and every outcome ends on a **completion criterion** with two properties:

- **Clarity** — can the agent tell done from not-done? A vague bound ("understanding reached") invites premature completion.
- **Demand** — how much work it forces. "Every modified model accounted for" drives legwork; "produce a change list" does not.

## Wording

- **Leading words**: prefer a compact pretrained word (_seam_, _frontier_, _tracer bullet_) over a spelled-out phrase; it anchors a region of behaviour in one token. A made-up word recruits no priors — define it or find the existing one.
- **Positive phrasing**: state the target behaviour; a prohibition drags the forbidden behaviour into context ("don't think of an elephant"). Prohibitions earn their place only as hard guardrails that cannot be phrased positively.
- **No-ops**: an instruction the model already obeys by default pays load to say nothing. Test: does it change behaviour versus the default? When a sentence fails, delete the whole sentence.
- **The environment is a source of truth**: package.json, config files, directory layout, `--help`. A document restating it is a cache — earns its load only when the lookup is expensive. Cache the unwritten convention and the reason behind a choice, not what one command would reveal.

## Pruning

Shorter documents are easier to keep relevant. The default fate of an unpruned doc is **sediment** — stale layers that settle because adding feels safe and removing feels risky. When editing a skill, hunt: restatements a leading word retires, branches that should be disclosed, rules with no citing consumer (archive, don't carry), facts the environment already holds. See `rules/anti-patterns.md` Archive for the consumer rule.
