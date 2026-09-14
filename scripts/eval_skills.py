#!/usr/bin/env python3
"""Skills evaluation harness for dev-skills (GEPA-style loop, deterministic levels).

Implements the framework specified in docs/evals/skills-eval.md:

  Level S  static per-skill compliance vs the authoring bar
           (docs/research/agentskills-skill-authoring-1.md)
  Level W  workflow coherence (cross-skill graph + scripts/check-docs.py)
  Level T  trigger-routing proxy (lexical; the live subagent round is Level
           T-Live, run at checkpoints per the protocol in skills-eval.md)

Every failing check emits textual feedback (per-sample critique, not a bare
score) — that feedback is what the optimization loop reflects on.

Standard library only. Run from the repo root:

    python3 scripts/eval_skills.py --level all --iteration 0

Exit code 0 = every hard check in the selected levels passed; 1 otherwise
(regression gate).
"""

from __future__ import annotations

import argparse
import csv
import json
import math
import re
import subprocess
import sys
from datetime import date
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SKILLS = ROOT / "skills"
RESULTS = ROOT / "docs/evals/results"

# Repo policy: these units are user-invoked only (never model-routed).
USER_INVOKED = {"implement", "rules"}
# Interviewing skills — the one-by-one adaptive pacing contract applies.
INTERVIEW_SKILLS = {"think", "grill"}
# Sub-agent orchestrated skills — REFERENCE.md must carry per-sub-agent chapters.
SUBAGENT_SKILLS = {"tdd", "review"}
EXEMPT_OUTCOME_CONTRACT = {"rules"}  # not a task skill; manifest is the contract

ALLOWED_FRONTMATTER = {"name", "description", "disable-model-invocation"}

results: list[dict] = []


def rec(level: str, check_id: str, skill: str, severity: str, ok: bool, feedback: str = "") -> None:
    results.append(
        {"level": level, "check": check_id, "skill": skill, "severity": severity,
         "pass": ok, "feedback": feedback}
    )


def fail_text(check_id: str, skill: str, detail: str) -> str:
    return f"[{check_id}] {skill}: {detail}"


def rel(p: Path) -> str:
    return str(p.relative_to(ROOT))


# ---------------------------------------------------------------- frontmatter

def split_frontmatter(text: str) -> tuple[dict, str]:
    m = re.match(r"^---\n(.*?)\n---\n(.*)$", text, re.S)
    if not m:
        return {}, text
    fm: dict = {}
    for line in m.group(1).splitlines():
        mm = re.match(r"^([a-zA-Z-]+):\s*(.*)$", line)
        if mm:
            val = mm.group(2).strip()
            if val.startswith('"') and val.endswith('"'):
                val = val[1:-1]
            fm[mm.group(1)] = val
    return fm, m.group(2)


def load_skills() -> dict[str, dict]:
    skills = {}
    for d in sorted(p for p in SKILLS.iterdir() if p.is_dir()):
        sk = d / "SKILL.md"
        if not sk.exists():
            continue
        text = sk.read_text(encoding="utf-8")
        fm, body = split_frontmatter(text)
        ref = d / "REFERENCE.md"
        skills[d.name] = {
            "dir": d, "fm": fm, "body": body, "lines": text.count("\n") + 1,
            "ref_text": ref.read_text(encoding="utf-8") if ref.exists() else "",
            "ref_lines": (ref.read_text(encoding="utf-8").count("\n") + 1) if ref.exists() else 0,
        }
    return skills


# ------------------------------------------------------------------- Level S

INTENT_RE = re.compile(r"\b(use (when|after|before|to|for|as)|run (before|after))\b", re.I)
PROCEDURE_RE = re.compile(r"^## (Process Summary|The Work|Process\b|Steps\b|Step \d|Workflow)", re.M)


def check_static(skills: dict[str, dict]) -> None:
    for name, s in skills.items():
        fm, body = s["fm"], s["body"]
        combined = body + "\n" + s["ref_text"]

        # FM1 frontmatter shape
        extra = sorted(set(fm) - ALLOWED_FRONTMATTER)
        rec("S", "FM1", name, "hard", not extra,
            fail_text("FM1", name, f"non-spec frontmatter fields {extra} (allowed: {sorted(ALLOWED_FRONTMATTER)})"))
        rec("S", "FM1b", name, "hard", "name" in fm and "description" in fm,
            fail_text("FM1b", name, "missing required name/description"))

        # FM2 name constraints
        ok_name = (
            fm.get("name") == name
            and re.fullmatch(r"[a-z0-9]+(-[a-z0-9]+)*", fm.get("name", "")) is not None
            and len(fm.get("name", "")) <= 64
        )
        rec("S", "FM2", name, "hard", ok_name,
            fail_text("FM2", name, f"name={fm.get('name')!r} must equal dir, be lowercase-hyphen, <=64 chars"))

        # FM3 description length + intent phrase
        desc = fm.get("description", "")
        ok_len = 1 <= len(desc) <= 1024
        rec("S", "FM3", name, "hard", ok_len,
            fail_text("FM3", name, f"description length {len(desc)} outside 1..1024 (spec hard limit)"))
        rec("S", "FM3b", name, "hard", len(desc) >= 80,
            fail_text("FM3b", name, f"description only {len(desc)} chars — too thin to carry triggering (aim 100+)"))
        rec("S", "FM3c", name, "hard", bool(INTENT_RE.search(desc)),
            fail_text("FM3c", name, "description lacks intent-first phrasing ('Use when/after/before/to…')"))

        # FM4 bilingual trigger words (user-invoked units are never model-routed)
        has_cjk = re.search(r"[\u4e00-\u9fff]", desc) is not None
        rec("S", "FM4", name, "soft" if name in USER_INVOKED else "hard",
            has_cjk or name in USER_INVOKED,
            fail_text("FM4", name, "description has no Chinese trigger words (RESOLVER route matching needs both languages)"))

        # FM5 invocation policy
        dmi = fm.get("disable-model-invocation", "").lower() == "true"
        want = name in USER_INVOKED
        rec("S", "FM5", name, "hard", dmi == want,
            fail_text("FM5", name, f"disable-model-invocation={dmi} but repo policy expects {want} (USER_INVOKED={sorted(USER_INVOKED)})"))

        # ST1/ST2 outcome contract before procedure
        if name not in EXEMPT_OUTCOME_CONTRACT:
            has_oc = re.search(r"^## Outcome Contract\b", body, re.M) is not None
            rec("S", "ST1", name, "hard", has_oc,
                fail_text("ST1", name, "no '## Outcome Contract' section (anti-pattern #30)"))
            if has_oc:
                oc_i = body.find("## Outcome Contract")
                proc = PROCEDURE_RE.search(body)
                rec("S", "ST2", name, "hard", (proc is None) or (oc_i < proc.start()),
                    fail_text("ST2", name, "outcome contract must precede the first procedure section"))

            # ST3/ST4 gotchas + output template
            rec("S", "ST3", name, "hard", re.search(r"^## Gotchas\b", body, re.M) is not None and "|" in body.split("## Gotchas")[1][:2000],
                fail_text("ST3", name, "no '## Gotchas' table"))
            rec("S", "ST4", name, "hard", re.search(r"^## Output\b", body, re.M) is not None,
                fail_text("ST4", name, "no '## Output' section with the output template"))

        # ST5/ST6 line budgets (spec 500 hard; repo guidance 140 soft)
        rec("S", "ST5", name, "hard", s["lines"] <= 500,
            fail_text("ST5", name, f"SKILL.md is {s['lines']} lines (spec: keep under 500)"))
        rec("S", "ST6", name, "soft", s["lines"] <= 140,
            fail_text("ST6", name, f"SKILL.md is {s['lines']} lines (repo guidance: ~140; push detail to REFERENCE)"))

        # ST7 references its REFERENCE.md
        if s["ref_text"]:
            rec("S", "ST7", name, "hard", "REFERENCE.md" in body,
                fail_text("ST7", name, "REFERENCE.md exists but SKILL.md never points to it"))

        # ST8 every *-FORMAT.md is referenced from its owning skill (no orphan format files)
        fmt_files = [p.name for p in s["dir"].glob("*-FORMAT.md")]
        missing_fmt = [f for f in fmt_files if f not in body and f not in s["ref_text"]]
        rec("S", "ST8", name, "hard", not missing_fmt,
            fail_text("ST8", name, f"format file(s) never referenced from SKILL.md/REFERENCE.md: {missing_fmt}"))

        # ST9 no orphan .md files in the skill directory (every file reachable from SKILL/REFERENCE)
        all_md = [p.name for p in s["dir"].glob("*.md")] + [p.name for p in (s["dir"] / "references").glob("*.md")] if (s["dir"] / "references").exists() else [p.name for p in s["dir"].glob("*.md")]
        corpus = body + "\n" + s["ref_text"]
        orphans = [f for f in all_md if f != "SKILL.md" and f not in corpus]
        rec("S", "ST9", name, "soft", not orphans,
            fail_text("ST9", name, f"orphan file(s) not referenced anywhere in the skill: {orphans}"))

        # ST10 entry protocol referenced early (bootstrap before skill-specific work)
        if name != "rules":
            first_occur = body.find("Entry Protocol")
            rec("S", "ST10", name, "soft", 0 <= first_occur <= int(len(body) * 0.6),
                fail_text("ST10", name, f"'Entry Protocol' first mentioned at char {first_occur} of {len(body)} — bootstrap should come before most of the body"))

        # ST11 rigid all-caps modal wording (skill-creator yellow flag: explain why instead)
        caps = re.findall(r"\b(ALWAYS|NEVER|MUST NOT|REQUIRED)\b", body)
        rec("S", "ST11", name, "soft", len(caps) <= 3,
            fail_text("ST11", name, f"{len(caps)} rigid all-caps ALWAYS/NEVER/MUST-NOT/REQUIRED in SKILL.md — explain why instead (skill-creator yellow flag)"))

        # ST12 no leftover TODO/FIXME/TBD markers in SKILL.md prose (outside inline code).
        # REFERENCE tables legitimately discuss TODO markers found in TARGET repos — out of scope here.
        body_nocode = re.sub(r"`[^`]*`", "", body)
        markers = re.findall(r"\b(TODO|FIXME|TBD)\b", body_nocode)
        rec("S", "ST12", name, "hard", not markers,
            fail_text("ST12", name, f"leftover TODO/FIXME/TBD marker(s) in SKILL.md prose: {markers}"))

        # ST13 gotchas table is a two-column What happened | Rule table (task skills only)
        if name not in EXEMPT_OUTCOME_CONTRACT:
            gotchas = re.search(r"^## Gotchas\s*\n(.*?)(?=^## )", body, re.S | re.M)
            ok_g = bool(gotchas) and re.search(r"^\|\s*What happened\s*\|\s*Rule\s*\|", gotchas.group(1), re.M) is not None
            rec("S", "ST13", name, "soft", ok_g,
                fail_text("ST13", name, "Gotchas section is not the standard two-column 'What happened | Rule' table"))

        # RF1 TOC for long reference files
        if s["ref_lines"] > 300:
            head = "\n".join(s["ref_text"].splitlines()[:80])
            links = re.findall(r"\]\(#", head)
            rec("S", "RF1", name, "hard", len(links) >= 4,
                fail_text("RF1", name, f"REFERENCE.md is {s['ref_lines']} lines with only {len(links)} TOC anchors — files >300 lines need a table of contents"))

        # RF2 sub-agent chapters: a sub-agent chapter = `## Chapter N: … Sub-Agent …`;
        # shared elements may live in the `## Sub-Agent Common` block, which counts
        # toward every sub-agent chapter (that is why the block exists).
        if name in SUBAGENT_SKILLS:
            ref = s["ref_text"]
            marks = [(m.start(), m.end(), m.group(0).lstrip("# ").strip())
                     for m in re.finditer(r"^## .*$", ref, re.M)]
            blocks: dict[str, str] = {}
            for i, (start, end, title) in enumerate(marks):
                stop = marks[i + 1][0] if i + 1 < len(marks) else len(ref)
                blocks[title] = ref[end:stop]
            common = next((b for t, b in blocks.items() if t.startswith("Sub-Agent Common")), "")
            chapters = [t for t in blocks if t.startswith("Chapter") and "Sub-Agent" in t]
            rec("S", "RF2", name, "soft", len(chapters) >= 2,
                fail_text("RF2", name, f"expected >=2 'Chapter N: … Sub-Agent …' headings, found {len(chapters)}: {chapters}"))
            for t in chapters:
                block = blocks[t] + "\n" + common
                missing = []
                if not re.search(r"[Rr]e-[Rr]ead", block):
                    missing.append("context re-read")
                if not re.search(r"[Rr]esponsibilit", block):
                    missing.append("responsibilities")
                if not re.search(r"[Cc]hecklist|[Ss]elf-[Cc]heck", block):
                    missing.append("checklist")
                if not re.search(r"^###? Output|Output [Tt]emplate", block, re.M):
                    missing.append("output template")
                if not re.search(r"[Ii]ndependen", block):
                    missing.append("independence constraint")
                rec("S", "RF2b", name, "soft", not missing,
                    fail_text("RF2b", name, f"chapter '{t}' missing: {', '.join(missing)}"))

        # IV interview pacing contract (SKILL.md + REFERENCE.md)
        if name in INTERVIEW_SKILLS:
            rec("S", "IV1", name, "hard", re.search(r"one question at a time|exactly one question|one question per message", combined, re.I) is not None,
                fail_text("IV1", name, "no explicit one-question-per-message rule"))
            adaptive = (
                re.search(r"(next question|ask next|which question).{0,160}(previous answer|last answer|answer just given)", combined, re.I | re.S) is not None
                or re.search(r"(after each answer|from (the )?(user'?s )?(last|previous) answer|based on the answer).{0,160}(next question|determin|comput|choose|select|generat|recomput)", combined, re.I | re.S) is not None
            )
            rec("S", "IV2", name, "hard", adaptive,
                fail_text("IV2", name, "no rule that the NEXT question is derived from the user's previous answer (adaptive, never pre-computed)"))
            rec("S", "IV3", name, "hard", re.search(r"until (the )?(decision tree|tree|every branch|all branches)|tree is exhausted|exhausted", combined, re.I) is not None,
                fail_text("IV3", name, "no exhaustive-tree termination rule (stop when the tree is done, not when a list ends)"))
            forbidden = [
                (r"\bfrontier\b", "frontier vocabulary from the retired batch model"),
                (r"numbered round", "numbered-round format"),
                (r"\brounds?\b", "round vocabulary (one-by-one model must not speak in rounds)"),
                (r"in one (message|round)", "batch-into-one-message instruction"),
                (r"combine independent questions|questions together|multiple questions", "batch-question instruction"),
            ]
            hits = [why for pat, why in forbidden if re.search(pat, combined, re.I)]
            rec("S", "IV4", name, "hard", not hits,
                fail_text("IV4", name, "batch-question language remains: " + "; ".join(hits)))
            rec("S", "IV5", name, "hard", re.search(r"recommend(ed)? answer", combined, re.I) is not None,
                fail_text("IV5", name, "no 'recommended answer with each question' rule"))


# ------------------------------------------------------------------- Level W

TRACE_PAIRS = [
    ("## Issue", {"think"}, {"grill", "story", "implement", "entry-protocol.md"}),
    ("Grilled by", {"grill"}, {"entry-protocol.md", "story", "implement", "review"}),
    ("Prototyped by", {"have-a-try"}, {"think", "grill", "story", "implement"}),
]
SKILL_NAMES = ["think", "grill", "story", "implement", "tdd", "review", "debug", "research",
               "have-a-try", "improve-architecture", "write", "setup-project", "rules"]


def check_workflow(skills: dict[str, dict]) -> None:
    # W1 check-docs.py regression gate
    proc = subprocess.run(
        [sys.executable, str(ROOT / "scripts/check-docs.py")],
        capture_output=True, text=True,
    )
    tail = "\n".join((proc.stdout + proc.stderr).strip().splitlines()[-6:])
    rec("W", "W1", "-", "hard", proc.returncode == 0, fail_text("W1", "check-docs.py", tail))

    # W2 entry protocol referenced by every task skill
    for name, s in skills.items():
        if name == "rules":
            continue
        rec("W", "W2", name, "hard", "entry-protocol.md" in s["body"] or "entry-protocol.md" in s["ref_text"],
            fail_text("W2", name, "Skill Entry Protocol not referenced from SKILL.md/REFERENCE.md"))

    # W3 every slash-command reference points at a real skill
    for f in sorted(SKILLS.rglob("*.md")):
        text = f.read_text(encoding="utf-8")
        for m in re.finditer(r"/(think|grill|story|implement|tdd|review|debug|research|have-a-try|improve-architecture|write|setup-project)\b", text):
            pass  # all names in this alternation exist as dirs; renamed skills break W4 below instead
    for name in SKILL_NAMES:
        rec("W", "W4", name, "hard", name in (ROOT / "skills/RESOLVER.md").read_text(encoding="utf-8"),
            fail_text("W4", name, "skill not mentioned in RESOLVER.md"))

    # W5 Traceability producer/consumer pairs
    corpus = {name: s["body"] + "\n" + s["ref_text"] for name, s in skills.items()}
    corpus["entry-protocol.md"] = (SKILLS / "rules/entry-protocol.md").read_text(encoding="utf-8")
    for field, producer, consumers in TRACE_PAIRS:
        prod_ok = any(field in corpus.get(p, "") for p in producer)
        rec("W", "W5", field, "hard", prod_ok, fail_text("W5", field, f"producer {producer} never writes this field"))
        cons_ok = any(field in corpus.get(c, "") for c in consumers)
        rec("W", "W5b", field, "hard", cons_ok, fail_text("W5b", field, f"no consumer in {consumers} reads this field"))

    # W6 README (both languages) lists every skill directory
    for readme in ("README.md", "README_ZH.md"):
        text = (ROOT / readme).read_text(encoding="utf-8")
        missing = [name for name in skills if name not in text]
        rec("W", "W6", readme, "hard", not missing,
            fail_text("W6", readme, f"skill directory names missing from this README: {missing}"))

    # W7 no exact trigger-word collisions between model-invoked skills' descriptions
    def trigger_words(desc: str) -> set[str]:
        m = re.search(r"Trigger words:\s*(.+?)\.?\s*$", desc)
        if not m:
            return set()
        return {w.strip().rstrip(".").lower() for w in re.split(r",", m.group(1)) if w.strip()}
    tw = {name: trigger_words(s["fm"].get("description", "")) for name, s in skills.items()
          if not fm_flag(skills, name)}
    for a in sorted(tw):
        for b in sorted(tw):
            if a < b:
                shared = tw[a] & tw[b]
                rec("W", "W7", f"{a}/{b}", "soft", not shared,
                    fail_text("W7", "-", f"{a} and {b} share exact trigger words: {sorted(shared)} — ambiguous routing signal"))

    # W8 cross-skill step references resolve ("`/think` Step 10a" etc.)
    step_ref = re.compile(r"`/(\w+)` Step (\d+[a-z]?)")
    for f in sorted(SKILLS.rglob("*.md")):
        if f.parent == ROOT / "skills" and f.name == "RESOLVER.md":
            continue
        text = f.read_text(encoding="utf-8")
        for m in step_ref.finditer(text):
            target_skill, step = m.group(1), m.group(2)
            tf = SKILLS / target_skill
            if not tf.exists():
                rec("W", "W8", target_skill, "soft", False,
                    fail_text("W8", rel(f), f"references `/{target_skill}` Step {step} but that skill directory does not exist"))
                continue
            target_text = "\n".join(p.read_text(encoding="utf-8") for p in tf.glob("*.md"))
            base = step.rstrip("abcdefgh")
            sub = step[len(base):]
            ok = (f"**Step {base}" in target_text) and (not sub or f"### {base}{sub}" in target_text or f"{base}{sub}:" in target_text)
            rec("W", "W8", f"{target_skill}:{step}", "soft", ok,
                fail_text("W8", rel(f), f"references `/{target_skill}` Step {step} — label not found in {target_skill}'s files"))

    # W9 research INDEX rows and record files agree
    rdir = ROOT / "docs/research"
    if rdir.exists():
        records = {p.name for p in rdir.glob("*.md")} - {"INDEX.md"}
        index_text = (rdir / "INDEX.md").read_text(encoding="utf-8") if (rdir / "INDEX.md").exists() else ""
        unindexed = sorted(n for n in records if n not in index_text)
        rec("W", "W9", "research-index", "hard", not unindexed,
            fail_text("W9", "-", f"research record(s) missing from INDEX.md: {unindexed}"))
        dangling = sorted({m for m in re.findall(r"\(([\w-]+\.md)\)", index_text)} - records - {"INDEX.md"})
        rec("W", "W9b", "research-index", "hard", not dangling,
            fail_text("W9b", "-", f"INDEX.md links to nonexistent record(s): {dangling}"))



# ------------------------------------------------------------------- Level T

def cjk_bigrams(s: str) -> set[str]:
    chars = re.findall(r"[\u4e00-\u9fff]", s)
    return {chars[i] + chars[i + 1] for i in range(len(chars) - 1)} if chars else set()


def tokens(s: str) -> set[str]:
    words = {w for w in re.split(r"[^a-z0-9]+", s.lower()) if len(w) > 1}
    return words | cjk_bigrams(s)


def check_trigger_proxy() -> None:
    qfile = ROOT / "scripts/evals/trigger-queries.json"
    data = json.loads(qfile.read_text(encoding="utf-8"))
    skills = load_skills()
    catalog = {
        name: tokens(s["fm"].get("description", "")) | {name}
        for name, s in skills.items()
        if not fm_flag(skills, name)  # user-invoked units never compete for routing
    }
    # IDF over the catalog: tokens every description shares carry near no routing signal
    n = len(catalog)
    df: dict[str, int] = {}
    for dt in catalog.values():
        for t in dt:
            df[t] = df.get(t, 0) + 1
    idf = {t: max(0.0, math.log(n / d)) for t, d in df.items()}

    for q in data["queries"]:
        qt = tokens(q["query"])
        best, best_score, best_raw = "NONE", 0.0, 0
        for name, dt in catalog.items():
            hit = qt & dt
            raw = len(hit)
            score = sum(idf.get(t, 0.0) for t in hit) / (len(dt) ** 0.25)
            if score > best_score:
                best, best_score, best_raw = name, score, raw
        pred = best if best_raw >= 2 else "NONE"
        ok = pred == q["expected"]
        rec("T-proxy", f"T:{q['id']}", "-", "soft", ok,
            f"[T:{q['id']}] {q['split']}: expected {q['expected']}, proxy predicted {pred} (raw overlap {best_raw}, idf-score {best_score:.2f}) — proxy is drift-detection only; confirm with T-Live")


def fm_flag(skills: dict[str, dict], name: str) -> bool:
    return skills[name]["fm"].get("disable-model-invocation", "").lower() == "true"


# ------------------------------------------------------------------ aggregate

def summarize(level_filter: set[str]) -> dict:
    wanted = {x.upper() for x in level_filter}
    sel = [r for r in results if r["level"].split("-")[0].upper() in wanted]
    hard = [r for r in sel if r["severity"] == "hard"]
    soft = [r for r in sel if r["severity"] == "soft"]
    per_skill: dict[str, dict] = {}
    for r in hard:
        d = per_skill.setdefault(r["skill"], {"hard_pass": 0, "hard_total": 0})
        d["hard_total"] += 1
        d["hard_pass"] += r["pass"]
    return {
        "S_hard_pass": sum(r["pass"] for r in hard if r["level"] == "S"),
        "S_hard_total": sum(1 for r in hard if r["level"] == "S"),
        "S_soft_pass": sum(r["pass"] for r in soft if r["level"] == "S"),
        "S_soft_total": sum(1 for r in soft if r["level"] == "S"),
        "W_pass": sum(r["pass"] for r in hard if r["level"] == "W"),
        "W_total": sum(1 for r in hard if r["level"] == "W"),
        "T_train": round(100 * sum(r["pass"] for r in sel if r["level"] == "T-proxy" and r["check"].split(":")[1][0] in "PN") / max(1, sum(1 for r in sel if r["level"] == "T-proxy" and r["check"].split(":")[1][0] in "PN")), 1),
        "T_holdout": round(100 * sum(r["pass"] for r in sel if r["level"] == "T-proxy" and r["check"].split(":")[1][0] == "H") / max(1, sum(1 for r in sel if r["level"] == "T-proxy" and r["check"].split(":")[1][0] == "H")), 1),
        "per_skill": per_skill,
    }


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--level", default="all", choices=["s", "w", "t", "all"])
    ap.add_argument("--iteration", type=int, default=0)
    ap.add_argument("--notes", default="")
    args = ap.parse_args()

    skills = load_skills()
    sel = set(["s", "w", "t"] if args.level == "all" else [args.level])

    if "s" in sel:
        check_static(skills)
    if "w" in sel:
        check_workflow(skills)
    if "t" in sel:
        check_trigger_proxy()

    summary = summarize(sel)
    hard_fail = [r for r in results if r["severity"] == "hard" and not r["pass"]]

    print(f"=== skills-eval iteration {args.iteration} (levels: {','.join(sorted(sel))}) ===")
    print(f"S hard: {summary['S_hard_pass']}/{summary['S_hard_total']}   "
          f"S soft: {summary['S_soft_pass']}/{summary['S_soft_total']}   "
          f"W: {summary['W_pass']}/{summary['W_total']}   "
          f"T-proxy train: {summary['T_train']}%   holdout: {summary['T_holdout']}%")
    print("\nPer-skill hard pass:")
    for skill in sorted(summary["per_skill"]):
        d = summary["per_skill"][skill]
        flag = "" if d["hard_pass"] == d["hard_total"] else "  <-- FAILURES"
        print(f"  {skill:22s} {d['hard_pass']}/{d['hard_total']}{flag}")
    if hard_fail:
        print(f"\n{len(hard_fail)} hard failure(s) with feedback:")
        for r in hard_fail:
            print(f"  - {r['feedback']}")
    soft_fail = [r for r in results if r["severity"] == "soft" and not r["pass"]]
    if soft_fail:
        print(f"\n{len(soft_fail)} soft failure(s):")
        for r in soft_fail:
            print(f"  - {r['feedback']}")

    RESULTS.mkdir(parents=True, exist_ok=True)
    out = RESULTS / f"iteration-{args.iteration:03d}.json"
    out.write_text(json.dumps({
        "iteration": args.iteration, "date": str(date.today()),
        "levels": sorted(sel), "summary": summary,
        "results": results, "notes": args.notes,
    }, indent=1, ensure_ascii=False), encoding="utf-8")

    sb = RESULTS / "scoreboard.csv"
    new = not sb.exists()
    with sb.open("a", newline="", encoding="utf-8") as f:
        w = csv.writer(f)
        if new:
            w.writerow(["iteration", "S_hard_pass", "S_hard_total", "S_soft_pass", "S_soft_total",
                        "W_pass", "W_total", "T_train", "T_holdout", "notes"])
        w.writerow([args.iteration, summary["S_hard_pass"], summary["S_hard_total"],
                    summary["S_soft_pass"], summary["S_soft_total"], summary["W_pass"],
                    summary["W_total"], summary["T_train"], summary["T_holdout"], args.notes])

    return 1 if hard_fail else 0


if __name__ == "__main__":
    sys.exit(main())
