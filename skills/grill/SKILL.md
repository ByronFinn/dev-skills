---
name: grill
description: "Challenge plans by extracting every open decision from the PRD and resolving them one by one — skip none. Interview relentlessly about every aspect of the plan, walking down each branch of the design tree until shared understanding is reached. Use after think to validate plan against existing domain model, sharpen terminology, update CONTEXT.md and ADRs."
when_to_use: "challenge,细化和验证,deep dive,question the plan,grill,validate plan,这个方案行不行,审查设计,find holes,stress test"
dispatch_intent: "Plan validation, domain model consistency, terminology sharpening"
---

# Grill: Challenge Plans and Update Domain Knowledge

🥷 Challenge the plan before coding.

Interview me relentlessly about every aspect of this plan until we reach shared understanding. Walk down each branch of the design tree, resolving dependencies between decisions one-by-one. For each question, provide your recommended answer.

Ask decision-tree questions one at a time — each question's answer may change how you frame the next one (this is not serial interrogation; see anti-pattern #3 exception for dependency-chain questions).

**Batch independent questions.** When multiple open decisions are independent — the answer to one does not affect how you frame the others — batch them in groups of 2-3 in a single message. Reserve one-at-a-time for genuine dependency chains where each answer reshapes the next question.

If a question can be answered by exploring the codebase, explore the codebase instead.

Before starting, read domain doc layout from `docs/agents/domain.md` (if exists) to locate `CONTEXT.md` and ADR paths. Read `docs/agents/repo-map.md` (if exists) to identify cross-repo domain model and ADRs. Then read the PRD at `docs/prd/<feature-name>.md`. If no PRD exists or it's too thin, suggest running `/think` first. Extract every open decision, unresolved assumption, vague term, and scope boundary into a mental checklist. Work through the checklist — skip none. Do not declare grill complete until every item is resolved.

## Outcome Contract

- **Outcome**: Validated PRD aligned with domain model, updated CONTEXT.md, relevant ADRs created
- **Done when**: User confirms plan, all terminology resolved, ADRs created for significant decisions
- **Evidence**: Updated `docs/prd/<feature-name>.md`, CONTEXT.md with new/sharpened terms, ADRs for hard-to-reverse decisions
- **Output**: Synced Issue (if exists), updated local files, next step to `/story`

## File Structure

Most repos have a single context:

```
/
├── CONTEXT.md
├── docs/
│   └── adr/
│       ├── 0001-event-sourced-orders.md
│       └── 0002-postgres-for-write-model.md
└── src/
```

If a `CONTEXT-MAP.md` exists at the root, the repo has multiple contexts:

```
/
├── CONTEXT-MAP.md
├── docs/
│   └── adr/                          ← system-wide decisions
├── src/
│   ├── ordering/
│   │   ├── CONTEXT.md
│   │   └── docs/adr/                 ← context-specific decisions
│   └── billing/
│       ├── CONTEXT.md
│       └── docs/adr/
```

Create files lazily — only when you have something to write. If no `CONTEXT.md` exists, create one when the first term is resolved. If no `docs/adr/` exists, create it when the first ADR is needed.

## Document Update Rules

### CONTEXT.md — Update Inline

When a term is resolved, update `CONTEXT.md` right there. Don't batch these up — capture them as they happen. Use the format in [CONTEXT-FORMAT.md](CONTEXT-FORMAT.md).

`CONTEXT.md` should be totally devoid of implementation details. Do not treat it as a spec, a scratch pad, or a repository for implementation decisions. It is a glossary and nothing more.

### ADRs — Offer Sparingly

Only offer to create an ADR when all three are true:

1. **Hard to reverse** — the cost of changing your mind later is meaningful
2. **Surprising without context** — a future reader will wonder "why did they do it this way?"
3. **The result of a real trade-off** — there were genuine alternatives and you picked one for specific reasons

If any of the three is missing, skip the ADR. Use the format in [ADR-FORMAT.md](ADR-FORMAT.md).

### PRD & Issue

Update PRD at `docs/prd/<feature-name>.md` with interview results — corrected technical approach, updated requirements, adjusted acceptance criteria, updated in/out scope. Sync Issue if one exists.

## Gotchas

| What happened | Rule |
|---|---|
| Skipped an unresolved assumption | Checklist: extract all open items first, resolve each one |
| Updated CONTEXT.md in batch at end | Update inline, as each term resolves |
| Created ADR for a trivial decision | Only when all 3 conditions met |
| CONTEXT.md contains implementation details | It is a glossary, nothing more |
| PRD not updated after interview | Update `docs/prd/<feature-name>.md` before declaring complete |

Shared behavioral constraints: apply [../rules/anti-patterns.md](../rules/anti-patterns.md) when a global anti-pattern is relevant.

## Output

```
Grill complete.

Updated files:
- docs/prd/<feature-name>.md — updated
- CONTEXT.md — updated (new/sharpened terms)
- docs/adr/xxx.md — created (if any)

Issue synced:
- #<issue-number> — updated

Next step:
- If scope changed significantly (new major requirements, fundamental approach change): Run /think to re-evaluate the full design.
- If plan validated with refinements only: Run /story to break PRD into Issues.
```
