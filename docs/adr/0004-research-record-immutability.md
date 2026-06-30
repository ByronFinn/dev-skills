# 0004 - Research Records Are Immutable Across Major Versions

Date: 2026-06-30

## Status

Accepted

## Context

The `research` skill (PRD-0001) maintains a knowledge base at `docs/research/<stack>-<topic>-<major>.md`. Each record captures the best practice for one stack × topic × major-version combination, sourced exclusively from authoritative sources (ADR-lite in PRD-0001, R4/R5).

A design question arose during `/grill`: when a new major version of a stack ships (e.g. React 18 → 19), should the existing record be **edited** to reflect the new best practice, or should a **new record** be created while the old one is frozen?

This is not obvious. Editing a single file keeps the knowledge base compact (one file per stack+topic) and always reflects "current" truth. Creating a new file per major doubles (or more) the file count and requires INDEX to track multiple rows per topic.

The decision matters because it determines whether the knowledge base is a **current-state snapshot** (editable, lossy history) or a **historical ledger** (immutable, comparable across versions).

## Decision

**Research records are immutable. Once written, a record is frozen and captures the best practice *as of* that major version. When a new major ships, a new record is created (`-18.md` → `-19.md`); the old one is never edited.**

Concretely:
- Filename always carries the major version: `<stack>-<topic>-<major>.md`
- Editing an existing record is forbidden — even to "fix" or "update" it
- A stale record (`Status: stale` in INDEX) means "current project uses a higher major"; it does **not** mean the record is wrong — it faithfully documents that major's era
- Re-research produces a new `-<newmajor>.md` file, not a rewrite

## Consequences

### Positive

* **Historical traceability** — best-practice evolution across majors is comparable (how React's concurrent rendering guidance changed from 17 → 18 → 19). This is impossible if old records are overwritten.
* **No edit conflicts** — multiple skills/agents reading records never race to "update" the same file; immutability removes a class of write conflicts.
* **Stale has clear meaning** — `stale` = "version skew", not "incorrect". A reader knows a stale record is still authoritative for its own major.
* **Auditability** — the Sources cited remain valid for the version they were written against; editing would silently break this linkage.
* **Aligns with ADR philosophy** — ADRs are also append-only (Superseded, not edited). Research records now follow the same archival discipline.

### Negative

* **File count grows with majors** — a stack with 4 majors and 10 topics produces 40 files, not 10. INDEX absorbs most of this (rows, not cognitive load), but the directory is larger.
* **Corrections within a major are awkward** — if a record written for v18 contains an error discovered while v18 is still current, "immutability" would forbid the edit. *Mitigation: immutability applies across majors; intra-major error correction is allowed via a `## Correction` appended block dated and sourced, not a silent rewrite.*
* **Reader must check the major** — a reader landing on `react-concurrent-rendering-17.md` must notice the major before applying the advice. Filename + TL;DR header carry this signal.

## Alternatives Considered

* **Edit-in-place (single file per stack+topic)**: Always reflects "current" truth; compact. But destroys history — once React 19's guidance overwrites the file, the v18-era guidance is gone forever. Also creates write races when multiple sessions research the same topic. Rejected: the user's stated need is *accumulation*, and accumulation implies preserving prior states.

* **Edit-in-place with a `## History` appendix**: Single file, history preserved as appended sections. Compromise, but the file becomes long and the "current verdict" is ambiguous (which section is canonical?). Also still allows silent edits to past sections. Rejected: filename-as-version is a stronger, more legible invariant than section headers.

* **Mutable records, separate `archive/` for old majors**: Move old records to `docs/research/archive/` when superseded. Adds a directory convention and a move operation (destructive, needs explicit authorization per anti-pattern #17). Rejected: unnecessary complexity when the filename already encodes the major.

## References

* PRD-0001 — Research Skill (R11 immutability requirement)
* CONTEXT.md — Research Record definition (immutability clause)
* ADR-0001 — Sub-Agent Orchestration Pattern (analogue: append-only archival discipline)
* anti-patterns.md #17 — Implicit authorization escalation (why moving files is avoided)
