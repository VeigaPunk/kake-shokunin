#!/usr/bin/env python3
"""Round-51 quote-truth counter — the C2 counter (freshness, assimilation).

What it is: a re-derivation of one assimilated theme over committed bytes only. It
reads `git show <revision>:<path>` and `git log`; it opens no worktree file of the
measured revision and performs no network access.

What its contract is: eight conditions over the theme the round assimilated from the
`shokuknow` package — the Google's canonical-selection and crawler-identity ground,
grounded on rows S262 and S263:

  C1 the two admitted knowledge entries exist at their repo-relative paths.
  C2 each entry cites its own row id below its metadata header.
  C3 each registry row is well formed (11 cells, no literal or escaped pipe, status
     `mined`, the round's opened date, a normalized recheck).
  C4 each registry row's `used-by` lists exactly the admitted entries that cite it.
  C5 each row's lesson Gate quote is 6 to 25 words and an exact RAW substring of the
     retained source body the round itself fetched.
  C6 each retained body's sha256 equals its receipt's sha256 and its receipt URL
     equals the registry row's URL.
  C7 the pre-append mirror was census-validated with `--file` before the append:
     the argv names the mirror path and not `--root`, the exit is 0 and the stdout
     carries no E03 and no E04.
  C8 the pre-append mirror commit is a strict ancestor of the measured revision, the
     registry at that mirror carries none of the adopted ids and the registry at the
     measured revision carries all of them.

Predicate (frozen in `.ufo/waves/round-51/contract.json` before any data):

    met: conditions_passed == 8 of 8

Exit codes: 0 the predicate is met, 1 it is not, 2 the evidence cannot be evaluated,
64 usage error.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
import sys

PREDICATE = "met: conditions_passed == 8 of 8"

ROUND_DATE = "2026-10-24"
REGISTRY = "corpus/SOURCES.md"
LESSON = "corpus/lessons/round-51.md"
SOURCES_DIR = ".ufo/waves/round-51/sources"
RECEIPTS = f"{SOURCES_DIR}/receipts.json"
MIRROR = ".ufo/waves/round-51/assimilation/pre-append/corpus/SOURCES.md"
CENSUS_DIR = ".ufo/waves/round-51/assimilation/pre-append"

# The theme: id -> (entry path, retained body path)
ADOPTED = {
    "S262": "corpus/knowledge/canonical-selection.md",
    "S263": "corpus/knowledge/crawler-identity.md",
}


def git(root: str, *args: str) -> tuple[int, str]:
    proc = subprocess.run(
        ["git", "-C", root, *args],
        stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True,
    )
    return proc.returncode, proc.stdout


def show(root: str, rev: str, path: str) -> str | None:
    rc, out = git(root, "show", f"{rev}:{path}")
    return out if rc == 0 else None


def show_bytes(root: str, rev: str, path: str) -> bytes | None:
    proc = subprocess.run(
        ["git", "-C", root, "show", f"{rev}:{path}"],
        stdout=subprocess.PIPE, stderr=subprocess.PIPE,
    )
    return proc.stdout if proc.returncode == 0 else None


def parse_registry(text: str) -> dict[str, list[str]]:
    """Parse the registry table the way the census parser does: 0 to 3 leading spaces."""
    rows: dict[str, list[str]] = {}
    in_registry = False
    for line in text.splitlines():
        if line.strip().startswith("## "):
            in_registry = line.strip().lower().startswith("## registry")
            continue
        if not in_registry:
            continue
        if not re.match(r"^ {0,3}\|", line):
            continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if len(cells) < 2:
            continue
        if not re.fullmatch(r"S[0-9]{3,}", cells[0]):
            continue
        rows[cells[0]] = cells
    return rows


def gate_quote(lesson: str, sid: str) -> str | None:
    in_gate = False
    for line in lesson.splitlines():
        if line.strip().startswith("## "):
            in_gate = line.strip().lower() == "## gate"
            continue
        if not in_gate:
            continue
        if not line.strip().startswith(f"- {sid} "):
            continue
        quotes = re.findall(r'"([^"]+)"', line)
        if not quotes:
            return None
        return quotes[-1]
    return None


def main() -> int:
    parser = argparse.ArgumentParser(description="Round-51 quote-truth counter (C2)")
    parser.add_argument("--root", required=True)
    parser.add_argument("--revision", required=True)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    root, rev = args.root, args.revision

    checks: dict[str, dict] = {}
    notes: list[str] = []

    registry_text = show(root, rev, REGISTRY)
    rows = parse_registry(registry_text) if registry_text else {}
    lesson_text = show(root, rev, LESSON)

    # C1 entries exist
    entries = {}
    for sid, path in ADOPTED.items():
        body = show(root, rev, path)
        entries[sid] = body
        if body is None:
            notes.append(f"{sid}: knowledge entry {path} absent at the measured revision")
    checks["C1_entries_exist"] = {"passed": not notes, "notes": list(notes)}

    # C2 each entry cites its id below the metadata header
    c2_notes = []
    for sid, path in ADOPTED.items():
        body = entries.get(sid)
        if body is None:
            c2_notes.append(f"{sid}: entry absent")
            continue
        lines = body.splitlines()
        header = len(lines[:8])
        if not any(re.search(rf"\b{sid}\b", line) for line in lines[header:]):
            c2_notes.append(f"{sid}: entry does not cite its id below the 8-line header")
    checks["C2_entry_cites_id"] = {"passed": not c2_notes, "notes": c2_notes}

    # C3 registry row shape
    c3_notes = []
    for sid in ADOPTED:
        row = rows.get(sid)
        if row is None:
            c3_notes.append(f"{sid}: no registry row at the measured revision")
            continue
        if len(row) != 11:
            c3_notes.append(f"{sid}: registry row has {len(row)} cells, expected 11")
        if any("\\|" in cell for cell in row):
            c3_notes.append(f"{sid}: registry row carries an escaped pipe")
        if len(row) >= 8 and row[7] != "mined":
            c3_notes.append(f"{sid}: registry status is {row[7]!r}, expected 'mined'")
        if len(row) >= 9 and row[8] != ROUND_DATE:
            c3_notes.append(f"{sid}: registry opened is {row[8]!r}, expected {ROUND_DATE!r}")
        if len(row) >= 10 and not re.fullmatch(
            r"(\d{4}-\d{2}-\d{2}|\d+d|on-release)", row[9]
        ):
            c3_notes.append(
                f"{sid}: registry recheck is {row[9]!r}, expected a normalized "
                "ISO date, NNd cadence or on-release"
            )
    checks["C3_row_shape"] = {"passed": not c3_notes, "notes": c3_notes}

    # C4 used-by lists exactly the citing entries
    c4_notes = []
    for sid, path in ADOPTED.items():
        row = rows.get(sid)
        if row is None or len(row) < 11:
            c4_notes.append(f"{sid}: no usable registry row")
            continue
        used_by = [p.strip() for p in row[10].split(",") if p.strip()]
        if used_by != [path]:
            c4_notes.append(f"{sid}: used-by is {used_by!r}, expected exactly [{path!r}]")
    checks["C4_used_by"] = {"passed": not c4_notes, "notes": c4_notes}

    # C5 gate quote is 6-25 words and a raw substring of the retained body
    c5_notes = []
    bodies = {}
    for sid in ADOPTED:
        body_path = f"{SOURCES_DIR}/{sid}.html"
        raw = show_bytes(root, rev, body_path)
        bodies[sid] = raw
        if raw is None:
            c5_notes.append(f"{sid}: retained body {body_path} absent")
            continue
        if lesson_text is None:
            c5_notes.append(f"{sid}: lesson {LESSON} absent")
            continue
        quote = gate_quote(lesson_text, sid)
        if quote is None:
            c5_notes.append(f"{sid}: no ## Gate quote found in the lesson")
            continue
        words = len(quote.split())
        if not 6 <= words <= 25:
            c5_notes.append(f"{sid}: Gate quote is {words} words, expected 6 to 25")
        try:
            text = raw.decode("utf-8")
        except UnicodeDecodeError:
            c5_notes.append(f"{sid}: retained body is not UTF-8")
            continue
        if quote not in text:
            c5_notes.append(f"{sid}: Gate quote is not a raw substring of the retained body")
    checks["C5_gate_quote_truth"] = {"passed": not c5_notes, "notes": c5_notes}

    # C6 receipt sha256 and URL agree with the bytes and the row
    c6_notes = []
    receipts_text = show(root, rev, RECEIPTS)
    receipts = json.loads(receipts_text) if receipts_text else {}
    if isinstance(receipts.get("sources"), dict):
        receipts = receipts["sources"]
    for sid in ADOPTED:
        receipt = receipts.get(sid)
        raw = bodies.get(sid)
        if receipt is None:
            c6_notes.append(f"{sid}: no receipt in {RECEIPTS}")
            continue
        if raw is None:
            c6_notes.append(f"{sid}: no retained body to hash")
            continue
        digest = hashlib.sha256(raw).hexdigest()
        if receipt.get("sha256") != digest:
            c6_notes.append(f"{sid}: receipt sha256 {receipt.get('sha256')} != body {digest}")
        row = rows.get(sid)
        if row and len(row) >= 2:
            if receipt.get("url") not in row[1]:
                c6_notes.append(f"{sid}: receipt URL is not the registry row's URL")
    checks["C6_receipt_pins"] = {"passed": not c6_notes, "notes": c6_notes}

    # C7 pre-append mirror census receipt
    c7_notes = []
    argv = show(root, rev, f"{CENSUS_DIR}/census-argv.txt")
    stdout = show(root, rev, f"{CENSUS_DIR}/census-stdout.txt")
    exit_text = show(root, rev, f"{CENSUS_DIR}/census-exit.txt")
    if argv is None or stdout is None or exit_text is None:
        c7_notes.append("pre-append census receipt is incomplete")
    else:
        if "--file" not in argv:
            c7_notes.append("pre-append census argv does not use --file")
        if "--root" in argv:
            c7_notes.append("pre-append census argv names --root, not a single file")
        if MIRROR not in argv:
            c7_notes.append("pre-append census argv does not name the mirror path")
        if exit_text.strip() != "0":
            c7_notes.append(f"pre-append census exit is {exit_text.strip()!r}, expected '0'")
        if "E03" in stdout or "E04" in stdout:
            c7_notes.append("pre-append census stdout carries an E03/E04 finding")
    checks["C7_validate_before_append"] = {"passed": not c7_notes, "notes": c7_notes}

    # C8 the mirror commit is a strict ancestor and the append came after it
    c8_notes = []
    rc, out = git(root, "log", "--diff-filter=A", "--format=%H", rev, "--", MIRROR)
    mirror_commits = [line.strip() for line in out.splitlines() if line.strip()]
    if not mirror_commits:
        c8_notes.append("no commit adds the pre-append mirror")
    else:
        mirror_commit = mirror_commits[-1]
        rc_anc, _ = git(root, "merge-base", "--is-ancestor", mirror_commit, rev)
        if rc_anc != 0:
            c8_notes.append(f"mirror commit {mirror_commit} is not an ancestor of {rev}")
        mirror_registry = show(root, mirror_commit, REGISTRY)
        mirror_rows = parse_registry(mirror_registry) if mirror_registry else {}
        for sid in ADOPTED:
            if sid in mirror_rows:
                c8_notes.append(f"{sid}: the mirror already carries the row")
            if sid not in rows:
                c8_notes.append(f"{sid}: the measured revision does not carry the row")
    checks["C8_append_after_mirror"] = {"passed": not c8_notes, "notes": c8_notes}

    passed = sum(1 for entry in checks.values() if entry["passed"])
    report = {
        "schema": "kake-r51-c2-quote-truth-v1",
        "predicate": PREDICATE,
        "revision": rev,
        "round_date": ROUND_DATE,
        "adopted": {sid: ADOPTED[sid] for sid in ADOPTED},
        "checks": checks,
        "conditions_passed": passed,
        "met": passed == 8,
    }
    if args.json:
        print(json.dumps(report, indent=2, ensure_ascii=False))
    else:
        print(f"C2 quote-truth {passed}/8 met={passed == 8}  ({PREDICATE})")
        for name, entry in checks.items():
            state = "pass" if entry["passed"] else "FAIL"
            print(f"  {name} {state}")
            for note in entry["notes"]:
                print(f"    - {note}")
        print(f"  revision: {rev}")
    return 0 if passed == 8 else 1


if __name__ == "__main__":
    sys.exit(main())
