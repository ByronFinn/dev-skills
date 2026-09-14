# agentskills: Skill Authoring Best Practices

> **Stack**: agentskills@unknown (unversioned open standard; open-standard release announced 2025-12-18)  | **Major**: 1  | **Verified**: 2026-09-14  | **Status**: verified

## TL;DR

Follow the spec mechanics exactly (name ≤64 chars lowercase-hyphen matching the directory; description 1–1024 chars carrying what+when with trigger keywords; SKILL.md <500 lines with detail pushed to referenced files) and the official authoring guidance: description carries the entire triggering burden, tell the agent **when** to load each referenced file, gotchas and defaults-not-menus beat exhaustive declarations, cut any instruction the model would get right anyway. Evaluate with the official two-track method — 20-query trigger evals (should-trigger + near-miss, 60/40 split) and with/without-skill output evals on 2–3 cases. Trade-off: description limits differ per surface (spec 1024 hard / Claude Code 1536 combined / Gemini 500), so stay under the strictest common denominator.

## Question

What do the authoritative sources (agentskills.io spec + Anthropic/OpenAI/Google official docs) prescribe for writing and evaluating agent skills (SKILL.md) as of 2026-09?

## Approach

Fetched and read the agentskills.io specification and its four skill-creation guides (best-practices, optimizing-descriptions, evaluating-skills, using-scripts), Anthropic's platform docs "Skill authoring best practices", the Claude Code skills reference, Anthropic's engineering post "Equipping agents for the real world with Agent Skills" (Dec 2025 update note), the official `anthropics/skills` skill-creator SKILL.md, OpenAI Codex skills docs, and Gemini CLI skills docs. Cross-tabulated every stated rule; divergences recorded in Findings. Spec has no version number — date-anchored to the 2025-12-18 open-standard announcement.

## Findings

| Rule | Spec (agentskills.io) | Anthropic docs/blog | Claude Code | skill-creator | Codex | Gemini CLI |
|---|---|---|---|---|---|---|
| `name` ≤64 chars, `[a-z0-9-]`, matches dir | required | ✔ | ✔ | ✔ | ✔ | ✔ |
| `description` 1–1024 chars, what+when, keywords | required (1024 hard) | 100–200 chars target | key use case first; 1536 combined w/ when_to_use | "pushy", all when-to-use here | clear scope+boundaries | ≤500 chars |
| Progressive disclosure: metadata → body → files | 3 levels (~100 tok / <5k tok) | 4th level: external tools | persists; no re-read on later turns | ~100 words / <500 lines | metadata-only at session start | ~100 / <5k words |
| SKILL.md <500 lines; detail in referenced files | ✔ | ✔ | ✔ | ✔ + TOC for >300-line files | ✔ | ✔ |
| Tell agent WHEN to read each referenced file; shallow hierarchy | ✔ (one level deep ideal) | ✔ | ✔ | ✔ | ✔ | ✔ |
| Don't restate what the model already knows | ✔ | ✔ | ✔ | ✔ | — | ✔ |
| Defaults not menus; imperative procedures | ✔ | — | ✔ | ✔ | ✔ | ✔ |
| Avoid rigid ALWAYS/NEVER; explain why instead | named pitfall | — | — | "yellow flag" | — | — |
| Evaluation: trigger evals + output evals | ✔ (20 queries, near-miss, 60/40, 3 runs) | start from evaluation | `claude plugin eval`, invoke + output measured separately | ✔ (same 20-query recipe) | test prompts vs description | test and iterate |
| Versioning | `metadata.version` only | — | accepts spec fields | — | — | SKILL_VERSION constant |

Key divergences: `disable-model-invocation` is a **Claude Code extension, not in the spec** (Codex equivalent: `agents/openai.yaml` `allow_implicit_invocation: false`); description length limits differ per surface. Evaluation recipe (convergent): ~20 queries (8–10 should-trigger + 8–10 should-not, near-misses the most valuable negatives), 3 runs each with trigger-rate threshold 0.5, 60/40 train/validation split, never keyword-patch failures, ~5 iterations, select by held-out score; output evals run with-vs-without the skill in clean contexts, assertions need concrete evidence, blind A/B between versions.

**Confirmed absence:** none of the official sources prescribe question pacing for interactive/interviewing skills — the only adjacent statements are skill-creator's creation-time interview questions (no pacing rule) and using-scripts' "avoid interactive prompts" (about non-interactive shells, not conversation).

## Verdict & Rationale

Adopt the spec mechanics and the official authoring/evaluation recipe as this repo's compliance bar: name/description-only frontmatter, description as the sole trigger surface (<1024 chars, intent-first, bilingual keywords, near-miss tested), SKILL.md <500 lines opening with the outcome contract, conditional file references with explicit when-to-read, gotchas tables, defaults-not-menus, explain-why over rigid MUSTs, TOC for reference files >300 lines, and the two-track evaluation method with train/holdout discipline. Rationale: every convergent rule above is stated by the spec or ≥2 official vendor docs (Tier 1); the repo's existing conventions (AGENTS.md File Conventions, rules/writing-skills.md) already encode most of it, so the delta is measurable compliance checks plus the evaluation harness.

## Boundary Conditions

Anchored to the unversioned spec as of 2026-09 (post 2025-12-18 open-standard release); re-verify if the spec gains a version/changelog. `disable-model-invocation` guidance applies to Claude Code-family runtimes only (spec portability: six allowed fields — name, description, license, compatibility, metadata, allowed-tools; extra fields hard-fail packaging). Not sensitive to minor changes.

## Sources

**Tier 1 (maintainer-authored, required)**
- [agentskills.io: Agent Skills Specification](https://agentskills.io/specification) — frontmatter fields, limits, progressive disclosure, 500-line guidance, file references
- [agentskills.io: Best practices for skill creators](https://agentskills.io/skill-creation/best-practices) — scoping, defaults-not-menus, gotchas, when-to-load guidance, trace-based iteration
- [agentskills.io: Optimizing skill descriptions](https://agentskills.io/skill-creation/optimizing-descriptions) — pushy descriptions, 20-query recipe, near-misses, 60/40 split, 3-run trigger rate
- [agentskills.io: Evaluating skill output quality](https://agentskills.io/skill-creation/evaluating-skills) — with/without baseline, concrete-evidence assertions, blind A/B, lean-skill iteration
- [Anthropic docs: Skill authoring best practices](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices) — description-first, evaluation-driven workflow, token budgets
- [Claude Code docs: Skills reference](https://code.claude.com/docs/en/skills) — frontmatter semantics, disable-model-invocation, 1536-char combined limit, eval tooling
- [Anthropic engineering: Equipping agents for the real world with Agent Skills](https://www.anthropic.com/engineering/equipping-agents-for-the-real-world-with-agent-skills) — progressive disclosure rationale, start-with-evaluation
- [anthropics/skills: skill-creator SKILL.md](https://raw.githubusercontent.com/anthropics/skills/main/skills/skill-creator/SKILL.md) — yellow-flag rule, TOC for >300-line files, interview process (no pacing rule)
- [OpenAI Codex docs: Skills](https://developers.openai.com/codex/skills/) — implicit matching depends on description; policy metadata
- [Gemini CLI docs: Skills best practices](https://geminicli.com/docs/cli/skills-best-practices) — ≤500-char description, design-for-discovery

**Tier 2 (supplementary only, never sole evidence)**
- [agentskills.io: Using scripts in skills](https://agentskills.io/skill-creation/using-scripts) — non-interactive script requirement (adjacent to, not about, conversational questioning)
