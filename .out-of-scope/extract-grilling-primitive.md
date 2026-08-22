# Extract `grilling` / `domain-modeling` as reusable primitive skills

Extracting the interview discipline (rounds, frontier, recommended answers) and the domain-modeling discipline (CONTEXT.md/ADR updates) from `grill`/`think` into standalone model-invoked primitive skills, composed via Skill-tool calls — the pattern mattpocock/skills uses (`grilling` reused by 5 skills, `grill-with-docs` is a 7-line shell).

## Why deferred (2026-08-22)

- **The test for extraction is reuse, and the consumers don't exist yet.** In this repo only `grill` and `think` run interviews; `think`'s question gating already differs (Blocking/Preference) from grill's dependency-chain pacing. Two consumers with divergent needs is evidence *for* keeping them separate, not for a shared primitive.
- **Composition depends on harness support** for skill-invoking-skill, which varies across agents this repo targets; the current monolith-with-shared-`rules/` design is harness-neutral.
- **Cost is real**: a new always-loaded description (context load) plus a migration touching grill, think, RESOLVER, and their REFERENCEs.

## Revisit when

A third skill needs the interview discipline (e.g. a future triage or wayfinder-style skill that grills users about incoming issues, or setup-project adopting an interview-driven flow). At that point extract `grilling` as model-invoked with the round format from grill/REFERENCE.md §Question Pacing, and link (not copy) from consumers.
