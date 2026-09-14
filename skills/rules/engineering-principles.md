# Engineering Principles

Single source for the principle definitions applied by `/review`, `/improve-architecture`, `/tdd` (Refactor phase), and `/implement` (direct implementation). Consuming skills link here; a principle's meaning, signals, caveats, and phase live together in its entry (anti-patterns.md #38).

**Thresholds live in one place**: [improve-architecture/REFERENCE.md §3.2](../improve-architecture/REFERENCE.md) owns the numeric scan cuts. An entry here states the shape of a violation; the scanner owns the cut.

## How to Apply

1. **A finding needs a named consequence.** State the specific future change the violation makes harder, the bug class it hides, or the duplicated knowledge that has already diverged. Without one there is no finding — a bare "this violates SRP" is [anti-patterns.md #25](anti-patterns.md).
2. **Severity defaults to `minor`.** `major` requires a named, specific consequence: it blocks a planned PRD change, couples tests to implementation, hides state behind a known bug class, or the same knowledge is maintained in diverging copies. A principle tag never *creates* a blocker, and never caps a perspective's own blocker definition — security failures, data loss, breaking bugs, and breaking changes without a migration path stay blockers where that perspective defines them ([review/REFERENCE.md](../review/REFERENCE.md) Chapters 3 and 4).
3. **"Where natural" beats rule-matching.** Each entry's *When NOT to apply* overrides the principle. These are heuristics for judgment, not lint rules.
4. **Scope follows the caller.** `/review` covers changed lines plus the code the change makes wrong ([anti-patterns.md #21](anti-patterns.md)); untouched modules belong to `/improve-architecture`. Generated code, vendored dependencies, migration scripts, and test fixtures are out of scope everywhere.
5. **Project decisions win.** ADRs, `CONTEXT.md` vocabulary, lint config, and framework conventions outrank every principle here.
6. **Conflict precedence**: correctness, security, and recorded decisions > **YAGNI > KISS > DRY > SOLID structure**. Uncalled abstractions cost the most; extracting a helper from three similar lines is negative value ([#8](anti-patterns.md), and the same shape as the archived "compensatory complexity"). Local consistency beats theoretical purity unless the local pattern is itself the finding.
7. **Report, don't refactor.** `/review` reports ([anti-patterns.md #5](anti-patterns.md)); fixes route through `/improve-architecture`, `/story`, or `/implement`.

## Consumer & Ownership Map

One owner per scope, so the two `/review` perspectives never report the same item twice.

| Consumer | Owns |
|---|---|
| `/review` Code Review Sub-Agent — local to the diff | SRP, LSP, ISP, DRY, KISS, YAGNI, LoD, Composition over Inheritance, Explicit over Implicit, Fail Fast, Immutability & Pure Functions |
| `/review` Impact Review Sub-Agent — cross-module | DIP, OCP, newly introduced abstractions and seams, new coupling |
| `/improve-architecture` | The mechanically detectable signal for each of the 13 (thresholds in [REFERENCE.md §3.2](../improve-architecture/REFERENCE.md)) |
| `/tdd` Refactor phase | Every entry whose Phase is `refactor-safe` — read the Phase field, not a copied list |
| `/implement` direct implementation | Every principle, design-time terms (this path has no Refactor phase behind it) |

**Overlap resolution:** when both review perspectives see the same principle issue, the diff-local instance belongs to Code Review and the cross-module boundary belongs to Impact Review. Chapter 5 already treats "different sub-agents finding different issues" as complementary, not a contradiction.

## Phase legend

- **design-time** — applies while writing new code.
- **refactor-safe** — applies in `/tdd`'s Refactor phase: structure changes, behavior and public surface do not.
- **review** — a judgment to report, never a change to make inside a refactor.

---

## Catalog

### Single Responsibility (SRP)

- **Meaning**: One unit, one reason to change. Validation, persistence, notification, and formatting do not share a unit.
- **Signals**: A unit carrying two nameable responsibilities; a class whose method count rivals its purpose; a name like Manager/Handler/Service that never narrows.
- **When NOT to apply**: A deliberate facade or adapter presents one simple surface over several concerns — that is its job, and splitting can force callers to know more. Plain data carriers have no responsibilities to separate.
- **Phase**: refactor-safe.

### Open/Closed (OCP)

- **Meaning**: New behavior arrives by extension — a new implementation, branch, or registration — not by rewriting the core path.
- **Signals**: The same type dispatch modified to add a variant across several commits; a new case requiring an edit to a core function.
- **When NOT to apply**: A closed set of a few variants is cheaper to edit than to abstract. An extension point with no second implementation violates YAGNI and KISS at once.
- **Phase**: design-time. Adding an extension point inside a refactor is new behavior — route it to `/improve-architecture`.

### Liskov Substitution (LSP)

- **Meaning**: A subtype or implementation replaces its base or interface without the caller knowing or breaking.
- **Signals**: An override that throws not-implemented; an override ignoring parameters its contract declares; strengthened preconditions or weakened postconditions; callers using type checks to special-case one subtype.
- **When NOT to apply**: Languages without inheritance have no LSP surface; marker interfaces carry no behavioral contract.
- **Phase**: refactor-safe. Changing a public inheritance contract is a scope change — route it to `/improve-architecture`.

### Interface Segregation (ISP)

- **Meaning**: Callers depend only on the methods they use.
- **Signals**: An interface method that is empty or throws in some implementers; a caller using one of many methods; test doubles stubbing methods they never exercise.
- **When NOT to apply**: Framework-mandated interfaces (ORM callbacks, DI lifecycle) cannot be split, and an interface whose every method has a caller needs no split.
- **Phase**: refactor-safe for internal interfaces; splitting a public interface starts with checking its callers.

### Dependency Inversion (DIP)

- **Meaning**: High-level logic depends on an abstraction instead of hardcoding a concrete implementation or an environment detail.
- **Signals**: A high-level module constructing or importing a concrete implementation; business logic testable only by stubbing a third-party SDK; configuration, clock, or filesystem details inside business functions.
- **When NOT to apply**: An abstraction with one implementation, no near-term second implementation, and no test-double need is YAGNI — wrapping a stdlib call "just in case" buys indirection and no caller benefit.
- **Phase**: refactor-safe when injecting a dependency that already exists; creating a new seam plus its callers is design-time.

### DRY (Don't Repeat Yourself)

- **Meaning**: One piece of knowledge, one authoritative home. Duplication means duplicated knowledge, not duplicated characters.
- **Signals**: A repeated block that has begun to diverge; the same validation rule, constant, or protocol format maintained in more than one file.
- **When NOT to apply**: Code that merely looks alike but will evolve separately — extracting it couples two independent change reasons ([#8](anti-patterns.md)). Duplication inside tests is usually cheaper than the wrong abstraction, and three similar lines need no shared function.
- **Phase**: refactor-safe.

### KISS (Keep It Simple)

- **Meaning**: The simplest structure that solves the actual problem — early returns, guard clauses, linear flow.
- **Signals**: Nesting that needs a comment to follow; boolean flag parameters that change what a function means; more layers than the requirement has concepts.
- **When NOT to apply**: A genuinely complex domain (tax rules, compliance, protocol state machines) is not simple, and flattening it hides complexity rather than removing it. That complexity belongs to the problem, not the code.
- **Phase**: refactor-safe.

### YAGNI (You Aren't Gonna Need It)

- **Meaning**: Build for the requirement in front of you. Unused code, speculative parameters, and reserved extension points are cost, not foresight.
- **Signals**: A zero-reference export, function, or class; a parameter never passed a non-default value; a config option never set; a flag never toggled; an abstraction with one implementation and no test-double need; a hook reserved for later.
- **When NOT to apply**: Public API and plugin contracts — external consumers are invisible to grep, so zero local references prove nothing. Framework registration points and language boilerplate are mandatory.
- **Phase**: refactor-safe for private or provably unused code; deleting public API is a scope change — report it to `/improve-architecture`.

### Law of Demeter (LoD)

- **Meaning**: Talk to your immediate collaborators; do not reach through an object into its internals.
- **Signals**: Call chains crossing ownership boundaries; a method touching several members of another object (feature envy); a caller that must know an internal structure to call correctly.
- **When NOT to apply**: Fluent APIs, builders, collection pipelines, and DSLs are chains by design — the chain *is* the interface. Depth alone means nothing until the chain crosses an ownership boundary.
- **Phase**: refactor-safe (introduce a delegating method — tell, don't ask).

### Composition over Inheritance

- **Meaning**: Express reuse through composition, delegation, or function composition rather than class hierarchy.
- **Signals**: Deep inheritance; a subclass overriding most of its parent's behavior; inheritance used to reuse a single method.
- **When NOT to apply**: Framework-mandated base classes cannot be composed away; languages without inheritance have no such surface.
- **Phase**: refactor-safe inside a hierarchy; replacing a public subclass API is a scope change — route it to `/improve-architecture`.

### Explicit over Implicit

- **Meaning**: Behavior, dependencies, and data flow are visible at the call site — no hidden side effects, magic values, or implicit coercions.
- **Signals**: Unnamed literals repeated through logic; implicit coercion relied on for correctness; a constructor or getter with side effects; positional booleans that change a function's meaning; variadic catch-alls swallowing the contract.
- **When NOT to apply**: Established language idioms (iteration protocols, truthiness checks) and framework conventions are explicit by convention; deviating from them is the less readable choice.
- **Phase**: refactor-safe for naming a constant or parameter; changing coercion semantics is a behavior change, not a refactor.

### Fail Fast

- **Meaning**: Errors surface early and close to their cause — validate at the boundary, fail loudly, make the message diagnostic.
- **Signals**: A boundary accepting input without validation while failure happens deep in the stack; empty `catch` blocks; sentinel returns instead of failure; messages without input or context.
- **When NOT to apply**: Unrecoverable or externally uncontrolled input that must degrade (network retries, tolerant user input) and batches that must continue past a bad item — there, continuing is the requirement.
- **Phase**: review and design-time. **Never in a refactor** — adding validation changes behavior.

### Immutability & Pure Functions First

- **Meaning**: Prefer fewer shared mutable states and side effects; where the language and project allow, compute with pure functions over immutable data.
- **Signals**: Module-level mutable state, singletons, or mutable default parameters; in-place mutation of a parameter; a function that returns a value and mutates the same object; time, randomness, or IO embedded in business logic.
- **When NOT to apply**: Performance-critical hot paths needing in-place mutation; languages without immutability support; frameworks requiring mutable models (ORM entities).
- **Phase**: refactor-safe, with one check — returning a copy instead of the same reference, or fixing a mutable default parameter, can change observable behavior, so confirm at the call sites.
