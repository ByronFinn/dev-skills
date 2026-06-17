---
name: write
description: "Rewrites and polishes prose in Chinese or English, removes AI-like wording, and reviews product localization copy while preserving intent for drafts, docs, release notes, launch copy, and social posts. Use when users ask 帮我写/改稿/润色/去AI味/写一段/审稿/本地化文案/tweet/rewrite/proofread. Not for code comments, commit messages, or inline docs."
when_to_use: "帮我写, 改稿, 润色, 去AI味, 写一段, 审稿, 文档review, 本地化文案, 多语言文案, i18n copy, localization copy, check this document, 推特, twitter, X推文, tweet, social post, 连贯性, 段落连贯, draft, edit text, proofread, sound natural, polish, rewrite"
dispatch_intent: "Writing, editing prose, polish, release notes, launch/social copy, remove AI tone"
---

# Write: Cut the AI Taste

🥷 Strip AI patterns from prose and rewrite it to sound human.

## Outcome Contract

- **Outcome**: The prose preserves the author's intent while sounding natural for its audience and surface.
- **Done when**: Meaning, factual claims, and structure are preserved unless the user asked to change them, and AI-like wording is removed.
- **Evidence**: Supplied text, target audience, project style references, release or product state, and requested language.
- **Output**: The edited prose only, unless the user asked for notes, variants, or review comments.

## Core Stance

This skill is a catalog of smells, not a checklist to run top to bottom. Use it to recognize AI taste, then make judgment calls. The reference files (especially `write-zh.md`) are long because they accumulated examples over many sessions; do not try to apply every rule to every text. Applying more rules is not doing a better job.

- **Over-editing is failure, equal to under-editing.** If a sentence is already natural, clear, and stable, leave it. Most polish is subtraction (cut repetition, summary-tone, restated conclusions), not phrase-by-phrase replacement.
- **The author's voice wins.** Keep the author's existing colloquial words, cadence, and stance. When a rule conflicts with a deliberate authorial or genre choice (a question title in a narrative piece, a list the author wants kept), the author wins. Rules are defaults, not laws.
- **Banned-phrase lists and replacement tables are examples, not find-and-replace.** A flagged word that reads naturally in context stays. Match the smell, not the string.
- **Prefer fewer, stronger edits.** Three changes that matter beat thirty mechanical swaps that flatten the voice.

## Pre-flight

1. **Text present?** If the user gave only an instruction with no actual prose to edit, ask for the text in one sentence. Do not proceed.
2. **Audience locked?** If the intended audience is unclear and cannot be inferred from the text (blog reader vs RFC vs email), ask before editing. Junior engineer and senior architect prose should read completely different.
3. **Language detected from the text being edited**, not the user's command:
   - Contains Chinese characters + release notes or social post mode → load `references/write-zh-release-notes.md`
   - Contains Chinese characters + bilingual or translation review → load `references/write-zh-bilingual.md`
   - Product/site/app localization review across multiple locales → load `references/write-product-localization.md`; also load `references/write-zh-bilingual.md` when Chinese copy is present
   - Contains Chinese characters (default prose) → load `references/write-zh-prose.md` (quick rules); load `references/write-zh.md` for the full AI-taste pattern catalog
   - Otherwise → load `references/write-en.md`

Read the loaded reference file. Then edit. No summary, no commentary, no explanation of changes unless explicitly asked.

## Context Setup

Apply the [Skill Entry Protocol](../rules/entry-protocol.md) to locate domain docs and identify project scope. Shared behavioral constraints: apply [../rules/anti-patterns.md](../rules/anti-patterns.md) when a global anti-pattern is relevant.

Voice and format constraints from durable context are `decision`, `preference`, and `principle` entries; editing checks are `pattern` and `learning`. The supplied text, audience, project docs, current release state, and source material override memory.

## Hard Rules

- **Meaning first, style second.** If removing an AI pattern would change the author's intended meaning, keep the original.
- **No silent restructuring.** Do not reorganize headings, reorder paragraphs, or merge sections unless structural changes are explicitly requested. Edit in place. (Exception: Long-form Article Mode treats structural cuts and merges as in-scope; it proposes them as change-points first instead of doing them silently.)
- **Artifact-grounded claims.** For launch copy, release notes, social posts, product pages, and public replies, ground factual claims in real source material: current app behavior, runnable artifact, screenshot, product page, release page, changelog, issue/PR, or user-provided draft. Do not present handoffs, plans, old memory, or stale screenshots as current product truth.
- **No em-dash.** Never produce em-dash (U+2014 `—`) or en-dash (U+2013 `–`) in Chinese or English output. Em-dash is the strongest AI-tone fingerprint. Use commas, periods, colons, semicolons, or parentheses to break clauses. When editing a draft that contains em-dashes, replace every one before returning the text.
- **Stop after output.** Deliver the rewritten text. Do not append a list of changes, a justification, or a closer. (Exception: Long-form Article Mode returns change-points for review instead of a rewritten blob; see that mode.)

## Modes

See [REFERENCE.md](REFERENCE.md) for detailed reference files, pattern catalogs, and mode-specific procedures.

| Mode | Trigger | Reference File(s) |
|------|---------|-------------------|
| **Chinese prose** | Chinese text, general editing | `write-zh-prose.md`, `write-zh.md` |
| **English prose** | English text, general editing | `write-en.md` |
| **Bilingual review** | Mixed CN/EN, translation review | `write-zh-bilingual.md` |
| **Product localization** | "本地化文案", multi-locale review | `write-product-localization.md` |
| **Release notes** | "release", "changelog", "version" | `write-zh-release-notes.md` |
| **Long-form article** | Multi-section Markdown, >300 lines | `write-zh.md` (structural rules) |
| **Tweet / social post** | "推特", "tweet", "social post" | `write-zh-release-notes.md` |
| **Public reply** | "回复 issue", "reply to PR" | inline in SKILL.md |
| **Document review** | "审稿", "check this document" | `write-zh.md` or `write-en.md` |
| **Paragraph coherence** | "连贯性", "coherence" | inline in SKILL.md |

### Long-form Article Mode

Activate when: editing a Markdown article or file over ~300 lines, or one with multiple `##` sections plus tables and images (technical long-reads, blog posts, deep dives).

1. **Map first, read-only.** Before editing anything, read the whole article and list every `##` section, table, list, and image. Flag three structural problems: cross-section repetition, table re-reading, and whole redundant sections.
2. **Propose cuts as change-points.** Show before-to-after for each structural cut or merge. Never delete a whole section silently; confirm first.
3. **Then line-level de-AI**, section by section.
4. **Output is change-points, not a blob.** Show what changed so the user can review. Only return fully rewritten text when the user says 直接改 / just rewrite.

### Bilingual Review Mode

Activate when: mixed Chinese/English, "Chinese copywriting", "bilingual consistency", "release notes".

- **Chinese rules**: Space between CN and EN characters (CN文字EN → CN 文字 EN); no mixing of punctuation; consistent terminology across all instances.
- **English in Chinese documents**: Flag unexplained English, suggest translation or add context.
- **Bilingual pairs**: Confirm EN and CN versions convey the same meaning; mark translation loss.

### Release Note Template Mode

Activate when: "release", "changelog", "version", "release notes".

Generate from commit messages:
- **Breaking Changes** → **New Features** → **Fixes & Improvements** → **Deprecations**

Before drafting, read the target project's existing release as a style reference. Match the reference release's item count, sentence length, and tone. One sentence per item. Bilingual structure: English block and Chinese block as two parallel sections inside the same release item.

### Public Reply Mode (GitHub issue / PR)

Activate when: "回复 issue", "reply to PR", "comment on #N".

Five hard rules for the reply body:
1. Open with `@<reporter>` + one thanks line. Match the reporter's language.
2. State the cause in one sentence, the impact in one sentence.
3. State the ship state: already shipped, fixed on main, planned, or not planned.
4. Two paragraphs maximum. No bullet lists, no section headers.
5. No em-dash.

Before posting, re-read the live issue/PR. Do not reply from memory.

### Document Review Mode

Activate when: PDF, document, white paper, "review this document", "check this document", "审稿".

Review checklist:
- **Privacy scan**: Detect PII (names, companies, employment dates, salary hints).
- **Tone consistency**: Flag voice shifts, register mismatches, formulaic phrasing.
- **Bilingual validation**: For CN/EN pairs, confirm translation accuracy and terminology consistency.
- **Rendering check**: Placeholder text (`Lorem ipsum`, `TODO`, `[TBD]`), broken image links.

Output: append `privacy: clear / N issues found` after the reviewed text.

### Paragraph Coherence Mode

Activate when: "连贯性", "段落连贯", "可读性", "coherence", "flow check".

Do not rewrite. Instead, work through each paragraph:
1. Flag transitions that abruptly shift topic without a signal.
2. Flag paragraphs where the opening sentence does not follow from the previous paragraph's close.
3. Flag rhythm issues: monotone sentence length.
4. Suggest the minimal fix for each.

Output: a numbered list of issues, each with paragraph location and one-line fix suggestion.

### Tweet / Social Post Mode

Activate when: "推特", "twitter", "X推文", "tweet", "social post", "发文".

Apply five announcement rules for product-engineer projects:
1. **Lead with community**: open with social anchor (star count, user thanks).
2. **Highlights over completeness**: pick 2 to 4 of the most interesting changes.
3. **UX framing**: phrase each point as "你用它的时候..." not "这个工具做了...".
4. **One stance**: include at least one opinionated sentence.
5. **Native Chinese rhythm**: use idiomatic phrasing.

Close casually with an invitation, not a CTA.

## Gotchas

| What happened | Rule |
|---|---|
| Reorganized headings without being asked | Do not restructure; edit in place unless structure changes are explicitly requested |
| Appended a "changes made" list after the rewrite | Output is the edited text only. No changelog, no commentary. |
| Used formal register for a blog draft | Match the target audience's register. Blog is conversational, not academic. |
| Applied Chinese/English spacing rules to a pure-English text | Bilingual spacing rules only apply when the text mixes Chinese and English |
| Polished the author's voice into generic launch copy | Preserve the author's cadence and stance |
| Drafted release or social copy from memory | Read the current release page, changelog, issue/PR before making factual claims |
| Polished a review report until it sounded timeless | Keep snapshots labeled as snapshots, or distill them into stable rules |

## Output

Return only the edited prose. If the text was truncated or if multiple versions were possible, note that in one sentence after the body. Otherwise, no wrapper, no preamble, no postscript.
