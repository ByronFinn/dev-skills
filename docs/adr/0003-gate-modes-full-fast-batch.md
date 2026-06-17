# 0003 - Gate Modes (Full / Fast / Batch)

Date: 2026-06-17

## Status

Accepted

Supersedes [0002 - Two-Stage Human Review Gate for Test Quality](0002-two-stage-human-review-gate.md).

## Context

ADR 0002 established the two-stage Human Review Gate (Scenario Review Gate + Test Code Review Gate) as mandatory for every acceptance criterion. Its stated rationale: scenario design is the highest-leverage decision in TDD, and a dedicated gate for it prevents wasted test-code effort and surfaces wrong-behavior choices early.

In practice, two gates per criterion proved costly for the common cases ADR 0002 itself anticipated:

- **Bug-fix TDD** — the bug already defines the scenario; a separate scenario-design gate adds ceremony without signal.
- **Experienced implementers** — well-defined criteria with obvious scenarios gain little from a dedicated scenario review.
- **Homogeneous criteria** — "validate field A", "validate field B", "validate field C" each repeating a scenario gate is redundant; the design space is identical across the group.

ADR 0002's Negative Consequences explicitly flagged this: *"Some scenarios may be simple enough that two-stage review feels excessive"* and *"Risk of review fatigue on features with many acceptance criteria."* The TDD skill responded with named Gate Modes (Full / Fast / Batch), but as written they conflict with ADR 0002's Decision, which allows no escape hatch. This ADR resolves that conflict by making Gate Modes an authoritative part of the decision rather than an unprincipled deviation.

The decision to make here: under what conditions is a single-gate (or grouped-gate) review an acceptable trade-off against the scenario-design attention that ADR 0002 prioritized?

## Decision

We adopt three **Gate Modes**, with **Full as the default** and explicit user request required to switch to a lighter mode:

| Mode | Gates per criterion | When applicable |
|------|---------------------|-----------------|
| **Full** (default) | 2 — Scenario Review Gate + Test Code Review Gate | New features, complex logic, first time implementing this domain, uncertain or novel scenarios |
| **Fast** | 1 — Test Code Review Gate (scenarios and code written together in one phase) | Bug-fix TDD, experienced user, well-defined criteria, user explicitly requests ("skip scenario gate", "quick tdd") |
| **Batch** | 1 gate per 2-3 **homogeneous** grouped criteria | Repeated near-identical criteria (e.g., a series of field validations sharing one testing pattern), user explicitly requests ("batch review") |

**Rules that preserve ADR 0002's intent:**

- Full mode is the default. Switch only when the user explicitly requests.
- In **Fast** mode, the single Test Code Review Gate's checklist must still include scenario-coverage items (completeness, boundary conditions) — the scenario concern is folded into code review, not dropped.
- In **Batch** mode, only **homogeneous** criteria may be grouped. Criteria from different domains, or with materially different testing patterns, must stay in Full mode individually.
- The user may switch modes mid-skill (e.g., Full for criteria 1-3, then Fast for trivial criteria 4-5).
- The active mode is stated at the start of each cycle so the user knows what to expect.

**What is NOT changed from ADR 0002:**

- The Scenario Review Gate and Test Code Review Gate, when used (Full mode), remain exactly as ADR 0002 defined them — two-stage, blocking, with the same checklists.
- ADR 0001's sub-agent independence constraint applies in all modes — Test Sub-Agent and Develop Sub-Agent always re-read shared context from disk.
- Scenario design remains the highest-leverage decision; Full mode stays the default precisely because ADR 0002's reasoning still holds for the general case.

## Consequences

### Positive

* Ceremony matches the stakes: complex work gets full two-stage review, trivial work doesn't force a redundant gate
* Bug-fix TDD and homogeneous-criteria workflows become practical — removing the main friction that would have pushed users off the sub-agent TDD flow entirely
* Review fatigue on long features is reduced, preserving gate quality where it matters
* ADR 0002's core insight (scenario design deserves dedicated attention) is retained as the default, not discarded
* The skill's existing Gate Modes behavior is now backed by a decision record — the Traceability chain no longer contradicts itself

### Negative

* A weaker default-for-the-moment path now exists, and users may default to Fast out of habit rather than judgment — the "explicit request required" rule is the primary guardrail
* In Fast mode, scenario-design issues are caught one step later (during code review) than in Full mode — slightly more test code may be written before a scenario problem surfaces
* Batch mode creates a partial horizontal slice within the grouped criteria (scenarios for several criteria reviewed together), though bounded to homogeneous groups
* Three modes add cognitive surface to the TDD skill; the "state the active mode each cycle" rule mitigates but doesn't eliminate this

## Alternatives Considered

* **Keep ADR 0002 as-is, no modes (the status quo that prompted this ADR):** Purest fidelity to the scenario-design-as-highest-leverage principle, but the TDD skill had already grown Gate Modes in practice, leaving the decision record in direct conflict with the product — the worst outcome for the Traceability chain.
* **Single mode only, but Fast (drop two-stage entirely):** Maximally efficient, but throws away ADR 0002's core finding that scenario design needs dedicated human attention. Rejected for the same reason ADR 0002 rejected single-gate review.
* **Auto-select mode based on criterion complexity:** Appealing in theory, but complexity assessment is itself a judgment call the human should make; auto-switching would silently downgrade review quality without user awareness.
* **Per-feature fixed mode (set once at skill start):** Simpler than per-criterion switching, but real features mix complex and trivial criteria; forcing one mode for the whole feature re-introduces the fatigue (Full) or quality loss (Fast) this decision is meant to balance.

## References

* Supersedes [0002 - Two-Stage Human Review Gate for Test Quality](0002-two-stage-human-review-gate.md) — ADR 0002's reasoning for Full mode remains the default case; this ADR adds the conditions under which lighter modes are acceptable.
* [0001 - Sub-Agent Orchestration Pattern](0001-sub-agent-orchestration-pattern.md) — Gate Modes are orthogonal to sub-agent independence; all modes retain the re-read-from-disk constraint.
* CONTEXT.md — "Human Review Gate" definition (to be updated to reflect modes per the improve-architecture finding H2).
* `skills/tdd/SKILL.md` Gate Modes section — the skill behavior this ADR authorizes.
