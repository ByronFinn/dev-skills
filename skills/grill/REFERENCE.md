# Grill: Detailed Reference

## Process Detail

### Step 1: Read PRD

Read `docs/prd/<feature-name>.md` to understand current plan.

### Step 2: Check Existing Domain Model

Look for existing documentation:

**Single context structure:**
```
/
├── CONTEXT.md
├── docs/
│   └── adr/
│       ├── 0001-event-sourced-orders.md
│       └── 0002-postgres-for-write-model.md
└── src/
```

**Multi-context structure (if CONTEXT-MAP.md exists):**
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

Create files lazily — only when you have something to write. If no `CONTEXT.md` exists, create it when resolving first term. If no `docs/adr/` exists, create it when first ADR is needed.

### Step 3: Interview Challenges

For each decision branch:

1. **Ask question** — one at a time, wait for feedback before continuing
2. **Provide recommended answer** — based on best practices and codebase conventions
3. **If answer can be found by exploring codebase** — explore codebase instead of asking

### Step 4: Challenge Glossary

When user uses a term that conflicts with existing language in `CONTEXT.md`, call it out immediately:
> "Your glossary defines 'cancellation' as X, but you seem to mean Y — which is it?"

### Step 5: Sharpen Fuzzy Language

When user uses vague or overloaded terms, propose precise canonical term:
> "You're saying 'account' — do you mean the Customer or the User? Those are different things."

### Step 6: Discuss Concrete Scenarios

When domain relationships are discussed, stress-test with specific scenarios. Invent scenarios that probe edge cases and force user to be precise about boundaries between concepts.

### Step 7: Cross-Check With Code

When user states how something works, check whether code agrees. If you find contradiction, surface it:
> "Your code cancels entire Orders, but you just said partial cancellation is possible — which is right?"

### Step 8: Update CONTEXT.md Inline

When term resolves, update `CONTEXT.md` right away. Don't batch — capture as they happen.

**Use format in CONTEXT-FORMAT.md.**

`CONTEXT.md` should be totally devoid of implementation details. Do not treat `CONTEXT.md` as a spec, scratch pad, or repository for implementation decisions. It is a glossary and nothing else.

### Step 9: Offer ADRs Sparingly

Only offer to create ADR when all three are true:

1. **Hard to reverse** — cost of changing mind later is meaningful
2. **Surprising without context** — future reader will wonder "why did they do it this way?"
3. **Result of real trade-off** — genuine alternatives existed and you chose one for specific reasons

If any of three is missing, skip ADR.

**Use format in ADR-FORMAT.md.**

### Step 10: Update PRD

Update PRD based on interview results:
- Corrected technical approach
- Updated requirements
- Adjusted acceptance criteria
- Updated in/out scope

### Step 11: Sync GitHub Issue (if exists)

If corresponding GitHub Issue exists, update its content:
- Update Issue body to reflect latest PRD
- Keep Issue number in sync

## CONTEXT-FORMAT.md

```markdown
# Context Glossary

## Core Concepts

Brief overview of domain (2-3 paragraphs).

## Domain Glossary

| Term | Definition |
|---|---|
| **Customer** | A person who has purchased a subscription |
| **User** | Anyone using the platform, including free tier |
| **Subscription** | A customer's paid access agreement |

## Key Relationships

- **Customer → Subscription**: One customer can have multiple active subscriptions
- **Subscription → Plan**: Each subscription is tied to a pricing plan
```

## ADR-FORMAT.md

```markdown
# ADR-XXX: [Decision Title]

## Status

Accepted / Proposed / Deprecated / Superseded by [ADR-YYY]

## Context

Why this decision was needed. What problem are we solving?

## Decision

What was decided. Be specific.

## Consequences

What becomes easier or harder. What risks are introduced.

## Alternatives Considered

What other options were considered and why rejected.

## References

Links to relevant discussions, docs, or issues.
```

## Example Dialogue

```
User: I want to add user subscription functionality

Agent: 🥷 Let's start with core concepts.

When you say "subscription", do you mean:
- Paid subscription (users pay for premium features)
- Free subscription (users opt-in to notifications)
- Something else?

User: Paid subscription, monthly billing

Agent: Got it. Let's check existing terminology.

[Read CONTEXT.md]
I see your glossary defines "Customer" as paid user, "User" as free user.

In subscription context, are you saying Customer subscribes, or User can subscribe?

User: Customer subscribes

Agent: Clear. I'll update CONTEXT.md to reflect "Subscription is a Customer's paid access agreement".

[Update CONTEXT.md]

Next question: Is subscription activation immediate or...
```
