# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/), and this project adheres to [Semantic Versioning](https://semver.org/).

## [Unreleased]

### Added
- **`/implement` skill** (`skills/implement/`) — workflow orchestration skill that sequences /tdd at pre-agreed seams, implements non-TDD items directly, runs typechecking and tests per item, dispatches /review at the end, and commits per completed seam. `disable-model-invocation: true` — only invoked by explicit `/implement` command. See RESOLVER.md, AGENTS.md, README.md for routing, pipeline position, and disambiguation updates.
- **Anti-pattern citations added** — `implement` (#5, #6, #12, #17), `think` (#20, #28), `debug` (#12, #21), `review` (#18). Reduces uncited anti-pattern rules from 23 to 19.

### Fixed
- **Pipeline diagram in README.md/README_ZH.md** — `/research` moved from mandatory main chain to optional side branch; `/review` moved from disconnected standalone box to main pipeline terminal; `/tdd` shown as sub-process of `/implement` rather than sequential step.
- **`think/SKILL.md` missing Step 10** — Process Summary now includes Create Parent Issue & Finalize PRD step (was only in REFERENCE.md and Gotchas, creating a gap where Step 10 existed in the contract but not in the listed workflow).
- **`think/REFERENCE.md` broken cross-reference** — PRD Conflict Check note incorrectly pointed to `story/REFERENCE.md §PRD Conflict Check` which doesn't exist. Now correctly states "the same procedure defined here."
- **PRD-0001 `InProgress` typo** — lifecycle comment used single-word `InProgress` instead of standardized two-word `In Progress`.
- **Project structure tree indentation** — `story/`, `implement/`, `tdd/` entries in README.md and README_ZH.md used tabs instead of spaces, breaking tree alignment.
- **RESOLVER.md duplicate "Direct breakdown" headings** — consolidated two entries with identical headings into one, with note that `/tdd → /review` remains available for single-issue manual TDD.
- **`review/SKILL.md` Output missing Next step** — added `Next: User decides — merge/release, or fix issues and re-review` for pipeline consistency.

### Changed
- **`disable-model-invocation: true` documented** — added to AGENTS.md File Conventions and Language Convention table as an allowed YAML frontmatter extension for explicit-invocation-only skills.
- **AGENTS.md Documents Produced table** — added `have-a-try` row (NOTES.md + PRD Traceability update).
- **Upstream/downstream skill references updated** — `story`, `have-a-try`, `improve-architecture` now point to `/implement` instead of `/tdd` as next step; `story` offers both `/implement` (orchestration) and `/tdd` (single-issue).
- **TDD Gate Modes** — Full (default, 2 gates per criterion), Fast (1 gate, scenarios + code together), Batch (1 gate per 2-3 homogeneous criteria). User can switch modes mid-skill and per-criterion.
- **Integration Review Mode** in `/review` — additional checks when all vertical slices of a PRD are complete (cross-slice data flow, shared state consistency, full acceptance criteria coverage).
- **Large diff handling** in `/review` — chunking strategy for diffs >30 files (group by module, prioritize high-risk files for full reads).
- **Environment-dependent bug guidance** in `/debug` — structured approach for "works on my machine" class bugs (version diff, lockfile comparison, OS-specific behavior).
- **Anti-pattern #3a** — explicit rule for when serial questioning is correct (dependency chains), complementing #3's batch-independent-questions rule.
- `Debugged by` and `Arch reviewed by` fields in PRD Traceability — completes the lifecycle tracking chain.
- `Prototyped by` field in PRD Traceability — captures verdict from `/have-a-try` prototype runs.
- `## Meta` section in shared Issue template — downstream skills (`/tdd`, `/review`) read `Meta → PRD` to locate the source PRD.
- `CHANGELOG.md` — this file.
- **PRD-0001 status reconciled to Done (B5)** — the `research` skill was shipped across all 4 files (SKILL/REFERENCE/RESEARCH-FORMAT/INDEX-FORMAT) and referenced by RESOLVER/AGENTS/entry-protocol, but its PRD-0001 was stuck at `Grilled` with all 18 ACs unchecked. Verified all 18 ACs against actual artifacts via script, checked them off (with annotation that AC1's frontmatter field list was superseded by the 2026-07-04 spec-compliance fix), advanced Status to `Done`, and filled Traceability. Closes the dogfood gap where the project's own `/review` "code is the source of truth" principle had not been applied to its own PRD.

### Changed
- **TDD Refactor exception** — implementation-coupled tests (mocking internals, asserting on private methods) SHOULD be fixed to test through public interface during refactor. Documented with reason in refactor report.
- **Grill "send back to think" criteria** — replaced unmeasurable "30% of requirements changed" with qualitative criteria (goal statement change, fundamental approach invalidation, new domain area).
- **Improve-architecture effort estimates** — replaced human-time-based ("1-3 days") with scope-and-impact-based ("Low: 1-3 files isolated", "Medium: multi-file one module", "High: cross-module coordinated").
- **Think Step 0.5 timing** — moved PRD-creation question to after auto-context collection (Step 1), so user decides with actual findings in hand.
- **PRD status normalized** — `InProgress` (one word) unified to `In Progress` (two words) across all skill instructions and lifecycle documentation.
- **RESOLVER.md positioning corrected (B1)** — re-labeled RESOLVER.md as a *derived* human-readable index, not the routing source of truth. Runtime routing is driven by each skill's `description` field (per [agentskills.io spec](https://agentskills.io/specification)); RESOLVER.md restates routing for humans and adds disambiguation rules that `description` fields cannot express. Updated the matching "single source" phrasing in RESOLVER.md and AGENTS.md so the trust direction is no longer inverted.
- **PRD Conflict Check relocated (B3)** — moved the full PRD-conflict-check procedure out of the shared `rules/entry-protocol.md` (where every skill's bootstrap paid for PRD-management ceremony it never used) into `think/REFERENCE.md §PRD Conflict Check` (the primary PRD-creator). `story/REFERENCE.md` and `PRD-FORMAT.md` now reference the new home; `entry-protocol.md` Step 3a is a short pointer. Non-PRD skills (`/write`, `/debug`, `/review`) no longer carry this check on their always-loaded path.
- **Anti-pattern debt surfaced (B2)** — audit found 27 of 38 rules never cited by any skill. Added 4 high-value citations (#6/#17→review, #27→research, #32→debug), bringing cited rules from 11 to 15. Marked 4 high-confidence archive candidates (#7/#25/#26/#31) and added a "name a consumer skill before adding a rule" guard in the Usage section to prevent re-accumulation. Full audit: `docs/audits/2026-07-03-anti-pattern-citation-audit.md`.
- **ADR-0001 sub-agent semantics clarified (C1)** — added an Implementation Note making explicit that "sub-agent" is a re-read-from-disk discipline, not a runtime scheduler concept. Independence comes from the discipline; parallel dispatch strengthens but does not create it. Removes the hallucinated-scheduler reading without renaming the term (which would break cross-references).

### Fixed
- **Broken reference** — `scripts/hitl-loop.template.sh` in debug/REFERENCE.md was referenced but did not exist. Replaced with inline script template.
- **Think Step 1 duplication** — removed duplicate Step 1 content caused by step reordering.
- **Frontmatter spec compliance** — all 11 `SKILL.md` files now use only `name` + `description` per [agentskills.io spec](https://agentskills.io/specification). Removed non-standard `when_to_use` and `dispatch_intent` fields; their trigger keywords (Chinese and English) are merged into `description` so loading is portable across Claude Code, Copilot, OpenCode, and any spec-compliant loader. Updated `AGENTS.md` file contract accordingly.
- **Anti-pattern citation drift** — `skills/review/REFERENCE.md:560` cited `#36` (Session recovery) where the context calls for `#34` (Skill-to-skill state drift). Root cause: renumber merge did not run a repo-wide citation sweep (anti-pattern #21). Audit report at `docs/audits/2026-07-03-anti-pattern-citation-audit.md`.
- **No-tracker degradation for `/think` Step 9a (B4)** — Step 9a's parent-issue requirement previously had no visible escape hatch for repos without an issue tracker, leaving the break path only documented inside a PRD Traceability. Added an explicit "No-tracker degradation" subsection in `think/REFERENCE.md` and a visible pointer in `think/SKILL.md` Step 9. Convention: write `N/A — no issue tracker configured` in the PRD `## Issue` field. Synced `grill/REFERENCE.md` and `story/REFERENCE.md` to recognize this signal.

## [0.1.0] - 2026-06-12

### Added
- Sub-agent orchestration pattern for TDD and Review skills (ADR 0001)
- Two-stage Human Review Gate for test quality (ADR 0002)
- Anti-patterns #37 (skill-to-skill state drift), #38 (sub-agent state leakage), #39 (session recovery)
- Acceptance Criterion Cycle in TDD — 5-step loop per criterion
- Parallel three-perspective review (Test ∥ Code ∥ Impact)
- CONTEXT.md domain model for this project
