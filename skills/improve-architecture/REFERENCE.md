# Improve Architecture: Detailed Reference

## Step 1: Read Domain Context

Apply the [Skill Entry Protocol](../rules/entry-protocol.md) to locate and read domain context:
- `CONTEXT.md` — domain terms and concepts
- `docs/adr/*.md` — historical architecture decisions
- `docs/prd/*.md` — current and planned features

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
- Files not tracked by version control

### 3.2 Design Debt Signals

For each signal, a concrete heuristic is provided to make detection objective:

| Signal | Detection Heuristic | Threshold |
|--------|-------------------|-----------|
| **Code duplication** | Same 6+ line block appears in ≥2 files | 2+ occurrences with ≥70% line similarity |
| **Long functions/classes** | Function body exceeds N lines; class has N+ methods | Function > 50 lines; class > 15 methods |
| **Tight coupling** | Module A imports >N modules from module B's internals | >3 direct imports from internal paths of another module |
| **Global state** | Mutable variable accessible from outside its defining module | Any `export let` / module-level mutable state / singleton pattern |
| **Leaked abstractions** | Caller must know implementation detail to use function correctly | Function requiring caller to pass internal config/state |
| **Missing abstractions** | Raw low-level calls repeated without wrapper | ≥3 direct uses of low-level API (fetch, fs, SQL) without shared adapter |
| **Shallow modules** | Interface surface ≈ implementation complexity | Public method count ≥ 50% of total lines of code |
| **God objects** | Single class/file handles >3 unrelated responsibilities | Class name contains "Manager", "Handler", "Service" + >500 lines |

**These thresholds are guidelines, not hard cutoffs.** Use judgment — a 55-line function doing one clear thing is fine; a 40-line function juggling three responsibilities is not. The heuristic identifies *candidates*; human judgment confirms.

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
- [ ] **Signal detected**: which debt signal or ADR violation was found
- [ ] **Evidence**: paste the relevant code snippet or metric (e.g., line count, import count)
- [ ] **Impact**: why this matters — performance, maintainability, onboarding cost, or blocked PRD
- [ ] **PRD link** (if applicable): which planned feature is affected

Findings without evidence are not actionable — do not include vague observations.

## Step 5: Propose Improvements

For each finding, propose:
- Current problem (why it's a problem)
- Suggested improvement (how to improve)
- Expected benefit (what improvement brings)
- **Scope estimate**: rough level with rationale
  - **Low**: isolated change, 1-3 files, no cross-module impact
  - **Medium**: multi-file change within one module, some cross-cutting concerns
  - **High**: cross-module refactor, affects multiple packages/services, requires coordinated rollout
- **Linked PRD** (if applicable)

## Step 6: Generate Report

Output structured report using the template in SKILL.md Output section.

## Design Debt Signals — Extended Examples

### Code Duplication

**Signal:** Same logic appears in multiple places (≥6 line block, ≥2 occurrences, ≥70% similarity).

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

**Signal:** Function body > 50 lines; class > 15 methods.

**Example:**
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

**Signal:** Module imports >3 internal paths from another module.

**Example:**
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

### Global State

**Signal**: Mutable variable accessible from outside its defining module.

**Example:**
```javascript
// Global state
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

**Signal:** Caller must know implementation detail to use function correctly.

**Example:**
```javascript
// Leaks file system implementation
function loadData() {
  const data = fs.readFileSync('./data.json'); // Caller must know about file system
  return JSON.parse(data);
}
```

**Improvement:** Hide behind interface that accepts any data source.

### Missing Abstractions

**Signal:** ≥3 direct uses of low-level API without shared adapter.

**Example:**
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
