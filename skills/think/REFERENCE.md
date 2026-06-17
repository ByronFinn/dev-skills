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
I'll help you think through this. Would you like me to create a PRD file at `docs/prd/<feature-name>.md` as we work through the design?

- **Yes** — I'll create and update a PRD file throughout our discussion
- **No** — I'll work through the plan conversationally and provide a summary at the end
```

**If Yes:** create PRD at `docs/prd/<feature-name>.md` using the template below.

**If No:** skip PRD creation. Still follow the brainstorming process (Steps 3-9), but keep notes in your working context and produce a design summary at the end.

**PRD Location:** `docs/prd/<feature-name>.md`

If creating, use this template:

```markdown
# <Feature Name>

## Goal
<why + what, one paragraph>

## What I already know
* <facts from user message>
* <facts discovered from code/docs>

## Assumptions (temporary)
* <assumptions to validate>

## Open Questions
* <only blocking/preference questions; keep brief>

## Requirements (evolving)
* <what is known>

## Acceptance Criteria (evolving)
* [ ] <testable criteria>

## Definition of Done (team quality standards)
* Add/update tests (unit/integration where appropriate)
* Lint/typecheck/CI passes
* Update docs/notes on behavior changes
* Consider release/rollback when risky

## Out of Scope (explicit)
* <what will not be done>

## Technical Notes
* <files checked, constraints, links, references>
* <summary of research notes (if applicable)>
```

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

Then present **2-3 viable approaches** in PRD:

```markdown
## Research References
* [Research Topic A](docs/research/topic-a.md) — <one-sentence summary>
* [Research Topic B](docs/research/topic-b.md) — <one-sentence summary>

## Feasible Approaches

**Approach A: <name>** (Recommended)
- How it works:
- Pros:
- Cons:

**Approach B: <name>**
- How it works:
- Pros:
- Cons:
```

Then ask **one** preference question:
- "Which approach do you prefer: A / B / C (or other)?"

## Step 6: Expansion Scan (DIVERGE) — Required After Initial Understanding

Once you can summarize the goal, proactively expand your thinking before converging.

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

## Step 8: Propose Approaches + Record Decision (Complex Tasks)

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

Record result in PRD as ADR-lite section:

```markdown
## Decision (ADR-lite)
**Context**: Why this decision was needed
**Decision**: Which approach was chosen
**Consequences**: Trade-offs, risks, potential future improvements
```

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

## Step 9a: Create Issue (Optional)

If user confirms, create issue as parent task. Read `docs/agents/issue-tracker.md` for the issue creation convention.

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

Throughout the brainstorming process, new domain concepts may emerge. Capture these so `/grill` can sharpen and promote them into `CONTEXT.md`.

**When to record:**
- A new concept was named or defined during discussion (not just code-level variables)
- A term was used in an ambiguous or overloaded way and a working definition was agreed
- An entity, relationship, or lifecycle was introduced that does not yet exist in `CONTEXT.md`

**Where to record:**
- If PRD was created: add a `## Domain Terms` section at the bottom of the PRD
- If no PRD: include the terms in the approved design summary under a `## Domain Terms` heading

**Format:**

```markdown
## Domain Terms (draft — for /grill to refine)

| Term | Working Definition | Status |
|------|--------------------|--------|
| <term> | <one-sentence working definition> | new / needs sharpening / conflicts with existing |
```

These are **draft** terms — they do NOT go into `CONTEXT.md` during `/think`. The `/grill` skill is responsible for sharpening terminology and updating `CONTEXT.md`. Recording them here ensures `/grill` knows what was discussed without re-discovering the same concepts.

**Rules:**
- Record only terms that are genuinely new or ambiguous — don't duplicate what's already clearly defined in `CONTEXT.md`
- If a term conflicts with an existing `CONTEXT.md` entry, flag it explicitly (`Status: conflicts with existing`) so `/grill` knows to resolve the conflict
- This step is lightweight — don't turn it into a full glossary exercise. 3-7 terms is typical; if you have more, consider whether the scope is too broad

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
