# Debug: Detailed Reference

## Phase 1: Root Cause Analysis (Quick Location)

**Goal:** Quickly locate root cause, output one-sentence root cause statement.

**Steps:**
1. Understand symptom: User-described error/anomaly/failure
2. Quick hypothesis: Form 1-2 hypotheses based on experience
3. Quick validation: Validate hypothesis via logs, breakpoints, or tests
4. Output root cause: One-sentence root cause statement

**Success signals:**
- You can predict next error
- You understand propagation path from root cause to symptom
- You can write test that fails on old code

**Quality gate:** Before acting on hypothesis, list all observable symptoms (not just first user-reported). Hypothesis must explain each symptom; if only covers some, it's symptom-level guess, not root cause.

**Escalation condition:** If 3 hypotheses fail, escalate to Phase 2 full 6-phase loop.

## Phase 2: 6-Phase Loop (Systematic Fix)

### Phase 1 — Build Feedback Loop

**This is the skill.** Everything else is mechanical. With fast, deterministic, agent-runnable bug pass/fail signal, you'll find cause — bisection, hypothesis testing, instrumentation just consume that signal. Without it, staring at code won't help.

**Spend disproportionate effort here. Be aggressive. Be creative. Refuse to give up.**

**How to build one — try in order:**
1. **Failing test** at any seam reaching bug — unit, integration, e2e
2. **Curl / HTTP script** against running dev server
3. **CLI invocation** with fixture input, diff stdout against known-good snapshot
4. **Headless browser script** (Playwright / Puppeteer) — drive UI, assert DOM/console/network
5. **Replay captured trace**. Save real network request/payload/event log to disk; replay through code path in isolation
6. **One-time harness**. Spin minimal system subset, exercise bug code path with one function call
7. **Property / fuzz loop**. If bug is "sometimes wrong output", run 1000 random inputs, look for failure pattern
8. **Bisection harness**. If bug appears between two known states (commit, dataset, version), automate "boot state X, check, repeat" so you can `git bisect run` it
9. **Differential loop**. Run same input through old-version vs new-version (or two configs) and diff output
10. **HITL bash script**. Last resort. If human must click, use `scripts/hitl-loop.template.sh` to drive them, keeping loop structured. Capture output feedback for you.

**Iterate on the loop itself.** Treat loop as product. Once you have loop, ask:
- Can I make it faster? (cache setup, skip irrelevant init, narrow test scope)
- Can I make signal clearer? (assert specific symptoms, not "didn't crash")
- Can I make it more deterministic? (fix time, seed RNG, isolate fs, freeze network)

Build right loop, bug 90% fixed.

**Non-deterministic bugs:**
Goal isn't clean repro but **higher repro rate**. Trigger loop 100×, parallelize, add stress, narrow time window, inject sleeps. 50%-flake bug is debuggable; 1% isn't — keep raising rate until debuggable.

**When you truly cannot build loop:**
Stop and state explicitly. List what you tried. Request user provide: (a) access to environment reproducing it, (b) captured artifacts (HAR file, log dump, core dump, timestamped screen recording), or (c) permission to add temporary production instrumentation. **Don't proceed without loop.**

Don't enter Phase 2 until you believe a loop.

### Phase 2 — Reproduce

Run loop. See bug appear.

Confirm:
- [ ] Loop produces user-reported failure mode — not different failure nearby. Wrong bug = wrong fix.
- [ ] Failure reproducible across multiple runs (or, for non-deterministic bugs, at sufficient rate to be debuggable)
- [ ] You captured exact symptom (error message, wrong output, slow timing) so later phases can verify fix actually solved it

Don't proceed until you reproduce bug.

### Phase 3 — Hypothesize

Generate **3-5 ranked hypotheses** before testing any. Single hypothesis generation anchors on first reasonable idea.

Each hypothesis must be **falsifiable**: State its prediction.
> Format: "If <X> is cause, then <change Y> will make bug disappear / <change Z> will make it worse."

If you can't state prediction, hypothesis is vibe — discard or sharpen.

**Present ranked list to user before testing.** They often have domain knowledge to immediately re-rank ("we just deployed change affecting #3"), or know what they already excluded. Cheap checkpoint, big time-saver. Don't block — if user AFK, continue with your ranking.

### Phase 4 — Instrument

Each probe must map to Phase 3's specific prediction. **Change one variable at a time.**

Tool preference:
1. **Debugger / REPL inspection** if environment supports. One breakpoint > ten logs.
2. **Targeted logging** at boundaries distinguishing hypotheses.
3. Never "log everything and grep."

**Perf branch.** For performance regression, logs often wrong. Instead: establish baseline measurement (timing harness, `performance.now()`, profiler, query plan), then bisect. Measure first, fix second.

**Mark each debug log** with unique prefix, e.g., `[DEBUG-a4f2]`. Cleanup becomes single grep at end. Unmarked logs survive; marked logs die.

### Phase 5 — Fix + Regression Test

**Write regression test before fix** — but only when **correct seam** exists.

Correct seam tests **real bug pattern** at call site. If only available seam too shallow (single-caller test when bug needs multiple callers, unit test can't replicate triggering bug chain), regression test there gives false confidence.

**If correct seam doesn't exist, that's itself a finding.** Note it. Codebase architecture prevents bug being locked. Flag for next phase.

If correct seam exists:
1. Convert minimal repro to failing test at that seam
2. See it fail
3. Apply fix
4. See it pass
5. Run Phase 1 feedback loop on original (non-minimal) scenario

### Phase 6: Cleanup + Retrospective

Required before done:
- [ ] Original repro no longer reproduces (re-run Phase 1 loop)
- [ ] Regression test passes (or seam doesn't exist, noted)
- [ ] All `[DEBUG-...]` instrumentation removed (`grep` prefix)
- [ ] One-time prototypes deleted (or moved to clearly marked debug location)
- [ ] Proven hypothesis stated in commit / PR message — so next debugger learns

**Then ask: what would prevent this bug?** If answer involves architecture change (no good test seam, tangled callers, hidden coupling), handoff to `/improve-architecture` with details. Suggest after fix, not before — you have more info now.

## Optional Modes

### Bisect Mode

Triggered by: "used to work", "broke after update", or user recalls specific good commit/version.

0. First protect user's worktree: run `git status --short --branch -uall`. If modified/staged/untracked files exist, don't bisect in current checkout. Create temporary detached worktree from same HEAD, run bisect there, then `git bisect reset` and delete temp worktree when done. If temp worktree impossible, stop and request explicit cleanup/stash approval.
1. Find candidate good tag: `git tag --sort=-version:refname | head -10` or ask user last known good commit.
2. Before starting bisect, define non-interactive pass/fail test command. Bisect without reproducible check has no value.
3. Run: `git bisect start && git bisect bad HEAD && git bisect good <tag-or-hash>`
4. At each step bisect checks out one commit. Run test command. Mark: `git bisect good` or `git bisect bad`.
5. Let bisect drive. Don't skip or re-order commits unless explicitly asked.
6. When bisect names culprit commit, only read that diff. Identify specific line introducing regression.
7. When done, run `git bisect reset`.

Read large file once and reference from notes, not re-read at each bisect step.

### Scope Scan Mode

Triggered after root cause pattern fixed, before declaring bug done, or user says "check if this exists elsewhere".

1. Extract pattern signature: specific function name, regex, API call, CSS selector, lock acquisition, validation skip, or input boundary producing bug.
2. `grep -rn <pattern>` across repo (exclude generated dirs, build output, vendored deps). For class-of-bug patterns (e.g., "any handler missing lock"), grep surrounding shape, not just literal text.
3. List each match. For each, answer in writing: same bug here? Choose fix / leave (explain why safe) / unsure (ask user). Don't silently skip matches.
4. Don't claim "fixed" until scope report in Outcome block.

Common triggers:
- Fix visual bug on one page: check every other page using same component, layout, or media-query breakpoint
- Fix race in one handler: check every handler acquiring same lock or touching same shared state
- Fix validation skip at one entry point: check every entry point reaching same downstream sink
- Fix regex/parser for one input shape: check every caller of same regex/parser

If scope scan exposes unrelated bugs, list but don't fix in this PR unless user agrees; scope creep is its own anti-pattern.

## Quality Gates

### Phase 1 Gate

List all observable symptoms before hypothesizing:
- User-reported error
- Console warnings (if any)
- Performance degradation (if any)
- Side effects in other features (if any)

Hypothesis must explain ALL symptoms, not just primary one.

### Phase 3 Gate

Before testing hypotheses, verify each is falsifiable:
- Can you state what specific change would disprove it?
- Can you measure the prediction?

If not, sharpen hypothesis before proceeding.

### Phase 5 Gate

Before declaring fix done:
- [ ] Original repro scenario passes
- [ ] Regression test at correct seam passes
- [ ] No new tests failing
- [ ] Fix is minimal (no unrelated changes)

## Example: Debug Loop Construction

**Bad approach:**
```
User: "Feature X crashes when I click button"
Agent: "Let me add logs to figure out why"
[Adds 20 log lines everywhere]
[Runs through UI manually]
"This will take a while to debug..."
```

**Good approach:**
```
User: "Feature X crashes when I click button"
Agent: "Let me build a repro loop I can run deterministically."

[Writes Playwright script that clicks button and captures error]
[Runs script 10x, confirms 100% crash rate]
"Repro built: 100% crash rate with [error message]. Now I'll form hypotheses."

Hypothesis 1: Null state when button clicked
Hypothesis 2: Race condition in event handler
Hypothesis 3: Missing error boundary

[Test Hypothesis 1: Add log for state, run script]
→ State not null, exclude.

[Test Hypothesis 2: Add delay before click, run script]
→ Still crashes, exclude.

[Test Hypothesis 3: Check if error boundary exists]
→ Missing boundary, this is root cause.

[Fix: Add error boundary]
[Regression test: test error boundary catches errors]
[Run original repro: passes]

Done.
```
