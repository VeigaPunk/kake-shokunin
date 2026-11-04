#!/usr/bin/env python3
"""Round-84 C1 counter: the round-83 routed-defect queue closes (kake).

Reads one measured tree (a worktree, or an exported revision) and decides the
four items frozen in `.ufo/waves/round-84/contract.md` §C1. Every item is a
state conjunct re-derived from a non-lesson file plus a row conjunct only
prose can carry; a missing or unreadable file reopens the item.

Usage:
  c84_defect_queue.py --root <tree> [--revision <rev>]
  c84_defect_queue.py --selftest [--work <dir>]

Exit: 0 printed and met, 1 printed and not met, 2 unevaluable input,
64 usage. Offline: it reads files and (in --revision mode) runs `git show`.
"""
from __future__ import annotations

import argparse
import json
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

LESSON = "corpus/lessons/round-84.md"
RFC = ".ufo/waves/round-83/w1/ScoutSources/rfc9111.txt"
SPEC = ".ufo/waves/round-84/w1-spec.json"
RESULTS = ".ufo/waves/round-84/w1-results.json"
CENSUS = ".ufo/waves/round-84/controls/census-before.txt"
SOURCES = "corpus/SOURCES.md"

HEADINGS = ("5.2.  Cache-Control", "5.2.1.  Request Directives",
            "5.2.2.  Response Directives", "5.2.3.  Extension Directives")
D2_RE = re.compile(r"D2 count=(\d+) span=838-844 measure=words-full-span")


class Tree:
    """One measured lane tree: a worktree directory or a git revision."""

    def __init__(self, root: Path, revision: str | None) -> None:
        self.root = root
        self.revision = revision

    def read(self, relative: str) -> str | None:
        if self.revision:
            proc = subprocess.run(
                ["git", "-C", str(self.root), "show", f"{self.revision}:{relative}"],
                capture_output=True, text=True, check=False)
            return proc.stdout if proc.returncode == 0 else None
        path = self.root / relative
        try:
            return path.read_text(encoding="utf-8", errors="replace")
        except OSError:
            return None

    @property
    def token(self) -> str:
        return self.revision or "worktree"


# ------------------------------------------------------------------ census W04

def url_of(source: str) -> str:
    match = re.search(r"https?://[^\s|]+", source)
    if not match:
        return ""
    url = re.sub(r"#[^ ]*$", "", match.group(0))
    if url.endswith("/"):
        url = url[:-1]
    url = re.sub(r"^[A-Za-z]+://", "", url)
    slash = url.find("/")
    return url[:slash].lower() + url[slash:] if slash >= 0 else url.lower()


def registry_rows(text: str) -> list[list[str]]:
    rows: list[list[str]] = []
    in_registry = False
    for line in text.splitlines():
        heading = re.match(r"^ {0,3}##[ \t]", line)
        if heading:
            in_registry = line.lstrip(" ")[2:].strip() == "Registry"
            continue
        if re.match(r"^ {0,3}#[ \t]", line):
            in_registry = False
            continue
        if not in_registry or not re.match(r"^ {0,3}\|", line):
            continue
        cells = line.lstrip(" ").split("|")
        if len(cells) != 13:
            continue
        if all(re.fullmatch(r"\s*:?-{3,}:?\s*", cell) for cell in cells[1:-1]):
            continue
        rows.append([cell.strip() for cell in cells[1:-1]])
    return rows


def census_w04(text: str) -> list[tuple[str, str]]:
    seen_urls: set[str] = set()
    scopes: list[tuple[str, str]] = []
    collisions: list[tuple[str, str]] = []
    for row in registry_rows(text):
        row_id, source, _kind, _tier, scope = row[0], row[1], row[2], row[3], row[4]
        if not re.fullmatch(r"S\d{3,}", row_id):
            continue
        url = url_of(source)
        if url:
            key = (url, scope)
            if url in seen_urls and key not in scopes:
                collisions.append((row_id, url))
            seen_urls.add(url)
            scopes.append(key)
    return collisions


# ------------------------------------------------------------------- the items

def item_d1(tree: Tree) -> tuple[bool, str, bool]:
    lesson = tree.read(LESSON) or ""
    rfc = tree.read(RFC) or ""
    lines = [line for line in lesson.splitlines() if line.lstrip().startswith("[r84-correction")]
    state = False
    detail = "no [r84-correction line"
    for line in lines:
        missing = [heading for heading in HEADINGS if heading not in line or heading not in rfc]
        if missing:
            detail = f"heading not cited-or-retained: {missing[0]!r}"
            continue
        state = True
        detail = "four real headings cited and retained"
        break
    row = False
    for line in lines:
        if "round-83.md" in line and "Gate" in line and state:
            row = True
            break
    return state and row, detail, row


def item_d2(tree: Tree) -> tuple[bool, str, bool]:
    lesson = tree.read(LESSON) or ""
    rfc = tree.read(RFC)
    if rfc is None:
        return False, "retained RFC 9111 absent", False
    claim = None
    for line in lesson.splitlines():
        match = D2_RE.search(line)
        if match:
            claim = int(match.group(1))
            break
    if claim is None:
        return False, "no `D2 count=<n> span=838-844 measure=words-full-span` line", False
    lines = rfc.splitlines()
    if len(lines) < 844:
        return False, f"retained RFC has {len(lines)} lines, span needs 844", False
    derived = len(re.findall(r"\S+", "\n".join(lines[837:844])))
    return claim == derived, f"claimed={claim} derived={derived}", claim == derived


def item_d3(tree: Tree) -> tuple[bool, str, bool]:
    spec_text = tree.read(SPEC)
    results_text = tree.read(RESULTS)
    if spec_text is None or results_text is None:
        return False, "w1-spec.json or w1-results.json absent", False
    try:
        spec = json.loads(spec_text)
        results = json.loads(results_text)
    except json.JSONDecodeError as exc:
        return False, f"unreadable json: {exc}", False
    roles = [str(item.get("role", "")) for item in spec.get("items", [])]
    spec_connectors = roles.count("connector")
    settled = [row for row in results.get("results", [])
               if str(row.get("agent", "")) == "connector" and str(row.get("output", "")).strip()]
    state = spec_connectors >= 1 and len(settled) >= 1
    return (state, f"spec_connectors={spec_connectors} settled_connectors={len(settled)}",
            len(settled) >= 1)


def item_d4(tree: Tree) -> tuple[bool, str, bool]:
    receipt = tree.read(CENSUS)
    sources = tree.read(SOURCES)
    if receipt is None or sources is None:
        return False, "census receipt or SOURCES.md absent", False
    if "census_exit=0" not in receipt:
        return False, "receipt does not record census_exit=0", False
    if not any("\tok\t" in line and "SOURCES.md" in line for line in receipt.splitlines()):
        return False, "receipt carries no ok line naming corpus/SOURCES.md", False
    claimed = sorted((parts[0], parts[1].removesuffix(" across scopes")) for parts in
                     (line.split("\t")[2].split(" duplicate url ") for line in receipt.splitlines()
                      if "\tW04\t" in line)
                     if len(parts) == 2)
    derived = sorted(census_w04(sources))
    state = claimed == derived
    return (state, f"receipt_w04={len(claimed)} derived_w04={len(derived)}",
            len(claimed) == len(derived) and len(derived) > 0)


def evaluate(tree: Tree) -> int:
    checks = [("D1", item_d1), ("D2", item_d2), ("D3", item_d3), ("D4", item_d4)]
    open_items = 0
    for name, check in checks:
        state, detail, row = check(tree)
        closed = state and row
        open_items += 0 if closed else 1
        print(f"item={name} closed={int(closed)} state={int(state)} row={int(row)} {detail}")
    closed = len(checks) - open_items
    met = open_items == 0
    print(f"C1v1 revision={tree.token} items={len(checks)} open={open_items} "
          f"closed={closed} met={'true' if met else 'false'}")
    return 0 if met else 1


# ------------------------------------------------------------------- selftest

def write_fixture(root: Path, *, lesson: str, spec: dict | None, results: dict | None,
                  receipt: str | None, rfc: str | None) -> None:
    files = {LESSON: lesson, SOURCES: "# SOURCES\n\n## Registry\n"
                                      "| S001 | A — https://a.example/x | docs | A | s1 | §1 | t | mined | 2026-01-01 | 90d | — |\n"
                                      "| S002 | B — https://a.example/x | docs | B | s2 | §2 | t | mined | 2026-01-01 | 90d | — |\n"}
    if spec is not None:
        files[SPEC] = json.dumps(spec)
    if results is not None:
        files[RESULTS] = json.dumps(results)
    if receipt is not None:
        files[CENSUS] = receipt
    if rfc is not None:
        files[RFC] = rfc
    for relative, content in files.items():
        path = root / relative
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(content, encoding="utf-8")


def good_rfc() -> str:
    lines = ["filler"] * 844
    for index in range(838, 845):
        lines[index - 1] = " ".join(["word"] * 9)
    lines[843] += " extra1 extra2 unused"
    for index, heading in enumerate(HEADINGS):
        lines[100 + index] = heading
    return "\n".join(lines) + "\n"


def good_lesson() -> str:
    return ("# fixture\n\n[r84-correction 2026-11-04] `round-83.md` §Gate cited "
            "`5.2.  Cache-Control`, `5.2.1.  Request Directives`, "
            "`5.2.2.  Response Directives`, `5.2.3.  Extension Directives`.\n"
            "D2 count=66 span=838-844 measure=words-full-span\n")


def good_spec() -> dict:
    return {"items": [{"name": "C", "role": "connector"}, {"name": "E", "role": "executor"}]}


def good_results() -> dict:
    return {"results": [{"name": "C", "agent": "connector", "output": "done"}]}


def good_receipt() -> str:
    return ("kake\tW04\tS002 duplicate url a.example/x across scopes\n"
            "kake\tok\t/tmp/kake/corpus/SOURCES.md\ncensus_exit=0\n")


def selftest(work: Path) -> int:
    results: list[tuple[str, bool, str]] = []

    def score(name: str, expect_open: int, **kwargs) -> None:
        root = work / name
        if root.exists():
            shutil.rmtree(root)
        root.mkdir(parents=True)
        base = dict(lesson=good_lesson(), spec=good_spec(), results=good_results(),
                    receipt=good_receipt(), rfc=good_rfc())
        base.update(kwargs)
        write_fixture(root, **base)
        tree = Tree(root, None)
        checks = [item_d1, item_d2, item_d3, item_d4]
        opened = sum(0 if (state and row) else 1 for state, _d, row in
                     (check(tree) for check in checks))
        results.append((name, opened == expect_open, f"open={opened} expect={expect_open}"))

    score("green-all-closed", 0)
    score("junk-prose-only", 2, lesson="# fixture\n\nAll four items are closed.\n")
    score("mutant-d1-wrong-heading", 1, lesson=good_lesson().replace(
        "5.2.3.  Extension Directives", "5.2.9.  Extension Directives"))
    score("mutant-d2-wrong-count", 1, lesson=good_lesson().replace("count=66", "count=48"))
    score("mutant-d3-no-connector", 1, spec={"items": [{"name": "E", "role": "executor"}]})
    score("mutant-d4-wrong-w04", 1,
          receipt=good_receipt().replace("S002", "S009"))
    score("mutant-rfc-absent", 2, rfc=None)

    missing = work / "missing-tree"
    if missing.exists():
        shutil.rmtree(missing)
    missing.mkdir(parents=True)
    tree = Tree(missing, None)
    opened = sum(0 if (state and row) else 1 for state, _d, row in
                 (check(tree) for check in (item_d1, item_d2, item_d3, item_d4)))
    results.append(("missing-tree-reopens-all", opened == 4, f"open={opened} expect=4"))

    passed = sum(1 for _n, ok, _d in results if ok)
    for name, ok, detail in results:
        print(("ok   " if ok else "FAIL ") + name + (f" — {detail}" if detail else ""))
    print(f"selftest: {passed}/{len(results)} passed")
    return 0 if passed == len(results) else 1


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--root", type=Path)
    parser.add_argument("--revision")
    parser.add_argument("--selftest", action="store_true")
    parser.add_argument("--work", type=Path)
    args = parser.parse_args(argv)
    if args.selftest:
        work = args.work or Path(tempfile.mkdtemp(dir=None, prefix="c84-st-"))
        work.mkdir(parents=True, exist_ok=True)
        try:
            return selftest(work)
        finally:
            if args.work is None:
                shutil.rmtree(work, ignore_errors=True)
    if not args.root:
        parser.print_usage(sys.stderr)
        return 64
    root = args.root.resolve()
    if not root.is_dir():
        print(f"fault: not a directory: {root}", file=sys.stderr)
        return 2
    return evaluate(Tree(root, args.revision))


if __name__ == "__main__":
    raise SystemExit(main())
