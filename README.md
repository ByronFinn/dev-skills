# Engineering Skills

[![skills.sh](https://skills.sh/b/ByronFinn/dev-skills)](https://skills.sh/ByronFinn/dev-skills)

Agent skills for software engineering workflows.

## Skills

- **setup-project** — Scaffold per-repo configuration: issue tracker convention, triage labels, domain docs layout. Run once before first use of other skills.
- **think** — Brainstorm and converge on solutions. Diverge on possibilities, converge on concrete plan, generate initial PRD.
- **grill** — Challenge plans against domain model. Interview relentlessly about plan aspects, resolve dependencies, sharpen terminology, update CONTEXT.md and ADRs.
- **story** — Break PRD into executable Issues using vertical slices (tracer bullets).
- **tdd** — Test-driven development with red-green-refactor loop.
- **review** — Code review, doc sync, and release check. Remote issue/release/publish actions require explicit current-turn authorization.
- **debug** — Root cause analysis and systematic fix.
- **improve-architecture** — Periodically review and improve code architecture based on domain language and decision records.

## Installation

```bash
npx skills@latest add ByronFinn/dev-skills
```

## Workflow

```
First time:           setup-project → (skills configured)
New feature:          think → grill → story → tdd → review → (release)
Bug/regression:       debug → review (optional)
Architecture health:  improve-architecture → grill/story/tdd (if approved)
```

0. **setup-project** — One-time repo configuration: issue tracker, triage labels, domain docs.
1. **think** — Transform rough ideas into decision-complete PRDs; stops before implementation.
2. **grill** — Validate plans against existing domain model and decision records.
3. **story** — Break PRDs into executable vertical-slice Issues.
4. **tdd** — Implement accepted behavior with red-green-refactor.
5. **review** — Review diffs, verify evidence, sync docs, and run authorized finish work.
6. **debug** — Diagnose unknown root causes when bugs, regressions, or test failures arise.
7. **improve-architecture** — Periodic architecture review and deepening-opportunity report.

Routing conflicts are documented in `skills/RESOLVER.md`. Route by the user's work object first: error logs go to **debug**, diffs/completed work go to **review**, PRDs/plans go to **grill**, accepted implementation issues go to **tdd**.

## Shared Rules

`skills/rules/anti-patterns.md` contains cross-skill behavioral constraints. It is a shared reference, not a standalone workflow skill.

## Repository Structure

```
skills/
├── setup-project/               # Project initialization skill
├── think/                       # Brainstorming skill
├── grill/                       # Plan validation skill
├── story/                       # PRD-to-issues skill
├── tdd/                         # Test-driven development skill
├── review/                      # Code review skill
├── debug/                       # Debugging skill
├── improve-architecture/        # Architecture improvement skill
├── RESOLVER.md                  # Human-readable skill routing table
└── rules/                       # Shared cross-skill constraints
    └── anti-patterns.md
```

## License

MIT
