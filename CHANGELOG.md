# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/), and this project adheres to [Semantic Versioning](https://semver.org/).

## [Unreleased]

### Added
- **Skill Entry Protocol** (`skills/rules/entry-protocol.md`) — shared bootstrap sequence for all skills. Replaces duplicated context-read instructions across 8 skills. Ensures standalone execution (graceful degradation) and composable execution (reads prior skill outputs via Traceability chain).
- **TDD Gate Modes** — Full (default, 2 gates per criterion), Fast (1 gate, scenarios + code together), Batch (1 gate per 2-3 homogeneous criteria). User can switch modes mid-skill and per-criterion.
- **Integration Review Mode** in `/review` — additional checks when all vertical slices of a PRD are complete (cross-slice data flow, shared state consistency, full acceptance criteria coverage).
- **Large diff handling** in `/review` — chunking strategy for diffs >30 files (group by module, prioritize high-risk files for full reads).
- **Environment-dependent bug guidance** in `/debug` — structured approach for "works on my machine" class bugs (version diff, lockfile comparison, OS-specific behavior).
- **Anti-pattern #3a** — explicit rule for when serial questioning is correct (dependency chains), complementing #3's batch-independent-questions rule.
- `Debugged by` and `Arch reviewed by` fields in PRD Traceability — completes the lifecycle tracking chain.
- `Prototyped by` field in PRD Traceability — captures verdict from `/have-a-try` prototype runs.
- `## Meta` section in shared Issue template — downstream skills (`/tdd`, `/review`) read `Meta → PRD` to locate the source PRD.
- `CHANGELOG.md` — this file.

### Changed
- **TDD Refactor exception** — implementation-coupled tests (mocking internals, asserting on private methods) SHOULD be fixed to test through public interface during refactor. Documented with reason in refactor report.
- **Grill "send back to think" criteria** — replaced unmeasurable "30% of requirements changed" with qualitative criteria (goal statement change, fundamental approach invalidation, new domain area).
- **Improve-architecture effort estimates** — replaced human-time-based ("1-3 days") with scope-and-impact-based ("Low: 1-3 files isolated", "Medium: multi-file one module", "High: cross-module coordinated").
- **Think Step 0.5 timing** — moved PRD-creation question to after auto-context collection (Step 1), so user decides with actual findings in hand.
- **PRD status normalized** — `InProgress` (one word) unified to `In Progress` (two words) across all skill instructions and lifecycle documentation.

### Fixed
- **Broken reference** — `scripts/hitl-loop.template.sh` in debug/REFERENCE.md was referenced but did not exist. Replaced with inline script template.
- **Think Step 1 duplication** — removed duplicate Step 1 content caused by step reordering.

## [0.1.0] - 2026-06-12

### Added
- Sub-agent orchestration pattern for TDD and Review skills (ADR 0001)
- Two-stage Human Review Gate for test quality (ADR 0002)
- Anti-patterns #37 (skill-to-skill state drift), #38 (sub-agent state leakage), #39 (session recovery)
- Acceptance Criterion Cycle in TDD — 5-step loop per criterion
- Parallel three-perspective review (Test ∥ Code ∥ Impact)
- CONTEXT.md domain model for this project
