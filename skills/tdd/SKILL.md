---
name: tdd
description: "Sub-agent orchestrated test-driven development. For each acceptance criterion, Test Sub-Agent designs scenarios and writes tests (RED), human reviews at two gates, Develop Sub-Agent implements (GREEN). After all cycles, unified Refactor. Use when user wants TDD for feature building or bug fixing, mentions red-green-refactor, or wants test-first development."
when_to_use: "TDD,测试,实现,red-green-refactor,test-driven,测试驱动"
dispatch_intent: "Test-driven development, feature implementation, bug fix"
---

# TDD: Test-Driven Development

🥷 Sub-agent orchestrated red-green-refactor, one acceptance criterion at a time.

## Outcome Contract

- **Outcome**: Feature implemented with passing tests, verified through independent sub-agent perspectives and human review gates (mode-dependent: Full/Fast/Batch)
- **Done when**: All acceptance criteria (from input Issue, PRD, or confirmed in Step 1) pass their cycle; unified refactor complete; all tests GREEN
- **Evidence**: Tests turn GREEN per cycle; human approved scenario design and test code at each gate; final refactor passes full suite
- **Output**: Per-cycle results with test locations, test statistics, refactor summary, next step to `/review`

## Core Principles

**Behavior testing through public interfaces.** Tests verify what the system does, not how. Code can change completely; tests should not.

**Sub-agent independence.** Test Sub-Agent and Develop Sub-Agent share no state and each re-reads shared context from disk before acting — see [anti-patterns.md #35](../rules/anti-patterns.md). The re-read checklist is in [REFERENCE.md Sub-Agent Common](REFERENCE.md).

**Two-stage human review (default).** Each acceptance criterion passes through two synchronous gates — Scenario Review Gate (scenario design quality) and Test Code Review Gate (code quality and fidelity). Both gates are blocking; execution halts until the human responds. See [Gate Modes](#gate-modes) for Fast and Batch alternatives.

**Runtime Note:** "Sub-agent" is a logical concept — each phase re-reads all shared context from disk independently (anti-patterns #34, #35). If your runtime supports true parallel sub-agent dispatch, use it. If not, execute phases sequentially — the independence guarantee comes from re-reading shared context from disk, not from concurrent execution timing.

**Vertical slicing.** One acceptance criterion = one independent cycle (design → review → test code → review → implement). The cycle structure enforces vertical slicing naturally — there is no way to batch all tests then implement.

## Input

Accept any of these, in priority order:
1. **Issue reference** (e.g., `#42` or a URL) — read the issue body; use its Acceptance Criteria as the cycle list
2. **PRD file** — read `docs/prd/PRD-NNNN-<title>.md`; extract Requirements and Acceptance Criteria
3. **Direct description** — user describes the behavior to implement; confirm acceptance criteria in Step 1 before proceeding

## Anti-Pattern: Horizontal Slicing

**Don't write all tests then all implementation.** Batch tests test imagined behavior, not actual — they test shape (data structures, function signatures) rather than user-visible behavior, and become insensitive to real changes.

**The Acceptance Criterion Cycle IS vertical slicing.** One cycle per criterion (scenarios → review → test code → review → implement). See [REFERENCE.md](REFERENCE.md) for the cycle diagram.

## Gate Modes

The two-stage Human Review Gate (Scenario Review + Test Code Review) is the **default** for maximum quality control. However, not every feature needs full ceremony. The user may request a lighter mode at any time:

| Mode | Gates per criterion | When to use |
|------|-------------------|-------------|
| **Full** (default) | 2 gates (Scenario + Code) | New features, complex logic, first time implementing this domain |
| **Fast** | 1 gate (Code only — scenarios and code written together) | Experienced user, well-defined criteria, bug-fix TDD, user says "quick tdd" or "skip scenario gate" |
| **Batch** | 1 gate per 2-3 grouped criteria | Homogeneous criteria (e.g., "validate field A", "validate field B"), user says "batch review" |

**Rules:**
- Default is Full mode. Switch only when user explicitly requests or when trivial criteria qualify for Fast/Batch.
- Fast mode: Test Sub-Agent writes scenarios and code in one phase; single gate reviews both.
- Batch mode: group only homogeneous criteria. Different-domain criteria stay in Full mode individually.
- State active mode at start of each cycle.

## Process Summary

**Step 1: Plan** — Apply the [Skill Entry Protocol](../rules/entry-protocol.md). Read input (Issue, PRD, or description). If the input is an Issue, read the PRD path from the Issue body's `Meta → PRD` field and load the corresponding PRD file. If the Issue has no PRD reference, scan `docs/prd/` for a matching PRD-NNNN, or ask the user to confirm.Extract acceptance criteria. **PRD quality check:** if PRD Traceability shows `Created by: /story (minimal PRD)`, note that requirements may not be decision-complete — confirm acceptance criteria with user before proceeding. Confirm interface changes with user. Prioritize behaviors. Identify which Issues/criteria to work on.

**Step 2: Acceptance Criterion Cycle** — For EACH acceptance criterion, run the 5-step loop:
1. **Test Sub-Agent (scenario design)** — design test scenarios as structured table
2. **Scenario Review Gate** — human reviews scenario design
3. **Test Sub-Agent (test code)** — write test code from approved scenarios → RED
4. **Test Code Review Gate** — human reviews test code
5. **Develop Sub-Agent (implementation)** — write code to make test GREEN

**Step 3: Refactor** — After all cycles GREEN, Develop Sub-Agent performs unified refactor: extract duplication, deepen modules, apply SOLID. Run full test suite after each refactor step.

**Step 4: Output** — Produce result summary. If a PRD file exists, fill the `Implemented by` field in its `## Traceability` section with the Issue reference. Update the corresponding Issue's status in the PRD's `Sliced into` list to `— In Progress`.

See [REFERENCE.md](REFERENCE.md) for detailed sub-agent instructions, checklists, and independence constraints.

## Scenario Review Gate

Test Sub-Agent produces a structured scenario table; the human reviews scenario design (coverage, boundaries, scope) before any test code is written. This is the highest-leverage decision in the cycle. Gate is **blocking**. See [REFERENCE.md Chapter 2](REFERENCE.md) for the scenario table format, review checklist, and human response options.

## Test Code Review Gate

Test Sub-Agent writes test code faithful to the approved scenarios (RED by design); the human reviews code quality (public interface use, behavior-not-implementation, fidelity to scenarios). Gate is **blocking**. See [REFERENCE.md Chapter 3](REFERENCE.md) for the review checklist and human response options.

> **Gate Modes:** In Fast mode these two gates collapse into one Test Code Review Gate (scenarios written inline, checklist folds in scenario coverage). In Batch mode, one gate per 2-3 homogeneous grouped criteria. Full mode (two gates) is the default. See [Gate Modes](#gate-modes) above and [REFERENCE.md Chapter 1](REFERENCE.md).

## Per-Cycle Checklist

Each cycle: Test Sub-Agent re-reads context from disk → scenarios cover criterion completely → Scenario Gate passed → test code faithful to approved scenarios, uses public interface only → Code Gate passed → Develop Sub-Agent re-reads context → minimal implementation → test GREEN → no speculative features.

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
| Scenario review skipped in Full mode | Full mode requires two-stage gate — scenario design is the highest-leverage decision. (Fast mode skips scenario gate by design) |
| Sub-agents share internal state | Each sub-agent starts fresh — no inherited context or cached understanding |
| Human says "looks fine" at gate | Use explicit checklist; treat approval as checklist confirmation |
| All criteria use Full mode when trivial ones could use Fast | Gate Modes: ask user if they want to switch to Fast/Batch for simpler criteria |
| Ran TDD on minimal PRD without confirming criteria | PRD quality check: if minimal PRD, confirm acceptance criteria with user first |

## Output

```
TDD complete.

Traceability:
- Source: <Issue #N / PRD <name> / direct description>
- Feature: <feature name> (PRD-NNNN)
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
