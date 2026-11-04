#!/usr/bin/env python3
"""Round-80 C1 counter — the round-79 routed-defect queue (kake, calibration).

Population (frozen in `.ufo/waves/round-80/contract.md`): the six report/receipt-accuracy items the
non-author round-79 closure filed in `corpus/lessons/round-79-verifier-spotcheck.md` §6 —
R79-1, R79-2, R79-3, R79-4, R79-5, R79-8. The two medium work items (R79-6, R79-7) are C2's.

Frozen predicate (contract §C1):

    met <=> open == 0 for the six items R79-1, R79-2, R79-3, R79-4, R79-5, R79-8

Every item is decided from bytes, never from a token that merely says "closed": a receipt must agree
with a re-run, a registry row must exist with its own source, a guard must be shown able to fail.
Exit: 0 met, 1 not met, 2 unevaluable, 64 usage. Read-only outside --work.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

ITEMS = ["R79-1", "R79-2", "R79-3", "R79-4", "R79-5", "R79-8"]

EXPORT_PATHS = [
    "corpus/SOURCES.md", "corpus/QUALITY.md", "corpus/README.md",
    "corpus/lessons/round-79.md", "corpus/lessons/round-80.md",
    "scripts/ledger_append_guard.py", "scripts/x_robots_tag_audit.py",
    ".ufo/waves/round-80/controls/c80-selftest.txt",
    ".ufo/waves/round-80/controls/c80-cheap-note.txt",
    ".ufo/waves/round-80/c80_ledger_fixtures.py",
    ".ufo/waves/round-80/defect-queue.json",
    ".ufo/waves/round-79/w1-results.json",
    "SCORECARD.md", "SKILL.md", "LOG.md", "PROVINCE.md",
]
SELF_ASSESSMENT = ["SCORECARD.md", "SKILL.md", "LOG.md", "PROVINCE.md", "corpus/README.md"]
WITHDRAWN = "passed 31/31 before the tool existed"


def sha256(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def materialise(root: Path, revision: str, work: Path) -> tuple[Path, list[str], list[str]]:
    """Export the paths this counter reads from `revision` into `work/tree`; return it and notes."""
    tree = work / "tree"
    tree.mkdir(parents=True, exist_ok=True)
    errors: list[str] = []
    exported: list[str] = []
    paths = list(EXPORT_PATHS)
    listing = subprocess.run(["git", "-C", str(root), "ls-tree", "-r", "--name-only", revision,
                              "--", "corpus/knowledge"], capture_output=True, text=True)
    if listing.returncode == 0:
        paths += [p for p in listing.stdout.splitlines() if p.endswith(".md")]
    else:
        errors.append(f"ls-tree corpus/knowledge rc={listing.returncode}")
    for rel in paths:
        show = subprocess.run(["git", "-C", str(root), "show", f"{revision}:{rel}"],
                              capture_output=True)
        dst = tree / rel
        dst.parent.mkdir(parents=True, exist_ok=True)
        if show.returncode != 0:
            continue
        dst.write_bytes(show.stdout)
        exported.append(rel)
    return tree, exported, errors


def read(path: Path) -> str:
    try:
        return path.read_text(encoding="utf-8", errors="replace")
    except OSError:
        return ""


def run(argv: list[str], cwd: Path, timeout: int = 240) -> tuple[int, str, str]:
    p = subprocess.run(argv, cwd=str(cwd), capture_output=True, text=True, timeout=timeout)
    return p.returncode, p.stdout, p.stderr


def row_shape(cells: list[str]) -> str:
    """The census's row-shape subset: 11 cells, closed enums, no community A tier, no empty cells."""
    if len(cells) != 11:
        return f"{len(cells)} cells, want 11"
    kind, tier, status = cells[2], cells[3], cells[7]
    if kind not in {"spec", "docs", "paper", "code", "tool", "dataset", "talk", "book",
                    "community", "own-work"}:
        return f"kind {kind}"
    if tier not in {"A", "B", "C"}:
        return f"tier {tier}"
    if status not in {"queued", "mined", "rejected"}:
        return f"status {status}"
    if tier == "A" and kind == "community":
        return "community tier A"
    for index, cell in enumerate(cells):
        if not cell:
            return f"empty cell {index}"
    return ""


def p_r79_1(tree: Path) -> tuple[bool, str]:
    reg = read(tree / "corpus/SOURCES.md")
    row = None
    for line in reg.splitlines():
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if cells and re.fullmatch(r"S[0-9]{3,}", cells[0] or "") and cells[0] == "S453":
            row = cells
            break
    if row is None:
        return False, "no S453 row in corpus/SOURCES.md"
    src = row[1].lower() if len(row) > 1 else ""
    if "rfc 9110" not in src and "rfc9110" not in src:
        return False, f"S453 source is not RFC 9110: {row[1][:60] if len(row) > 1 else ''}"
    if "9309" in src:
        return False, "S453 source still cites RFC 9309"
    lesson = read(tree / "corpus/lessons/round-80.md")
    if not ("R79-1" in lesson and "S453" in lesson and "RFC 9309" in lesson):
        return False, "round-80 lesson lacks the R79-1 erratum naming S453 and RFC 9309"
    used = row[11] if len(row) > 11 else ""
    cited = [p.strip() for p in used.split(",") if p.strip() and p.strip() != "—"]
    resolved = [p for p in cited if (tree / p).is_file() and "S453" in read(tree / p)]
    if not resolved:
        return False, "S453 used-by resolves to no file that cites S453"
    shape = row_shape(row)
    if shape:
        return False, f"S453 row fails the registry shape: {shape}"
    return True, f"S453 = RFC 9110 row present, used-by resolves ({resolved[0]}), row shape ok, erratum recorded"


def p_r79_2(tree: Path, work: Path) -> tuple[bool, str]:
    guard = tree / "scripts/ledger_append_guard.py"
    if not guard.exists():
        return False, "scripts/ledger_append_guard.py absent"
    rc, out, err = run([sys.executable, "-B", str(guard), "--selftest"], work)
    if rc != 0:
        return False, f"guard --selftest rc={rc}: {(out + err).strip().splitlines()[-1:] or ''}"
    if "non-prefix" not in out or not re.search(r"non-prefix[^\n]*failed", out):
        return False, "guard --selftest prints no failed non-prefix fixture"
    rc2, out2, err2 = run([sys.executable, "-B", str(guard), "--root", str(tree), "--json"], work)
    try:
        doc = json.loads(out2)
    except json.JSONDecodeError:
        return False, f"guard --json unparseable rc={rc2}: {err2.strip()[:120]}"
    if rc2 != 0 or not doc.get("prefix_preserved") or int(doc.get("files") or 0) < 1:
        return False, f"guard reports prefix_preserved={doc.get('prefix_preserved')} files={doc.get('files')}"
    return True, f"guard selftest green (non-prefix fixture failed); ledger files={doc.get('files')} prefix preserved"


def p_r79_3(tree: Path, work: Path) -> tuple[bool, str]:
    receipt = read(tree / ".ufo/waves/round-80/controls/c80-selftest.txt")
    m = re.search(r"^(selftest: \d+/\d+ passed)$", receipt, re.M)
    if not m or "exit=0" not in receipt:
        return False, "receipt c80-selftest.txt lacks a `selftest: N/N passed` line or `exit=0`"
    tool = tree / "scripts/x_robots_tag_audit.py"
    if not tool.exists():
        return False, "tool absent in measured tree"
    rc, out, err = run([sys.executable, "-B", str(tool), "--selftest"], work)
    line = [ln for ln in out.splitlines() if ln.startswith("selftest: ")]
    if rc != 0 or not line:
        return False, f"tool --selftest rc={rc} line={line}: {err.strip()[:120]}"
    if line[-1] != m.group(1):
        return False, f"receipt `{m.group(1)}` != re-run `{line[-1]}`"
    return True, f"receipt matches re-run: {line[-1]}"


def p_r79_4(tree: Path, work: Path) -> tuple[bool, str]:
    harness = tree / ".ufo/waves/round-80/c80_ledger_fixtures.py"
    if not harness.exists():
        return False, ".ufo/waves/round-80/c80_ledger_fixtures.py absent"
    rc, out, err = run([sys.executable, "-B", str(harness), "--root", str(tree), "--json"], work)
    try:
        doc = json.loads(out)
    except json.JSONDecodeError:
        return False, f"fixture harness unparseable rc={rc}: {(out + err).strip()[-160:]}"
    fixtures = doc.get("fixtures") or {}
    if int(doc.get("killed") or 0) != 3 or len(fixtures) != 3:
        return False, f"fixture harness killed={doc.get('killed')} fixtures={sorted(fixtures)}"
    cheap = fixtures.get("cheap_note") or {}
    if cheap.get("ledger_red") is not True or int(cheap.get("undisclosed") or 0) != 1:
        return False, f"cheap-note fixture not red through undisclosed=1: {cheap}"
    receipt = read(tree / ".ufo/waves/round-80/controls/c80-cheap-note.txt")
    if "cheap-note" not in receipt or "undisclosed=1" not in receipt:
        return False, "c80-cheap-note.txt lacks `cheap-note` or `undisclosed=1`"
    quality = read(tree / "corpus/QUALITY.md")
    if "R79-4" not in quality or "undisclosed=1" not in quality:
        return False, "QUALITY.md carries no R79-4 clause with undisclosed=1"
    return True, "k3/k4/k5 killed by isolated fixtures (cheap-note red via undisclosed=1); QUALITY clause present"


def p_r79_5(tree: Path) -> tuple[bool, str]:
    lesson = read(tree / "corpus/lessons/round-80.md")
    withdrawing = [ln for ln in lesson.splitlines() if "R79-5" in ln and WITHDRAWN in ln]
    if not withdrawing:
        return False, "round-80 lesson carries no R79-5 withdrawal row quoting the sentence"
    hits = []
    for rel in SELF_ASSESSMENT:
        if WITHDRAWN in read(tree / rel):
            hits.append(rel)
    for path in sorted((tree / "corpus/knowledge").rglob("*.md")):
        if WITHDRAWN in read(path):
            hits.append(str(path.relative_to(tree)))
    if hits:
        return False, f"withdrawn sentence still asserted in: {', '.join(hits[:4])}"
    return True, "withdrawal recorded; no self-assessment file repeats the sentence"


def p_r79_8(tree: Path) -> tuple[bool, str]:
    try:
        results = json.loads(read(tree / ".ufo/waves/round-79/w1-results.json"))["results"]
    except (json.JSONDecodeError, KeyError, TypeError) as exc:
        return False, f"round-79 results unreadable: {exc}"
    empty = {r.get("name"): (r.get("output") or "") for r in results if not (r.get("output") or "").strip()}
    if not empty:
        return False, "round-79 results carry no empty-output seat; population premise lost"
    try:
        record = json.loads(read(tree / ".ufo/waves/round-80/defect-queue.json"))["seats"]
    except (json.JSONDecodeError, KeyError, TypeError):
        return False, "defect-queue.json absent or malformed"
    for name, output in empty.items():
        entry = record.get(name)
        if not isinstance(entry, dict):
            return False, f"defect-queue.json has no entry for {name}"
        if entry.get("output_bytes") != len(output.encode("utf-8")):
            return False, f"{name}: output_bytes {entry.get('output_bytes')} != {len(output.encode('utf-8'))}"
        if entry.get("output_sha256") != sha256(output):
            return False, f"{name}: output_sha256 mismatch"
    return True, f"{len(empty)} empty-output seats recorded with re-derived bytes ({', '.join(empty)})"


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--root", default=".")
    ap.add_argument("--revision")
    ap.add_argument("--work")
    a = ap.parse_args()
    root = Path(a.root).resolve()
    work = Path(a.work) if a.work else Path(tempfile.mkdtemp(prefix="kake-c80-dq-"))
    work.mkdir(parents=True, exist_ok=True)
    owned = a.work is None
    try:
        if a.revision:
            tree, exported, errors = materialise(root, a.revision, work)
            label = a.revision
            if errors:
                print(f"note: {errors}")
        else:
            tree, exported, label = root, [], "worktree"
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
        print(f"C1v1 revision={label} items={len(ITEMS)} open={len(open_items)} "
              f"closed={len(ITEMS) - len(open_items)} exported={len(exported)} "
              f"met={'true' if met else 'false'}")
        print(f"exit={0 if met else 1}")
        return 0 if met else 1
    finally:
        if owned:
            shutil.rmtree(work, ignore_errors=True)


if __name__ == "__main__":
    sys.exit(main())
