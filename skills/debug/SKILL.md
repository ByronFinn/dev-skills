---
name: debug
description: "Root cause analysis and systematic fix. Quick root cause location, then 6-phase systematic loop for bug fixes. Use when errors, crashes, regressions, test failures, anomalous behavior, or user says 'used to work'."
when_to_use: "debug,排查,报错,崩溃,不工作,regression,以前是好的,broken after update"
dispatch_intent: "Bug fix, root cause analysis, performance regression"
---

# Debug: Root Cause Analysis and Systematic Fix

🥷 Find root cause before fixing.

## Outcome Contract

- **Outcome**: Bug fixed with regression test, root cause documented, debug artifacts cleaned
- **Done when**: Bug no longer reproduces, regression test passes, instrumentation removed, root cause in commit/PR message
- **Evidence**: Reproduction loop passes, test fails on old code/passes on new
- **Output**: Root cause, fix, confirmation, test location, regression guard

## Process Summary

**Stage 0 (Context Setup)**: Apply the [Skill Entry Protocol](../rules/entry-protocol.md) to locate domain docs and identify multi-repo scope. Read `CONTEXT.md` for domain vocabulary that helps form accurate hypotheses.

**Stage 1 (Quick Locate)**: Root cause analysis — form 1-2 hypotheses, validate, output one-sentence root cause

**Stage 2 (Systematic Fix)**: 6-phase loop
- Phase 1: Build feedback loop — construct deterministic repro (the critical skill)
- Phase 2: Reproduce — run loop, confirm bug appears
- Phase 3: Hypothesize — generate 3-5 ranked falsifiable predictions
- Phase 4: Instrument — add targeted logging for each prediction
- Phase 5: Fix + regression test — write test first if correct seam exists
- Phase 6: Cleanup + retrospective — remove debug logs, document proof

See [REFERENCE.md](REFERENCE.md) for detailed phases, optional modes (bisect, scope scan), and quality gates.

Shared behavioral constraints: apply [../rules/anti-patterns.md](../rules/anti-patterns.md) when a global anti-pattern is relevant.

## Optional Modes

**Bisect mode**: Triggered by "used to work", "broke after update", or user recalls specific good commit/version

**Scope scan mode**: Triggered after root fix, before declaring done, or user says "check similar areas"

## Gotchas

| What happened | Rule |
|---|---|
| Fix client pane instead of local pane | Trace execution path before touching files |
| Say "try again" or "I'm confident" | Write hypothesis; run instrumentation to prove |
| MCP not loading, switch tools instead of diagnose | Check server status, API key, config first |
| Compile passes but UI looks wrong | Move up Runtime Evidence Ladder, verify rendered surface |
| Fix one instance, ignore siblings | After fix, grep pattern and fix or report each instance |
| Fix needs >5 files | Pause and confirm scope with user |

## Output (Success)

```
Root cause:    [what broke, file:line]
Fix:           [what changed, file:line]
Confirmation:  [evidence fix works or test]
Test:          [pass/fail count, regression test location]
Regression:    [test file:line] or [none, reason]
```

Status: **resolved**, **resolved with caveats**, or **blocked**.

**Regression guard:** For recurrence, fix not complete until regression test exists (fails on old, passes on new), lives in project suite, and commit message explains why bug recurred and why this fix prevents it.

**PRD Traceability:** If a PRD exists for the affected feature, fill the `Debugged by` field in its `## Traceability` section so downstream skills know a bug fix touched this feature:

```markdown
- **Debugged by**: `/debug` (<YYYY-MM-DD>) — <one-line root cause + fix summary>
```

Next: Run `/review` for code review (recommended for non-trivial fixes). For simple, well-tested fixes with clear regression tests, review is optional.

## Output (Handoff Format after 3 failed hypotheses)

```
Symptom: [original error, one sentence]

Tested hypotheses:
1. [hypothesis 1] → [test method] → [result: excluded due to...]
2. [hypothesis 2] → [test method] → [result: excluded due to...]
3. [hypothesis 3] → [test method] → [result: excluded due to...]

Collected evidence:
- [log snippets / stack traces / file contents]
- [reproduction steps]
- [environment: version, config, runtime]

Excluded:
- [ruled out root causes]

Unknown:
- [what remains unclear]
- [what information is missing]

Suggested next steps:
1. [next investigation direction]
2. [possible external tools or permissions needed]
3. [additional context user should provide]
```

Status: **blocked**

Next: Share this handoff document with a fresh agent session to continue investigation with clean context, or provide additional information (access to environment, captured artifacts, etc.) and re-run /debug.
