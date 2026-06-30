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

A synchronous checkpoint where a human must review and approve sub-agent output before the next phase begins. The gate is blocking — execution halts until the human responds. In the TDD flow, the number of gates per acceptance criterion depends on the **Gate Mode** (ADR 0003):

1. **Full mode (default)** — two gates: **Scenario Review Gate** (human reviews test scenario design: completeness, boundary coverage, reasonableness) and **Test Code Review Gate** (human reviews test code: quality, naming, fidelity to approved scenarios, public interface usage).
2. **Fast mode** — one gate: the Scenario Review Gate collapses into the Test Code Review Gate (scenarios written inline, checklist folds in scenario coverage). Used for bug-fix TDD or well-defined criteria.
3. **Batch mode** — one gate per 2-3 homogeneous grouped criteria.

Full mode is the default; switching to Fast or Batch requires explicit user request.

**Related terms**: Sub-Agent, Test Sub-Agent, Acceptance Criterion Cycle, Gate Mode

**Anti-patterns**:
- Don't skip the Scenario Review Gate in Full mode — scenario design is where the most important decisions happen
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

### Research Record

A durable note capturing technical best practices for one **stack × topic × major-version** combination, produced by the `research` skill. Lives at `docs/research/<stack>-<topic>-<major>.md` (major version is always part of the filename, e.g. `react-concurrent-rendering-18.md`). **Records are immutable** — once written, a record is frozen and captures the best practice *as of* that major version. When a new major ships, a new record is created (`-18.md` → `-19.md`); the old one is never edited. This preserves historical traceability (best-practice evolution across majors is comparable) and avoids edit conflicts. Each record carries a `stack@version` field (full version), a one-line **TL;DR** verdict at the top, and a mandatory `## Sources` section restricted to authoritative sources. This is the smallest reusable unit of the knowledge base — a concrete answer that can be indexed and re-queried without re-searching.

**Related terms**: Stack, Topic, INDEX, TL;DR, Authoritative Source

**Anti-patterns**:
- Don't write a record whose verdict needs a branching matrix ("in case A do X, in case B do Y") — the topic is too broad, split it
- Don't cite a non-authoritative source (blog, tutorial, SO answer) as decision evidence
- Don't drop the major version from the filename — INDEX reads version from the filename
- Don't edit an existing record to "update" it for a new major — create a new `-<newmajor>.md` record instead; the old record stays frozen as historical truth

### Stack

A **leaf technology unit** — a single library, framework, or language with its own independent version number and official source. Examples: `react`, `next`, `postgres`, `go`, `cpp`. A composite platform (e.g. Next.js = React + framework) is **not** one stack; it decomposes into its leaf units, each carrying independent version and source. Stack names are slug-cased (lowercase, hyphenated, special chars and dots stripped): `C++` → `cpp`, `Node.js` → `nodejs`, `PostgreSQL` → `postgres`, `.NET` → `dotnet`.

**Related terms**: Research Record, Topic

**Anti-patterns**:
- Don't create a composite stack slug like `react-nextjs` — decompose into separate leaf stacks

### Topic

A specific question narrow enough to be answered by **a single one-line verdict**. If a topic's verdict requires a branching matrix ("in case A choose X, in case B choose Y"), the topic is too broad and must be split. Examples: `concurrent-rendering`, `presigned-upload`, `index-strategy`. Topics are slug-cased like stacks.

**Related terms**: Research Record, Stack, TL;DR

### INDEX

The searchable entry point to the knowledge base at `docs/research/INDEX.md`. Provides two views over the same records: **By Stack** (records grouped per stack, with version + verdict) and **By Topic** (cross-stack comparison of the same topic across different stacks). Each row links to the full record file. Downstream skills (notably `/think` Step 5) query INDEX first; only on a miss do they start new research.

**Related terms**: Research Record, Stack, Topic

### TL;DR

A 2-3 line block at the top of a Research Record containing the **verdict + key trade-off**. Exists so that downstream skills can make a decision by reading only the TL;DR without loading the full record. The one-line verdict in INDEX is a further distillation of the TL;DR.

**Related terms**: Research Record, INDEX

### Authoritative Source

A source whose authority derives from the technology's official maintainers, not from third-party commentary. **Tier 1 (required)**: official documentation, official source code, official specifications/standards. **Tier 2 (supplementary)**: official changelogs, RFCs, official repo issues/PR discussions. **Excluded**: personal blogs, tutorial sites, unofficial translations, AI-generated content, Stack Overflow answers (unless they link to an official source), community-maintained-but-not-official sites (e.g. cppreference, community-maintained periods of a project's docs), unaccepted RFC/proposal drafts, any comment by a non-maintainer. Every Research Record's `## Sources` field must list at least one Tier 1 source with a directly accessible URL.

**Tier 1 (required, maintainer-authored)**: official documentation, official source code, official specifications/standards (ISO/W3C/ECMA-262 etc.).
**Tier 2 (supplementary only, never sole evidence)**: official changelogs, Accepted/Merged RFCs or proposals (rejected/withdrawn/draft excluded), maintainer-authored official comments (pinned/labeled) in official repos.

**Decision rule**: every verdict needs at least one Tier 1 source as primary evidence; Tier 2 only supplements, never solely supports a verdict.

**Related terms**: Research Record

**Anti-patterns**:
- Don't cite a Tier 2 source as the sole basis for a verdict
- Don't cite a source without a directly accessible URL pointing to the specific page, not a homepage

## Domain Glossary

| Term | Definition | Related |
|------|------------|---------|
| Sub-Agent | Independent execution phase within a skill, re-reads context from disk | Orchestrator, Human Review Gate |
| Orchestrator | SKILL.md entry point that sequences sub-agents | Sub-Agent |
| Human Review Gate | Synchronous human checkpoint; 1-2 gates per criterion per Gate Mode (Full=2, Fast/Batch=1) | Test Sub-Agent, Develop Sub-Agent, Gate Mode |
| Acceptance Criterion Cycle | Per-acceptance-criterion loop: design→review→code→review→implement | Test Sub-Agent, Develop Sub-Agent |
| Gate Mode | TDD gate configuration: Full (2 gates, default), Fast (1 gate, bug-fix/well-defined), Batch (1 gate per 2-3 homogeneous criteria). See ADR 0003 | Human Review Gate |
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
