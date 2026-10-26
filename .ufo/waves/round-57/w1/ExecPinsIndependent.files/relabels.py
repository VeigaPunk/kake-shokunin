#!/usr/bin/env python3
"""ExecPinsIndependent (round-57 W1, claim C1): independent re-derivation of the
committed revision-pin relabel set.

Method is deliberately independent of `.ufo/waves/round-57/c57_receipt_pins.py`
(never imported, never executed here): stream `git log -p --first-parent` with
`--unified=0` over the lane, restricted to `.ufo/waves/round-40..49` and
`.ufo/waves/round-50..57`, and pair removed/added revision-pin lines that land in
the same commit and the same file.  The counter's population is only
`.ufo/waves/round-5[2-7]/{control,controls}/` with `^[ ]*revision[:=]`; this scan is
wider in round range (40-57), in directory (every subdirectory), and in key form
(`rev:`, `measured:`, JSON `"revision":`, `sourceRevision`, ...).

Read-only: only `git log`/`git ls-tree`/`git grep`/`git rev-parse` are invoked.

Usage:
  python3 -B relabels.py                 # full report on stdout
  python3 -B relabels.py --json out.json # also dump the derived rows
"""
from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys

ROOT = "/home/vgpnk/Projects/shokunin/kake-shokunin"
ROUND_DIRS = [f".ufo/waves/round-{n}" for n in list(range(40, 50)) + list(range(50, 58))]
BASE_CONTROL = ".ufo/waves/round-57/controls/base-c1-receipt-pins.txt"

# wide key set: anything that names a revision pin at line start
KEY_ALT = r"revision|rev|sourceRevision|source_revision|measuredRevision|measured|pinned_revision"
KEY = "(?:" + KEY_ALT + ")"
WIDE = re.compile(r'^[ \t]*"?' + KEY + r'"?[ \t]*[:=]')
# the counter's own stated regex, for the "would the counter have seen it" column
COUNTER = re.compile(r"^[ ]*revision[:=]")
HEX = re.compile(r"\b([0-9a-f]{7,40})\b")
KEYNAME = re.compile(r'^[ \t]*"?(' + KEY + r')"?[ \t]*[:=]')

RECEIPT_EXT = {".txt", ".json", ".jsonl", ".ndjson", ".md", ".tsv", ".log",
               ".yaml", ".yml", ".csv", ".out", ".err", ""}
CODE_EXT = {".py", ".sh", ".mjs", ".js", ".c", ".h", ".rs"}


def git(*args: str) -> subprocess.CompletedProcess:
    return subprocess.run(["git", "-C", ROOT, *args], capture_output=True,
                          text=True, errors="replace")


def key_of(line: str) -> str:
    m = KEYNAME.match(line)
    return m.group(1) if m else "?"


def value_of(line: str) -> str:
    """First hex token of a pin line, else the trimmed value text."""
    m = HEX.search(line)
    if m:
        return m.group(1)
    m = re.match(r"^[ \t]*\"?" + KEY + r"\"?[ \t]*[:=][ \t]*(.*)$", line)
    return (m.group(1).strip() if m else "").strip()


def ext_of(path: str) -> str:
    tail = path.rsplit("/", 1)[-1]
    return ("." + tail.rsplit(".", 1)[1]) if "." in tail else ""


def scan_history():
    """Stream `git log -p --first-parent` and bucket pin-line deltas per commit+path."""
    cmd = ["git", "-C", ROOT, "log", "--first-parent", "-p", "--unified=0",
           "--no-color", "--format=@@@ %H", "--", *ROUND_DIRS]
    proc = subprocess.Popen(cmd, stdout=subprocess.PIPE, text=True,
                            errors="replace", bufsize=1 << 16)
    commit = None
    path = None
    buckets: dict[tuple[str, str], dict[str, list]] = {}
    order: list[tuple[str, str]] = []
    commits_seen: list[str] = []
    diff_blocks = 0
    for raw in proc.stdout:
        line = raw.rstrip("\n")
        if line.startswith("@@@ "):
            commit = line[4:].strip()
            commits_seen.append(commit)
            continue
        if line.startswith("diff --git "):
            m = re.match(r"diff --git a/(.*?) b/(.*)$", line)
            path = m.group(2) if m else None
            diff_blocks += 1
            continue
        if commit is None or path is None:
            continue
        if line.startswith(("--- ", "+++ ", "@@", "index ", "new file", "deleted file",
                            "old mode", "new mode", "similarity", "rename ")):
            continue
        if not line or line[0] not in "+-":
            continue
        text = line[1:]
        if not WIDE.match(text):
            continue
        key = (commit, path)
        if key not in buckets:
            buckets[key] = {"removed": [], "added": []}
            order.append(key)
        buckets[key]["removed" if line[0] == "-" else "added"].append(text)
    proc.wait()
    return buckets, order, commits_seen, diff_blocks


def derive(buckets, order):
    relabels, intros, strips, reformats = [], [], [], []
    for commit, path in order:
        b = buckets[(commit, path)]
        rem, add = b["removed"], b["added"]
        # group by key name so a two-pin file with one changed pin still pairs right
        for kname in sorted({key_of(x) for x in rem} | {key_of(x) for x in add}):
            r = [x for x in rem if key_of(x) == kname]
            a = [x for x in add if key_of(x) == kname]
            for i in range(min(len(r), len(a))):
                row = {
                    "commit": commit, "path": path, "key": kname,
                    "from": value_of(r[i]), "to": value_of(a[i]),
                    "from_line": r[i].strip(), "to_line": a[i].strip(),
                    "counter_saw_removed": bool(COUNTER.match(r[i])),
                    "counter_saw_added": bool(COUNTER.match(a[i])),
                    "ext": ext_of(path),
                }
                row["kind"] = ("code" if row["ext"] in CODE_EXT
                               else "receipt" if row["ext"] in RECEIPT_EXT else "other")
                if row["from"] != row["to"]:
                    relabels.append(row)
                else:
                    reformats.append(row)
            for x in r[min(len(r), len(a)):]:
                strips.append({"commit": commit, "path": path, "key": kname,
                               "value": value_of(x), "line": x.strip(),
                               "ext": ext_of(path)})
            for x in a[min(len(r), len(a)):]:
                intros.append({"commit": commit, "path": path, "key": kname,
                               "value": value_of(x), "line": x.strip(),
                               "ext": ext_of(path)})
    return relabels, intros, strips, reformats


def head_key_forms():
    """Every HEAD line under the wide population that starts with a revision-ish key."""
    # POSIX ERE (git grep -E) has no non-capturing groups: use the plain alternation
    pat = (r'^[[:blank:]]*"?(' + KEY_ALT + r'|[A-Za-z_]*[Rr]evision[A-Za-z_]*)'
           r'"?[[:blank:]]*[:=]')
    res = git("grep", "-n", "-I", "-E", "-e", pat, "HEAD", "--", *ROUND_DIRS)
    rows = []
    for ln in res.stdout.splitlines():
        # HEAD:path:lineno:content
        parts = ln.split(":", 3)
        if len(parts) < 4 or parts[0] != "HEAD":
            continue
        _, path, lineno, content = parts
        m = re.match(r'^[ \t]*"?([A-Za-z_]+)"?[ \t]*[:=]', content)
        kname = m.group(1) if m else "?"
        rows.append({"path": path, "line": int(lineno), "key": kname,
                     "counter_regex_matches": bool(COUNTER.match(content)),
                     "ext": ext_of(path), "content": content.strip()[:160]})
    return rows


def confirm_against_base_control(relabels):
    """Confirm/deny each UNDISCLOSED line the base control receipt names."""
    path = f"{ROOT}/{BASE_CONTROL}"
    expected = []
    with open(path, encoding="utf-8", errors="replace") as fh:
        for ln in fh:
            m = re.match(r"\s*UNDISCLOSED (\S+) ([0-9a-f]{7,40}) -> ([0-9a-f]{7,40}) at ([0-9a-f]{7,40})", ln)
            if m:
                expected.append({"path": m.group(1), "from": m.group(2),
                                 "to": m.group(3), "commit": m.group(4)})
    out = []
    for e in expected:
        hits = [r for r in relabels if r["path"] == e["path"]
                and r["from"].startswith(e["from"][:12])
                and r["to"].startswith(e["to"][:12])
                and r["commit"].startswith(e["commit"][:12])]
        out.append({"expected": e, "confirmed": bool(hits),
                    "derived": hits[0] if hits else None})
    return expected, out


ANCHORED_PIN = re.compile(
    r'(?m)^[ \t]*"?(revision|rev|sourceRevision|source_revision|measuredRevision|measured)"?'
    r'[ \t]*[:=][ \t]*"?([0-9a-f]{40})')
ANYWHERE_PIN = re.compile(
    r'"(revision|rev|sourceRevision|source_revision|measuredRevision|measured)"'
    r'[ \t]*:[ \t]*"([0-9a-f]{40})"')


def blob_pin_history():
    """Blob-level pin comparison over every path with >= 2 first-parent commits.

    Complements the line-pair scan: a compact single-line JSON receipt carries its
    revision token mid-line, where no line-anchored regex (this script's or the
    counter's) can see it.  Compares the set of (key, 40-hex) tokens of consecutive
    committed versions of each path, so a rewrite of such a token is still caught.
    """
    out = git("log", "--first-parent", "--name-only", "--format=C %H", "--", *ROUND_DIRS)
    cur, per_path = None, {}
    for ln in out.stdout.splitlines():
        if ln.startswith("C "):
            cur = ln[2:].strip()
        elif ln.strip():
            per_path.setdefault(ln.strip(), []).append(cur)
    multi = {p: cs for p, cs in per_path.items() if len(cs) >= 2}
    rows = []
    for path, cs in sorted(multi.items()):
        prev = None
        for c in reversed(cs):  # oldest first
            blob = git("show", f"{c}:{path}")
            if blob.returncode != 0:
                prev = None
                continue
            text = blob.stdout
            toks = set(ANCHORED_PIN.findall(text)) | set(ANYWHERE_PIN.findall(text))
            if prev is not None and toks != prev:
                for key, val in sorted(prev - toks):
                    for key2, val2 in sorted(toks - prev) or [("", "")]:
                        rows.append({"path": path, "commit": c, "key": key,
                                     "from": val, "to": val2,
                                     "ext": ext_of(path),
                                     "kind": "receipt" if ext_of(path) in RECEIPT_EXT else "other"})
            prev = toks
    return multi, rows


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--json")
    args = ap.parse_args()

    tip = git("rev-parse", "HEAD").stdout.strip()
    buckets, order, commits, blocks = scan_history()
    relabels, intros, strips, reformats = derive(buckets, order)
    head_rows = head_key_forms()
    expected, confirm = confirm_against_base_control(relabels)
    multi, blob_rows = blob_pin_history()

    receipt_relabels = [r for r in relabels if r["kind"] == "receipt"]
    code_relabels = [r for r in relabels if r["kind"] != "receipt"]

    print(f"HEAD {tip}")
    print(f"population {ROUND_DIRS[0]} .. {ROUND_DIRS[-1]} ({len(ROUND_DIRS)} dirs)")
    print(f"commits_scanned={len(commits)} diff_blocks={blocks} "
          f"commit_path_buckets={len(order)}")
    print(f"relabels_total={len(relabels)} receipt_like={len(receipt_relabels)} "
          f"non_receipt={len(code_relabels)} reformat_same_value={len(reformats)} "
          f"pin_introductions={len(intros)} pin_strips={len(strips)}")

    print("\n== RELABELS (receipt-like files) ==")
    for r in sorted(receipt_relabels, key=lambda x: (x["commit"], x["path"])):
        print(f"  {r['path']}  {r['from'][:12]} -> {r['to'][:12]}  at {r['commit'][:12]}"
              f"  key={r['key']} counter_regex={r['counter_saw_removed'] and r['counter_saw_added']}")

    print("\n== RELABELS (non-receipt files: code/prose; not pin relabels) ==")
    for r in sorted(code_relabels, key=lambda x: (x["commit"], x["path"])):
        print(f"  {r['path']}  {r['from'][:12]} -> {r['to'][:12]}  at {r['commit'][:12]}"
              f"  key={r['key']} ext={r['ext']}")

    print("\n== PIN INTRODUCTIONS (first pin in a file; not relabels) ==")
    for r in intros:
        print(f"  + {r['path']}  {r['key']}={r['value'][:12]} at {r['commit'][:12]}")
    print("\n== PIN STRIPS (pin line removed, nothing added) ==")
    for r in strips:
        print(f"  - {r['path']}  {r['key']}={r['value'][:12]} at {r['commit'][:12]}")

    print(f"\n== BLOB-LEVEL PIN HISTORY (paths with >=2 commits: {len(multi)}; "
          f"tokens compared anywhere in the blob) ==")
    line_seen = {(r["path"], r["commit"][:12], r["from"][:12], r["to"][:12]) for r in relabels}
    blob_only = [r for r in blob_rows
                 if (r["path"], r["commit"][:12], r["from"][:12], r["to"][:12]) not in line_seen]
    print(f"  blob_relabels={len(blob_rows)} not_seen_by_line_pairing={len(blob_only)}")
    for r in sorted(blob_rows, key=lambda x: (x["commit"], x["path"])):
        tag = "LINE-SEEN" if r not in blob_only else "BLOB-ONLY"
        print(f"  {tag} {r['path']}  {r['from'][:12]} -> {r['to'][:12] or '(none)'}"
              f"  at {r['commit'][:12]}  key={r['key']}")

    print(f"\n== CONFIRM AGAINST {BASE_CONTROL} ({len(expected)} UNDISCLOSED) ==")
    for c in confirm:
        e = c["expected"]
        tag = "CONFIRMED" if c["confirmed"] else "DENIED"
        print(f"  {tag} {e['path']} {e['from'][:12]} -> {e['to'][:12]} at {e['commit'][:12]}")
    derived_keys = {(r["path"], r["commit"][:12]) for r in relabels}
    exp_keys = {(e["path"], e["commit"][:12]) for e in expected}
    print("  derived-only (not in base control):")
    for k in sorted(derived_keys - exp_keys):
        print(f"    {k[0]} at {k[1]}")
    if not (derived_keys - exp_keys):
        print("    (none)")

    print(f"\n== HEAD KEY FORMS (wide population, {len(head_rows)} lines) ==")
    by_key: dict[str, list] = {}
    for r in head_rows:
        by_key.setdefault(r["key"], []).append(r)
    for k in sorted(by_key, key=lambda x: (-len(by_key[x]), x)):
        rows = by_key[k]
        missed = [r for r in rows if not r["counter_regex_matches"]]
        print(f"  key={k!r} lines={len(rows)} counter_regex_matches={len(rows) - len(missed)} "
              f"missed_by_counter={len(missed)}")
        for r in missed[:40]:
            print(f"      MISSED {r['path']}:{r['line']}  {r['content']}")
        if len(missed) > 40:
            print(f"      ... {len(missed) - 40} more")

    if args.json:
        with open(args.json, "w", encoding="utf-8") as fh:
            json.dump({"head": tip, "relabels": relabels, "intros": intros,
                       "strips": strips, "reformats": reformats,
                       "confirm": confirm, "head_key_forms": head_rows,
                       "blob_relabels": blob_rows,
                       "multi_commit_paths": len(multi)}, fh, indent=1)
        print(f"\njson written: {args.json}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
