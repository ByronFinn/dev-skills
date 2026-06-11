---
name: tdd
description: "Test-driven development. Build features or fix bugs using red-green-refactor loop. One vertical slice at a time, test behavior not implementation details. Use when user wants TDD for feature building or bug fixing, mentions red-green-refactor, or wants test-first development."
when_to_use: "TDD,测试,实现,red-green-refactor,test-driven"
dispatch_intent: "Test-driven development, feature implementation, bug fix"
---

# TDD: Test-Driven Development

🥷 Red-green-refactor, one test at a time.

## Outcome Contract

- **Outcome**: Feature implemented with passing tests, code behavior verified
- **Done when**: All acceptance criteria (from input Issue, PRD, or confirmed in Step 1) pass, tests cover public interface behavior
- **Evidence**: Failing tests turn green, implementation passes all tests
- **Output**: Behavior list with test locations, test statistics, next step to `/review`

## Core Principle

**Tests should verify behavior through public interfaces, not implementation details.** Code can change completely; tests should not.

**Good tests** are integration-style: exercise real code paths through public API. Describe **what** system does, not **how**. Survive refactoring because they don't care about internal structure.

**Bad tests** couple to implementation: mock internal collaborators, test private methods, verify externally. Warning sign: tests fail during refactoring when behavior unchanged.

## Input

Accept any of these, in priority order:
1. **Issue reference** (e.g., `#42` or a URL) — read the issue body; use its Acceptance Criteria as the test target list
2. **PRD file** — read `docs/prd/<feature-name>.md`; extract Requirements and Acceptance Criteria
3. **Direct description** — user describes the behavior to implement; confirm acceptance criteria in Step 1 before proceeding

## Anti-Pattern: Horizontal Slicing

**Don't write all tests then all implementation.** This produces bad tests:
- Batch tests test **imagined** behavior, not **actual** behavior
- End up testing **shape** (data structures, function signatures) not user-visible behavior
- Tests become insensitive to real changes — pass when behavior breaks, fail when behavior correct

**Correct method:** Vertical slicing via tracer bullets. One test → one implementation → repeat.

```
WRONG (horizontal):
  RED:   test1, test2, test3, test4, test5
  GREEN: impl1, impl2, impl3, impl4, impl5

RIGHT (vertical):
  RED→GREEN: test1→impl1
  RED→GREEN: test2→impl2
  RED→GREEN: test3→impl3
  ...
```

## Process Summary

**Step 1**: Plan — read input (Issue, PRD, or description), extract acceptance criteria, confirm interface changes with user, prioritize behaviors, identify deep module opportunities

**Step 2**: Tracer bullet — write ONE test confirming ONE thing → test fails → write minimal code → test passes

**Step 3**: Incremental loop — repeat for each remaining behavior

**Step 4**: Refactor — after all green, extract duplication, deepen modules, apply SOLID

See [REFERENCE.md](REFERENCE.md) for detailed checklist and examples.

## Per-Cycle Checklist

```
[ ] Test describes behavior, not implementation
[ ] Test uses only public interface
[ ] Test survives internal refactoring
[ ] Code minimal for this test
[ ] No speculative features added
```

Shared behavioral constraints: apply [../rules/anti-patterns.md](../rules/anti-patterns.md) when a global anti-pattern is relevant.

## Gotchas

| What happened | Rule |
|---|---|
| Batch write tests then implement | Use vertical slicing: test→impl, repeat |
| Tests fail when renaming function | Test behavior, not implementation |
| Test private methods | Test public interfaces |
| Mock internal collaborators | Test real integrations |
| Tests pass but behavior broken | Tests describe observable behavior |
| Refactor while RED | Get to GREEN first |

## Output

```
TDD complete.

Implemented behaviors:
* <behavior 1> — test: <test-file>:<line>
* <behavior 2> — test: <test-file>:<line>

Test statistics:
- <count> tests passing
- <count> failures (if any)

Next: Run /review for code review.
```
