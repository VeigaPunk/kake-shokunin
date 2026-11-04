#!/usr/bin/env python3
"""Round-83 D5 killer suite — the five round-82 mutation-probe survivors.

The round-82 author-side probe (corpus/lessons/round-82.md, "Author-side
mutation probe") left five mutants alive against their own selftests: C1 `m3`
(D4's derived byte count replaced by the constant 3801) and `m5` (D7's
`met=true` requirement dropped), C2 `m2` (the instant order made non-strict),
`m4` (`selftest_ok` hard-coded to 1) and `m5` (`surfaces_a == 3` dropped from
`met`). Each one is repaired here by a fixture, not by a sentence.

For every mutant this runner:

  1. copies the frozen round-82 counter into its scratch tree (the originals
     at `.ufo/waves/round-82/` are only read, and their sha256 is checked
     against `population.json` before anything runs);
  2. applies the recorded patch as one literal text replacement to the copy,
     refusing to start if the anchor is not unique;
  3. builds the named fixture from the counter's own green builders
     (`build_green_tree` / `build_green`), so the fixture exercises the same
     code paths the counter measures;
  4. runs the fixture through BOTH the pristine copy and the mutant copy and
     compares the predicate each one prints — `open` for C1, `met` for C2;
  5. prints one row: `killed` when the printed predicate differs (and matches
     the expected direction), `equivalent` only when the patch provably cannot
     move the predicate, with the guarding source line printed.

`run_killers.py --check` prints five rows and `distinguished=5/5`, exit 0.
A `missed` row means the fixture did not separate the copies; exit 1.

Layout: the lane is resolved from `__file__` (`killers/` -> `round-83` ->
`waves` -> `.ufo` -> lane), never from cwd — the round-82 probe scored a whole
mutant run red for the wrong reason because its path resolution moved with the
mutant. Scratch defaults to `/fast/scratch/hyaku/kake-r83/ExecKillers` and is
removed on exit unless `--keep`/`--work` says otherwise. Offline: no socket is
opened; the only subprocesses are `git` inside the fixture fleet and the
counter's own tool under `scripts/`.

`--control` is the negative control for the harness itself: every fixture is run
pristine against pristine (no patch staged), and the suite must read all five
rows `unchanged`. A harness that printed `killed` there would be reading its own
state rather than the patch — the round-82 probe's own failure mode.

Usage: run_killers.py --check [--work DIR] [--journal DIR] [--keep]
       run_killers.py --control [--work DIR] [--journal DIR]
       run_killers.py --list
Exit: 0 all five distinguished (or all five unchanged under --control),
      1 a row missed/moved, 2 setup fault, 64 usage.
"""
from __future__ import annotations

import argparse
import contextlib
import hashlib
import importlib.util
import io
import json
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

HERE = Path(__file__).resolve().parent
LANE = HERE.parents[3]
POPULATION = HERE / "population.json"
PREFERRED_SCRATCH = Path("/fast/scratch/hyaku/kake-r83/ExecKillers")
PREDICATE = {
    "C1": (re.compile(r"\bopen=(\d+)"), "open"),
    "C2": (re.compile(r"\bmet=(true|false)"), "met"),
}
EQUAL_INSTANT = "2026-11-04T12:50:00Z"
DROPPED_SURFACE = "ds4cc-sitemap"
BROKEN_SELFTEST = ("    if args.selftest:\n        return selftest()\n",
                   "    if args.selftest:\n        return 1\n")


class Fault(Exception):
    pass


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def load_population() -> dict:
    try:
        document = json.loads(POPULATION.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError) as exc:
        raise Fault(f"population.json unreadable: {exc}")
    mutants = document.get("mutants")
    if not isinstance(mutants, list) or len(mutants) != 5:
        raise Fault("population.json must carry exactly five mutants")
    for mutant in mutants:
        for key in ("id", "counter", "counter_file", "patch", "fixture", "expect", "verdict"):
            if key not in mutant:
                raise Fault(f"population.json mutant lacks {key!r}")
    return document


def load_module(path: Path, name: str):
    spec = importlib.util.spec_from_file_location(name, path)
    if spec is None or spec.loader is None:
        raise Fault(f"cannot import counter at {path}")
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def stage_counters(population: dict, work: Path) -> dict:
    staged = {}
    for counter, entry in population["frozen_counters"].items():
        source = LANE / entry["file"]
        if not source.is_file():
            raise Fault(f"frozen counter absent: {entry['file']}")
        if sha256(source) != entry["sha256"]:
            raise Fault(f"frozen counter bytes moved: {entry['file']}")
        target = work / "pristine" / f"{counter}.py"
        target.parent.mkdir(parents=True, exist_ok=True)
        target.write_bytes(source.read_bytes())
        staged[counter] = load_module(target, f"pristine_{counter}")
    return staged


def stage_mutant(mutant: dict, work: Path) -> object:
    source = LANE / mutant["counter_file"]
    text = source.read_text(encoding="utf-8")
    old = mutant["patch"]["old"]
    new = mutant["patch"]["new"]
    count = text.count(old)
    if count != 1:
        raise Fault(f"{mutant['id']}: patch anchor occurs {count} times")
    mutated = text.replace(old, new, 1)
    if mutated == text:
        raise Fault(f"{mutant['id']}: patch changed no bytes")
    target = work / "mutants" / mutant["id"] / Path(mutant["counter_file"]).name
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(mutated, encoding="utf-8")
    return load_module(target, f"mutant_{mutant['id'].replace('-', '_')}")


def git(repo: Path, *args: str) -> str:
    proc = subprocess.run(["git", "-C", str(repo), *args], stdout=subprocess.PIPE,
                          stderr=subprocess.PIPE, check=False)
    if proc.returncode != 0:
        detail = proc.stderr.decode("utf-8", "replace").strip()
        raise Fault(f"git {' '.join(args)} failed: {detail}")
    return proc.stdout.decode("utf-8", "replace").strip()


def build_fleet(work: Path, c1) -> tuple[Path, str]:
    """A two-commit fixture repo: the second commit rewrites the filed report."""
    fleet = work / "fleet"
    fleet.mkdir(parents=True)
    git(fleet, "init", "-q")
    resolved = Path(git(fleet, "rev-parse", "--show-toplevel")).resolve()
    if resolved != fleet.resolve():
        raise Fault(f"fixture git toplevel {resolved} != {fleet.resolve()}")
    identity = ["-c", "user.name=fixture", "-c", "user.email=fixture@example.test"]
    report = fleet / c1.FLEET_REPORT
    report.parent.mkdir(parents=True)
    report.write_text("filed report\n", encoding="utf-8")
    git(fleet, "add", c1.FLEET_REPORT)
    git(fleet, *identity, "commit", "-q", "-m", "filed")
    report.write_text("filed report\namended lane-tip line\n", encoding="utf-8")
    git(fleet, "add", c1.FLEET_REPORT)
    git(fleet, *identity, "commit", "-q", "-m", "amended")
    return fleet, git(fleet, "rev-parse", "--short=8", "HEAD")


def c1_fixture(c1, work: Path, name: str, fleet_commit: str, mutant_id: str) -> Path:
    tree = work / "fixtures" / name
    tree.mkdir(parents=True)
    c1.build_green_tree(tree, fleet_commit, c1.LIVE_RECEIPT)
    if mutant_id == "C1-m3":
        record_path = tree / c1.SEAT_RECORD
        record = json.loads(record_path.read_text(encoding="utf-8"))
        changed = 0
        for entry in record["seats"].values():
            if isinstance(entry, dict) and entry.get("role") == "mutation-tester":
                entry["output_bytes"] = 4417
                changed += 1
        if changed != 1:
            raise Fault(f"{mutant_id}: {changed} mutation-tester seats in the fixture record")
        record_path.write_text(json.dumps(record, indent=1), encoding="utf-8")
        lesson_path = tree / c1.LESSON
        text = lesson_path.read_text(encoding="utf-8")
        tokens = text.count("3801")
        if tokens != 1:
            raise Fault(f"{mutant_id}: lesson carries {tokens} 3801 tokens")
        lesson_path.write_text(text.replace("3801", "4417"), encoding="utf-8")
    elif mutant_id == "C1-m5":
        path = tree / c1.LEDGER_RECEIPT
        text = path.read_text(encoding="utf-8")
        tokens = text.count("met=true")
        if tokens != 1:
            raise Fault(f"{mutant_id}: receipt carries {tokens} met=true tokens")
        path.write_text(text.replace("met=true", "met=false"), encoding="utf-8")
    else:
        raise Fault(f"{mutant_id}: no C1 fixture recipe")
    return tree


def regenerate_record(tree: Path, c2) -> None:
    work = tree / "_tool"
    work.mkdir()
    try:
        rc, out = c2.run_tool(tree, work)
    finally:
        shutil.rmtree(work, ignore_errors=True)
    if rc != 0:
        raise Fault(f"tool run on fixture failed rc={rc}")
    (tree / c2.RECORD).write_bytes(out)


def equal_instants(tree: Path, c2) -> None:
    capture = tree / c2.BASE_CAPTURE
    touched = 0
    for leaf in sorted(capture.iterdir()):
        receipt = leaf / "response.json"
        if not receipt.is_file():
            continue
        meta = json.loads(receipt.read_text(encoding="utf-8"))
        meta["fetchedAt"] = EQUAL_INSTANT
        receipt.write_text(json.dumps(meta, indent=1, sort_keys=True), encoding="utf-8")
        touched += 1
    if touched != 3:
        raise Fault(f"equal-instants fixture touched {touched} capture-A receipts, expected 3")
    regenerate_record(tree, c2)


def break_tool_selftest(tree: Path, c2, tool_source: Path) -> None:
    text = tool_source.read_text(encoding="utf-8")
    old, new = BROKEN_SELFTEST
    count = text.count(old)
    if count != 1:
        raise Fault(f"broken-selftest anchor occurs {count} times in {c2.TOOL}")
    (tree / c2.TOOL).write_text(text.replace(old, new, 1), encoding="utf-8")
    work = tree / "_tool"
    work.mkdir()
    try:
        rc, out = c2.run_tool(tree, work)
    finally:
        shutil.rmtree(work, ignore_errors=True)
    record = (tree / c2.RECORD).read_bytes()
    if rc != 0 or out.rstrip(b"\n") != record.rstrip(b"\n"):
        raise Fault("broken-selftest tool no longer re-derives the committed record")


def drop_a_surface(tree: Path, c2) -> None:
    capture = tree / c2.BASE_CAPTURE
    leaf = capture / DROPPED_SURFACE
    if not (leaf / "response.json").is_file():
        raise Fault(f"dropped-surface fixture: {DROPPED_SURFACE} absent from capture A")
    shutil.rmtree(leaf)
    manifest_path = capture / "manifest.json"
    manifest = json.loads(manifest_path.read_text(encoding="utf-8"))
    before = len(manifest["checks"])
    manifest["checks"] = [check for check in manifest["checks"]
                          if not (isinstance(check, dict)
                                  and check.get("id") == DROPPED_SURFACE)]
    if before != 3 or len(manifest["checks"]) != 2:
        raise Fault("dropped-surface fixture: manifest check count moved unexpectedly")
    manifest_path.write_text(json.dumps(manifest, indent=1, sort_keys=True), encoding="utf-8")
    regenerate_record(tree, c2)


def c2_fixture(c2, work: Path, name: str, mutant_id: str, tool_source: Path) -> Path:
    tree = work / "fixtures" / name
    tree.mkdir(parents=True)
    c2.build_green(tree, tool_source)
    if mutant_id == "C2-m2":
        equal_instants(tree, c2)
    elif mutant_id == "C2-m4":
        break_tool_selftest(tree, c2, tool_source)
    elif mutant_id == "C2-m5":
        drop_a_surface(tree, c2)
    else:
        raise Fault(f"{mutant_id}: no C2 fixture recipe")
    return tree


def invoke(module, counter: str, tree: Path, work: Path, fleet: Path) -> dict:
    work.mkdir(parents=True, exist_ok=True)
    for sub in ("run1", "run2", "selftest"):
        (work / sub).mkdir(exist_ok=True)
    buffer = io.StringIO()
    with contextlib.redirect_stdout(buffer):
        if counter == "C1":
            rc = module.run(tree, None, work, fleet)
        else:
            rc = module.run(tree, None, work)
    text = buffer.getvalue()
    pattern, label = PREDICATE[counter]
    match = pattern.search(text)
    if match is None:
        raise Fault(f"{counter} printed no {label}= predicate: {text[-200:]!r}")
    return {"rc": rc, "text": text, "predicate": f"{label}={match.group(1)}"}


def guard_line(work: Path, mutant: dict) -> str:
    guard = mutant.get("guard")
    if not isinstance(guard, dict):
        raise Fault(f"{mutant['id']}: equivalent verdict without a guard block")
    lines = (LANE / guard["file"]).read_text(encoding="utf-8").splitlines()

    def resolve(number, needle: str, label: str) -> str:
        if not 1 <= int(number) <= len(lines):
            raise Fault(f"{mutant['id']}: {label} line {number} is out of range")
        line = lines[int(number) - 1]
        if needle not in line:
            raise Fault(f"{mutant['id']}: {label} line {number} lacks {needle!r}")
        return f"{guard['file']}:{number}:{line.strip()}"

    guards = [resolve(guard["line"], guard["contains"], "guard")]
    if guard.get("also_line"):
        guards.append(resolve(guard["also_line"], guard["also_contains"], "co-guard"))
    staged = (work / "mutants" / mutant["id"]
              / Path(mutant["counter_file"]).name).read_text(encoding="utf-8")
    for needle in (guard["contains"], guard.get("also_contains")):
        if needle and needle not in staged:
            raise Fault(f"{mutant['id']}: the mutant copy lost the guard {needle!r}")
    return "; ".join(guards)


def check(work: Path, journal: Path | None, control: bool = False) -> int:
    population = load_population()
    tool_entry = population.get("tool") or {}
    tool_source = LANE / str(tool_entry.get("file", "scripts/capture_delta.py"))
    if not tool_source.is_file():
        raise Fault(f"capture tool absent: {tool_source}")
    expected_tool = tool_entry.get("sha256")
    if expected_tool and sha256(tool_source) != expected_tool:
        raise Fault("scripts/capture_delta.py moved since population.json was written")

    pristine = stage_counters(population, work)
    fleet, fleet_commit = build_fleet(work, pristine["C1"])

    lines: list[str] = []
    rows: list[dict] = []
    for mutant in population["mutants"]:
        mid = mutant["id"]
        counter = mutant["counter"]
        try:
            module = pristine[counter]
            fixture = mutant["fixture"]
            if counter == "C1":
                tree = c1_fixture(module, work, fixture, fleet_commit, mid)
            else:
                tree = c2_fixture(module, work, fixture, mid, tool_source)
            mutant_module = module if control else stage_mutant(mutant, work)
            left = invoke(module, counter, tree, work / "runs" / mid / "pristine", fleet)
            right = invoke(mutant_module, counter, tree, work / "runs" / mid / "mutant", fleet)
            if control:
                verdict = "unchanged" if left["predicate"] == right["predicate"] else "moved"
                detail = (f"fixture={fixture} pristine={left['predicate']} "
                          f"pristine_again={right['predicate']}")
                lines.append(f"{mid} control {verdict} {detail}")
                rows.append({"id": mid, "verdict": verdict,
                             "left": left["text"], "right": right["text"]})
                continue
            expect = mutant["expect"]
            matched = (left["predicate"] == expect["pristine"]
                       and right["predicate"] == expect["mutant"])
            differs = left["predicate"] != right["predicate"]
            if differs and matched:
                verdict = "killed"
            elif not differs and matched and mutant.get("verdict") == "equivalent":
                verdict = "equivalent"
            else:
                verdict = "missed"
            detail = (f"fixture={fixture} "
                      f"counter={mutant['counter_file']}:{mutant['line']} "
                      f"pristine={left['predicate']} mutant={right['predicate']}")
            if verdict == "killed":
                old = " ".join(mutant["patch"]["old"].split())
                new = " ".join(mutant["patch"]["new"].split())
                detail += f" patch=[{old}]->[{new}]"
            elif verdict == "equivalent":
                detail += f" guard={guard_line(work, mutant)} proof={mutant['guard']['proof']}"
            else:
                detail += (f" expected pristine={expect['pristine']} "
                           f"mutant={expect['mutant']}")
            lines.append(f"{mid} {verdict} {detail}")
            rows.append({"id": mid, "verdict": verdict,
                         "left": left["text"], "right": right["text"]})
        except Exception as exc:  # one broken fixture must not hide the other four
            lines.append(f"{mid} missed fixture={mutant.get('fixture')} "
                         f"reason={type(exc).__name__}: {exc}")
            rows.append({"id": mid, "verdict": "missed", "left": "", "right": ""})

    if journal is not None:
        directory = Path(journal)
        directory.mkdir(parents=True, exist_ok=True)
        for row in rows:
            (directory / f"{row['id']}.pristine.txt").write_text(row["left"], encoding="utf-8")
            (directory / f"{row['id']}.mutant.txt").write_text(row["right"], encoding="utf-8")
        (directory / "rows.txt").write_text("\n".join(lines) + "\n", encoding="utf-8")

    for line in lines:
        print(line)
    total = len(population["mutants"])
    if control:
        unchanged = sum(1 for row in rows if row["verdict"] == "unchanged")
        print(f"control={unchanged}/{total} unchanged")
        return 0 if unchanged == total else 1
    distinguished = sum(1 for row in rows if row["verdict"] in ("killed", "equivalent"))
    print(f"distinguished={distinguished}/{total}")
    return 0 if distinguished == total else 1


def make_work(explicit: str | None) -> tuple[Path, bool]:
    if explicit:
        path = Path(explicit)
        path.mkdir(parents=True, exist_ok=True)
        return path, False
    try:
        PREFERRED_SCRATCH.mkdir(parents=True, exist_ok=True)
        return Path(tempfile.mkdtemp(prefix="run-", dir=str(PREFERRED_SCRATCH))), True
    except OSError:
        return Path(tempfile.mkdtemp(prefix="kake83-killers-")), True


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--check", action="store_true",
                        help="run all five mutants and print the verdict rows")
    parser.add_argument("--control", action="store_true",
                        help="negative control: every fixture pristine against pristine")
    parser.add_argument("--list", action="store_true", help="print the population table")
    parser.add_argument("--work", help="scratch directory (default: under /fast/scratch)")
    parser.add_argument("--journal", help="write each counter's printed text here")
    parser.add_argument("--keep", action="store_true", help="retain the default scratch dir")
    args = parser.parse_args(argv)
    if args.list:
        for mutant in load_population()["mutants"]:
            print(f"{mutant['id']} counter={mutant['counter']} "
                  f"fixture={mutant['fixture']} verdict={mutant['verdict']} "
                  f"change={mutant['change']}")
        return 0
    if not args.check and not args.control:
        parser.print_usage(sys.stderr)
        return 64
    work, owned = make_work(args.work)
    print(f"# work={work}", file=sys.stderr)
    try:
        return check(work, Path(args.journal) if args.journal else None,
                     control=args.control)
    except Fault as exc:
        print(f"fault {exc}", file=sys.stderr)
        return 2
    finally:
        if owned and not args.keep:
            shutil.rmtree(work, ignore_errors=True)


if __name__ == "__main__":
    raise SystemExit(main())
