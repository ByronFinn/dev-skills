# TDD: Sub-Agent Instruction Reference

Detailed instructions for each phase of the sub-agent orchestrated TDD process. Each chapter is self-contained — an agent reading only that chapter should know exactly what to do.

---

## Chapter 1: Planning Phase (Orchestrator)

### Purpose

The orchestrator reads the user's input, extracts acceptance criteria, confirms scope with the user, and produces an ordered list of acceptance criteria. Each criterion becomes one Acceptance Criterion Cycle handled by the Test Sub-Agent and Develop Sub-Agent in subsequent chapters.

### Reading Input

Accept any of these, in priority order:

**First, apply the Skill Entry Protocol:**
0. Apply the [Skill Entry Protocol](../rules/entry-protocol.md) to locate CONTEXT.md, ADR paths, and multi-repo scope

**If input is an Issue (e.g., `#42` or a URL):**
1. Fetch the issue body via the tracker convention in `docs/agents/issue-tracker.md`
2. Extract `Acceptance Criteria` as the test target list
3. Extract `What to build` as the scope description
4. Confirm understanding with user before proceeding

**If input is a PRD:**
1. Read `docs/prd/PRD-NNNN-<title>.md` (use path from `domain.md` if available)
2. Focus on `Requirements`, `Acceptance Criteria`, and `Technical Approach` sections
3. Extract each acceptance criterion as a separate cycle target

**If input is a direct description:**
1. Confirm scope with the user
2. Derive acceptance criteria collaboratively — ask: "What would prove this works correctly?"
3. Convert the answer into testable acceptance criteria before starting any cycle

### Extracting Acceptance Criteria

- Each acceptance criterion must describe **observable behavior** — what the system does, not how
- Each criterion must be independently testable — no hidden dependencies on other criteria
- If a criterion is ambiguous, clarify with the user before proceeding
- If the input contains no explicit criteria, you must create them with the user in this step

### Confirming Interface Changes

Before starting cycles, confirm with the user:

- What the public interface should look like
- Whether new modules, functions, or API endpoints are needed
- Whether existing interfaces will change
- Whether there are integration points or external dependencies to account for

Ask: "What should the public interface look like? Which behaviors matter most?"

### Prioritizing Behaviors

**You cannot test everything.** Confirm with the user exactly which behaviors are most important. Prioritize by:

1. **Critical paths** — the main user-facing workflows
2. **Complex logic** — algorithms, state machines, business rules
3. **Error handling** — important failure modes
4. **Edge cases** — boundary conditions worth covering

Lower-priority items can be deferred to a later cycle. Focus test work where it matters most.

### Identifying Deep Module Opportunities

Note opportunities for deep modules (small interface, deep implementation) during planning. The definition and principle live in Chapter 5 §Deep Modules Principle (single source). These notes inform the refactor phase (Chapter 5) but should not drive premature design during cycles.

### Planning Checklist

- [ ] Input read and understood (Issue, PRD, or direct description)
- [ ] Acceptance criteria extracted — each describes observable behavior
- [ ] Interface changes confirmed with user
- [ ] Behaviors prioritized (critical paths first)
- [ ] Deep module opportunities noted for refactor phase
- [ ] User approves the plan before any cycle begins

### Output

An ordered list of acceptance criteria. Each criterion will be processed as one Acceptance Criterion Cycle (Chapter 2 → Chapter 3 → Chapter 4).

Example:
```
Acceptance Criteria (ordered):
1. User can create an account with valid email and password
2. User receives error when email is already registered
3. User can log in with correct credentials
4. User receives error with wrong password
5. User session persists across page reloads
```

### Acceptance Criterion Cycle (Visual)

```
WRONG (horizontal slicing):
  RED:   test1, test2, test3, test4, test5
  GREEN: impl1, impl2, impl3, impl4, impl5

RIGHT (Acceptance Criterion Cycle — vertical):
  Cycle 1: scenarios→review→test1→review→impl1
  Cycle 2: scenarios→review→test2→review→impl2
  Cycle 3: scenarios→review→test3→review→impl3
  ...
  Refactor: unified after all cycles GREEN
```

Each cycle completes one criterion end-to-end. The Develop Sub-Agent only sees one approved test at a time and cannot batch.

### Gate Mode Selection

The authoritative Gate Modes table (Full / Fast / Batch) and their switching rules live in [SKILL.md → Gate Modes](SKILL.md#gate-modes). Before starting cycles, confirm the mode with the user (default is Full). Recap of how each mode reshapes the chapters below:

- **Fast mode**: Chapters 2 and 3 merge — Test Sub-Agent designs scenarios and writes code in one phase; the single Test Code Review Gate folds in scenario coverage.
- **Batch mode**: group homogeneous criteria; one Scenario Review Gate and one Test Code Review Gate cover the whole group; Develop Sub-Agent implements each criterion in the group sequentially.

---

## Sub-Agent Common (applies to Chapters 2, 3, 4)

### Independence

Sub-agents share no state and re-read all shared context from disk — see [anti-patterns.md #35](../rules/anti-patterns.md). The operational consequence is the re-read checklist below.

### Shared Context Re-Read Checklist

Every sub-agent re-reads all of the following from disk before starting its phase:

- [ ] PRD file (`docs/prd/PRD-NNNN-<title>.md`) — requirements and acceptance criteria
- [ ] Story/Issue — fetch the latest issue body
- [ ] `CONTEXT.md` — domain glossary and terminology
- [ ] ADRs (`docs/adr/`) — relevant architecture decisions
- [ ] Existing codebase — scan relevant source to understand current interfaces

Each chapter adds **phase-specific** items (the approved artifact from the prior phase, which the human may have edited at a gate).

---

## Chapter 2: Test Sub-Agent — Scenario Design Phase

### Purpose

For one acceptance criterion, design test scenarios as a structured table. This phase produces the scenario table for the Scenario Review Gate — the first human checkpoint. The quality of scenario design determines the quality of everything that follows.

### Phase-Specific Context

Apply the [Sub-Agent Common](#sub-agent-common-applies-to-chapters-2-3-4) independence + shared re-read before designing scenarios. This is the first phase — no approved artifact exists yet for this cycle.

### Responsibilities

For the assigned acceptance criterion:
1. Understand what behavior the criterion requires
2. Identify all scenarios needed to verify that behavior
3. Design scenarios as a structured table
4. Present the table for Scenario Review Gate

### Scenario Table Format

```
| Scenario | Input | Expected Output | Boundary Conditions |
|----------|-------|-----------------|---------------------|
| <description> | <what goes in> | <what comes out> | <edges, limits, edge cases> |
```

Each row is one test case. The table must be complete enough that someone could write test code from it without asking further questions.

### How to Design Good Scenarios

Cover these categories for each acceptance criterion:

1. **Happy path** — the normal, expected usage. Does the core behavior work?
2. **Error cases** — what happens with invalid input, missing data, or precondition failures?
3. **Boundary values** — empty inputs, maximum lengths, zero, negative numbers, off-by-one
4. **Edge cases** — race conditions, concurrent access, unusual state combinations

**Scenario scope guidelines:**
- Each scenario should test one coherent behavior — not too broad (multiple assertions on unrelated things), not too narrow (trivially true)
- Avoid redundant scenarios — two scenarios that prove the same thing
- Include only scenarios that provide meaningful signal — omit trivially true cases

### Example

Acceptance criterion: "User can create an account with valid email and password"

```
| Scenario | Input | Expected Output | Boundary Conditions |
|----------|-------|-----------------|---------------------|
| Valid registration | email="user@example.com", password="Str0ng!Pass" | account created, returns user ID | — |
| Email at max length | email=<255-char valid email>, password="Str0ng!Pass" | account created | RFC 5321 max email length |
| Minimum password length | email="user@example.com", password="Abc123!" (exactly 7 chars if min is 7) | account created | boundary of minimum password rule |
| Duplicate email | email="existing@example.com" (already registered) | error: "email already registered" | — |
| Empty email | email="", password="Str0ng!Pass" | validation error: email required | — |
| Invalid email format | email="not-an-email", password="Str0ng!Pass" | validation error: invalid email | — |
| Password too short | email="user@example.com", password="Ab1!" | validation error: password too short | below minimum length |
```

### Scenario Review Gate

Present the scenario table to the human. The gate is **blocking** — wait for explicit response.

**Human review checklist (provide to human):**
- [ ] All acceptance criterion behaviors covered
- [ ] Boundary conditions identified and appropriate
- [ ] No missing or redundant scenarios
- [ ] Scenario scope is reasonable (not too broad, not too narrow)

**Human response options:**
- **Approve** → proceed to Test Code Phase (Chapter 3)
- **Reject with feedback** → revise scenarios based on feedback, re-present for review

### Output

Approved scenario table for this acceptance criterion. This table becomes the input for the Test Code Phase (Chapter 3).

---

## Chapter 3: Test Sub-Agent — Test Code Phase

### Purpose

Write test code from the approved scenario table. Tests must be RED — they describe required behavior that does not yet exist. This phase produces test code for the Test Code Review Gate — the second human checkpoint.

### Phase-Specific Context

Apply the [Sub-Agent Common](#sub-agent-common-applies-to-chapters-2-3-4) independence + shared re-read. Additionally re-read from disk:

- [ ] Approved scenario table — the human may have edited it during the Scenario Review Gate (human edits are authoritative)

### Responsibilities

1. Convert each approved scenario into a test function
2. Ensure tests are RED (they describe behavior that does not exist yet)
3. Present test code for Test Code Review Gate

### Test Code Checklist

Every test must satisfy ALL of these:

- [ ] **Uses only public interface** — no importing internal modules, no accessing private members, no reaching into internals
- [ ] **Verifies behavior, not implementation** — tests check what the system does (outputs, side effects, state changes), not how it does it
- [ ] **Test naming reflects scenario intent** — test name describes the scenario, e.g., `test_create_account_with_valid_credentials_returns_user_id`
- [ ] **Faithful to approved scenarios** — each test case maps to one row in the approved scenario table, no more, no less
- [ ] **No implementation coupling** — no mocking internal collaborators, no spying on private methods, no testing internal state

### Good Test vs Bad Test

**Good test — behavior through public interface:**
```javascript
// Test describes WHAT the system does
test("user can create account with valid credentials", () => {
  const result = createAccount("user@example.com", "Str0ng!Pass");
  expect(result.status).toBe("success");
  expect(result.userId).toBeDefined();
});
```
- Survives refactoring
- Tests user-visible outcomes
- Clear intent
- Does not care how the account is created internally

**Bad test — coupled to implementation:**
```javascript
// Test describes HOW the system works internally
test("createAccount calls user repository with correct params", () => {
  const spy = jest.spyOn(userRepository, "save");
  createAccount("user@example.com", "Str0ng!Pass");
  expect(spy).toHaveBeenCalledWith({
    email: "user@example.com",
    passwordHash: expect.any(String),
  });
});
```
- Breaks on refactoring
- Tests internal details
- Brittle coupling — renaming `userRepository.save` to `userRepository.insert` breaks the test even though behavior is unchanged

**Bad test — testing private method:**
```javascript
// Private method should be tested through public interface
test("hashPassword uses bcrypt with cost 12", () => {
  const result = hashPassword("mypassword");
  expect(result).toMatch(/^\$2b\$12\$/);
});
```
- If `hashPassword` is worth testing, make it public or test it through the public interface (e.g., verify that stored password can be verified with the correct input)

### Test Code Review Gate

Present the test code to the human. The gate is **blocking** — wait for explicit response.

**Human review checklist (provide to human):**
- [ ] Tests use only public interface
- [ ] Tests verify behavior, not implementation
- [ ] Test naming reflects scenario intent
- [ ] Tests are faithful to approved scenarios
- [ ] No implementation coupling (no mocking internals, no testing private methods)

**Human response options:**
- **Approve** → proceed to Develop Sub-Agent (Chapter 4)
- **Reject with feedback** → revise test code based on feedback, re-present for review

### Output

Approved test code, RED by design. This code becomes the input for the Develop Sub-Agent (Chapter 4).

---

## Chapter 4: Develop Sub-Agent — Implementation Phase

### Purpose

Write minimal code to make the approved test turn GREEN. The Develop Sub-Agent is strictly forbidden from modifying tests — it only writes implementation code.

### Phase-Specific Context

Apply the [Sub-Agent Common](#sub-agent-common-applies-to-chapters-2-3-4) independence + shared re-read. Additionally re-read from disk:

- [ ] Approved test code — the human may have edited it during the Test Code Review Gate; always read the latest version

### Responsibilities

1. Read the approved test code carefully — understand exactly what behavior is required
2. Write the minimal implementation to make the test pass
3. Run the test and confirm it turns GREEN

### Implementation Checklist

- [ ] **Code is minimal for this test only** — implement exactly what the test requires, nothing more
- [ ] **No speculative features** — do not add functionality for future tests or imagined requirements
- [ ] **If test design issue found: STOP** — report to human, do NOT modify the test

### Minimal Implementation Examples

**Test requires:**
```javascript
test("user can create account with valid credentials", () => {
  const result = createAccount("user@example.com", "Str0ng!Pass");
  expect(result.status).toBe("success");
  expect(result.userId).toBeDefined();
});
```

**Correct minimal implementation:**
```javascript
function createAccount(email, password) {
  return { status: "success", userId: generateId() };
}
```

This is correct even though it doesn't validate email format or check for duplicates — those behaviors belong to other acceptance criterion cycles. The implementation is minimal for THIS test only.

**Wrong — speculative implementation:**
```javascript
function createAccount(email, password) {
  if (!isValidEmail(email)) throw new Error("invalid email");
  if (userExists(email)) throw new Error("email already registered");
  if (password.length < 7) throw new Error("password too short");
  // ... 50 more lines of validation and persistence
  return { status: "success", userId: generateId() };
}
```

This adds behavior for tests that don't exist yet. Each acceptance criterion cycle adds its own behavior incrementally.

### Fallback Strategy: When Tests Have Design Problems

The Develop Sub-Agent may discover issues with the test code:

**What to do:**
1. **STOP immediately** — do not attempt to work around the problem
2. **Do NOT modify the test** — the Develop Sub-Agent never touches test code
3. **Report to the human** with a specific description:
   - What the test expects
   - Why the expectation is problematic (contradicts PRD, tests implementation detail, impossible to satisfy, conflicts with another test, etc.)
   - What the test probably should expect instead (if you can suggest a fix)

**Example report:**
```
⚠️ Test design issue found.

Test: "user can create account with valid credentials"
Problem: Test asserts `result.userId` is a UUID, but the PRD (section 3.2) specifies
auto-incrementing integer IDs for this entity.
Suggestion: Change assertion to `expect(typeof result.userId).toBe("number")`.

Human decision needed: Should I proceed with UUID (changing implementation to match test)
or should the test be updated to match PRD?
```

The human decides whether to:
- Send the test back to the Test Sub-Agent for revision
- Accept the test as-is and instruct the Develop Sub-Agent to implement accordingly

### Output

Implementation code. Test turns GREEN. Proceed to the next acceptance criterion cycle (back to Chapter 2), or if all cycles are done, proceed to Refactor Phase (Chapter 5).

---

## Chapter 5: Refactor Phase (Develop Sub-Agent)

### Purpose

After **all** acceptance criterion cycles are GREEN, perform a unified refactor. This is the only phase where structural improvements happen — during cycles, the focus is strictly on making each test pass with minimal code.

### When to Refactor

Refactoring happens **only after**:
- All acceptance criterion cycles are complete
- Every test in the suite is GREEN
- The user has confirmed all cycles are done

**Never refactor while any test is RED.** Get to GREEN first.

### What to Refactor

Look for these improvement opportunities:

1. **Extract duplication** — repeated logic across implementations. Wait until repetition is proven and stable (anti-patterns.md #8) before extracting.
2. **Deepen modules** — move complexity behind simple interfaces. A function with a small public surface but rich internal logic is a deep module. A function that exposes all its internals through a large interface is shallow.
3. **Apply SOLID principles where natural** — do not force SOLID patterns where they add complexity without clarity.
4. **Consider what new code reveals about existing code** — the feature you just built may expose patterns or abstractions that already-existing code could benefit from.

### Deep Modules Principle

See the [Deep Module definitions in Chapter 1](#identifying-deep-module-opportunities). When refactoring, look for opportunities to create deep modules — hide complexity behind simple interfaces. This is the main structural improvement to seek.

### Refactor Rules and Step Sequence

Refactoring changes **structure, not behavior**. No new features; if you find yourself adding functionality, stop and note it as a future acceptance criterion. Run the full test suite after **each** step; tests must stay GREEN (a refactor that breaks a test is wrong, or the test was implementation-coupled — see Chapter 3).

Per step:
1. Identify one refactor candidate (duplication, shallow module, SOLID violation)
2. Make the structural change
3. Run full test suite
4. GREEN → commit the step, find next candidate. RED → revert, the refactor is not safe.

### Refactor Checklist

- [ ] All duplication extracted (or noted as not-yet-stable)
- [ ] Deep module opportunities addressed
- [ ] SOLID principles applied where natural
- [ ] Full test suite GREEN after each step
- [ ] No new behavior introduced
- [ ] Existing tests unchanged (refactor does not touch tests)

**Exception — Implementation-coupled tests:** If a test is discovered to be coupled to implementation details (asserts on private method calls, mocks internal collaborators, verifies mock call counts), the refactor SHOULD fix the test to test through public interface instead. This is not "adding" or "removing" a test — it's making the test behavior-focused so refactoring is safe. Document each test change in the refactor report with the reason.

### Output

Refactored codebase with full test suite GREEN. Report what was refactored and what was intentionally left for later.

---

## Chapter 6: TDD-Specific Mistakes

Mistakes specific to this TDD flow. For the general per-skill gotchas (testing private methods, fragile/implementation-coupled tests, batching across criteria, sub-agent cached context, skipping gates), see [SKILL.md → Gotchas](SKILL.md) and [anti-patterns.md #35](../rules/anti-patterns.md). Those are not repeated here.

**1. Mocking internal collaborators.**
Tests become coupled to implementation details. If you mock `userRepository.save` in an account creation test, the test breaks when you rename the method or switch to a different persistence strategy. Test real integrations where possible; mock only external boundaries (HTTP APIs, file system, time) behind thin adapters.

**2. Writing tests after code.**
This is not TDD — it is just testing. The test-first constraint is what drives good interface design and ensures tests describe intent rather than implementation. If code already exists, the test will unconsciously confirm the implementation rather than specify the behavior.

**3. Skipping the refactor phase.**
Without refactoring, code quality degrades with each cycle. The incremental nature of TDD means each cycle adds minimal code — duplication and shallow abstractions accumulate. The refactor phase is where you pay down that debt.

**4. Testing everything.**
Not all behaviors need tests. Focus on high-value areas: critical paths, complex logic, important edge cases. Trivial getters, simple data pass-through, and one-line delegations rarely justify dedicated tests.

**5. Develop Sub-Agent modifies tests.**
The Develop Sub-Agent must NEVER modify test code. If the test has a design problem, stop and report to the human. The human decides whether to send the test back to the Test Sub-Agent. This separation preserves the independence of perspectives.

**8. Sub-agent uses cached context / shares internal state.**
Stale or shared context produces incorrect implementations and defeats the independence that catches misinterpretations — the PRD may have been updated, the issue may have new comments, CONTEXT.md may have new entries. This is [anti-patterns.md #35](../rules/anti-patterns.md); the re-read procedure is in [Sub-Agent Common](#sub-agent-common-applies-to-chapters-2-3-4).

**9. Batch all scenarios across criteria.**
One acceptance criterion per cycle, enforced by the gate structure. Batching scenarios across criteria is horizontal slicing — the anti-pattern that motivated the sub-agent design. Each cycle completes one criterion end-to-end before starting the next.

**10. Skipping the Scenario Review Gate in Full mode.**
In **Full mode** (the default), the two-stage gate is mandatory — scenario design is the highest-leverage decision in TDD, and skipping the Scenario Review Gate to write test code faster produces poorly designed tests that test the wrong things. In **Fast mode**, the Scenario Review Gate is skipped *by design* (scenario coverage folds into the single Test Code Review Gate); this is not a violation, but it requires an explicit user request. In **Batch mode**, one gate covers a homogeneous group. See ADR 0003 (Gate Modes).

**11. Treating "looks fine" as approval.**
Human review gates use explicit checklists. A vague "looks fine" or "ok" is not a proper review — prompt the human to confirm each checklist item. Approval means checklist confirmation, not casual acknowledgment.

### General Testing Anti-Patterns

**12. Horizontal slicing.**
Writing all tests then all implementation. This produces tests based on imagined behavior rather than actual behavior. Tests end up verifying data shapes and function signatures rather than user-visible outcomes. The Acceptance Criterion Cycle structure enforces vertical slicing — one criterion at a time, end to end.

**13. Test naming that describes implementation.**
```javascript
// Bad — describes implementation detail
test("userService calls bcrypt.compare", () => { ... });

// Good — describes scenario intent
test("login fails with wrong password", () => { ... });
```

**14. Assertions on mock call counts.**
```javascript
// Bad — coupled to implementation
expect(emailService.send).toHaveBeenCalledTimes(1);

// Good — verify observable behavior
expect(result.emailSent).toBe(true);
```

If the implementation changes to send two emails (one welcome, one verification) instead of one, the mock count test breaks even though the behavior of "send an email" is still correct.
---

## Chapter 7: Session Recovery

If the session is interrupted, apply the general recovery procedure (re-read latest user message, re-read shared context from disk, verify on-disk artifacts, state recovery summary, confirm before continuing) from [anti-patterns.md #36](../rules/anti-patterns.md). What follows is the TDD-specific recovery logic #36 does not cover.

### Recovery by Phase

**If interrupted during Planning (Chapter 1):**
- Re-read the input (Issue, PRD, or description) from disk
- Check if acceptance criteria were already extracted — look for any notes or partial output
- Resume from where you left off, or restart planning if no artifacts were created

**If interrupted during an Acceptance Criterion Cycle (Chapters 2-4):**
- Check which cycle was in progress by looking at test files on disk
- Each completed cycle should have a GREEN test file; the latest cycle may have a RED test or no test
- Determine the sub-phase:
  - **Scenario design** — no test file exists yet. Re-read the acceptance criterion, re-design scenarios.
  - **Test code** — test file exists but is RED. Re-read approved scenarios and test code from disk.
  - **Implementation** — test file exists (RED or partially GREEN). Re-read test code and any partial implementation.
- Do NOT assume the scenario table or test code from memory — always re-read from disk

**If interrupted during Refactor (Chapter 5):**
- Run the full test suite first — if all GREEN, refactoring was either not started or completed safely
- If any RED, the refactor was in progress and may be in a broken state. Examine the diff to determine if a partial refactor needs to be reverted or completed.

### Progress Tracking

To aid recovery, output a brief progress marker after each cycle completes:

```
Cycle progress: <n>/<total> — <criterion> GREEN
```

This gives future sessions a clear recovery point.
