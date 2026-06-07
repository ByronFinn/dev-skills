---
name: improve-architecture
description: "Periodically review and improve code architecture. Scan existing PRDs, find deepening opportunities and design debt based on domain language and decision records. Use for regular code health checks or proactive design debt cleanup."
when_to_use: "architecture,improve-architecture,重构,清理,债务,架构审查"
dispatch_intent: "Architecture improvement, design debt cleanup, module deepening, architecture assessment"
---

# Improve Architecture: Review and Improve Code Architecture

🥷 Periodically clean design debt, keep code healthy.

## Core Principle

Based on domain language, ADRs, and current PRDs, review codebase for improvement opportunities.

**Deep Modules**: Best modules are deep — small interface, deep implementation. Avoid large interface + shallow implementation (complexity leak).

**PRD Alignment**: Architecture improvements should align with current development direction. Check if: new features fit existing architecture, need improvements in advance, or current debt blocks planned features.

## Outcome Contract

- **Outcome**: Architecture improvement report with findings, priorities, and PRD alignment analysis
- **Done when**: All PRDs scanned, codebase analyzed, findings categorized with priorities and effort estimates
- **Evidence**: Collected code patterns, PRD analysis, architecture alignment assessment
- **Output**: Structured report with blocking/high/medium priority findings

## Prerequisites

- `CONTEXT.md` exists (domain glossary)
- `docs/adr/` exists (architecture decisions)
- `docs/prd/*.md` exists (product requirements)

## Process Summary

**Step 1**: Read domain context — CONTEXT.md, ADRs, PRDs

**Step 2**: Analyze current development direction — extract planned features, check compatibility with existing architecture

**Step 3**: Scan codebase — look for design debt signals and deepening opportunities

**Step 4**: Analyze findings — categorize as blocking/high priority/medium priority with PRD links

**Step 5**: Propose improvements — problem, suggestion, benefit, effort, linked PRD

**Step 6**: Generate report — structured findings with next steps

See [REFERENCE.md](REFERENCE.md) for detailed design debt signals and report template.

Shared behavioral constraints: apply [../rules/anti-patterns.md](../rules/anti-patterns.md) when a global anti-pattern is relevant.

## Gotchas

| What happened | Rule |
|---|---|
| Modify working code without verifying | Read and understand code before suggesting |
| Rename without improving structure | Deepen modules, don't just rename |
| Change too much at once | Small improvements, one at a time |
| Ignore domain language | Name based on CONTEXT.md terms |
| Violate historical ADR | Check ADRs, create new ADR if needed |
| Ignore PRD constraints | Check if improvement aligns with planned features |
| Introduce new concept without updating | Sync update to CONTEXT.md |

## Output

```
Improve Architecture complete.

Scan scope:
- PRDs: <count>
- Code files: <count>
- ADRs: <count>

Architecture alignment:
- ✅ Compatible: <count> features
- ⚠️ Needs improvement: <count> features
- ❌ Conflicts: <count> features

Findings:
- Blocking: <count>
- High priority: <count>
- Medium priority: <count>

Suggested next steps:
1. Review blocking issues
2. Create issues for approved improvements
3. Use /story to decompose
4. Use /tdd to implement
```

## Workflow Position

**Independent periodic activity**, not in main development flow:

```
New feature dev: think → grill → story → tdd → review
Bug fix: debug
Independent periodic: improve-architecture (every 2-4 weeks)
```
