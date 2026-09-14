#!/usr/bin/env python3
"""Documentation integrity checks for dev-skills.

The product of this repo is Markdown, so the failure mode is not a broken build
— it is silent drift between documents (a rule renamed in one file, a shared
definition restated in another, a tree that no longer matches disk). This script
turns the cheapest of those invariants into a command.

Standard library only. Run from the repo root:

    python3 scripts/check-docs.py

Exit code 0 = every check passed; 1 = at least one failed.

What it does NOT do: judge content. It cannot tell whether a principle's
counter-indication is wise, whether a threshold is right, or whether a finding
names a real consequence. Those stay human review.
"""

from __future__ import annotations

import os
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
CATALOG = ROOT / "skills/rules/engineering-principles.md"
ANTI_PATTERNS = ROOT / "skills/rules/anti-patterns.md"
SCAN_TABLE = ROOT / "skills/improve-architecture/REFERENCE.md"
AGENTS = ROOT / "AGENTS.md"

# Illustrative paths in *-FORMAT.md examples. These name files a *target* repo
# would have, so they intentionally do not exist here.
ILLUSTRATIVE = re.compile(
    r"(<[a-z-]+>|react-concurrent-rendering-18\.md|react-suspense-data-fetching-18\.md"
    r"|postgres-index-strategy-15\.md)"
)

failures: list[str] = []
notes: list[str] = []


def check(name: str, ok: bool, detail: str = "") -> None:
    if ok:
        print(f"  PASS  {name}")
    else:
        print(f"  FAIL  {name}" + (f"\n        {detail}" if detail else ""))
        failures.append(name)


def md_files() -> list[Path]:
    return sorted(p for p in ROOT.rglob("*.md") if ".git" not in p.parts)


def rel(p: Path) -> str:
    return str(p.relative_to(ROOT))


# ---------------------------------------------------------------- link integrity
def check_links() -> None:
    print("links: every relative markdown link resolves")
    broken: list[str] = []
    for f in md_files():
        for m in re.finditer(r"\]\(([^)\s]+\.md)\)", f.read_text(encoding="utf-8")):
            target = m.group(1)
            if target.startswith(("http://", "https://", "mailto:")):
                continue
            if ILLUSTRATIVE.search(target):
                continue
            if not (f.parent / target).exists():
                broken.append(f"{rel(f)} -> {target}")
    check("all relative links resolve", not broken, "\n        ".join(broken))


# ------------------------------------------------------------- catalog structure
def catalog_entries() -> dict[str, str]:
    text = CATALOG.read_text(encoding="utf-8")
    parts = re.split(r"^### ", text, flags=re.M)[1:]
    return {p.splitlines()[0].strip(): p for p in parts}


def principle_key(heading: str) -> str:
    """Reduce a catalog heading to the token the ownership map names it by.

    Handles all three heading shapes: `DRY (Don't Repeat Yourself)`, `Law of
    Demeter (LoD)`, and bare `Composition over Inheritance`.
    """
    head = heading.strip()
    m = re.match(r"([A-Z]{2,6})\b", head)
    if m:
        return m.group(1)
    m = re.search(r"\(([A-Za-z]{2,6})\)", head)
    if m:
        return m.group(1)
    return head.split(" & ")[0].split(" over ")[0].strip()


def check_catalog() -> None:
    print("catalog: structure and field completeness")
    entries = catalog_entries()
    check("13 principle entries", len(entries) == 13, f"found {len(entries)}")
    for field in ("Meaning", "Signals", "When NOT to apply", "Phase"):
        missing = [h for h, body in entries.items() if not re.search(rf"- \*\*{re.escape(field)}\*\*", body)]
        check(f"every entry has {field}", not missing, ", ".join(missing))

    print("catalog: owns the definitions, not the thresholds")
    numbers = re.findall(r"≥?\s*\d+\s*%|>\s*\d+\s*(?:lines|methods)|≥\s*\d+\s*(?:levels|sites|members)", CATALOG.read_text(encoding="utf-8"))
    check("no numeric thresholds in the catalog", not numbers, f"found {numbers} — thresholds live in improve-architecture/REFERENCE.md §3.2")


# --------------------------------------------------------------- catalog ownership
def check_ownership() -> None:
    print("ownership: the two /review perspectives cover every principle")
    text = CATALOG.read_text(encoding="utf-8")
    code = re.search(r"Code Review Sub-Agent[^|]*\|(.+?)\|", text)
    impact = re.search(r"Impact Review Sub-Agent[^|]*\|(.+?)\|", text)
    if not (code and impact):
        check("ownership map rows found", False, "could not parse the Consumer & Ownership Map")
        return
    owned = code.group(1) + " " + impact.group(1)
    unowned = [principle_key(h) for h in catalog_entries() if principle_key(h) not in owned]
    check("all 13 principles have an owner", not unowned, "unowned: " + ", ".join(unowned))


# ------------------------------------------------------------- single-source rule
def check_single_source() -> None:
    print("anti-pattern #38: definitions are not restated outside their home")
    offenders = [
        rel(f)
        for f in md_files()
        if f != CATALOG and "**Meaning**" in f.read_text(encoding="utf-8")
    ]
    check("principle definitions live only in the catalog", not offenders, ", ".join(offenders))


# --------------------------------------------------------- anti-pattern invariants
def anti_pattern_tables() -> tuple[set[int], set[int]]:
    text = ANTI_PATTERNS.read_text(encoding="utf-8")
    main = text.split("## Usage")[0]
    archive = text.split("## Archive")[1].split("## Numbering history")[0]
    num = r"^\|\s*(\d+)\s*\|"
    return (
        {int(n) for n in re.findall(num, main, re.M)},
        {int(n) for n in re.findall(num, archive, re.M)},
    )


def cited_rule_numbers(body: str) -> set[int]:
    """Collect anti-pattern numbers cited in any of the repo's citation shapes.

    Seen in practice: `anti-patterns.md #8`, `[#8](anti-patterns.md)`,
    `(anti-patterns #34, #35)`, `(anti-pattern #3 and #4)`, `(anti-pattern #21)`.
    """
    found: set[int] = set()
    for m in re.finditer(r"anti-patterns?(?:\.md)?\s*#(\d+)", body):
        found.add(int(m.group(1)))
        tail = body[m.end():]
        while True:
            nxt = re.match(r"\s*(?:,|and|/)\s*#(\d+)", tail)
            if not nxt:
                break
            found.add(int(nxt.group(1)))
            tail = tail[nxt.end():]
    found |= {int(n) for n in re.findall(r"\[#(\d+)\]\([^)]*anti-patterns", body)}
    return found


def check_anti_patterns() -> None:
    print("anti-patterns: consumer rule and archive invariants")
    main, archive = anti_pattern_tables()
    cited: set[int] = set()
    for f in md_files():
        if f == ANTI_PATTERNS:
            continue
        cited |= cited_rule_numbers(f.read_text(encoding="utf-8"))
    uncited = sorted(main - cited)
    archived_cited = sorted(archive & cited)
    check("every main-table rule has a citing consumer", not uncited, f"uncited: {uncited}")
    check("no archived rule is cited", not archived_cited, f"archived but cited: {archived_cited}")


# ------------------------------------------------------------------- tree syncing
def check_tree() -> None:
    print("AGENTS.md: repository tree matches disk")
    block = re.search(r"^skills/\n(.*?)^```", AGENTS.read_text(encoding="utf-8"), re.M | re.S)
    if not block:
        check("repository tree found in AGENTS.md", False)
        return
    tree = block.group(1)
    on_disk = sorted(d for d in os.listdir(ROOT / "skills") if (ROOT / "skills" / d).is_dir() and d != "rules")
    missing_dirs = [d for d in on_disk if not re.search(rf"── {re.escape(d)}/", tree)]
    check("every skill directory appears in the tree", not missing_dirs, ", ".join(missing_dirs))
    rules = sorted(p.name for p in (ROOT / "skills/rules").glob("*.md"))
    missing_rules = [r for r in rules if r not in tree]
    check("every rules/ file appears in the tree", not missing_rules, ", ".join(missing_rules))


# ------------------------------------------------------------------ scan-table tags
def check_scan_tags() -> None:
    print("improve-architecture §3.2: principle tags point at real catalog entries")
    known = {principle_key(h) for h in catalog_entries()}
    known |= {"Composition", "Explicit", "Fail Fast", "Immutability", "Deep modules", "LoD"}
    text = SCAN_TABLE.read_text(encoding="utf-8")
    table = re.search(r"### 3\.2 Design Debt Signals(.*?)\n\n", text, re.S)
    if not table:
        check("§3.2 table found", False)
        return
    tags = re.findall(r"^\|\s*([^|]+?)\s*\|", table.group(1), re.M)[1:]  # drop header row
    unknown = [
        t for t in tags
        if not t.startswith("—")
        and not all(part.strip() in known for part in t.split("/"))
    ]
    check("every tag is a catalog principle or an explicit exemption", not unknown, ", ".join(unknown))


def check_shipped_links() -> None:
    print("shipped content does not link outside the shipped tree")
    escaping: list[str] = []
    for f in sorted((ROOT / "skills").rglob("*.md")):
        for m in re.finditer(r"\]\(([^)\s]+\.md)\)", f.read_text(encoding="utf-8")):
            target = m.group(1)
            if target.startswith(("http://", "https://", "mailto:")):
                continue
            resolved = os.path.normpath(os.path.join(rel(f.parent), target))
            if not (resolved == "skills" or resolved.startswith("skills" + os.sep)):
                escaping.append(f"{rel(f)} -> {target}")
    check(
        "no link escapes skills/ (installed copies hold only these units)",
        not escaping,
        "\n        ".join(escaping),
    )


def check_rules_bundle() -> None:
    print("rules/: the shared bundle is shippable and completely indexed")
    manifest = ROOT / "skills/rules/SKILL.md"
    if not manifest.exists():
        check(
            "rules/ carries a SKILL.md manifest",
            False,
            "without it the installer never ships the bundle and every ../rules/* link breaks after install"
            " (docs/audits/2026-09-14-shared-rules-not-installed.md)",
        )
        return
    check("rules/ carries a SKILL.md manifest", True)
    body = manifest.read_text(encoding="utf-8")
    check(
        "the manifest is not model-invocable",
        "disable-model-invocation: true" in body,
        "the bundle must never compete for routing",
    )
    unindexed = [p.name for p in (ROOT / "skills/rules").glob("*.md") if p.name != "SKILL.md" and p.name not in body]
    check("every rules/ file is listed in the manifest", not unindexed, "unlisted: " + ", ".join(unindexed))


def check_tdd_phase_pointer() -> None:
    print("tdd: the Refactor phase reads the Phase field instead of a copied list")
    tdd = (ROOT / "skills/tdd/REFERENCE.md").read_text(encoding="utf-8")
    check(
        "refactor scope points at the catalog's Phase field",
        'Phase is `refactor-safe`' in tdd,
        "tdd/REFERENCE.md no longer tells the agent where the refactor-safe set is defined",
    )
    hand_list = re.search(r"refactor-safe subset is\b", tdd)
    check(
        "no hand-copied principle list in tdd",
        not hand_list,
        "a hand-copied list drifts from the catalog's Phase fields; link instead",
    )


def main() -> int:
    for check_fn in (
        check_links,
        check_catalog,
        check_ownership,
        check_single_source,
        check_anti_patterns,
        check_tree,
        check_scan_tags,
        check_shipped_links,
        check_rules_bundle,
        check_tdd_phase_pointer,
    ):
        check_fn()
    print()
    if failures:
        print(f"{len(failures)} check(s) failed: {', '.join(failures)}")
        return 1
    print("All documentation checks passed.")
    for note in notes:
        print(f"note: {note}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
