#!/usr/bin/env python3
"""Independent re-implementation of the six round-80 C1 predicates (kake, calibration).

Written by seat ExecQueue (wave w1) straight from the frozen contract
`.ufo/waves/round-80/contract.md` §C1 "Per-item closure conditions". No import
from, and no code shared with, `.ufo/waves/round-80/c80_defect_queue.py`; every
predicate below is my own reading of the contract sentence, used to cross-check
the shipped counter. Where my contract-literal reading diverges from the
counter, the divergence is reported in `.ufo/waves/round-80/w1/ExecQueue.md`.

Usage: python3 -B indep_queue.py --root <lane> [--revision <rev>] [--work <scratch>]
Exit: 0 met, 1 not met, 64 usage. Read-only outside --work.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
import sys
from pathlib import Path

ITEMS = ["R79-1", "R79-2", "R79-3", "R79-4", "R79-5", "R79-8"]

# Union of the paths the six predicates read (the contract's closure surfaces).
EXPORT_PATHS = [
    "corpus/SOURCES.md",
    "corpus/QUALITY.md",
    "corpus/lessons/round-80.md",
    "scripts/ledger_append_guard.py",
    "scripts/x_robots_tag_audit.py",
    ".ufo/waves/round-80/controls/c80-selftest.txt",
    ".ufo/waves/round-80/controls/c80-cheap-note.txt",
    ".ufo/waves/round-80/c80_ledger_fixtures.py",
    ".ufo/waves/round-80/defect-queue.json",
    ".ufo/waves/round-79/w1-results.json",
    "SCORECARD.md",
    "SKILL.md",
    "LOG.md",
    "PROVINCE.md",
    "corpus/README.md",
]

# Contract R79-5: "no lane self-assessment file (SCORECARD.md, SKILL.md, LOG.md,
# PROVINCE.md, corpus/README.md, corpus/knowledge/**) repeats it".
SELF_ASSESSMENT = ["SCORECARD.md", "SKILL.md", "LOG.md", "PROVINCE.md", "corpus/README.md"]

# The sentence R79-5 withdraws, per corpus/lessons/round-79-verifier-spotcheck.md §6 item 5
# and the round-79 report (`.ufo/reports/round-79/kake.md:29`).
WITHDRAWN_SENTENCE = "passed 31/31 before the tool existed"

WITHDRAWAL_VERB = re.compile(r"withdraw|retract|dropped?|recant|repudiat|supersed", re.I)
ERRATUM_VERB = re.compile(r"erratum|never written|was false|incorrect|wrong|withdraw|retract|correct", re.I)


def read(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return ""


def run(argv: list[str], cwd: Path, timeout: int = 240) -> tuple[int, str, str]:
    p = subprocess.run(argv, cwd=str(cwd), capture_output=True, text=True, timeout=timeout)
    return p.returncode, p.stdout, p.stderr


def sha256(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def materialise(root: Path, revision: str, work: Path) -> Path:
    """Export every path this script reads from `revision` into `work/tree`."""
    tree = work / "tree"
    tree.mkdir(parents=True, exist_ok=True)
    paths = list(EXPORT_PATHS)
    listing = subprocess.run(["git", "-C", str(root), "ls-tree", "-r", "--name-only", revision,
                              "--", "corpus/knowledge"], capture_output=True, text=True)
    if listing.returncode == 0:
        paths += [p for p in listing.stdout.splitlines() if p.endswith(".md")]
    for rel in paths:
        show = subprocess.run(["git", "-C", str(root), "show", f"{revision}:{rel}"],
                              capture_output=True)
        if show.returncode != 0:
            continue
        dst = tree / rel
        dst.parent.mkdir(parents=True, exist_ok=True)
        dst.write_bytes(show.stdout)
    return tree


def p_r79_1(tree: Path) -> tuple[bool, str]:
    """Contract: SOURCES.md carries an S453 row whose `source` cites RFC 9110 and not
    RFC 9309, AND corpus/lessons/round-80.md records the erratum naming R79-1, the
    withdrawn sentence's subject and S453."""
    reg = read(tree / "corpus/SOURCES.md")
    row = None
    for line in reg.splitlines():
        if not line.lstrip().startswith("|"):
            continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if cells and cells[0] == "S453":
            row = cells
            break
    if row is None:
        return False, "no S453 row in corpus/SOURCES.md"
    src = (row[1] if len(row) > 1 else "").lower()
    if "rfc 9110" not in src and "rfc9110" not in src:
        return False, f"S453 source cell does not cite RFC 9110: {row[1][:60]!r}"
    if "9309" in src:
        return False, "S453 source cell still cites RFC 9309"
    lesson = read(tree / "corpus/lessons/round-80.md")
    if "R79-1" not in lesson:
        return False, "round-80 lesson names no R79-1"
    if "S453" not in lesson:
        return False, "round-80 lesson names no S453"
    subject = re.search(r"rejected\s+(row|S453)|S453[^.\n]{0,80}rejected|rejected[^.\n]{0,80}S453",
                        lesson, re.I)
    if not subject:
        return False, "round-80 lesson names not the withdrawn sentence's subject (the kept rejected S453 row)"
    if not ERRATUM_VERB.search(lesson):
        return False, "round-80 lesson records no erratum/correction semantics"
    return True, "S453 row cites RFC 9110 (not 9309); lesson erratum names R79-1, the rejected-row subject and S453"


def p_r79_2(tree: Path, work: Path) -> tuple[bool, str]:
    """Contract: scripts/ledger_append_guard.py exists, its --selftest exits 0 and prints
    one non-prefix append fixture as failed, and its run over the lane reports the
    receipt ledger's byte prefix preserved."""
    guard = tree / "scripts/ledger_append_guard.py"
    if not guard.exists():
        return False, "scripts/ledger_append_guard.py absent"
    rc, out, err = run([sys.executable, "-B", str(guard), "--selftest"], work)
    if rc != 0:
        return False, f"guard --selftest rc={rc}: {(out + err).strip().splitlines()[-1:] or ''}"
    failed_nonprefix = [ln for ln in out.splitlines()
                        if re.search(r"non[-_ ]?prefix", ln, re.I) and re.search(r"fail", ln, re.I)]
    if not failed_nonprefix:
        return False, "guard --selftest prints no non-prefix append fixture as failed"
    rc2, out2, err2 = run([sys.executable, "-B", str(guard), "--root", str(tree), "--json"], work)
    try:
        doc = json.loads(out2)
    except json.JSONDecodeError:
        return False, f"guard --json unparseable rc={rc2}: {err2.strip()[:120]}"
    if not doc.get("prefix_preserved"):
        return False, f"guard reports prefix_preserved={doc.get('prefix_preserved')} (run rc={rc2})"
    if int(doc.get("files") or 0) < 1:
        return False, f"guard run covered files={doc.get('files')}"
    return True, (f"guard selftest exits 0 with a failed non-prefix fixture; run over the lane "
                  f"prefix_preserved={doc.get('prefix_preserved')} files={doc.get('files')} (run rc={rc2})")


def p_r79_3(tree: Path, work: Path) -> tuple[bool, str]:
    """Contract: controls/c80-selftest.txt holds a `selftest: N/N passed` line and `exit=0`,
    and re-running the tool's --selftest at the measured revision prints the identical line.
    (Contract text does not require the re-run itself to exit 0; recorded in the detail.)"""
    receipt = read(tree / ".ufo/waves/round-80/controls/c80-selftest.txt")
    m = re.search(r"^(selftest: \d+/\d+ passed)$", receipt, re.M)
    if not m:
        return False, "receipt c80-selftest.txt holds no `selftest: N/N passed` line"
    if "exit=0" not in receipt:
        return False, "receipt c80-selftest.txt carries no `exit=0`"
    tool = tree / "scripts/x_robots_tag_audit.py"
    if not tool.exists():
        return False, "scripts/x_robots_tag_audit.py absent in measured tree"
    rc, out, err = run([sys.executable, "-B", str(tool), "--selftest"], work)
    lines = [ln for ln in out.splitlines() if ln.startswith("selftest: ")]
    if not lines:
        return False, f"tool --selftest prints no selftest line rc={rc}: {err.strip()[:120]}"
    if lines[-1] != m.group(1):
        return False, f"receipt `{m.group(1)}` != re-run `{lines[-1]}`"
    return True, f"receipt `{m.group(1)}` == re-run line (re-run rc={rc})"


def _walk(obj):
    if isinstance(obj, dict):
        yield obj
        for v in obj.values():
            yield from _walk(v)
    elif isinstance(obj, list):
        for v in obj:
            yield from _walk(v)


def p_r79_4(tree: Path, work: Path) -> tuple[bool, str]:
    """Contract: c80_ledger_fixtures.py --root <tree> --json reports killed == 3 with the
    three survivors isolated (k3 wrong_kind, k4 cheap-note, k5 symlinks), the cheap-note
    fixture red through undisclosed == 1; controls/c80-cheap-note.txt records that run;
    corpus/QUALITY.md carries a criterion clause naming R79-4 with undisclosed=1."""
    harness = tree / ".ufo/waves/round-80/c80_ledger_fixtures.py"
    if not harness.exists():
        return False, ".ufo/waves/round-80/c80_ledger_fixtures.py absent"
    rc, out, err = run([sys.executable, "-B", str(harness), "--root", str(tree), "--json"], work)
    try:
        doc = json.loads(out)
    except json.JSONDecodeError:
        return False, f"fixture harness unparseable rc={rc}: {(out + err).strip()[-160:]}"
    if int(doc.get("killed") or 0) != 3:
        return False, f"fixture harness killed={doc.get('killed')}"
    blob = json.dumps(doc)
    survivors = {"wrong_kind": re.search(r"wrong_?kind", blob, re.I),
                 "cheap-note": re.search(r"cheap[-_ ]?note", blob, re.I),
                 "symlinks": re.search(r"symlinks?", blob, re.I)}
    missing = [k for k, v in survivors.items() if not v]
    if missing:
        return False, f"harness output isolates no survivor(s) {missing}"
    cheap_red = any(int(d.get("undisclosed") or 0) == 1
                    and (d.get("ledger_red") is True or d.get("red") is True)
                    for d in _walk(doc))
    if not cheap_red:
        return False, "no fixture reports undisclosed == 1 while red"
    receipt = read(tree / ".ufo/waves/round-80/controls/c80-cheap-note.txt")
    if not receipt:
        return False, "controls/c80-cheap-note.txt absent"
    if "cheap-note" not in receipt or "undisclosed=1" not in receipt:
        return False, "c80-cheap-note.txt records not the cheap-note undisclosed=1 run"
    quality = read(tree / "corpus/QUALITY.md")
    if "R79-4" not in quality or "undisclosed=1" not in quality:
        return False, "QUALITY.md carries no criterion clause naming R79-4 with undisclosed=1"
    return True, "killed==3; survivors wrong_kind/cheap-note/symlinks isolated; cheap-note red via undisclosed=1; receipt + QUALITY clause present"


def p_r79_5(tree: Path) -> tuple[bool, str]:
    """Contract: corpus/lessons/round-80.md withdraws the sentence in a row naming R79-5,
    and no lane self-assessment file repeats it."""
    lesson = read(tree / "corpus/lessons/round-80.md")
    rows = [ln for ln in lesson.splitlines()
            if "R79-5" in ln and WITHDRAWN_SENTENCE in ln and WITHDRAWAL_VERB.search(ln)]
    if not rows:
        return False, "round-80 lesson carries no R79-5 row withdrawing the sentence"
    hits = []
    for rel in SELF_ASSESSMENT:
        if WITHDRAWN_SENTENCE in read(tree / rel):
            hits.append(rel)
    for path in sorted((tree / "corpus/knowledge").rglob("*.md")):
        if WITHDRAWN_SENTENCE in read(path):
            hits.append(str(path.relative_to(tree)))
    if hits:
        return False, f"withdrawn sentence still asserted in: {', '.join(hits[:4])}"
    return True, "R79-5 withdrawal row present; no self-assessment file repeats the sentence"


def p_r79_8(tree: Path) -> tuple[bool, str]:
    """Contract: defect-queue.json records every round-79 seat whose output was empty, with
    output_bytes and output_sha256 re-derived from .ufo/waves/round-79/w1-results.json.
    ("empty" read literally: output == "", zero bytes.)"""
    try:
        results = json.loads(read(tree / ".ufo/waves/round-79/w1-results.json"))["results"]
    except (json.JSONDecodeError, KeyError, TypeError) as exc:
        return False, f"round-79 results unreadable: {exc}"
    empty = [(i, r.get("name"), r.get("output")) for i, r in enumerate(results)
             if r.get("output") == ""]
    try:
        record = json.loads(read(tree / ".ufo/waves/round-80/defect-queue.json"))["seats"]
    except (json.JSONDecodeError, KeyError, TypeError):
        return False, "defect-queue.json absent or malformed"
    for i, name, output in empty:
        entry = record.get(name)
        if not isinstance(entry, dict):
            return False, f"defect-queue.json has no entry for {name} (results index {i})"
        if entry.get("output_bytes") != 0:
            return False, f"{name}: output_bytes {entry.get('output_bytes')} != 0"
        if entry.get("output_sha256") != sha256(output or ""):
            return False, f"{name}: output_sha256 mismatch"
    extra = [n for n in record if n not in {name for _, name, _ in empty}]
    detail = f"{len(empty)} empty-output seats recorded with re-derived bytes ({', '.join(n for _, n, _ in empty)})"
    if extra:
        detail += f"; extra entries present: {extra}"
    return True, detail


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--root", default=".")
    ap.add_argument("--revision")
    ap.add_argument("--work", required=True)
    a = ap.parse_args()
    root = Path(a.root).resolve()
    work = Path(a.work).resolve()
    work.mkdir(parents=True, exist_ok=True)
    if a.revision:
        tree = materialise(root, a.revision, work)
        label = a.revision
    else:
        tree, label = root, "worktree"
    verdicts = {
        "R79-1": p_r79_1(tree),
        "R79-2": p_r79_2(tree, work),
        "R79-3": p_r79_3(tree, work),
        "R79-4": p_r79_4(tree, work),
        "R79-5": p_r79_5(tree),
        "R79-8": p_r79_8(tree),
    }
    open_items = [i for i in ITEMS if not verdicts[i][0]]
    for item in ITEMS:
        ok, detail = verdicts[item]
        print(f"{item} {'closed' if ok else 'open'} {detail}")
    met = not open_items
    print(f"INQC1v1 revision={label} items=6 open={len(open_items)} "
          f"closed={6 - len(open_items)} met={'true' if met else 'false'}")
    return 0 if met else 1


if __name__ == "__main__":
    sys.exit(main())
