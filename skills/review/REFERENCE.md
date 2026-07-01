# Review: Detailed Reference

This reference contains detailed instructions for the orchestrator phases and each sub-agent. Each chapter is self-contained — an agent reading only that chapter should know exactly what to do.

---

## Chapter 1: Context Collection (Orchestrator)

The orchestrator collects all context before dispatching sub-agents. Every sub-agent will re-read shared context independently, but the orchestrator must gather the initial bundle of file paths and diffs to pass along.

### Step 1: Collect the Diff

Gather the full code change under review:

```bash
# Staged changes
git diff --cached

# Unstaged changes
git diff

# Combined (staged + unstaged)
git diff HEAD
```

If there are untracked files relevant to the review, include them:

```bash
git ls-files --others --exclude-standard
```

Read each changed file's full content (not just the diff) for complete context.

**Large diff handling (>30 files):** When the diff exceeds 30 files, reading every full file may exceed context limits. Strategy:

1. Group changed files by module/package
2. Prioritize high-risk groups for full reads: business logic, security-sensitive code, public API changes
3. For low-risk groups (config, docs, generated code, test fixtures), read diffs only — skip full file reads
4. State explicitly: "Large diff detected (<N> files). Reviewing by module group, full-reading high-risk files only."
5. Each sub-agent applies the same prioritization independently

### Step 2: Read Project Config

Extract project commands, conventions, and constraints from:

| File | Extract |
|------|---------|
| `README.md` | Project description, setup instructions, contribution guidelines |
| `package.json` | Scripts (test, lint, build, typecheck), dependencies |
| `Makefile` | Build targets, test commands, lint targets |
| CI configs (`.github/workflows/*`, `.gitlab-ci.yml`, `Jenkinsfile`, etc.) | Pipeline stages, required checks, deployment steps |
| `tsconfig.json` / `pyproject.toml` / equivalent | Language/compiler configuration |
| `.eslintrc*` / `.flake8` / equivalent | Code style rules |

From these, determine the exact commands to run for verification:

- **Test command**: e.g., `npm test`, `pytest`, `go test ./...`
- **Lint command**: e.g., `npm run lint`, `flake8`, `golangci-lint run`
- **Typecheck command**: e.g., `tsc --noEmit`, `mypy .`
- **Build command**: e.g., `npm run build`, `cargo build`, `go build ./...`

### Step 3: Read Domain Doc Layout

Apply the [Skill Entry Protocol](../rules/entry-protocol.md) to determine where domain docs actually live. The entry protocol reads `domain.md` and `repo-map.md` to discover actual paths for CONTEXT.md, PRDs, and ADRs — which may differ from defaults in multi-repo or monorepo setups.

Read `docs/agents/repo-map.md` (if exists) to identify which repos are part of this project. If the diff touches files in multiple repos, note the cross-repo scope for the Impact Review sub-agent.

If `domain.md` does not exist, use default paths below.

### Step 3.1: Quality Check (Degradation Handling)

After reading the shared context, check for signs that upstream skills were skipped:

| Signal | Meaning | Action |
|--------|---------|--------|
| PRD has `Open Questions` or `TODO` markers | `/grill` may not have resolved all decisions | Note in report: "PRD has unresolved items — some decisions may be unvalidated" |
| No tests in diff | Tests may not have been written | Flag in Test Review: "No new tests found in diff" |
| `CONTEXT.md` mentions terms not used in code | Domain model may have drifted | Note in Impact Review: "Domain terms in CONTEXT.md not reflected in implementation" |

These are notes, not blockers. Record them in the appropriate sub-agent reports.

### Step 4: Gather Shared Context Paths

Collect paths to all domain documents that sub-agents will need to re-read. Use paths from `domain.md` (Step 3) if available, otherwise fall back to defaults:

| Document | Default path | Purpose |
|----------|-------------|---------|
| PRD | `docs/prd/PRD-NNNN-<title>.md` | Requirements, acceptance criteria |
| Story / Issues | Issue tracker or `docs/issues/` | Vertical-slice implementation tickets |
| CONTEXT.md | `CONTEXT.md` | Domain glossary, terminology definitions |
| ADRs | `docs/adr/*.md` | Architecture Decision Records |

Not all documents may exist. Record which are available and which are missing — sub-agents need to know the boundaries of available context.

### Step 5: Build the Context Bundle

The orchestrator assembles a context bundle containing:

1. **Diff** — full staged + unstaged diff
2. **Changed file list** — every file touched, with full paths
3. **Project commands** — test, lint, typecheck, build commands extracted from config
4. **Domain doc layout** — from `domain.md` (if read in Step 3), otherwise default paths
5. **Shared context paths** — available PRD, Story/Issue, CONTEXT.md, ADR paths
6. **Project metadata** — language, framework, package manager (derived from config files)

This bundle is passed to all three sub-agents. Each sub-agent re-reads the actual files from disk independently (anti-patterns #34, #35).

## Sub-Agent Common (applies to Chapters 2, 3, 4)

The three review sub-agents (Test / Code / Impact) share these rules. Each chapter below states only what is **unique** to that perspective — responsibilities, its specific checklist focus, and its output's extra fields.

### Independence

Sub-agents share no state and re-read all shared context from disk — see [anti-patterns.md #34, #35](../rules/anti-patterns.md). The operational consequence is the re-read checklist below.

### Shared Context Re-Read Checklist

Every sub-agent re-reads all of the following from disk before starting:

- [ ] `docs/agents/domain.md` (if exists) — domain doc layout
- [ ] PRD (from `docs/prd/` or path from `domain.md`) — requirements and acceptance criteria
- [ ] Story / Issue — vertical-slice implementation ticket being reviewed
- [ ] `CONTEXT.md` — domain glossary and terminology
- [ ] ADRs (from `docs/adr/` or path from `domain.md`) — relevant architecture decisions
- [ ] Full diff (staged + unstaged)

Each chapter adds **one more bullet** for the files its perspective cares about. If any document is missing, note it and state how it limits the review.

### Output Scaffold (shared shape)

Every sub-agent report uses this structure:

```markdown
## <Perspective> Review

**<status fields specific to the perspective>**

### Issues
- **[<severity: blocker | major | minor>]** <description>
  - File: `<path>` (omit for Impact Review)
  - Line: <line number or range> (omit for Impact Review)
  - Evidence: <what you observed>
  - Suggestion: <how to fix or mitigate>

### Positives
- <description of good practice observed>

### Verdict
<Approve | Request Changes> — <one-line justification>

**Verdict reasoning**: <2-3 sentences explaining the key factors that determined this verdict. What tipped the balance? If Request Changes, what must be fixed? This reasoning helps the orchestrator identify contradictions between sub-agents.>
```

### Severity Levels (shared definition)

- **blocker**: critical defects specific to the perspective (see each chapter for examples)
- **major**: significant gaps requiring attention before merge
- **minor**: improvements, non-critical

Each chapter notes what counts as a blocker for its perspective.

---

## Chapter 2: Test Review Sub-Agent

### Responsibilities

Review test quality for the changes in the diff. Focus exclusively on test concerns:

- **Test coverage**: are all acceptance criteria from the PRD/Issue tested?
- **Boundary coverage**: are edge cases and boundary conditions tested?
- **Test design**: do tests verify behavior through public interfaces, not implementation details?
- **Mock usage**: are mocks used appropriately?
- **Naming**: do test names clearly describe the scenario?
- **Isolation**: are tests independent of each other?

Do NOT review implementation quality, security, performance, or release impact — those belong to other sub-agents.

### Review Checklist

#### Test Coverage

- [ ] Every acceptance criterion from the PRD/Issue has at least one test
- [ ] New public functions/methods have corresponding tests
- [ ] Bug fixes include regression tests
- [ ] Tests cover the happy path AND failure paths

#### Boundary Coverage

- [ ] Edge cases tested: empty inputs, null/undefined, zero, max values
- [ ] Boundary conditions tested: off-by-one, minimum/maximum allowed values
- [ ] Error conditions tested: invalid input, network failures, permission denied
- [ ] Concurrent/parallel scenarios tested (if applicable)

#### Test Design

- [ ] Tests verify behavior through public interfaces, not private internals
- [ ] Tests do not assert on implementation details (e.g., "this function called helper X")
- [ ] Each test has a single clear purpose
- [ ] Test data is realistic and representative

#### Mock Usage

- [ ] Mocks used only for external dependencies (network, database, filesystem, time)
- [ ] No mocks for internal modules/classes within the same unit
- [ ] Mocked behavior matches real dependency contract (mock won't mask real bugs)
- [ ] No over-mocking that makes tests trivially pass

#### Naming

- [ ] Test names describe the scenario (`<unit> <condition> <expected result>`) and are consistent across the suite

#### Isolation

- [ ] Tests are independent — order-independent, self-contained fixtures, no shared mutable state, clean up after themselves

### Output Template

Use the [shared Output Scaffold](#output-scaffold-shared-shape) with status field **Coverage assessment**: `<assessment of overall test coverage>`.

**Test Review blockers** (specific to this perspective): missing tests for critical acceptance criteria, tests that mask real bugs.

### Extra Context Re-Read

- [ ] All test files in the diff — read full file content, not just changed lines

---

## Chapter 3: Code Review Sub-Agent

### Extra Context Re-Read

- [ ] All implementation files in the diff — read full file content, not just changed lines

### Responsibilities

Review implementation quality for the changes in the diff. Focus exclusively on code quality concerns:

- **Security**: vulnerabilities, credential handling, input validation
- **Performance**: obvious inefficiencies, resource management
- **Code conventions**: project style, naming, formatting
- **Error handling**: are errors handled properly?
- **Readability**: is the code clear and maintainable?

Do NOT review test quality or release impact — those belong to other sub-agents.

### Security Checklist

Run these on every review:

- [ ] No credentials or keys in diff
- [ ] No hardcoded secrets
- [ ] Input validation present
- [ ] Output encoding/escaping correct
- [ ] SQL queries parameterized
- [ ] File operations validate paths
- [ ] Dependencies checked with the project-supported audit command, or marked not checked with reason
- [ ] Error messages don't leak sensitive info

If any security check fails, the verdict must be **Request Changes** with severity **blocker**. Security issues are non-negotiable.

### Performance Checklist

- [ ] No obvious N+1 queries
- [ ] No unnecessary loops in hot paths
- [ ] Appropriate caching (if applicable)
- [ ] Resource cleanup (connections, handles)
- [ ] Pagination/limiting on list operations

### Code Quality Checklist

#### Error Handling

- [ ] Errors are caught and handled, not silently swallowed
- [ ] Error messages are descriptive and actionable
- [ ] Async errors (promises, callbacks) are handled
- [ ] Error boundaries or equivalents are in place where needed

#### Readability

- [ ] Code is clear and self-documenting
- [ ] Comments explain "why", not "what"
- [ ] No unnecessary complexity
- [ ] Functions/methods are focused and reasonably sized

#### Conventions

- [ ] Code follows project naming conventions
- [ ] Code follows project formatting/style rules
- [ ] Imports are organized per project convention
- [ ] No dead code or commented-out code

### Output Template

Use the [shared Output Scaffold](#output-scaffold-shared-shape) with status fields **Security status**: `<clean | issues found>`, **Performance status**: `<clean | issues found>`, **Overall quality assessment**: `<assessment>`.

**Code Review blockers** (specific to this perspective): security vulnerabilities, data loss risk, breaking bugs. If any security checklist item fails, verdict must be **Request Changes** with severity **blocker**.

### Extra Context Re-Read

- [ ] All implementation files in the diff — read full file content, not just changed lines

---

## Chapter 4: Impact Review Sub-Agent

### Extra Context Re-Read

- [ ] CI configs (`.github/workflows/*`, `.gitlab-ci.yml`, etc.) — pipeline stages and checks
- [ ] Release configs (`CHANGELOG.md`, version files, deployment configs) — release process
- [ ] Dependency files (`package.json`, `go.mod`, `requirements.txt`, etc.) — dependency changes

### Responsibilities

Perform full-chain impact analysis. Focus on what this change affects beyond the immediate code:

- **Change scope**: what areas are affected?
- **Regression risk**: could this break existing functionality?
- **Compatibility**: are there breaking changes?
- **Architecture health (LOCAL only)**: does this change introduce coupling or violate ADRs?
- **Tech debt**: does this change introduce technical debt?
- **Release strategy**: feature flags, canary, rollback plan?
- **Documentation**: are docs updated?

**Traceability:**
- **New domain terms**: identify terms used in the code that are not in `CONTEXT.md`. Record them as suggestions for CONTEXT.md update.
- **New decisions**: identify architectural decisions made in the code that are not in `docs/adr/`. Record them as suggestions for ADR creation.

Do NOT review test quality or implementation quality — those belong to other sub-agents.

### Boundary with improve-architecture

This sub-agent evaluates architecture impact **local to this change only**: does this specific diff introduce new coupling, violate existing ADRs, or create local design problems?

For **global** architecture concerns — overall system design health, cross-cutting patterns, strategic refactoring — suggest the user run `/improve-architecture` separately. Do not attempt a full architecture review here.

### Review Checklist

#### Change Scope

- [ ] List all modules/packages/areas touched by this change
- [ ] Identify callers/consumers affected by changed interfaces
- [ ] Identify downstream services or systems affected

#### Regression Risk

- [ ] Could this change break existing functionality?
- [ ] Are there integration points that could be affected?
- [ ] Are there data format changes that could break consumers?
- [ ] Risk level: <low | medium | high> — with justification

#### Compatibility

- [ ] API changes: are there breaking changes to public APIs?
- [ ] Database changes: are there schema migrations? Are they backward-compatible?
- [ ] Config changes: are there config format changes that require migration?
- [ ] Dependency changes: are there version bumps that could break consumers?

#### Architecture Health (LOCAL)

- [ ] Does this change introduce new coupling between modules?
- [ ] Does this change violate any existing ADR?
- [ ] Does this change follow established patterns in the codebase?
- [ ] Does this change make future extensions harder?

#### Tech Debt

- [ ] Does this change introduce TODOs or workarounds?
- [ ] Does this change hardcode values that should be configurable?
- [ ] Does this change bypass existing abstractions?

#### Release Strategy

- [ ] Are feature flags needed for this change?
- [ ] Is a canary deployment recommended?
- [ ] Is there a rollback plan if this goes wrong?
- [ ] Are there data migration steps that need coordination?

#### Documentation

- [ ] Are API docs updated for changed endpoints?
- [ ] Is README updated (if affected)?
- [ ] Is CHANGELOG updated for user-visible changes?
- [ ] Are config docs updated for config changes?

### Output Template

Use the [shared Output Scaffold](#output-scaffold-shared-shape) with these status fields and extra sections:

```markdown
**Change scope**: <summary of affected areas>
**Regression risk**: <low | medium | high> — <justification>
**Compatibility**: <backward-compatible | breaking changes found>
```

Plus an **Architecture Note** section (local concerns here; global concerns → suggest `/improve-architecture`) and a **Release Readiness** section (feature flags / canary / rollback plan / data migration).

**Impact Review blockers** (specific to this perspective): breaking changes without migration path, high regression risk without mitigation.

### Extra Context Re-Read

- [ ] CI configs (`.github/workflows/*`, `.gitlab-ci.yml`, etc.) — pipeline stages and checks
- [ ] Release configs (`CHANGELOG.md`, version files, deployment configs) — release process
- [ ] Dependency files (`package.json`, `go.mod`, `requirements.txt`, etc.) — dependency changes

---

## Chapter 5: Report Merge and Presentation (Orchestrator)

After all three sub-agents produce their reports, the orchestrator merges them into a single unified review.

### Step 1: Concatenate Reports

Present each sub-agent's report as a distinct section in this order:

1. Test Review
2. Code Review
3. Impact Review

Do not reorder, summarize, or restructure individual sub-agent reports. Each section stays exactly as the sub-agent produced it.

### Step 2: Extract Contradictions

Compare the three reports. If two or more sub-agents reach **conflicting conclusions about the same item**, extract them into a dedicated Contradictions block.

What counts as a contradiction:
- One sub-agent says "Approve" and another says "Request Changes" for the same concern
- Sub-agents recommend different solutions for the same issue
- One sub-agent flags an issue as "blocker" while another considers it acceptable

What does NOT count as a contradiction:
- Different sub-agents finding different issues (that is expected — different perspectives)
- One sub-agent mentioning something another didn't notice (supplementary, not contradictory)

### Contradiction Format

For each contradiction, present both sides' reasoning without taking a side:

```markdown
### Contradiction: <topic>

**Test Review position**: <summary of this sub-agent's conclusion and reasoning>
**Code Review position**: <summary of this sub-agent's conclusion and reasoning>

→ Human adjudication needed.
```

Do not auto-resolve contradictions. The human adjudicates.

### Step 3: Unified Recommendation

Derive a single recommendation from the three verdicts:

| Condition | Recommendation |
|-----------|---------------|
| All three say Approve | **Approve** |
| Any one says Request Changes | **Request Changes** |
| Sub-agents disagree on recommendation | **Request Changes** + list the disagreement in Contradictions |

### Step 4: No Silent Resolution

Never drop or merge away a sub-agent's finding to avoid presenting a contradiction. Every finding from every sub-agent must appear in the merged report. If findings conflict, that is exactly what the Contradictions block is for.

### Merged Report Template

The merged report template (Traceability, per-perspective sections, Contradictions block, Verification, Findings, Recommendation, Next steps) is defined once in [SKILL.md §Output](SKILL.md). Follow that structure when assembling the merged report.

---

## Chapter 6: Authorization and Follow-Through (Orchestrator)

After presenting the merged report, the orchestrator asks the user what to do next. Different actions have different authorization requirements.

### Local Doc Updates (Allowed Without Authorization)

These updates are allowed **only when the review has verified the underlying change**:

| Action | When |
|--------|------|
| Update PRD implementation status | Task verified as complete by review |
| Check off completed acceptance criteria | Task verified as complete |
| Update `CONTEXT.md` with new terms | New domain terms introduced by the change |
| Update or create ADRs | Architecture decisions made in the change |
| Update README | Setup instructions or project description changed |
| Update CHANGELOG | User-visible changes exist |

**Judgment standard:** Only update when the review verified a change that the document should reflect (e.g., acceptance criteria met, new terms introduced in verified code). If the update is speculative or forward-looking (e.g., "will be implemented in next PR"), list it as follow-up instead — do not update the file.

**PRD Traceability:** When updating the PRD, fill the `## Traceability` section:
- `Reviewed by`: add `/review` with PR reference (if available) or date
- `New terms`: add domain terms found in the code that are not yet in CONTEXT.md
- `New decisions`: add architectural decisions made in the code that are not yet in ADRs

**PRD Child Issues Status Sync:** When the review verifies a task is complete:
1. From the Issue being reviewed, read `Meta → PRD` to locate the PRD
2. Find the Issue in the PRD's `Sliced into` list
3. Update the Issue's status marker: `— In Progress` → `— Done`
4. Check if ALL Child Issues are marked `— Done`:
   - If yes: update PRD `Status` from `In Progress` to `Done`
   - If no: keep PRD `Status` as `In Progress`

Perform these updates as part of the review when applicable. List what was updated in the report.

### Issue Comments and Updates (Allowed for Verified Work)

Adding comments to issues or updating issue bodies to reflect completed, verified work is allowed — it is equivalent to local doc sync. The review has verified the code, so recording that verification is appropriate.

### Issue Close / Status / Label Changes (Requires Authorization)

These are **public, irreversible signals**. They require explicit user authorization in the current turn:

- Closing issues
- Changing issue status (e.g., "in progress" → "done")
- Adding or removing labels

A previous-turn "ok" or "looks good" does not authorize these. The user must explicitly request them now.

### Release Actions (Always Require Authorization)

All release actions require explicit user authorization in the current turn:

- Creating tags
- Pushing to remote
- Publishing to registry
- Creating or updating releases

If the user only approves the review report, list release steps as recommended next steps — do not execute them.

### How to Execute Authorized Actions

When the user explicitly authorizes an action:

1. **Issue operations**: Read `docs/agents/issue-tracker.md` for the project's convention on close, comment, and update operations.
2. **Release operations**: Follow the project's release process as documented in CI configs, Makefile, or README.
3. **Commit message**: Never add AI attribution (anti-pattern #15). The user is the author.

### Request Changes Guidance

When the recommendation is **Request Changes**, guide the user based on severity:

**How to decide "minor" vs "scope change":**

- **Minor**: bugs in existing code, missing test cases, naming issues, small logic errors. The original plan is still valid. Fix issues, then run `/review` again.
- **Scope change**: the fix requires new features, changes acceptance criteria, or adds requirements not in the original PRD. The plan needs to be updated first. Re-evaluate with `/think` or `/grill`, then `/tdd` → `/review`.

**Escalation paths:**
- If requirements changed → `/think` or `/grill` to update the plan
- If global architecture concerns surfaced → `/improve-architecture`
- If the fix is straightforward → fix → `/review` again

---

## Chapter 7: Session Recovery

If the session is interrupted during the review process, follow these steps.

### General Recovery Steps

1. **Re-read the latest user message** — determine what triggered the review
2. **Re-read shared context from disk** — PRD, Story/Issue, CONTEXT.md, ADRs (anti-pattern #36)
3. **Re-read the diff** — run `git diff HEAD` again; the code may have changed since the interruption
4. **Determine progress** — which sub-agents completed, which was in progress
5. **State recovery summary** — tell the user what was recovered and where you'll resume from. Confirm before continuing

### Recovery by Phase

**If interrupted during Context Collection (Chapter 1):**
- No sub-agents have run yet. Re-read project config and diff from disk. Resume from Step 1.

**If interrupted during Sub-Agent Dispatch (Chapter 2-4):**
- Check which sub-agent reports were completed (look for any partial output in the conversation)
- Re-dispatch any sub-agents whose reports are missing or incomplete
- Each sub-agent independently re-reads all shared context — no state is lost
- Do NOT reuse a sub-agent's partial output from memory — re-run the sub-agent from scratch

**If interrupted during Report Merge (Chapter 5):**
- If all three reports were produced, re-merge them from the sub-agent outputs
- If some reports are missing, re-dispatch the missing sub-agents

**If interrupted during Authorization (Chapter 6):**
- Present the merged report again (re-read from disk if any local files were updated)
- Re-ask the user for authorization — never assume a previous authorization carries over after interruption

---

## Chapter 8: Integration Review

When all vertical slices of a PRD are complete, perform additional checks beyond single-slice review:

- **Cross-slice data flow**: Do the slices integrate correctly when combined?
- **Shared state consistency**: Do slices agree on data models, state transitions, event payloads?
- **Full PRD acceptance criteria coverage**: Are ALL acceptance criteria from the PRD met across all child issues?
- **Integration test coverage**: Are there tests that verify slices working together, not just unit tests per slice?
- **Dependency order verification**: Were slices implemented in the correct dependency order?

State explicitly: "Integration Review — checking <N> slices for PRD <name>."
