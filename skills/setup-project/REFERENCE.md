# Setup Project: Detailed Reference

## Re-run Checklist

When `docs/agents/` already exists, run this drift detection loop **before** any user interaction. Each config file is checked against the current repo state:

| Config file | Detection check | Drift signal | Action |
|---|---|---|---|
| `issue-tracker.md` | `git remote -v` → does the remote match the tracker type in the file? | Remote changed (GitHub→GitLab, or no remote→local) | Present change, confirm, rewrite `issue-tracker.md` |
| `triage-labels.md` | Check actual labels on 1-2 recent issues → do they still match the file? | Labels renamed, added, or deprecated | Present change, confirm, rewrite `triage-labels.md` |
| `domain.md` | Does `CONTEXT-MAP.md` exist now when it didn't before? Were domain dirs (`docs/prd/`, `docs/adr/`, `docs/research/`) reorganized? | Context layout changed (single↔multi), dirs moved | Present change, confirm, rewrite `domain.md` |
| `language.md` | Read existing value. Ask: "Is `<language>` still the right doc language for the team?" | Language preference changed | Confirm, rewrite `language.md`. If changed, trigger **Conformance Sweep** (Language Audit) |
| **doc content** | Scan `docs/prd/`, `docs/adr/`, `docs/research/` for naming/language/format drift | Config changed (language, naming, FORMAT) | Trigger **Conformance Sweep** after overrides |
| `repo-map.md` (if exists) | Has the project structure changed? (Workspace files added/removed? User mentions sibling repos?) | Package count changed, repos added/removed, project type (single↔mono↔multi) changed | Present diff, confirm, rewrite `repo-map.md`. If project type changed → trigger **Migration** path below |
| (no `repo-map.md` yet) | Detect new multi-repo or monorepo signals: workspace files, user mentions sibling repos, subproject dirs | New structure signals found | Ask if project structure changed, create `repo-map.md` if needed |

**If no drift detected in any section**, tell the user: "All config is current — no changes needed." and stop.

## Re-run Behavior

When re-running, follow this sequence:

1. **Read current config** — load all existing `docs/agents/*.md` files before detecting anything new
2. **Run the Re-run Checklist** (above) — detect drift per config file
3. **Present diff** — show what changed vs what stayed the same. Only ask about changed sections.
4. **Update selectively** — rewrite only files that need changes. Leave untouched files alone.

If the user says "update repo map" or "switch issue tracker", focus on that section only. Still run the full checklist first to verify nothing else drifted.

## Migration (Structural Changes)

When the repo's structure has changed significantly since the last setup-project run, additional migration actions are needed beyond the normal re-run update.

| Previous state | Current state | Migration actions |
|---|---|---|
| **Single repo** | **Monorepo** (workspace files detected) | Add per-package `docs/agents/` dirs for packages with their own domain scope. Update `domain.md` to mention multi-context option. If `CONTEXT-MAP.md` was created, reference it in `domain.md`. |
| **Single repo** | **Multi-repo** (user mentions sibling repos) | Create `repo-map.md` listing all repos. Update `issue-tracker.md` to reference the primary tracker. Ask: "Which repo owns the primary issue tracker for cross-repo features?" |
| **Monorepo** | **Single repo** (workspace removed) | Remove per-package `docs/agents/` dirs (**ask first** — destructive). Simplify `domain.md` back to single-context. If `CONTEXT-MAP.md` was removed, remove references to it. |
| **Multi-repo** | **Single repo** | Remove `repo-map.md` (**ask first** — destructive). Simplify `issue-tracker.md` to point to this repo's tracker. |
| **Monorepo** | **Multi-repo** (packages split into separate repos) | Move per-package config to the new repos (`repo-map.md` + per-repo `docs/agents/`). Ask: "Which repo gets the shared domain docs?" |
| Any structure | **Reorganized domain dirs** (e.g. `docs/prd/` renamed or split across contexts) | Update `domain.md` with new paths. Check if old paths have stale files and ask about cleanup. |

**Rule:** Migration implies rewriting more files than a normal re-run. Always present the full diff of what will be created, rewritten, and removed. Get explicit approval before removing any files (anti-pattern #16).

## Conformance Sweep (Re-run Only)

After config overrides are confirmed, sweep existing domain docs for drift against the new settings. This runs **after** Step 4 but **before** writing files.

### Naming Audit

Check each file's name against the convention defined in the relevant FORMAT spec:

| Directory | Expected pattern | Example |
|-----------|-----------------|---------|
| `docs/prd/` | `PRD-NNNN-<title>.md` | `PRD-0001-user-subscription.md` |
| `docs/adr/` | `<NNNN>-<title>.md` (no `ADR-` prefix) | `0001-event-sourced-orders.md` |
| `docs/research/` | `<stack>-<topic>-<major>.md` | `react-concurrent-rendering-18.md` |

For each mismatch: report `<file> does not match convention — expected <pattern>`. Ask before renaming. Batch multiple files into one question.

### Language Audit

Read `docs/agents/language.md` for expected language. Scan each file's first 3 lines of prose:

- If detected language differs from setting → flag the file
- Do NOT auto-translate → suggest `/write` for translation
- Report: `"<file> is in <detected>, but language.md requires <expected>. Run /write to translate."`

### Format Audit

Compare each file's section headers against its FORMAT spec:

| Type | Required sections |
|------|------------------|
| PRD | `# Title`, `## Goal`, `## Requirements`, `## Acceptance Criteria`, `## Out of Scope`, `## Traceability` |
| ADR | `# Title`, `## Status`, `## Context`, `## Decision`, `## Consequences` |
| Research | `# Title`, `## TL;DR`, `## Question`, `## Approach`, `## Findings`, `## Verdict`, `## Boundary Conditions`, `## Sources` |

Report missing or extra sections. Do NOT auto-add placeholder sections.

### Metadata Consistency

Check PRD `## Traceability` fields against lifecycle:
- `Sliced into` exists but child issues list empty?
- `Status` says `Grilled` but `Grilled by` empty?
- Child Issue referenced but `## Issue` field missing?
- `Status` says `Done` but not all child issues `— Done`?

Informational only — report, don't auto-fix.

### Action Rules

| Category | Action |
|----------|--------|
| **Naming** | Ask per file before renaming. Batch into one question. |
| **Language** | Flag only; suggest `/write`. Never auto-translate. |
| **Format** | Report deviations only. Never auto-add empty sections. |
| **Metadata** | Report inconsistencies only. Never auto-fix. |

## Traceability

This skill does not create or modify PRDs, so it does not fill any PRD `## Traceability` field. Instead, its outputs form the **config layer** of the project's traceability chain:

```
setup-project (config layer)
    ↓ docs/agents/*.md are read by the Entry Protocol
    ↓
think / research / grill / story / tdd / review / debug / improve-architecture / write
    ↓ each fills its own PRD Traceability fields
```

Consumer skills reference these config files via the [Skill Entry Protocol](../rules/entry-protocol.md), which reads `docs/agents/` at startup. Without this setup, consumer skills degrade to guesses and defaults (entry protocol "If missing" paths).

When the project structure changes, re-running `/setup-project` updates the config layer so all downstream skills continue to read correct paths.

## Step 1: Explore

Look at the current repo to understand its starting state. Read whatever exists; don't assume:

- `git remote -v` — is this a GitHub repo? GitLab? No remote?
- `AGENTS.md` and `CLAUDE.md` at the repo root — does either exist? Is there already an `## Agent skills` section in either?
- `CONTEXT.md` and `CONTEXT-MAP.md` at the repo root
- `docs/adr/` and `docs/prd/` directories
- `docs/agents/` — does this skill's prior output already exist?
- `.scratch/` — sign that a local-markdown issue tracker convention is already in use

**Monorepo detection (Step 2):**
- `package.json` with `"workspaces"` field (npm/yarn)
- `pnpm-workspace.yaml` — pnpm workspaces
- `lerna.json` — Lerna monorepo
- `Cargo.toml` with `[workspace]` — Rust monorepo
- `go.work` or `go.mod` with workspace — Go workspace
- `pyproject.toml` with `[tool.poe.tasks]` or similar — Python workspace
- `build.gradle.kts` or `settings.gradle.kts` — Gradle multi-project
- `pom.xml` with `<modules>` — Maven multi-module
- `subprojects/` or `packages/` or `apps/` or `libs/` directory patterns
- `docs/adr/` inside subdirectories — sign of per-package architecture tracking

## Step 2: Detect Project Structure

Based on your exploration, classify the project:

| Signal | Classification |
|---|---|
| No workspace files, no subproject dirs | **Single repo** |
| Workspace files found (see Step 1), multiple packages/apps/libs | **Monorepo** |
| User mentions related repos or sibling repos exist outside this clone | **Multi-repo** |
| Both workspace files AND related repos | **Monorepo + Multi-repo** |

Ask the user to confirm the detection. If unsure, ask: "Is this a single project, a monorepo with multiple packages, or part of a multi-repo setup?"

### Multi-repo: Collect Repo Information

If multi-repo, ask the user for each related repo:
- **Repo name/slug** — e.g., `backend`, `frontend`, `shared`
- **Remote URL** — so skills can reference it
- **Domain role** — what the repo does (API server, web app, shared library, infrastructure)
- **Issue tracker** — which repo's issues should skills use for story creation? (usually the "main" or "frontend" repo)

Record this as `docs/agents/repo-map.md` (see seed template below).

## Step 3: Present Findings

Summarise what's present and what's missing. Show the detected defaults:

- **Project structure**: single repo / monorepo / multi-repo
- **Issue tracker**: GitHub (if remote points to github.com), GitLab (if gitlab.com or self-hosted), or Local markdown (if no remote)
- **Triage labels**: defaults (needs-triage, needs-info, ready-for-agent, ready-for-human, wontfix)
- **Domain docs**: single-context (one CONTEXT.md + docs/adr/ at root) or multi-context (CONTEXT-MAP.md exists)
- **Documentation language**: undetected by default — present as "please choose" (see Section D). If existing PRDs/ADRs/CONTEXT.md are consistently in one language, offer that as the recommended default.

## Step 4: Ask for Overrides

Present the detected configuration. Ask the user: "Does this look right? Anything to change?"

If the user wants to change something, walk through that section **one at a time**:

### Section A — Issue Tracker

> The "issue tracker" is where issues live for this repo. Skills like `story` and `review` read from and write to it — they need to know whether to call `gh issue create`, write a markdown file under `.scratch/`, or follow some other workflow you describe.

Options:
- **GitHub** — issues live in the repo's GitHub Issues (uses the `gh` CLI)
- **GitLab** — issues live in the repo's GitLab Issues (uses the `glab` CLI)
- **Local markdown** — issues live as files under `.scratch/<feature>/` in this repo (good for solo projects or repos without a remote)
- **Other** (Jira, Linear, etc.) — ask the user to describe the workflow in one paragraph; the skill will record it as freeform prose

For **multi-repo**: ask which repo owns the primary issue tracker. The other repos' `issue-tracker.md` can point to the primary repo's tracker.

### Section B — Triage Label Vocabulary

> When issues are created or managed, they carry triage labels. The five canonical roles:

- `needs-triage` — maintainer needs to evaluate
- `needs-info` — waiting on reporter
- `ready-for-agent` — fully specified, AFK-ready (an agent can pick it up with no human context)
- `ready-for-human` — needs human implementation
- `wontfix` — will not be actioned

Ask the user if they want to override any of the default label strings. If their issue tracker has no existing labels, the defaults are fine.

### Section C — Domain Docs

> Some skills (`improve-architecture`, `debug`, `tdd`, `review`) read `CONTEXT.md` for domain language, `docs/adr/` for past decisions, and `docs/prd/` for product requirements. They need to know where these live.

Options:
- **Single-context** — one `CONTEXT.md` + `docs/adr/` + `docs/prd/` at the repo root. Most repos are this.
- **Multi-context** — `CONTEXT-MAP.md` at the root pointing to per-context `CONTEXT.md` files (typically a monorepo). PRDs and ADRs may be per-context or shared.

For **multi-repo**: the domain docs may be split across repos. The `repo-map.md` records which repo owns which docs. Consumer skills check the map first.

### Section D — Documentation Language

> Skills produce a lot of human-facing text: PRDs, ADRs, `CONTEXT.md`, issue bodies and titles, review reports, comments. Writing all of it in one consistent language keeps the docs readable for the whole team — regardless of which member (or agent session) triggered the skill. Without this config, each skill falls back to "follow the user's input language", which drifts whenever a different member runs a skill.

Options:
- **English** — all human-facing output is written in English.
- **Chinese (中文)** — all human-facing output is written in Chinese.
- **Other** — name the language (e.g. 日本語, Deutsch); skills write output in it.

This is a **single language for the whole project** — it applies uniformly to PRDs, ADRs, `CONTEXT.md`, Issues, and comments. It is recorded in `docs/agents/language.md`, and every consumer skill reads it via the Skill Entry Protocol. Code, identifiers, and CLI commands are never affected — only prose.

**Detection heuristic (Step 3):** there is nothing in the repo that reliably reveals the team's preferred doc language, so do **not** guess. Surface this section as "undetected — please choose" and let the user pick. If `CONTEXT.md` or existing PRDs already exist and are consistently in one language, offer that as the recommended default.

**Common pitfall:** the user typing the command is not necessarily the audience. A Chinese-speaking developer may still want English docs for an international team. Ask which language the *team* reads, not which language the conversation is in.

## Step 5: Confirm

Show the user a draft of all files to be written. Let them edit before writing.

## Step 6: Write

**Pick the file to edit:**

- If `CLAUDE.md` exists, edit it.
- Else if `AGENTS.md` exists, edit it.
- If neither exists, ask the user which one to create — don't pick for them.

Never create `AGENTS.md` when `CLAUDE.md` already exists (or vice versa) — always edit the one that's already there.

If an `## Agent skills` block already exists in the chosen file, update its contents in-place rather than appending a duplicate. Don't overwrite user edits to the surrounding sections.

**The `## Agent skills` block** (single-repo / monorepo baseline; multi-repo adds the Repo map section):

```markdown
## Agent skills

### Issue tracker

[one-line summary of where issues are tracked]. See `docs/agents/issue-tracker.md`.

### Triage labels

[one-line summary of the label vocabulary]. See `docs/agents/triage-labels.md`.

### Domain docs

[one-line summary of layout — "single-context" or "multi-context"]. See `docs/agents/domain.md`.

### Documentation language

[one-line summary — e.g. "all docs in English"]. See `docs/agents/language.md`.

<!-- Multi-repo only: include this section -->
### Repo map

[one-line summary of multi-repo structure]. See `docs/agents/repo-map.md`.
```

Then write the docs files using the seed templates in [templates/](templates/).

### Monorepo: Per-Package Config

For each detected package with its own domain scope, create `docs/agents/` inside that package as well, but with a simpler config:

```markdown
# Domain Docs (package: <pkg-name>)

This package's domain docs:
- **`CONTEXT.md`** at the package root (falls back to repo root if missing)
- **`docs/adr/`** at the package root (falls back to repo root if missing)

For shared conventions (including documentation language), see repo root `docs/agents/`.
```

**On re-run:** check that per-package `docs/agents/` dirs are still in sync with the current package structure. If packages were added, create new per-package configs. If packages were removed/renamed, update or remove the corresponding per-package configs (**ask first** before removing — destructive).

## Step 7: Done

	Tell the user the setup is complete and which engineering skills will now read from these files. Mention they can edit `docs/agents/*.md` directly later. Re-run this skill whenever the project structure changes, issue tracker switches, domain docs are reorganized, or documentation language preference changes. Re-running is always safe — it detects what changed and only touches affected files.

---

## Seed Templates

Each `docs/agents/` file is generated from a seed template, customised based on the user's choices in Step 3-4. The templates live as separate files so they can be maintained independently and read on demand:

| Output file | Seed template | When used |
|---|---|---|
| `docs/agents/issue-tracker.md` | [templates/issue-tracker-github.md](templates/issue-tracker-github.md) | Remote points to github.com |
| | [templates/issue-tracker-gitlab.md](templates/issue-tracker-gitlab.md) | Remote points to gitlab.com or self-hosted GitLab |
| | [templates/issue-tracker-local.md](templates/issue-tracker-local.md) | No remote (local markdown in `.scratch/`) |
| `docs/agents/triage-labels.md` | [templates/triage-labels.md](templates/triage-labels.md) | Always (edit right-hand column to match the tracker's vocabulary) |
| `docs/agents/domain.md` | [templates/domain.md](templates/domain.md) | Always. **Before writing:** scan `docs/prd/`, `docs/adr/`, `docs/research/` for existing files; replace the example filenames in the template's File structure section with the actual filenames, and omit empty/missing branches. On first run (no docs yet), use the template examples as-is. |
| `docs/agents/language.md` | [templates/language.md](templates/language.md) | Always (fill in the team's chosen language) |
| `docs/agents/repo-map.md` | [templates/repo-map.md](templates/repo-map.md) | Multi-repo only |

Read the relevant template file, apply the user's Step 4 overrides, and write the customised result to the target path.
