---
name: have-a-try
description: "Build a throwaway prototype to answer one design question with disposable code. Two branches: a tiny interactive terminal app for logic/state-model questions, or several radically different UI variations toggleable from one route. Use when a design doubt is easier to resolve by running code than by reasoning on paper — state machine edges, data-model expressiveness, or what a page should look like."
when_to_use: "prototype,原型,试一下,spike,验证一下,看看效果,跑起来看看,有没有更简单的方式,这个状态机对不对,这个数据模型能表达吗"
dispatch_intent: "Design validation via throwaway prototype code"
---

# Have-a-Try: Throwaway Prototype to Answer a Design Question

🥷 Write disposable code to answer one question. The question decides the shape.

A prototype is **throwaway code that answers a question**. The validated answer is the only thing worth keeping — the code itself is deleted or absorbed. This sits between `/think` (pure conversation, no code) and `/tdd` (serious red-green-refactor with gates). Use it when a design doubt is cheaper to resolve by *running* code than by *reasoning* about it.

## Outcome Contract

- **Outcome**: One validated design answer (the question it was answering is resolved), captured durably. Prototype code either deleted or its validated core absorbed into real code.
- **Done when**: The question is answered and the verdict recorded (PRD `## Traceability` / ADR / commit message / `NOTES.md` next to the prototype). Prototype disposed of.
- **Evidence**: The prototype runs via one command; the user (or a follow-up pass) recorded the verdict.
- **Output**: Question, branch taken, verdict, where it was captured, prototype disposition.

## Pick a Branch

Identify which question is being answered — from the user's prompt, the surrounding code, or by asking if the user is around:

- **"Does this logic / state model feel right?"** → **LOGIC mode** ([REFERENCE.md](REFERENCE.md)). Build a tiny interactive terminal app that pushes the state machine through cases that are hard to reason about on paper.
- **"What should this look like?"** → **UI mode** ([REFERENCE.md](REFERENCE.md)). Generate several radically different UI variations on a single route, switchable via a URL search param and a floating bottom bar.

The two branches produce very different artifacts — getting this wrong wastes the whole prototype. If the question is genuinely ambiguous and the user isn't reachable, default to whichever branch better matches the surrounding code (a backend module → logic; a page or component → UI) and **state the assumption at the top of the prototype**.

## Rules That Apply to Both Branches

1. **Throwaway from day one, and clearly marked as such.** Locate the prototype code close to where it will actually be used (next to the module or page it's prototyping for) so context is obvious — but name it so a casual reader can see it's a prototype, not production. For throwaway UI routes, obey whatever routing convention the project already uses; don't invent a new top-level structure. *(Honors anti-pattern #14 — tell the user where prototype files are created.)*
2. **One command to run.** Whatever the project's existing task runner supports — `pnpm <name>`, `python <path>`, `bun <path>`, etc. The user must be able to start it without thinking. *(Run command is the success contract — see anti-pattern #31.)*
3. **No persistence by default.** State lives in memory. Persistence is the thing the prototype is _checking_, not something it should depend on. If the question explicitly involves a database, hit a scratch DB or a local file with a clear "PROTOTYPE — wipe me" name.
4. **Skip the polish.** No tests, no error handling beyond what makes the prototype _runnable_, no abstractions. The point is to learn something fast and then delete it. *(This is a prototype-scoped rule. It is the opposite of `/tdd`'s test-first discipline — do not let this mindset leak into production code.)*
5. **Surface the state.** After every action (logic) or on every variant switch (UI), print or render the full relevant state so the user can see what changed.
6. **Delete or absorb when done.** When the prototype has answered its question, either delete it or fold the validated decision into the real code — don't leave it rotting in the repo.

## Process Summary

**Step 0 — Bootstrap.** Apply the [Skill Entry Protocol](../rules/entry-protocol.md) to locate domain docs. Read `CONTEXT.md` and `docs/adr/` even when there's no PRD — reuse already-validated domain language and past decisions instead of re-deriving them in the prototype. State what's missing.

**Step 1 — State the question.** Before writing code, write down what model/question is being prototyped in one paragraph (top-of-file comment or prototype `README`/`NOTES.md`). A prototype that answers the wrong question is pure waste.

**Step 2 — Pick the branch.** Logic vs UI (see above). If ambiguous, match surrounding code; state the assumption.

**Step 3 — Build.** Follow the branch's process in [REFERENCE.md](REFERENCE.md). Match the project's existing language, tooling, and conventions — don't add a new package manager, runtime, component library, or routing structure for the prototype. *(Honors anti-pattern #21 — read project conventions at runtime, don't hardcode them into skill behavior.)*

**Step 4 — Hand it over.** Give the user the one run command (logic) or the URL + `?variant=` keys (UI). They drive it. The interesting moments are "wait, that shouldn't be possible" or "huh, I assumed X would be different" — those are bugs in the _idea_, which is the whole point.

**Step 5 — Capture the answer and dispose.** When the prototype has done its job, capture the verdict durably (PRD `## Traceability` `Prototyped by` field / ADR / commit / `NOTES.md`). Then delete the prototype or absorb its validated core. Don't leave it rotting.

See [REFERENCE.md](REFERENCE.md) for the full LOGIC mode and UI mode processes, anti-patterns, and the floating switcher spec.

Shared behavioral constraints: apply [../rules/anti-patterns.md](../rules/anti-patterns.md) when a global anti-pattern is relevant.

## Gotchas

| What happened | Rule |
|---|---|
| Wrong branch picked (built a UI prototype for a logic question, or vice versa) | Step 2: the two branches produce very different artifacts — confirm the question type first; when ambiguous, match surrounding code and state the assumption |
| Didn't write the question down before coding | Step 1: a prototype answering the wrong question is pure waste — make the question explicit and checkable |
| Prototype references `console.log`/prompts/escape codes in its logic module | LOGIC mode: keep the logic in a pure portable module; the TUI is a thin shell — nothing flows back |
| Variants differ only in colour or copy | UI mode: that's a tweak, not a prototype. Real variants disagree about structure (layout, hierarchy, primary affordance) |
| Prototype left rotting in repo after the question was answered | Step 5: capture the verdict, then delete the shell or absorb the validated core into real code |
| Added tests / error handling / abstractions to the prototype | Rule 4: skip the polish — the point is to learn fast then delete. (Prototype-scoped; do NOT carry this into `/tdd`) |
| Hardcoded the project's component library / routing convention into behavior | Honor anti-pattern #21: read conventions at runtime, don't bake repo-specific facts into skill rules |
| Prototype created files without telling the user where | Honor anti-pattern #14: state the prototype file location explicitly |
| Tried to wire the prototype to the real database by default | Rule 3: in-memory by default; only touch a scratch store if persistence IS the question |

## Output

```
Have-a-try complete.

Question:  <the one question being answered, one sentence>
Branch:    LOGIC | UI
Run:       <the one command, or URL + ?variant= keys>

Verdict:   <what the prototype taught us — the validated answer>
           e.g. "The state machine does NOT handle X→Y; needs an explicit guard."

Captured at: <PRD-NNNN ## Traceability Prototyped by | ADR-NNNN | commit | NOTES.md>

Prototype disposition:
- Deleted (shell only, nothing worth keeping) | Absorbed core into <real module/route> (shell deleted)

Next:
- If the verdict changes the design: /think to re-evaluate, or /grill to update the PRD
- If the design is now decision-complete: /grill → /story → /tdd
```

**PRD Traceability:** If a PRD exists for the feature, fill the `Prototyped by` field in its `## Traceability` section so downstream skills know a prototype validated (or invalidated) a design assumption:

```markdown
- **Prototyped by**: `/have-a-try` (<YYYY-MM-DD>) — <one-line question + verdict>
```
