# Improve Architecture: Detailed Reference

## Step 1: Read Domain Context

Apply the [Skill Entry Protocol](../rules/entry-protocol.md) to locate and read domain context:
- `CONTEXT.md` — domain terms and concepts
- `docs/adr/*.md` — historical architecture decisions
- `docs/prd/*.md` — current and planned features
- `docs/audits/*.md` — read the most recent record before proposing structural changes; it holds the judgments already made on these modules and the reasons behind them

## Step 2: Analyze Current Development Direction

Extract from PRDs:
- Planned new features
- Expected technical changes
- Identified architecture requirements

**Check consistency with existing architecture:**
- Do new features require architecture changes?
- Does existing architecture support new features?
- Are there conflicts or constraints?

## Step 3: Scan Codebase

### 3.1 Scanning Strategy

Scan in this order — not random full-repo reads:

1. **PRD-linked modules first** — for each PRD, identify the modules it will touch. Scan those modules for design debt that would block or complicate the planned feature. This produces the highest-signal findings.

2. **High-change-frequency modules next** — run `git log --oneline --since="4 weeks ago" -- <path>` or equivalent to find modules with the most recent changes. Active code accumulates debt faster.

3. **Cross-cutting concerns last** — scan shared utilities, middleware, configuration, error handling patterns across the repo. These affect everything but are often neglected.

**Skip entirely:**
- Generated code, build output, vendored dependencies
- Test fixtures, mock data
- Files not tracked by version control

### 3.2 Design Debt Signals

For each signal, a concrete heuristic is provided to make detection objective. This table is the **only home of the thresholds** — principle definitions, counter-indications, and severity rules live in [../rules/engineering-principles.md](../rules/engineering-principles.md). The `Principle` column tags each signal with the principle it detects; `—` marks a signal that is a scanner heuristic without a catalog entry.

| Principle | Signal | Detection Heuristic | Threshold |
|-----------|--------|-------------------|-----------|
| **DRY** | **Code duplication** | Same 6+ line block appears in ≥2 files | 2+ occurrences with ≥70% line similarity |
| **SRP** | **Long functions/classes** | Function body exceeds N lines; class has N+ methods | Function > 50 lines; class > 15 methods |
| **DIP** | **Tight coupling** | Module A imports >N modules from module B's internals | >3 direct imports from internal paths of another module |
| **Immutability & Pure Functions** | **Mutable shared state** | Mutable state reachable from outside its defining module | Any `export let` / module-level mutable state / singleton / mutable default parameter / in-place mutation of a parameter |
| **Explicit over Implicit** | **Leaked abstractions** | Caller must know implementation detail to use function correctly | Function requiring caller to pass internal config/state |
| — (deep module) | **Missing abstractions** | Raw low-level calls repeated without wrapper | ≥3 direct uses of low-level API (fetch, fs, SQL) without shared adapter |
| — (deep module) | **Shallow modules** | Interface surface ≈ implementation complexity | Public method count ≥ 50% of total lines of code |
| **SRP / ISP** | **God objects** | Single class/file handles >3 unrelated responsibilities | Class name contains "Manager", "Handler", "Service" + >500 lines |
| **YAGNI** | **Dead / unreachable code** | Exported or top-level symbol with no references | 0 non-test references, excluding entrypoints, public API surface, and framework-registered symbols |
| **YAGNI** | **Speculative generality** | Parameters, options, flags, or abstractions with no real user | ≥2 parameters never passed a non-default value; config option never set; abstraction with exactly 1 implementation and no test double; feature flag never toggled |
| **LoD** | **Message chains / feature envy** | Depth of chained calls; count of foreign-object members accessed | Chain depth ≥3 across ownership boundaries; method touching ≥3 members of another object |
| **Composition over Inheritance** | **Deep or convenience inheritance** | Inheritance chain depth; override ratio | Depth ≥3 levels; subclass overrides >50% of inherited behavior; subclass exists to reuse a single method |
| **ISP / LSP** | **Stub implementations / contract violations** | Empty or throwing implementation of an interface method | ≥1 method that is empty or throws not-implemented in any implementer |
| **Explicit over Implicit** | **Magic values & hidden side effects** | Unnamed literals repeated in logic; side effects in accessors or constructors | Same literal in ≥3 sites; getter or constructor that mutates state or performs IO |
| **Fail Fast** | **Deferred validation / swallowed errors** | Validation far from the boundary; errors caught and dropped | Catch/except that neither rethrows, logs, nor handles; boundary accepting input without validation |
| **OCP** | **Repeated type dispatch** | Same type switch extended repeatedly | Same `switch`/if-else on a type modified to add a variant in ≥3 separate commits |

The two `— (deep module)` rows are described in [tdd/REFERENCE.md](../tdd/REFERENCE.md) §Deep Modules Principle (the definition's single source).

**These thresholds are guidelines, not hard cutoffs.** Use judgment — a 55-line function doing one clear thing is fine; a 40-line function juggling three responsibilities is not. The heuristic identifies *candidates*; human judgment confirms.

When a signal fires, the improvement direction follows from its category: duplication → extract shared utility; long functions/classes → split into focused units; tight coupling → depend on abstractions / inject dependencies; mutable shared state → pass state explicitly, return copies; leaked/missing abstractions → hide behind an interface or add a shared adapter; shallow modules → deepen (hide complexity behind a smaller interface); dead code → delete; speculative generality → delete until a real caller exists; message chains → tell, don't ask; deep inheritance → compose and delegate; stub implementations → split the interface or fix the contract; magic values and hidden side effects → named constant, explicit parameter, side effect moved to the caller; swallowed errors → validate at the boundary and fail fast; repeated type dispatch → extension point, but only once a second real implementation exists (otherwise it is speculative generality).

### 3.3 ADR Compliance Check

For each ADR in `docs/adr/`, verify the codebase still follows the decision:

1. Read each ADR's `Decision` and `Consequences` sections
2. Identify the code areas the ADR governs (from `Context` section or file references)
3. Check whether current code contradicts the ADR's decision
4. If contradicted, classify the finding:
   - **ADR drift** — code evolved away from the decision unintentionally. Flag as High priority.
   - **ADR obsolete** — the decision no longer makes sense given current requirements. Flag as Medium priority, suggest updating or superseding the ADR.
   - **ADR violated** — code directly contradicts a still-valid decision. Flag as Blocking.

5. Record findings with ADR reference, affected code, and classification.

### 3.4 Deepening Opportunities

Look for:

- **Complex logic behind wide interface** — a module with many public methods but each does little. Candidate for merging into fewer, deeper methods.
- **Similar functionality scattered across modules** — two or more modules solving variants of the same problem. Candidate for unified abstraction.
- **Repeated patterns that can be extracted** — initialization, validation, error handling, logging patterns that appear in many places. Candidate for shared utility or middleware.

## Step 4: Analyze Findings

Categorize findings into:

| Category | Description | Priority | PRD Link |
|---|---|---|---|
| **Blocking** | Blocks planned PRD | Urgent | Link to specific PRD |
| **High** | Technical debt accumulating, affects future | High | May affect multiple PRDs |
| **Medium** | Improves structure, not urgent | Medium | Doesn't directly affect PRDs |

### Finding Quality Checklist

Each finding must include:
- [ ] **Location**: specific file and module (not "the auth module" — use file paths)
- [ ] **Signal detected**: which debt signal or ADR violation was found (name the `Principle` tag from §3.2 when one applies)
- [ ] **Impact**: why this matters — performance, maintainability, onboarding cost, or blocked PRD. A principle-tagged finding must name the concrete consequence, not just the violated principle (anti-patterns.md #25)
- [ ] **Evidence**: paste the relevant code snippet or metric (e.g., line count, import count)
- [ ] **PRD link** (if applicable): which planned feature is affected

## Step 5: Propose Improvements

For each approved finding, propose:

| Field | Content |
|-------|---------|
| **Problem** | What design debt exists |
| **Suggestion** | Specific improvement |
| **Benefit** | What improves (maintainability, clarity, PRD unblock) |
| **Effort** | Low / Medium / High — with rationale |
| **Linked PRD** | Which PRD this improvement supports |

## Step 6: Generate Report

Output structured report using the template in SKILL.md Output section.

## Design Debt Signals — Extended Examples

Worked examples for each §3.2 row. **Thresholds live only in the §3.2 table** — this section adds examples and improvements, never restates the numbers (cite the §3.2 row instead: "per §3.2 Code Duplication").

### Code Duplication

**Example:**
```javascript
// File A
function validateEmail(email) {
  return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);
}

// File B (duplicate!)
function validateEmail(email) {
  return /^[^\s@]+@[^\s@]+\.[^\s@]+$/.test(email);
}
```

**Improvement:** Extract to shared utility module.

### Long Functions/Classes

**Example (per §3.2 Long Functions/Classes):**
```javascript
function processOrder(order) {
  // 50 lines of validation
  // 30 lines of payment processing
  // 40 lines of inventory update
  // 20 lines of notification
  // 10 lines of logging
}
```

**Improvement:** Split into focused functions: `validateOrder`, `processPayment`, `updateInventory`, `sendNotification`.

### Tight Coupling

**Example (per §3.2 Tight Coupling):**
```javascript
// OrderService directly depends on implementation details of PaymentProcessor, Inventory, EmailService
class OrderService {
  constructor() {
    this.payment = new PaymentProcessor(); // tight coupling
    this.inventory = new Inventory();
    this.email = new EmailService();
  }
}
```

**Improvement:** Depend on abstractions, inject dependencies.

### Mutable Shared State

**Example (per §3.2 Mutable shared state):**
```javascript
// Module-level mutable state
let currentUser = null;

function setUser(user) {
  currentUser = user;
}

function getUser() {
  return currentUser; // Hard to reason about when this changes
}
```

**Improvement:** Pass state explicitly or use state management library.

### Leaked Abstractions

**Example (per §3.2 Leaked Abstractions):**
```javascript
// Leaks file system implementation
function loadData() {
  const data = fs.readFileSync('./data.json'); // Caller must know about file system
  return JSON.parse(data);
}
```

**Improvement:** Hide behind interface that accepts any data source.

### Missing Abstractions

**Example (per §3.2 Missing Abstractions):**
```javascript
// Direct HTTP calls scattered everywhere
fetch('/api/users').then(/* ... */);
fetch('/api/orders').then(/* ... */);
fetch('/api/products').then(/* ... */);
```

**Improvement:** Create API client abstraction with consistent error handling.

## Deep Module Examples

> The deep/shallow module concept originates in *A Philosophy of Software Design*; the refactor-phase definition lives in `tdd/REFERENCE.md` §Deep Modules Principle. Below are scan-phase examples for spotting shallow modules during architecture review.

**Shallow (not worth having):**
```javascript
// Complex implementation, equally complex interface
function processData(options) {
  const { format, validate, transform, output, error } = options;
  // ... 50 lines of logic
  return { format, validate, transform, output, error };
}
```

**Deep (ideal):**
```javascript
// Simple interface, deep implementation
function process(data) {
  // ... 50 lines of hidden logic
  return processedData;
}
```
## Trigger Timing

- **Regular check:** Every 2-4 weeks proactively
- **Code health assessment:** When code quality feels degraded
- **Technical debt accumulation:** When hitting same pain points repeatedly
- **Pre-feature planning:** Before starting a major feature (quick scan of affected modules)
