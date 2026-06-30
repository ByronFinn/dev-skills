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

A catalog of smells, not a checklist. Use it to recognize AI taste, then make judgment calls.

- **Over-editing is failure.** If a sentence is natural, leave it. Most polish is subtraction — cut repetition, summary-tone, restated conclusions.
- **The author's voice wins.** Keep colloquial words, cadence, and stance. When a rule conflicts with authorial or genre choice, the author wins.
- **Banned-phrase lists are examples, not find-and-replace.** Match the smell, not the string.
- **Prefer fewer, stronger edits.** Three changes that matter beat thirty mechanical swaps.

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

- **Meaning first, style second.** If removing an AI pattern changes the author's meaning, keep the original.
- **No silent restructuring.** Edit in place unless structure changes explicitly requested. (Exception: Long-form Article Mode proposes cuts as change-points first.)
- **Artifact-grounded claims.** For release/social/product copy, ground factual claims in real source material (current app behavior, runnable artifact, screenshot, changelog, issue/PR, user draft). Do not rely on memory or stale screenshots.
- **No em-dash.** Never produce em-dash (U+2014) or en-dash (U+2013). Replace any found in drafts before returning. Use commas, periods, colons, or parentheses instead.
- **Stop after output.** Deliver the rewritten text only. No changelog, no commentary. (Exception: Long-form Article Mode returns change-points for review.)

## Modes

See [REFERENCE.md](REFERENCE.md) for detailed mode procedures (Long-form Article, Bilingual Review, Release Notes, Document Review).

| Mode | Trigger | Reference File(s) |
|------|---------|-------------------|
| **Chinese prose** | Chinese text, general editing | `write-zh-prose.md`, `write-zh.md` |
| **English prose** | English text, general editing | `write-en.md` |
| **Bilingual review** | Mixed CN/EN, translation review | `write-zh-bilingual.md` |
| **Product localization** | "本地化文案", multi-locale review | `write-product-localization.md` |
| **Release notes** | "release", "changelog", "version" | `write-zh-release-notes.md` |
| **Long-form article** | Multi-section Markdown, >300 lines | see REFERENCE.md |
| **Tweet / social post** | "推特", "tweet", "social post" | `write-zh-release-notes.md` |
| **Public reply** | "回复 issue", "reply to PR" | see below |
| **Document review** | "审稿", "check this document" | see REFERENCE.md |
| **Paragraph coherence** | "连贯性", "coherence" | see below |

### Public Reply Mode (GitHub issue / PR)

Activate when: "回复 issue", "reply to PR", "comment on #N".

1. Open with `@<reporter>` + one thanks line in the reporter's language.
2. State cause in one sentence, impact in one sentence.
3. State ship state: already shipped, fixed on main, planned, or not planned.
4. Two paragraphs max. No bullet lists, no section headers.
5. No em-dash.
Before posting, re-read the live issue/PR. Do not reply from memory.

### Paragraph Coherence Mode

Activate when: "连贯性", "段落连贯", "可读性", "coherence", "flow check".

Do not rewrite. Instead flag: transitions that shift topic without signal, opening sentences that don't follow from previous paragraph's close, and monotone sentence length. Suggest minimal fix per issue. Output: numbered list with paragraph location and one-line fix suggestion.

### Tweet / Social Post Mode

Activate when: "推特", "twitter", "X推文", "tweet", "social post", "发文".

Lead with community (star count, user thanks). Pick 2-4 highlights. Frame each point as user benefit ("你用它的时候..."). Include one opinionated sentence. Use native Chinese rhythm. Close casually with invitation, not CTA.

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
