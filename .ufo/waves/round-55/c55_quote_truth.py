#!/usr/bin/env python3
"""Round-55 C2 counter — freshness: Yahoo! JAPAN robots.txt assimilation, quote truth.

Successor of `.ufo/waves/round-52/c52_quote_truth.py` (same committed-bytes-only discipline:
`git show`, `git ls-tree`, `git log`; no worktree reads, no network). Differences from r52:

  * two of the three adopted rows (S372, S373) already exist in the lane registry (opened by
    round 53 and used by `yahoo-japan-rel-nofollow-semantics.md`); their only in-place change
    is `used-by` (CORPUS.md rule 2). The third row (S418, staged id S380) is appended.
  * every quoted span, and every Gate quote, is at most 25 units (a CJK character is one
    unit) — the strictest reading of the CORPUS.md rule 1 ceiling, so no word-segmentation
    ambiguity (round-54 routed defect 3) can arise for the new material.
  * C7 validates the append block *as appended*: the validated scratch registry carries the
    same S418 row bytes and the same three entry bytes as the landed tree.

Conditions (frozen in `contract.json` before any data):

  C1 the three admitted knowledge entries exist at their repo-relative paths.
  C2 each entry opens with `source:` / `verified-at:` / `recheck:` in its first 8 lines, the
     `source:` line names its row id, and the entry cites that id again below the header.
  C3 registry rows are well formed (11 cells, no pipe inside a cell, status `mined`, opened
     = the round date, recheck normalised); S418 carries the page URL; S372 and S373 differ
     from their base-revision row in `used-by` only.
  C4 used-by: S372 = prior + entry 1; S373 = prior + entry 2; S418 = exactly entry 3.
  C5 quote truth: lesson `## Gate` quote per id (6..25 units, raw substring of the retained
     body, URL and access date present) and every double-quoted span of 6+ units below each
     entry header (at most 25 units, raw substring of that row's retained body).
  C6 the retained body is pinned by its receipt (sha256, bytes, httpStatus 200, fetchedAt on
     the round date) and the receipt URL is exactly the registry row's URL.
  C7 the append block was census-validated before the append: argv names `--file` and the
     validated scratch registry, not `--root`; exit 0; no E03/E04; last line `ok`; the
     scratch registry's S418 row and the three scratch entries are byte-equal to the landed
     ones.
  C8 the pre-append mirror equals the base-revision registry (pinned sha256), its add-commit
     is a strict ancestor of the measured revision, and the measured registry minus the S418
     row, with S372/S373 used-by restored to the prior value, reproduces the mirror bytes.

Predicate (frozen in `contract.json`):

    met: conditions_passed == 8 of 8

Exit codes: 0 predicate met, 1 not met, 2 evidence unevaluable, 64 usage.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
from datetime import datetime, timezone

PREDICATE = "met: conditions_passed == 8 of 8"
ROUND_DATE = "2026-10-25"
BASE_REV = "fcaf4b85ce32dbe2a88ce9924a4994e8cd93212d"
REGISTRY = "corpus/SOURCES.md"
LESSON = "corpus/lessons/round-55.md"
WAVE = ".ufo/waves/round-55"
SOURCES_DIR = f"{WAVE}/sources"
RECEIPTS = f"{SOURCES_DIR}/receipts.json"
ASSIM = f"{WAVE}/assimilation"
MIRROR = f"{ASSIM}/pre-append/corpus/SOURCES.md"
MIRROR_PIN = f"{ASSIM}/mirror-pin.json"
VALIDATE = f"{ASSIM}/validate"
VALIDATE_REG = f"{VALIDATE}/corpus/SOURCES.md"
UNIT_CEILING = 25

NOFOLLOW = "corpus/knowledge/yahoo-japan-rel-nofollow-semantics.md"
BAIDU = "corpus/knowledge/baidu-friendly-crawl-guidance.md"
ADOPTED = {
    "S372": "corpus/knowledge/yahoo-japan-robots-txt-refusal-rules.md",
    "S373": "corpus/knowledge/yahoo-japan-robots-pattern-syntax.md",
    "S418": "corpus/knowledge/yahoo-japan-robots-txt-basics.md",
}
NEW_ROWS = ("S418",)
PRIOR_USED_BY = {"S372": [NOFOLLOW], "S373": [NOFOLLOW, BAIDU]}
ROW_URL = {
    "S372": "https://info-search.yahoo.co.jp/archives/002849.php",
    "S373": "https://info-search.yahoo.co.jp/archives/002850.php",
    "S418": "https://info-search.yahoo.co.jp/archives/002885.php",
}

CJK_RE = re.compile(r"[\u3040-\u30ff\u3400-\u4dbf\u4e00-\u9fff\uf900-\ufaff]")
ROW_RE = r"^ {0,3}\| *(%s) *\|"


def git(root: str, *args: str) -> tuple[int, str]:
    proc = subprocess.run(["git", "-C", root, *args], stdout=subprocess.PIPE,
                          stderr=subprocess.PIPE, text=True)
    return proc.returncode, proc.stdout


def show(root: str, rev: str, path: str) -> str | None:
    rc, out = git(root, "show", f"{rev}:{path}")
    return out if rc == 0 else None


def show_bytes(root: str, rev: str, path: str) -> bytes | None:
    proc = subprocess.run(["git", "-C", root, "show", f"{rev}:{path}"],
                          stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    return proc.stdout if proc.returncode == 0 else None


def parse_registry(text: str) -> dict[str, list[str]]:
    """Census-parser behaviour: 0 to 3 leading spaces before the pipe, under `## Registry`."""
    rows: dict[str, list[str]] = {}
    in_registry = False
    for line in text.splitlines():
        if line.strip().startswith("## "):
            in_registry = line.strip().lower().startswith("## registry")
            continue
        if not in_registry or not re.match(r"^ {0,3}\|", line):
            continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if len(cells) >= 2 and re.fullmatch(r"S[0-9]{3,}", cells[0]):
            rows[cells[0]] = cells
    return rows


def row_lines(text: str) -> dict[str, str]:
    out: dict[str, str] = {}
    for line in text.split("\n"):
        m = re.match(ROW_RE % r"S[0-9]{3,}", line)
        if m:
            out[m.group(1)] = line
    return out


def used_by(cell: str) -> list[str]:
    return [p.strip() for p in re.split(r"[,;]", cell) if p.strip() and p.strip() != "—"]


def units(text: str) -> int:
    """One unit per CJK character, one per non-CJK whitespace token."""
    return len(CJK_RE.findall(text)) + len([t for t in text.split() if not CJK_RE.search(t)])


def gate_lines(lesson: str) -> list[str]:
    out, in_gate = [], False
    for line in lesson.splitlines():
        if line.strip().startswith("## "):
            in_gate = line.strip().lower() == "## gate"
            continue
        if in_gate:
            out.append(line)
    return out


def gate_line(lesson: str, sid: str) -> str | None:
    for line in gate_lines(lesson):
        if line.strip().startswith(f"- {sid} "):
            return line
    return None


def parse_iso(value) -> datetime | None:
    if not isinstance(value, str):
        return None
    try:
        stamp = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return None
    return stamp.astimezone(timezone.utc) if stamp.tzinfo else None


def row_url(row: list[str]) -> str | None:
    for token in reversed(row[1].split()) if len(row) > 1 else []:
        if token.startswith(("http://", "https://")):
            return token
    return None


def set_used_by(line: str, value: str) -> str:
    """Replace the last data cell (used-by) of a registry row line."""
    head, _, _tail = line.rstrip().rstrip("|").rpartition("|")
    return f"{head}| {value} |"


def run_checks(root: str, rev: str) -> tuple[int, list[dict]]:
    results: list[dict] = []

    def add(check: str, notes: list[str], facts: dict | None = None) -> None:
        results.append({"check": check, "state": "pass" if not notes else "fail",
                        "notes": notes, "facts": facts or {}})

    def unevaluable(check: str, note: str) -> tuple[int, list[dict]]:
        return 2, results + [{"check": check, "state": "unevaluable", "notes": [note], "facts": {}}]

    try:
        registry_text = show(root, rev, REGISTRY)
        rows = parse_registry(registry_text) if registry_text else {}
        lesson_text = show(root, rev, LESSON)
        entries: dict[str, str | None] = {}
        bodies: dict[str, bytes | None] = {}

        c1: list[str] = []
        for sid, path in ADOPTED.items():
            entries[sid] = show(root, rev, path)
            if entries[sid] is None:
                c1.append(f"{sid}: knowledge entry {path} absent at the measured revision")
        add("C1_entries_exist", c1, {"entries": len(ADOPTED)})

        c2: list[str] = []
        for sid, body in entries.items():
            if body is None:
                c2.append(f"{sid}: entry absent")
                continue
            lines = body.splitlines()
            head = lines[:8]
            for key in ("source", "verified-at", "recheck"):
                if not any(re.match(rf"^[-* ]*{key} *:\s*\S", ln) for ln in head):
                    c2.append(f"{sid}: header lacks a filled `{key}:` line in its first 8 lines")
            src = next((ln for ln in head if re.match(r"^[-* ]*source *:", ln)), "")
            if not re.search(rf"\b{sid}\b", src):
                c2.append(f"{sid}: `source:` line does not name {sid}")
            if not any(re.search(rf"\b{sid}\b", ln) for ln in lines[8:]):
                c2.append(f"{sid}: entry does not cite its id below the 8-line header")
        add("C2_entry_provenance", c2)

        c3: list[str] = []
        base_registry = show(root, BASE_REV, REGISTRY)
        base_rows = parse_registry(base_registry) if base_registry else {}
        for sid in ADOPTED:
            row = rows.get(sid)
            if row is None:
                c3.append(f"{sid}: no registry row at the measured revision")
                continue
            if len(row) != 11:
                c3.append(f"{sid}: registry row has {len(row)} cells, expected 11")
                continue
            if any("\\|" in cell for cell in row):
                c3.append(f"{sid}: registry row carries an escaped pipe")
            if row[7] != "mined":
                c3.append(f"{sid}: status is {row[7]!r}, expected 'mined'")
            if row[8] != ROUND_DATE:
                c3.append(f"{sid}: opened is {row[8]!r}, expected {ROUND_DATE!r}")
            if not re.fullmatch(r"(\d{4}-\d{2}-\d{2}|\d+d|on-release)", row[9]):
                c3.append(f"{sid}: recheck {row[9]!r} is not an ISO date, NNd or on-release")
            if row_url(row) != ROW_URL[sid]:
                c3.append(f"{sid}: row URL {row_url(row)!r} != {ROW_URL[sid]!r}")
            if sid in NEW_ROWS:
                if sid in base_rows:
                    c3.append(f"{sid}: already in the base registry; not a new row")
            else:
                base = base_rows.get(sid)
                if base is None:
                    c3.append(f"{sid}: no base-revision row to compare with")
                elif row[:10] != base[:10]:
                    c3.append(f"{sid}: a cell other than used-by differs from the base row")
        add("C3_row_shape", c3, {"rows": len(rows), "base_rows": len(base_rows)})

        c4: list[str] = []
        for sid, path in ADOPTED.items():
            row = rows.get(sid)
            if row is None or len(row) < 11:
                c4.append(f"{sid}: no usable registry row")
                continue
            want = PRIOR_USED_BY.get(sid, []) + [path]
            got = used_by(row[10])
            if got != want:
                c4.append(f"{sid}: used-by is {got!r}, expected {want!r}")
        add("C4_used_by", c4)

        c5: list[str] = []
        for sid in ADOPTED:
            raw = show_bytes(root, rev, f"{SOURCES_DIR}/{sid}.html")
            bodies[sid] = raw
            if raw is None:
                c5.append(f"{sid}: retained body absent")
                continue
            try:
                text = raw.decode("utf-8")
            except UnicodeDecodeError:
                c5.append(f"{sid}: retained body is not UTF-8")
                continue
            if len(raw) < 1000:
                c5.append(f"{sid}: retained body is {len(raw)} bytes, below the 1000-byte floor")
            if lesson_text is None:
                c5.append(f"{sid}: lesson {LESSON} absent")
            else:
                line = gate_line(lesson_text, sid)
                if line is None:
                    c5.append(f"{sid}: no `- {sid} ` line in the lesson ## Gate")
                else:
                    quotes = re.findall(r'"([^"]+)"', line)
                    if not quotes:
                        c5.append(f"{sid}: Gate line carries no double-quoted located quote")
                    else:
                        q = quotes[-1]
                        u = units(q)
                        if not 6 <= u <= UNIT_CEILING:
                            c5.append(f"{sid}: Gate quote is {u} units, expected 6 to {UNIT_CEILING}")
                        if q not in text:
                            c5.append(f"{sid}: Gate quote is not a raw substring of the retained body")
                    if ROW_URL[sid] not in line:
                        c5.append(f"{sid}: Gate line does not carry the URL")
                    if ROUND_DATE not in line:
                        c5.append(f"{sid}: Gate line does not carry the access date {ROUND_DATE}")
            body = entries.get(sid)
            if body is None:
                continue
            for lineno, line in enumerate(body.splitlines()[8:], start=9):
                if "[INFERENCE" in line:
                    continue
                for span in re.findall(r'"([^"]{1,400})"', line):
                    u = units(span)
                    if u < 6:
                        continue
                    if u > UNIT_CEILING:
                        c5.append(f"{sid}: entry line {lineno} quotes {u} units, ceiling {UNIT_CEILING}")
                    if span not in text:
                        c5.append(f"{sid}: entry line {lineno} quotes {span[:40]!r}… "
                                  "which is not a raw substring of the retained body")
        add("C5_quote_truth", c5)

        c6: list[str] = []
        receipts_text = show(root, rev, RECEIPTS)
        receipts: dict = {}
        if receipts_text is None:
            c6.append(f"{RECEIPTS} absent")
        else:
            try:
                receipts = json.loads(receipts_text).get("sources", {})
            except (json.JSONDecodeError, AttributeError):
                return unevaluable("C6_receipt_pins", f"{RECEIPTS} is not a JSON object with sources")
        for sid in ADOPTED:
            receipt = receipts.get(sid)
            raw = bodies.get(sid)
            if receipt is None:
                c6.append(f"{sid}: no receipt in {RECEIPTS}")
                continue
            if raw is None:
                c6.append(f"{sid}: no retained body to hash")
                continue
            digest = hashlib.sha256(raw).hexdigest()
            if receipt.get("sha256") != digest:
                c6.append(f"{sid}: receipt sha256 {receipt.get('sha256')} != body {digest}")
            if receipt.get("bytes") != len(raw):
                c6.append(f"{sid}: receipt bytes {receipt.get('bytes')} != body {len(raw)}")
            status = receipt.get("httpStatus")
            if not isinstance(status, int) or isinstance(status, bool) or status != 200:
                c6.append(f"{sid}: receipt httpStatus is {status!r}, expected the integer 200")
            stamp = parse_iso(receipt.get("fetchedAt"))
            if stamp is None:
                c6.append(f"{sid}: receipt fetchedAt {receipt.get('fetchedAt')!r} is not ISO 8601")
            elif stamp.date().isoformat() != ROUND_DATE:
                c6.append(f"{sid}: receipt fetchedAt date {stamp.date()} != round date {ROUND_DATE}")
            row = rows.get(sid)
            url = row_url(row) if row else None
            if url is None:
                c6.append(f"{sid}: no registry URL to compare the receipt with")
            elif receipt.get("url") != url:
                c6.append(f"{sid}: receipt URL {receipt.get('url')!r} != registry row URL {url!r}")
        add("C6_receipt_pins", c6, {"receipts": len(receipts)})

        c7: list[str] = []
        argv = show(root, rev, f"{VALIDATE}/census-argv.txt")
        stdout = show(root, rev, f"{VALIDATE}/census-stdout.txt")
        exit_text = show(root, rev, f"{VALIDATE}/census-exit.txt")
        validated = show(root, rev, VALIDATE_REG)
        if None in (argv, stdout, exit_text, validated):
            c7.append("append-block validation receipt is incomplete")
        else:
            if "--file" not in argv:
                c7.append("validation argv does not use --file")
            if "--root" in argv:
                c7.append("validation argv names --root, not a single file")
            if VALIDATE_REG not in argv:
                c7.append("validation argv does not name the validated scratch registry")
            if exit_text.strip() != "exit=0":
                c7.append(f"validation exit is {exit_text.strip()!r}, expected 'exit=0'")
            for code in ("E03", "E04"):
                if code in stdout:
                    c7.append(f"validation stdout carries an {code} finding")
            tail = [ln for ln in stdout.splitlines() if ln.strip()]
            if not tail or tail[-1].split("\t")[1:2] != ["ok"]:
                c7.append("validation stdout does not end in an ok line")
            vlines, llines = row_lines(validated), row_lines(registry_text or "")
            for sid in ADOPTED:
                if vlines.get(sid) is None:
                    c7.append(f"{sid}: validated scratch registry carries no row")
                elif vlines.get(sid) != llines.get(sid):
                    c7.append(f"{sid}: validated row bytes differ from the landed row")
            for sid, path in ADOPTED.items():
                scratch = show(root, rev, f"{VALIDATE}/{path}")
                if scratch is None or scratch != entries.get(sid):
                    c7.append(f"{sid}: validated scratch entry differs from the landed entry")
        add("C7_validate_before_append", c7)

        c8: list[str] = []
        mirror_text = show(root, rev, MIRROR)
        pin_text = show(root, rev, MIRROR_PIN)
        pin: dict = {}
        if mirror_text is None:
            c8.append(f"mirror {MIRROR} absent at the measured revision")
        elif pin_text is None:
            c8.append(f"mirror pin {MIRROR_PIN} absent")
        else:
            try:
                pin = json.loads(pin_text)
            except json.JSONDecodeError:
                return unevaluable("C8_mirror_bytes", f"{MIRROR_PIN} is not JSON")
        if mirror_text is not None and pin:
            mirror_rows = parse_registry(mirror_text)
            if base_registry is None or base_registry != mirror_text:
                c8.append("mirror bytes differ from the base-revision registry")
            for sid in NEW_ROWS:
                if sid in mirror_rows:
                    c8.append(f"{sid}: the mirror bytes already carry the row")
            digest = hashlib.sha256(mirror_text.encode("utf-8")).hexdigest()
            if pin.get("sha256") != digest:
                c8.append(f"mirror sha256 {digest} != pinned {pin.get('sha256')}")
            if pin.get("rows") != len(mirror_rows):
                c8.append(f"mirror rows {len(mirror_rows)} != pinned {pin.get('rows')}")
            if len(rows) != len(mirror_rows) + len(NEW_ROWS):
                c8.append(f"registry rows {len(rows)} != mirror rows {len(mirror_rows)} + {len(NEW_ROWS)}")
            restored = []
            mlines = row_lines(mirror_text)
            for line in (registry_text or "").split("\n"):
                m = re.match(ROW_RE % r"S[0-9]{3,}", line)
                sid = m.group(1) if m else None
                if sid in NEW_ROWS:
                    continue
                if sid in PRIOR_USED_BY and sid in mlines:
                    mrow = [c.strip() for c in mlines[sid].strip().strip("|").split("|")]
                    line = set_used_by(line, mrow[10])
                restored.append(line)
            if "\n".join(restored) != mirror_text:
                c8.append("append-only: measured registry minus new rows, used-by restored, != mirror bytes")
            rc, out = git(root, "log", "--diff-filter=A", "--format=%H", rev, "--", MIRROR)
            commits = [ln.strip() for ln in out.splitlines() if ln.strip()]
            if not commits:
                c8.append("no commit adds the mirror")
            else:
                add_commit = commits[-1]
                if git(root, "merge-base", "--is-ancestor", add_commit, rev)[0] != 0:
                    c8.append(f"mirror add-commit {add_commit} is not an ancestor of {rev}")
                if add_commit == rev:
                    c8.append("mirror add-commit is the measured revision (not strictly earlier)")
                add_blob = show(root, add_commit, MIRROR)
                if add_blob is None:
                    c8.append("mirror blob unreadable at its add-commit")
                elif hashlib.sha256(add_blob.encode("utf-8")).hexdigest() != pin.get("sha256"):
                    c8.append("mirror blob at its add-commit does not hash to the pinned sha256")
                else:
                    for sid in NEW_ROWS:
                        if sid in parse_registry(add_blob):
                            c8.append(f"{sid}: the mirror blob at its add-commit carries the row")
            for sid in ADOPTED:
                if sid not in rows:
                    c8.append(f"{sid}: the measured revision does not carry the row")
        add("C8_mirror_bytes", c8, {"registry_rows": len(rows)})
    except Exception as exc:  # unevaluable evidence is exit 2, never a silent miss
        return 2, results + [{"check": "exception", "state": "unevaluable",
                              "notes": [f"{type(exc).__name__}: {exc}"], "facts": {}}]

    if any(r["state"] == "unevaluable" for r in results):
        return 2, results
    return (0 if all(r["state"] == "pass" for r in results) else 1), results


# --------------------------------------------------------------------------- selftest


def _build(files: dict[str, str], pre_keys: set[str]) -> tuple[str, str]:
    """Sandbox repo: base-revision registry commit, pre-append evidence commit, then the rest."""
    d = tempfile.mkdtemp(prefix="c55-qt-")
    subprocess.run(["git", "-C", d, "init", "-q"], check=True)
    rc, top = git(d, "rev-parse", "--show-toplevel")
    if os.path.realpath(top.strip()) != os.path.realpath(d):
        raise RuntimeError("fixture repo toplevel mismatch")

    def commit(batch: dict[str, str], msg: str) -> str:
        for rel, text in batch.items():
            tgt = os.path.join(d, rel)
            os.makedirs(os.path.dirname(tgt), exist_ok=True)
            with open(tgt, "w", encoding="utf-8") as fh:
                fh.write(text)
        subprocess.run(["git", "-C", d, "add", "-A"], check=True)
        subprocess.run(["git", "-C", d, "-c", "user.name=selftest", "-c", "user.email=selftest@local",
                        "commit", "-q", "--allow-empty", "-m", msg], check=True)
        return git(d, "rev-parse", "HEAD")[1].strip()

    base_text = files.get("__base_registry__", "")
    commit({REGISTRY: base_text}, "base")
    base_sha = git(d, "rev-parse", "HEAD")[1].strip()
    commit({k: v for k, v in files.items() if k in pre_keys}, "pre-append evidence")
    tip = commit({k: v for k, v in files.items() if k not in pre_keys and k != "__base_registry__"},
                 "append")
    return d, tip, base_sha


def selftest() -> int:
    global BASE_REV
    rev = os.environ.get("KAKE_R55_SELFTEST_REV") or git(os.getcwd(), "rev-parse", "HEAD")[1].strip()
    root = os.getcwd()
    keys = [REGISTRY, LESSON, RECEIPTS, MIRROR, MIRROR_PIN, VALIDATE_REG,
            f"{VALIDATE}/census-argv.txt", f"{VALIDATE}/census-stdout.txt", f"{VALIDATE}/census-exit.txt",
            *ADOPTED.values(), *(f"{VALIDATE}/{p}" for p in ADOPTED.values()),
            *(f"{SOURCES_DIR}/{sid}.html" for sid in ADOPTED)]
    real: dict[str, str] = {}
    for rel in keys:
        raw = show(root, rev, rel)
        if raw is None:
            print(f"selftest: missing round-55 evidence {rel}", file=sys.stderr)
            return 2
        real[rel] = raw
    base_text = show(root, BASE_REV, REGISTRY)
    if base_text is None:
        print("selftest: base registry unreadable", file=sys.stderr)
        return 2

    def variant(mut) -> dict[str, str]:
        files = dict(real)
        files["__base_registry__"] = base_text
        mut(files)
        return files

    def row(files, sid):
        return next(ln for ln in files[REGISTRY].split("\n") if re.match(ROW_RE % sid, ln))

    def jload(files, rel):
        return json.loads(files[rel])

    def jdump(obj):
        return json.dumps(obj, ensure_ascii=False, indent=1)

    cases: dict[str, tuple] = {"pass": (variant(lambda f: None), 0)}

    def case(name, want=1):
        def deco(fn):
            cases[name] = (variant(fn), want)
            return fn
        return deco

    @case("fail_missing_entry")
    def _(f): del f[ADOPTED["S373"]]

    @case("fail_no_source_header")
    def _(f): f[ADOPTED["S418"]] = f[ADOPTED["S418"]].replace("source:", "origin:", 1)

    @case("fail_no_cite_below_header")
    def _(f): f[ADOPTED["S372"]] = f[ADOPTED["S372"]].replace("S372", "S999")

    @case("fail_row_short")
    def _(f): f[REGISTRY] = f[REGISTRY].replace(row(f, "S418"), "|".join(row(f, "S418").split("|")[:-2]) + " |")

    @case("fail_new_row_wrong_url")
    def _(f): f[REGISTRY] = f[REGISTRY].replace(row(f, "S418"), row(f, "S418").replace("002885", "002886"))

    @case("fail_held_row_cell_changed")
    def _(f): f[REGISTRY] = f[REGISTRY].replace(row(f, "S372"), row(f, "S372").replace("| docs | A |", "| docs | B |", 1))

    @case("fail_used_by_dropped_prior")
    def _(f):
        f[REGISTRY] = f[REGISTRY].replace(row(f, "S373"), set_used_by(row(f, "S373"), ADOPTED["S373"]))

    @case("fail_used_by_not_extended")
    def _(f):
        f[REGISTRY] = f[REGISTRY].replace(row(f, "S372"), set_used_by(row(f, "S372"), NOFOLLOW))

    @case("fail_lesson_quote")
    def _(f):
        q = re.findall(r'"([^"]+)"', next(ln for ln in gate_lines(f[LESSON]) if ln.strip().startswith("- S373 ")))[-1]
        f[LESSON] = f[LESSON].replace(q, q[:-3] + "ZZZ")

    @case("fail_lesson_no_date")
    def _(f):
        f[LESSON] = "\n".join(ln.replace(ROUND_DATE, "2026-10-24") if ln.strip().startswith("- S418 ") else ln
                              for ln in f[LESSON].split("\n"))

    @case("fail_entry_quote")
    def _(f):
        body = f[ADOPTED["S372"]]
        spans = [s for s in re.findall(r'"([^"]{1,400})"', "\n".join(body.splitlines()[8:])) if units(s) >= 6]
        f[ADOPTED["S372"]] = body.replace(spans[0], spans[0][:-2] + "ZZ")

    @case("fail_entry_quote_over_ceiling")
    def _(f):
        f[ADOPTED["S372"]] += '\n> "' + "あ" * 40 + '"\n'

    @case("fail_receipt_sha")
    def _(f):
        r = jload(f, RECEIPTS); r["sources"]["S373"]["sha256"] = "0" * 64; f[RECEIPTS] = jdump(r)

    @case("fail_receipt_status")
    def _(f):
        r = jload(f, RECEIPTS); r["sources"]["S372"]["httpStatus"] = 500; f[RECEIPTS] = jdump(r)

    @case("fail_receipt_status_bool")
    def _(f):
        r = jload(f, RECEIPTS); r["sources"]["S372"]["httpStatus"] = True; f[RECEIPTS] = jdump(r)

    @case("fail_receipt_stale_date")
    def _(f):
        r = jload(f, RECEIPTS); r["sources"]["S418"]["fetchedAt"] = "2026-10-24T10:00:00+00:00"; f[RECEIPTS] = jdump(r)

    @case("fail_receipt_url")
    def _(f):
        r = jload(f, RECEIPTS); r["sources"]["S418"]["url"] = ROW_URL["S372"]; f[RECEIPTS] = jdump(r)

    @case("fail_validate_exit")
    def _(f): f[f"{VALIDATE}/census-exit.txt"] = "exit=1\n"

    @case("fail_validate_e04")
    def _(f): f[f"{VALIDATE}/census-stdout.txt"] += "file\tE04\tS418 duplicate source row\n"

    @case("fail_validate_root_argv")
    def _(f): f[f"{VALIDATE}/census-argv.txt"] = "validate --root /x kake\n"

    @case("fail_validated_row_differs")
    def _(f): f[VALIDATE_REG] = f[VALIDATE_REG].replace(row(f, "S418"), row(f, "S418").replace("mined", "queued"))

    @case("fail_validated_entry_differs")
    def _(f):
        p = f"{VALIDATE}/{ADOPTED['S373']}"; f[p] = f[p] + "\nextra\n"

    @case("fail_mirror_contaminated")
    def _(f): f[MIRROR] = f[MIRROR] + row(f, "S418") + "\n"

    @case("fail_mirror_not_base")
    def _(f): f[MIRROR] = f[MIRROR].replace("| S001 |", "| S001 | x", 1)

    @case("fail_pin_sha")
    def _(f):
        p = jload(f, MIRROR_PIN); p["sha256"] = "f" * 64; f[MIRROR_PIN] = jdump(p)

    @case("fail_registry_row_dropped")
    def _(f): f[REGISTRY] = f[REGISTRY].replace(row(f, "S418") + "\n", "")

    @case("fail_not_append_only")
    def _(f): f[REGISTRY] = f[REGISTRY].replace("| S263 |", "| S263 (edited) |", 1)

    @case("fail_empty_body")
    def _(f): f[f"{SOURCES_DIR}/S418.html"] = ""

    @case("fail_bad_receipts", 2)
    def _(f): f[RECEIPTS] = "{not json"

    passed, fails = 0, []
    pre = {MIRROR, MIRROR_PIN, VALIDATE_REG, f"{VALIDATE}/census-argv.txt", f"{VALIDATE}/census-stdout.txt",
           f"{VALIDATE}/census-exit.txt", *(f"{VALIDATE}/{p}" for p in ADOPTED.values())}
    for name in sorted(cases):
        files, want = cases[name]
        d, tip, base_sha = _build(files, pre)
        BASE_REV = base_sha
        try:
            code, results = run_checks(d, tip)
        finally:
            shutil.rmtree(d, ignore_errors=True)
        if code == want:
            passed += 1
        else:
            fails.append(f"{name}: expected {want}, got {code}")
            for r in results:
                fails.extend(f"    {r['check']}: {n}" for n in r["notes"][:2])
    print(f"c55 quote-truth selftest: {passed}/{len(cases)} (fixture revision {rev[:12]})")
    for line in fails:
        print("  FAIL", line)
    return 0 if passed == len(cases) else 1


def main() -> int:
    ap = argparse.ArgumentParser(description="Round-55 C2 counter (Yahoo! robots assimilation)")
    ap.add_argument("--root", default=".")
    ap.add_argument("--revision")
    ap.add_argument("--selftest", action="store_true")
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()
    if args.selftest:
        return selftest()
    if not args.revision:
        ap.error("--revision is required unless --selftest is used")
    code, results = run_checks(args.root, args.revision)
    passed = sum(1 for r in results if r["state"] == "pass")
    if args.json:
        print(json.dumps({
            "schema": "kake-r55-c2-quote-truth-v1", "predicate": PREDICATE, "revision": args.revision,
            "adopted": ADOPTED,
            "checks": {r["check"]: {"passed": r["state"] == "pass", "state": r["state"],
                                    "notes": r["notes"], "facts": r["facts"]} for r in results},
            "conditions_passed": passed, "met": code == 0}, indent=1, ensure_ascii=False))
    else:
        print(f"C2 quote-truth {passed}/8 met={code == 0}  ({PREDICATE})")
        for r in results:
            print(f"  {r['check']} {r['state'].upper()}")
            for note in r["notes"]:
                print(f"    - {note}")
        print(f"  revision: {args.revision}")
    print(f"EXIT={code}")
    return code


if __name__ == "__main__":
    sys.exit(main())
