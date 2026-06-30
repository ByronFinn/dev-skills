# Repo Map

This project spans multiple repositories. This file records which repo does what and where skills should read/write.

## Repositories

| Repo | URL | Role | Issue Tracker | Domain Docs |
|------|-----|------|---------------|-------------|
| `<name>` | `<clone-url>` | `<role: API server / web app / shared lib / infra>` | `<GitHub / GitLab / Local / Shared>` | `<single-context / multi-context>` |

## Primary issue tracker

Issues for cross-repo features live in **`<primary-repo-name>`**. When skills like `story` need to create or read issues, use that repo's tracker.

## Domain doc ownership

- **Shared domain terms** live in `<repo>/CONTEXT.md`
- **Per-repo domain terms** live in each repo's own `CONTEXT.md`
- **Cross-repo ADRs** live in `<repo>/docs/adr/`
- **Per-repo ADRs** live in each repo's `docs/adr/`

## Skill behavior across repos

When working on a feature that spans multiple repos:
1. Read all relevant `CONTEXT.md` files first
2. Read shared ADRs from the primary repo, then per-repo ADRs
3. Create issues in the primary repo's tracker
4. Label cross-repo issues with `<cross-repo-label>` (if configured)
