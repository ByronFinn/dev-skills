# Setup Project: Detailed Reference

## Re-run Checklist

When `docs/agents/` already exists, run this drift detection loop **before** any user interaction. Each config file is checked against the current repo state:

| Config file | Detection check | Drift signal | Action |
|---|---|---|---|
| `issue-tracker.md` | `git remote -v` → does the remote match the tracker type in the file? | Remote changed (GitHub→GitLab, or no remote→local) | Present change, confirm, rewrite `issue-tracker.md` |
| `triage-labels.md` | Check actual labels on 1-2 recent issues → do they still match the file? | Labels renamed, added, or deprecated | Present change, confirm, rewrite `triage-labels.md` |
| `domain.md` | Does `CONTEXT-MAP.md` exist now when it didn't before? Were domain dirs (`docs/prd/`, `docs/adr/`, `docs/research/`) reorganized? | Context layout changed (single↔multi), dirs moved | Present change, confirm, rewrite `domain.md` |
| `language.md` | Read existing value. Ask: "Is `<language>` still the right doc language for the team?" | Team's language preference changed since last setup | Confirm, rewrite `language.md` |
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

**Rule:** Migration implies rewriting more files than a normal re-run. Always present the full diff of what will be created, rewritten, and removed. Get explicit approval before removing any files (anti-pattern #17).

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

**The `## Agent skills` block (single repo / monorepo):**

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
```

**The `## Agent skills` block (multi-repo):**

```markdown
## Agent skills

### Issue tracker

[one-line summary of where issues are tracked]. See `docs/agents/issue-tracker.md`.

### Triage labels

[one-line summary of the label vocabulary]. See `docs/agents/triage-labels.md`.

### Domain docs

[one-line summary of layout]. See `docs/agents/domain.md`.

### Documentation language

[one-line summary — e.g. "all docs in English"]. See `docs/agents/language.md`.

### Repo map

[one-line summary of multi-repo structure]. See `docs/agents/repo-map.md`.
```

Then write the docs files using the seed templates below.

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

Below are the seed templates for each `docs/agents/` file. Use these as a starting point, customising based on the user's choices in Step 3.

### issue-tracker-github.md

```markdown
# Issue tracker: GitHub

Issues and PRDs for this repo live as GitHub issues. Use the `gh` CLI for all operations.

## Conventions

- **Create an issue**: `gh issue create --title "..." --body "..."`. Use a heredoc for multi-line bodies. Issue body format follows the Story Format (see `STORY-FORMAT.md` from dev-skills): includes `## What to build`, `## Acceptance Criteria`, `## Blocked by` sections.
- **Read an issue**: `gh issue view <number> --comments`, filtering comments by `jq` and also fetching labels.
- **List issues**: `gh issue list --state open --json number,title,body,labels,comments --jq '[.[] | {number, title, body, labels: [.labels[].name], comments: [.comments[].body]}]'` with appropriate `--label` and `--state` filters.
- **Comment on an issue**: `gh issue comment <number> --body "..."`
- **Apply / remove labels**: `gh issue edit <number> --add-label "..."` / `--remove-label "..."`
- **Close**: `gh issue close <number> --comment "..."`

Infer the repo from `git remote -v` — `gh` does this automatically when run inside a clone.

## When a skill says "publish to the issue tracker"

Create a GitHub issue. Use the Story Format (see `STORY-FORMAT.md` from dev-skills) body (## What to build, ## Acceptance Criteria, ## Blocked by).

## When a skill says "fetch the relevant ticket"

Run `gh issue view <number> --comments`.
```

### issue-tracker-gitlab.md

```markdown
# Issue tracker: GitLab

Issues and PRDs for this repo live as GitLab issues. Use the [`glab`](https://gitlab.com/gitlab-org/cli) CLI for all operations.

## Conventions

- **Create an issue**: `glab issue create --title "..." --description "..."`. Use a heredoc for multi-line descriptions. Pass `--description -` to open an editor. Issue body format follows the Story Format (see `STORY-FORMAT.md` from dev-skills): includes `## What to build`, `## Acceptance Criteria`, `## Blocked by` sections.
- **Read an issue**: `glab issue view <number> --comments`. Use `-F json` for machine-readable output.
- **List issues**: `glab issue list -F json` with appropriate `--label` filters.
- **Comment on an issue**: `glab issue note <number> --message "..."`. GitLab calls comments "notes".
- **Apply / remove labels**: `glab issue update <number> --label "..."` / `--unlabel "..."`. Multiple labels can be comma-separated or by repeating the flag.
- **Close**: `glab issue close <number>`. `glab issue close` does not accept a closing comment, so post the explanation first with `glab issue note <number> --message "..."`, then close.
- **Merge requests**: GitLab calls PRs "merge requests". Use `glab mr create`, `glab mr view`, `glab mr note`, etc. — the same shape as `gh pr ...` with `mr` in place of `pr` and `note`/`--message` in place of `comment`/`--body`.

Infer the repo from `git remote -v` — `glab` does this automatically when run inside a clone.

## When a skill says "publish to the issue tracker"

Create a GitLab issue. Use the Story Format (see `STORY-FORMAT.md` from dev-skills) body (## What to build, ## Acceptance Criteria, ## Blocked by).

## When a skill says "fetch the relevant ticket"

Run `glab issue view <number> --comments`.
```

### issue-tracker-local.md

```markdown
# Issue tracker: Local Markdown

Issues and PRDs for this repo live as markdown files in `.scratch/`.

## Conventions

- One feature per directory: `.scratch/<feature-slug>/`
- The PRD is `.scratch/<feature-slug>/PRD.md`
- Implementation issues are `.scratch/<feature-slug>/issues/<NN>-<slug>.md`, numbered from `01`
- Issue body follows the Story Format (see `STORY-FORMAT.md` from dev-skills): `## What to build`, `## Acceptance Criteria`, `## Blocked by`
- Triage state is recorded as a `Status:` line near the top of each issue file (see `triage-labels.md` for the role strings)
- Comments and conversation history append to the bottom of the file under a `## Comments` heading

## When a skill says "publish to the issue tracker"

Create a new file under `.scratch/<feature-slug>/issues/` (creating the directory if needed). Use the Story Format (see `STORY-FORMAT.md` from dev-skills) body.

## When a skill says "fetch the relevant ticket"

Read the file at the referenced path. The user will normally pass the path or the issue number directly.
```

### triage-labels.md

```markdown
# Triage Labels

The skills speak in terms of five canonical triage roles. This file maps those roles to the actual label strings used in this repo's issue tracker.

| Canonical role | Label in our tracker | Meaning                                  |
| -------------- | -------------------- | ---------------------------------------- |
| `needs-triage`             | `needs-triage`       | Maintainer needs to evaluate this issue  |
| `needs-info`               | `needs-info`         | Waiting on reporter for more information |
| `ready-for-agent`          | `ready-for-agent`    | Fully specified, ready for an AFK agent  |
| `ready-for-human`          | `ready-for-human`    | Requires human implementation            |
| `wontfix`                  | `wontfix`            | Will not be actioned                     |

When a skill mentions a role (e.g. "apply the AFK-ready triage label"), use the corresponding label string from this table.

Edit the right-hand column to match whatever vocabulary you actually use.

<!-- For multi-repo projects, add cross-repo labels:
| `cross-repo`         | `cross-repo`         | Touches multiple repositories            |
-->
```

### domain.md

```markdown
# Domain Docs

How the engineering skills should consume this repo's domain documentation when exploring the codebase.

## Before exploring, read these

- **`CONTEXT.md`** at the repo root — domain glossary (core concepts, terminology, relationships)
- **`CONTEXT-MAP.md`** at the root if it exists — it points at one `CONTEXT.md` per context. Read each one relevant to the topic.
- **`docs/prd/`** — product requirements documents. Skills like `improve-architecture` and `review` read these for planned features and acceptance criteria.
- **`docs/adr/`** — architecture decision records. Read ADRs that touch the area you're about to work in. In multi-context repos, also check `src/<context>/docs/adr/` for context-scoped decisions.
- **`docs/research/INDEX.md`** — searchable index of persisted technical research records (stack × topic × major). `/think` Step 5 queries it before re-searching; `/research` produces records here.

If any of these files don't exist, **proceed silently**. Don't flag their absence; don't suggest creating them upfront. The producer skills (`/grill` for CONTEXT.md and ADRs, `/think` or `/story` for PRDs) create them lazily.

## What to do if files are missing

If `CONTEXT.md` doesn't exist yet, consumer skills should proceed without it. The first run of `/grill` will create it lazily. Do not create an empty `CONTEXT.md` during setup — an empty file is noise.

Same for `docs/prd/`, `docs/adr/`, and `docs/research/` — create them only when there's actual content to write.

## File structure

Single-context repo (most repos):

```
/
├── CONTEXT.md
├── docs/
│   ├── prd/
│   │   ├── PRD-0001-user-subscription.md
│   │   └── PRD-0002-payment-integration.md
│   ├── adr/
│   │   ├── 0001-event-sourced-orders.md
│   │   └── 0002-postgres-for-write-model.md
│   └── research/
│       ├── INDEX.md
│       ├── react-concurrent-rendering-18.md
│       └── postgres-index-strategy-15.md
└── src/
```

**File naming conventions** (producer skills define these; consumer skills read them):

- PRD: `PRD-NNNN-<title>.md` — see `PRD-FORMAT.md` (dev-skills /think)
- ADR: `<NNNN>-<title>.md` (no `ADR-` prefix) — see `ADR-FORMAT.md` (dev-skills /grill)
- Research: `<stack>-<topic>-<major>.md` — see `RESEARCH-FORMAT.md` (dev-skills /research)

Multi-context repo (presence of `CONTEXT-MAP.md` at the root):

```
/
├── CONTEXT-MAP.md
├── docs/
│   ├── prd/                           ← shared PRDs
│   └── adr/                           ← system-wide decisions
└── src/
    ├── ordering/
    │   ├── CONTEXT.md
    │   └── docs/adr/                  ← context-specific decisions
    └── billing/
        ├── CONTEXT.md
        └── docs/adr/
```

## Use the glossary's vocabulary

When your output names a domain concept (in an issue title, a refactor proposal, a hypothesis, a test name), use the term as defined in `CONTEXT.md`. Don't drift to synonyms the glossary explicitly avoids.

If the concept you need isn't in the glossary yet, that's a signal — either you're inventing language the project doesn't use (reconsider) or there's a real gap (note it for `/grill`).

## Flag ADR conflicts

If your output contradicts an existing ADR, surface it explicitly rather than silently overriding:

> _Contradicts ADR-0007 (event-sourced orders) — but worth reopening because…_
```

### language.md

```markdown
# Documentation Language

The language engineering skills should write **human-facing output** in for this repo.

## Language

**<English / 中文 / Other — fill in the team's choice>**

All prose produced by skills — PRDs (`docs/prd/`), ADRs (`docs/adr/`), `CONTEXT.md`, issue titles and bodies, review reports, and comments — is written in this language.

## Scope

- **In scope**: human-facing prose in documents and issues.
- **Out of scope**: code, identifiers, file names, CLI commands, and configuration values. These follow code conventions, never this setting.

## When a skill says "write the output"

Write the prose in the language above. Do not silently switch to the conversation's language — the team reads the configured language, which may differ from whoever triggered the skill.

If a single artifact genuinely needs a second language (e.g. a bilingual release note), the producing skill may deviate, but the configured language is always the primary one.

## If this file is missing

Fall back to the user's input language, and ask which language the team prefers so it can be recorded here. Don't keep guessing every session.
```

### repo-map.md (multi-repo only)

```markdown
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
```
