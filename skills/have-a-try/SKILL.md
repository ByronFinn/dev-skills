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

The two branches produce very different artifacts — picking wrong wastes the whole prototype. If ambiguous and user isn't reachable, default by matching surrounding code (backend module → LOGIC; page/component → UI) and **state the assumption** at the top of the prototype.

## Rules That Apply to Both Branches

1. **Throwaway from day one.** Locate prototype close to its target code; name it to signal prototype, not production. Follow project routing conventions. *(Honors anti-pattern #14)*
2. **One command to run.** Use project's existing task runner. *(anti-pattern #31 — run command is the success contract.)*
3. **No persistence by default.** In-memory state. If persistence IS the question, use a scratch store with a clear "PROTOTYPE" name.
4. **Skip the polish.** No tests, no error handling beyond runnability, no abstractions. *(Prototype-scoped; opposite of `/tdd` discipline — don't let it leak.)*
5. **Surface the state.** Print/render full relevant state after every action or variant switch.
6. **Delete or absorb when done.** Capture the verdict, then delete the shell or fold validated core into real code. Don't leave it rotting.

## Process Summary

**Step 0 — Bootstrap.** Apply the [Skill Entry Protocol](../rules/entry-protocol.md). Read `CONTEXT.md` and `docs/adr/` — reuse validated domain language and decisions instead of re-deriving. State what's missing.

**Step 1 — State the question.** Write down the model/question being prototyped (top-of-file comment or `NOTES.md`). A prototype answering the wrong question is pure waste.

**Step 2 — Pick the branch.** Logic vs UI. If ambiguous, match surrounding code; state the assumption.

**Step 3 — Build.** Follow branch process in [REFERENCE.md](REFERENCE.md). Match project's existing language, tooling, conventions — don't add new runtimes or structures. *(anti-pattern #21)*

**Step 4 — Hand it over.** Give the user the run command (logic) or URL + `?variant=` keys (UI). They drive it. The interesting moments are "wait, that shouldn't be possible" — those are bugs in the *idea*, which is the point.

**Step 5 — Capture the answer and dispose.** Record the verdict (PRD `Prototyped by` / ADR / commit / `NOTES.md`). Then delete the shell or absorb its validated core.

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
