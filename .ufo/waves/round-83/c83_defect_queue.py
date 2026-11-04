#!/usr/bin/env python3
"""Round-83 C1 counter — the round-82 routed-defect queue (kake, calibration).

The non-author round-82 closure (`corpus/lessons/round-82-verifier-spotcheck.md`
§6) filed six routed defects D1..D6. This counter decides, from committed lane
bytes (and the fleet repo's history, read-only), whether each one is closed. It
never reads a word that merely says "closed": every item carries a state
conjunct re-derived from a non-lesson file (wave accounting re-computed from
spec+results, UTF-8 byte lengths, an instrument receipt's own fields, the
fleet diff that removed the superseded lines, an executable killer suite, a
standing QUALITY criterion).

Frozen predicate (contract §C1):

    met <=> open == 0

Usage: c83_defect_queue.py --root <lane> [--revision <rev>] [--work <dir>]
       [--fleet <dir>] [--selftest]

Exit: 0 met, 1 measured defect, 2 unevaluable input, 64 usage. Read-only.
"""
from __future__ import annotations

import argparse
import io
import json
import re
import shutil
import subprocess
import sys
import tarfile
import tempfile
from pathlib import Path

ITEMS = ("D1", "D2", "D3", "D4", "D5", "D6")
LESSON = "corpus/lessons/round-83.md"
QUALITY = "corpus/QUALITY.md"
SPEC = ".ufo/waves/round-83/w1-spec.json"
RESULTS = ".ufo/waves/round-83/w1-results.json"
ACCOUNTING = ".ufo/waves/round-83/w1-accounting.json"
INSTRUMENT_RECEIPT = ".ufo/waves/round-83/controls/after-c83-instrument-check.txt"
KILLER = ".ufo/waves/round-83/killers/run_killers.py"
FLEET_REPORT = ".ufo/reports/round-81/kake.md"
ATTACK_ROLES = ("reviewer", "critic", "mutation-tester", "labrat")
KILLER_NAMES = ("C1-m3", "C1-m5", "C2-m2", "C2-m4", "C2-m5")
HEX40 = re.compile(r"\b([0-9a-f]{40})\b")


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

    def json(self, rel: str):
        raw = self.text(rel)
        if raw is None:
            return None
        try:
            return json.loads(raw)
        except json.JSONDecodeError:
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


def git(fleet: Path, *args: str) -> tuple[int, str]:
    proc = subprocess.run(["git", "-C", str(fleet), *args], stdout=subprocess.PIPE,
                          stderr=subprocess.PIPE, check=False)
    return proc.returncode, proc.stdout.decode("utf-8", "replace")


def derive_population(tree: Tree) -> tuple[dict | None, str]:
    spec = tree.json(SPEC)
    results = tree.json(RESULTS)
    if spec is None or results is None:
        return None, "spec or results absent/unreadable"
    items = spec.get("items")
    rows = results.get("results")
    if not isinstance(items, list) or not isinstance(rows, list):
        return None, "spec items or results rows malformed"
    roles: dict[str, str] = {}
    for item in items:
        if isinstance(item, dict) and isinstance(item.get("name"), str):
            roles[item["name"]] = str(item.get("role", ""))
    settled: list[str] = []
    seats: list[dict] = []
    for row in rows:
        if not isinstance(row, dict) or not isinstance(row.get("name"), str):
            continue
        output = row.get("output") or ""
        size = len(output.encode("utf-8")) if isinstance(output, str) else 0
        seats.append({"name": row["name"], "role": roles.get(row["name"], ""),
                      "output_bytes": size})
        if size > 0:
            settled.append(row["name"])
    settled_attack = [name for name in settled if roles.get(name) in ATTACK_ROLES]
    share = round(len(settled_attack) / len(settled), 4) if settled else 0.0
    return {
        "requested": len(roles),
        "settled": len(settled),
        "settled_names": sorted(settled),
        "settled_attack": len(settled_attack),
        "settled_share": share,
        "seats": seats,
    }, ""


def item_d1(tree: Tree, lesson: str | None, _fleet: Path) -> tuple[bool, str]:
    derived, detail = derive_population(tree)
    if derived is None:
        return False, detail
    record = tree.json(ACCOUNTING)
    if not isinstance(record, dict):
        return False, "w1-accounting.json absent or unreadable"
    recorded_names = record.get("settled_names")
    ok = (derived["settled_attack"] >= 2 and derived["settled_share"] >= 0.25
          and record.get("settled") == derived["settled"]
          and sorted(recorded_names or []) == derived["settled_names"]
          and record.get("settled_attack") == derived["settled_attack"]
          and record.get("settled_share") == derived["settled_share"])
    log = line_with(lesson, "D1", ["0/7", "settled_attack="])
    return ok and log is not None, (
        f"settled={derived['settled']} settled_attack={derived['settled_attack']} "
        f"settled_share={derived['settled_share']} record={'ok' if record else 'no'} "
        f"log={'yes' if log else 'no'}")


def item_d2(tree: Tree, lesson: str | None, _fleet: Path) -> tuple[bool, str]:
    derived, detail = derive_population(tree)
    record = tree.json(ACCOUNTING)
    if derived is None or not isinstance(record, dict):
        return False, detail or "w1-accounting.json absent"
    if record.get("bytes_basis") != "utf-8":
        return False, f"bytes_basis={record.get('bytes_basis')!r}"
    recorded = {row.get("name"): row.get("output_bytes")
                for row in record.get("seats", []) if isinstance(row, dict)}
    mismatched = [row["name"] for row in derived["seats"]
                  if row["output_bytes"] > 0 and recorded.get(row["name"]) != row["output_bytes"]]
    log = line_with(lesson, "D2", ["UTF-8", "w1-accounting.json"])
    return not mismatched and log is not None, (
        f"mismatched={mismatched[:3]} log={'yes' if log else 'no'}")


def item_d3(tree: Tree, lesson: str | None, _fleet: Path) -> tuple[bool, str]:
    receipt = tree.text(INSTRUMENT_RECEIPT)
    if receipt is None:
        return False, "after-c83-instrument-check.txt absent"
    line = None
    for candidate in receipt.splitlines():
        if candidate.startswith("C2v1 ") and HEX40.search(candidate):
            line = candidate
            break
    if line is None:
        return False, "no C2v1 revision line"
    fields = dict(re.findall(r"(\w+)=(\S+)", line))
    ok = (fields.get("bound") == fields.get("population")
          and fields.get("mismatches") == "0" and fields.get("met") == "true")
    log = line_with(lesson, "D3", ["after-c83-instrument-check.txt", "--check"])
    return ok and log is not None, (
        f"bound={fields.get('bound')} population={fields.get('population')} "
        f"mismatches={fields.get('mismatches')} met={fields.get('met')} "
        f"log={'yes' if log else 'no'}")


def item_d4(tree: Tree, lesson: str | None, fleet: Path) -> tuple[bool, str]:
    if lesson is None:
        return False, "lesson absent"
    rc, listing = git(fleet, "log", "--format=%H", "--", FLEET_REPORT)
    commits = [line.strip() for line in listing.splitlines() if line.strip()]
    if rc != 0 or len(commits) < 2:
        return False, f"fleet history for {FLEET_REPORT} has {len(commits)} commit(s)"
    after, before = commits[0], commits[1]
    rc, diff = git(fleet, "diff", before, after, "--", FLEET_REPORT)
    if rc != 0:
        return False, "fleet diff failed"
    removed = [line[1:] for line in diff.splitlines()
               if line.startswith("-") and not line.startswith("---") and len(line) > 41]
    quoted = [line for line in removed if line in lesson]
    log = line_with(lesson, "D4", [after[:8], "erratum"])
    return len(quoted) >= 4 and log is not None, (
        f"removed={len(removed)} quoted={len(quoted)} amendment={after[:8]} "
        f"log={'yes' if log else 'no'}")


def item_d5(tree: Tree, lesson: str | None, _fleet: Path) -> tuple[bool, str]:
    runner = tree.root / KILLER
    if not runner.is_file():
        return False, "run_killers.py absent"
    proc = subprocess.run([sys.executable, "-B", str(runner), "--check"],
                          cwd=str(tree.root), stdout=subprocess.PIPE,
                          stderr=subprocess.PIPE, check=False)
    out = proc.stdout.decode("utf-8", "replace")
    tail = out.strip().splitlines()[-1] if out.strip() else ""
    rows_ok = all(any(name in line and ("killed" in line or "equivalent" in line)
                      for line in out.splitlines()) for name in KILLER_NAMES)
    ok = proc.returncode == 0 and "distinguished=5/5" in out and rows_ok
    log = line_with(lesson, "D5", ["distinguished=5/5", *KILLER_NAMES])
    return ok and log is not None, (
        f"rc={proc.returncode} tail={tail[:60]!r} rows={'yes' if rows_ok else 'no'} "
        f"log={'yes' if log else 'no'}")


def item_d6(tree: Tree, lesson: str | None, _fleet: Path) -> tuple[bool, str]:
    quality = tree.text(QUALITY)
    if quality is None:
        return False, "QUALITY.md absent"
    criterion = any("corpus/lessons/round-82.md" in line and "Gate" in line
                    and "round-83" in line for line in quality.splitlines())
    log = line_with(lesson, "D6", ["§Gate", "corpus/QUALITY.md"])
    return criterion and log is not None, (
        f"criterion={'yes' if criterion else 'no'} log={'yes' if log else 'no'}")


EVALUATORS = {"D1": item_d1, "D2": item_d2, "D3": item_d3,
              "D4": item_d4, "D5": item_d5, "D6": item_d6}


def evaluate(tree: Tree, fleet: Path) -> list[tuple[str, bool, str]]:
    lesson = tree.text(LESSON)
    rows = []
    for item in ITEMS:
        try:
            ok, detail = EVALUATORS[item](tree, lesson, fleet)
        except Exception as exc:  # a broken input is an open item, never a crash
            ok, detail = False, f"evaluator error: {exc}"
        rows.append((item, ok, detail))
    return rows


def run(tree_root: Path, revision: str | None, work: Path, fleet: Path) -> int:
    if revision:
        root = export(tree_root, revision, work)
        label = revision
    else:
        root = tree_root
        label = "worktree"
    rows = evaluate(Tree(root), fleet)
    for item, ok, detail in rows:
        print(f"{item} {'closed' if ok else 'open'} {detail}")
    closed = sum(1 for _item, ok, _detail in rows if ok)
    open_items = len(rows) - closed
    met = open_items == 0
    print(f"C1v1 revision={label} items={len(rows)} open={open_items} "
          f"closed={closed} met={'true' if met else 'false'}")
    return 0 if met else 1


# --------------------------------------------------------------------- selftest

def write_fixture(root: Path, fleet: Path) -> None:
    (root / "corpus" / "lessons").mkdir(parents=True, exist_ok=True)
    (root / ".ufo/waves/round-83/controls").mkdir(parents=True, exist_ok=True)
    (root / ".ufo/waves/round-83/killers").mkdir(parents=True, exist_ok=True)
    (root / SPEC).write_text(json.dumps({"items": [
        {"name": "Alfa", "role": "executor"},
        {"name": "Bravo", "role": "reviewer"},
        {"name": "Charlie", "role": "scribe"},
        {"name": "Delta", "role": "critic"},
    ]}), encoding="utf-8")
    (root / RESULTS).write_text(json.dumps({"results": [
        {"name": "Alfa", "output": "a" * 300},
        {"name": "Bravo", "output": "b" * 300},
        {"name": "Charlie", "output": "c" * 300},
        {"name": "Delta", "output": "d" * 300},
    ]}), encoding="utf-8")
    (root / ACCOUNTING).write_text(json.dumps({
        "bytes_basis": "utf-8", "settled": 4,
        "settled_names": ["Alfa", "Bravo", "Charlie", "Delta"],
        "settled_attack": 2, "settled_share": 0.5,
        "seats": [{"name": "Alfa", "role": "executor", "output_bytes": 300},
                  {"name": "Bravo", "role": "reviewer", "output_bytes": 300},
                  {"name": "Charlie", "role": "scribe", "output_bytes": 300},
                  {"name": "Delta", "role": "critic", "output_bytes": 300}],
    }), encoding="utf-8")
    (root / INSTRUMENT_RECEIPT).write_text(
        "C2v1 revision=" + "a" * 40 + " population=30 bound=30 mismatches=0 met=true\n",
        encoding="utf-8")
    (root / KILLER).write_text(
        "import sys\n"
        "print('C1-m3 killed fixture=seat-bytes')\n"
        "print('C1-m5 killed fixture=gate-red')\n"
        "print('C2-m2 killed fixture=equal-instants')\n"
        "print('C2-m4 killed fixture=broken-tool')\n"
        "print('C2-m5 killed fixture=dropped-a-surface')\n"
        "print('distinguished=5/5')\n"
        "raise SystemExit(0 if '--check' in sys.argv else 0)\n", encoding="utf-8")
    (root / QUALITY).write_text(
        "# QUALITY (fixture)\n\n"
        "- A Gate summary must cite the lesson section it summarises "
        "(`corpus/lessons/round-82.md` §Gate); added `round-83`.\n", encoding="utf-8")
    rc, diff = git(fleet, "diff", "HEAD~1", "HEAD", "--", FLEET_REPORT)
    removed = [line[1:] for line in diff.splitlines()
               if line.startswith("-") and not line.startswith("---") and len(line) > 41][:4]
    quotes = "\n".join("> " + line for line in removed)
    (root / LESSON).write_text(
        "# Round 83 (fixture)\n\n"
        "**D1 — attack floor.** settled_attack=1 of 3, superseding 0/7.\n"
        "**D2 — units.** UTF-8 bytes from w1-accounting.json.\n"
        "**D3 — instrument receipt.** controls/after-c83-instrument-check.txt, `--check`.\n"
        f"**D4 — erratum.** commit `{git(fleet, 'rev-parse', 'HEAD')[1].strip()[:8]}` — "
        "the superseded statements quoted:\n\n" + quotes + "\n\n"
        "**D5 — killers.** distinguished=5/5 over C1-m3 C1-m5 C2-m2 C2-m4 C2-m5.\n"
        "**D6 — provenance.** §Gate rule lands in corpus/QUALITY.md.\n", encoding="utf-8")


def selftest() -> int:
    work = Path(tempfile.mkdtemp(prefix="c83-defect-selftest-"))
    results: list[tuple[str, bool, str]] = []
    try:
        fleet = work / "fleet"
        fleet.mkdir()
        subprocess.run(["git", "-C", str(fleet), "init", "-q"], check=True)
        if Path(subprocess.run(["git", "-C", str(fleet), "rev-parse", "--show-toplevel"],
                               stdout=subprocess.PIPE, check=True
                               ).stdout.decode().strip()).resolve() != fleet.resolve():
            raise RuntimeError("fixture git toplevel mismatch")
        identity = ["-c", "user.name=fixture", "-c", "user.email=fixture@example.test"]
        report = fleet / FLEET_REPORT
        report.parent.mkdir(parents=True)
        lines = [
            "# report fixture line one is long enough to matter",
            "the lane tip at filing abc is superseded by the amendment",
            "the wave bullet said one seat died and was not replaced",
            "the claim row measured at the earlier carrier only",
            "controls were named without a receipt path at all",
        ]
        report.write_text("\n".join(lines) + "\n", encoding="utf-8")
        subprocess.run(["git", "-C", str(fleet), "add", FLEET_REPORT], check=True)
        subprocess.run(["git", "-C", str(fleet), *identity, "commit", "-q", "-m", "filed"],
                       check=True)
        report.write_text("\n".join(lines[:1]) + "\nrevised\n", encoding="utf-8")
        subprocess.run(["git", "-C", str(fleet), "add", FLEET_REPORT], check=True)
        subprocess.run(["git", "-C", str(fleet), *identity, "commit", "-q", "-m", "amended"],
                       check=True)

        def score(name: str, expect_open: int, mutate) -> None:
            tree = work / ("tree-" + name)
            if tree.exists():
                shutil.rmtree(tree)
            tree.mkdir()
            write_fixture(tree, fleet)
            mutate(tree)
            rows = evaluate(Tree(tree), fleet)
            open_items = sum(1 for _item, ok, _detail in rows if not ok)
            results.append((name, open_items == expect_open,
                            "" if open_items == expect_open else
                            f"open={open_items} expected={expect_open} "
                            f"({[i for i, ok, _d in rows if not ok]})"))

        score("green-all-six-closed", 0, lambda tree: None)
        score("junk-prose-only", 6, lambda tree: (
            (tree / LESSON).write_text(
                "# lessons\n\n" + "\n".join(
                    f"**{item} — closed.** The work is done." for item in ITEMS) + "\n"),
            (tree / QUALITY).write_text("# QUALITY\n"),
            (tree / ACCOUNTING).unlink(), (tree / INSTRUMENT_RECEIPT).unlink(),
            (tree / KILLER).unlink()))

        def d1_mutant(tree: Path) -> None:
            (tree / RESULTS).write_text(json.dumps({"results": [
                {"name": "Alfa", "output": "a" * 300},
                {"name": "Bravo", "output": ""},
                {"name": "Charlie", "output": "c" * 300},
                {"name": "Delta", "output": "d" * 300},
            ]}), encoding="utf-8")

        score("d1-attack-seat-empty", 1, d1_mutant)

        def d2_mutant(tree: Path) -> None:
            record = json.loads((tree / ACCOUNTING).read_text())
            record["seats"][0]["output_bytes"] = 301
            (tree / ACCOUNTING).write_text(json.dumps(record), encoding="utf-8")

        score("d2-byte-count-drift", 1, d2_mutant)

        def d3_mutant(tree: Path) -> None:
            (tree / INSTRUMENT_RECEIPT).write_text(
                "C2v1 revision=" + "a" * 40 +
                " population=30 bound=30 mismatches=2 met=true\n", encoding="utf-8")

        score("d3-red-instrument-receipt", 1, d3_mutant)

        def d4_mutant(tree: Path) -> None:
            text = (tree / LESSON).read_text(encoding="utf-8")
            (tree / LESSON).write_text(
                "\n".join(line for line in text.splitlines()
                          if not line.startswith("> ")) + "\n", encoding="utf-8")

        score("d4-unquoted-erratum", 1, d4_mutant)

        def d5_mutant(tree: Path) -> None:
            (tree / KILLER).write_text(
                "print('C1-m3 killed')\nprint('distinguished=1/5')\n", encoding="utf-8")

        score("d5-partial-killers", 1, d5_mutant)

        def d6_mutant(tree: Path) -> None:
            (tree / QUALITY).write_text("# QUALITY\n\n- no provenance criterion\n",
                                        encoding="utf-8")

        score("d6-missing-criterion", 1, d6_mutant)
        rows = evaluate(Tree(work / "absent-tree"), fleet)
        results.append(("missing-tree-all-open", len(rows) == len(ITEMS), ""))
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
    work = Path(args.work) if args.work else Path(tempfile.mkdtemp(prefix="c83-defect-"))
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
