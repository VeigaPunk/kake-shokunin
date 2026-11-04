#!/usr/bin/env python3
"""doc_quote_truth.py — claim-row quote truth (kake round 76, C1 calibration).

Predicate frozen in `.ufo/waves/round-76/contract.md` §C1 before any after-state:

  Claim rows.  Markdown table data rows inside a `## Round <N>` section of
  `SCORECARD.md` (headers and separator rows excluded); bullets inside a
  `## Round-<N> criterion` section of `corpus/QUALITY.md`; table data rows and
  bullets inside `## Mistakes` / `## Gate` / `## Claims` / `## Corrections` of
  `corpus/lessons/round-<N>.md`.  N in {75, 76}.

  Claim-bearing span.  A backticked span of a claim row carrying an observed-value
  shape: `token=value`, `exit <n>`, an `a/b` tally, or a 7-64 char lowercase hex
  token.  Command lines, CLI flags and path tokens are never claim-bearing.

  Receipt universe.  Committed files at the measured revision under `.ufo/waves/**`
  that are observed data: any file inside a `controls/`, `verification/`, `resid/`,
  `receipts/`, `frozen/`, `fixtures/` or `cases/` directory, plus
  `.txt/.json/.csv/.tsv/.log/.out/.ndjson` files outside them.  Dispatcher
  artifacts (`*-results.json`, `*-dispatch.json`, `*-spec.json`,
  `swarm-registry.json`, `*.ready*`) are never receipts.

  Findings.
    T1  span absent from every receipt.
    T2  elided span whose non-empty fragments are not all contiguous inside one
        receipt file.
    T4  correction line (`[rNN-correction` or `supersedes`) that carries no
        validated receipt quote.
    A1  claim row present at `--base` and gone at the measured revision
        (append-only conjunct).
  met = (findings == 0) and append_only.  Exit 0 met, 1 findings, 2 input fault,
  64 usage (`--base` required).

Revision citations.  v1 of this counter accepts a span that is entirely a
7-64 char lowercase hex token resolving to a commit at the measured revision as
a revision citation, not as a quote of observed output.  That behaviour is kept
here because the frozen base (findings=8) and the five frozen controls were
measured with it: two round-75 ledger citations resolve as commits but appear in
no receipt.  The contract §C1 sentence does not state the carve-out; dropping it
turns those two spans into T1 findings (findings=10).  The divergence is recorded
in `.ufo/waves/round-76/w1/ExecQuoteCounter.md`, not silently amended here.

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
ASSIGN_RE = re.compile(r"[A-Za-z_][A-Za-z0-9_.-]=\S")
PATHY_RE = re.compile(r"^(?:[.~/]|scripts/|corpus/|\.ufo/|node |python3 |git |sh )")
FILEEXT_RE = re.compile(r"\.(?:md|py|mjs|js|txt|json|html|xml|ya?ml|csv|log)$")
COMMAND_RE = re.compile(
    r"^(?:\$ |(?:bash|sh|zsh|dash|python|python3|uv|pip|node|npm|npx|git|jj|"
    r"curl|wget|grep|rg|sed|awk|find|cat|head|tail|ls|cp|mv|rm|mkdir|chmod|"
    r"make|cargo|go|rustc|time|/usr/bin/time|env|export|set|cd|source|diff|"
    r"cmp|sha256sum|shasum)\s)"
)

RECEIPT_DIRS = ("/controls/", "/verification/", "/resid/", "/receipts/",
                "/frozen/", "/fixtures/", "/cases/")
DATA_EXT = (".txt", ".json", ".csv", ".tsv", ".log", ".out", ".ndjson")
ARTIFACT_GLOBS = ("*-results.json", "*-dispatch.json", "*-spec.json",
                  "swarm-registry.json", "*.ready*")
REQUIRED_FILES = ("SCORECARD.md", "corpus/QUALITY.md")
CORRECTION_RE = re.compile(r"\[r\d+-correction|\bsupersedes\b", re.I)


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


def commit_exists(root: Path, rev: str, token: str) -> bool:
    if not HEX_RE.match(token):
        return False
    key = (str(root), rev, token)
    if key not in _COMMIT_CACHE:
        p = subprocess.run(["git", "-C", str(root), "cat-file", "-e", f"{token}^{{commit}}"],
                           capture_output=True)
        _COMMIT_CACHE[key] = p.returncode == 0
    return _COMMIT_CACHE[key]


def is_receipt(name: str) -> bool:
    """A receipt is observed data, never prose.  Dispatcher artifacts are never
    receipts even when they sit inside a receipt directory."""
    base = name.rsplit("/", 1)[-1]
    if any(fnmatch.fnmatchcase(base, g) for g in ARTIFACT_GLOBS):
        return False
    if any(d in name for d in RECEIPT_DIRS):
        return True
    return name.endswith(DATA_EXT)


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


def receipt_texts(root: Path, rev: str) -> list[tuple[str, str]]:
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
        if is_receipt(name):
            entries.append((name, oid.decode("ascii")))
    bodies = _read_blobs(root, [oid for _, oid in entries])
    return [(name, bodies[oid]) for name, oid in entries if oid in bodies]


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


def sections(text: str, head_re: re.Pattern) -> list[tuple[int, list[tuple[int, str]]]]:
    """Return [(line_no, [(line_no, line), ...])] per matching section body."""
    lines = text.splitlines()
    heads = [(i, m.group(1), m.group(2)) for i, line in enumerate(lines)
             for m in [re.match(r"^(#{1,6})\s+(.*)$", line)] if m]
    out = []
    for i, hashes, title in heads:
        if not head_re.search(title):
            continue
        level = len(hashes)
        body = []
        for j in range(i + 1, len(lines)):
            m = re.match(r"^(#{1,6})\s+", lines[j])
            if m and len(m.group(1)) <= level:
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
    """Data rows of every markdown table block: header + separator lines dropped."""
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
        if line.lstrip().startswith("|"):
            block.append((no, line))
        else:
            flush()
            block = []
    flush()
    return rows


def bullets(body: list[tuple[int, str]]) -> list[tuple[int, str]]:
    out: list[tuple[int, str]] = []
    cur: tuple[int, str] | None = None
    for no, line in body:
        if line.lstrip().startswith(("- ", "* ")):
            if cur:
                out.append(cur)
            cur = (no, line)
        elif (cur is not None and line.startswith(("  ", "\t")) and line.strip()
              and not line.lstrip().startswith("|")):
            cur = (cur[0], cur[1] + " " + line.strip())
        elif cur is not None:
            out.append(cur)
            cur = None
    if cur:
        out.append(cur)
    return out


def rows_for(root: Path, rev: str, rounds: list[int]) -> tuple[list[dict], list[str]]:
    rows: list[dict] = []
    missing: list[str] = []
    files = list(REQUIRED_FILES) + [f"corpus/lessons/round-{n}.md" for n in rounds]
    for path in files:
        text = show(root, rev, path)
        if text is None:
            if path in REQUIRED_FILES:
                raise Fault(f"required file missing at {rev}: {path}")
            missing.append(path)
            continue
        if path == "SCORECARD.md":
            pat = re.compile(r"\bround[ -]?(?:%s)\b" % "|".join(str(n) for n in rounds), re.I)
            for _, body in sections(text, pat):
                for no, line in table_rows(body):
                    rows.append({"file": path, "line": no + 1, "text": line})
        elif path == "corpus/QUALITY.md":
            pat = re.compile(r"\bround[- ]?(?:%s)\b" % "|".join(str(n) for n in rounds), re.I)
            for _, body in sections(text, pat):
                for no, line in bullets(body):
                    rows.append({"file": path, "line": no + 1, "text": line})
        else:
            pat = re.compile(r"^mistakes$|^gate$|^claims$|^corrections$", re.I)
            for _, body in sections(text, pat):
                for no, line in table_rows(body):
                    rows.append({"file": path, "line": no + 1, "text": line})
                for no, line in bullets(body):
                    rows.append({"file": path, "line": no + 1, "text": line})
    return rows, missing


def span_ok(span: str, receipts: list[tuple[str, str]], root: Path, rev: str) -> bool:
    if HEX_RE.match(span) and commit_exists(root, rev, span):
        return True
    frags = [f for f in ELIDE_RE.split(span) if f.strip()] if ELIDE_RE.search(span) else [span]
    return any(all(f in body for f in frags) for _, body in receipts)


def correction_lines(rows: list[dict]) -> list[dict]:
    return [r for r in rows if CORRECTION_RE.search(r["text"])]


def row_ids(rows: list[dict]) -> set[tuple[str, str]]:
    return {(r["file"], re.sub(r"\s+", " ", r["text"]).strip()) for r in rows}


def evaluate(root: Path, rev: str, rounds: list[int], base: str | None = None) -> dict:
    require_worktree(root)
    rev_commit = resolve_commit(root, rev)
    if not base:
        raise Fault("--base is required (append-only conjunct)")
    base_commit = resolve_commit(root, base)
    receipts = receipt_texts(root, rev_commit)
    rows, missing = rows_for(root, rev_commit, rounds)
    append_only = True
    base_rows, _ = rows_for(root, base_commit, rounds)
    gone = sorted(row_ids(base_rows) - row_ids(rows))
    append_only = not gone
    for f, text in gone:
        rows.append({"file": f, "line": 0, "text": text, "spans": [], "deleted": True})
    for r in rows:
        r["spans"] = spans_of(r["text"])
    validated: list[tuple[dict, list[str]]] = []
    findings: list[dict] = []
    for c in correction_lines(rows):
        good = [sp for sp in c["spans"] if span_ok(sp, receipts, root, rev_commit)]
        if good:
            validated.append((c, good))
        else:
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
            continue
        for span in r["spans"]:
            checked += 1
            if span_ok(span, receipts, root, rev_commit):
                continue
            if any(span in c["text"] for c, _ in validated):
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
)


def _pages(score_rows: str = "", quality: str = "- prose\n", lesson_extra: str = "",
           lesson: bool = True, extra: dict[str, str] | None = None) -> dict[str, str]:
    files = {
        "SCORECARD.md": "## Round 75 — selftest\n\n| Claim | Verdict |\n|---|---|\n" + score_rows,
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
    p = subprocess.run(["git", *args], capture_output=True, text=True, cwd=str(cwd) if cwd else None)
    if p.returncode != 0:
        raise RuntimeError(f"git {' '.join(args)} failed: {p.stderr.strip()}")
    return p


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
        for rel, text in payload.items():
            path = root / rel
            path.parent.mkdir(parents=True, exist_ok=True)
            path.write_text(text, encoding="utf-8")
        _git_ok(["-C", str(root), "add", "-A"])
        _git_ok(["-C", str(root), "-c", "user.name=t", "-c", "user.email=t@t",
                 "-c", "commit.gpgsign=false", "commit", "-q", "--no-verify", "-m", f"fixture {idx}"])
        hashes.append(_git_ok(["-C", str(root), "rev-parse", "HEAD"]).stdout.strip())
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
                fields: dict | None = None, stderr_has: str | None = None) -> None:
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
        if stderr_has is not None and stderr_has not in p.stderr:
            ok = False
            detail += f" stderr!~{stderr_has!r}"
        if p.returncode not in (0, 1) and p.stderr:
            detail += f" stderr={p.stderr.strip().splitlines()[-1][:120]!r}"
        print(f"  {'PASS' if ok else 'FAIL'}  {name}: want ids={want_ids} rc={want_rc}; got {detail}")
        results.append((ok, name))

    def run(root: Path, extra: list[str], base: str = "HEAD", revision: str = "HEAD") -> tuple:
        return _run_tool(["--root", str(root), "--revision", revision, "--base", base,
                          "--rounds", "75", "--json", *extra])

    # 1. plain span contiguous in a receipt
    root, _ = _fixture(work, "green_plain", [_pages("| S | `ax=1 by=2` |\n")])
    p, d = run(root, [])
    verdict("green_plain", p, d, [], 0, {"met": True, "append_only": True,
                                         "rows": 1, "receipt_files": 1, "spans_checked": 1})

    # 2. elision, both fragments inside one receipt file
    root, _ = _fixture(work, "green_elision_same_receipt", [_pages("| S | `ax=1 … by=2` |\n")])
    p, d = run(root, [])
    verdict("green_elision_same_receipt", p, d, [], 0, {"met": True})

    # 3. elision with an empty trailing fragment
    root, _ = _fixture(work, "green_elision_open_end", [_pages("| S | `by=2 …` |\n")])
    p, d = run(root, [])
    verdict("green_elision_open_end", p, d, [], 0, {"met": True})

    # 4. 64-hex digest quoted by a receipt
    root, _ = _fixture(work, "green_hex_digest_in_receipt", [_pages("| S | `" + "e" * 64 + "` |\n")])
    p, d = run(root, [])
    verdict("green_hex_digest_in_receipt", p, d, [], 0, {"met": True})

    # 5. a row whose span is a plain commit hash (revision citation carve-out)
    root, hashes = _fixture(work, "green_commit_citation", [
        _pages(""),
        _pages(f"| S | `{hashes_short} ` |\n") if False else _pages(""),
    ])
    root, hashes = _fixture(work, "green_commit_citation", [
        _pages(""),
        {"SCORECARD.md": "## Round 75 — selftest\n\n| Claim | Verdict |\n|---|---|\n"
                         f"| S | `{hashes[0][:8]}` |\n",
         "corpus/QUALITY.md": "## Round-75 criterion — selftest\n\n- prose\n",
         "corpus/lessons/round-75.md": "# round 75\n\n## Mistakes\n\n| Class | Evidence |\n|---|---|\n",
         ".ufo/waves/round-75/controls/ctl.txt": RECEIPT_DEFAULT},
    ])
    p, d = run(root, [], base=hashes[0])
    verdict("green_commit_citation", p, d, [], 0, {"met": True, "receipt_files": 1})

    # 6. correction row quotes a validated line and names the defective span
    root, _ = _fixture(work, "green_correction_names_span", [_pages(
        "| S | `ax=1 cz=3` |\n"
        "| T | [r76-correction] quote `ax=1 by=2` names `ax=1 cz=3` |\n")])
    p, d = run(root, [])
    verdict("green_correction_names_span", p, d, [], 0,
            {"met": True, "corrections": 1, "spans_exempted": 1})

    # 7. QUALITY bullet under a Round-<N> criterion section
    root, _ = _fixture(work, "green_quality_bullet", [_pages(
        quality="- **Criterion** `files=15 append_only=false met=false`\n")])
    p, d = run(root, [])
    verdict("green_quality_bullet", p, d, [], 0, {"met": True, "rows": 1})

    # 8. lessons Gate bullet
    root, _ = _fixture(work, "green_lessons_gate_bullet", [_pages(
        lesson_extra="\n## Gate\n\n- `mismatches=2 classes=E1 E3`\n")])
    p, d = run(root, [])
    verdict("green_lessons_gate_bullet", p, d, [], 0, {"met": True})

    # 9. rows outside the measured round are not claim rows
    root, _ = _fixture(work, "green_population_outside_round", [{
        "SCORECARD.md": "## Round 74 — old\n\n| Claim | Verdict |\n|---|---|\n| S | `zz=9` |\n\n"
                        "## Round 75 — selftest\n\n| Claim | Verdict |\n|---|---|\n",
        "corpus/QUALITY.md": "## Round-75 criterion — selftest\n\n- prose\n",
        "corpus/lessons/round-75.md": "# round 75\n\n## Mistakes\n\n| Class | Evidence |\n|---|---|\n",
        ".ufo/waves/round-75/controls/ctl.txt": RECEIPT_DEFAULT,
    }])
    p, d = run(root, [])
    verdict("green_population_outside_round", p, d, [], 0, {"met": True, "rows": 0})

    # 10-12. command line / flag / path tokens are never claim-bearing
    root, _ = _fixture(work, "green_path_token", [_pages("| S | `scripts/doc_quote_truth.py` |\n")])
    p, d = run(root, [])
    verdict("green_path_token_not_claim", p, d, [], 0, {"met": True})
    root, _ = _fixture(work, "green_command_line", [_pages("| S | `python3 -B scripts/x.py --root .` |\n")])
    p, d = run(root, [])
    verdict("green_command_line_not_claim", p, d, [], 0, {"met": True})
    root, _ = _fixture(work, "green_cli_flag", [_pages("| S | `--json` |\n")])
    p, d = run(root, [])
    verdict("green_cli_flag_not_claim", p, d, [], 0, {"met": True})

    # 13. a missing round lesson is recorded, not an input fault (base has no round-76 lesson)
    root, _ = _fixture(work, "green_missing_lesson", [_pages("| S | `ax=1 by=2` |\n", lesson=False)])
    p, d = run(root, [])
    verdict("green_missing_lesson_tolerated", p, d, [], 0,
            {"met": True, "missing_files": ["corpus/lessons/round-75.md"]})

    # 14. span absent from every receipt
    root, _ = _fixture(work, "t1_absent", [_pages("| S | `zz=9` |\n")])
    p, d = run(root, [])
    verdict("t1_absent", p, d, ["T1"], 1, {"met": False})

    # 15. span non-contiguous inside one receipt line
    root, _ = _fixture(work, "t1_noncontiguous", [_pages("| S | `ax=1 cz=3` |\n")])
    p, d = run(root, [])
    verdict("t1_noncontiguous", p, d, ["T1"], 1)

    # 16. a/b tally absent from receipts
    root, _ = _fixture(work, "t1_ratio", [_pages("| S | `9/9 passed` |\n")])
    p, d = run(root, [])
    verdict("t1_ratio", p, d, ["T1"], 1)

    # 17. hex token that is neither in a receipt nor a commit
    root, _ = _fixture(work, "t1_hex_absent", [_pages("| S | `deadbeef` |\n")])
    p, d = run(root, [])
    verdict("t1_hex_absent_noncommit", p, d, ["T1"], 1)

    # 18. a seat's *-results.json is prose, never a receipt
    root, _ = _fixture(work, "t1_seat_prose", [_pages(
        "| S | `zz=9` |\n",
        extra={".ufo/waves/round-75/w1-results.json": '{"note":"zz=9"}\n'})])
    p, d = run(root, [])
    verdict("t1_seat_prose_results_json", p, d, ["T1"], 1, {"receipt_files": 1})

    # 19. *.ready* is a dispatcher artifact even inside controls/
    root, _ = _fixture(work, "t1_ready_artifact", [_pages(
        "| S | `zz=9` |\n",
        extra={".ufo/waves/round-75/controls/w1.ready.txt": "zz=9\n"})])
    p, d = run(root, [])
    verdict("t1_artifact_ready_in_controls", p, d, ["T1"], 1, {"receipt_files": 1})

    # 20. elided span whose fragments are not all present
    root, _ = _fixture(work, "t2_elision_bad", [_pages("| S | `ax=1 … nope=3` |\n")])
    p, d = run(root, [])
    verdict("t2_elision_bad", p, d, ["T2"], 1)

    # 21. elided fragments split across two receipt files
    root, _ = _fixture(work, "t2_elision_split", [_pages(
        "| S | `ax=1 … by=2` |\n",
        extra={".ufo/waves/round-75/controls/ctl.txt": "ax=1\n",
               ".ufo/waves/round-75/controls/ctl2.txt": "by=2\n"})])
    p, d = run(root, [])
    verdict("t2_elision_split_files", p, d, ["T2"], 1)

    # 22. junk correction: supersedes with no validated quote
    root, _ = _fixture(work, "t4_junk", [_pages(
        "| S | `ax=1 cz=3` |\n| T | [r76-correction] supersedes `zz=9` |\n")])
    p, d = run(root, [])
    verdict("t4_junk_correction", p, d, ["T1", "T4"], 1, {"corrections": 0})

    # 23. correction line with no span at all
    root, _ = _fixture(work, "t4_no_span", [_pages(
        "| S | `ax=1 cz=3` |\n| T | [r76-correction] supersedes the row |\n")])
    p, d = run(root, [])
    verdict("t4_correction_no_span", p, d, ["T1", "T4"], 1)

    # 24. laundering: validated quote that names no defective span
    root, _ = _fixture(work, "launder", [_pages(
        "| S | `ax=1 cz=3` |\n| T | [r76-correction] quote `ax=1 by=2` only |\n")])
    p, d = run(root, [])
    verdict("t1_launder_correction_valid_no_name", p, d, ["T1"], 1,
            {"corrections": 1, "spans_exempted": 0})

    # 25. append-only conjunct: a base claim row is gone at the measured revision
    root, hashes = _fixture(work, "a1_deleted", [
        _pages("| S | `ax=1 by=2` |\n"),
        _pages("| U | `ax=1 by=2` |\n"),
    ])
    p, d = run(root, [], base=hashes[0])
    verdict("a1_deleted_row", p, d, ["A1"], 1, {"append_only": False, "met": False})

    # 26. nested subsection rows are still claim rows
    root, _ = _fixture(work, "nested_subsection", [{
        "SCORECARD.md": "## Round 75 — selftest\n\n| Claim | Verdict |\n|---|---|\n| A | `ax=1 by=2` |\n\n"
                        "### Capabilities acquired in round 75\n\n| Capability | Evidence |\n|---|---|\n"
                        "| X | `zz=9` |\n",
        "corpus/QUALITY.md": "## Round-75 criterion — selftest\n\n- prose\n",
        "corpus/lessons/round-75.md": "# round 75\n\n## Mistakes\n\n| Class | Evidence |\n|---|---|\n",
        ".ufo/waves/round-75/controls/ctl.txt": RECEIPT_DEFAULT,
    }])
    p, d = run(root, [])
    verdict("nested_subsection_rows_checked", p, d, ["T1"], 1)

    # 27. indented markdown table row is a data row
    root, _ = _fixture(work, "indented_row", [_pages(
        "| S | `ax=1 by=2` |\n  | I | `zz=9` |\n")])
    p, d = run(root, [])
    verdict("indented_table_row", p, d, ["T1"], 1, {"rows": 2})

    # 28. append-only green: rows may be appended between base and measured
    root, hashes = _fixture(work, "append_only_green", [
        _pages("| S | `ax=1 by=2` |\n"),
        _pages("| S | `ax=1 by=2` |\n| T | `ax=1 by=2 cz=3` |\n"),
    ])
    p, d = run(root, [], base=hashes[0])
    verdict("append_only_green", p, d, [], 0, {"append_only": True, "met": True, "rows": 2})

    # 29. input fault: root is not a work-tree root
    notgit = work / "notgit"
    if notgit.exists():
        shutil.rmtree(notgit)
    notgit.mkdir(parents=True)
    (notgit / "x.txt").write_text("nothing\n", encoding="utf-8")
    p, d = run(notgit, [])
    verdict("fault_not_git_repo", p, d, None, 2, stderr_has="input:")

    # 30-31. input fault: unresolved revisions
    root, _ = _fixture(work, "fault_revs", [_pages("| S | `ax=1 by=2` |\n")])
    p, _ = run(root, [], revision="0000000")
    verdict("fault_missing_revision", p, None, None, 2, stderr_has="input:")
    p, _ = run(root, [], base="0000000")
    verdict("fault_missing_base_revision", p, None, None, 2, stderr_has="input:")

    # 32-35. usage -> 64
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

    # 36. JSON field names and values
    root, _ = _fixture(work, "json_fields", [_pages("| S | `ax=1 by=2` |\n")])
    p, d = run(root, [])
    required = ["rows", "receipt_files", "spans_checked", "spans_exempted",
                "corrections", "append_only", "findings", "met"]
    missing = [k for k in required if not isinstance(d, dict) or k not in d]
    if missing or not isinstance(d, dict):
        print(f"  FAIL  json_fields: missing keys {missing}")
        results.append((False, "json_fields"))
    else:
        ok = (d["rows"] == 1 and d["receipt_files"] == 1 and d["spans_checked"] == 1
              and d["spans_exempted"] == 0 and d["corrections"] == 0
              and d["append_only"] is True and d["findings"] == [] and d["met"] is True)
        print(f"  {'PASS' if ok else 'FAIL'}  json_fields: {[ (k, d[k]) for k in required ]}")
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
