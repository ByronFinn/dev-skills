# Sub-Agent Runtime Semantics

Shared rule for all sub-agent orchestrated skills (`tdd`, `review`). Stated once here; skills link to it instead of restating (anti-pattern #38).

## The Rule

"Sub-agent" is a **logical concept, not a runtime scheduler concept**. dev-skills is Markdown only — there is no scheduler. Concretely:

- **Independence comes from the re-read-from-disk discipline** (anti-patterns #34, #35), not from concurrent execution. Each sub-agent phase begins by re-reading all shared context from disk before acting.
- **If the host runtime supports true parallel sub-agent dispatch**, dispatch phases in parallel — it strengthens the guarantee.
- **If not** (single-context execution), execute phases sequentially — the independence guarantee holds as far as the re-read discipline is followed faithfully.

Full decision record: [ADR-0001 Implementation Note](../../docs/adr/0001-sub-agent-orchestration-pattern.md).

## Reference

Skills link to this file as:

```
See [Sub-Agent Runtime Semantics](../rules/sub-agent-runtime.md) — independence comes from re-reading shared context from disk, not from execution timing.
```
