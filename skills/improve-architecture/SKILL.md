---
name: improve-architecture
description: "Periodically review and improve code architecture. Scan existing PRDs, find deepening opportunities and design debt based on domain language and decision records. Use for regular code health checks or proactive design debt cleanup."
when_to_use: "architecture,improve-architecture,重构,清理,债务,架构审查"
dispatch_intent: "Architecture improvement, design debt cleanup, module deepening, architecture assessment"
---

# Improve Architecture: Review and Improve Code Architecture

🥷 Periodically clean design debt, keep code healthy.

## Outcome Contract

- **Outcome**: Architecture improvement report with findings, priorities, and PRD alignment analysis
- **Done when**: All PRDs scanned, codebase analyzed, findings categorized with priorities and effort estimates
- **Evidence**: Collected code patterns, PRD analysis, architecture alignment assessment
- **Output**: Structured report with blocking/high/medium priority findings

## Prerequisites

Read available domain context before starting. If any are missing, proceed without them and note the limitation in the report:

- `CONTEXT.md` — domain glossary (if missing: scan code naming conventions instead)
- `docs/adr/` — architecture decisions (if missing: no historical decisions to check against)
- `docs/prd/*.md` — product requirements (if missing: report focuses on code patterns only, no PRD alignment analysis)

## Process Summary

**Step 1**: Read domain doc layout — check `docs/agents/domain.md` (if exists) to locate CONTEXT.md, ADR, and PRD paths. Read `docs/agents/repo-map.md` (if exists) to identify cross-repo architecture scope. Read domain context — CONTEXT.md, ADRs, PRDs. If any file is missing, note it and proceed. The scan will be less precise but still useful — code-level design debt signals (duplication, coupling, long functions) don't require domain context to detect.

**Step 2**: Analyze current development direction — extract planned features, check compatibility with existing architecture

**Step 3**: Scan codebase using prioritized strategy — PRD-linked modules first, high-change-frequency modules next, cross-cutting concerns last. Apply objective detection heuristics for each debt signal. Run ADR compliance check against each ADR in `docs/adr/`.

**Step 4**: Analyze findings — categorize as blocking/high priority/medium priority with PRD links. Each finding must have specific location, evidence, and impact.

**Step 5**: Propose improvements — problem, suggestion, benefit, effort (Low/Medium/High with rationale), linked PRD

**Step 6**: Generate report — structured findings with next steps

See [REFERENCE.md](REFERENCE.md) for scanning strategy, detection heuristics, ADR compliance procedure, and extended examples.

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
