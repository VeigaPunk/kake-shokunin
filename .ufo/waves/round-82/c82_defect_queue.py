#!/usr/bin/env python3
"""Round-82 C1 counter — the round-81 routed-defect queue (kake, calibration).

The non-author round-81 closure (`corpus/lessons/round-81-verifier-spotcheck.md`
§7) filed eight routed defects D1..D8. This counter decides, from committed
lane bytes (and the fleet repo's history, read-only), whether each one is
closed. It never reads a word that merely says "closed": every item carries at
least one state conjunct re-derived from a non-lesson file (registry cells, a
receipt's own revision, a fleet commit's blob pair, a seat record's numbers, a
path's presence, a selftest tally, a gate receipt's fields, or the round-80
lesson bytes).

Frozen predicate (contract §C1):

    met <=> open == 0

Usage: c82_defect_queue.py --root <lane> [--revision <rev>] [--work <dir>]
       [--fleet <dir>] [--selftest]

Exit: 0 met, 1 measured defect, 2 unevaluable input, 64 usage. Read-only.
"""
from __future__ import annotations

import argparse
import json
import re
import shutil
import subprocess
import sys
import tarfile
import tempfile
import io
from pathlib import Path

ITEMS = ("D1", "D2", "D3", "D4", "D5", "D6", "D7", "D8")
LESSON = "corpus/lessons/round-82.md"
ROUND80_LESSON = "corpus/lessons/round-80.md"
REGISTRY = "corpus/SOURCES.md"
QUALITY = "corpus/QUALITY.md"
SEAT_RECORD = ".ufo/waves/round-81/seat-failures.json"
C1_FINAL = ".ufo/waves/round-81/controls/after-c1-final.txt"
C2_SELFTEST = ".ufo/waves/round-81/controls/c81-selftest-c2.txt"
LEDGER_RECEIPT = ".ufo/waves/round-82/controls/after-c1-ledger-gate.txt"
FLEET_REPORT = ".ufo/reports/round-81/kake.md"
DEAD_PATHS = (".ufo/waves/round-81/controls/after-c81-defect-queue.txt",
              ".ufo/waves/round-81/controls/after-c81-capture-audit.txt")
LIVE_RECEIPT = ".ufo/waves/round-81/controls/after-c1-final.txt"
HEX40 = re.compile(r"\b([0-9a-f]{40})\b")
HEX7 = re.compile(r"\b([0-9a-f]{7,40})\b")
WORD = re.compile(r"[A-Za-z0-9_.\-/]+")


class Tree:
    def __init__(self, root: Path) -> None:
        self.root = root

    def text(self, rel: str) -> str | None:
        path = self.root / rel
        if not path.is_file():
            return None
        try:
            return path.read_text(encoding="utf-8", errors="replace")
        except OSError:
            return None

    def exists(self, rel: str) -> bool:
        return (self.root / rel).is_file()


def export(root: Path, revision: str, work: Path) -> Path:
    target = work / "export"
    if target.exists():
        shutil.rmtree(target)
    target.mkdir(parents=True)
    proc = subprocess.run(
        ["git", "-C", str(root), "archive", "--format=tar", revision],
        stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False,
    )
    if proc.returncode != 0:
        raise RuntimeError(
            f"git archive {revision} failed: {proc.stderr.decode('utf-8', 'replace').strip()}"
        )
    with tarfile.open(fileobj=io.BytesIO(proc.stdout)) as archive:
        archive.extractall(target)
    return target


def row_cells(line: str) -> list[str]:
    return [cell.strip() for cell in line.split("|")]


def registry_row(tree: Tree, source_id: str) -> list[str] | None:
    text = tree.text(REGISTRY)
    if text is None:
        return None
    pattern = re.compile(r"^\|\s*" + source_id + r"\s*\|")
    for line in text.splitlines():
        if pattern.match(line):
            cells = row_cells(line)
            if len(cells) == 13:  # leading and trailing pipe yield two empty cells
                return cells[1:-1]
    return None


def line_with(text: str | None, tag: str, tokens: list[str]) -> str | None:
    if text is None:
        return None
    tag_re = re.compile(r"\b" + re.escape(tag) + r"\b")
    for line in text.splitlines():
        if not tag_re.search(line):
            continue
        if all(token in line for token in tokens):
            return line
    return None


def git_show(fleet: Path, revision: str, rel: str) -> str | None:
    proc = subprocess.run(
        ["git", "-C", str(fleet), "show", f"{revision}:{rel}"],
        stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False,
    )
    if proc.returncode != 0:
        return None
    return proc.stdout.decode("utf-8", "replace")


def git_resolves(fleet: Path, revision: str) -> bool:
    proc = subprocess.run(
        ["git", "-C", str(fleet), "cat-file", "-e", f"{revision}^{{commit}}"],
        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, check=False,
    )
    return proc.returncode == 0


def item_d1(tree: Tree, lesson: str | None, _fleet: Path) -> tuple[bool, str]:
    row = registry_row(tree, "S433")
    if row is None:
        return False, "S433 row absent"
    recheck, used_by = row[9], row[10]
    log = line_with(lesson, "D1", ["180d", "2027-05-03"])
    ok = recheck == "2027-05-03" and "corpus/lessons/round-81.md" in used_by and log is not None
    return ok, (f"recheck={recheck!r} used-by={used_by!r} log={'yes' if log else 'no'}")


def item_d2(tree: Tree, lesson: str | None, _fleet: Path) -> tuple[bool, str]:
    receipt = tree.text(C1_FINAL)
    if receipt is None:
        return False, "after-c1-final.txt absent"
    match = HEX40.search(receipt)
    if not match:
        return False, "after-c1-final.txt carries no revision"
    revision = match.group(1)
    log = line_with(lesson, "D2", [revision, "2b46f5c4", "superseded"])
    return log is not None, f"receipt revision={revision} log={'yes' if log else 'no'}"


def item_d3(tree: Tree, lesson: str | None, fleet: Path) -> tuple[bool, str]:
    log = line_with(lesson, "D3", ["erratum"])
    if log is None:
        return False, "no D3 erratum line"
    candidates = [token for token in HEX7.findall(log) if 7 <= len(token) <= 40]
    if not candidates:
        return False, "D3 line names no commit token"
    for candidate in candidates:
        if not git_resolves(fleet, candidate):
            continue
        parent = f"{candidate}^"
        if not git_resolves(fleet, parent):
            continue
        after = git_show(fleet, candidate, FLEET_REPORT)
        before = git_show(fleet, parent, FLEET_REPORT)
        if after is None or before is None:
            continue
        if after != before:
            return True, f"commit {candidate} rewrites {FLEET_REPORT} against {parent}"
    return False, f"no named commit with a report blob change ({candidates})"


def item_d4(tree: Tree, lesson: str | None, _fleet: Path) -> tuple[bool, str]:
    raw = tree.text(SEAT_RECORD)
    if raw is None:
        return False, "seat-failures.json absent"
    try:
        record = json.loads(raw)
        seats = record["seats"]
    except (json.JSONDecodeError, KeyError, TypeError):
        return False, "seat-failures.json unreadable"
    numbers = [entry.get("output_bytes") for entry in seats.values()
               if isinstance(entry, dict) and entry.get("role") == "mutation-tester"]
    numbers = [value for value in numbers if isinstance(value, int)]
    if not numbers:
        return False, "no mutation-tester output_bytes"
    derived = numbers[0]
    log = line_with(lesson, "D4", [str(derived), "superseded"])
    if log is None:
        return False, f"no D4 line carrying {derived} and superseded"
    if lesson is not None:
        for line in lesson.splitlines():
            if ("3771" in line or "3,771" in line) and "superseded" not in line:
                return False, f"uncorrected wrong number on: {line.strip()[:80]}"
    return True, f"derived output_bytes={derived}"


def item_d5(tree: Tree, lesson: str | None, _fleet: Path) -> tuple[bool, str]:
    log = line_with(lesson, "D5", [DEAD_PATHS[0], DEAD_PATHS[1], LIVE_RECEIPT])
    if log is None:
        return False, "no D5 line naming both dead paths and the live receipt"
    present = [path for path in DEAD_PATHS if tree.exists(path)]
    if present:
        return False, f"dead path present: {present}"
    if not tree.exists(LIVE_RECEIPT):
        return False, f"live receipt absent: {LIVE_RECEIPT}"
    return True, "both dead paths absent, live receipt present"


def item_d6(tree: Tree, _lesson: str | None, _fleet: Path) -> tuple[bool, str]:
    quality = tree.text(QUALITY)
    receipt = tree.text(C2_SELFTEST)
    if quality is None or receipt is None:
        return False, "QUALITY.md or selftest receipt absent"
    grounded = any("22/22" in line and "supersedes" in line and "round-81" in line
                   for line in quality.splitlines())
    tally = "selftest: 22/22 passed" in receipt
    return grounded and tally, f"criterion={'yes' if grounded else 'no'} receipt22={'yes' if tally else 'no'}"


def item_d7(tree: Tree, lesson: str | None, _fleet: Path) -> tuple[bool, str]:
    receipt = tree.text(LEDGER_RECEIPT)
    if receipt is None:
        return False, "after-c1-ledger-gate.txt absent"
    log = line_with(lesson, "D7", ["after-c1-ledger-gate.txt"])
    ok = "undisclosed=0" in receipt and "met=true" in receipt and log is not None
    return ok, (f"receipt green={'yes' if 'met=true' in receipt else 'no'}"
                f" log={'yes' if log else 'no'}")


def item_d8(tree: Tree, lesson: str | None, _fleet: Path) -> tuple[bool, str]:
    round80 = tree.text(ROUND80_LESSON)
    if round80 is None:
        return False, "round-80 lesson absent"
    corrected = any("[r82-correction" in line and "corpus/SOURCES.md:200" in line
                    for line in round80.splitlines())
    log = line_with(lesson, "D8", [".ufo/reports/round-80/kake.md", "corpus/SOURCES.md:200"])
    return corrected and log is not None, (
        f"round-80 correction={'yes' if corrected else 'no'} log={'yes' if log else 'no'}")


EVALUATORS = {
    "D1": item_d1, "D2": item_d2, "D3": item_d3, "D4": item_d4,
    "D5": item_d5, "D6": item_d6, "D7": item_d7, "D8": item_d8,
}


def evaluate(tree: Tree, fleet: Path) -> tuple[list[tuple[str, bool, str]], bool]:
    lesson = tree.text(LESSON)
    results = []
    for item in ITEMS:
        ok, detail = EVALUATORS[item](tree, lesson, fleet)
        results.append((item, ok, detail))
    return results, lesson is not None


def run(tree_root: Path, revision: str | None, work: Path, fleet: Path) -> int:
    if revision:
        root = export(tree_root, revision, work)
        label = revision
    else:
        root = tree_root
        label = "worktree"
    tree = Tree(root)
    results, _lesson_present = evaluate(tree, fleet)
    for item, ok, detail in results:
        print(f"{item} {'closed' if ok else 'open'} {detail}")
    closed = sum(1 for _item, ok, _detail in results if ok)
    open_items = len(results) - closed
    met = open_items == 0
    print(f"C1v1 revision={label} items={len(results)} open={open_items} "
          f"closed={closed} met={'true' if met else 'false'}")
    return 0 if met else 1


# --------------------------------------------------------------------- selftest

GREEN_LESSON = """# Round 82 — lessons (fixture)

**D1 — registry cells.** S433 `recheck 180d -> 2027-05-03`, `used-by` gained `corpus/lessons/round-81.md`.

**D2 — measured revision superseded.** The receipt records `{rev}`; commit `2b46f5c4` only adds the receipts, so the superseded citation is corrected to the receipt's own revision.

**D3 — erratum for the filed report.** `.ufo/reports/round-81/kake.md` was rewritten in place at `{fleet_commit}`; this is the erratum naming the superseded statements.

**D4 — disclosure arithmetic.** The record carries output_bytes {bytes}; the superseded byte count was wrong.

**D5 — receipt paths.** {dead1} and {dead2} never existed; the committed receipts are {live}.

**D6 — superseded tally.** QUALITY.md row supersedes 18/18 with 22/22 for round-81.

**D7 — ledger gate.** The standing gate receipt {ledger} is green.

**D8 — routed pointer.** `corpus/SOURCES.md:201` is superseded by `corpus/SOURCES.md:200`; the fleet report `.ufo/reports/round-80/kake.md` is named here.
"""


def build_green_tree(root: Path, fleet_commit: str, live_receipt: str) -> None:
    (root / "corpus" / "lessons").mkdir(parents=True)
    (root / "corpus" / "knowledge").mkdir(parents=True)
    (root / ".ufo/waves/round-81/controls").mkdir(parents=True)
    (root / ".ufo/waves/round-82/controls").mkdir(parents=True)
    (root / QUALITY).write_text(
        "# QUALITY (fixture)\n\n- Criterion supersedes the round-81 18/18 tally with the committed "
        "22/22 receipt (round-81 selftest).\n", encoding="utf-8")
    (root / REGISTRY).write_text(
        "# SOURCES (fixture)\n\n"
        "| id | source | kind | tier | scope | anchor | teaches | status | opened | recheck | used-by |\n"
        "|---|---|---|---|---|---|---|---|---|---|---|\n"
        "| S433 | RFC 9110 — https://example.test/rfc9110 | spec | A | fixture scope | fixture anchor | "
        "fixture teaches | mined | 2026-10-27 | 2027-05-03 | corpus/knowledge/response-header-expectations.md, "
        "corpus/lessons/round-81.md |\n", encoding="utf-8")
    (root / LESSON).write_text(GREEN_LESSON.format(
        rev="a" * 40, fleet_commit=fleet_commit, bytes=3801,
        dead1=DEAD_PATHS[0], dead2=DEAD_PATHS[1], live=LIVE_RECEIPT,
        ledger=LEDGER_RECEIPT), encoding="utf-8")
    (root / ROUND80_LESSON).write_text(
        "# Round 80\n\n**R80-1 [r82-correction 2026-11-04]** the pointer is "
        "`corpus/SOURCES.md:200`, not `:201`.\n", encoding="utf-8")
    (root / C1_FINAL).write_text(
        "$ python3 ... --revision " + "a" * 40 + "\nC1v1 revision=" + "a" * 40 +
        " items=6 open=0 closed=6 met=true\nexit=0\n", encoding="utf-8")
    (root / C2_SELFTEST).write_text("$ python3 ... --selftest\nselftest: 22/22 passed\nexit=0\n",
                                    encoding="utf-8")
    (root / LEDGER_RECEIPT).write_text(
        "C1v2 revision=" + "b" * 40 + " events=40 undisclosed=0 phantom=0 malformed=0 "
        "wrong_kind=0 unpointed=0 symlinks=0 round_rewritten=0 met=true\nexit=0\n",
        encoding="utf-8")
    (root / SEAT_RECORD).write_text(json.dumps({
        "round": 81, "wave": "w1",
        "seats": {"MutC": {"agent": "mutation-tester", "role": "mutation-tester",
                           "status": "reported", "output_bytes": 3801,
                           "error": "not recorded in w1-results.json", "exit": "unknown"}},
    }, indent=1), encoding="utf-8")
    for path in DEAD_PATHS:
        code = root / path
        if code.exists():
            code.unlink()


def git(repo: Path, *args: str) -> str:
    proc = subprocess.run(["git", "-C", str(repo), *args], check=True,
                          stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    return proc.stdout.decode().strip()


def selftest() -> int:
    work = Path(tempfile.mkdtemp(prefix="c82-defect-selftest-"))
    results: list[tuple[str, bool, str]] = []
    try:
        fleet = work / "fleet"
        fleet.mkdir()
        git(fleet, "init", "-q")
        if Path(git(fleet, "rev-parse", "--show-toplevel")).resolve() != fleet.resolve():
            raise RuntimeError("fixture git toplevel mismatch")
        identity = ["-c", "user.name=fixture", "-c", "user.email=fixture@example.test"]
        report = fleet / FLEET_REPORT
        report.parent.mkdir(parents=True)
        report.write_text("filed report\n", encoding="utf-8")
        git(fleet, "add", FLEET_REPORT)
        git(fleet, *identity, "commit", "-q", "-m", "filed")
        report.write_text("filed report\namended lane-tip line\n", encoding="utf-8")
        git(fleet, "add", FLEET_REPORT)
        git(fleet, *identity, "commit", "-q", "-m", "amended")
        fleet_commit = git(fleet, "rev-parse", "--short=8", "HEAD")

        def score(name: str, expect_open: int, mutate) -> None:
            tree = work / ("tree-" + name)
            if tree.exists():
                shutil.rmtree(tree)
            tree.mkdir()
            build_green_tree(tree, fleet_commit, LIVE_RECEIPT)
            mutate(tree)
            rows, _present = evaluate(Tree(tree), fleet)
            open_items = sum(1 for _item, ok, _detail in rows if not ok)
            results.append((name, open_items == expect_open,
                            "" if open_items == expect_open else
                            f"open={open_items} expected={expect_open} "
                            f"({[i for i, ok, _d in rows if not ok]})"))

        score("green-all-eight-closed", 0, lambda tree: None)
        score("junk-no-corrections", 8, lambda tree: (
            (tree / LESSON).write_text(
                "# lessons\n\n" + "\n".join(
                    f"**{item} — closed.** The work is done." for item in ITEMS) + "\n",
                encoding="utf-8"),
            (tree / QUALITY).write_text("# QUALITY\n", encoding="utf-8"),
            (tree / ROUND80_LESSON).write_text("# Round 80\n", encoding="utf-8"),
            (tree / C1_FINAL).unlink(), (tree / C2_SELFTEST).unlink(),
            (tree / LEDGER_RECEIPT).unlink(), (tree / SEAT_RECORD).unlink()))

        def d1_mutant(tree: Path) -> None:
            text = (tree / REGISTRY).read_text()
            (tree / REGISTRY).write_text(text.replace("| 2027-05-03 |", "| 180d |"))

        score("d1-registry-cell-unchanged", 1, d1_mutant)

        def d2_mutant(tree: Path) -> None:
            text = (tree / C1_FINAL).read_text().replace("a" * 40, "c" * 40)
            (tree / C1_FINAL).write_text(text)

        score("d2-receipt-revision-drift", 1, d2_mutant)

        def d3_mutant(tree: Path) -> None:
            text = (tree / LESSON).read_text()
            (tree / LESSON).write_text(text.replace(fleet_commit, "d" * 8))

        score("d3-fabricated-commit", 1, d3_mutant)

        def d4_mutant(tree: Path) -> None:
            text = (tree / LESSON).read_text().replace("3801", "3771")
            (tree / LESSON).write_text(text)

        score("d4-wrong-number", 1, d4_mutant)

        def d5_mutant(tree: Path) -> None:
            dead = tree / DEAD_PATHS[0]
            dead.write_text("fabricated receipt\n", encoding="utf-8")

        score("d5-dead-path-materialised", 1, d5_mutant)

        def d6_mutant(tree: Path) -> None:
            (tree / QUALITY).write_text("# QUALITY\n\n- 18/18 tally, supersedes nothing.\n")

        score("d6-stale-tally", 1, d6_mutant)

        def d7_mutant(tree: Path) -> None:
            text = (tree / LEDGER_RECEIPT).read_text().replace("undisclosed=0", "undisclosed=3")
            (tree / LEDGER_RECEIPT).write_text(text)

        score("d7-red-gate-receipt", 1, d7_mutant)

        def d8_mutant(tree: Path) -> None:
            (tree / ROUND80_LESSON).write_text("# Round 80\n\nno correction here\n")

        score("d8-no-round80-correction", 1, d8_mutant)

        missing = work / "absent-tree"
        try:
            evaluate(Tree(missing), fleet)
            rows = [(item, False, "absent") for item in ITEMS]
            open_items = len(rows)
        except Exception:  # a missing tree must not crash: the evaluator returns opens
            open_items = 0
        results.append(("missing-tree-all-open", open_items == len(ITEMS),
                        "" if open_items == len(ITEMS) else f"open={open_items}"))
    finally:
        shutil.rmtree(work, ignore_errors=True)

    passed = sum(1 for _name, ok, _detail in results if ok)
    for name, ok, detail in results:
        print(("ok   " if ok else "FAIL ") + name + (f" — {detail}" if detail else ""))
    print(f"selftest: {passed}/{len(results)} passed")
    return 0 if passed == len(results) else 1


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--root", default=".")
    parser.add_argument("--revision")
    parser.add_argument("--work")
    parser.add_argument("--fleet", default="/home/vgpnk/Projects/shokunin")
    parser.add_argument("--selftest", action="store_true")
    try:
        args = parser.parse_args(argv)
    except SystemExit as exc:
        return 0 if exc.code == 0 else 64
    if args.selftest:
        return selftest()
    root = Path(args.root).resolve()
    fleet = Path(args.fleet).resolve()
    if not (root / ".git").exists() and args.revision:
        print("fault (tree) root carries no git repository", file=sys.stderr)
        return 2
    work = Path(args.work) if args.work else Path(tempfile.mkdtemp(prefix="c82-defect-"))
    own_work = args.work is None
    try:
        return run(root, args.revision, work, fleet)
    except RuntimeError as exc:
        print(f"fault (tree) {exc}", file=sys.stderr)
        return 2
    finally:
        if own_work:
            shutil.rmtree(work, ignore_errors=True)


if __name__ == "__main__":
    raise SystemExit(main())
