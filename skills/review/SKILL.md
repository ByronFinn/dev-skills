---
name: review
description: "Code review, doc sync, and release check. Review code diffs, update local PRD/docs, sync GitHub Issues, handle release/publish follow-through, verify with evidence. Use after task completion, before merge, or before release."
when_to_use: "review,check,把关,publish前,完成,验收"
dispatch_intent: "Code review, doc sync, release check, completion workflow"
---

# Review: Code Review, Doc Sync, and Release Check

🥷 Complete all finish work before merge or release.

Review code diffs, update local files (PRD, docs), sync remote info (Issues, releases), handle release follow-through, verify with evidence.

## Outcome Contract

- **Outcome**: Comprehensive review report with verification status, updated local files, synced GitHub state
- **Done when**: All checks run, findings documented, local files updated, GitHub synced, recommendation clear
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

**Step 7**: Sync GitHub Issues — close completed, update parent

**Step 8**: Handle release follow-through (if approved) — tag, push, publish, reactions

**Step 9**: Generate review report

See [REFERENCE.md](REFERENCE.md) for detailed checklist and report template.

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
