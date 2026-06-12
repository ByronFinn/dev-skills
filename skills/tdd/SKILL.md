---
name: tdd
description: "Sub-agent orchestrated test-driven development. For each acceptance criterion, Test Sub-Agent designs scenarios and writes tests (RED), human reviews at two gates, Develop Sub-Agent implements (GREEN). After all cycles, unified Refactor. Use when user wants TDD for feature building or bug fixing, mentions red-green-refactor, or wants test-first development."
when_to_use: "TDD,测试,实现,red-green-refactor,test-driven,测试驱动"
dispatch_intent: "Test-driven development, feature implementation, bug fix"
---

# TDD: Test-Driven Development

🥷 Sub-agent orchestrated red-green-refactor, one acceptance criterion at a time.

## Outcome Contract

- **Outcome**: Feature implemented with passing tests, verified through independent sub-agent perspectives and two-stage human review
- **Done when**: All acceptance criteria (from input Issue, PRD, or confirmed in Step 1) pass their cycle; unified refactor complete; all tests GREEN
- **Evidence**: Tests turn GREEN per cycle; human approved scenario design and test code at each gate; final refactor passes full suite
- **Output**: Per-cycle results with test locations, test statistics, refactor summary, next step to `/review`

## Core Principles

**Behavior testing through public interfaces.** Tests verify what the system does, not how. Code can change completely; tests should not.

**Sub-agent independence.** Test Sub-Agent and Develop Sub-Agent each re-read shared context (PRD, Story, Issue, CONTEXT.md, ADRs) from disk before acting. They never share internal state or cached understanding. See anti-patterns.md #38.

**Two-stage human review.** Each acceptance criterion passes through two synchronous gates — Scenario Review Gate (scenario design quality) and Test Code Review Gate (code quality and fidelity). Both gates are blocking; execution halts until the human responds.

**Vertical slicing.** One acceptance criterion = one independent cycle (design → review → test code → review → implement). The cycle structure enforces vertical slicing naturally — there is no way to batch all tests then implement.

## Input

Accept any of these, in priority order:
1. **Issue reference** (e.g., `#42` or a URL) — read the issue body; use its Acceptance Criteria as the cycle list
2. **PRD file** — read `docs/prd/<feature-name>.md`; extract Requirements and Acceptance Criteria
3. **Direct description** — user describes the behavior to implement; confirm acceptance criteria in Step 1 before proceeding

## Anti-Pattern: Horizontal Slicing

**Don't write all tests then all implementation.** This produces bad tests:
- Batch tests test **imagined** behavior, not **actual** behavior
- End up testing **shape** (data structures, function signatures) not user-visible behavior
- Tests become insensitive to real changes — pass when behavior breaks, fail when behavior correct

**The Acceptance Criterion Cycle IS vertical slicing.** Each cycle completes one criterion end-to-end: scenario design → human review → test code → human review → implementation. The sub-agent pattern enforces this naturally — the Develop Sub-Agent only sees one approved test at a time, and cannot batch.

```
WRONG (horizontal):
  RED:   test1, test2, test3, test4, test5
  GREEN: impl1, impl2, impl3, impl4, impl5

RIGHT (Acceptance Criterion Cycle):
  Cycle 1: scenarios→review→test1→review→impl1
  Cycle 2: scenarios→review→test2→review→impl2
  Cycle 3: scenarios→review→test3→review→impl3
  ...
  Refactor: unified after all cycles GREEN
```

## Process Summary

**Step 1: Plan** — Read `docs/agents/domain.md` (if exists) to locate CONTEXT.md and ADR paths. Read `docs/agents/repo-map.md` (if exists) to identify cross-repo context. Read input (Issue, PRD, or description). Extract acceptance criteria. Confirm interface changes with user. Prioritize behaviors. Identify which Issues/criteria to work on.

**Step 2: Acceptance Criterion Cycle** — For EACH acceptance criterion, run the 5-step loop:
1. **Test Sub-Agent (scenario design)** — design test scenarios as structured table
2. **Scenario Review Gate** — human reviews scenario design
3. **Test Sub-Agent (test code)** — write test code from approved scenarios → RED
4. **Test Code Review Gate** — human reviews test code
5. **Develop Sub-Agent (implementation)** — write code to make test GREEN

**Step 3: Refactor** — After all cycles GREEN, Develop Sub-Agent performs unified refactor: extract duplication, deepen modules, apply SOLID. Run full test suite after each refactor step.

**Step 4: Output** — Produce result summary. If a PRD file exists, fill the `Implemented by` field in its `## Traceability` section with the Issue reference.

See [REFERENCE.md](REFERENCE.md) for detailed sub-agent instructions, checklists, and independence constraints.

## Scenario Review Gate

Test Sub-Agent produces a structured scenario table:

```
| Scenario | Input | Expected Output | Boundary Conditions |
|----------|-------|-----------------|---------------------|
| <description> | <what goes in> | <what comes out> | <edges, limits, edge cases> |
```

**Human review checklist:**
- [ ] All acceptance criterion behaviors covered
- [ ] Boundary conditions identified and appropriate
- [ ] No missing or redundant scenarios
- [ ] Scenario scope is reasonable (not too broad, not too narrow)

**Human response:** Approve (proceed to test code) / Reject with feedback (Test Sub-Agent revises scenarios)

## Test Code Review Gate

Test Sub-Agent writes test code faithful to approved scenarios. Tests are RED by design.

**Human review checklist:**
- [ ] Tests use only public interface
- [ ] Tests verify behavior, not implementation
- [ ] Test naming reflects scenario intent
- [ ] Tests are faithful to approved scenarios
- [ ] No implementation coupling (mocking internals, testing private methods)

**Human response:** Approve (proceed to Develop Sub-Agent) / Reject with feedback (Test Sub-Agent revises test code)

## Per-Cycle Checklist

```
[ ] Test Sub-Agent re-read shared context from disk
[ ] Scenarios cover acceptance criterion completely
[ ] Scenario Review Gate passed
[ ] Test code faithful to approved scenarios
[ ] Test code uses public interface only
[ ] Test Code Review Gate passed
[ ] Develop Sub-Agent re-read shared context from disk
[ ] Implementation is minimal for this test
[ ] Test turns GREEN
[ ] No speculative features added
```

Shared behavioral constraints: apply [../rules/anti-patterns.md](../rules/anti-patterns.md) when a global anti-pattern is relevant.

## Gotchas

| What happened | Rule |
|---|---|
| Develop Sub-Agent modifies tests | Stop work, report issue to human, let human decide |
| Sub-agent uses cached context | Re-read PRD/Story/Issue/CONTEXT.md/ADRs from disk before each phase |
| Batch all scenarios across criteria | One acceptance criterion per cycle, enforced by gate structure |
| Tests fail when renaming function | Test behavior through public interface, not implementation |
| Test private methods | Test public interfaces only |
| Mock internal collaborators | Test real integrations |
| Refactor while any test is RED | Get all cycles GREEN first, then unified refactor |
| Scenario review skipped | Two-stage gate is mandatory — scenario design is the highest-leverage decision |
| Sub-agents share internal state | Each sub-agent starts fresh — no inherited context or cached understanding |
| Human says "looks fine" at gate | Use explicit checklist; treat approval as checklist confirmation |

## Output

```
TDD complete.

Traceability:
- Source: <Issue #N / PRD <name> / direct description>
- Feature: <feature name>
- Criteria implemented: <count>

Cycles:
* <acceptance criterion 1> — test: <test-file>:<line> — GREEN
* <acceptance criterion 2> — test: <test-file>:<line> — GREEN

Refactor:
- <refactor summary>

Test statistics:
- <count> tests passing
- <count> failures (if any)

Gates passed:
- Scenario Review: <count> approved
- Test Code Review: <count> approved

Next: Run /review for code review.
```
