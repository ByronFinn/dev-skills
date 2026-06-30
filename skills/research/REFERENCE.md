# Research Skill — Reference

Detailed process, decision trees, and checklists for the `research` skill. The [SKILL.md](SKILL.md) is the entry point; this file holds the depth.

## Table of Contents

1. [Stack & Topic Granularity Test](#1-stack--topic-granularity-test)
2. [Dedup: Query INDEX Before Writing](#2-dedup-query-index-before-writing)
3. [Version Detection](#3-version-detection)
4. [Authoritative Source Decision Tree](#4-authoritative-source-decision-tree)
5. [Authoritative Source Identification Checklist](#5-authoritative-source-identification-checklist)
6. [Stale Detection & Collaborative Marking](#6-stale-detection--collaborative-marking)
7. [Immutability & Intra-Major Correction](#7-immutability--intra-major-correction)
8. [Integration With Other Skills](#8-integration-with-other-skills)

---

## 1. Stack & Topic Granularity Test

### Stack must be a leaf unit

A **stack** is a single library/framework/language with its own version number and official source. Composite platforms decompose:

| User says | Wrong (composite) | Right (leaf units) |
|---|---|---|
| "Next.js 数据获取" | `nextjs` | `next` + `react` (separate records, topics differ) |
| "MEAN 栈认证" | `mean` | `express` + `mongodb` (separate) |
| "Spring Boot 缓存" | `springboot` | `spring` (acceptable if cache is Spring's own abstraction) or `redis`/`caffeine` if the question is about the cache backend |

**Test**: can you find one official documentation site and one version number for it, independently? If you'd need to combine multiple sites/versions, it's composite — decompose.

### Topic must fit one verdict

A **topic** is right-sized when its answer is a **single one-line verdict**. If the honest answer requires a branching matrix ("in case A do X, in case B do Y"), the topic is too broad — split it.

| Topic | Verdict shape | Verdict |
|---|---|---|
| `concurrent-rendering` | single verdict | "Use useTransition; don't build a scheduler" |
| `rendering` (too broad) | branching matrix | "For concurrent use X, for virtualization use Y, for SSR use Z" → **split** into `concurrent-rendering`, `virtualization`, `ssr` |
| `state-management` (too broad) | branching matrix | "For small apps X, for large Y, for server Z" → **split** |

**Anti-pattern**: writing one record whose `## Findings` is a decision tree that should be three records. Each leaf of the tree is its own topic.

---

## 2. Dedup: Query INDEX Before Writing

Before creating a new record, **always** scan `docs/research/INDEX.md` for an existing record matching `stack + topic + major`. This mirrors Entry Protocol Step 3a (PRD conflict check) and anti-pattern #40 (silent duplicate).

### Match signals (any one = candidate collision)

1. **Filename match** — `<stack>-<topic>-<major>.md` already exists (strongest signal).
2. **Topic + major match** — same topic slug AND same major in INDEX, even if the verdict differs.

### On a candidate collision

Ask the user one question (Preference type, with a recommended answer):

```
Found an existing research record on this stack+topic+major:
- react-concurrent-rendering-18.md — "Use useTransition; don't build a scheduler" (verified)

Is this the same question, or different?
1. Reuse (Recommended) — load and cite the existing record; no new file
2. New record — different topic, create with a distinct topic slug
```

- **Reuse** → cite the existing record path; do not create a new file. If the existing record is stale against the current project, mark it stale (see §6) rather than duplicating.
- **New record** → assign a clearly distinct topic slug.

### On a hit at a *different* major

If `react-concurrent-rendering-17.md` exists and you're researching React 18, this is **not** a duplicate — it's a sibling. Create `react-concurrent-rendering-18.md` (immutability, ADR-0004). Both coexist; INDEX gets a new row.

### On no INDEX yet

If `docs/research/INDEX.md` doesn't exist, this is the first record — create INDEX lazily alongside the record (see INDEX-FORMAT.md). No collision possible.

---

## 3. Version Detection

### Where to read

Read the project's dependency manifest to find the stack's current version:

| Ecosystem | Manifest | Field |
|---|---|---|
| JS/TS | `package.json` / `package-lock.json` | `dependencies` / `devDependencies` |
| Go | `go.mod` | `require` block |
| Rust | `Cargo.toml` / `Cargo.lock` | `[dependencies]` |
| Python | `requirements.txt` / `pyproject.toml` / `Pipfile.lock` | pinned versions |
| Java | `pom.xml` / `build.gradle` | `<dependency>` / `implementation` |

### Major extraction

From a full version like `18.2.0`, the **major** is `18`. The filename gets `-18.md`; the record's `stack@version` field keeps the full `react@18.2.0`.

### Multi-major coexistence (monorepo)

If the same stack appears at multiple majors across the repo (React 17 in package A, React 18 in package B):

- **Each major gets its own record.** Create `react-<topic>-17.md` and `react-<topic>-18.md` separately. Do not merge.
- INDEX gets two rows under the same stack, different major.
- This is the intended behavior — the best practices genuinely differ across majors.

### No manifest readable

If no dependency manifest is found (e.g. a docs-only repo, or the stack isn't a declared dependency):

- Set `stack@version=unknown` in the record header.
- **Skip stale checks** for this record (can't compare versions). Status stays `verified` regardless of project changes.
- Note this in `## Boundary Conditions`: "Version could not be auto-detected; stale checks skipped."

---

## 4. Authoritative Source Decision Tree

```
Is the source produced by the stack's official maintainers themselves?
├── YES → Is it a normative/specification document?
│        ├── YES (official docs, source, spec/standard) → Tier 1 (required primary)
│        └── NO  (changelog, RFC, repo discussion)
│             ├── Is the RFC/proposal Accepted or Merged?
│             │    ├── YES → Tier 2 (supplementary only)
│             │    └── NO  (draft/withdrawn/rejected) → EXCLUDE
│             └── Is it a maintainer-flagged official comment (pinned/labeled)?
│                  ├── YES → Tier 2 (supplementary only)
│                  └── NO  (random contributor comment) → EXCLUDE
└── NO → Is it endorsed-as-official by the maintainers?
         ├── It's a community-maintained site (cppreference, community-period docs) → EXCLUDE
         ├── Personal blog / tutorial / SO answer → EXCLUDE
         ├── AI-generated content → EXCLUDE
         └── Unofficial translation → EXCLUDE
              (Exception: a SO/blog answer that LINKS to a Tier 1 source → cite the Tier 1 source directly, skip the intermediary)
```

**Hard rule**: every verdict needs **at least one Tier 1 source** as primary evidence. A record with only Tier 2 sources fails the contract.

---

## 5. Authoritative Source Identification Checklist

Run this checklist against each candidate source before citing it:

- [ ] **Maintainer-produced?** Is the content authored/hosted by the project's official maintainers (official docs domain, official GitHub org, official spec body)?
- [ ] **Specific page URL?** Does the URL point to the *specific page/section* proving the claim, not a homepage or category index?
- [ ] **Directly accessible?** Is the URL reachable without login/paywall? (Don't cite paywalled or access-restricted content.)
- [ ] **Version-aligned?** Does the source correspond to the major version under study? (Don't cite React 19 docs for a React 18 record.)
- [ ] **Tier classification correct?** If calling it Tier 2: is it an *Accepted/Merged* RFC, an official changelog entry, or a *maintainer-flagged* comment? If none, it's excluded.
- [ ] **Not community-maintained-as-official?** Even widely-trusted community sites (cppreference, MDN for non-Mozilla specs) are excluded unless the maintainers officially own them.
- [ ] **Not AI-generated?** The source must be human-maintainer-authored, not AI output (avoids self-reference loops).

If any check fails, either find a better source or exclude it.

---

## 6. Stale Detection & Collaborative Marking

### Who marks stale

**Any skill reading INDEX** (think/research/grill) is responsible for marking stale when it detects a version mismatch. This is *collaborative* — the first reader to notice flags it, so later readers benefit. No central stale-sweeper.

### Threshold: major-only

A record is marked stale **only when the project's current major is higher than the record's major**:

| Record major | Project current major | Status |
|---|---|---|
| 18 | 18 (any minor/patch) | `verified` |
| 18 | 19 | `stale` |
| 18 | 17 (project downgraded) | `verified` (record covers 18; downgrade is project's concern) |

**Minor/patch differences never trigger stale by default.** Exception: the record's `## Boundary Conditions` explicitly declares "sensitive to minor changes" (e.g. a security library where a patch flips a default). Then minor differences also trigger stale — the author owns that call, not a global rule.

### How to mark stale (two-field edit)

When marking a row stale, edit **both** fields (never embed data in Status):

1. `Status` column → `stale` (pure token, no data)
2. `Version` column → `studied-version → current-major` (e.g. `react@18.2.0 → 19`)

Then add the re-research hint (in the verdict cell or a note below the table):
`→ suggest /research react <topic>-19`

### Do not auto-trigger re-research

Marking stale is a **hint, not an action**. The next `/research` for that stack+topic is the user's explicit decision. Never auto-start research from a stale detection — that would be an unrequested network operation (anti-pattern: unsolicited action).

---

## 7. Immutability & Intra-Major Correction

### Across majors: never edit

A record is frozen the moment it's written. When a new major ships:

- **DO**: Create `<stack>-<topic>-<newmajor>.md` (new file, new INDEX row).
- **DON'T**: Never open `<stack>-<topic>-<oldmajor>.md` to "update" it.

The old record is historical truth for that major era. Editing it would destroy traceability and break the Sources↔version linkage. See ADR-0004.

### Within a major: append, don't rewrite

If you discover an error in an already-written record **for the same major** (e.g. a wrong API signature, a misread source), do **not** silently rewrite the original text. Instead, append a `## Correction` block:

```markdown
## Correction (2026-07-15)

Based on [React official docs: useTransition signature](<URL>) (Tier 1), the original `## Verdict` statement "useTransition returns a tuple" is incorrect — it returns `[isPending, startTransition]`. The original text is retained above for history; the corrected understanding is reflected here.
```

The original prose stays. This preserves auditability within the immutability model.

### When NOT to use Correction

- New major → new file (not Correction).
- New finding that doesn't contradict the original → belongs in the new-major record's Findings.
- The original was right and you were wrong → no Correction needed.

---

## 8. Integration With Other Skills

### `/think` Step 5 (consumer)

Before researching a technical choice, `/think` queries INDEX:
- **Hit at current major** → read the record's TL;DR; reuse the verdict. Default: don't read full record.
- **Hit but stale** → **read full record** (Boundary Conditions decide if old conclusion still applies), then optionally suggest `/research` for the new major.
- **Decision depends on implementation detail** (API shape, code pattern) → **read full record** even if verified.
- **Miss** → either start `/research`, or proceed with inline research and create a record.

### `/grill` (consumer + marker)

`/grill` reads INDEX when challenging a PRD's technical approach. If the PRD cites a research record, grill verifies the citation matches the record's verdict. Grill also marks stale rows it encounters (collaborative marking).

### ADR (referencer)

When the project adopts a research conclusion as a decision, the ADR's `## References` cites the research record path. The research record stays in `docs/research/` (frozen, general truth); the ADR records the *project's* decision. They reference, never copy. See PRD-0001 R14.

### PRD `## Research References` (referencer)

PRDs cite research records in `## Research References`:
```markdown
## Research References
* [react concurrent-rendering](docs/research/react-concurrent-rendering-18.md) — useTransition sufficient for our list filtering
```

This connects the previously-orphaned field to real records (PRD-0001 R9).
