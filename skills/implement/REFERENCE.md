# Implement: Detailed Reference

## Step 1: Entry Protocol Detail

Apply the [Skill Entry Protocol](../rules/entry-protocol.md) to read config and domain context.

### Context Checklist

- [ ] `docs/agents/domain.md` — actual paths for CONTEXT.md, PRDs, ADRs
- [ ] `docs/agents/repo-map.md` — multi-repo structure
- [ ] `docs/agents/issue-tracker.md` — tracker type and CLI conventions
- [ ] `docs/agents/triage-labels.md` — label vocabulary
- [ ] `docs/agents/language.md` — human-facing output language
- [ ] `CONTEXT.md` — domain glossary
- [ ] `docs/prd/PRD-NNNN-<title>.md` — product requirements (the PRD)
- [ ] `docs/adr/*.md` — architecture decision records
- [ ] `docs/research/INDEX.md` — research knowledge base

### Upstream Quality Check

Check the PRD's `## Traceability` section for each of these signals and note them in the output:

| Signal | Meaning | Note |
|--------|---------|------|
| `Created by: /story (minimal PRD)` | Requirements may not be decision-complete | Confirm acceptance criteria with user before proceeding |
| `Open Questions` or `TODO` markers remain | Decisions unresolved | Flag uncertainty in output |
| `Grilled by` field empty | Plan not validated against domain model | Proceed but note plan is unvalidated |

### Filing-Consistency Check

While scanning domain docs, flag (report, do not auto-fix):

- PRD content outside `docs/prd/`
- ADR files with `PRD-` prefix or PRD files without `PRD-` prefix
- Research records outside `docs/research/`
- Number collisions (two PRDs sharing the same NNNN, two ADRs sharing the same NNNN)
- Research record collisions (same `<stack>-<topic>-<major>` filename)

## Step 2: Work Inventory

### Determine Work Items

Priority order for determining what to implement:

1. **Issues from `/story`** — read the `## Sliced into` list in the PRD. Each issue is a seam. Read each issue's body for its Acceptance Criteria and blocked-by relationships.
2. **PRD Acceptance Criteria** — if no issues exist, extract the `## Acceptance Criteria` section from the PRD as work items.
3. **User description** — if only a verbal description is given, confirm work items with the user before proceeding.

### Dependency Ordering

Check each issue for `Blocked by` references in its body. Implement non-blocked items first, then their dependents. If no explicit dependencies exist, implement in the order listed in `## Sliced into`.

### PRD Status Update

Update the PRD status line from:
```
> **Status**: Sliced | **PRD**: PRD-NNNN | **Created**: YYYY-MM-DD | **Last updated**: YYYY-MM-DD
```
to:
```
> **Status**: In Progress | **PRD**: PRD-NNNN | **Created**: YYYY-MM-DD | **Last updated**: YYYY-MM-DD
```

Also set `Last updated` to today's date.

## Step 3: Implement Each Seam

### 3a. TDD Suitability Assessment

For each work item, evaluate all criteria. If **all** are true, the item is TDD-suitable:

- [ ] Acceptance criteria are clearly defined (testable, unambiguous)
- [ ] Behavior can be tested through public interfaces (API, component props, function signature)
- [ ] No external integration is required that makes fast test feedback impossible
- [ ] The expected behavior is deterministic (same input → same output)
- [ ] The implementation does not primarily consist of configuration, data migration, or UI layout

If TDD-suitable → proceed to 3b. If not → proceed to 3c.

### 3b. Run /tdd on This Item

Follow the full `/tdd` process for this issue/seam:

1. Read `skills/tdd/SKILL.md` and `skills/tdd/REFERENCE.md` for the detailed process
2. Execute all of `/tdd`'s steps: Plan → Acceptance Criterion Cycles (per criterion: Test Sub-Agent scenarios → Scenario Review Gate → Test Sub-Agent test code → Code Review Gate → Develop Sub-Agent implementation) → Refactor → Output
3. Let `/tdd` handle its own test writing, implementation, and refactoring
4. **Do not** run `/tdd`'s "Next: Run /review" step — the implement workflow handles review at Step 5
5. When `/tdd` outputs its completion summary, resume implement workflow

**If `/tdd` is cancelled mid-cycle** (user interrupts):
- Check which criteria completed (GREEN) vs not
- For completed criteria, proceed to typechecking (3d)
- For incomplete criteria, either resume `/tdd` or implement directly per 3c

### 3c. Direct Implementation (with Tests)

When an item is not TDD-suitable:

1. **Understand the behavior** — read the issue body or PRD acceptance criteria
2. **Write tests first if possible** — even outside formal TDD, write tests that verify the behavior
3. **Implement** — write the minimal code to satisfy the tests
4. **Run tests** — ensure all tests pass (both new and existing)

### 3d. Typechecking

After each item is implemented (via `/tdd` or direct):

1. Detect the project's typechecker from existing config files:
   - `tsconfig.json` → `tsc --noEmit`
   - `pyproject.toml` with `[tool.mypy]` → `mypy .`
   - `Cargo.toml` → `cargo check`
   - `Makefile` with `typecheck` target → `make typecheck`
   - `package.json` with `typecheck` script → `npm run typecheck`
   - Other patterns as discovered
2. Run the typechecker. If it fails, **read the error output and diagnose** (anti-pattern #12 — ignoring error output). Fix type errors before proceeding.

If no typechecker is detected, skip silently and note the absence in the output.

### 3e. Testing

After typechecking passes:

1. Identify the most specific test target for the changed files:
   - Single test file: `npm test -- --grep <pattern>` or `pytest tests/test_foo.py`
   - Module-level: `npm run test -- --dir src/foo` or `pytest tests/foo/`
2. Run that target. All tests must pass.
3. If tests fail, fix the implementation and re-run.

**Verify the artifact, not just the source** (anti-pattern #17) — ensure the test runner actually executed and reported results. Paste the output as evidence (anti-pattern #6 — claim without evidence).

### 3f. Committing

Commit with a descriptive message:

```
[PRD-NNNN] <seam title> — <summary>

Implemented <what> via <tdd | direct>.
<additional context if needed>
```

- Reference the issue number in the commit message body
- Commit only the changes related to this item
- Do not commit changes that belong to a different work item — **minimal change per commit** (anti-pattern #5)
- If the working tree has pre-existing dirty state unrelated to this session, warn the user before committing

**Commit message examples:**
```
[PRD-0003] User subscription data model — schema + CRUD API

Implemented subscription schema, repository, and CRUD API via /tdd.
Closes #42
```

```
[PRD-0003] Subscription management UI — view/cancel/upgrade

Implemented subscription management page with view, cancel, and upgrade flows.
Includes E2E tests for all three actions.
Closes #43
```

### PRD Issue Status Update

After each item is committed, update the PRD's `## Sliced into` list. Change the relevant issue's status from `— In Progress` or `— <empty>` to `— Done`:

```
- #<issue-1> — [PRD-NNNN] <slice title> (AFK) — Done
```

If `/tdd` already set the issue to `— In Progress`, update it to `— Done`.

## Step 4: Full Test Suite

After all items are implemented and committed:

1. Run the project's full test suite (the command used for CI or pre-merge testing)
2. If all tests pass → proceed to Step 5
3. If any tests fail:
   - Identify which item's changes caused the failure
   - Return to Step 3 for that item
   - Fix and re-commit (amend the previous commit for that item, or create a fixup commit)

## Step 5: Dispatch /review

Present the completed state to the user:

```
All <N> work items implemented, tested, and committed.
Full test suite: GREEN

Next: Run /review to review all changes before merge.
```

Do not auto-run `/review`. Follow the project's convention that skills do not auto-chain — the user explicitly invokes the next skill.

## Step 6: Output

Produce the output template from SKILL.md, filling in:
- Each work item with its implementation method and commit hash
- PRD reference and current status
- Full test suite result
- Next step to `/review`

## Recovery Procedures

### /tdd Cancelled Mid-Cycle

If the user interrupts `/tdd` (e.g., "stop", "skip this one", "this is taking too long"):

1. Check which acceptance criteria within `/tdd` completed (GREEN)
2. For GREEN criteria: record them, proceed to typechecking (3d)
3. For incomplete criteria: assess whether to implement directly (3c) or skip
4. Ask the user: "Item <X> was not completed by /tdd. Implement directly, skip, or resume /tdd?"

### Test Suite Regression

If a change for item B breaks tests for previously implemented item A:

1. The dependency ordering was wrong — item B should have been implemented after A
2. Fix item B's implementation to not break A
3. Re-run tests for both A and B before proceeding

### Dirty Working Tree

If the working tree has uncommitted changes before starting:

1. Warn the user: "Working tree has uncommitted changes from outside this session."
2. Ask: "Stash them and proceed, or commit them separately?"
3. Follow the user's choice. Do not include unrelated changes in implement commits.

### Typechecker Not Found

If no typechecker can be detected:

1. Skip typechecking for all items
2. Note in the output: "No typechecker detected — skipped typechecking"
3. Proceed with testing
