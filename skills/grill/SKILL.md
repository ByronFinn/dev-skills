---
name: grill
description: "Challenge plans and update domain knowledge. Interview relentlessly about plan aspects, walk down design branches, resolve dependencies one-by-one. Use after think to validate plan against existing domain model, sharpen terminology, update CONTEXT.md and ADRs."
when_to_use: "challenge,细化和验证,deep dive,question the plan,grill"
dispatch_intent: "Plan validation, domain model consistency, terminology sharpening"
---

# Grill: Challenge Plans and Update Domain Knowledge

🥷 Challenge the plan before coding.

Interview relentlessly about every aspect of this plan until we reach shared understanding. Walk down each branch of the design tree, resolving dependencies between decisions one-by-one. For each question, provide your recommended answer.

## Outcome Contract

- **Outcome**: Validated PRD aligned with domain model, updated CONTEXT.md, relevant ADRs created
- **Done when**: User confirms plan, terminology resolved, ADRs created for significant decisions
- **Evidence**: Updated PRD, CONTEXT.md with new/sharpened terms, ADRs for hard-to-reverse decisions
- **Output**: Synced GitHub Issue (if exists), updated local files, next step to `/story`

## Domain Structure

**Single context:** `CONTEXT.md` + `docs/adr/`

**Multiple contexts** (if CONTEXT-MAP.md exists): system-wide `docs/adr/` + context-specific `src/*/CONTEXT.md` + `src/*/docs/adr/`

Create files lazily — only when you have something to write.

## Process Summary

**Step 1**: Read PRD at `docs/prd/<feature-name>.md`

**Step 2**: Check existing domain model (CONTEXT.md, docs/adr/)

**Step 3**: Interview challenges — one question at a time, wait for feedback

**Step 4**: Challenge glossary — call out conflicting terms immediately

**Step 5**: Sharpen fuzzy language — propose precise canonical terms

**Step 6**: Discuss concrete scenarios — stress-test with edge cases

**Step 7**: Cross-check with code — verify code matches stated behavior

**Step 8**: Update CONTEXT.md inline as terms resolve

**Step 9**: Offer ADRs sparingly (only when: hard to reverse + surprising + real trade-off)

**Step 10**: Update PRD with interview results

**Step 11**: Sync GitHub Issue (if exists)

See [REFERENCE.md](REFERENCE.md) for CONTEXT-FORMAT.md and ADR-FORMAT.md.

Shared behavioral constraints: apply [../rules/anti-patterns.md](../rules/anti-patterns.md) when a global anti-pattern is relevant.

## Gotchas

| What happened | Rule |
|---|---|
| Conflict with existing terminology | Step 4: Call out immediately |
| Used fuzzy terms | Step 5: Propose precise canonical term |
| Code contradicts statement | Step 7: Cross-check with code |
| Batched term updates | Step 8: Update CONTEXT.md immediately |
| Over-creation of ADRs | Step 9: Only when all 3 conditions met |
| PRD went stale | Step 10: Update PRD after interview |
| Issue content outdated | Step 11: Sync GitHub Issue |

## Output

```
Grill complete.

Updated files:
- docs/prd/<name>.md — updated
- CONTEXT.md — updated (new/sharpened terms)
- docs/adr/xxx.md — created (if any)

GitHub Issue synced:
- #<issue-number> — updated

Next: Run /story to break PRD into Issues.
```

Keep CONTEXT.md devoid of implementation details. It is a glossary, nothing more.
