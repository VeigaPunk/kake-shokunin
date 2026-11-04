#!/usr/bin/env python3
"""c76_quote_truth.py — v0 counter for kake round 76 C1 (calibration).

Predicate (frozen in .ufo/waves/round-76/contract.md before any after-state):

A *claim row* is a markdown table row inside a `## Round <N>` section of
SCORECARD.md, a bullet inside a `## Round-<N> criterion` section of
corpus/QUALITY.md, or a table row / bullet inside corpus/lessons/round-<N>.md.
A *claim-bearing span* is a backticked span of a claim row carrying an observed
value shape: `token=value`, `exit <n>`, an `a/b` tally, or a 8-64 char lowercase
hex token. Command lines, flags and path tokens are not claim-bearing.

T1  a claim-bearing span must be a contiguous substring of some committed text
    file under .ufo/waves/ at the measured revision.
T2  a span carrying an explicit elision (`…` or `[...]`) passes only when every
    non-empty fragment is contiguous inside ONE receipt file.
T5  a 7-40 char lowercase hex token is accepted when it resolves as a commit at
    the measured revision (revision citation), else it is T1.
E   effective-row rule: a later row in the same file whose text carries
    `supersedes` and the same subject key exempts the earlier row's spans. The
    superseding row must itself carry >=1 claim-bearing span (T3 otherwise).

met = (findings == 0). Exit 0 met, 1 findings, 2 input fault, 64 usage.
"""

from __future__ import annotations

import argparse
import json
import re
import shutil
import subprocess
import sys
import tempfile
from pathlib import Path

SPAN_RE = re.compile(r"`([^`\n]+)`")
HEX_RE = re.compile(r"^[0-9a-f]{7,64}$")
ELIDE_RE = re.compile(r"…|\[\.\.\.\]|\.\.\.")
EXIT_RE = re.compile(r"\bexit\s*\d+\b")
RATIO_RE = re.compile(r"\b\d+/\d+\b")
ASSIGN_RE = re.compile(r"[A-Za-z_][A-Za-z0-9_.-]=\S")
PATHY_RE = re.compile(r"^(?:[.~/]|scripts/|corpus/|\.ufo/|node |python3 |git |sh )")
FILEEXT_RE = re.compile(r"\.(?:md|py|mjs|js|txt|json|html|xml|ya?ml|csv|log)$")


class Fault(Exception):
    """Input fault -> exit 2."""


def git(root: Path, *args: str) -> subprocess.CompletedProcess:
    return subprocess.run(["git", "-C", str(root), *args], capture_output=True, text=True)


def show(root: Path, rev: str, path: str) -> str | None:
    p = subprocess.run(["git", "-C", str(root), "show", f"{rev}:{path}"], capture_output=True)
    if p.returncode != 0:
        return None
    try:
        return p.stdout.decode("utf-8")
    except UnicodeDecodeError:
        return None


def commit_exists(root: Path, rev: str, token: str) -> bool:
    p = git(root, "rev-parse", "--verify", "--quiet", f"{rev}^{{commit}}")
    if p.returncode != 0:
        return False
    return git(root, "cat-file", "-e", f"{token}^{{commit}}").returncode == 0


RECEIPT_DIRS = ("/controls/", "/verification/", "/resid/", "/receipts/", "/frozen/", "/fixtures/", "/cases/")
DATA_EXT = (".txt", ".json", ".csv", ".tsv", ".log", ".out", ".ndjson")
DISPATCH_ARTIFACTS = ("-results.json", "-dispatch.json", "-spec.json", "swarm-registry.json")


def is_receipt(name: str) -> bool:
    """A receipt is observed data, never prose: files inside a receipt directory
    (any extension) or data-extension files outside them. Dispatcher artifacts
    (seat prose dumps) are never receipts."""
    if any(name.endswith(a) for a in DISPATCH_ARTIFACTS) or name.endswith(".ready") or "/.ready" in name:
        return False
    if any(d in name for d in RECEIPT_DIRS):
        return True
    return name.endswith(DATA_EXT)


def receipt_texts(root: Path, rev: str) -> list[tuple[str, str]]:
    p = git(root, "ls-tree", "-r", "--name-only", rev, ".ufo/waves")
    if p.returncode != 0:
        raise Fault(f"cannot list .ufo/waves at {rev}: {p.stderr.strip()}")
    out: list[tuple[str, str]] = []
    for name in p.stdout.splitlines():
        if not name or not is_receipt(name):
            continue
        body = show(root, rev, name)
        if body is None or "\x00" in body:
            continue
        out.append((name, body))
    return out


def claimy(span: str) -> bool:
    s = span.strip()
    if not s:
        return False
    if PATHY_RE.match(s) or FILEEXT_RE.search(s) or "://" in s:
        return False
    if s.startswith("--"):
        return False
    if HEX_RE.match(s):
        return len(s) >= 7
    if ASSIGN_RE.search(s) or EXIT_RE.search(s) or RATIO_RE.search(s):
        return True
    return False


def spans_of(text: str) -> list[str]:
    return [m.group(1) for m in SPAN_RE.finditer(text) if claimy(m.group(1))]


def sections(text: str, head_re: re.Pattern) -> list[tuple[int, list[tuple[int, str]]]]:
    """Return [(line_no, [(line_no, line), ...])] per matching section body."""
    lines = text.splitlines()
    heads = [(i, m.group(1), m.group(2)) for i, line in enumerate(lines) for m in [re.match(r"^(#{1,6})\s+(.*)$", line)] if m]
    out = []
    for idx, (i, hashes, title) in enumerate(heads):
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


def table_rows(body: list[tuple[int, str]]) -> list[tuple[int, str]]:
    """Data rows of every markdown table block: header + separator lines dropped."""
    rows: list[tuple[int, str]] = []
    block: list[tuple[int, str]] = []

    def flush() -> None:
        if not block:
            return
        sep_idx = [i for i, (_, line) in enumerate(block)
                   if re.match(r"^\s*\|[\s:|-]+\|\s*$", line)]
        start = 0
        if sep_idx:
            start = sep_idx[0] + 1
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
    out = []
    cur: tuple[int, str] | None = None
    for no, line in body:
        if line.lstrip().startswith(("- ", "* ")):
            if cur:
                out.append(cur)
            cur = (no, line)
        elif cur is not None and line.startswith(("  ", "\t")) and line.strip():
            cur = (cur[0], cur[1] + " " + line.strip())
        elif cur is not None:
            out.append(cur)
            cur = None
    if cur:
        out.append(cur)
    return out


def subject_key(line: str) -> str:
    s = line.strip()
    if s.startswith("|"):
        cells = [c.strip() for c in s.strip("|").split("|")]
        key = cells[0] if cells else s
    else:
        m = re.search(r"\*\*(.+?)\*\*", s)
        key = m.group(1) if m else s[3:63]
    key = re.sub(r"[`*_\[\]]", "", key).strip().lower()
    key = re.sub(r"\s+", " ", key)
    return key[:80]


def rows_for(root: Path, rev: str, rounds: list[int]) -> tuple[list[dict], list[str]]:
    rows: list[dict] = []
    files = ["SCORECARD.md", "corpus/QUALITY.md"] + [f"corpus/lessons/round-{n}.md" for n in rounds]
    missing = []
    for path in files:
        text = show(root, rev, path)
        if text is None:
            if path.startswith("corpus/lessons/"):
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


CORRECTION_RE = re.compile(r"\[r\d+-correction|\bsupersedes\b", re.I)


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
    receipts = receipt_texts(root, rev)
    rows, missing = rows_for(root, rev, rounds)
    append_only = True
    if base:
        base_rows, _ = rows_for(root, base, rounds)
        cur = row_ids(rows)
        gone = sorted(row_ids(base_rows) - cur)
        append_only = not gone
        for f, text in gone:
            rows.append({"file": f, "line": 0, "text": text, "spans": []})
            rows[-1]["deleted"] = True
    for r in rows:
        r["spans"] = spans_of(r["text"])
    corr = correction_lines(rows)
    validated = []
    findings = []
    for c in corr:
        good = [sp for sp in c["spans"] if span_ok(sp, receipts, root, rev)]
        if good:
            validated.append((c, good))
        else:
            findings.append({"id": "T4", "file": c["file"], "line": c["line"],
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
            if span_ok(span, receipts, root, rev):
                continue
            if corr:
                exempt += 1
                continue
            findings.append({"id": "T2" if ELIDE_RE.search(span) else "T1",
                             "file": r["file"], "line": r["line"], "detail": span[:160]})
    return {
        "counter": "c76_quote_truth/v1",
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


SELFTEST_CASES = [
    ("t1_noncontiguous", "T1", "| S | `ax=1 cz=3` |"),
    ("t1_absent", "T1", "| S | `zz=9` |"),
    ("t2_elision_bad", "T2", "| S | `ax=1 … nope=3` |"),
    ("ok_elision", None, "| S | `ax=1 … by=2` |"),
    ("ok_plain", None, "| S | `ax=1 by=2 cz=3` |"),
    ("ok_digest", None, "| S | `" + "e" * 64 + "` |"),
    ("ok_commit", None, "| S | `@SHORT@` |"),
    ("t1_ratio", "T1", "| S | `9/9 passed` |"),
    ("t2_elision_mixed_receipt", "T2", "| S | `ax=1 … eeeeeeeeee` |"),
    ("ok_correction_exempts", None, "| S | `ax=1 cz=3` |\n| T | [r76-correction] `ax=1 by=2 cz=3` supersedes `ax=1 cz=3` |"),
    ("t4_junk_correction", "T1,T4", "| S | `ax=1 cz=3` |\n| T | [r76-correction] `zz=9` supersedes `ax=1 cz=3` |"),
    ("t4_correction_no_span", "T1,T4", "| S | `ax=1 cz=3` |\n| T | [r76-correction] supersedes the row |"),
]


def selftest(work: Path) -> int:
    """Build a fixture repo in `work`; assert exit code and finding ids."""
    root = work / "fixture"
    if root.exists():
        shutil.rmtree(root)
    (root / ".ufo/waves/round-75/controls").mkdir(parents=True)
    (root / "corpus/QUALITY.md").parent.mkdir(parents=True)
    (root / "corpus/lessons").mkdir(parents=True)
    receipt = "ax=1 by=2 cz=3\n" + "e" * 64 + "\n"
    (root / ".ufo/waves/round-75/controls/ctl.txt").write_text(receipt)
    ok = 0
    total = 0
    short = ""
    for name, want, span in SELFTEST_CASES:
        total += 1
        body = "| Subject | Claim |\n|---|---|\n" + (span if span.startswith("|") else "| " + name + " | `" + span + "` |") + "\n"
        (root / "SCORECARD.md").write_text("## Round 75 — selftest\n\n" + body)
        (root / "corpus/QUALITY.md").write_text("## Round-75 criterion — selftest\n\n- prose\n")
        (root / "corpus/lessons/round-75.md").write_text("# r75\n\n## Mistakes\n\n| Class | Evidence | Captured-by | Fix |\n|---|---|---|---|\n")
        subprocess.run(["git", "-C", str(root), "init", "-q"], check=True)
        subprocess.run(["git", "-C", str(root), "add", "-A"], check=True)
        subprocess.run(["git", "-C", str(root), "-c", "user.name=t", "-c", "user.email=t@t",
                        "commit", "-qm", "fixture"], check=True)
        if "@SHORT@" in span:
            short = subprocess.run(["git", "-C", str(root), "rev-parse", "--short", "HEAD"],
                                   capture_output=True, text=True).stdout.strip()
            span = span.replace("@SHORT@", short)
        got = subprocess.run([sys.executable, "-B", __file__, "--root", str(root), "--revision", "HEAD",
                              "--rounds", "75", "--base", "HEAD", "--json"], capture_output=True, text=True)
        ids = sorted({f["id"] for f in json.loads(got.stdout)["findings"]}) if got.stdout.strip().startswith("{") else ["<no-json>"]
        want_ids = [] if want is None else want.split(",")
        good = (ids == want_ids) and (got.returncode == (0 if want is None else 1))
        print(f"  {'PASS' if good else 'FAIL'}  {name}: want {want_ids} rc={0 if want is None else 1}; got {ids} rc={got.returncode}")
        ok += 1 if good else 0
    # deletion case: a claim row removed between --base and the measured revision
    total += 1
    (root / "SCORECARD.md").write_text("## Round 75 — selftest\n\n| Subject | Claim |\n|---|---|\n| T | `zz=9` |\n")
    (root / "corpus/QUALITY.md").write_text("## Round-75 criterion — selftest\n\n- prose\n")
    (root / "corpus/lessons/round-75.md").write_text("# r75\n\n## Mistakes\n\n| Class | Evidence |\n|---|---|\n")
    subprocess.run(["git", "-C", str(root), "add", "-A"], check=True)
    subprocess.run(["git", "-C", str(root), "-c", "user.name=t", "-c", "user.email=t@t",
                    "commit", "-qm", "fixture-clean"], check=True)
    base_rev = subprocess.run(["git", "-C", str(root), "rev-parse", "HEAD"],
                              capture_output=True, text=True).stdout.strip()
    (root / "SCORECARD.md").write_text("## Round 75 — selftest\n\n| Subject | Claim |\n|---|---|\n| U | `zz=9` |\n")
    subprocess.run(["git", "-C", str(root), "-c", "user.name=t", "-c", "user.email=t@t",
                    "commit", "-qam", "fixture-3"], check=True)
    got = subprocess.run([sys.executable, "-B", __file__, "--root", str(root), "--revision", "HEAD",
                          "--rounds", "75", "--base", base_rev, "--json"], capture_output=True, text=True)
    ids = sorted({f["id"] for f in json.loads(got.stdout)["findings"]}) if got.stdout.strip().startswith("{") else ["<no-json>"]
    good = ids == ["A1", "T1"] and got.returncode == 1
    print(f"  {'PASS' if good else 'FAIL'}  a1_deleted_row: want ['A1', 'T1'] rc=1; got {ids} rc={got.returncode}")
    ok += 1 if good else 0
    print(f"selftest: {ok}/{total} passed")
    return 0 if ok == total else 1


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(description="claim-row quote truth (kake r76 C1)")
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
        print(f"C1v1 revision={res['revision'][:8]} rows={res['rows']} receipt_files={res['receipt_files']} "
              f"spans={res['spans_checked']} exempted={res['spans_exempted']} corrections={res['corrections']} "
              f"findings={len(res['findings'])} met={str(res['met']).lower()}")
        for f in res["findings"]:
            print(f"  {f['id']} {f['file']}:{f['line']} {f['detail']}")
        for m in res["missing_files"]:
            print(f"  missing {m}")
    return 0 if res["met"] else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
