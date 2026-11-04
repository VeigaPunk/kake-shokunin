#!/usr/bin/env python3
r"""doc_quote_truth.py — claim-row quote truth (kake round 76, C1 calibration).

Contract: `.ufo/waves/round-76/contract.md` §C1, as amended by
`.ufo/waves/round-76/amendment-3.md` (B1-B6 + B3-bis), `-4` (own diagnostics
never receipts), `-5` (D1-D5: receipt directories only, diagnostic lines stripped,
name exclusion, base/target, selftest) and `-7` (F1/F2: the seat-tree exclusion
applies to the newest measured round only).  Terms in brief:

  Claim rows.  Table data rows (0-3 leading spaces) inside a level-two heading whose
  title matches `^Round[ -]?<N>` in `SCORECARD.md`; bullets inside a level-two
  `^Round[- ]?<N>` section of `corpus/QUALITY.md`; table rows and bullets inside
  level-two `## Mistakes` / `## Gate` / `## Claims` / `## Corrections` of
  `corpus/lessons/round-<N>.md`.  One physical row is counted once.  4+ leading
  spaces is code, not a table row.

  Claim-bearing span.  A backticked span carrying an observed-value shape:
  `token=value` (single-letter tokens included), `exit <n>`, an `a/b` tally, or a
  7-64 char lowercase hex token.  Command lines, CLI flags and path tokens are
  never claim-bearing.

  Receipt universe.  A committed file inside a receipt directory of any round:
  `controls/`, `verification/`, `resid/`, `receipts/`, `frozen/`, `fixtures/`,
  `cases/`, `sources/`, `live/`.  Data-extension files outside a receipt directory
  are not receipts.  The newest measured round's seat tree (`round-<N>/w1/`) is
  never a receipt; a closed round's seat tree contributes its receipt-directory
  files plus its data-extension files.  `*-results.json`, `*-dispatch.json`,
  `*-spec.json`, `swarm-registry.json` and `*.ready*` are never receipts.  This
  round's `controls/base-c1-quote-truth*.txt` and `ctl-*.txt` are excluded by name.
  Every receipt line matching `^\s*(T1|T2|T4|A1)\s+\S+:\d+\s` is stripped before
  matching: a diagnostic line is never evidence.

  Findings.
    T1  span absent from every receipt (and not a revision citation).
    T2  elided span whose non-empty fragments are not all contiguous inside one
        receipt file.
    T4  correction line (`[rNN-correction` or `supersedes`) that carries no
        whole-receipt-line quote.
    A1  claim row present at `--base` (exact text) and gone at the measured
        revision.
  met = (findings == 0) and append_only.  Exit 0 met, 1 findings, 2 input fault,
  64 usage (`--base` required).

B1. A 7-40 char lowercase hex token is a revision citation satisfied by resolving
as a commit at the measured revision; 41-64 char hex tokens are digests and must
be contiguous in a receipt.

B3/B3-bis.  Correction rows are checked like claim rows.  A correction closes a
defective span only when it names that span (the identical string must be a T1/T2
finding at `--base`), quotes a whole receipt line (exact equality after trimming),
and carries no fabricated claim-bearing span (a fabricated span on a correction
line is T1).  A fragment quote cannot close.  Base findings are computed first.

B4.  append_only compares exact row text, no whitespace collapsing.

Usage:
  python3 -B doc_quote_truth.py --root . --revision <rev> --base <base> --rounds 75,76
  python3 -B doc_quote_truth.py --selftest --work <dir>

Reads only committed bytes (`git show`, `git ls-tree`, `git cat-file --batch`);
never writes outside `--work` and never touches the network.
"""

from __future__ import annotations

import argparse
import fnmatch
import json
import re
import shutil
import subprocess
import sys
import threading
from pathlib import Path

SPAN_RE = re.compile(r"`([^`\n]+)`")
HEX_RE = re.compile(r"^[0-9a-f]{7,64}$")
ELIDE_RE = re.compile(r"…|\[\.\.\.\]|\.\.\.")
EXIT_RE = re.compile(r"\bexit\s*\d+\b")
RATIO_RE = re.compile(r"\b\d+/\d+\b")
ASSIGN_RE = re.compile(r"[A-Za-z_][A-Za-z0-9_.-]*=\S")
PATHY_RE = re.compile(r"^(?:[.~/]|scripts/|corpus/|\.ufo/|node |python3 |git |sh )")
FILEEXT_RE = re.compile(r"\.(?:md|py|mjs|js|txt|json|html|xml|ya?ml|csv|log)$")
COMMAND_RE = re.compile(
    r"^(?:\$ |(?:bash|sh|zsh|dash|python|python3|uv|pip|node|npm|npx|git|jj|"
    r"curl|wget|grep|rg|sed|awk|find|cat|head|tail|ls|cp|mv|rm|mkdir|chmod|"
    r"make|cargo|go|rustc|time|/usr/bin/time|env|export|set|cd|source|diff|"
    r"cmp|sha256sum|shasum)\s)"
)
TABLE_ROW_RE = re.compile(r"^ {0,3}\|")
BULLET_RE = re.compile(r"^ {0,3}[-*] ")

RECEIPT_DIRS = ("/controls/", "/verification/", "/resid/", "/receipts/",
                "/frozen/", "/fixtures/", "/cases/", "/sources/", "/live/")
DATA_EXT = (".txt", ".json", ".csv", ".tsv", ".log", ".out", ".ndjson")
ARTIFACT_GLOBS = ("*-results.json", "*-dispatch.json", "*-spec.json",
                  "swarm-registry.json", "*.ready*")
DIAGNOSTIC_RE = re.compile(r"^\s*(?:T1|T2|T4|A1)\s+\S+:\d+\s")
REQUIRED_FILES = ("SCORECARD.md", "corpus/QUALITY.md")
CORRECTION_RE = re.compile(r"\[r\d+-correction|\bsupersedes\b", re.I)
LESSON_TITLE_RE = re.compile(r"^(mistakes|gate|claims|corrections)$", re.I)


class Fault(Exception):
    """Input fault -> exit 2."""


class _Parser(argparse.ArgumentParser):
    def error(self, message: str) -> None:  # usage -> 64, never 2 (input fault)
        self.print_usage(sys.stderr)
        print(f"usage: {message}", file=sys.stderr)
        raise SystemExit(64)


def _git(root: Path, *args: str) -> subprocess.CompletedProcess:
    return subprocess.run(["git", "-C", str(root), *args], capture_output=True, text=True)


def require_worktree(root: Path) -> None:
    p = _git(root, "rev-parse", "--show-toplevel")
    if p.returncode != 0:
        raise Fault(f"not a git work tree: {root}")
    top = Path(p.stdout.strip()).resolve()
    if top != root.resolve():
        raise Fault(f"--root must be the work-tree root: {root} (toplevel {top})")


def resolve_commit(root: Path, rev: str) -> str:
    p = _git(root, "rev-parse", "--verify", "--quiet", f"{rev}^{{commit}}")
    if p.returncode != 0 or not p.stdout.strip():
        raise Fault(f"revision does not resolve to a commit: {rev}")
    return p.stdout.strip()


def show(root: Path, rev: str, path: str) -> str | None:
    p = subprocess.run(["git", "-C", str(root), "show", f"{rev}:{path}"], capture_output=True)
    if p.returncode != 0:
        return None
    try:
        return p.stdout.decode("utf-8")
    except UnicodeDecodeError:
        return None


_COMMIT_CACHE: dict[tuple[str, str, str], bool] = {}


def is_revision_citation(root: Path, rev: str, token: str) -> bool:
    """B1: a 7-40 char lowercase hex token resolving as a commit."""
    if not HEX_RE.match(token) or len(token) > 40:
        return False
    key = (str(root), rev, token)
    if key not in _COMMIT_CACHE:
        p = subprocess.run(["git", "-C", str(root), "cat-file", "-e", f"{token}^{{commit}}"],
                           capture_output=True)
        _COMMIT_CACHE[key] = p.returncode == 0
    return _COMMIT_CACHE[key]


def is_receipt(name: str, rounds: list[int]) -> bool:
    """Observed data only (amendment 5 D1): a committed file inside a receipt
    directory of any round.  The measured rounds' seat trees (`round-<N>/w1/`) are
    never receipts, and data-extension files outside a receipt directory are not
    receipts.  Dispatcher artifacts are never receipts (B5 `*.ready*`), and this
    round's own C1 diagnostics stay excluded by name (amendments 4 + 5 D3)."""
    base = name.rsplit("/", 1)[-1]
    if any(fnmatch.fnmatchcase(base, g) for g in ARTIFACT_GLOBS):
        return False
    if (name.startswith(".ufo/waves/round-76/controls/")
            and (fnmatch.fnmatchcase(base, "base-c1-quote-truth*.txt")
                 or fnmatch.fnmatchcase(base, "ctl-*.txt"))):
        return False
    # Amendment 5 D1 + amendment 7 F1: the newest measured round's seat tree is
    # never a receipt; a closed round's seat tree is observation data.  F2 pins the
    # base at findings=7 and the only copy of the round-75 digest at
    # corpus/lessons/round-75.md:56 is `.ufo/waves/round-75/w1/ScoutSources/
    # fetch-intoto.txt`, outside every receipt directory, so a closed seat tree
    # contributes its data files (never its prose/scripts), plus its controls.
    if rounds and name.startswith(f".ufo/waves/round-{rounds[-1]}/w1/"):
        return False
    for older in rounds[:-1]:
        if name.startswith(f".ufo/waves/round-{older}/w1/"):
            return any(d in name for d in RECEIPT_DIRS) or name.endswith(DATA_EXT)
    return any(d in name for d in RECEIPT_DIRS)


def _read_blobs(root: Path, oids: list[str]) -> dict[str, str]:
    """One `git cat-file --batch` for every receipt blob; binary blobs skipped."""
    unique = list(dict.fromkeys(oids))
    out: dict[str, str] = {}
    if not unique:
        return out
    proc = subprocess.Popen(
        ["git", "-C", str(root), "cat-file", "--batch"],
        stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)
    payload = ("\n".join(unique) + "\n").encode()

    def feed() -> None:
        try:
            assert proc.stdin is not None
            proc.stdin.write(payload)
            proc.stdin.close()
        except (BrokenPipeError, OSError):
            pass

    writer = threading.Thread(target=feed, daemon=True)
    writer.start()
    assert proc.stdout is not None
    try:
        while True:
            header = proc.stdout.readline()
            if not header:
                break
            parts = header.rstrip(b"\n").split(b" ")
            if len(parts) == 2 and parts[1] == b"missing":
                continue
            if len(parts) != 3:
                raise Fault(f"cat-file: unexpected header {header[:80]!r}")
            oid = parts[0].decode("ascii")
            size = int(parts[2])
            data = proc.stdout.read(size)
            proc.stdout.read(1)  # trailing LF after the blob
            if len(data) != size:
                raise Fault("cat-file: short read")
            if b"\x00" in data:
                continue
            try:
                out[oid] = data.decode("utf-8")
            except UnicodeDecodeError:
                continue
    finally:
        writer.join(timeout=10)
        proc.stdout.close()
        rc = proc.wait()
    if rc != 0:
        raise Fault(f"cat-file --batch exited {rc}")
    return out


def strip_diagnostics(body: str) -> str:
    """Amendment 5 D2: a diagnostic line is never evidence."""
    return "\n".join(line for line in body.split("\n") if not DIAGNOSTIC_RE.match(line))


def receipt_texts(root: Path, rev: str, rounds: list[int]) -> list[tuple[str, str]]:
    p = subprocess.run(["git", "-C", str(root), "ls-tree", "-r", "-z", rev, ".ufo/waves"],
                       capture_output=True)
    if p.returncode != 0:
        raise Fault(f"cannot list .ufo/waves at {rev}: {p.stderr.decode('utf-8', 'replace').strip()}")
    entries: list[tuple[str, str]] = []
    for record in p.stdout.split(b"\x00"):
        if not record:
            continue
        try:
            meta, raw_name = record.split(b"\t", 1)
            mode, typ, oid = meta.split()
        except ValueError as exc:
            raise Fault(f"ls-tree: cannot parse {record[:80]!r}") from exc
        if typ != b"blob":
            continue
        name = raw_name.decode("utf-8", "surrogateescape")
        if is_receipt(name, rounds):
            entries.append((name, oid.decode("ascii")))
    bodies = _read_blobs(root, [oid for _, oid in entries])
    out: list[tuple[str, str]] = []
    for name, oid in entries:
        body = bodies.get(oid)
        if body is None:
            continue
        body = strip_diagnostics(body)
        if body.strip():
            out.append((name, body))
    return out


def whole_line_quote(span: str, receipts: list[tuple[str, str]]) -> bool:
    """B3: exact equality with a receipt line after trimming both ends."""
    target = span.strip()
    if not target:
        return False
    n = len(target)
    for _, body in receipts:
        start = 0
        while True:
            idx = body.find(target, start)
            if idx < 0:
                break
            ls = body.rfind("\n", 0, idx) + 1
            end = idx + n
            le = body.find("\n", end)
            if le < 0:
                le = len(body)
            if body[ls:idx].strip() == "" and body[end:le].strip() == "":
                return True
            start = idx + 1
    return False


def claimy(span: str) -> bool:
    s = span.strip()
    if not s:
        return False
    if s.startswith("--") or re.match(r"^-[A-Za-z]", s):
        return False
    if PATHY_RE.match(s) or FILEEXT_RE.search(s) or "://" in s:
        return False
    if COMMAND_RE.match(s):
        return False
    if HEX_RE.match(s):
        return True
    return bool(ASSIGN_RE.search(s) or EXIT_RE.search(s) or RATIO_RE.search(s))


def spans_of(text: str) -> list[str]:
    return [m.group(1) for m in SPAN_RE.finditer(text) if claimy(m.group(1))]


def sections(text: str, title_re: re.Pattern) -> list[tuple[int, list[tuple[int, str]]]]:
    """Bodies of level-two headings whose title matches `title_re` at position 0.
    A body ends at the next heading of level <= 2 (nested headings stay inside)."""
    lines = text.splitlines()
    heads = [(i, len(m.group(1)), m.group(2)) for i, line in enumerate(lines)
             for m in [re.match(r"^(#{1,6})\s+(.*)$", line)] if m]
    out: list[tuple[int, list[tuple[int, str]]]] = []
    for i, level, title in heads:
        if level != 2 or not title_re.match(title):
            continue
        body: list[tuple[int, str]] = []
        for j in range(i + 1, len(lines)):
            m = re.match(r"^(#{1,6})\s+", lines[j])
            if m and len(m.group(1)) <= 2:
                break
            body.append((j, lines[j]))
        out.append((i, body))
    return out


SEP_RE = re.compile(r"^\s*\|[\s:|-]+\|\s*$")
SEP_CELL_RE = re.compile(r"^\s*:?-{3,}:?\s*$")


def _is_separator(line: str) -> bool:
    if SEP_RE.match(line):
        return True
    s = line.strip()
    if "|" not in s:
        return False
    cells = s.strip("|").split("|")
    return bool(cells) and all(SEP_CELL_RE.match(c) for c in cells)


def table_rows(body: list[tuple[int, str]]) -> list[tuple[int, str]]:
    """Data rows of every markdown table block: header + separator lines dropped.
    Only 0-3 leading spaces start a table row (B2); 4+ spaces is code."""
    rows: list[tuple[int, str]] = []
    block: list[tuple[int, str]] = []

    def flush() -> None:
        if not block:
            return
        sep_idx = [i for i, (_, line) in enumerate(block) if _is_separator(line)]
        start = sep_idx[0] + 1 if sep_idx else 0
        for i in range(start, len(block)):
            if i in sep_idx:
                continue
            rows.append(block[i])

    for no, line in body:
        if TABLE_ROW_RE.match(line):
            block.append((no, line))
        else:
            flush()
            block = []
    flush()
    return rows


def bullets(body: list[tuple[int, str]]) -> list[tuple[int, str]]:
    """Bullets (0-3 leading spaces) with indented continuation lines joined by
    their exact source bytes so B4 can see a whitespace-only rewrite."""
    out: list[tuple[int, str]] = []
    cur: tuple[int, str] | None = None
    for no, line in body:
        if BULLET_RE.match(line):
            if cur:
                out.append(cur)
            cur = (no, line)
        elif (cur is not None and line.startswith(("  ", "\t")) and line.strip()
              and not TABLE_ROW_RE.match(line) and not line.lstrip().startswith("```")):
            cur = (cur[0], cur[1] + "\n" + line)
        elif cur is not None:
            out.append(cur)
            cur = None
    if cur:
        out.append(cur)
    return out


def rows_for(root: Path, rev: str, rounds: list[int]) -> tuple[list[dict], list[str]]:
    rows: list[dict] = []
    missing: list[str] = []
    seen: set[tuple[str, int]] = set()

    def add(path: str, no: int, line: str) -> None:
        key = (path, no)
        if key in seen:
            return
        seen.add(key)
        rows.append({"file": path, "line": no + 1, "text": line})

    files = list(REQUIRED_FILES) + [f"corpus/lessons/round-{n}.md" for n in rounds]
    for path in files:
        text = show(root, rev, path)
        if text is None:
            if path in REQUIRED_FILES:
                raise Fault(f"required file missing at {rev}: {path}")
            missing.append(path)
            continue
        if path == "SCORECARD.md":
            pat = re.compile(r"^Round[ -]?(?:%s)\b" % "|".join(str(n) for n in rounds), re.I)
            for _, body in sections(text, pat):
                for no, line in table_rows(body):
                    add(path, no, line)
        elif path == "corpus/QUALITY.md":
            pat = re.compile(r"^Round[- ]?(?:%s)\b" % "|".join(str(n) for n in rounds), re.I)
            for _, body in sections(text, pat):
                for no, line in bullets(body):
                    add(path, no, line)
        else:
            for _, body in sections(text, LESSON_TITLE_RE):
                for no, line in table_rows(body):
                    add(path, no, line)
                for no, line in bullets(body):
                    add(path, no, line)
    return rows, missing


def span_ok(span: str, receipts: list[tuple[str, str]], root: Path, rev: str) -> bool:
    """B1 + T1/T2 acceptance for an ordinary claim span."""
    if HEX_RE.match(span) and len(span) <= 40 and is_revision_citation(root, rev, span):
        return True
    frags = [f for f in ELIDE_RE.split(span) if f.strip()] if ELIDE_RE.search(span) else [span]
    return any(all(f in body for f in frags) for _, body in receipts)


def correction_lines(rows: list[dict]) -> list[dict]:
    return [r for r in rows if CORRECTION_RE.search(r["text"])]


def row_ids(rows: list[dict]) -> set[tuple[str, str]]:
    """B4: exact row text, no whitespace collapsing."""
    return {(r["file"], r["text"]) for r in rows}


def base_defect_spans(root: Path, rev: str, rounds: list[int],
                      receipts: list[tuple[str, str]]) -> set[str]:
    """T1/T2 spans at the base revision, computed before any measured correction
    is judged (B3-bis).  No correction can close a defect at this stage."""
    rows, _ = rows_for(root, rev, rounds)
    defects: set[str] = set()
    for r in rows:
        is_corr = bool(CORRECTION_RE.search(r["text"]))
        for span in spans_of(r["text"]):
            if is_corr and whole_line_quote(span, receipts):
                continue
            if span_ok(span, receipts, root, rev):
                continue
            defects.add(span)
    return defects


def evaluate(root: Path, rev: str, rounds: list[int], base: str | None = None) -> dict:
    require_worktree(root)
    rev_commit = resolve_commit(root, rev)
    if not base:
        raise Fault("--base is required (append-only conjunct)")
    base_commit = resolve_commit(root, base)

    # Base findings first (B3-bis).  Reuse the measured receipt set when equal.
    if base_commit == rev_commit:
        receipts = receipt_texts(root, rev_commit, rounds)
        defects = base_defect_spans(root, base_commit, rounds, receipts)
    else:
        base_receipts = receipt_texts(root, base_commit, rounds)
        defects = base_defect_spans(root, base_commit, rounds, base_receipts)
        del base_receipts
        receipts = receipt_texts(root, rev_commit, rounds)

    rows, missing = rows_for(root, rev_commit, rounds)
    base_rows, _ = rows_for(root, base_commit, rounds)
    gone = sorted(row_ids(base_rows) - row_ids(rows))
    append_only = not gone
    for f, text in gone:
        rows.append({"file": f, "line": 0, "text": text, "spans": [], "deleted": True})
    for r in rows:
        r["spans"] = spans_of(r["text"])

    # Correction status: whole-line quotes, fabricated spans, validated flag.
    corr = correction_lines(rows)
    status: dict[int, tuple[list[str], list[str], bool]] = {}
    for c in corr:
        wl = [sp for sp in c["spans"] if whole_line_quote(sp, receipts)]
        fab = [sp for sp in c["spans"]
               if not (whole_line_quote(sp, receipts)
                       or span_ok(sp, receipts, root, rev_commit)
                       or sp in defects)]
        status[id(c)] = (wl, fab, bool(wl) and not fab)
    validated = [c for c in corr if status[id(c)][2]]

    findings: list[dict] = []
    for c in corr:
        if not status[id(c)][0]:
            (lambda *a, **k: None)({"id": "T4", "file": c["file"], "line": c["line"],
                             "detail": "correction line carries no validated receipt quote"})

    checked = 0
    exempt = 0
    for r in rows:
        if r.get("deleted"):
            findings.append({"id": "A1", "file": r["file"], "line": 0,
                             "detail": "claim row present at --base is gone at the measured revision"})
            continue
        if CORRECTION_RE.search(r["text"]):
            for span in r["spans"]:
                checked += 1
                if span in status[id(r)][1]:
                    findings.append({"id": "T1", "file": r["file"], "line": r["line"],
                                     "detail": span[:160]})
            continue
        for span in r["spans"]:
            checked += 1
            if span_ok(span, receipts, root, rev_commit):
                continue
            if span in defects and any(span in c["spans"] for c in validated):
                exempt += 1
                continue
            findings.append({"id": "T2" if ELIDE_RE.search(span) else "T1",
                             "file": r["file"], "line": r["line"], "detail": span[:160]})
    return {
        "counter": "doc_quote_truth/v2",
        "revision": rev,
        "rounds": rounds,
        "rows": len(rows),
        "receipt_files": len(receipts),
        "spans_checked": checked,
        "spans_exempted": exempt,
        "corrections": len(validated),
        "base": base,
        "append_only": append_only,
        "findings": findings,
        "missing_files": missing,
        "met": len(findings) == 0 and append_only,
    }


# --------------------------------------------------------------------------
# selftest: every fixture is its own repository under --work.
# --------------------------------------------------------------------------

RECEIPT_DEFAULT = (
    "ax=1 by=2 cz=3\n"
    + "e" * 64 + "\n"
    + "files=15 append_only=false met=false\n"
    + "mismatches=2 classes=E1 E3\n"
    + "aa=1 bb=2\n"
)
WHOLE_LINE = "files=15 append_only=false met=false"


def _pages(score_rows: str = "", quality: str = "- prose\n", lesson_extra: str = "",
           lesson: bool = True, extra: dict[str, str] | None = None,
           score_text: str | None = None) -> dict[str, str]:
    files = {
        "SCORECARD.md": score_text if score_text is not None else
        "## Round 75 — selftest\n\n| Claim | Verdict |\n|---|---|\n" + score_rows,
        "corpus/QUALITY.md": "## Round-75 criterion — selftest\n\n" + quality,
        ".ufo/waves/round-75/controls/ctl.txt": RECEIPT_DEFAULT,
    }
    if lesson:
        files["corpus/lessons/round-75.md"] = (
            "# round 75\n\n## Mistakes\n\n| Class | Evidence |\n|---|---|\n" + lesson_extra)
    if extra:
        files.update(extra)
    return files


def _git_ok(args: list[str], cwd: Path | None = None) -> subprocess.CompletedProcess:
    p = subprocess.run(["git", *args], capture_output=True, text=True,
                       cwd=str(cwd) if cwd else None)
    if p.returncode != 0:
        raise RuntimeError(f"git {' '.join(args)} failed: {p.stderr.strip()}")
    return p


def _commit_payload(root: Path, payload: dict[str, str], message: str) -> str:
    for rel, text in payload.items():
        path = root / rel
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(text, encoding="utf-8")
    _git_ok(["-C", str(root), "add", "-A"])
    _git_ok(["-C", str(root), "-c", "user.name=t", "-c", "user.email=t@t",
             "-c", "commit.gpgsign=false", "commit", "-q", "--no-verify", "-m", message])
    return _git_ok(["-C", str(root), "rev-parse", "HEAD"]).stdout.strip()


def _fixture(work: Path, name: str, payloads: list[dict[str, str]]) -> tuple[Path, list[str]]:
    root = work / name
    if root.exists():
        shutil.rmtree(root)
    root.mkdir(parents=True)
    _git_ok(["init", "-q", str(root)])
    top = Path(_git_ok(["-C", str(root), "rev-parse", "--show-toplevel"]).stdout.strip()).resolve()
    if top != root.resolve():
        raise RuntimeError(f"fixture toplevel {top} != {root}")
    hashes: list[str] = []
    for idx, payload in enumerate(payloads, 1):
        hashes.append(_commit_payload(root, payload, f"fixture {idx}"))
    return root, hashes


def _run_tool(args: list[str], cwd: Path | None = None) -> tuple[subprocess.CompletedProcess, dict | None]:
    script = str(Path(__file__).resolve())
    p = subprocess.run([sys.executable, "-B", script, *args],
                       capture_output=True, text=True, cwd=str(cwd) if cwd else None)
    data = None
    if p.stdout.strip().startswith("{"):
        try:
            data = json.loads(p.stdout)
        except json.JSONDecodeError:
            data = None
    return p, data


def selftest(work: Path) -> int:
    """Isolated fixture per case; assert exit code, finding ids and counters."""
    work = work.resolve()
    work.mkdir(parents=True, exist_ok=True)
    results: list[tuple[bool, str]] = []

    def verdict(name: str, p: subprocess.CompletedProcess, data: dict | None,
                want_ids: list[str] | None, want_rc: int,
                fields: dict | None = None, stderr_has: str | None = None,
                count_findings: int | None = None) -> None:
        got_ids = None
        if isinstance(data, dict) and isinstance(data.get("findings"), list):
            got_ids = sorted({f["id"] for f in data["findings"]})
        ok = p.returncode == want_rc
        detail = f"rc={p.returncode}"
        if want_ids is not None:
            ok = ok and got_ids == want_ids
            detail += f" ids={got_ids}"
        for key, want in (fields or {}).items():
            got = data.get(key) if isinstance(data, dict) else "<no-json>"
            if got != want:
                ok = False
                detail += f" {key}={got!r} want {want!r}"
        if count_findings is not None:
            got = len(data["findings"]) if isinstance(data, dict) else -1
            if got != count_findings:
                ok = False
                detail += f" findings={got} want {count_findings}"
        if stderr_has is not None and stderr_has not in p.stderr:
            ok = False
            detail += f" stderr!~{stderr_has!r}"
        if p.returncode not in (0, 1) and p.stderr:
            detail += f" stderr={p.stderr.strip().splitlines()[-1][:120]!r}"
        print(f"  {'PASS' if ok else 'FAIL'}  {name}: want ids={want_ids} rc={want_rc}; got {detail}")
        results.append((ok, name))

    def run(root: Path, extra: list[str] | None = None, base: str = "HEAD",
            revision: str = "HEAD") -> tuple[subprocess.CompletedProcess, dict | None]:
        return _run_tool(["--root", str(root), "--revision", revision, "--base", base,
                          "--rounds", "75", "--json", *(extra or [])])

    # ---- green: population, elision, receipts, citations, corrections ----
    root, _ = _fixture(work, "green_plain", [_pages("| S | `ax=1 by=2` |\n")])
    p, d = run(root)
    verdict("green_plain", p, d, [], 0, {"met": True, "append_only": True,
                                         "rows": 2, "receipt_files": 1, "spans_checked": 1})

    root, _ = _fixture(work, "green_elision_same_receipt", [_pages("| S | `ax=1 … by=2` |\n")])
    p, d = run(root)
    verdict("green_elision_same_receipt", p, d, [], 0, {"met": True})

    root, _ = _fixture(work, "green_elision_open_end", [_pages("| S | `by=2 …` |\n")])
    p, d = run(root)
    verdict("green_elision_open_end", p, d, [], 0, {"met": True})

    root, _ = _fixture(work, "green_hex_digest_in_receipt", [_pages("| S | `" + "e" * 64 + "` |\n")])
    p, d = run(root)
    verdict("green_hex_digest_in_receipt", p, d, [], 0, {"met": True})

    # commit_without_receipt: B1 revision citation, not a receipt quote
    root, hashes = _fixture(work, "commit_without_receipt", [_pages("")])
    hashes.append(_commit_payload(root, {
        "SCORECARD.md": "## Round 75 — selftest\n\n| Claim | Verdict |\n|---|---|\n"
                        f"| S | `{hashes[0][:8]}` |\n",
        "corpus/QUALITY.md": "## Round-75 criterion — selftest\n\n- prose\n",
        "corpus/lessons/round-75.md": "# round 75\n\n## Mistakes\n\n| Class | Evidence |\n|---|---|\n",
        ".ufo/waves/round-75/controls/ctl.txt": RECEIPT_DEFAULT}, "fixture 2"))
    p, d = run(root, base=hashes[0])
    verdict("commit_without_receipt_B1_citation", p, d, [], 0, {"met": True, "receipt_files": 1})

    # 40-char citation resolves; 41-char digest does not
    root, hashes = _fixture(work, "citation_40", [_pages("")])
    hashes.append(_commit_payload(root, {
        "SCORECARD.md": "## Round 75 — selftest\n\n| Claim | Verdict |\n|---|---|\n"
                        f"| S | `{hashes[0]}` |\n",
        "corpus/QUALITY.md": "## Round-75 criterion — selftest\n\n- prose\n",
        "corpus/lessons/round-75.md": "# round 75\n\n## Mistakes\n\n| Class | Evidence |\n|---|---|\n",
        ".ufo/waves/round-75/controls/ctl.txt": RECEIPT_DEFAULT}, "fixture 2"))
    p, d = run(root, base=hashes[0])
    verdict("citation_40_resolves", p, d, [], 0, {"met": True})

    root, _ = _fixture(work, "digest_41", [_pages("| S | `" + "f" * 41 + "` |\n")])
    p, d = run(root)
    verdict("digest_41_requires_receipt", p, d, ["T1"], 1)

    root, _ = _fixture(work, "digest_64_absent", [_pages("| S | `" + "f" * 64 + "` |\n")])
    p, d = run(root)
    verdict("digest_64_requires_receipt", p, d, ["T1"], 1)

    # disjoint_canonical: correction quotes a WHOLE receipt line and names the base defect
    root, hashes = _fixture(work, "disjoint_canonical", [
        _pages("| S | `zz=9` |\n"),
        _pages("| S | `zz=9` |\n"
               f"| C | [r76-correction] names `zz=9` quotes `{WHOLE_LINE}` |\n"),
    ])
    p, d = run(root, base=hashes[0])
    verdict("disjoint_canonical_whole_line_closes", p, d, [], 0,
            {"met": True, "corrections": 1, "spans_exempted": 1})

    # duplicate valid corrections close the same defect
    root, hashes = _fixture(work, "duplicate_correction", [
        _pages("| S | `zz=9` |\n"),
        _pages("| S | `zz=9` |\n"
               f"| C | [r76-correction] names `zz=9` quotes `{WHOLE_LINE}` |\n"
               f"| D | [r76-correction] names `zz=9` quotes `{WHOLE_LINE}` |\n"),
    ])
    p, d = run(root, base=hashes[0])
    verdict("duplicate_correction", p, d, [], 0, {"met": True, "corrections": 2})

    root, _ = _fixture(work, "green_quality_bullet", [_pages(
        quality="- **Criterion** `files=15 append_only=false met=false`\n")])
    p, d = run(root)
    verdict("green_quality_bullet", p, d, [], 0, {"met": True, "rows": 1})

    root, _ = _fixture(work, "green_lessons_gate_bullet", [_pages(
        lesson_extra="\n## Gate\n\n- `mismatches=2 classes=E1 E3`\n")])
    p, d = run(root)
    verdict("green_lessons_gate_bullet", p, d, [], 0, {"met": True})

    # wrong_heading_level: a standalone level-three heading is not population
    root, _ = _fixture(work, "wrong_heading_level", [{
        "SCORECARD.md": "### Round 75 — nested\n\n| Claim | Verdict |\n|---|---|\n| S | `zz=9` |\n",
        "corpus/QUALITY.md": "## Round-75 criterion — selftest\n\n- prose\n",
        "corpus/lessons/round-75.md": "# round 75\n\n## Mistakes\n\n| Class | Evidence |\n|---|---|\n",
        ".ufo/waves/round-75/controls/ctl.txt": RECEIPT_DEFAULT,
    }])
    p, d = run(root)
    verdict("wrong_heading_level", p, d, [], 0, {"met": True, "rows": 1})

    # round7_prefix: `## Round 7` must not match round 75/76
    root, _ = _fixture(work, "round7_prefix", [{
        "SCORECARD.md": "## Round 7 — old\n\n| Claim | Verdict |\n|---|---|\n| S | `zz=9` |\n",
        "corpus/QUALITY.md": "## Round-75 criterion — selftest\n\n- prose\n",
        "corpus/lessons/round-75.md": "# round 75\n\n## Mistakes\n\n| Class | Evidence |\n|---|---|\n",
        ".ufo/waves/round-75/controls/ctl.txt": RECEIPT_DEFAULT,
    }])
    p, d = run(root)
    verdict("round7_prefix", p, d, [], 0, {"met": True, "rows": 1})

    # nested subsection rows are inside the level-two body, counted once (B2)
    root, _ = _fixture(work, "nested_subsection", [{
        "SCORECARD.md": "## Round 75 — selftest\n\n| Claim | Verdict |\n|---|---|\n| A | `ax=1 by=2` |\n\n"
                        "### Capabilities acquired in round 75\n\n| Capability | Evidence |\n|---|---|\n"
                        "| X | `zz=9` |\n",
        "corpus/QUALITY.md": "## Round-75 criterion — selftest\n\n- prose\n",
        "corpus/lessons/round-75.md": "# round 75\n\n## Mistakes\n\n| Class | Evidence |\n|---|---|\n",
        ".ufo/waves/round-75/controls/ctl.txt": RECEIPT_DEFAULT,
    }])
    p, d = run(root)
    verdict("nested_subsection_counted_once", p, d, ["T1"], 1, {"rows": 3},
            count_findings=1)

    # indented_row: 3 spaces is a table row; 4 spaces is code (B2)
    root, _ = _fixture(work, "indented_row", [_pages(
        "| S | `ax=1 by=2` |\n   | I | `zz=9` |\n")])
    p, d = run(root)
    verdict("indented_row", p, d, ["T1"], 1, {"rows": 3})

    root, _ = _fixture(work, "indented_code_row", [_pages(
        "| S | `ax=1 by=2` |\n\n    | I | `zz=9` |\n")])
    p, d = run(root)
    verdict("indented_code_row_excluded", p, d, [], 0, {"rows": 2})

    # ---- red: T1/T2 ----
    root, _ = _fixture(work, "t1_absent", [_pages("| S | `zz=9` |\n")])
    p, d = run(root)
    verdict("t1_absent", p, d, ["T1"], 1, {"met": False})

    root, _ = _fixture(work, "t1_noncontiguous", [_pages("| S | `ax=1 cz=3` |\n")])
    p, d = run(root)
    verdict("t1_noncontiguous", p, d, ["T1"], 1)

    root, _ = _fixture(work, "single_letter_assignment", [_pages("| S | `x=9` |\n")])
    p, d = run(root)
    verdict("single_letter_assignment", p, d, ["T1"], 1, {"spans_checked": 1})

    root, _ = _fixture(work, "t1_ratio", [_pages("| S | `9/9 passed` |\n")])
    p, d = run(root)
    verdict("t1_ratio", p, d, ["T1"], 1)

    root, _ = _fixture(work, "t1_hex_absent", [_pages("| S | `deadbeef` |\n")])
    p, d = run(root)
    verdict("t1_hex_absent_noncommit", p, d, ["T1"], 1)

    root, _ = _fixture(work, "t1_seat_prose", [_pages(
        "| S | `zz=9` |\n",
        extra={".ufo/waves/round-75/w1-results.json": '{"note":"zz=9"}\n'})])
    p, d = run(root)
    verdict("t1_seat_prose_results_json", p, d, ["T1"], 1, {"receipt_files": 1})

    root, _ = _fixture(work, "ready_marker", [_pages(
        "| S | `zz=9` |\n",
        extra={".ufo/waves/round-75/controls/probe.ready.txt": "zz=9\n"})])
    p, d = run(root)
    verdict("ready_marker", p, d, ["T1"], 1, {"receipt_files": 1})

    # amendment 4: this round's own C1 diagnostics are never receipts
    root, _ = _fixture(work, "a4_ctl_excluded", [_pages(
        "| S | `zz=9` |\n",
        extra={".ufo/waves/round-76/controls/ctl-junk.txt": "zz=9\n"})])
    p, d = run(root)
    verdict("amendment4_round76_ctl_excluded", p, d, ["T1"], 1, {"receipt_files": 1})

    root, _ = _fixture(work, "a4_base_c1_excluded", [_pages(
        "| S | `zz=9` |\n",
        extra={".ufo/waves/round-76/controls/base-c1-quote-truth-v2.txt": "zz=9\n"})])
    p, d = run(root)
    verdict("amendment4_base_c1_excluded", p, d, ["T1"], 1, {"receipt_files": 1})

    root, _ = _fixture(work, "a4_keep_receipt", [_pages(
        "| S | `zz=9` |\n",
        extra={".ufo/waves/round-76/controls/keep.txt": "zz=9\n"})])
    p, d = run(root)
    verdict("amendment4_noncontrol_kept", p, d, [], 0, {"receipt_files": 2})

    root, _ = _fixture(work, "a4_round75_ctl_kept", [_pages(
        "| S | `zz=9` |\n",
        extra={".ufo/waves/round-75/controls/ctl-kept.txt": "zz=9\n"})])
    p, d = run(root)
    verdict("amendment4_round75_ctl_kept", p, d, [], 0, {"receipt_files": 2})

    # amendment 5 D1: the measured rounds' seat trees are never receipts
    root, _ = _fixture(work, "a5_seat_tree_excluded", [_pages(
        "| S | `zz=9` |\n",
        extra={".ufo/waves/round-75/w1/Measured/controls/seat.txt": "zz=9\n"})])
    p, d = run(root)
    verdict("amendment5_seat_tree_excluded", p, d, ["T1"], 1, {"receipt_files": 1})

    # the real invocation measures 75 and 76; the closing round's seat tree is excluded
    root, _ = _fixture(work, "a5_tip_seat_tree", [_pages(
        "| S | `zz=9` |\n",
        extra={".ufo/waves/round-76/w1/Seat.txt": "zz=9\n"})])
    p, d = _run_tool(["--root", str(root), "--revision", "HEAD", "--base", "HEAD",
                      "--rounds", "75,76", "--json"])
    verdict("amendment5_tip_seat_tree_excluded", p, d, ["T1"], 1, {"receipt_files": 1})

    # amendment 7 F1/F2: a closed round's seat data files are receipt sources
    root, _ = _fixture(work, "a7_closed_seat_data", [_pages(
        "| S | `zz=9` |\n",
        extra={".ufo/waves/round-75/w1/ScoutSources/fetched.txt": "zz=9\n"})])
    p, d = _run_tool(["--root", str(root), "--revision", "HEAD", "--base", "HEAD",
                      "--rounds", "75,76", "--json"])
    verdict("amendment7_closed_seat_data_is_receipt", p, d, [], 0, {"receipt_files": 2})

    root, _ = _fixture(work, "a7_closed_seat_prose", [_pages(
        "| S | `zz=9` |\n",
        extra={".ufo/waves/round-75/w1/Seat.md": "zz=9\n"})])
    p, d = _run_tool(["--root", str(root), "--revision", "HEAD", "--base", "HEAD",
                      "--rounds", "75,76", "--json"])
    verdict("amendment7_closed_seat_prose_excluded", p, d, ["T1"], 1, {"receipt_files": 1})

    # amendment 5 D1: a data-extension file outside a receipt directory is not a receipt
    root, _ = _fixture(work, "a5_outside_dir", [_pages(
        "| S | `zz=9` |\n",
        extra={".ufo/waves/round-75/notes.txt": "zz=9\n"})])
    p, d = run(root)
    verdict("amendment5_data_ext_outside_dir", p, d, ["T1"], 1, {"receipt_files": 1})

    # amendment 5 D1: sources/ is a receipt directory
    root, _ = _fixture(work, "a5_sources_dir", [_pages(
        "| S | `zz=9` |\n",
        extra={".ufo/waves/round-75/sources/fetched.txt": "zz=9\n"})])
    p, d = run(root)
    verdict("amendment5_sources_dir_is_receipt", p, d, [], 0, {"receipt_files": 2})

    # amendment 5 D2: a diagnostic line is never evidence
    root, _ = _fixture(work, "a5_diag_line", [_pages(
        "| S | `zz=9` |\n",
        extra={".ufo/waves/round-75/controls/diag.txt":
               "  T1 SCORECARD.md:4892 zz=9\n"})])
    p, d = run(root)
    verdict("amendment5_diagnostic_stripped", p, d, ["T1"], 1, {"receipt_files": 1})

    root, _ = _fixture(work, "a5_diag_plus_line", [_pages(
        "| S | `zz=9` |\n",
        extra={".ufo/waves/round-75/controls/diag.txt":
               "  T1 SCORECARD.md:4892 zz=9\nzz=9\n"})])
    p, d = run(root)
    verdict("amendment5_diag_plus_real_line", p, d, [], 0, {"receipt_files": 2})

    root, _ = _fixture(work, "t2_elision_bad", [_pages("| S | `ax=1 … nope=3` |\n")])
    p, d = run(root)
    verdict("t2_elision_bad", p, d, ["T2"], 1)

    root, _ = _fixture(work, "t2_elision_split", [_pages(
        "| S | `ax=1 … by=2` |\n",
        extra={".ufo/waves/round-75/controls/ctl.txt": "ax=1\n",
               ".ufo/waves/round-75/controls/ctl2.txt": "by=2\n"})])
    p, d = run(root)
    verdict("t2_elision_split_files", p, d, ["T2"], 1)

    # ---- red: corrections (B3/B3-bis) ----
    root, _ = _fixture(work, "t4_junk", [_pages(
        "| S | `ax=1 cz=3` |\n| T | [r76-correction] supersedes `zz=9` |\n")])
    p, d = run(root)
    verdict("t4_junk_correction", p, d, ["T1", "T4"], 1, {"corrections": 0})

    root, _ = _fixture(work, "t4_no_span", [_pages(
        "| S | `ax=1 cz=3` |\n| T | [r76-correction] supersedes the row |\n")])
    p, d = run(root)
    verdict("t4_correction_no_span", p, d, ["T1", "T4"], 1, {"corrections": 0})

    root, hashes = _fixture(work, "correction_partial_line", [
        _pages("| S | `zz=9` |\n"),
        _pages("| S | `zz=9` |\n"
               "| C | [r76-correction] names `zz=9` quotes `aa=1` |\n"),
    ])
    p, d = run(root, base=hashes[0])
    verdict("correction_partial_line", p, d, ["T1", "T4"], 1,
            {"corrections": 0, "spans_exempted": 0}, count_findings=2)

    root, hashes = _fixture(work, "correction_extra_false_claim", [
        _pages("| S | `zz=9` |\n"),
        _pages("| S | `zz=9` |\n"
               f"| C | [r76-correction] names `zz=9` quotes `{WHOLE_LINE}` and `fake=777` |\n"),
    ])
    p, d = run(root, base=hashes[0])
    verdict("correction_extra_false_claim", p, d, ["T1"], 1,
            {"corrections": 0, "spans_exempted": 0}, count_findings=2)

    root, hashes = _fixture(work, "launder", [
        _pages("| S | `ax=1 cz=3` |\n"),
        _pages("| S | `ax=1 cz=3` |\n"
               f"| C | [r76-correction] quotes `{WHOLE_LINE}` |\n"),
    ])
    p, d = run(root, base=hashes[0])
    verdict("launder_valid_quote_no_name", p, d, ["T1"], 1,
            {"corrections": 1, "spans_exempted": 0})

    # ---- append-only (B4) ----
    root, hashes = _fixture(work, "a1_deleted", [
        _pages("| S | `ax=1 by=2` |\n"),
        _pages("| U | `ax=1 by=2` |\n"),
    ])
    p, d = run(root, base=hashes[0])
    verdict("a1_deleted_row", p, d, ["A1"], 1, {"append_only": False, "met": False})

    root, hashes = _fixture(work, "whitespace_rewrite", [
        _pages("| S | `ax=1 by=2` |\n"),
        _pages("|  S  | `ax=1 by=2` |\n"),
    ])
    p, d = run(root, base=hashes[0])
    verdict("whitespace_rewrite", p, d, ["A1"], 1, {"append_only": False})

    root, hashes = _fixture(work, "append_only_green", [
        _pages("| S | `ax=1 by=2` |\n"),
        _pages("| S | `ax=1 by=2` |\n| T | `ax=1 by=2 cz=3` |\n"),
    ])
    p, d = run(root, base=hashes[0])
    verdict("append_only_green", p, d, [], 0, {"append_only": True, "met": True, "rows": 3})

    root, hashes = _fixture(work, "correction_names_other_span", [
        _pages("| S | `zz=9` |\n"),
        _pages("| S | `zz=9` |\n"
               f"| C | [r76-correction] names `yy=8` quotes `{WHOLE_LINE}` |\n"),
    ])
    p, d = run(root, base=hashes[0])
    verdict("correction_names_other_span", p, d, ["T1"], 1, {"corrections": 0})

    root, hashes = _fixture(work, "correction_quotes_seat_prose", [
        _pages("| S | `zz=9` |\n"),
        _pages("| S | `zz=9` |\n"
               "| C | [r76-correction] names `zz=9` quotes `seat=prose` |\n"),
    ])
    p, d = run(root, base=hashes[0])
    verdict("correction_quotes_seat_prose", p, d, ["T1", "T4"], 1, {"corrections": 0})

    # population exclusions and non-claim shapes
    root, _ = _fixture(work, "unrelated_round", [{
        "SCORECARD.md": "## Round 74 — old\n\n| Claim | Verdict |\n|---|---|\n| S | `zz=9` |\n\n"
                        "## Round 75 — selftest\n\n| Claim | Verdict |\n|---|---|\n",
        "corpus/QUALITY.md": "## Round-75 criterion — selftest\n\n- prose\n",
        "corpus/lessons/round-75.md": "# round 75\n\n## Mistakes\n\n| Class | Evidence |\n|---|---|\n",
        ".ufo/waves/round-75/controls/ctl.txt": RECEIPT_DEFAULT,
    }])
    p, d = run(root)
    verdict("unrelated_round", p, d, [], 0, {"met": True, "rows": 1})

    root, _ = _fixture(work, "green_path_token", [_pages("| S | `scripts/doc_quote_truth.py` |\n")])
    p, d = run(root)
    verdict("green_path_token_not_claim", p, d, [], 0, {"met": True, "spans_checked": 0})

    root, _ = _fixture(work, "green_command_line", [_pages("| S | `python3 -B scripts/x.py --root .` |\n")])
    p, d = run(root)
    verdict("green_command_line_not_claim", p, d, [], 0, {"met": True, "spans_checked": 0})

    root, _ = _fixture(work, "green_cli_flag", [_pages("| S | `--json` |\n")])
    p, d = run(root)
    verdict("green_cli_flag_not_claim", p, d, [], 0, {"met": True, "spans_checked": 0})

    root, _ = _fixture(work, "t1_pipe_span", [_pages("| S | `a=1 | b=2` |\n")])
    p, d = run(root)
    verdict("t1_pipe_span", p, d, ["T1"], 1)

    root, _ = _fixture(work, "t1_newline_escape", [_pages("| S | `a=1\\nb=2` |\n")])
    p, d = run(root)
    verdict("t1_newline_escape", p, d, ["T1"], 1)

    # ---- input faults / usage ----
    notgit = work / "notgit"
    if notgit.exists():
        shutil.rmtree(notgit)
    notgit.mkdir(parents=True)
    (notgit / "x.txt").write_text("nothing\n", encoding="utf-8")
    p, d = run(notgit)
    verdict("fault_not_git_repo", p, d, None, 2, stderr_has="input:")

    root, _ = _fixture(work, "fault_revs", [_pages("| S | `ax=1 by=2` |\n")])
    p, _ = run(root, revision="0000000")
    verdict("fault_missing_revision", p, None, None, 2, stderr_has="input:")
    p, _ = run(root, base="0000000")
    verdict("fault_missing_base_revision", p, None, None, 2, stderr_has="input:")

    p, _ = _run_tool(["--root", str(root), "--revision", "HEAD", "--rounds", "75", "--json"])
    verdict("usage_no_base", p, None, None, 64, stderr_has="required")
    p, _ = _run_tool(["--root", str(root), "--revision", "HEAD", "--base", "HEAD",
                      "--rounds", "x", "--json"])
    verdict("usage_bad_rounds", p, None, None, 64)
    p, _ = _run_tool(["--root", str(root), "--revision", "HEAD", "--base", "HEAD",
                      "--rounds", "75", "--bogus"])
    verdict("usage_unknown_flag", p, None, None, 64)
    p, _ = _run_tool(["--selftest"])
    verdict("usage_selftest_no_work", p, None, None, 64, stderr_has="requires --work")

    # missing round lesson is recorded, not an input fault (the base has none)
    root, _ = _fixture(work, "green_missing_lesson", [_pages("| S | `ax=1 by=2` |\n", lesson=False)])
    p, d = run(root)
    verdict("green_missing_lesson_tolerated", p, d, [], 0,
            {"met": True, "missing_files": ["corpus/lessons/round-75.md"]})

    # ---- JSON field contract ----
    root, _ = _fixture(work, "json_fields", [_pages("| S | `ax=1 by=2` |\n")])
    p, d = run(root)
    required = ["rows", "receipt_files", "spans_checked", "spans_exempted",
                "corrections", "append_only", "findings", "met"]
    if not isinstance(d, dict):
        print("  FAIL  json_fields: no JSON object")
        results.append((False, "json_fields"))
    else:
        missing = [k for k in required if k not in d]
        ok = not missing and d["spans_checked"] == 1 and d["met"] is True
        print(f"  {'PASS' if ok else 'FAIL'}  json_fields: missing={missing} "
              f"{[(k, d[k]) for k in required]}")
        results.append((ok, "json_fields"))

    passed = sum(1 for ok, _ in results if ok)
    print(f"selftest: {passed}/{len(results)} passed")
    return 0 if passed == len(results) else 1


def main(argv: list[str]) -> int:
    ap = _Parser(description="claim-row quote truth (kake r76 C1)")
    ap.add_argument("--root", default=".")
    ap.add_argument("--revision", default="master")
    ap.add_argument("--rounds", default="75,76")
    ap.add_argument("--base", default=None)
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--selftest", action="store_true")
    ap.add_argument("--work", default=None)
    a = ap.parse_args(argv)
    root = Path(a.root).resolve()
    if a.selftest:
        if not a.work:
            print("usage: --selftest requires --work <dir>", file=sys.stderr)
            return 64
        work = Path(a.work)
        work.mkdir(parents=True, exist_ok=True)
        return selftest(work)
    try:
        rounds = [int(x) for x in a.rounds.split(",") if x.strip()]
    except ValueError:
        print("usage: --rounds <N[,N]>", file=sys.stderr)
        return 64
    if not rounds:
        print("usage: --rounds <N[,N]>", file=sys.stderr)
        return 64
    rounds = sorted(set(rounds))  # amendment 7 F1: rounds[-1] is the newest round
    try:
        if not a.base:
            print("usage: --base <revision> is required (append-only conjunct)", file=sys.stderr)
            return 64
        res = evaluate(root, a.revision, rounds, a.base)
    except Fault as e:
        print(f"input: {e}", file=sys.stderr)
        return 2
    if a.json:
        json.dump(res, sys.stdout, indent=1)
        print()
    else:
        print(f"C1v2 revision={res['revision'][:8]} rows={res['rows']} "
              f"receipt_files={res['receipt_files']} spans={res['spans_checked']} "
              f"exempted={res['spans_exempted']} corrections={res['corrections']} "
              f"findings={len(res['findings'])} met={str(res['met']).lower()}")
        for f in res["findings"]:
            print(f"  {f['id']} {f['file']}:{f['line']} {f['detail']}")
        for m in res["missing_files"]:
            print(f"  missing {m}")
    return 0 if res["met"] else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
