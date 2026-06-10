---
name: review
description: "Code review, doc sync, and release check. Review code diffs, verify with evidence, update local PRD/docs when needed, and handle GitHub/release follow-through only when explicitly authorized in the current user turn. Use after task completion, before merge, or before release."
when_to_use: "review,check,把关,发布前,完成开发,验收"
dispatch_intent: "Code review, doc sync, release check, completion workflow"
---

# Review: Code Review, Doc Sync, and Release Check

🥷 Complete all finish work before merge or release.

Review code diffs, verify evidence, update local files (PRD, docs) when needed, and handle remote finish work only when the user explicitly authorizes it in the current turn.

## Outcome Contract

- **Outcome**: Comprehensive review report with verification status, findings, local file updates when needed, and remote sync status when explicitly authorized
- **Done when**: All checks run, findings documented, local file updates completed or listed as follow-up, remote actions completed only if explicitly authorized, recommendation clear
- **Evidence**: Test/lint/typecheck/build output, code diff analysis, updated files
- **Output**: Structured review report with approve/request changes/comments

## Prerequisites

- Code is complete (by `tdd` or manual)
- Uncommitted changes exist (staged or unstaged)

## Process Summary

**Step 1**: Collect context — diff, README, package.json, Makefile, CI configs

**Step 2**: Review code diff — functionality, quality, test coverage, documentation

**Step 3**: Identify project constraints — commands, artifacts, risk areas, release rules

**Step 4**: Check pre-release requirements (if applicable) — version, CHANGELOG, CI, artifacts

**Step 5**: Verify evidence — run tests, lint, typecheck, build

**Step 6**: Update local files — PRD, docs, CONTEXT.md, ADRs

**Step 7**: Sync GitHub Issues only if explicitly authorized in the current user turn — close completed, update parent

**Step 8**: Handle release follow-through only if explicitly authorized in the current user turn — tag, push, publish, reactions

**Step 9**: Generate review report

See [REFERENCE.md](REFERENCE.md) for detailed checklist and report template.

Shared behavioral constraints: apply [../rules/anti-patterns.md](../rules/anti-patterns.md) when a global anti-pattern is relevant.

## Authorization Boundaries

- Default review is local inspection and verification only.
- Local docs/PRD/CONTEXT/ADR updates are allowed when they are necessary to make completed work accurate; otherwise list them as follow-up.
- GitHub issue close/comment/update, tag, push, publish, registry upload, and GitHub Release creation/update require explicit user authorization in the current turn.
- Approval of a draft report or recommendation does not authorize remote or destructive actions.

## Hard Rules

- **Don't assume**: Derive from code/config, don't guess
- **Verify everything**: Run actual commands, don't say "should work"
- **Evidence first**: Every conclusion needs evidence
- **Security first**: Block immediately on any security issue
- **Test coverage**: New code must have tests

## Gotchas

| What happened | Rule |
|---|---|
| Said "should work" without verification | Step 5: Run verification commands |
| Assumed project commands | Step 1: Extract from config |
| Ignored generated artifacts | Step 3: Identify generated artifacts |
| Didn't check security issues | Hard Rules: Security first |
| Didn't verify test coverage | Step 2: Check tests |
| PRD not updated | Step 6: Update local files |
| Issues not closed | Step 7: Sync GitHub Issues |
| Docs out of sync | Step 6: Check doc updates |

## Output

```
Review complete.

Summary: <one-line summary>

Files changed: <count>

Verification:
- Tests: <pass/fail>
- Lint: <pass/fail>
- Typecheck: <pass/fail>
- Build: <pass/fail>

Updated files:
- docs/prd/<name>.md — updated
- CONTEXT.md — updated (if any)
- docs/adr/*.md — updated (if any)

Synced to GitHub:
- Issues: <count> closed
- Comments: <count> added

Recommendation: Approve / Request changes / Comments

Next steps:
- If Approve: Can merge or release
- If Request changes: Fix then re-review
```
