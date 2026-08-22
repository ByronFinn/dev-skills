# Have-a-Try Reference

Detailed processes for the four tactics, plus the CUSTOM synthesis rules. Pick the tactic in [SKILL.md](SKILL.md) first — building the wrong one wastes the whole demo.

---

# Chapter: LOGIC Mode — Interactive Probe

Use when the core conflict is **"does this logic / state model / data shape actually hold up"** — the kind of thing that looks reasonable on paper but only feels wrong once you push it through real cases. A tiny interactive app lets the adjudicator drive the model by hand.

By default a terminal app in the host project's language. When the person adjudicating doesn't live in a terminal (PM, designer, domain expert), build the [shareable HTML variant](#the-shareable-html-variant) instead.

## When This Is the Right Shape

- "I'm not sure if this state machine handles the edge case where X then Y."
- "Does this data model actually let me represent the case where..."
- "I want to feel out what the API should look like before writing it."
- Anything where someone wants to **press buttons and watch state change**.

If the conflict is "what should this look like" — wrong tactic. Use [UI mode](#chapter-ui-mode--side-by-side-variants). If it's "which is faster" — use [BENCH mode](#chapter-bench-mode--comparative-measurement).

## Process

### 1. State the divergence

Before writing code, write down what state model and what conflicting positions you're prototyping ("this machine handles X→Y" vs "it can't"). One paragraph, in the demo's README or a comment at the top of the file; in the HTML variant, a visible intro — not just a comment. A probe answering the wrong divergence is pure waste — make it explicit so it can be checked later, whether the user is watching now or returning to it AFK.

### 2. Check who will drive it

The adjudicator decides the shell:

- **A developer (the default)** → terminal app in the host project's language. Continue with steps 3–9.
- **A non-developer judging the design** (PM, designer, domain expert) → a keyboard TUI is the wrong vehicle. Build the [shareable HTML variant](#the-shareable-html-variant): one self-contained file they double-click — no terminal, no install. State the trade-off in the intro: the pure module inside it is JavaScript, so in a non-JS codebase the **verdict is portable, the module isn't**.

Either way, **labels speak the domain, not the code**: buttons and state fields use the business's vocabulary — the Skill Entry Protocol's `CONTEXT.md` read supplies the glossary when one exists — not reducer/action identifiers. The person judging shouldn't have to translate.

### 3. Pick the language

Use whatever the host project uses. If the project has no obvious runtime (e.g. a docs repo), ask.

Match the project's existing conventions for tooling — don't add a new package manager or runtime just for the demo. (The HTML variant is the one exception: its runtime is the browser, by design.)

### 4. Isolate the logic in a portable module

Put the actual logic — the bit that's answering the question — behind a small, pure interface that could be lifted out and dropped into the real codebase later. The shell around it is throwaway; the logic module shouldn't be.

The right shape depends on the question:

- **A pure reducer** — `(state, action) => state`. Good when actions are discrete events and state is a single value.
- **A state machine** — explicit states and transitions. Good when "which actions are even legal right now" is part of the question.
- **A small set of pure functions** over a plain data type. Good when there's no implicit current state — just transformations.
- **A class or module with a clear method surface** when the logic genuinely owns ongoing internal state.

Pick whichever shape best fits the question being asked, *not* whichever is easiest to wire to a shell. Keep it pure: no I/O, no terminal code, no `console.log` for control flow. The shell imports it and calls into it; nothing flows the other direction. In the HTML variant the module is a single `<script>` block — same rule: no DOM, no `document`, no handlers reaching inside.

> **This is the core insight of LOGIC mode.** It's what makes the prototype useful past its own lifetime. When the question's been answered, the validated reducer / machine / function set can be lifted into the real module — the shell gets deleted.

### 5. Build the smallest TUI that exposes the state

Build it as a **lightweight TUI** — on every tick, clear the screen (`console.clear()` / `print("\033[2J\033[H")` / equivalent) and re-render the whole frame. The user should always see one stable view, not an ever-growing scrollback.

Each frame has two parts, in this order:

1. **Current state**, pretty-printed and diff-friendly (one field per line, or formatted JSON). Use **bold** for field names or section headers and **dim** for less important context (timestamps, IDs, derived values). Native ANSI escape codes are fine — `\x1b[1m` bold, `\x1b[2m` dim, `\x1b[0m` reset. No need to pull in a styling library unless one is already in the project. Under the state, one **change line** for what the last action moved — `→ order.status: pending → shipped`, or a `▸` marker on changed fields — so after a full re-render the eye lands on the delta, not the whole panel.
2. **Keyboard shortcuts**, listed at the bottom: `[a] add user  [d] delete user  [t] tick clock  [q] quit`. Bold the key, dim the description, or vice-versa — whatever reads cleanly.

Behaviour:

1. **Initialise state** — a single in-memory object/struct. Render the first frame on start.
2. **Read one keystroke (or one line)** at a time, dispatch to a handler that mutates state.
3. **Re-render** the full frame after every action — don't append, replace.
4. **Loop until quit.**

The whole frame should fit on one screen.

### 6. Script the awkward cases as guided scenarios

Free play alone hopes the user stumbles into the interesting cases. Don't hope — script them:

- Each scenario has a short **domain-language name**, a one-line **"what to watch for"**, and an ordered list of actions.
- Entering a scenario **resets to a known initial state**, so it runs the same way every time; each keypress advances one step, re-rendering the full frame (change line included) after each.
- Minimum set: the happy path; the trickiest edge case behind the divergence; and **one sequence that should be rejected** — "wait, that shouldn't be possible" is the whole point.
- In the TUI, scenarios hang off the shortcut bar (`[s] scenarios` → `[1] refund after shipping   [2] double-charge guard`); `[f]` returns to free play. In the HTML variant, one tab per scenario with the ordered buttons visible.

### 7. Make it runnable in one command

Add a script to the project's existing task runner (`package.json` scripts, `Makefile`, `justfile`, `pyproject.toml`). The user should run `pnpm run <prototype-name>` or equivalent — never need to remember a path.

If the host project has no task runner, just put the command at the top of the demo's README. For the HTML variant, the file itself is the run command — say "double-click to open" in the intro.

### 8. Hand it over

Give the user the run command (or the file). They'll drive it themselves; the interesting moments are when they say "wait, that shouldn't be possible" or "huh, I assumed X would be different" — those are the bugs in the _idea_, which is the whole point. If they want new actions added, add them. Prototypes evolve.

### 9. Capture the answer

When the probe has done its job, the answer to the divergence is the only thing worth keeping. The verdict may **select** ("the model holds — absorb it") or **eliminate** ("it breaks on X — this design assumption is dead"); both are full successes. If the user is around, ask what it taught them. If not, leave a `NOTES.md` next to the demo so the answer can be filled in before the demo gets deleted.

## Anti-Patterns (LOGIC Mode)

- **Don't add tests.** A prototype that needs tests is no longer a prototype.
- **Don't wire it to the real database.** Use an in-memory store unless the question is specifically about persistence.
- **Don't generalise.** No "what if we wanted to support X later." The prototype answers one divergence.
- **Don't blur the logic and the shell together.** If the reducer / state machine references `console.log`, prompts, terminal escape codes, DOM, or `document`, it's no longer portable. Keep the shell as a thin layer over a pure module.
- **Don't ship the shell into production.** The shell (TUI or HTML page) is optimised for being driven by hand. The logic module behind it is the bit worth keeping.

## The shareable HTML variant

One file, plain HTML/CSS/JS: no framework, no bundler, no server — everything inline so it opens by double-click and survives being emailed around. Anyone should be able to run it by opening it.

Write it for a non-developer: every label in **domain language**, plain-word explanations of what's happening. Layout, top to bottom:

1. **Title and one-line intro** — the divergence being explored (from step 1), visible, not hidden in a comment.
2. **Current state** — the full relevant state as a readable panel of labelled fields (not a raw JSON dump), re-rendered after every click, with the last change called out.
3. **Free-play buttons** — one per action, always available, so anyone can poke at the model in any order.
4. **Guided scenarios** — one per tab, per step 6: short description, then the ordered buttons for that scenario.

Keep it beautiful but restrained: clean typography, generous spacing, one accent colour. No animations, no gimmicks — nothing that competes with the state and the buttons.

In a non-JS codebase, note the trade-off in the intro: the **verdict is portable, the module isn't** — plan to re-express the validated design in the host language when absorbing.

---

# Chapter: UI Mode — Side-by-Side Variants

Generate **several radically different UI variations** on a single route, switchable from a floating bottom bar. The user flips between variants in the browser, picks one (or steals bits from each), then throws the rest away.

If the conflict is about logic/state rather than what something looks like — wrong tactic. Use [LOGIC mode](#chapter-logic-mode--interactive-probe).

## When This Is the Right Shape

- "What should this page look like?"
- "I want to see a few options for this dashboard before committing."
- "Try a different layout for the settings screen."
- Any time the user would otherwise spend a day picking between three vague mockups in their head.

## Two Sub-Shapes — Strongly Prefer Sub-Shape A

A UI prototype is much easier to judge when it's **butting up against the rest of the app** — real header, real sidebar, real data, real density. A throwaway route on its own is a vacuum: every variant looks fine in isolation. Default to sub-shape A whenever there's a plausible existing page to host the variants. Only reach for sub-shape B if the prototype genuinely has no nearby home.

### Sub-Shape A — Adjustment to an Existing Page (Preferred)

The route already exists. Variants are rendered **on the same route**, gated by a `?variant=` URL search param. The existing data fetching, params, and auth all stay — only the rendering swaps. This is the default; pick it unless there's a specific reason not to.

If the prototype is for something that doesn't yet have a page but *would naturally live inside one* (a new section of the dashboard, a new card on the settings screen, a new step in an existing flow) — that's still sub-shape A. Mount the variants inside the host page.

### Sub-Shape B — A New Page (Last Resort)

Only use this when the thing being prototyped genuinely has no existing page to live inside — e.g. an entirely new top-level surface, or a flow that can't be embedded anywhere sensible.

Create a **throwaway route** following whatever routing convention the project already uses — don't invent a new top-level structure. Name it so it's obviously a prototype (e.g. include the word `prototype` in the path or filename). Same `?variant=` pattern.

Before committing to sub-shape B, sanity-check: is there really no existing page this could be embedded in? An empty route hides design problems that a populated one would expose.

In both sub-shapes the floating bottom bar is identical.

## Process

### 1. State the divergence and pick N

Default to **3 variants**. More than 5 stops being radically different and starts being noise — cap there.

Write down the plan in one line, in the prototype's location or a top-of-file comment:

> "Three variants of the settings page, switchable via `?variant=`, on the existing `/settings` route."

This works whether the user is here to push back or not.

### 2. Generate radically different variants

Draft each variant. Hold each one to:

- The page's purpose and the data it has access to.
- The project's component library / styling system (TailwindCSS, shadcn, MUI, plain CSS, whatever).
- A clear exported component name, e.g. `VariantA`, `VariantB`, `VariantC`.

Variants must be **structurally different** — different layout, different information hierarchy, different primary affordance, not just different colours. Three slightly-tweaked card grids isn't a UI prototype, it's wallpaper. If two drafts come out too similar, redo one with explicit "do not use a card grid" guidance.

### 3. Wire them together

Create a single switcher component on the route:

```tsx
// pseudo-code — adapt to the project's framework
const variant = searchParams.get('variant') ?? 'A';
return (
  <>
    {variant === 'A' && <VariantA {...data} />}
    {variant === 'B' && <VariantB {...data} />}
    {variant === 'C' && <VariantC {...data} />}
    <PrototypeSwitcher variants={['A','B','C']} current={variant} />
  </>
);
```

For sub-shape A (existing page): keep all the existing data fetching above the switcher; only the rendered subtree changes per variant.

For sub-shape B (new page): the throwaway route under `/prototype/<name>` mounts the same switcher.

### 4. Build the Floating Switcher

A small fixed-position bar at the bottom-centre of the screen with three pieces:

- **Left arrow** — cycles to the previous variant (wraps around).
- **Variant label** — shows the current variant key and, if the variant exports a name, that name too. e.g. `B — Sidebar layout`.
- **Right arrow** — cycles forward (wraps around).

Behaviour:

- Clicking an arrow updates the URL search param (use the framework's router — `router.replace` on Next, `navigate` on React Router, etc) so the variant is shareable and reload-stable.
- Keyboard: `←` and `→` arrow keys also cycle. Don't intercept arrow keys when an `<input>`, `<textarea>`, or `[contenteditable]` is focused.
- Visually distinct from the page (e.g. high-contrast pill, subtle shadow) so it's obviously not part of the design being evaluated.
- **Hidden in production builds** — gate on `process.env.NODE_ENV !== 'production'` or an equivalent check, so a stray prototype merge can't ship the bar to users.

Put the switcher in a single shared component so both sub-shapes can reuse it. Locate it wherever shared UI lives in the project.

### 5. Hand it over

Surface the URL (and the `?variant=` keys). The user will flip through whenever they get to it. The interesting feedback is usually **"I want the header from B with the sidebar from C"** — that's the actual design they want.

### 6. Capture the Verdict and Clean Up

Once a variant has won, write down which one and why (commit message, ADR, issue, or a `NOTES.md` next to the prototype if running AFK and the user hasn't responded yet) — and note what the losing variants got wrong, since elimination evidence is half the value. Then:

- **Sub-shape A** — delete the losing variants and the switcher; fold the winner into the existing page.
- **Sub-shape B** — promote the winning variant to a real route, delete the throwaway route and the switcher.

If the verdict is contested or the losing variants have archive value: commit the full set (variants + switcher) to a throwaway branch off main and leave a pointer at the verdict record — then remove them from main. Don't leave variant components or the switcher lying around on main; they rot fast and confuse the next reader.

## Anti-Patterns (UI Mode)

- **Variants that differ only in colour or copy.** That's a tweak, not a prototype. Real variants disagree about structure.
- **Sharing too much code between variants.** A shared `<Header>` is fine; a shared `<Layout>` defeats the point. Each variant should be free to throw out the layout.
- **Wiring variants to real mutations.** Read-only prototypes are fine. If a variant needs to mutate, point it at a stub — the question is "what should this look like", not "does the backend work".
- **Promoting the prototype directly to production.** The variant code was written under prototype constraints (no tests, minimal error handling). Rewrite it properly when you fold it in. (Hand off to `/tdd` for the real, test-first implementation.)

---

# Chapter: BENCH Mode — Comparative Measurement

Use when the core conflict is **"which of these candidates is faster / leaner / scales better"** — A vs B, library vs library, optimized vs unoptimized. The adjudicator is numbers, and numbers are only evidence when the comparison is fair and the environment is recorded.

Comparative only. Open-ended tuning with no candidates to compare ("just make it faster") is `/debug` territory; if documentation settles the choice without your machine and your load, it's `/research` territory.

## When This Is the Right Shape

- "Is A or B faster for our workload?"
- "Does the optimization actually help?" (before vs after)
- "Which of these libraries fits our constraints better?" — typically after `/research` narrowed the field by docs; BENCH settles the final call by measurement.

## Process

### 1. State the divergence and the candidates

Write down the decision, the candidates, the metric(s) — latency? throughput? peak memory? allocation count? — and the acceptable outcomes, **including elimination** ("if B loses on every metric, we drop it").

### 2. Build one shared harness

All candidates do the same work through the same interface: **one harness, candidates plugged in** — shared fixtures, shared data generation, shared timing code. A harness that treats candidates differently measures the harness, not the candidates.

### 3. Make the load honest

Shape the workload like the real one — data size, cardinality, contention — or label the result **synthetic** in the report. Warm up before measuring (JIT, caches, connection pools). Run **N rounds** and **alternate execution order** (A,B,B,A or shuffled) so machine drift, thermal throttling, and cache warmth can't fake a winner.

### 4. Record the environment

Machine, OS, runtime + library versions, data size, number of rounds. Numbers without environment are not reproducible — they aren't evidence.

### 5. Adjudicate

Report per-candidate metrics with **median and p95** (means hide tails). The verdict:

- **Selected** — the winner, plus one line on *why* it wins (allocation? algorithmic complexity? caching?). A win with no explanation teaches nothing.
- **Eliminated** — one or more candidates dropped, with the numbers that dropped them.
- **Tie** — the gap is within run-to-run noise. Say so; a tie that saves you a migration is a real result.
- **All failed** — nothing meets the bar. Also a valid verdict; route back to `/think` for new candidates.

Capture the numbers + environment + verdict where the divergence was born (ADR / PRD / issue), then dispose of the harness per Rule 6.

## Anti-Patterns (BENCH Mode)

- **Reporting only means.** Tails and variance are the story — report median and p95.
- **An unfair harness** — different fixtures or different work per candidate.
- **A verdict without environment** (machine, versions, data size, rounds).
- **Synthetic numbers presented as production behaviour.** Label them, or shape the load realistically.
- **Comparing at one data size only.** The interesting crossovers happen at scale.

---

# Chapter: SPIKE Mode — Concern Verification

Use when the core conflict is **"does option X survive concern C"** — feasibility, concurrency, memory, compatibility, API expressiveness. The adjudicator is a checklist: each concern verified against a targeted demo, producing a **concern×option matrix**.

## When This Is the Right Shape

- "Can this library handle our concurrency pattern?"
- "Will approach X work under constraint Y?" (browser, embedded, offline, size budget...)
- "Which of these three approaches satisfies all our concerns?"

If you can't list the concerns, the divergence isn't ready — the shape is wrong. `/think` first.

## Process

### 1. List the concerns first

Take them from the PRD's Open Questions, ADR pending options, or the user. A concern is a **single checkable statement** ("survives 1k concurrent writes", "installs under the size budget"), not a vibe ("check it works").

### 2. One minimal targeted demo per option

Each demo exercises **only the concerns** — the smallest code that could fail. No walking skeleton, no full feature, no polish. Different options may need different demos; keep them **symmetric in scope**, or the comparison fakes a verdict.

### 3. Verify each concern against each option

Run them. Record per cell: **✓ works / ✗ blocked / △ works with caveat** — a △ must name the caveat in the same cell. The caveat is the finding.

### 4. Adjudicate

The matrix is the evidence. The verdict: **selected** (which option + why), **eliminated** (which options died, on which concern), or **all failed** (→ `/think` for new options). Record matrix + verdict where the divergence was born (ADR / PRD / issue), then dispose of the demos per Rule 6. The production implementation of the survivor goes through `/tdd`, not the spike.

## Anti-Patterns (SPIKE Mode)

- **The spike becomes a real implementation.** Tests, abstractions, polish — inverted priorities. The knowledge is the product, not the code.
- **Concern list missing or vague.** "Check it works" is not a concern; list checkable statements first.
- **Reporting △ as ✓.** The caveat is exactly what the decision needs to know.
- **Asymmetric demos** — a 20-line probe for option A, a mini-framework for option B.

---

# Chapter: CUSTOM — Synthesizing an Experiment

The four tactics are walked paths, not a closed enum. When the divergence matches none of them, synthesize an experiment:

1. **What is the divergence?** Decision + conflicting positions. Can't name it → `/think`.
2. **What evidence would settle it?** If documentation settles it → `/research`. Otherwise name the evidence type — a number, a checklist, a feel, a choice.
3. **What is the smallest disposable rig that produces that evidence?** Borrow from the tactics: scenario resets (LOGIC), `?variant=` switching (UI), a shared harness (BENCH), a ✓/✗ matrix (SPIKE).
4. **Who adjudicates?** A human's feel or choice, numbers, or a checklist — the answer shapes the presentation (interactive demo vs report).

Then run the pipeline: minimal, one command, surface the evidence, adjudicate both ways (select or eliminate), fix the evidence where the divergence was born, dispose of the rig.
