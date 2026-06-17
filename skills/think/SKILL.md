---
name: think
description: "Brainstorm and converge on solutions. Diverge on possibilities, converge to concrete plan, generate initial PRD. Use when requirements unclear, multiple implementation paths, or user describes new feature or complex task."
when_to_use: "brainstorm,构思,plan,how should I,design approach,feasibility,技术方案"
dispatch_intent: "New feature, architecture decision, requirements discovery, executable plan"
---

# Think: Brainstorm and Solution Convergence

🥷 Think before you code.

Transform rough ideas into decision-complete plans. Ask one question at a time, each with your recommended answer. Do not write code, generate scaffolds, or write pseudocode until the user explicitly starts an implementation workflow.

If a question can be answered by exploring the codebase or a quick research pass, do that instead of asking.

## Outcome Contract

- **Outcome**: Decision-complete plan. Optionally persisted as a PRD with clear requirements, acceptance criteria, technical approach, and implementation plan
- **Done when**: User approves plan and (optionally) PRD is created for `/grill`
- **Evidence**: Updated `docs/prd/PRD-NNNN-<title>.md` (if user opts to create PRD), or approved design summary
- **Output**: Approved design summary with next step to `/grill`

## Core Principles

1. **Task-first** — capture the idea immediately
2. **Action-before-asking** — derive from codebase/docs before asking. Apply the [Skill Entry Protocol](../rules/entry-protocol.md) to locate existing domain docs and prior PRDs
3. **One question at a time** — each with a recommended answer; update the PRD after each
4. **Prefer concrete options** — present 2-3 viable approaches with trade-offs
5. **Research-first for technical choices** — study industry conventions before proposing
6. **Diverge → Converge** — expand on future/edge cases, then converge to MVP

## Process Summary

**Step 0 — Quick assessment.** If the request is Trivial (typo, single-line fix, one obvious approach), tell the user `/think` is unnecessary, recommend direct implementation or `/tdd`, and stop. No PRD created.

**Step 1 — Auto-collect context.** Explore the codebase (affected modules, existing patterns, constraints) and docs (prior PRDs, README, ADRs) before asking anything. Write findings into the PRD's `What I already know` and `Technical Notes`.

**Step 2 — Offer to create a PRD.** Ask whether to persist the plan as `docs/prd/PRD-NNNN-<title>.md`. By now you have enough context to explain what the PRD would contain — the user decides with findings in hand. Don't create one automatically. If declined, work conversationally and produce a summary at the end. When creating: scan `docs/prd/` for existing `PRD-NNNN-*.md` files, assign next NNNN (max + 1, starting from 0000).

**Step 3 — Classify complexity.** Simple / Moderate / Complex (see REFERENCE.md). Depth of brainstorming scales with complexity.

**Step 4 — Gate your questions.** Only ask **Blocking** (can't continue without input) or **Preference** (multiple valid choices) questions. Derivable questions → inspect the code/research instead. Meta questions ("should I search?") → never ask, just act.

**Step 5 — Research-first for technical choices.** When the task involves choosing an approach/library/framework, research 2-4 comparable patterns first, map to codebase constraints, then present 2-3 options with trade-offs and ask one preference question.

**Step 6 — Expansion scan (diverge).** Proactively raise 1-2 points each on future evolution, related scenarios, and failure/edge cases before converging. Let the user pick what enters the MVP vs `Out of Scope`.

**Step 7 — Q&A loop (converge).** One question at a time. After each answer, immediately update the PRD: move resolved items from `Open Questions` to `Requirements`, sharpen `Acceptance Criteria`, clarify `Out of Scope`.

**Step 8 — Propose approaches + record decision.** When requirements are clear, present 2-3 approaches (if not already done via research), ask preference, and record the result in the PRD's `Decision (ADR-lite)` section.

**Step 9 — Final confirmation + implementation plan.** Present the complete requirements (Goal, Requirements, Acceptance Criteria, Definition of Done, Out of Scope, Technical Approach, small-PR implementation plan). Stop after approval. Optionally create a parent Issue and record new domain terms for `/grill` to refine.

See [REFERENCE.md](REFERENCE.md) for the PRD template, complexity classification detail, question-gate rules, and worked message formats.

Shared behavioral constraints: apply [../rules/anti-patterns.md](../rules/anti-patterns.md) when a global anti-pattern is relevant.

## Gotchas

| What happened | Rule |
|---|---|
| Created PRD without asking user first | Step 2: ask before creating PRD |
| Asked user about code/context that could be derived | Step 1: auto-collect context first |
| Had user choose approach before presenting options | Step 5: research-first for technical choices |
| Asked meta questions like "should I search?" | Step 4: never ask, take action |
| Drifted without updating PRD | Update PRD after every answer |
| Stayed on initial request without considering edges | Step 6: expansion scan before converging |
| Domain terms introduced but not recorded for grill | Step 9: record new terms in PRD `## Domain Terms` section |

## Output

When plan is approved, output:

```
Plan approved. Next: Run /grill to challenge and refine this approach.
```

**Approved design summary:**
- **Building**: What this is (1 paragraph)
- **Not building**: Explicit exclusion list
- **Approach**: Chosen option + rationale
- **Key decisions**: 3-5 items with rationale
- **Unknowns**: Only explicitly deferred items with reason and owner

Stop after approval. Implementation only starts on request.
