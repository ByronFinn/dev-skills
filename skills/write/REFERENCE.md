# Write: Reference

Detailed pattern catalogs, mode procedures, and reference files loaded by the Write skill.

> **How to use**: Reference files are a catalog of smells, not a checklist to run top to bottom. The principles in `SKILL.md` Core Stance apply: over-editing is failure, the author's voice wins, and lists are examples not find-and-replace. A sentence that already reads natural stays. Match the smell, not the word.

## File Index

| File | Purpose | Loaded when |
|------|---------|-------------|
| [write-en.md](references/write-en.md) | English prose: AI-taste patterns, sentence structures, tone patterns, quick checks | Text is English |
| [write-zh.md](references/write-zh.md) | Chinese prose: full AI-taste pattern catalog, structural rules for long-form articles | Chinese text (full catalog) |
| [write-zh-prose.md](references/write-zh-prose.md) | Chinese prose: top-10 high-frequency patterns, quick rules | Chinese text (quick reference) |
| [write-zh-bilingual.md](references/write-zh-bilingual.md) | CN/EN bilingual: spacing, punctuation, terminology consistency, translationese patterns | Mixed CN/EN, translation review |
| [write-zh-release-notes.md](references/write-zh-release-notes.md) | Release notes and social posts: tweet rules, release format, public-facing checks | "release", "changelog", "tweet" |
| [write-product-localization.md](references/write-product-localization.md) | Product localization: multi-locale review, surface splitting, locale-specific failure patterns | Multi-locale product copy |

## Reference Files

### English Prose (`write-en.md`)

See [references/write-en.md](references/write-en.md). Key sections:
- Core rules (cut filler, break formulaic structures, use active voice, be specific)
- Word choice (overused emphasis adverbs, AI vocabulary table, pompous copulas)
- Sentence structures to avoid (negative parallelism, rhetorical self-questions, anaphora, false agency)
- Tone patterns to avoid (false suspense, patronizing analogies, futurist invitation, pedagogical hand-holding)
- Paragraph and composition patterns (bold-first bullets, fractal summaries, dead metaphor, one-point dilution)
- Quick checks before delivering

### Chinese Prose (`write-zh.md`)

See [references/write-zh.md](references/write-zh.md). Key sections:
- Execution flow (preserve meaning → de-AI → smooth sentences → adjust punctuation)
- Natural > stylized (don't force colloquialisms)
- Technical long-form default mode
- AI-taste patterns (summary-tone sentences, contrast frames, explanation-voice openers)
- Sentence structure rules (no em-dash, no telegraph-style short sentences)
- Word simplification table
- Punctuation rules (brackets, quotes, semicolons, spacing)
- Structural-level patterns for long-form articles (cross-section repetition, table re-reading)
- Title design and list rules

### Chinese Quick Reference (`write-zh-prose.md`)

See [references/write-zh-prose.md](references/write-zh-prose.md). Top 10 high-frequency patterns:
1. Summary-tone ending sentences
2. Sublimation sentences
3. Contrast frames ("不是…而是…")
4. Bold subheading pattern
5. Chapter transition sentences
6. Vague adjective pre-judgment
7. Parallel bold titles
8. Intra-paragraph repetition
9. Explanation-voice openers
10. Preachy openers

### Bilingual (`write-zh-bilingual.md`)

See [references/write-zh-bilingual.md](references/write-zh-bilingual.md). Key rules:
- CN/EN spacing: space between Chinese and English characters
- Punctuation consistency: Chinese uses `、。？！；：`
- English terms: first appearance annotation, subsequent Chinese-only
- Translationese patterns (physical-action verbs, abstract-noun subjects)
- Bilingual layout (EN block / CN block, numbered correspondence)

### Release Notes & Social Posts (`write-zh-release-notes.md`)

See [references/write-zh-release-notes.md](references/write-zh-release-notes.md). Key rules:
- Tweet five rules (community lead, highlights, UX framing, one stance, native rhythm)
- Release notes format (Breaking → Features → Fixes → Deprecations)
- Public-facing pre-check (identity anonymization, no competitor bashing, user-feeling first)
- Pre-release checks (no "stop maintaining" signals, bilingual correspondence)

### Product Localization (`write-product-localization.md`)

See [references/write-product-localization.md](references/write-product-localization.md). Key rules:
- Split surfaces before editing
- Keep product facts fixed
- Use source files as edit targets
- Review final rendered surface
- Locale-specific failure patterns (Chinese, Japanese, Korean, German, Spanish, French, Italian)
- Rewrite rules (preserve placeholders, no broad find-and-replace without residual scan)

## Mode Procedures

### Long-form Article Mode

1. Read the whole article. Map all sections, tables, lists, images.
2. Flag structural problems:
   - Cross-section repetition (same checklist/judgment in 2+ sections)
   - Table re-reading (prose walks the rows of the table above it)
   - Whole redundant sections or paragraphs
3. Propose cuts as change-points. Show before-to-after. Confirm with user.
4. Line-level de-AI, section by section, per loaded reference file.
5. Output change-points, not a full rewrite. Only rewrite when user explicitly approves.

### Release Notes Mode

1. Gather style references: read project's existing releases (changelog, release page, `gh release view`).
2. Extract from `git log <last-tag>..HEAD` rather than memory. Read every `feat:` and `fix:` commit.
3. Group by user-perceivable feature, not internal taxonomy.
4. One sentence per item, naming the user-visible change.
5. Bilingual: English block and Chinese block as parallel sections.

### Public Reply Mode

1. Re-read the live issue/PR with `gh issue view <num>` or `gh pr view <num>`.
2. Draft reply:
   - `@<reporter>` + thanks line (match reporter's language)
   - Cause in one sentence, impact in one sentence
   - Ship state: shipped / on main / planned / not planned
   - Two paragraphs max
3. No em-dash. No meta narration about your own process.

### Document Review Mode

1. Privacy scan: detect PII, job-seeking signals, personal data leakage.
2. Tone consistency: flag voice shifts, register mismatches, formulaic phrasing.
3. Bilingual validation: confirm CN/EN translation accuracy.
4. Rendering check: placeholder text, broken image links.
5. Durable-doc scan: if the document is a review report or snapshot, flag dated claims and stale references.
6. Output: reviewed text + `privacy: clear / N issues found`.

### Paragraph Coherence Mode

1. Work through each paragraph in sequence.
2. Flag: abrupt topic shifts, disconnected opening sentences, monotone rhythm.
3. Suggest minimal fixes (one word, one reordered clause, one bridging sentence).
4. Output: numbered list with paragraph location and one-line fix suggestion.

## Maintenance Notes

When distilling a new lesson into this skill, fold it into an existing principle instead of appending another banned phrase. The skill must not grow monotonically; collapsing specifics back into principles is part of maintaining it.
