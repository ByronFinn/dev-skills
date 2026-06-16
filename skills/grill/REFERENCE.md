# Grill: Detailed Reference

## Think vs Grill Boundary

**think** is for requirements discovery — what to build. The output is a PRD at `docs/prd/<feature-name>.md`.

**grill** is for plan validation — how well does the PRD hold up. The input is an existing PRD, the output is a validated PRD with sharpened terminology and documented decisions.

If during grill the user raises entirely new requirements not in the PRD, consider whether this should go back to `/think` first. Small clarifications can be resolved inline. Major scope changes deserve a proper think session.

**When to send back to /think:**
- The goal statement itself needs to change (not just individual requirements)
- A fundamental technical approach needs re-evaluation (not just refinement)
- New requirements introduce an entirely new domain area not in the original scope
- The PRD's Decision (ADR-lite) section's chosen approach is invalidated by new information
- The original PRD was created by `/story` as a minimal PRD (no `/think` session) and major design questions surface during grilling

**When to proceed to /story:**
- Only terminology was sharpened
- Scope boundaries were confirmed or slightly adjusted
- Technical approach was validated with minor refinements
- ADRs were created but the approach direction is the same

## What to Challenge

When reading the PRD at `docs/prd/<feature-name>.md`, look for these categories of open decisions:

- **Open Questions** — unresolved items explicitly listed in the PRD
- **Assumptions** — things the PRD assumes but hasn't validated
- **Vague terms** — words that could mean different things to different people
- **Scope boundaries** — why is something in scope vs out of scope
- **Technical approach** — is the chosen approach sound, are alternatives considered
- **Edge cases** — what happens when things go wrong
- **Conflicts with CONTEXT.md** — terms that clash with existing domain glossary
- **Code contradictions** — stated behavior that doesn't match what the code does
- **ADR-lite decisions in PRD** — decisions recorded in the PRD's "Decision (ADR-lite)" section during /think. Evaluate each against the 3 ADR conditions. Upgrade qualifying ones to formal ADRs; leave the rest as PRD-internal notes.

## Challenge Types

### Terminology Conflict

When a term in the PRD conflicts with existing language in `CONTEXT.md`:

> "Your glossary defines 'cancellation' as X, but the PRD seems to mean Y — which is it?"

### Fuzzy Language

When the PRD uses vague or overloaded terms, propose a precise canonical term:

> "The PRD says 'account' — do you mean the Customer or the User? Those are different things."

### Scope Boundary

When something is excluded without clear justification:

> "You've excluded batch operations from scope — is that because they're genuinely not needed, or because they're deferred? If deferred, should we note the extension point?"

### Edge Case

When domain relationships are discussed, stress-test with specific scenarios:

> "What happens when a customer cancels mid-billing cycle? Prorate? Full refund? No refund?"

### Code Cross-Check

When the PRD states how something works, verify against code:

> "The PRD says partial cancellation is possible, but the code currently cancels entire Orders — which is the target state?"

## Exhaustiveness Gate

Before declaring grill complete, verify:

- [ ] Every PRD Open Question has a resolution
- [ ] Every PRD Assumption validated or converted to requirement
- [ ] Every term conflict with CONTEXT.md addressed
- [ ] Every scope boundary confirmed (why is X out of scope?)
- [ ] Code cross-check completed for all stated behaviors

## Question Pacing: Dependency Chains vs Independent Decisions

Not every question needs to be asked one at a time. Use this decision framework:

**Ask one at a time when:**
- The answer to question A changes how you frame question B (dependency chain)
- The answer determines which branch of the design tree to explore next
- Example: "What payment provider?" → answer determines "What webhook format?" → answer determines "What retry strategy?"

**Batch 2-3 questions together when:**
- Each question's answer is independent of the others
- The answers won't change how you frame subsequent questions
- Example: "Should subscription include a trial state?" + "Is upgrade/downgrade in scope?" + "What's the minimum billing period?" — these three don't depend on each other

**Batch format:**
```markdown
These 3 decisions are independent — I'll ask them together:

1. **<topic A>**: <options>
2. **<topic B>**: <options>
3. **<topic C>**: <options>

Answer any or all. If you're unsure on any, I can drill down separately.
```

This reduces total rounds without sacrificing the depth of dependency-chain questioning.

## PRD Traceability Update

When updating the PRD after grill, fill the `Grilled by` field in the PRD's `## Traceability` section:

```markdown
- **Grilled by**: `/grill` (completed <YYYY-MM-DD>) — <summary: terms sharpened, assumptions resolved, ADRs created>
```

This enables downstream skills (story, tdd, review) to verify that the plan was validated.

## Example Dialogue

```
User: /grill (after completing /think for "user subscription feature")

Agent: [Reads docs/prd/subscription.md and CONTEXT.md]

I've reviewed the PRD and found 6 items to resolve:

1. "Subscription" — not defined in CONTEXT.md, used ambiguously in PRD
2. Assumption: "Payment is immediate" — not validated
3. Open Question: cancellation policy
4. Scope: "upgrade/downgrade" listed as out of scope without reason
5. Technical: Stripe vs custom payment — no decision recorded
6. Code: existing User model has no payment fields — migration path unclear

Starting with #1.

Your PRD uses "subscription" to mean both "the act of subscribing" and
"the subscription entity". In CONTEXT.md, neither term exists yet.

I recommend defining it as: **Subscription** — a Customer's active paid
access agreement, with a lifecycle (created → active → past_due → cancelled).

Does this definition match your intent, or should it be narrower/wider?

User: That works, but add "trial" as a possible state.

Agent: Updated CONTEXT.md: Subscription definition includes trial state.

[Updates CONTEXT.md]

Moving to #2. The PRD assumes "payment is immediate" — but what about:
- Bank transfers (1-3 business days)
- Payment failures and retries
- Free trial period before first charge

I recommend starting with credit card + retry as the default, and adding
free trial support as an extension point later.

Which of these exist in your system?

User: Only credit card, with retry on failure. No free trial for now.

Agent: Clear. I'll update the PRD:
- Assumption validated: payment is credit card only, with retry
- "Free trial" noted as explicitly out of scope

Moving to #3. Cancellation policy — when a customer cancels:

1. **End of billing period** — access continues until paid period ends (Recommended: simpler, less refund logic)
2. **Immediate with prorate** — access ends now, refund unused portion
3. **Immediate, no refund** — access ends now, no refund

Which approach?

User: Option 1 for now.

Agent: Recorded. Checking ADR conditions:
1. Hard to reverse? Yes — changing cancellation policy later affects billing, UX, and customer expectations
2. Surprising without context? Yes — a future reader won't know why EOP was chosen
3. Real trade-off? Yes — we chose simplicity over prorate fairness

All three met. Creating ADR.

[Creates docs/adr/0003-cancellation-eop.md]

Moving to #4. "Upgrade/downgrade" is out of scope — is that because they're
genuinely not needed, or deferred? I recommend deferring and noting the
extension point for future phases.

User: Deferred.

Agent: Recorded. Updated PRD to mark upgrade/downgrade as deferred with extension note.

Moving to #5. I'll check the codebase instead of asking — whether Stripe
or a custom payment module exists.

[Grep: payment, stripe, gateway]

Found `src/payment/` with custom gateway. Stripe is not used. The PRD
didn't specify — updating it to match existing architecture.

Moving to #6. Checking the User model:

[Read: src/models/user.ts]

Confirmed — User model has no payment-related fields. I recommend adding
a `payment_method_id` field and a `payments` relation, or creating a
separate `Customer` entity. Which do you prefer?

User: Separate Customer entity.

Agent: Recorded. Updated PRD.

[Continues through remaining items]

Agent: All 6 items resolved. Running exhaustiveness check:

- [x] Every PRD Open Question resolved
- [x] Every Assumption validated
- [x] No term conflicts with CONTEXT.md
- [x] Scope boundaries confirmed
- [x] Code cross-check done

Files updated:
- docs/prd/subscription.md — updated
- CONTEXT.md — 3 new terms, 1 sharpened
- docs/adr/0003-cancellation-eop.md — created

Next: Run /story to break PRD into Issues.
```
