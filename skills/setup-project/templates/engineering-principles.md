# Engineering Principles (seed template)

<!--
Seed for the `## Engineering principles` section written into the repo's AGENTS.md/CLAUDE.md,
immediately after the `## Agent skills` block. Tailoring rules (apply before writing; the result
is confirmed with the user in Step 4E / Step 5):

- Language: render the section in the team's documentation language (docs/agents/language.md) —
  translate headings and prose; keep commands, paths, and identifiers as-is.
- Stack fit: drop the blocks marked <Multi-tenant>, <Backend>, or <Frontend> when the repo lacks
  that dimension (e.g. no frontend → drop principle 6). Confirm the resulting scope with the user.
- Placeholders: fill every <...> from evidence — file-size bound and dependency locations from
  the repo layout; quick-reference commands from package.json scripts / Makefile / justfile / CI
  workflows. Never invent commands; a row with no real command is dropped, not guessed.
- Layers (principle 3): adapt the model kinds to the project's actual architecture — protocol /
  domain / persistence / view are the common four; rename or trim to match.
- ADR path (principle 8): use the path configured in docs/agents/domain.md.

These are project-level mandates for the target repo. They complement the dev-skills catalog
(skills/rules/engineering-principles.md) consumed by /review and /tdd; overlap in spirit is
intentional. Keep the section self-contained — no links into install-path-dependent skill files.
-->

## Engineering principles

These principles govern all engineering work in this repo — planning, implementation, review. They are enforced in design and code, not aspirations.

1. **Architecture and domain first.** Plan against the ideal architecture before coding: business goals, domain boundaries, module responsibilities, dependency directions, data flows. Design completely, implement restrainedly — no speculative abstraction: introduce an abstraction at the second real use case; with a single scenario, implement directly.

2. **Elegant modules.** High cohesion, low coupling; hide internal complexity behind small, stable interfaces so responsibilities, naming, dependencies, and extension points stay obvious. One responsibility per file; keep files under <500 — adjust to repo convention> lines and refactor module boundaries when approaching the limit.

3. **Clear boundaries, clean data flow.** <protocol / domain / persistence / view — adapt to the repo's layers> models never leak into one another; validate and convert at each boundary; no shared mutable state across layers.

4. **Secure and isolated by default.** <Multi-tenant: design every feature for multi-tenant, multi-user use; make authentication, authorization, and data-isolation boundaries explicit.> Least privilege throughout; treat all external input as untrusted; keep secrets and sensitive data out of code, logs, and responses.

5. **Designed for concurrency and failure.** <Backend> Address idempotency, races, transaction boundaries, timeouts, cancellation, bounded retries, backpressure, and resource cleanup by design. Failures surface — never mask them with unbounded retries, swallowed errors, or hidden shared state.

6. **Complete user experience.** <Frontend> Control render cost, async state, and concurrent requests; keep the UI structure clear; every user flow covers loading, empty, error, retry, feedback, and accessibility.

7. **Reuse before you add.** Prefer existing modules and capabilities; don't extract an abstraction from surface similarity — when duplicating deliberately, comment why the copies may evolve independently. Before adding a dependency, check what the repo already ships (<root package.json + packages/ workspace — adapt>); don't assume a library lacks a feature — read its docs and types first. When adding is justified, prefer mature, maintained libraries over re-implementing common functionality.

8. **Leave context for future maintainers.** Code, comments, tests, and architecture docs are collaboration across time. Non-obvious decisions, compatibility constraints, known defects, and stopgaps record why, impact, risk, and removal conditions. Tech debt links to a tracked issue; key architecture decisions become ADRs (<docs/adr/>); no context-free TODOs.

9. **Every change verifiable, observable, reversible.** Behavior-testable, observable at runtime, diagnosable in failure; backward compatibility and a rollback path are part of the change, not an afterthought. Logs keep diagnostic context without leaking sensitive data.

10. **Deletion over compatibility.** Refactoring internal paths deletes the superseded implementation outright — no shims, deprecated aliases, or dual-write logic. Compatibility for external contracts (<public API, DB migrations — adapt>) is assessed per contract: a contractual duty, not deference to old code.

### Change quick reference

Run the matching verification before committing:

| Changed | Run |
|---|---|
| Anything (baseline) | `<precheck / lint + typecheck + tests>` |
| <Frontend code> | `<build / typecheck command>` |
| <Database schema> | `<migration generate>` then `<migrate>` |
| <Data backfill / repair> | `<data-migration runner>` (after DDL) |
