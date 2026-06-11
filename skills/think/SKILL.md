---
name: think
description: "Brainstorm and converge on solutions. Diverge on possibilities, converge on concrete plan, generate initial PRD. Use when requirements unclear, multiple implementation paths, or user describes new feature or complex task."
when_to_use: "brainstorm,构思,plan,how should I,design approach,feasibility,技术方案"
dispatch_intent: "New feature, architecture decision, requirements discovery, executable plan"
---

# Think: Brainstorm and Solution Convergence

🥷 Think before you code.

Transform rough ideas into decision-complete plans. Do not write code, generate scaffolds, or write pseudocode until user explicitly starts an implementation workflow.

## Outcome Contract

- **Outcome**: Decision-complete plan. Optionally persisted as a PRD with clear requirements, acceptance criteria, technical approach, and implementation plan
- **Done when**: User approves plan and (optionally) PRD is created for `/grill`
- **Evidence**: Updated `docs/prd/<feature-name>.md` (if user opts to create PRD), or approved design summary
- **Output**: Approved design summary with next step to `/grill`

## Core Principles

1. **Task-first**: Capture idea immediately
2. **Action-before-asking**: Derive from codebase/docs before asking
3. **One question per message**: Ask one, update PRD, repeat
4. **Prefer concrete options**: Present 2-3 viable approaches with trade-offs
5. **Research-first for technical choices**: Study industry conventions before proposing
6. **Diverge → Converge**: Expand on future/edge cases, then converge to MVP
7. **No meta questions**: Never ask "should I search?"

## Process Summary

**Step 0**: Quick assessment — if Trivial (typo, single-line fix), recommend `/tdd` or direct implementation and stop

**Step 0.5**: Ask user if they want to create a PRD — don't create one automatically

**Step 1**: Auto-collect context from codebase and docs before asking

**Step 2**: Classify complexity (Simple/Moderate/Complex)

**Step 3**: Gate questions — only ask blocking or preference questions

**Step 4**: Research-first mode for technical choices (present approaches after research)

**Step 5**: Expansion scan on future evolution, related scenarios, failure/edge cases

**Step 6**: Q&A loop — one question at a time, update PRD (if created) after each answer

**Step 7**: Propose approaches + record decision as ADR-lite (in PRD if created)

**Step 8**: Final confirmation with implementation plan; stop after approval

**Step 9**: Create Issue (optional)

See [REFERENCE.md](REFERENCE.md) for detailed templates and examples.

Shared behavioral constraints: apply [../rules/anti-patterns.md](../rules/anti-patterns.md) when a global anti-pattern is relevant.

## Gotchas

| What happened | Rule |
|---|---|
| Created PRD without asking user first | Step 0.5: Ask before creating PRD |
| Asked user about code/context that could be derived | Step 1: Auto-collect context first |
| Had user choose approach before presenting options | Step 4: Research-first for technical choices |
| Asked meta questions like "should I search?" | Step 3: Use question gates |
| Drifted without updating PRD | Update PRD after every answer |
| Stayed on initial request without considering edges | Step 5: Expansion scan before converging |

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
