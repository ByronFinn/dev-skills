# Improve Architecture: Detailed Reference

## Step 1: Read Domain Context

Read files to understand project:
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

Look for following patterns:

**Design debt signals:**
- Code duplication (same logic appears multiple times)
- Long functions/classes (too many responsibilities)
- Tight coupling (changing one affects many others)
- Global state (hard to reason about)
- Leaked abstractions (implementation details leak)
- Missing abstractions (direct use of low-level details)

**Deepening opportunities:**
- Complex logic that can hide behind simple interface
- Similar functionality that can merge
- Common patterns that can extract

## Step 4: Analyze Findings

Categorize findings into:

| Category | Description | Priority | PRD Link |
|---|---|---|---|
| **Blocking** | Blocks planned PRD | Urgent | Link to specific PRD |
| **High** | Technical debt accumulating, affects future | High | May affect multiple PRDs |
| **Medium** | Improves structure, not urgent | Medium | Doesn't directly affect PRDs |

## Step 5: Propose Improvements

For each finding, propose:
- Current problem (why it's a problem)
- Suggested improvement (how to improve)
- Expected benefit (what improvement brings)
- Effort estimate (rough effort level)
- **Linked PRD** (if applicable)

## Step 6: Generate Report

Output structured report:

```markdown
# Architecture Improvement Report

## Summary

<one-line summary>

## Current Development Direction

Based on PRDs:
- <PRD 1>: <one-sentence>
- <PRD 2>: <one-sentence>

## Architecture Alignment

✅ Compatible: <features>
⚠️ Needs improvement: <features>
❌ Conflicts: <features>

## Findings

### Blocking (Urgent)

1. **<Issue Title>**
   - **Location**: `<file:line>`
   - **Problem**: <description>
   - **Suggestion**: <description>
   - **Benefit**: <description>
   - **Effort**: <low/medium/high>
   - **Blocking PRD**: `docs/prd/<name>.md`

### High Priority

...

### Medium Priority

...

## Next Steps

1. Review and prioritize findings
2. Create issues for approved improvements
3. Implement before blocked PRDs
```

## Design Debt Signals

### Code Duplication

**Signal:** Same logic appears in multiple places.

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

**Signal:** Function or class does too many things.

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

**Signal:** Change in one module forces changes in many others.

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

**Signal**: Shared mutable state accessible from anywhere.

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

**Signal:** Implementation details visible to callers.

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

**Signal:** Direct use of low-level operations everywhere.

**Example:**
```javascript
// Direct HTTP calls scattered everywhere
fetch('/api/users').then(/* ... */);
fetch('/api/orders').then(/* ... */);
fetch('/api/products').then(/* ... */);
```

**Improvement:** Create API client abstraction with consistent error handling.

## Deep Module Examples

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

## Report Template

```markdown
**Improve Architecture Complete**

**Scan scope:**
- PRDs: <count>
- Code files: <count>
- ADRs: <count>

**Architecture alignment:**
- ✅ Compatible: <count> features
- ⚠️ Needs improvement: <count> features
- ❌ Conflicts: <count> features

**Findings:**
- Blocking: <count>
- High priority: <count>
- Medium priority: <count>

**Suggested next steps:**
1. Review blocking issues
2. Create issues for approved improvements
3. Use /story to decompose
4. Use /tdd to implement
```
