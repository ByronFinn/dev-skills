<!-- markdownlint-disable MD033 MD041 -->

<h1 align="center">🛠️ Engineering Skills</h1>

<p align="center">
  <em>Reusable agent skills for software engineering workflows — from idea to release.</em>
</p>

<p align="center">
  <a href="https://skills.sh/ByronFinn/dev-skills"><img src="https://skills.sh/b/ByronFinn/dev-skills" alt="skills.sh"></a>
  <a href="LICENSE"><img src="https://img.shields.io/badge/License-MIT-yellow.svg" alt="License: MIT"></a>
  <a href="https://github.com/ByronFinn/dev-skills"><img src="https://img.shields.io/badge/GitHub-ByronFinn/dev--skills-181717?logo=github" alt="GitHub"></a>
</p>

<p align="center">
  <a href="#-table-of-contents">TOC</a> ·
  <a href="#-quick-start">Quick Start</a> ·
  <a href="#-skills-overview">Skills</a> ·
  <a href="#-workflow-pipelines">Workflows</a> ·
  <a href="#-design-principles">Principles</a> ·
  <a href="#-sub-agent-architecture">Architecture</a> ·
  <a href="#-contributing">Contributing</a>
</p>

<p align="center">
  <a href="README_ZH.md">🇨🇳 中文版</a>
</p>

---

**Engineering Skills** is a collection of **Markdown-based instruction sets** for AI coding agents (e.g., Claude Code via [skills.sh](https://skills.sh)).  
There is no application code, no build step, no runtime — **the skill documents themselves are the product**.

## 🤔 Why This Exists

AI coding agents are powerful but inconsistent. They skip planning, forget domain context, mix test design with implementation, and lose track of decisions. This project solves that with **structured skill documents** that enforce engineering discipline:

| Principle | Command | What it enforces |
|---|---|---|
| **Think** before code | `/think` | Brainstorm and converge before writing anything |
| **Challenge** before implement | `/grill` | Stress-test plans against domain model |
| **Test** before implement | `/tdd` | Red-green-refactor with independent perspectives |
| **Review** before merge | `/review` | Parallel three-perspective review |
| **Root cause** before fix | `/debug` | Systematic debugging with reproducible feedback loops |
| **Investigate** before commit | `/research` | Capture best practices durably from authoritative sources |

---

## 📋 Table of Contents

- [Quick Start](#-quick-start)
- [Skills Overview](#-skills-overview)
- [Workflow Pipelines](#-workflow-pipelines)
- [Routing](#-routing)
- [Design Principles](#-design-principles)
- [Key Concepts](#-key-concepts)
- [Sub-Agent Architecture](#-sub-agent-architecture)
- [Project Structure](#-project-structure)
- [Requirements](#-requirements)
- [Contributing](#-contributing)
- [License](#-license)

---

## 🚀 Quick Start

```bash
# Install all skills into your project (one-time)
npx skills@latest add ByronFinn/dev-skills

# In your repo, configure skill behavior (one-time)
/setup-project

# Start building a feature
/think
```

That's it. Each skill is triggered by a **slash command** and stops when done — skills never auto-chain. You decide when to move to the next step.

---

## 🧰 Skills Overview

> **11 skills** covering the full engineering lifecycle: planning → research → validation → breakdown → implementation → review → debugging → maintenance → writing.

| Skill | Command | Input → Output | Description |
|---|---|---|---|
| **setup-project** | `/setup-project` | Repo state → `docs/agents/` config | One-time scaffold: issue tracker, triage labels, domain doc layout, repo map. Re-run when project structure changes. |
| **think** | `/think` | Rough idea → PRD (`docs/prd/`) | Brainstorm → converge to a decision-complete plan. One question at a time with a recommended answer. |
| **research** | `/research` | Stack×topic question → Immutable record + INDEX | Investigate against authoritative sources (official docs, source, spec). Persist as a versioned, immutable record re-usable across sessions. |
| **have-a-try** | `/have-a-try` | Design question → Answer (prototype → delete) | Build a throwaway prototype to answer one design question. LOGIC mode (terminal app) or UI mode (variant switcher). Delete when done. |
| **grill** | `/grill` | PRD → Validated PRD + CONTEXT.md + ADRs | Read the PRD with "hostile eyes". Extract every open question, assumption, and vague term — resolve them one at a time until exhaustion. |
| **story** | `/story` | PRD or description → Vertical-slice Issues | Break a plan into independently executable issues (tracer bullets through all layers). Publish in dependency order. |
| **tdd** | `/tdd` | Issue / PRD → GREEN code + tests | Sub-agent orchestrated TDD: Test Sub-Agent → Human Review Gates → Develop Sub-Agent. One acceptance criterion per cycle. |
| **review** | `/review` | Diff → Merged 3-perspective report | Parallel sub-agents: Test Review ∥ Code Review ∥ Impact Review. Merge with contradiction highlighting for human adjudication. |
| **debug** | `/debug` | Error/crash/regression → Fix + regression test | 6-phase systematic loop: reproduce → hypothesize → instrument → fix → test → cleanup. Bisect and scope-scan modes. |
| **improve-architecture** | `/improve-architecture` | Codebase + PRDs + ADRs → Architecture report | Scan for design debt, ADR compliance, and deepening opportunities. Blocking / High / Medium priorities with scope estimates. |
| **write** | `/write` | Draft prose → Edited prose | Strip AI tone, polish, rewrite. Supports Chinese and English. Release notes, launch/social copy, localization, document review. |

---

## 🔄 Workflow Pipelines

Skills compose into standard engineering workflows. Each skill **stops** after its output — you trigger the next step.

### New Feature — Full Pipeline

```
/setup-project → /think → /grill → /story → /tdd → /review → 🚀 merge/release
                        ↗                        ↗
              /research (on INDEX miss)    /have-a-try (design doubt)
```

### Common Sequences

| Scenario | Pipeline | When to use |
|---|---|---|
| **New feature** | `/think` → `/grill` → `/story` → `/tdd` → `/review` | Full pipeline, from rough idea to reviewed code |
| **Direct breakdown** | `/story` → `/tdd` → `/review` | You already have a clear plan, skip brainstorming |
| **Bug fix** | `/debug` → `/review` (optional) | Error, crash, regression — find root cause first |
| **Technical investigation** | `/research` → `/think` (consumes INDEX) | Persist best-practice knowledge for reuse |
| **Architecture health** | `/improve-architecture` → `/grill` → `/story` → `/tdd` | Periodic design debt scan |

### Pipeline Diagram

```
                    ┌─────────────────────────────────────────────────────┐
                    │                 New Feature Pipeline                 │
                    └─────────────────────────────────────────────────────┘

  ┌──────────┐    ┌──────────┐    ┌──────────┐    ┌──────────┐    ┌──────────┐
  │  /think  │───▶│ /research│───▶│ /grill   │───▶│ /story   │───▶│  /tdd    │
  │  idea→PRD│    │  rec→INDEX│   │  PRD→valid│   │  →Issues │   │  →GREEN  │
  └──────────┘    └──────────┘    └──────────┘    └──────────┘    └──────────┘
       │               ▲               │                              ▲
       │               │               │                              │
       │     ┌─────────┴─────────┐     │                              │
       │     │ /think Step 5     │     │                              │
       │     │ queries INDEX     │     │                              │
       │     └───────────────────┘     │                              │
       │                               │                              │
       │     ┌───────────────────┐     │                              │
       └────▶│  /have-a-try      │     │                              │
             │  (design doubt)   │◀────┘                              │
             └───────────────────┘                                    │
                                                                      │
               ┌──────────┐                                           │
               │ /debug   │◀──────────────────────────────────────────┘
               └──────────┘

  ┌──────────┐    ┌──────────┐    ┌──────────┐
  │/setup-   │    │/review   │    │/improve- │
  │project   │    │          │    │architecture│
  └──────────┘    └──────────┘    └──────────┘

  ┌──────────┐
  │  /write  │
  └──────────┘
```

---

## 🧭 Routing

Route by your **work object** — what you have determines which skill to use:

| You have / want to do | Use |
|---|---|
| 🆕 New project, need configuration | `/setup-project` |
| 💡 Rough idea, unclear requirements | `/think` |
| 🔬 Stack/version investigation to capture durably | `/research` |
| 🧪 Design doubt to resolve by running code | `/have-a-try` |
| 🔥 PRD/plan to challenge | `/grill` |
| 📋 Plan to break into tickets | `/story` |
| ✅ Accepted issue to implement | `/tdd` |
| 🐛 Error, crash, regression | `/debug` |
| 👀 Completed work / diff to review | `/review` |
| 🏗️ Architecture health / design debt | `/improve-architecture` |
| ✍️ Prose editing / polish / de-AI | `/write` |

> **Full disambiguation rules** in [`skills/RESOLVER.md`](skills/RESOLVER.md) cover edge cases: Bug vs TDD, Grill vs Review, Think vs Research, and more.

---

## 🎯 Design Principles

### 🧩 Standalone + Composable

Every skill works **on its own** — no hard dependencies on prior skills. Missing prerequisites trigger graceful degradation, not errors. When chained, skills read prior outputs through the **PRD Traceability chain**:

```
Created by → (Prototyped by) → Grilled by → Sliced by → Implemented by → Reviewed by
                                                    ↑                    ↑
                                              Debugged by        Arch reviewed by
```

The [Entry Protocol](skills/rules/entry-protocol.md) standardizes this bootstrap: locate domain docs → check upstream artifacts → proceed with or without them.

### 🧠 Sub-Agent Orchestration

TDD and Review skills use a **sub-agent pattern** — each sub-agent independently re-reads all shared context from disk before acting, with **no shared memory or cached understanding** ([ADR 0001](docs/adr/0001-sub-agent-orchestration-pattern.md)):

- **TDD**: Test Sub-Agent (design scenarios → write tests) → Human Review Gates → Develop Sub-Agent (implement → refactor)
- **Review**: Test Review ∥ Code Review ∥ Impact Review → merge with contradiction highlighting

This is a **logical concept** implemented through instruction-level isolation in Markdown — no runtime scheduler needed.

### 📊 Evidence Over Claims

Skills enforce running commands and pasting output. "Should work" is never acceptable evidence. Every conclusion must cite a verification command or explicit runtime check.

### 🎯 Minimal Change

Fix what was asked, nothing more. After fixing one instance of a pattern, grep for siblings. Scope creep is flagged, not silently absorbed.

### 🔒 Immutable Research Records

Research records are **immutable** — once written, a record is frozen and captures best practice *as of* that major version. When a new major ships, a new record is created; the old one is never edited ([ADR 0004](docs/adr/0004-research-record-immutability.md)).

---

## 📖 Key Concepts

<details>
<summary><b>📄 PRD (Product Requirements Document)</b></summary>

**Format**: [`skills/think/PRD-FORMAT.md`](skills/think/PRD-FORMAT.md) · **Location**: `docs/prd/<feature>.md`

The central artifact. Created by `/think` or `/story`, validated by `/grill`, implemented by `/tdd`, verified by `/review`. Contains goal, requirements, acceptance criteria, technical approach, and a **Traceability** section tracking every skill that touched it.

</details>

<details>
<summary><b>📖 CONTEXT.md (Domain Glossary)</b></summary>

**Format**: [`skills/grill/CONTEXT-FORMAT.md`](skills/grill/CONTEXT-FORMAT.md) · **Location**: repo root

Ubiquitous language for the project. Pure terminology definitions — no implementation details. Created and maintained by `/grill`. Consumer skills use its vocabulary for naming, test design, and documentation.

</details>

<details>
<summary><b>📝 ADR (Architecture Decision Record)</b></summary>

**Format**: [`skills/grill/ADR-FORMAT.md`](skills/grill/ADR-FORMAT.md) · **Location**: `docs/adr/<NNNN>-<title>.md`

Records hard-to-reverse, surprising, real-trade-off decisions. Created sparingly by `/grill` — only when all three conditions are met. Checked for compliance by `/improve-architecture` and `/review`.

</details>

<details>
<summary><b>🚦 Human Review Gate</b></summary>

**Format**: Full / Fast / Batch modes ([ADR 0003](docs/adr/0003-gate-modes-full-fast-batch.md)) · **Inside**: `/tdd` skill

Blocking checkpoint where a human must approve before the next phase begins. **Full** mode (default): **Scenario Review Gate** (test design) → **Test Code Review Gate** (code quality + fidelity). **Fast** mode collapses to one gate. **Batch** mode groups 2-3 homogeneous criteria.

</details>

<details>
<summary><b>🔬 Research Record</b></summary>

**Format**: [`skills/research/RESEARCH-FORMAT.md`](skills/research/RESEARCH-FORMAT.md) · **Location**: `docs/research/<stack>-<topic>-<major>.md`

Durable note capturing technical best-practice for one **stack × topic × major-version** combination. Contains a **TL;DR** verdict, findings, boundary conditions, and a mandatory `## Sources` section restricted to authoritative sources. Immutable per ADR 0004.

</details>

<details>
<summary><b>📊 Research INDEX</b></summary>

**Format**: [`skills/research/INDEX-FORMAT.md`](skills/research/INDEX-FORMAT.md) · **Location**: `docs/research/INDEX.md`

Searchable entry point to the knowledge base. Two views: **By Stack** (records grouped per stack) and **By Topic** (cross-stack comparison). Downstream skills (notably `/think` Step 5) query INDEX first; only on a miss do they start new research.

</details>

---

## 🏗️ Sub-Agent Architecture

Two skills (TDD and Review) use an advanced **sub-agent orchestration pattern**. Each sub-agent is an independent execution phase that re-reads all shared context from disk, with no memory or state shared between them.

### TDD Flow

```
 ┌───────────── Acceptance Criterion Cycle (one per criterion) ─────────────┐
 │                                                                           │
 │  ┌──────────────┐     ┌──────────────┐     ┌──────────────┐              │
 │  │ Test Sub-    │────▶│ Scenario     │────▶│ Test Sub-    │              │
 │  │ Agent        │     │ Review Gate  │     │ Agent        │              │
 │  │ (design      │     │ (Human       │     │ (write test  │──────┐       │
 │  │  scenarios)  │     │  approves)   │     │  code: RED)  │      │       │
 │  └──────────────┘     └──────────────┘     └──────────────┘      │       │
 │                                                                    │       │
 │  ┌──────────────┐     ┌──────────────┐                            │       │
 │  │ Develop Sub- │◀────│ Test Code    │◀───────────────────────────┘       │
 │  │ Agent        │     │ Review Gate  │                                    │
 │  │ (implement:  │     │ (Human       │                                    │
 │  │  GREEN)      │     │  approves)   │                                    │
 │  └──────────────┘     └──────────────┘                                    │
 │                                                                           │
 └───────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
                       ┌──────────────────────┐
                       │  Unified Refactor     │
                       │  (all cycles done)    │
                       └──────────────────────┘
```

**Gate Modes** ([ADR 0003](docs/adr/0003-gate-modes-full-fast-batch.md)):
- **Full** (default): 2 gates per criterion — Scenario + Test Code
- **Fast**: 1 gate (scenarios inline with code review)
- **Batch**: 1 gate per 2-3 homogeneous criteria

### Review Flow

```
                           ┌──────────────────────┐
                    ┌─────▶│  Test Review          │
                    │      │  Agent                │
                    │      │  (test quality,       │
                    │      │   boundary coverage)   │
                    │      └──────────────────────┘
                    │
 ┌──────────┐      │      ┌──────────────────────┐     ┌──────────┐
 │Orchestrator│─────┼─────▶│  Code Review          │────▶│  Merge    │
 │(SKILL.md) │      │      │  Agent                │     │  Report   │
 │           │      │      │  (implementation,     │     │  (contra- │
 │           │      │      │   security, perf)     │     │  dictions │
 └──────────┘      │      └──────────────────────┘     │  high-    │
                    │                                    │  lighted) │
                    │      ┌──────────────────────┐     └──────────┘
                    └─────▶│  Impact Review        │
                           │  Agent                │
                           │  (regression risk,    │
                           │   release strategy,   │
                           │   compatibility)      │
                           └──────────────────────┘
```

---

## 📁 Project Structure

```
dev-skills/
├── AGENTS.md                      # Workspace instructions
├── README.md                      # ← You are here
├── README_ZH.md                   # 中文版
├── CHANGELOG.md                   # Version history
├── CONTEXT.md                     # Domain model (dogfooding example)
├── LICENSE                        # MIT
│
├── docs/
│   ├── prd/                       # PRDs for this project
│   ├── adr/                       # Architecture Decision Records
│   └── agents/                    # Skill configuration
│       ├── domain.md
│       ├── issue-tracker.md
│       ├── triage-labels.md
│       ├── language.md
│       └── repo-map.md
│
├── skills/                        # ← All skills live here
│   ├── RESOLVER.md                # Routing table & disambiguation
│   ├── rules/
│   │   ├── anti-patterns.md       # Cross-skill behavioral constraints
│   │   └── entry-protocol.md      # Shared bootstrap sequence
│   │
│   ├── setup-project/             # Initialization skill
│   ├── think/                     # Brainstorming skill
│   ├── research/                  # Technical investigation skill
│   ├── have-a-try/                # Prototyping skill
│   ├── grill/                     # Plan validation skill
│   ├── story/                     # Plan-to-issues skill
│   ├── tdd/                       # TDD implementation skill
│   ├── review/                    # Code review skill
│   ├── debug/                     # Debugging skill
│   ├── improve-architecture/      # Architecture improvement
│   └── write/                     # Prose editing skill
│       └── references/            # Language-specific patterns
```

Each skill directory follows a consistent structure:

| File | Purpose |
|---|---|
| `SKILL.md` | Entry point — YAML front matter, outcome contract, process summary, gotchas, output template |
| `REFERENCE.md` | Detailed steps, checklists, examples, sub-agent chapters |
| `*-FORMAT.md` | Bilingual format templates (where applicable) |

---

## 🔧 Requirements

- An AI coding agent that supports [skills.sh](https://skills.sh) skill loading (e.g., Claude Code)
- Git repository (required for `review`, `debug`, and diff-based skills)
- Optional: `gh` CLI (for GitHub issue tracker integration in `story` and `review`)

---

## 🤝 Contributing

See [AGENTS.md](AGENTS.md) for project conventions, file structure rules, and language guidelines.

When adding or modifying skills:

1. **Follow existing structure**: `SKILL.md` (entry) → `REFERENCE.md` (detail) → `*-FORMAT.md` (templates)
2. **Keep `SKILL.md` concise**; move deep detail to `REFERENCE.md`
3. **Update routing** — Update [`skills/RESOLVER.md`](skills/RESOLVER.md) when adding or changing skills
4. **Respect shared rules** — Run [`anti-patterns.md`](skills/rules/anti-patterns.md) rules against your own output
5. **Use the Entry Protocol** — Reference [`rules/entry-protocol.md`](skills/rules/entry-protocol.md) instead of duplicating context-read instructions. See [anti-pattern #36](skills/rules/anti-patterns.md#L42)
6. **Update CHANGELOG** — Log your changes in [`CHANGELOG.md`](CHANGELOG.md)

This project **dogfoods** its own skills — all documentation (PRDs, ADRs, CONTEXT.md) is written in Simplified Chinese per the project's [language configuration](docs/agents/language.md).

---

## 📄 License

[MIT](LICENSE) © 2026 ByronFinn

---

<p align="center">
  <sub>Built with skills, by skills. 🤖</sub>
</p>
