---
name: setup-project
description: "Scaffold or update per-repo configuration for engineering skills: issue tracker convention, triage label vocabulary, domain doc layout, and multi-repo coordination. Run before first use of story, review, or any skill that creates issues or reads domain docs. Re-run when project structure changes (new repo added, tracker switched, docs reorganized)."
when_to_use: "setup,initialize,initialise,configure skills,issue tracker setup,new project,update config,project changed,添加仓库,配置变更"
dispatch_intent: "Project initialization, skill configuration, AGENTS.md setup, config update"
---

# Setup Project

🥷 Configure the repo so skills know where to read and write.

Scaffold the per-repo configuration that the engineering skills assume:

- **Project structure** — single repo, monorepo (multiple packages in one repo), or multi-repo (multiple related repos)
- **Issue tracker** — where issues live (GitHub, GitLab, local markdown, or other)
- **Triage labels** — the strings used for the five canonical triage roles
- **Domain docs** — where `CONTEXT.md`, ADRs, and PRDs live; how consumer skills find them across repos

This is a prompt-driven skill, not a deterministic script. Explore, present what you found, confirm with the user, then write.

**Can be re-run.** If `docs/agents/` already exists, read current config first, detect what changed since last setup, present only the sections that need updating, and rewrite affected files. The user can also use this to switch issue trackers, add/remove repos from the map, or reorganize domain docs.

## Outcome Contract

- **Outcome**: `docs/agents/` directory with issue-tracker, triage-labels, domain docs, and (for multi-repo) repo-map; `## Agent skills` block in AGENTS.md
- **Done when**: User confirms configuration, all files written, AGENTS.md updated
- **Evidence**: `docs/agents/issue-tracker.md`, `docs/agents/triage-labels.md`, `docs/agents/domain.md`; `docs/agents/repo-map.md` (multi-repo only)
- **Output**: Summary of configuration, next step to use engineering skills

## Process Summary

**Step 1: Explore** — detect current repo state (remote, AGENTS.md, existing docs/agents/, workspace/monorepo structure). If `docs/agents/` exists, read all current config files to understand existing setup.

**Step 2: Detect project structure** — single repo, monorepo, or multi-repo. Ask the user if detection is uncertain or if there are related repos not visible in this clone. If config already exists, compare detected structure against `repo-map.md` to find what changed.

**Step 3: Present findings** — show detected defaults (project structure, issue tracker, triage labels, domain layout). If updating, show a diff of what changed vs current config.

**Step 4: Ask for overrides** — present the full detected configuration as a draft; ask if anything needs changing. If the user wants to change something, walk through that section one at a time. If everything looks good, proceed.

**Step 5: Confirm** — show the complete draft of all files to be written (AGENTS.md block + each `docs/agents/` file). If updating, show only files that changed.

**Step 6: Write** — edit AGENTS.md, create or update `docs/agents/*.md` files. Update in-place, never append duplicates.

**Step 7: Done** — list skills now configured, suggest next step

See [REFERENCE.md](REFERENCE.md) for seed templates and detailed steps.

## Gotchas

| What happened | Rule |
|---|---|
| Assumed GitHub without checking remote | Step 1: Run `git remote -v` first |
| Missed monorepo/multi-repo structure | Step 2: Check for workspace files, subprojects, sibling repos |
| Monorepo: only configured root, missed packages | Step 6: Create per-package `docs/agents/` dirs in monorepo |
| Multi-repo: no coordination between repos | Step 6: Create `repo-map.md` linking repos to skill domains |
| Domain docs don't mention `docs/prd/` | Step 6: Domain config lists PRDs, ADRs, and CONTEXT paths |
| Asked all decisions at once | Step 4: Present detected defaults, ask for overrides |
| Created AGENTS.md when CLAUDE.md exists | Step 6: Edit the file that already exists |
| Duplicated existing `## Agent skills` block | Step 6: Update in-place, don't append |
| Used wrong skill names in templates | Replace with dev-skills skill names |
| Wrote files without user confirmation | Step 5: Show full draft before writing |
| Re-run: overwrote unchanged config sections | Step 1: Read existing config first, only update what changed |
| Re-run: missed structural drift (repos added/removed) | Step 2: Compare detected structure against existing `repo-map.md` |

Shared behavioral constraints: apply [../rules/anti-patterns.md](../rules/anti-patterns.md) when a global anti-pattern is relevant.

## Output

**First run:**
```
Setup complete.

Configuration:
- Project structure: <single / monorepo / multi-repo>
- Issue tracker: <GitHub / GitLab / Local / Other>
- Triage labels: <defaults / customised>
- Domain docs: <single-context / multi-context>

Updated files:
- AGENTS.md — added ## Agent skills block
- docs/agents/issue-tracker.md — created
- docs/agents/triage-labels.md — created
- docs/agents/domain.md — created
- docs/agents/repo-map.md — created (multi-repo only)

Skills now configured: think, grill, story, tdd, review, debug, improve-architecture

Next: Start using skills. Run /think to brainstorm a feature, or /debug to investigate a bug.
```

**Re-run (config update):**
```
Config updated.

Changes:
- <what changed, e.g., "Added frontend repo to repo-map">
- <what changed, e.g., "Switched issue tracker from GitHub to GitLab">

Updated files:
- docs/agents/<file>.md — updated (changed: <sections>)
- <... other files ...>

Unchanged: docs/agents/<files not touched> — no changes needed

Next: Re-run affected skills if config change affects their behavior (e.g., after tracker switch, re-run /story for new issues).
```
