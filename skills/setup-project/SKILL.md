---
name: setup-project
description: "Scaffold per-repo configuration for engineering skills: issue tracker convention, triage label vocabulary, and domain doc layout. Run before first use of story, review, or any skill that creates issues or reads domain docs."
when_to_use: "setup,initialize,initialise,configure skills,issue tracker setup,new project"
dispatch_intent: "Project initialization, skill configuration, AGENTS.md setup"
---

# Setup Project

🥷 Configure the repo so skills know where to read and write.

Scaffold the per-repo configuration that the engineering skills assume:

- **Issue tracker** — where issues live (GitHub, GitLab, local markdown, or other)
- **Triage labels** — the strings used for the five canonical triage roles
- **Domain docs** — where `CONTEXT.md` and ADRs live, and the consumer rules for reading them

This is a prompt-driven skill, not a deterministic script. Explore, present what you found, confirm with the user, then write.

## Outcome Contract

- **Outcome**: `docs/agents/` directory with issue-tracker, triage-labels, and domain docs; `## Agent skills` block in AGENTS.md
- **Done when**: User confirms configuration, all files written, AGENTS.md updated
- **Evidence**: `docs/agents/issue-tracker.md`, `docs/agents/triage-labels.md`, `docs/agents/domain.md`
- **Output**: Summary of configuration, next step to use engineering skills

## Process Summary

**Step 1: Explore** — detect current repo state (remote, AGENTS.md, existing docs/agents/)

**Step 2: Present findings** — show detected defaults (issue tracker, triage labels, domain layout)

**Step 3: Ask for overrides** — present the full detected configuration as a draft; ask if anything needs changing. If the user wants to change something, walk through that section one at a time. If everything looks good, proceed.

**Step 4: Confirm** — show the complete draft of all files to be written (AGENTS.md block + each `docs/agents/` file)

**Step 5: Write** — edit AGENTS.md, create `docs/agents/*.md` files

**Step 6: Done** — list skills now configured, suggest next step

See [REFERENCE.md](REFERENCE.md) for seed templates and detailed steps.

## Gotchas

| What happened | Rule |
|---|---|
| Assumed GitHub without checking remote | Step 1: Run `git remote -v` first |
| Asked all three decisions at once | Step 3: Present detected defaults, ask for overrides |
| Created AGENTS.md when CLAUDE.md exists | Step 5: Edit the file that already exists |
| Duplicated existing `## Agent skills` block | Step 5: Update in-place, don't append |
| Used wrong skill names in templates | Replace with dev-skills skill names |
| Wrote files without user confirmation | Step 4: Show full draft before writing |

Shared behavioral constraints: apply [../rules/anti-patterns.md](../rules/anti-patterns.md) when a global anti-pattern is relevant.

## Output

```
Setup complete.

Configuration:
- Issue tracker: <GitHub / GitLab / Local / Other>
- Triage labels: <defaults / customised>
- Domain docs: <single-context / multi-context>

Updated files:
- AGENTS.md — added ## Agent skills block
- docs/agents/issue-tracker.md — created
- docs/agents/triage-labels.md — created
- docs/agents/domain.md — created

Skills now configured: think, grill, story, tdd, review, debug, improve-architecture

Next: Start using skills. Run /think to brainstorm a feature, or /debug to investigate a bug.
```
