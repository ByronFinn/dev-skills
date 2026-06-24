# 0002 - Two-Stage Human Review Gate for Test Quality

Date: 2026-06-12

## Status

Superseded by [0003 - Gate Modes (Full / Fast / Batch)](0003-gate-modes-full-fast-batch.md)

The two-stage gate defined here remains the **default** behavior (Full mode in ADR 0003). ADR 0003 adds the conditions under which lighter modes (Fast, Batch) are acceptable; it does not overturn this decision for the general case.

## Context

The refactored TDD skill separates test design from implementation via independent sub-agents. Between them, a Human Review Gate ensures test quality before development begins. The question is: what exactly does the human review?

Two concerns need human judgment:
1. **Scenario design** — Are the right behaviors being tested? Are boundary conditions appropriate? Is the scope correct? This is the highest-leverage decision — a wrong scenario means the wrong thing gets built.
2. **Test code quality** — Does the test code correctly implement the approved scenarios? Does it use public interfaces? Is it free of implementation coupling?

Reviewing both in one step creates an unclear approval criteria: is the human approving the scenario choices, the code quality, or both? Rejecting for a scenario issue when the code is fine (or vice versa) creates confusion about what needs to change.

## Decision

Split the Human Review Gate into two sequential stages per acceptance criterion:

1. **Scenario Review Gate**: Test Sub-Agent produces a structured scenario table (scenario, input, expected output, boundary conditions). Human reviews completeness and reasonableness. Only after scenario approval does test code get written.
2. **Test Code Review Gate**: Test Sub-Agent writes test code from approved scenarios. Human reviews code quality, naming, fidelity to scenarios, public interface usage. Only after code approval does Develop Sub-Agent begin implementation.

This creates the per-acceptance-criterion flow:
```
Test Sub-Agent (scenario design) → Scenario Review Gate → Test Sub-Agent (code) → Test Code Review Gate → Develop Sub-Agent (implementation)
```

## Consequences

### Positive

* Clearer approval criteria at each gate — human knows exactly what they're approving
* Scenario design gets dedicated attention before any code is written
* Catching scenario issues early prevents wasted test code effort
* Test code review is simpler because scenarios are already approved — just check fidelity

### Negative

* Two gates per acceptance criterion increases human interaction overhead
* Slower overall cycle time — each acceptance criterion requires two human responses
* Some scenarios may be simple enough that two-stage review feels excessive
* Risk of review fatigue on features with many acceptance criteria

## Alternatives Considered

* **Single gate (review test code only)**: Faster but scenario design — the highest-leverage decision — gets no dedicated human attention. Humans might miss scenario gaps while focusing on code quality.
* **Single gate (review scenario + code together)**: More efficient but conflates two different concerns. Rejection reasons become ambiguous. Requires the human to context-switch between design review and code review.
* **Batch scenario review (all scenarios for all criteria first, then all code)**: Efficient for human but re-introduces horizontal slicing — losing the vertical-slice benefit of per-criterion iteration.

## References

* CONTEXT.md — Human Review Gate, Acceptance Criterion Cycle definitions
* PRD `docs/prd/PRD-0000-multi-agent-skill-refactor.md` — TDD skill requirements
