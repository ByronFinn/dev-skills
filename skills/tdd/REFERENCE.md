# TDD: Detailed Reference

## Step 1: Plan

Before writing code:
- [ ] Confirm interface changes with user
- [ ] Confirm which behaviors to test (prioritized)
- [ ] Identify [deep modules](https://www.youtube.com/watch?v=ZCuS flirtde6A) opportunities (small interface, deep implementation)
- [ ] Design interfaces for [testability](https://testingjavascript.com/)
- [ ] List behaviors to test (not implementation steps)
- [ ] Get user approval for plan

Ask: "What should the public interface look like? Which behaviors matter most?"

**You cannot test everything.** Confirm with user exactly which behaviors are most important. Focus test work on critical paths and complex logic, not every possible edge case.

## Step 2: Tracer Bullet

Write **one** test that confirms system does **one thing**:

```
RED:   Write first behavior test → test fails
GREEN: Write minimal code to pass → test passes
```

This is your tracer bullet — proves path works end-to-end.

## Step 3: Incremental Loop

For each remaining behavior:

```
RED:   Write next test → fails
GREEN: Write minimal code to pass → passes
```

Rules:
- One test at a time
- Only enough code to pass current test
- Don't predict future tests
- Keep tests focused on observable behavior

## Step 4: Refactor

After all tests pass, look for refactor candidates:
- [ ] Extract duplication
- [ ] Deepen modules (move complexity behind simple interface)
- [ ] Apply SOLID principles where natural
- [ ] Consider what new code reveals about existing code
- [ ] Run tests after each refactor step

**Never refactor while RED.** Get to GREEN first.

## Horizontal vs Vertical Slicing

**Horizontal slicing (anti-pattern):**
```
Phase 1 (RED):   Write ALL tests
Phase 2 (GREEN): Write ALL implementations
```

Problems:
- Tests are based on imagination, not actual behavior
- Tests verify structure (signatures, data shapes) not behavior
- Tests become brittle — fail when renaming, pass when breaking
- Run too fast, commit to test structure before understanding implementation

**Vertical slicing (correct):**
```
Cycle 1: test1 → impl1
Cycle 2: test2 → impl2
Cycle 3: test3 → impl3
...
```

Benefits:
- Each test responds to learning from previous cycle
- Know exactly what behavior matters and how to verify it
- Tests describe actual behavior, not imagined

## Behavior vs Implementation Testing

**Behavior testing (good):**
```javascript
// Test describes WHAT system does
test("user can checkout with valid cart", () => {
  const result = checkout(validCart);
  expect(result.status).toBe("success");
  expect(result.orderId).toBeDefined();
});
```
- Survives refactoring
- Tests user-visible outcomes
- Clear intent

**Implementation testing (bad):**
```javascript
// Test describes HOW system works internally
test("checkout calls payment processor", () => {
  const spy = jest.spyOn(PaymentProcessor, "charge");
  checkout(validCart);
  expect(spy).toHaveBeenCalledWith(expectedArgs);
});
```
- Breaks on refactoring
- Tests internal details
- Brittle coupling

## Deep Modules Principle

From "A Philosophy of Software Design":

- **Shallow module**: Small interface, shallow implementation (not worth having)
- **Deep module**: Small interface, deep implementation (ideal)
- **Avoid**: Large interface, shallow implementation (complexity leak)

When refactoring, look for opportunities to create deep modules — hide complexity behind simple interfaces.

## Common TDD Mistakes

1. **Testing private methods**: If method is worth testing, it should be public or tested through public interface
2. **Mocking internal collaborators**: Tests become coupled to implementation details
3. **Writing tests after code**: Not TDD, just testing
4. **Skipping refactor phase**: Code quality degrades
5. **Testing everything**: Not all behaviors need tests; focus on high-value areas
6. **Fragile tests**: Tests that fail on refactoring indicate implementation coupling

## When to Use TDD

**Good for:**
- New features with clear acceptance criteria
- Bug fixes (write failing test first)
- Refactoring (test protects against regressions)
- API design (tests serve as documentation)

**Less suitable for:**
- Pure exploration/spiking (no clear requirements)
- UI polish/visual tweaks (hard to test behavior)
- One-off scripts (not worth investment)

## Test First vs Test After

| Aspect | Test First (TDD) | Test After |
|---|---|---|
| Design focus | Drives interface design | Validates existing design |
| Coverage | High (all code has test) | Variable (may miss paths) |
| Documentation | Tests describe intent | Tests describe implementation |
| Refactoring | Safe (tests protect behavior) | Risky (tests may miss changes) |

## Example: Vertical Slicing

**Scenario:** Build user login feature

**Wrong (horizontal):**
```
Day 1: Write tests for login, logout, password reset, session management
Day 2-4: Implement everything
```

**Right (vertical):**
```
Cycle 1: test login → implement login
Cycle 2: test logout → implement logout
Cycle 3: test password reset → implement password reset
Cycle 4: test session management → implement session management
```

Each cycle:
- Produces working, testable code
- Informs next test based on what was learned
- Can demo progress after each cycle
