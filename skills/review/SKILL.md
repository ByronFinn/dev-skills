---
name: review
description: "Parallel three-perspective code review via sub-agent orchestration. Dispatches Test Review, Code Review, and Impact Review sub-agents in parallel — each independently re-reads all shared context. Merges reports, highlights contradictions for human adjudication. Use after task completion, before merge, or before release."
when_to_use: "review,check,把关,发布前,完成开发,验收,code review"
dispatch_intent: "Code review via parallel sub-agents, doc sync, release check, completion workflow"
---

# Review: Parallel Three-Perspective Review

🥷 Complete all finish work before merge or release.

Dispatches three independent review sub-agents in parallel — Test Review, Code Review, Impact Review — each re-reading all shared context from scratch. Merges their reports into a single comprehensive review. Issue sync and release follow-through require current-turn explicit authorization.

## Outcome Contract

- **Outcome**: Merged three-perspective review report — test quality, implementation quality, and impact analysis — with contradictions highlighted for human adjudication
- **Done when**: All three sub-agent reports produced, merged report presented, local file updates completed or listed as follow-up, remote actions completed only if explicitly authorized
- **Evidence**: Test/lint/typecheck/build output, code diff analysis, updated files
- **Output**: Structured merged report with per-perspective sections, contradiction block (if any), and unified recommendation

## Prerequisites

- Code is complete (by `tdd` or manual)
- Uncommitted changes exist (staged or unstaged)

## Runtime Note

"Parallel sub-agents" means each review perspective independently re-reads all shared context from disk (anti-patterns #37, #38). If your runtime supports true parallel dispatch, dispatch all three simultaneously. If not, execute sequentially — the independence guarantee comes from re-reading shared context from disk, not from concurrent execution timing.

## Process Summary

**Step 1 — Collect context**: Apply the [Skill Entry Protocol](../rules/entry-protocol.md) to locate domain docs, identify multi-repo scope, and check upstream artifacts. Read diff (staged + unstaged), README, package.json, Makefile, CI configs. Gather available shared context paths (PRD, Story, Issues, CONTEXT.md, ADRs). **PRD quality check:** if PRD Traceability shows `Created by: /story (minimal PRD)`, note that requirements may not be decision-complete — review acceptance criteria coverage with extra care.

**Step 2 — Dispatch three parallel review sub-agents**: Each sub-agent independently re-reads all shared context files. No shared internal state between sub-agents. See [Three Sub-Agents](#three-sub-agents) below.

**Step 3 — Merge reports**: Concatenate the three reports. Do not auto-resolve contradictions — flag them explicitly for human adjudication. See [Report Merge Rules](#report-merge-rules).

**Step 4 — Present merged report**: Show the full merged report to the user with per-perspective sections, verification status, contradiction block, and unified recommendation.

**Step 5 — Authorization gate**: Ask the user what to do next. Options: approve and merge, fix issues then re-review, proceed to release. Local doc updates are allowed when necessary; remote actions require current-turn explicit authorization.

**Step 6 — Execute authorized actions**: Perform only actions the user explicitly requested in the current turn — local file updates, issue sync, release follow-through. See [Authorization Boundaries](#authorization-boundaries).

See [REFERENCE.md](REFERENCE.md) for detailed sub-agent instructions, checklists, and report templates.

Shared behavioral constraints: apply [../rules/anti-patterns.md](../rules/anti-patterns.md) when a global anti-pattern is relevant.

## Three Sub-Agents

Each sub-agent is an independent review perspective. They run in parallel, each re-reading all shared context from scratch (PRD, Story, Issues, CONTEXT.md, ADRs, diff). No sub-agent sees another sub-agent's output until the merge step.

| Sub-Agent | Focus Area |
|---|---|
| **Test Review** | Test quality, boundary coverage, test design reasonableness, naming, isolation, mock usage |
| **Code Review** | Implementation quality, security, performance, code conventions, error handling, readability |
| **Impact Review** | Change scope, regression risk, compatibility, architecture health (local to this change), tech debt introduced, release strategy (feature flags, canary, rollback plan). Suggests `/improve-architecture` for global architecture concerns |

### Sub-Agent Independence (anti-pattern #38)

Every sub-agent must independently re-read all shared context. A sub-agent must not carry over conclusions, file reads, or understanding from another sub-agent or from a previous skill invocation. Each builds its perspective from raw context.

## Report Merge Rules

1. **Concatenate** — present each sub-agent's report as a distinct section (Test, Code, Impact)
2. **Contradictions** — if two or more sub-agents reach conflicting conclusions about the same item, extract those into a dedicated `Contradictions` block. Present each side's reasoning. Do not auto-resolve — the human adjudicates
3. **Unified recommendation** — after all perspectives and contradictions, state a single recommendation (Approve / Request Changes / Comments). If sub-agents disagree on recommendation, the recommendation is "Request Changes" and the disagreement is listed in the Contradictions block
4. **No silent resolution** — never drop or merge away a sub-agent's finding to avoid presenting a contradiction

## Authorization Boundaries

- Default review is local inspection and verification only.
- Local docs/PRD/CONTEXT/ADR updates are allowed only when the review has verified the underlying change — never update speculatively or for forward-looking statements. When in doubt, list as follow-up.
- **Issue body update / add comment** — allowed when necessary to reflect completed work (the review verified the code). Equivalent to local doc sync.
- **Issue close / status change / label change** — requires explicit user authorization in the current turn. These are public, irreversible signals.
- Tag, push, publish, registry upload, and release creation/update — require explicit user authorization in the current turn.
- Approval of a draft report or recommendation does not authorize remote or destructive actions.

## Hard Rules

- **Security first**: Block immediately on any security issue. Code Review Sub-Agent runs the full Security Checklist in REFERENCE.md before approving any diff.
- **Test coverage**: New code must have tests. Test Review Sub-Agent verifies this independently.
- **Evidence first**: Every conclusion needs evidence. Run actual commands — never say "should work".
- **Don't assume**: Derive from code/config, don't guess.

## Integration Review

When all vertical slices of a PRD are complete (user says "review all", "integration check", or the review detects the last child issue of a PRD), perform additional checks beyond single-slice review:

- **Cross-slice data flow**: Do the slices integrate correctly when combined?
- **Shared state consistency**: Do slices agree on data models, state transitions, event payloads?
- **Full PRD acceptance criteria coverage**: Are ALL acceptance criteria from the PRD met across all child issues?
- **Integration test coverage**: Are there tests that verify slices working together, not just unit tests per slice?
- **Dependency order verification**: Were slices implemented in the correct dependency order?

State explicitly: "Integration Review — checking <N> slices for PRD <name>."

## Gotchas

| What happened | Rule |
|---|---|
| Sub-agent reused context from another sub-agent | Independence rule: each sub-agent re-reads all shared context from scratch (anti-pattern #38) |
| Contradictions silently resolved in merge | Report Merge Rules: extract to Contradictions block, present both sides |
| Said "should work" without verification | Hard Rules: run verification commands |
| Assumed project commands | Step 1: extract from config |
| Didn't check security issues | Hard Rules: Security first — Code Review Sub-Agent runs Security Checklist |
| Impact Review drifts into global architecture review | Impact Review scope: local impact only. Suggest `/improve-architecture` for global concerns |
| Sub-agents run sequentially when parallel is possible | Runtime Note: dispatch in parallel if runtime supports it; sequential is acceptable fallback |
| PRD not updated after review | Step 6: update local files when authorized |
| Issues closed without authorization | Authorization Boundaries: close/status/label requires current-turn authorization |
| Sub-agent skipped re-reading shared context | Independence rule: never cache file reads from previous skill or sub-agent (anti-pattern #37, #38) |

## Output

```
Review complete.

Traceability:
- Source: <Issue #N / PRD <name>>
- Feature: <feature name>
- Files changed: <count>
- Tests added: <count>

── Test Review ──
<Test Review Sub-Agent report>

── Code Review ──
<Code Review Sub-Agent report>

── Impact Review ──
<Impact Review Sub-Agent report>

── Contradictions ──
<If any sub-agents disagreed, list each with both sides' reasoning>
<If none: "No contradictions between perspectives.">

── Verification ──
- Tests: <pass/fail>
- Lint: <pass/fail>
- Typecheck: <pass/fail>
- Build: <pass/fail>

── Findings ──
New domain terms (for CONTEXT.md):
- <term>: <definition> (if any)

New decisions (for ADR):
- <decision summary> (if any)

Updated files:
- docs/prd/<name>.md — updated
- CONTEXT.md — updated (if any)
- docs/adr/*.md — updated (if any)

Synced:
- Issues: <count> closed
- Comments: <count> added

Recommendation: Approve / Request Changes / Comments

Next steps:
- If Approve: Can merge or release
- If Request Changes (minor): Fix issues → /review again
- If Request Changes (scope change): Re-evaluate with /think or /grill if requirements changed, then /tdd → /review
- If global architecture concerns surfaced: Run /improve-architecture
```
