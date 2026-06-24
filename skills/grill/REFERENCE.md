# Grill: Detailed Reference

## File Layout

grill creates and updates domain docs. Where they live depends on the repo shape.

**Single context (most repos):**

```
/
├── CONTEXT.md
├── docs/
│   ├── adr/
│   │   ├── 0001-event-sourced-orders.md
│   │   └── 0002-postgres-for-write-model.md
│   └── prd/
│       └── PRD-NNNN-<title>.md
└── src/
```

**Multi-context** — a root `CONTEXT-MAP.md` marks the repo as having several bounded contexts, each with its own glossary and ADRs:

```
/
├── CONTEXT-MAP.md
├── docs/adr/                 ← system-wide decisions
└── src/
    ├── ordering/
    │   ├── CONTEXT.md
    │   └── docs/adr/         ← context-specific decisions
    └── billing/
        ├── CONTEXT.md
        └── docs/adr/
```

Create files lazily — only when you have something to write. No `CONTEXT.md` yet → create it when the first term resolves. No `docs/adr/` yet → create it when the first ADR is needed.

## Think vs Grill Boundary

**think** discovers *what to build* → outputs a PRD. **grill** validates *how well the PRD holds up* → outputs a sharpened PRD + CONTEXT.md + ADRs.

**Send back to `/think`** when:
- The goal statement itself needs to change (not just individual requirements)
- A fundamental technical approach needs re-evaluation (not just refinement)
- New requirements introduce an entirely new domain area outside original scope
- The PRD's Decision (ADR-lite) is invalidated by new information
- The PRD was a minimal `/story` PRD (no `/think` session) and major design questions surface

**Proceed to `/story`** when only terminology was sharpened, scope confirmed, or approach validated with refinements.

Small clarifications can be resolved inline. Major scope changes deserve a proper think session.

## What to Challenge

Read the PRD with hostile eyes. Pull out every open decision across these categories — skip none:

| Category | What to look for |
|---|---|
| **Open Questions** | Items explicitly unresolved in the PRD |
| **Assumptions** | Things the PRD assumes but hasn't validated |
| **Vague terms** | Words that could mean different things to different people |
| **Scope boundaries** | Why something is in vs out of scope — and is "out" really "deferred"? |
| **Technical approach** | Is the chosen approach sound? Were alternatives considered? |
| **Edge cases** | What happens when things go wrong (mid-billing cancellation, partial failure, concurrency)? |
| **CONTEXT.md conflicts** | Terms that clash with the existing domain glossary |
| **Code contradictions** | Stated behavior that doesn't match what the code does |
| **ADR-lite decisions** | Each decision in the PRD's "Decision (ADR-lite)" section — evaluate against the 3 ADR conditions; upgrade qualifying ones to formal ADRs |

## Challenge Patterns

For each item, lead with your recommended answer, then ask. A few patterns:

- **Terminology conflict** — *"Your glossary defines 'cancellation' as X, but the PRD seems to mean Y — which is it?"*
- **Fuzzy language** — *"The PRD says 'account' — do you mean Customer or User? Those are different."* Propose a precise canonical term.
- **Scope boundary** — *"You've excluded batch operations — genuinely not needed, or deferred? If deferred, note the extension point."*
- **Edge case** — *"What happens when a customer cancels mid-billing cycle? Prorate / full refund / no refund?"*
- **Code cross-check** — *"The PRD says partial cancellation is possible, but the code cancels entire Orders — which is the target state?"* Verify by reading the code, don't just ask.

## Question Pacing

Default to **one question at a time** — grill is a dependency tree, and a question's answer often reshapes the next. This is the anti-pattern #3 dependency-chain exception, not serial interrogation.

You may batch 2-3 questions in one message **only** when they are genuinely independent — no answer changes how you frame the others. When in doubt, stay one-at-a-time.

## Exhaustiveness Gate

Before declaring complete, verify every box:

- [ ] Every PRD Open Question has a resolution
- [ ] Every Assumption validated or converted to a requirement
- [ ] Every term conflict with CONTEXT.md addressed
- [ ] Every scope boundary confirmed (why is X out of scope?)
- [ ] Code cross-check completed for all stated behaviors

If any box is unchecked, keep going.

## PRD Traceability Update

Fill the `Grilled by` field in the PRD's `## Traceability` section AND set `Status` to `Grilled` so downstream skills know the plan was validated:

```markdown
- **Grilled by**: `/grill` (completed <YYYY-MM-DD>) — <summary: terms sharpened, assumptions resolved, ADRs created>
```

## Sync Parent Issue

The parent Issue is created by `/think` Step 9a (required) and recorded in the PRD's `## Issue` field (e.g. `#42`). grill's job is to **sync**, not create — creation is `/think`'s responsibility, and this division keeps a single point of ownership so `/story` always finds a parent to attach child issues to.

**3-step logic:**

1. **Read** the PRD `## Issue` field.
2. **Number present** → update the parent Issue body to reflect this grill's scope changes:
   - Sharpened terminology (link to updated `CONTEXT.md` entries)
   - Confirmed scope boundaries (what's in vs deferred)
   - New ADRs and their key conclusions
   - **Do not** change the Issue title (it uses the PRD's `<Feature Name>`, set by `/think`)
   - **Do not** close the parent Issue — it stays open until child issues from `/story` are done
3. **Field empty or missing** → skip. A minimal PRD from a direct `/story` path (which skipped `/think`) has no parent Issue by design; child issues there stand alone. Do not create one here.

**Boundary:** grill is "validate + sync", not "create". If you find yourself wanting to create a parent Issue, the right fix is upstream — the PRD should have gone through `/think` Step 9a.

## Worked Example

```
User: /grill  (after /think for "user subscription feature")

Agent: [reads docs/prd/PRD-0003-subscription.md and CONTEXT.md]

I've reviewed the PRD and found 6 items to resolve:

1. "Subscription" — not in CONTEXT.md, used ambiguously
2. Assumption: "payment is immediate" — not validated
3. Open Question: cancellation policy
4. Scope: "upgrade/downgrade" excluded without reason
5. Technical: Stripe vs custom payment — no decision recorded
6. Code: existing User model has no payment fields — migration unclear

Starting with #1. Your PRD uses "subscription" to mean both the act and
the entity. I recommend defining it as: **Subscription** — a Customer's
active paid access agreement with a lifecycle
(created → active → past_due → cancelled). Match your intent, or narrower?

User: That works, but add "trial" as a possible state.

Agent: Updated CONTEXT.md — Subscription definition includes trial state.
Moving to #2...

#2 is a code question — let me check rather than ask.
[grep: payment, stripe, gateway] → found src/payment/ with custom gateway,
no Stripe. Updating PRD to match existing architecture.

#3. Cancellation policy — recommend End-of-period (simpler, less refund
logic). Alternatives: immediate+prorate, immediate+no-refund. Which?

User: End-of-period.

Agent: Recorded. Checking ADR conditions: hard to reverse ✓ (affects
billing/UX/expectations), surprising without context ✓, real trade-off ✓
(simplicity over prorate fairness). All three met — creating ADR.
[creates docs/adr/0003-cancellation-eop.md]

[continues through #4-6...]

All 6 resolved. Exhaustiveness check: ✓ Open Questions, ✓ Assumptions,
✓ Terms, ✓ Scope, ✓ Code.

Updated files:
- docs/prd/PRD-0003-subscription.md — updated (Status → Grilled)
- CONTEXT.md — 3 new terms, 1 sharpened
- docs/adr/0003-cancellation-eop.md — created

Next: /story to break PRD into Issues.
```

Note the shape: extract all items up front, give a recommendation before each ask, fall back to the code when a question is code-answerable, and create the ADR inline the moment its decision lands — not in a batch at the end.
