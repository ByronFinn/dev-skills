# Review: Detailed Reference

## Step 1: Collect Context

Extract project context from:
- Current diff (staged + unstaged)
- README, package.json, Makefile, CI configs
- Project public docs and examples
- User-provided task context

## Step 2: Review Code Diff

Check the following aspects:

**Functionality:**
- [ ] Implementation meets requirements
- [ ] Edge cases handled
- [ ] Error handling complete

**Code Quality:**
- [ ] Naming clear and consistent
- [ ] Logic simple and understandable
- [ ] No obvious performance issues
- [ ] No security vulnerabilities (SQL injection, XSS, etc.)

**Test Coverage:**
- [ ] New features have tests
- [ ] Tests cover critical paths
- [ ] Test naming clear

**Documentation:**
- [ ] API changes update docs
- [ ] Breaking changes recorded in CHANGELOG

## Step 3: Identify Project Constraints

From diff and project context, identify:
- Project commands (test, lint, build)
- Generated artifacts
- Risk areas (security, permissions, data migration)
- Release rules (version bump, changelog)

## Step 4: Check Pre-Release Requirements (if applicable)

If this change involves release:
- [ ] Version number updated
- [ ] CHANGELOG updated
- [ ] Release notes prepared
- [ ] CI passes
- [ ] Generated artifacts verified

## Step 5: Verify Evidence

Run necessary verification commands:
- Tests: `npm test` / `pytest` / project test command
- Lint: `npm run lint` / project lint command
- Typecheck: `tsc` / `mypy` / project typecheck
- Build: `npm run build` / project build command

## Step 6: Update Local Files

Check and update related local files:

**PRD Updates:**
- [ ] If task has PRD, update implementation status
- [ ] Check off completed items in PRD's `Acceptance Criteria`
- [ ] Update implementation progress (if any)

**Doc Updates:**
- [ ] API changes update docs
- [ ] README update (if any)
- [ ] CHANGELOG update (breaking changes)

**CONTEXT.md Updates:**
- [ ] New domain terms added
- [ ] Corrected terms updated

**ADRs Updates:**
- [ ] New architecture decisions recorded
- [ ] Outdated decisions marked deprecated

## Step 7: Sync GitHub Issues (only with current-turn authorization)

Do not close, comment on, or update GitHub Issues unless the user explicitly requests that remote sync in the current turn.

**Update Issue Status:**
- [ ] Close completed sub-issues
- [ ] Update parent issue progress
- [ ] Add comments on completion

**Issue Comment Template:**
```markdown
✅ Completed

**Implemented:**
- <item 1>
- <item 2>

**Verification:**
- Tests pass ✅
- Code review approved ✅

**Related files:**
- <file1>
- <file2>
```

## Step 8: Handle Release Follow-Through (only with current-turn authorization)

If user explicitly requests release/publish/push in the current turn:
- Create tag (if applicable)
- Push to remote
- Publish to registry (if applicable)
- Add GitHub release reactions (+1, heart, hooray, rocket, eyes)
- Create/update GitHub Release (if applicable)

If the user only approves the review report, list these as recommended next steps instead of executing them.

## Step 9: Generate Review Report

Output structured report:

```markdown
## Review Report

### Summary
<one-line summary>

### Changes
- <file1>: <change>
- <file2>: <change>

### Issues Found
- <issue 1> (if any)
- <issue 2> (if any)

### Verification
- Tests: <pass/fail>
- Lint: <pass/fail>
- Typecheck: <pass/fail>
- Build: <pass/fail>

### Recommendation
Approve / Request changes / Comments
```

## Security Checklist

Run these on every review:

- [ ] No credentials or keys in diff
- [ ] No hardcoded secrets
- [ ] Input validation present
- [ ] Output encoding/escaping correct
- [ ] SQL queries parameterized
- [ ] File operations validate paths
- [ ] Dependencies checked with the project-supported audit command, or marked not checked with reason
- [ ] Error messages don't leak sensitive info

## Performance Checklist

- [ ] No obvious N+1 queries
- [ ] No unnecessary loops in hot paths
- [ ] Appropriate caching (if applicable)
- [ ] Resource cleanup (connections, handles)
- [ ] Pagination/limiting on list operations

## Review Report Template

```markdown
**Review Complete**

**Summary:** <one-line summary>

**Files changed:** <count> files

**Verification:**
- Tests: ✅ <count> passing
- Lint: ✅ clean
- Typecheck: ✅ no errors
- Build: ✅ success

**Updated files:**
- docs/prd/<name>.md — updated
- CONTEXT.md — updated (if any)
- docs/adr/*.md — updated (if any)

**Synced to GitHub:**
- Issues: <count> closed
- Comments: <count> added

**Recommendation:** ✅ Approve

**Next steps:**
- Ready to merge or release
```
