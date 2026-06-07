# Engineering Skills

[![skills.sh](https://skills.sh/b/ByronFinn/dev-skills)](https://skills.sh/ByronFinn/dev-skills)

Agent skills for software engineering workflows.

## Skills

- **think** — Brainstorm and converge on solutions. Diverge on possibilities, converge on concrete plan, generate initial PRD.
- **grill** — Challenge plans against domain model. Interview relentlessly about plan aspects, resolve dependencies, sharpen terminology, update CONTEXT.md and ADRs.
- **story** — Break PRD into executable Issues using vertical slices (tracer bullets).
- **tdd** — Test-driven development with red-green-refactor loop.
- **review** — Code review, doc sync, and release check.
- **debug** — Root cause analysis and systematic fix.
- **improve-architecture** — Periodically review and improve code architecture based on domain language and decision records.

## Installation

```bash
npx skills@latest add ByronFinn/dev-skills
```

## Workflow

```
think → grill → story → (implementation) → review → (release)
                ↘ debug ↗
```

1. **think** — Transform rough ideas into decision-complete PRDs
2. **grill** — Validate plan against existing domain model
3. **story** — Break PRD into executable Issues
4. **Implement** — Build features (use **tdd** for test-driven development)
5. **review** — Code review and documentation sync
6. **debug** — Root cause analysis when bugs arise

## Repository Structure

```
skills/
├── .claude-plugin/plugin.json  # Plugin manifest
├── think/                       # Brainstorming skill
├── grill/                       # Plan validation skill
├── story/                       # PRD-to-issues skill
├── tdd/                         # Test-driven development skill
├── review/                      # Code review skill
├── debug/                       # Debugging skill
└── improve-architecture/        # Architecture improvement skill
```

## License

MIT
