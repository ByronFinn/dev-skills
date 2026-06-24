---
name: grill
description: "Challenge plans by extracting every open decision from the PRD and resolving them one by one — skip none. Interview relentlessly about every aspect of the plan, walking down each branch of the design tree until shared understanding is reached. Use after think to validate plan against existing domain model, sharpen terminology, update CONTEXT.md and ADRs."
when_to_use: "challenge,细化和验证,deep dive,question the plan,grill,validate plan,这个方案行不行,审查设计,find holes,stress test"
dispatch_intent: "Plan validation, domain model consistency, terminology sharpening"
---

# Grill: Challenge Plans and Update Domain Knowledge

🥷 Challenge the plan before coding.

Interview me relentlessly about every aspect of this plan until we reach shared understanding. Walk down each branch of the design tree, resolving dependencies between decisions one-by-one. For each question, provide your recommended answer.

Ask the questions one at a time — a question's answer often changes how you frame the next one (this is a dependency chain, not serial interrogation; see anti-pattern #3 and #3a).

If a question can be answered by exploring the codebase, explore the codebase instead.

## Outcome Contract

- **Outcome**: Validated PRD aligned with the domain model, CONTEXT.md sharpened, significant decisions recorded as ADRs
- **Done when**: Every open decision resolved, terminology consistent with CONTEXT.md, ADRs created where the 3 conditions are met
- **Evidence**: Updated `docs/prd/PRD-NNNN-<title>.md` (status → Grilled), updated `CONTEXT.md`, created `docs/adr/<NNNN>-*.md` (where warranted)
- **Output**: Parent Issue synced (if created by `/think`), next step to `/story`

## Before You Start

Apply the [Skill Entry Protocol](../rules/entry-protocol.md) to locate domain docs and check upstream artifacts. Read the PRD at `docs/prd/PRD-NNNN-<title>.md` and `CONTEXT.md`. If no PRD exists or it's too thin, suggest `/think` first — don't grill vapor.

## The Work

1. **Extract everything unresolved.** Read the PRD with hostile eyes and pull out every open decision: Open Questions, unvalidated Assumptions, vague terms, unexplained scope boundaries, shaky technical approach, edge cases, conflicts with `CONTEXT.md`, behavior that contradicts the code. Skip none.
2. **Work the checklist one item at a time.** For each item: give your recommended answer first, then ask. Questions whose answers depend on each other stay one-at-a-time; if 2-3 items are genuinely independent, you may batch them in one message to save rounds.
3. **Resolve as you go, not in a batch at the end.** Update files inline the moment a decision lands:
   - **Terminology resolved** → update `CONTEXT.md` now (see [CONTEXT-FORMAT.md](CONTEXT-FORMAT.md)). CONTEXT.md is a glossary, nothing more — no implementation details.
   - **Significant decision** → offer an ADR only when all three are true: (1) hard to reverse, (2) surprising without context, (3) the result of a real trade-off. If any is missing, skip the ADR (see [ADR-FORMAT.md](ADR-FORMAT.md)).
   - **Code can answer it** → grep/read the code instead of asking the user.
4. **Run the exhaustiveness gate** before declaring complete: every Open Question resolved, every Assumption validated or converted, every term conflict addressed, every scope boundary confirmed, code cross-check done.
5. **Fill the PRD `## Traceability` `Grilled by` field** so downstream skills (story, tdd, review) know the plan was validated.
6. **Sync the parent Issue (if it exists).** The PRD `## Issue` field holds the parent Issue number created by `/think` (Step 9a, required). If present, update its body to reflect this grill's scope changes (sharpened terminology, confirmed scope boundaries, new ADRs). Do **not** change its title, do **not** close it. If the field is empty (e.g. minimal PRD from a direct `/story` path that skipped `/think`), skip — this skill does not create parent Issues; creation is `/think`'s responsibility.

## What Goes Where

| Situation | Action |
|---|---|
| Goal statement itself needs to change, or fundamental approach invalidated | Send back to `/think` — too big for grill |
| Only terminology sharpened, scope confirmed, approach validated with refinements | Proceed to `/story` |

For the challenge types (terminology conflict, fuzzy language, scope boundary, edge case, code cross-check), the file layout (single vs multi-context via `CONTEXT-MAP.md`), and a worked example, see [REFERENCE.md](REFERENCE.md).

Shared behavioral constraints: apply [../rules/anti-patterns.md](../rules/anti-patterns.md) when a global anti-pattern is relevant.

## Gotchas

| What happened | Rule |
|---|---|
| Skipped an unresolved assumption | Extract every open item first, then resolve each |
| Updated CONTEXT.md in a batch at the end | Update inline, the moment each term resolves |
| Created an ADR for a trivial decision | Only when all 3 conditions met |
| CONTEXT.md gained implementation details | It is a glossary, nothing more |
| Asked the user something the code could answer | Explore the codebase instead |
| PRD not updated after interview | Update `docs/prd/PRD-NNNN-<title>.md` and set `Status` to `Grilled` before declaring complete |
| Declared complete without the exhaustiveness gate | Run the 5-point gate first |
| Parent Issue body stale after grill changed scope | Sync the parent Issue (if `## Issue` field present) — reflect sharpened terms, scope, ADRs; don't change title or close |

## Output

```
Grill complete.

Resolved <N> items:
- <term>: <resolution>
- <assumption>: <validated/converted>
- <decision>: <ADR created | recorded in PRD>

Updated files:
- docs/prd/PRD-NNNN-<title>.md — updated (Status → Grilled)
- CONTEXT.md — <count> terms sharpened/added
- docs/adr/<NNNN>-<title>.md — created (if any)

Exhaustiveness gate: passed (Open Questions / Assumptions / Terms / Scope / Code all checked)

Parent Issue synced:
- #<issue-number> — updated (created by /think)
- (skipped — no parent, direct /story path with minimal PRD)

Next step:
- If scope changed significantly: /think to re-evaluate the full design
- If plan validated: /story to break PRD into Issues
```
