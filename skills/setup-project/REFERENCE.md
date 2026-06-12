# Setup Project: Detailed Reference

## Re-run Behavior

This skill can be run multiple times. When `docs/agents/` already exists:

1. **Read current config** — load all existing `docs/agents/*.md` files before detecting anything new
2. **Detect drift** — compare current repo state against existing config:
   - `git remote -v` vs `issue-tracker.md` — did the tracker change?
   - Workspace files vs `repo-map.md` — were repos added/removed?
   - `CONTEXT.md` location vs `domain.md` — were domain docs reorganized?
   - Label usage vs `triage-labels.md` — did label vocabulary change?
3. **Present diff** — show what changed vs what stayed the same. Only ask about changed sections.
4. **Update selectively** — rewrite only files that need changes. Leave untouched files alone.

If the user says "update repo map" or "switch issue tracker", focus on that section only. Still read everything first to verify nothing else drifted.

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

For shared conventions, see repo root `docs/agents/`.
```

## Step 7: Done

Tell the user the setup is complete and which engineering skills will now read from these files. Mention they can edit `docs/agents/*.md` directly later — re-running this skill is only necessary if they want to switch issue trackers or restart from scratch.

---

## Seed Templates

Below are the seed templates for each `docs/agents/` file. Use these as a starting point, customising based on the user's choices in Step 3.

### issue-tracker-github.md

```markdown
# Issue tracker: GitHub

Issues and PRDs for this repo live as GitHub issues. Use the `gh` CLI for all operations.

## Conventions

- **Create an issue**: `gh issue create --title "..." --body "..."`. Use a heredoc for multi-line bodies. Issue body format follows the Story Format: includes `## What to build`, `## Acceptance Criteria`, `## Blocked by` sections.
- **Read an issue**: `gh issue view <number> --comments`, filtering comments by `jq` and also fetching labels.
- **List issues**: `gh issue list --state open --json number,title,body,labels,comments --jq '[.[] | {number, title, body, labels: [.labels[].name], comments: [.comments[].body]}]'` with appropriate `--label` and `--state` filters.
- **Comment on an issue**: `gh issue comment <number> --body "..."`
- **Apply / remove labels**: `gh issue edit <number> --add-label "..."` / `--remove-label "..."`
- **Close**: `gh issue close <number> --comment "..."`

Infer the repo from `git remote -v` — `gh` does this automatically when run inside a clone.

## When a skill says "publish to the issue tracker"

Create a GitHub issue. Use the Story Format body (## What to build, ## Acceptance Criteria, ## Blocked by).

## When a skill says "fetch the relevant ticket"

Run `gh issue view <number> --comments`.
```

### issue-tracker-gitlab.md

```markdown
# Issue tracker: GitLab

Issues and PRDs for this repo live as GitLab issues. Use the [`glab`](https://gitlab.com/gitlab-org/cli) CLI for all operations.

## Conventions

- **Create an issue**: `glab issue create --title "..." --description "..."`. Use a heredoc for multi-line descriptions. Pass `--description -` to open an editor. Issue body format follows the Story Format: includes `## What to build`, `## Acceptance Criteria`, `## Blocked by` sections.
- **Read an issue**: `glab issue view <number> --comments`. Use `-F json` for machine-readable output.
- **List issues**: `glab issue list -F json` with appropriate `--label` filters.
- **Comment on an issue**: `glab issue note <number> --message "..."`. GitLab calls comments "notes".
- **Apply / remove labels**: `glab issue update <number> --label "..."` / `--unlabel "..."`. Multiple labels can be comma-separated or by repeating the flag.
- **Close**: `glab issue close <number>`. `glab issue close` does not accept a closing comment, so post the explanation first with `glab issue note <number> --message "..."`, then close.
- **Merge requests**: GitLab calls PRs "merge requests". Use `glab mr create`, `glab mr view`, `glab mr note`, etc. — the same shape as `gh pr ...` with `mr` in place of `pr` and `note`/`--message` in place of `comment`/`--body`.

Infer the repo from `git remote -v` — `glab` does this automatically when run inside a clone.

## When a skill says "publish to the issue tracker"

Create a GitLab issue. Use the Story Format body (## What to build, ## Acceptance Criteria, ## Blocked by).

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
- Issue body follows the Story Format: `## What to build`, `## Acceptance Criteria`, `## Blocked by`
- Triage state is recorded as a `Status:` line near the top of each issue file (see `triage-labels.md` for the role strings)
- Comments and conversation history append to the bottom of the file under a `## Comments` heading

## When a skill says "publish to the issue tracker"

Create a new file under `.scratch/<feature-slug>/issues/` (creating the directory if needed). Use the Story Format body.

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

If any of these files don't exist, **proceed silently**. Don't flag their absence; don't suggest creating them upfront. The producer skills (`/grill` for CONTEXT.md and ADRs, `/think` or `/story` for PRDs) create them lazily.

## What to do if files are missing

If `CONTEXT.md` doesn't exist yet, consumer skills should proceed without it. The first run of `/grill` will create it lazily. Do not create an empty `CONTEXT.md` during setup — an empty file is noise.

Same for `docs/prd/` and `docs/adr/` — create them only when there's actual content to write.

## File structure

Single-context repo (most repos):

```
/
├── CONTEXT.md
├── docs/
│   ├── prd/
│   │   ├── user-subscription.md
│   │   └── payment-integration.md
│   └── adr/
│       ├── 0001-event-sourced-orders.md
│       └── 0002-postgres-for-write-model.md
└── src/
```

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
