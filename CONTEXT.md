# Context

## Core Concepts

### Sub-Agent

A logical execution unit within a skill that operates with independent context. A sub-agent re-reads all shared context files (PRD, Story, Issues, CONTEXT.md, ADRs) from disk before acting, and does not inherit any internal state or cached understanding from other sub-agents or the orchestrating skill.

**Related terms**: Orchestrator, Human Review Gate

**Anti-patterns**:
- Don't confuse "sub-agent" with a separate top-level skill — it is an internal execution phase of an existing skill
- Don't assume sub-agents share memory or conversation context

### Orchestrator

The SKILL.md entry point of a multi-phase skill. The orchestrator defines the sequence and dependencies between sub-agents, but does not perform implementation work itself. It delegates to sub-agents described in REFERENCE.md.

**Related terms**: Sub-Agent

### Human Review Gate

A synchronous checkpoint where a human must review and approve sub-agent output before the next phase begins. The gate is blocking — execution halts until the human responds. In the TDD flow, there are two gates per acceptance criterion:

1. **Scenario Review Gate** — human reviews test scenario design (completeness, boundary coverage, reasonableness) before test code is written
2. **Test Code Review Gate** — human reviews test code (quality, naming, fidelity to approved scenarios, public interface usage) before implementation begins

**Related terms**: Sub-Agent, Test Sub-Agent, Acceptance Criterion Cycle

**Anti-patterns**:
- Don't skip the Scenario Review Gate and jump straight to test code — scenario design is where the most important decisions happen
- Don't treat "looks fine" as approval — use the explicit checklist

### Acceptance Criterion Cycle

The basic unit of work in the refactored TDD skill. For each acceptance criterion in an Issue, the system runs:

1. Test Sub-Agent → design test scenarios (table: scenario, input, expected output, boundary conditions)
2. Scenario Review Gate → human approves/rejects scenario design
3. Test Sub-Agent → write test code from approved scenarios (RED)
4. Test Code Review Gate → human approves/rejects test code
5. Develop Sub-Agent → implement code to make test GREEN

After all cycles complete, Develop Sub-Agent performs a unified Refactor phase.

This preserves vertical slicing while achieving sub-agent independence and two-stage human quality control.

**Related terms**: Test Sub-Agent, Develop Sub-Agent, Human Review Gate

### Test Sub-Agent

The sub-agent responsible for test design and test code. For each acceptance criterion, it has two phases:

1. **Scenario Design phase**: independently reads shared context, designs test scenarios and boundary conditions as a structured table. Output goes to Scenario Review Gate.
2. **Test Code phase**: after scenario approval, writes test code faithful to the approved scenarios. Tests are RED by design. Output goes to Test Code Review Gate.

**Related terms**: Develop Sub-Agent, Human Review Gate, Acceptance Criterion Cycle

### Develop Sub-Agent

The sub-agent responsible for implementation. For each acceptance criterion, after Test Code Review Gate approval, it independently re-reads shared context plus the approved test, and writes minimal code to make the test GREEN. After all acceptance criterion cycles complete, Develop Sub-Agent performs a unified Refactor phase (extract duplication, deepen modules, apply SOLID).

**Related terms**: Test Sub-Agent, Human Review Gate, Acceptance Criterion Cycle

### Review Sub-Agent

One of three parallel sub-agents within the Review skill: Test Review, Code Review, or Impact Review. Each independently re-reads all shared context and produces a separate report. Reports are merged by the orchestrator.

**Related terms**: Orchestrator, Test Review Sub-Agent, Code Review Sub-Agent, Impact Review Sub-Agent

## Domain Glossary

| Term | Definition | Related |
|------|------------|---------|
| Sub-Agent | Independent execution phase within a skill, re-reads context from disk | Orchestrator, Human Review Gate |
| Orchestrator | SKILL.md entry point that sequences sub-agents | Sub-Agent |
| Human Review Gate | Two-stage synchronous human checkpoint (scenario + code review) | Test Sub-Agent, Develop Sub-Agent |
| Acceptance Criterion Cycle | Per-acceptance-criterion loop: design→review→code→review→implement | Test Sub-Agent, Develop Sub-Agent |
| Test Sub-Agent | Designs test scenarios + writes test code per acceptance criterion (RED) | Develop Sub-Agent, Human Review Gate |
| Develop Sub-Agent | Implements code to make approved test GREEN + unified refactor | Test Sub-Agent |
| Test Review Sub-Agent | Reviews test quality, boundary coverage, test design | Review Sub-Agent |
| Code Review Sub-Agent | Reviews implementation quality, security, performance | Review Sub-Agent |
| Impact Review Sub-Agent | Full-chain impact analysis including release strategy | Review Sub-Agent |

## Key Relationships

```
Orchestrator --sequences--> Sub-Agent
Test Sub-Agent --scenarios_to--> Scenario Review Gate --approves_to--> Test Sub-Agent (code phase)
Test Sub-Agent (code) --test_to--> Test Code Review Gate --approves_to--> Develop Sub-Agent
Review Orchestrator --parallel--> Test Review ∥ Code Review ∥ Impact Review
Issue --contains--> Acceptance Criteria --each_becomes--> Acceptance Criterion Cycle
```
