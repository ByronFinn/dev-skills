# agent-interviewing: Question Pacing (One-at-a-Time Adaptive Interviewing)

> **Stack**: agent-interviewing@unknown (practice domain, not a software stack — see Boundary Conditions)  | **Major**: 1  | **Verified**: 2026-09-14  | **Status**: verified

## TL;DR

For skill-driven requirements interviews (think/grill-style), ask **exactly one question per message, with a recommended answer, and generate the next question from the user's last answer** until the decision tree is exhausted — supported by elicitation research (conversational adaptive interviewing outperforms standardized batch scripts on accuracy; ~half of well-generated interviewer questions are context-dependent) and by convergent community practice (interview-me, grill-me, omc-plan, loop-me). Honest boundary: **official vendor docs are silent on pacing** and even endorse small batches (1–4) for one-shot clarification — so strict one-by-one is a product decision for dev-skills, adopted by owner mandate 2026-09-14, not an externally mandated rule.

## Question

Should skill-driven interviewing in dev-skills (/think, /grill) ask questions one at a time with each next question derived from the previous answer, rather than pre-computed batches — and what evidence supports that choice?

## Approach

Searched official vendor docs (Anthropic Constitution, Claude Code best-practices + Agent SDK user-input, OpenAI GPT-5.2 prompting guide, Google Gemini prompting strategies, Microsoft Bot Framework UX, IBM watsonx Assistant), the agentskills.io spec, and the requirements-engineering literature (LLMREI arXiv 2507.02564, follow-up generation arXiv 2507.02858, interviews-vs-surveys arXiv 2505.23684, preference-elicitation clarifying questions arXiv 2510.12015, Schober & Conrad 1997 POQ peer-reviewed), plus community skill implementations (Addy Osmani interview-me, grill-me write-up, omc-plan, mattpocock loop-me). Mapped each pacing claim to its source tier.

## Findings

| Claim | Support | Tier |
|---|---|---|
| Ask clarifying questions on genuine ambiguity instead of guessing | Anthropic Constitution; Claude Code SDK; OpenAI; IBM | Official |
| Over-questioning is a defect; bound the count | Constitution ("more than necessary" objectionable); OpenAI "1–3 precise clarifying questions"; Google "prefer acting over asking"; Microsoft "minimal back and forth" | Official |
| Small batches officially acceptable for one-shot clarification | AskUserQuestion supports 1–4 questions/call; OpenAI endorses 1–3 | Official |
| "Interview me" as a requirements pattern | Claude Code best-practices ("For larger features, have Claude interview you first… Keep interviewing until we've covered everything") | Official |
| Strict one-question-at-a-time (with "unless closely related" exception) | LLMREI — added after early versions **overwhelmed users**; raters judged bot communication better than human interviewers' | Preprint |
| ~50% of good interview questions depend on previous responses | LLMREI measurement (context-deepening 44.4%/32.3% + context-enhancing 15.3%/10.4% + parameterized 12.8%/28.9% vs context-independent ~27%) | Preprint |
| Follow-ups conditioned on the interviewee's last utterance match or beat human-authored questions | Shen/Singhal/Breaux RE 2025 | Preprint (accepted) |
| Conversational (adaptive) interviewing beats strictly standardized scripts on accuracy for hard questions | Schober & Conrad 1997, Public Opinion Quarterly, ~523 citations | Peer-reviewed |
| Interviews = most needs per participant-time; surveys = more total coverage with redundancy; hybrid recommended | Obaidi et al. RE 2025 (18 interviews vs 188-participant survey) | Preprint (accepted) |
| Sequential funnel questioning broad-to-specific trainable in LLMs | Montazeralghaem et al. 2025 | Preprint |
| One-question-per-message in agent skills | interview-me ("spend it one question at a time", stop at ~95% confidence); grill-me ("include your recommended answer. Ask one question at a time"); omc-plan ("never batch multiple questions"); loop-me | Community |

Explicit absences: no official vendor document prescribes one-at-a-time pacing; no controlled study directly compares one-at-a-time vs batched multi-question chat messages on measured outcomes (overwhelm is motivated, not measured, beyond LLMREI's design change); decision-tree interviewing has no canonical authoritative source.

## Verdict & Rationale

Adopt strict one-by-one adaptive questioning for dev-skills' interviewing skills: one question per message, each with a recommended answer; the next question is computed from the decision tree state after the previous answer (never pre-computed as a batch); stop when the tree is exhausted, not when a list runs out. Rationale: adaptive conversational interviewing is the only pacing with empirical accuracy evidence (Schober & Conrad, peer-reviewed; LLMREI/shen et al. for LLM interviewers specifically), it is the convergent community practice for exactly this skill genre, and it is the repo owner's explicit product decision. Cost accepted: more turns per session (Microsoft's "minimal back and forth" concern) — mitigated by recommended answers (one-key replies) and by never asking what code/research can answer. Non-interview contexts (single collision confirmations, gate approvals) are not interviews and may still ask their single question inline.

## Boundary Conditions

This record grades a **practice domain**, not a software stack: "major 1" is a placeholder for "first settled version of this practice in this repo" (format's leaf-unit rule honored in spirit). The one-by-one rule applies to decision-tree interviews (/think converge loop, /grill interrogation); it deliberately does not apply to (a) scripts, which must stay non-interactive, nor (b) one-shot bounded clarification in non-interview skills, where official guidance permits 1–3. Official-vendor silence means a future vendor pacing standard would supersede the community tier here. Sensitive to the owner's product decisions first and foremost.

## Sources

**Tier 1 (maintainer-authored, required)**
- [Anthropic: Claude Code best practices](https://code.claude.com/docs/en/best-practices) — "have Claude interview you first", "Keep interviewing until we've covered everything" (pattern endorsement, no pacing rule)
- [Anthropic: Claude Code Agent SDK — user input](https://code.claude.com/docs/en/agent-sdk/user-input) — AskUserQuestion semantics, 1–4 questions/call
- [Anthropic: Claude's Constitution](https://www.anthropic.com/constitution) — clarification on genuine ambiguity; over-questioning flagged as defect
- [OpenAI: GPT-5.2 prompting guide](https://developers.openai.com/cookbook/examples/gpt-5/gpt-5-2_prompting_guide) — "Ask up to 1–3 precise clarifying questions"; users dislike too many questions
- [agentskills.io: Agent Skills Specification](https://agentskills.io/specification) — verified silent on question pacing (absence as evidence)

**Tier 2 (supplementary only, never sole evidence)**
- [Schober & Conrad 1997, Public Opinion Quarterly 61(4)](https://academic.oup.com/poq/article/61/4/576/1913600) — peer-reviewed: conversational interviewing reduces measurement error vs standardized scripts
- [LLMREI: Automating Requirements Elicitation Interviews with LLMs (arXiv 2507.02564)](https://arxiv.org/abs/2507.02564) — one-at-a-time as overwhelm fix; ~50% context-dependent questions; 60.94% requirements fully elicited
- [Shen, Singhal, Breaux (RE 2025, arXiv 2507.02858)](https://arxiv.org/abs/2507.02858) — last-utterance-conditioned follow-ups rated no worse than human-authored
- [Obaidi et al. (RE 2025, arXiv 2505.23684)](https://arxiv.org/abs/2505.23684) — interviews vs surveys efficiency/coverage trade-off
- [Addy Osmani: interview-me SKILL.md](https://github.com/addyosmani/agent-skills/blob/main/skills/interview-me/SKILL.md) — community one-question-at-a-time with confidence stopping
- [grill-me write-up](https://azukiazusa.dev/en/blog/before-implementation-interview-design-requirements-grill-me) — one question at a time + recommended answers
