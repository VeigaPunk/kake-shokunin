#!/usr/bin/env python3
"""Round-52 quote-truth counter — the C2 counter (freshness, assimilation).

Supersedes `.ufo/waves/round-51/c51_quote_truth.py`. Same eight conditions over
committed bytes only (`git show`, `git ls-tree`, `git log`; no worktree reads, no
network), with the three round-51 closure defects folded in:

  C8 now reads the mirror BYTES at the measured revision (`show(root, rev, MIRROR)`)
     and pins their sha256 in `.ufo/waves/round-52/assimilation/mirror-pin.json`;
     it also proves append-only: the measured registry minus the adopted rows is
     byte-identical to the mirror.
  C6 now checks the receipt's `httpStatus` (integer 200), `bytes` (equal to the
     retained body length) and `fetchedAt` (parsable ISO 8601) as well as sha256 and
     an EXACT URL match against the registry row.
  C5 now guards every entry as well as the lesson: each `## Gate` quote (6-40 units,
     a CJK character counting as one unit) and every double-quoted span of 6+ units
     below an entry's header must be a raw substring of that row's retained body.

Conditions (frozen in `.ufo/waves/round-52/contract.json` before any data):

  C1 the three admitted knowledge entries exist at their repo-relative paths.
  C2 each entry cites its own row id below its 8-line metadata header.
  C3 each registry row is well formed (11 cells, no literal or escaped pipe, status
     `mined`, the round's opened date, a normalized recheck).
  C4 each registry row's `used-by` lists exactly the admitted entry that cites it.
  C5 quote truth at lesson and entry level (rule above).
  C6 the retained body is pinned by its receipt (sha256, bytes, httpStatus,
     fetchedAt) and the receipt URL is exactly the registry row's URL.
  C7 the pre-append mirror was census-validated with `--file` before the append:
     argv names the mirror path and not `--root`, the exit is 0, the stdout carries
     no E03 and no E04, and its last line is `ok`.
  C8 the mirror bytes carry none of the adopted ids and equal the pinned sha256 at
     both the measured revision and the mirror's add-commit; that commit is a strict
     ancestor of the measured revision; the measured registry carries all three ids;
     and removing the three appended rows reproduces the mirror bytes exactly.

Predicate (frozen in `.ufo/waves/round-52/contract.json` before any data):

    met: conditions_passed == 8 of 8

Exit codes: 0 predicate met, 1 not met, 2 evidence unevaluable (malformed JSON or
exception), 64 usage.
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
from datetime import datetime, timezone

PREDICATE = "met: conditions_passed == 8 of 8"
ROUND_DATE = "2026-10-25"
REGISTRY = "corpus/SOURCES.md"
LESSON = "corpus/lessons/round-52.md"
SOURCES_DIR = ".ufo/waves/round-52/sources"
RECEIPTS = f"{SOURCES_DIR}/receipts.json"
ASSIM = ".ufo/waves/round-52/assimilation"
MIRROR = f"{ASSIM}/pre-append/corpus/SOURCES.md"
MIRROR_PIN = f"{ASSIM}/mirror-pin.json"
CENSUS_DIR = f"{ASSIM}/pre-append"
SELFTEST_DIR = ".ufo/waves/round-52/selftest/quote"

ADOPTED = {
    "S374": "corpus/knowledge/yahoo-japan-rel-nofollow-semantics.md",
    "S329": "corpus/knowledge/baidu-friendly-crawl-guidance.md",
    "S312": "corpus/knowledge/baidu-mobile-matching-error-causes.md",
}

CJK_RE = re.compile(r"[\u3040-\u30ff\u3400-\u4dbf\u4e00-\u9fff\uf900-\ufaff]")


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


def units(text: str) -> int:
    """One unit per CJK character, one per non-CJK whitespace token."""
    cjk = len(CJK_RE.findall(text))
    latin = len([t for t in text.split() if not CJK_RE.search(t)])
    return cjk + latin


def parse_iso(value) -> datetime | None:
    if not isinstance(value, str):
        return None
    try:
        stamp = datetime.fromisoformat(value.replace("Z", "+00:00"))
    except ValueError:
        return None
    if stamp.tzinfo is None:
        return None
    return stamp.astimezone(timezone.utc)


def row_url(row: list[str]) -> str | None:
    if len(row) < 2:
        return None
    for token in reversed(row[1].split()):
        if token.startswith("http://") or token.startswith("https://"):
            return token
    return None


def run_checks(root: str, rev: str) -> tuple[int, list[dict]]:
    results: list[dict] = []

    def add(check: str, notes: list[str], facts: dict | None = None) -> None:
        results.append({
            "check": check,
            "state": "pass" if not notes else "fail",
            "notes": notes,
            "facts": facts or {},
        })

    try:
        registry_text = show(root, rev, REGISTRY)
        rows = parse_registry(registry_text) if registry_text else {}
        lesson_text = show(root, rev, LESSON)
        entries: dict[str, str | None] = {}
        bodies: dict[str, bytes | None] = {}

        # C1 — entries exist
        c1: list[str] = []
        for sid, path in ADOPTED.items():
            entries[sid] = show(root, rev, path)
            if entries[sid] is None:
                c1.append(f"{sid}: knowledge entry {path} absent at the measured revision")
        add("C1_entries_exist", c1, {"entries": len(ADOPTED)})

        # C2 — entry cites its id below the header
        c2: list[str] = []
        for sid, body in entries.items():
            if body is None:
                c2.append(f"{sid}: entry absent")
                continue
            lines = body.splitlines()
            if not any(re.search(rf"\b{sid}\b", line) for line in lines[8:]):
                c2.append(f"{sid}: entry does not cite its id below the 8-line header")
        add("C2_entry_cites_id", c2)

        # C3 — registry row shape
        c3: list[str] = []
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
                c3.append(f"{sid}: registry status is {row[7]!r}, expected 'mined'")
            if row[8] != ROUND_DATE:
                c3.append(f"{sid}: registry opened is {row[8]!r}, expected {ROUND_DATE!r}")
            if not re.fullmatch(r"(\d{4}-\d{2}-\d{2}|\d+d|on-release)", row[9]):
                c3.append(
                    f"{sid}: registry recheck is {row[9]!r}, expected a normalized "
                    "ISO date, NNd cadence or on-release"
                )
        add("C3_row_shape", c3, {"rows": len(rows)})

        # C4 — used-by names exactly the citing entry
        c4: list[str] = []
        for sid, path in ADOPTED.items():
            row = rows.get(sid)
            if row is None or len(row) < 11:
                c4.append(f"{sid}: no usable registry row")
                continue
            used_by = [p.strip() for p in row[10].split(",") if p.strip()]
            if used_by != [path]:
                c4.append(f"{sid}: used-by is {used_by!r}, expected exactly [{path!r}]")
        add("C4_used_by", c4)

        # C5 — quote truth at lesson and entry level
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
                quote = gate_quote(lesson_text, sid)
                if quote is None:
                    c5.append(f"{sid}: no ## Gate quote in the lesson")
                else:
                    u = units(quote)
                    if not 6 <= u <= 40:
                        c5.append(f"{sid}: Gate quote is {u} units, expected 6 to 40")
                    if quote not in text:
                        c5.append(f"{sid}: Gate quote is not a raw substring of the retained body")
            body = entries.get(sid)
            if body is None:
                continue
            for lineno, line in enumerate(body.splitlines()[8:], start=9):
                if "[INFERENCE" in line:
                    continue
                for span in re.findall(r'"([^"]{1,400})"', line):
                    if units(span) < 6:
                        continue
                    if span not in text:
                        c5.append(
                            f"{sid}: entry line {lineno} quotes {span[:40]!r}… "
                            "which is not a raw substring of the retained body"
                        )
        add("C5_quote_truth", c5)

        # C6 — receipt pins the body, and the body's URL is the row's URL
        c6: list[str] = []
        receipts_text = show(root, rev, RECEIPTS)
        if receipts_text is None:
            c6.append(f"{RECEIPTS} absent")
            receipts = {}
        else:
            try:
                receipts = json.loads(receipts_text).get("sources", {})
            except json.JSONDecodeError:
                return 2, results + [{
                    "check": "C6_receipt_pins",
                    "state": "unevaluable",
                    "notes": [f"{RECEIPTS} is not JSON"],
                    "facts": {},
                }]
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
            if not isinstance(status, int) or status != 200:
                c6.append(f"{sid}: receipt httpStatus is {status!r}, expected the integer 200")
            if parse_iso(receipt.get("fetchedAt")) is None:
                c6.append(f"{sid}: receipt fetchedAt {receipt.get('fetchedAt')!r} is not ISO 8601")
            row = rows.get(sid)
            if row is None:
                c6.append(f"{sid}: no registry row to compare the URL with")
            else:
                url = row_url(row)
                if url is None:
                    c6.append(f"{sid}: registry row carries no URL")
                elif receipt.get("url") != url:
                    c6.append(
                        f"{sid}: receipt URL {receipt.get('url')!r} != registry row URL {url!r}"
                    )
        add("C6_receipt_pins", c6, {"receipts": len(receipts)})

        # C7 — the pre-append mirror was census-validated with --file
        c7: list[str] = []
        argv = show(root, rev, f"{CENSUS_DIR}/census-argv.txt")
        stdout = show(root, rev, f"{CENSUS_DIR}/census-stdout.txt")
        exit_text = show(root, rev, f"{CENSUS_DIR}/census-exit.txt")
        if argv is None or stdout is None or exit_text is None:
            c7.append("pre-append census receipt is incomplete")
        else:
            if "--file" not in argv:
                c7.append("pre-append census argv does not use --file")
            if "--root" in argv:
                c7.append("pre-append census argv names --root, not a single file")
            if MIRROR not in argv:
                c7.append("pre-append census argv does not name the mirror path")
            if exit_text.strip() != "exit=0":
                c7.append(f"pre-append census exit is {exit_text.strip()!r}, expected 'exit=0'")
            for code in ("E03", "E04"):
                if code in stdout:
                    c7.append(f"pre-append census stdout carries an {code} finding")
            tail = [l for l in stdout.splitlines() if l.strip()]
            if not tail or tail[-1].split("\t")[1:2] != ["ok"]:
                c7.append("pre-append census stdout does not end in an ok line")
        add("C7_validate_before_append", c7)

        # C8 — mirror bytes, pinned sha256, strict ancestry, append-only
        c8: list[str] = []
        mirror_text = show(root, rev, MIRROR)
        pin_text = show(root, rev, MIRROR_PIN)
        if mirror_text is None:
            c8.append(f"mirror {MIRROR} absent at the measured revision")
            pin = {}
        elif pin_text is None:
            c8.append(f"mirror pin {MIRROR_PIN} absent")
            pin = {}
        else:
            try:
                pin = json.loads(pin_text)
            except json.JSONDecodeError:
                return 2, results + [{
                    "check": "C8_mirror_bytes",
                    "state": "unevaluable",
                    "notes": [f"{MIRROR_PIN} is not JSON"],
                    "facts": {},
                }]
        if mirror_text is not None and pin:
            mirror_rows = parse_registry(mirror_text)
            for sid in ADOPTED:
                if sid in mirror_rows:
                    c8.append(f"{sid}: the mirror bytes already carry the row")
            digest = hashlib.sha256(mirror_text.encode("utf-8")).hexdigest()
            if pin.get("sha256") != digest:
                c8.append(f"mirror sha256 {digest} != pinned {pin.get('sha256')}")
            if pin.get("rows") != len(mirror_rows):
                c8.append(f"mirror rows {len(mirror_rows)} != pinned {pin.get('rows')}")
            if len(rows) != len(mirror_rows) + len(ADOPTED):
                c8.append(
                    f"registry rows {len(rows)} != mirror rows {len(mirror_rows)} + "
                    f"{len(ADOPTED)}"
                )
            stripped = "\n".join(
                line for line in (registry_text or "").split("\n")
                if not re.match(r"^ {0,3}\| (S374|S329|S312) \|", line)
            )
            if stripped != mirror_text:
                c8.append("append-only: measured registry minus the adopted rows != mirror bytes")
            rc, out = git(root, "log", "--diff-filter=A", "--format=%H", rev, "--", MIRROR)
            commits = [line.strip() for line in out.splitlines() if line.strip()]
            if not commits:
                c8.append("no commit adds the mirror")
            else:
                add_commit = commits[-1]
                rc_anc, _ = git(root, "merge-base", "--is-ancestor", add_commit, rev)
                if rc_anc != 0:
                    c8.append(f"mirror add-commit {add_commit} is not an ancestor of {rev}")
                if add_commit == rev:
                    c8.append("mirror add-commit is the measured revision (not strictly earlier)")
                add_blob = show(root, add_commit, MIRROR)
                if add_blob is None:
                    c8.append("mirror blob unreadable at its add-commit")
                else:
                    add_digest = hashlib.sha256(add_blob.encode("utf-8")).hexdigest()
                    if pin.get("sha256") != add_digest:
                        c8.append(
                            f"mirror blob at add-commit hashes {add_digest}, pinned {pin.get('sha256')}"
                        )
                    add_rows = parse_registry(add_blob)
                    for sid in ADOPTED:
                        if sid in add_rows:
                            c8.append(f"{sid}: the mirror blob at its add-commit carries the row")
            for sid in ADOPTED:
                if sid not in rows:
                    c8.append(f"{sid}: the measured revision does not carry the row")
        add("C8_mirror_bytes", c8, {
            "mirror_rows": len(parse_registry(mirror_text)) if mirror_text else 0,
            "registry_rows": len(rows),
        })
    except Exception as exc:  # unevaluable evidence is exit 2, never a silent miss
        return 2, results + [{
            "check": "exception",
            "state": "unevaluable",
            "notes": [f"{type(exc).__name__}: {exc}"],
            "facts": {},
        }]

    if any(r["state"] == "unevaluable" for r in results):
        return 2, results
    if all(r["state"] == "pass" for r in results):
        return 0, results
    return 1, results


# --------------------------------------------------------------------------- selftest


def _commit(fixture_dir: str, files: dict[str, str], message: str) -> None:
    for path, content in files.items():
        target = os.path.join(fixture_dir, path)
        os.makedirs(os.path.dirname(target), exist_ok=True)
        with open(target, "w", encoding="utf-8") as fh:
            fh.write(content)
    subprocess.run(["git", "-C", fixture_dir, "add", "-A"], check=True)
    subprocess.run(
        ["git", "-C", fixture_dir, "-c", "user.email=selftest@local", "-c",
         "user.name=selftest", "commit", "-q", "--allow-empty", "-m", message],
        check=True,
    )


def _repo(fixture_dir: str, pre: dict[str, str], post: dict[str, str]) -> str:
    """Build a sandbox git repo: `pre` is the mirror/evidence commit, `post` the append."""
    os.makedirs(fixture_dir, exist_ok=True)
    subprocess.run(["git", "init", "-q", fixture_dir], check=True)
    _commit(fixture_dir, pre, "wave evidence and pre-append mirror")
    _commit(fixture_dir, post, "append registry rows and entries")
    rc, out = git(fixture_dir, "rev-parse", "HEAD")
    return out.strip()


def selftest() -> int:
    rev = os.environ.get("KAKE_R52_SELFTEST_REV")
    if not rev:
        rc, out = git(os.getcwd(), "rev-parse", "HEAD")
        if rc != 0:
            print("selftest: cannot resolve HEAD", file=sys.stderr)
            return 2
        rev = out.strip()
    root = os.getcwd()
    base_files: dict[str, str] = {}
    for rel in (REGISTRY, LESSON, RECEIPTS, MIRROR, MIRROR_PIN,
                f"{CENSUS_DIR}/census-argv.txt", f"{CENSUS_DIR}/census-stdout.txt",
                f"{CENSUS_DIR}/census-exit.txt", *ADOPTED.values(),
                *(f"{SOURCES_DIR}/{sid}.html" for sid in ADOPTED)):
        raw = show(root, rev, rel)
        if raw is None:
            print(f"selftest: missing round-52 evidence {rel}", file=sys.stderr)
            return 2
        base_files[rel] = raw

    def clone(mutate) -> dict[str, str]:
        files = dict(base_files)
        mutate(files)
        return files

    def load(rel):
        return json.loads(base_files[rel])

    def row_line(sid: str) -> str:
        for line in base_files[REGISTRY].split("\n"):
            if line.startswith(f"| {sid} |"):
                return line
        raise KeyError(sid)

    fixtures: dict[str, dict[str, str]] = {"pass": dict(base_files)}

    def f_missing_entry(files):
        del files[ADOPTED["S374"]]
    fixtures["fail_missing_entry"] = clone(f_missing_entry)

    def f_no_cite(files):
        body = files[ADOPTED["S329"]]
        files[ADOPTED["S329"]] = body.replace("S329", "S999")
    fixtures["fail_no_cite"] = clone(f_no_cite)

    def f_row_short(files):
        line = row_line("S312")
        files[REGISTRY] = files[REGISTRY].replace(line, "|".join(line.split("|")[:-2]) + " |")
    fixtures["fail_row_short"] = clone(f_row_short)

    def f_usedby(files):
        files[REGISTRY] = files[REGISTRY].replace(
            "| 180d | corpus/knowledge/yahoo-japan-rel-nofollow-semantics.md |",
            "| 180d | corpus/knowledge/crawler-identity.md |",
        )
    fixtures["fail_usedby"] = clone(f_usedby)

    def f_lesson_quote(files):
        files[LESSON] = files[LESSON].replace(
            "このリンク先のウェブページの巡回を推奨していない",
            "このリンク先のウェブページの巡回を推奨しています",
        )
    fixtures["fail_lesson_quote"] = clone(f_lesson_quote)

    def f_entry_quote(files):
        files[ADOPTED["S312"]] = files[ADOPTED["S312"]].replace(
            "手机页使用了ajax等异步加载的方法加载内容主体",
            "手机页使用了脚本等异步加载的方法加载内容主体",
        )
    fixtures["fail_entry_quote"] = clone(f_entry_quote)

    def f_receipt_sha(files):
        receipts = load(RECEIPTS)
        receipts["sources"]["S329"]["sha256"] = "0" * 64
        files[RECEIPTS] = json.dumps(receipts, ensure_ascii=False, indent=1)
    fixtures["fail_receipt_sha"] = clone(f_receipt_sha)

    def f_receipt_status(files):
        receipts = load(RECEIPTS)
        receipts["sources"]["S374"]["httpStatus"] = 500
        files[RECEIPTS] = json.dumps(receipts, ensure_ascii=False, indent=1)
    fixtures["fail_receipt_status"] = clone(f_receipt_status)

    def f_receipt_url(files):
        receipts = load(RECEIPTS)
        receipts["sources"]["S312"]["url"] = "https://ziyuan.baidu.com/college/courseinfo?id=267&page=16"
        files[RECEIPTS] = json.dumps(receipts, ensure_ascii=False, indent=1)
    fixtures["fail_receipt_url"] = clone(f_receipt_url)

    def f_census_exit(files):
        files[f"{CENSUS_DIR}/census-exit.txt"] = "exit=1\n"
    fixtures["fail_census_exit"] = clone(f_census_exit)

    def f_census_e04(files):
        files[f"{CENSUS_DIR}/census-stdout.txt"] = (
            base_files[f"{CENSUS_DIR}/census-stdout.txt"]
            + "file\tE04\tS329 duplicate source row\n"
        )
    fixtures["fail_census_e04"] = clone(f_census_e04)

    def f_mirror_contaminated(files):
        files[MIRROR] = files[MIRROR] + row_line("S374") + "\n"
    fixtures["fail_mirror_contaminated"] = clone(f_mirror_contaminated)

    def f_pin_sha(files):
        pin = load(MIRROR_PIN)
        pin["sha256"] = "f" * 64
        files[MIRROR_PIN] = json.dumps(pin, ensure_ascii=False, indent=1)
    fixtures["fail_pin_sha"] = clone(f_pin_sha)

    def f_registry_row_dropped(files):
        files[REGISTRY] = files[REGISTRY].replace(row_line("S329") + "\n", "")
    fixtures["fail_registry_row_dropped"] = clone(f_registry_row_dropped)

    def f_not_append_only(files):
        files[REGISTRY] = files[REGISTRY].replace(
            "| S263 | Google Search Central — Googlebot",
            "| S263 | Google Search Central — Googlebot (edited)",
        )
    fixtures["fail_not_append_only"] = clone(f_not_append_only)

    def f_empty_body(files):
        files[f"{SOURCES_DIR}/S312.html"] = ""
    fixtures["fail_empty_body"] = clone(f_empty_body)

    def f_bad_receipts(files):
        files[RECEIPTS] = "{not json"
    fixtures["fail_bad_receipts"] = clone(f_bad_receipts)

    work_root = os.path.join(root, SELFTEST_DIR, "work")
    if os.path.exists(work_root):
        shutil.rmtree(work_root)
    os.makedirs(work_root, exist_ok=True)
    passed = 0
    total = len(fixtures)
    failures: list[str] = []
    for name in sorted(fixtures):
        files = fixtures[name]
        work = os.path.join(work_root, name)
        pre = {k: v for k, v in files.items() if k not in (REGISTRY, LESSON)}
        post = {k: v for k, v in files.items() if k in (REGISTRY, LESSON)}
        fixture_rev = _repo(work, pre, post)
        code, results = run_checks(work, fixture_rev)
        expected = 0 if name == "pass" else (2 if name == "fail_bad_receipts" else 1)
        if code == expected:
            passed += 1
        else:
            failures.append(f"{name}: expected {expected}, got {code}")
            for r in results:
                for note in r["notes"][:2]:
                    failures.append(f"    {r['check']}: {note}")
    shutil.rmtree(work_root, ignore_errors=True)
    print(f"c52 quote-truth selftest: {passed}/{total} (fixture revision {rev[:12]})")
    for line in failures:
        print("  FAIL", line)
    return 0 if passed == total else 1


def main() -> int:
    parser = argparse.ArgumentParser(description="Round-52 quote-truth counter (C2)")
    parser.add_argument("--root", default=".")
    parser.add_argument("--revision", default=None)
    parser.add_argument("--selftest", action="store_true")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()
    if args.selftest:
        return selftest()
    if not args.revision:
        parser.error("--revision is required unless --selftest is used")
    code, results = run_checks(args.root, args.revision)
    passed = sum(1 for r in results if r["state"] == "pass")
    if args.json:
        body = {
            "schema": "kake-r52-c2-quote-truth-v1",
            "predicate": PREDICATE,
            "revision": args.revision,
            "adopted": ADOPTED,
            "checks": {
                r["check"]: {
                    "passed": r["state"] == "pass",
                    "state": r["state"],
                    "notes": r["notes"],
                    "facts": r["facts"],
                }
                for r in results
            },
            "conditions_passed": passed,
            "met": code == 0,
        }
        print(json.dumps(body, indent=1, ensure_ascii=False))
    else:
        print(f"C2 quote-truth {passed}/{len(ADOPTED) + 5} met={code == 0}  ({PREDICATE})")
        for r in results:
            print(f"  {r['check']} {r['state'].upper()}")
            for note in r["notes"]:
                print(f"    - {note}")
        print(f"  revision: {args.revision}")
    print(f"EXIT={code}")
    return code


if __name__ == "__main__":
    sys.exit(main())
