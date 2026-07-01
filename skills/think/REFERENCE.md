# Think: Detailed Reference

## Step 0: Quick Assessment

Before doing anything, assess complexity from the user's request:

- If the request is obviously **Trivial** (single-line fix, typo, obvious change with one clear approach): tell the user `/think` is unnecessary, recommend direct implementation or `/tdd`, and **stop here**. No PRD file is created.
- For all other complexity levels: proceed to Step 1.

This avoids wasting time on requests that don't need brainstorming.

## Step 1: Auto-Context Collection

Before asking "what does the code look like?", collect context yourself:

**Codebase Checklist:**
- Identify likely affected modules/files
- Find existing patterns (similar features, conventions, error handling style)
- Check configs, scripts, existing command definitions
- Note constraints (runtime, dependency policies, build tools)

**Docs Checklist:**
- Find existing PRD/spec/templates
- Find command usage examples, README, ADRs (if any)

Write findings to PRD:
- Add to `What I already know`
- Add constraints/links to `Technical Notes`

## Step 2: Offer to Create a PRD

After auto-context collection (Step 1), ask the user if they want to persist the plan as a PRD file. **Do not create the PRD automatically.** By this point you have enough context to explain what the PRD would contain.

Step 2 is sequenced after Step 1 so the user can make an informed decision based on actual findings, not just the initial request.

**Ask (for non-Trivial tasks):**

```
I'll help you think through this. Would you like me to create a PRD file at `docs/prd/PRD-NNNN-<title>.md` as we work through the design?

- **Yes** — I'll create and update a PRD file throughout our discussion
- **No** — I'll work through the plan conversationally and provide a summary at the end
```

**If Yes:** first apply [Skill Entry Protocol](../rules/entry-protocol.md) **Step 3a (PRD Conflict Check)** to catch topic collisions against existing `PRD-NNNN-*.md` (resume vs create-new). Only after Step 3a passes, scan `docs/prd/` for existing `PRD-NNNN-*.md` files, assign the next NNNN (max + 1, starting from 0000), and create the PRD at `docs/prd/PRD-NNNN-<title>.md`.

**If No:** skip PRD creation. Still follow the brainstorming process (Steps 3-9), but keep notes in your working context and produce a design summary at the end.

**PRD Location:** `docs/prd/PRD-NNNN-<title>.md`

If creating, use the template and field rules in [PRD-FORMAT.md](PRD-FORMAT.md). Do not retype the template here — PRD-FORMAT.md is the single source.

## Step 3: Classify Complexity

Determine depth of brainstorming for Simple/Moderate/Complex tasks:

| Complexity | Criteria | Behavior |
|---|---|---|
| **Simple** | Clear goal, 1-2 files, clear scope | Ask 1 confirmation question, then finalize a lightweight PRD or recommend `/tdd` if user wants test-first implementation |
| **Moderate** | Multiple files, some ambiguity | Light brainstorming (2-3 high-value questions) |
| **Complex** | Unclear goal, architecture choices, multiple approaches | Full brainstorming |

## Step 4: Question Gates (Only Ask High-Value Questions)

Before asking any question, run these gates:

**Gate A — Can I derive this without user?**

If answer obtainable via:
- Codebase inspection (code/configs)
- Docs/specs/conventions
- Quick market/OSS research

→ **Don't ask.** Fetch it, summarize, update PRD.

**Gate B — Is this a meta/lazy question?**

Examples:
- "Should I search?"
- "Can you paste code so I can continue?"
- "What does the code look like?" (when codebase is available)

→ **Don't ask.** Take action.

**Gate C — What type of question is this?**

- **Blocking**: Cannot continue without user input
- **Preference**: Multiple valid choices, depends on product/UX/risk preference
- **Derivable**: Should be answered by inspection/research

→ Only ask **Blocking** or **Preference**.

## Step 5: Research-First Mode (Mandatory for Technical Choices)

**Triggers (any one → research first):**
- Task involves choosing approach, library, protocol, framework, template system, plugin mechanism, or CLI UX convention
- User asks "best practice", "how do others do this", "recommended"
- User cannot reasonably enumerate options

**Research Steps:**
1. Identify 2-4 comparable tools/patterns
2. Summarize common conventions and why they exist
3. Map conventions to our codebase constraints
4. Write to PRD's `Research References` section

Then present **2-3 viable approaches** in the PRD. Fill the `## Research References` and `## Feasible Approaches` sections per [PRD-FORMAT.md](PRD-FORMAT.md) — that file is the single source for the exact field shape.

Then ask **one** preference question:
- "Which approach do you prefer: A / B / C (or other)?"

## Step 6: Expansion Scan (DIVERGE)

Once you can summarize the goal, proactively expand your thinking before converging. **Scale to complexity** (from Step 3):

- **Simple** — skip this step entirely. Simple tasks have a clear goal and 1-2 files; forcing future-evolution/related-scenario divergence on them is over-ceremony. Go straight to Step 7.
- **Moderate** — do only category 3 (Failure & edge cases). One round.
- **Complex** — do all three categories below, 1-2 points each.

**Expansion Categories (1-2 points each):**

1. **Future evolution**
   - What might this feature become in 1-3 months?
   - Which extension points are worth preserving now?

2. **Related scenarios**
   - Related commands/workflows this should align with?
   - Parity expectations (create vs update, import vs export)?

3. **Failure & edge cases**
   - Conflicts, offline/network failures, retry, idempotency, compatibility, rollback
   - Input validation, security boundaries, permission checks

**Expansion message template (to user):**

```markdown
I understand you want to implement: <current goal>.

Before deep design, let me quickly diverge on three categories (avoid rework later):

1. Future evolution: <1-2 points>
2. Related scenarios: <1-2 points>
3. Failure/edge cases: <1-2 points>

Which do you want in this MVP (or none)?

1. Current requirements only (minimum viable)
2. Add <X> (reserve for future expansion)
3. Add <Y> (improve robustness/consistency)
4. Other: describe your preference
```

Then update PRD:
- What goes in MVP → `Requirements`
- What's excluded → `Out of Scope`

## Step 7: Q&A Loop (CONVERGE)

**Rules:**
- One question at a time
- Use multiple choice for preference questions
- After each user answer:
  - Immediately update PRD
  - Move answered items from `Open Questions` to `Requirements`
  - Update `Acceptance Criteria` with testable checkboxes
  - Clarify `Out of Scope`

**Question priority (recommended):**
1. MVP scope boundaries (what's in/out)
2. Preference decisions (after presenting specific options)
3. Failure/edge behavior (only for MVP-critical paths)
4. Success metrics & acceptance criteria (what proves it works)

**Preference question format (multiple choice):**

```markdown
For <topic>, which approach do you prefer?

1. **Option A** — <implication + trade-off>
2. **Option B** — <implication + trade-off>
3. **Option C** — <implication + trade-off>
4. **Other** — describe your preference
```

## Step 8: Propose Approaches + Record Decision

When requirements are clear enough, propose 2-3 approaches (if not already done via research-first):

```markdown
Based on current information, here are 2-3 viable approaches:

**Approach A: <name>** (Recommended)
- How:
- Pros:
- Cons:

**Approach B: <name>**
- How:
- Pros:
- Cons:

Which direction do you prefer?
```

Record the result in the PRD's `## Decision (ADR-lite)` section, using the field shape defined in [PRD-FORMAT.md](PRD-FORMAT.md) (Context / Decision / Consequences).

## Step 9: Final Confirmation + Implementation Plan

When open questions are resolved, confirm complete requirements with structured summary:

**Final confirmation format:**

```markdown
Here is my understanding of complete requirements:

**Goal**: <one sentence>

**Requirements**:
* ...

**Acceptance Criteria**:
* [ ] ...
* [ ] ...

**Definition of Done**:
* ...

**Out of Scope**:
* ...

**Technical Approach**:
<brief summary + key decisions>

**Implementation Plan (small PRs)**:
* PR1: <scaffolding + tests + minimal pipeline>
* PR2: <core behavior>
* PR3: <edge cases + docs + cleanup>

Does this look correct? If so, I'll finalize the PRD and recommend the next workflow step (`/grill` for plan challenge, or `/story` if already validated).
```

## Step 9a: Create Parent Issue (Required)

After the user confirms the plan in Step 9, create the parent Issue as a **required** action. This is the single point where the PRD's parent Issue is created — `/grill` and `/story` downstream rely on the PRD's `## Issue` field to attach child issues. Skipping it leaves child issues orphaned (the "PRD has no parent Issue" break in the chain). Read `docs/agents/issue-tracker.md` for the issue creation convention.

Create the issue with a structured body (not the raw PRD dump). Use the same Issue Format as `/story` for consistency:

```markdown
## Parent

(This is the parent issue — child issues created by `/story`)

## What to build

<goal from PRD, 1-2 sentences>

## Acceptance Criteria

* [ ] <from PRD>
* [ ] ...

## Blocked by

None — this is a parent issue
```

For GitHub:
```bash
gh issue create --title "<Feature Name>" --body "$(cat <<'EOF'
## Parent

(This is the parent issue — child issues created by \`/story\`)

## What to build

<goal>

## Acceptance Criteria

* [ ] ...

## Blocked by

None — this is a parent issue
EOF
)" --label "prd"
```

Record Issue number in PRD:

```markdown
## Issue
#<issue-number>
```

## Step 9b: Record Domain Terms

If new domain concepts emerged during brainstorming (a named concept, an agreed working definition for an ambiguous term, or an entity/relationship not yet in `CONTEXT.md`), capture them so `/grill` can sharpen and promote them. These are **draft** terms — they do NOT go into `CONTEXT.md` during `/think`; that is `/grill`'s job.

Add a `## Domain Terms` section (to the PRD, or to the approved design summary if no PRD):

```markdown
## Domain Terms (draft — for /grill to refine)

| Term | Working Definition | Status |
|------|--------------------|--------|
| <term> | <one-sentence working definition> | new / needs sharpening / conflicts with existing |
```

Keep this lightweight — record only genuinely new or ambiguous terms (don't duplicate `CONTEXT.md`), flag conflicts explicitly, and 3-7 terms is typical. If you have notably more, the scope may be too broad.

## Complexity Classification Detail

### Trivial

**Criteria:**
- Single-line fix
- Typo correction
- Obvious change with one clear approach

**Behavior:**
- Skip brainstorming entirely
- State that `/think` is unnecessary for this request
- Recommend direct implementation outside this skill, or `/tdd` if the user wants test-first work

**Example:** "Fix typo in error message"

### Simple

**Criteria:**
- Clear goal
- 1-2 files affected
- Clear scope, no ambiguity

**Behavior:**
- Ask 1 confirmation question if needed
- Finalize a lightweight PRD or recommend `/tdd` for test-first implementation
- Do not write code inside `/think`

**Example:** "Add retry to this API call"

### Moderate

**Criteria:**
- Multiple files
- Some ambiguity
- Clear goal but multiple paths

**Behavior:**
- Light brainstorming
- 2-3 high-value questions only

**Example:** "Add user preferences page"

### Complex

**Criteria:**
- Unclear goal
- Architecture choices required
- Multiple valid approaches
- Significant implementation effort

**Behavior:**
- Full brainstorming process
- All steps apply
- Research-first for technical choices

**Example:** "Design multi-tenant authentication system"
