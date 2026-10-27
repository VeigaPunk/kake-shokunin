#!/usr/bin/env python3 -B
"""Classify corpus/knowledge/**/*.md changes on the real kake-shokunin lane.

Implements the same rule the round-60 C2 contract gives scripts/append_guard.py,
plus a finer-grained label for reporting:

  per file (regular blob at the older side):
    * missing or non-regular at the newer side          -> deleted      (tool: `deleted P`)
    * newer blob not an ordered supersequence of older  -> changed      (tool: `changed P`)
    * supersequence, exists alignment where every
      inserted run before the last matched base line
      begins with a visible [rN-correction YYYY-MM-DD]  -> tagged_insertion (tool: clean)
      (if the older blob is an exact prefix this is
       reported separately as eof_append; also clean)
    * supersequence, no such alignment                  -> untagged_insertion
                                                          (tool: `untagged_insertion P:<line>`)
  paths new at the newer side (A/R/C dest)              -> new_file     (tool: unchecked)
  R status (rename)                                     -> rename       (tool: `deleted <old>`)
  identical blob sha                                    -> identical    (tool: unchecked)

A "visible" tag = regex r"\[r[0-9]+-correction [0-9]{4}-[0-9]{2}-[0-9]{2}\]"
matching outside HTML comments (<!-- ... -->) and outside backtick code
spans (`...`). Implemented per line: comments are stripped first (an
unclosed `<!--` hides the rest of the line), then backtick spans.

Usage:
  classify_lane_changes.py --root <lane> commits A..B   # per-commit table
  classify_lane_changes.py --root <lane> diff OLD NEW   # endpoint diff (tool run)
"""
import re
import subprocess
import sys

TAG = re.compile(rb"\[r[0-9]+-correction [0-9]{4}-[0-9]{2}-[0-9]{2}\]")
NEAR = re.compile(rb"\[r[0-9]+[^\]]{0,40}\]")
COMMENT = re.compile(rb"<!--.*?-->")
OPEN_COMMENT = re.compile(rb"<!--")
BACKTICK = re.compile(rb"`[^`]*`")


def visible_tag(line):
    """Matched tag bytes on this line outside comments/code spans, or None."""
    s = COMMENT.sub(b"", line)
    s = OPEN_COMMENT.split(s, 1)[0]
    s = BACKTICK.sub(b"", s)
    m = TAG.search(s)
    return m.group(0) if m else None


def git(root, *args, binary=False):
    out = subprocess.run(
        ["git", "-C", root, *args],
        stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True,
    ).stdout
    return out if binary else out.decode("utf-8", "replace")


def blob(root, rev, path):
    """Blob bytes at rev:path, or None if missing."""
    try:
        return git(root, "cat-file", "blob", f"{rev}:{path}", binary=True)
    except subprocess.CalledProcessError:
        return None


def raw_entries(root, old, new):
    """git diff-tree -r --find-renames -z old new -> list of dicts."""
    raw = git(root, "diff-tree", "-r", "--find-renames", "-z", old, new,
              binary=True)
    parts = raw.split(b"\x00")
    if parts and parts[-1] == b"":
        parts.pop()
    ents = []
    i = 0
    while i < len(parts):
        head = parts[i].decode("ascii", "replace")
        i += 1
        seg = head.split(" ")
        m1, m2, s1, s2, st = seg[0][1:], seg[1], seg[2], seg[3], seg[4]
        p1 = parts[i].decode("utf-8", "surrogateescape"); i += 1
        p2 = None
        if st and st[0] in "RC":
            p2 = parts[i].decode("utf-8", "surrogateescape"); i += 1
        ents.append(dict(m1=m1, m2=m2, s1=s1, s2=s2, st=st, p1=p1, p2=p2))
    return ents


def regular(mode):
    return mode.startswith("100")


def in_scope(path):
    return path.startswith("corpus/knowledge/") and path.endswith(".md")


def split_lines(b):
    return b.split(b"\n")


def prefix(b_lines, r_lines):
    return len(b_lines) <= len(r_lines) and r_lines[:len(b_lines)] == b_lines


def tagged_alignment(B, R):
    """Does an alignment exist embedding B in R where every inserted run not
    wholly after the last matched base line begins with a tagged line?
    Returns a reconstructed match list (indices into R, len==len(B)) or None.
    """
    m, n = len(B), len(R)
    if m == 0:
        return [] if n == 0 else None  # nonempty base required for a run tail
    if m > n:
        return None
    tag = [visible_tag(R[p]) is not None for p in range(n)]
    prev = None           # reach[i-1][p]
    parents = {}          # (i,p) -> match position of B[i-1]
    for i in range(m):
        row = [False] * n
        prefix_or = [False] * n
        if prev is not None:
            run = False
            for pos in range(n):
                if pos > 0 and prev[pos - 1] and tag[pos]:
                    run = True
                prefix_or[pos] = run
        for p in range(i, n):
            if R[p] != B[i]:
                continue
            if i == 0:
                if p == 0 or tag[0]:
                    row[p] = True
                    parents[(i, p)] = None
            else:
                if p > 0 and prev[p - 1]:
                    row[p] = True
                    parents[(i, p)] = p - 1
                elif p > 1 and prefix_or[p - 2]:
                    row[p] = True
                    q = 0
                    while not (prev[q] and tag[q + 1]):
                        q += 1
                    parents[(i, p)] = q
        prev = row
    if prev is None:
        return None
    ends = [p for p in range(n) if prev[p]]
    if not ends:
        return None
    p = ends[0]  # earliest end: leftmost alignment
    match = [0] * m
    i = m - 1
    while True:
        match[i] = p
        if i == 0:
            break
        p = parents[(i, p)]
        i -= 1
    return match


def subsequence(B, R):
    it = iter(R)
    for b in B:
        for r in it:
            if r == b:
                break
        else:
            return False
    return True


def leftmost_match(B, R):
    match, j = [], 0
    for b in B:
        while R[j] != b:
            j += 1
        match.append(j)
        j += 1
    return match


def runs_of(match, n_r):
    """Inserted (start,end) R-index ranges between consecutive matches."""
    out = []
    prev = -1
    for p in match:
        if p > prev + 1:
            out.append((prev + 1, p - 1))
        prev = p
    if prev + 1 < n_r:
        out.append((prev + 1, n_r - 1))
    return out


def classify_pair(B_bytes, R_bytes):
    """-> (kind, detail). kind in eof_append / tagged_insertion /
    untagged_insertion / changed / identical."""
    if B_bytes == R_bytes:
        return "identical", {}
    B, R = split_lines(B_bytes), split_lines(R_bytes)
    if prefix(B, R):
        return "eof_append", {"added": len(R) - len(B)}
    match = tagged_alignment(B, R)
    if match is not None:
        tags = {}
        for a, b in runs_of(match, len(R)):
            t = visible_tag(R[a])
            if t:
                tags.setdefault(t.decode("ascii"), []).append(a + 1)
        return "tagged_insertion", {"tags": tags}
    if subsequence(B, R):
        match = leftmost_match(B, R)
        first = None
        for a, b in runs_of(match, len(R)):
            if a <= match[-1]:  # run not wholly after last match
                first = a + 1
                break
        near = sorted({s.decode("utf-8", "replace")
                       for a, b in runs_of(match, len(R))
                       for s in NEAR.findall(R[a])})
        return "untagged_insertion", {"line": first, "near": near}
    return "changed", {}


def endpoint_rows(root, old, new):
    """Tool-style classification for one endpoint diff.
    Returns (rows, findings): rows = (path, kind, detail); findings = tool lines."""
    findings, rows = [], []
    for e in raw_entries(root, old, new):
        st = e["st"]
        if st[0] == "R":
            p, d = e["p1"], e["p2"]
            if in_scope(p):
                rows.append((p, "rename", f"-> {d} (tool: deleted {p})"))
                findings.append(f"deleted {p}")
            elif in_scope(d):
                rows.append((d, "rename_dest", f"<- {p} (unchecked new path)"))
            continue
        path = e["p1"]
        if not in_scope(path):
            continue
        if st == "A":
            rows.append((path, "new_file", "unchecked"))
            continue
        if st == "D" or not regular(e["m2"]):
            rows.append((path, "deleted", ""))
            findings.append(f"deleted {path}")
            continue
        B = blob(root, old, e["p1"])
        R = blob(root, new, path)
        kind, det = classify_pair(B, R)
        if kind == "changed":
            findings.append(f"changed {path}")
        elif kind == "untagged_insertion":
            findings.append(f"untagged_insertion {path}:{det['line']}")
        rows.append((path, kind, det))
    return rows, findings


def cmd_diff(root, old, new):
    rows, findings = endpoint_rows(root, old, new)
    for path, kind, det in rows:
        print(f"{kind:22s} {path} {det}")
    print("--- tool findings ---")
    for f in findings or ["(none — exit 0)"]:
        print(f)
    print(f"files={len(rows)} findings={len(findings)}")


def cmd_commits(root, rng):
    commits = git(root, "log", "--format=%H%x09%s", "--first-parent",
                  "--reverse", rng).splitlines()
    for line in commits:
        if not line.strip():
            continue
        sha, subj = line.split("\t", 1)
        for e in raw_entries(root, sha + "^", sha):
            st = e["st"]
            if st[0] == "R":
                if in_scope(e["p1"]) or in_scope(e["p2"]):
                    print(f"{sha[:10]} {'R':2s} rename              "
                          f"{e['p1']} -> {e['p2']}")
                continue
            path = e["p1"]
            if not in_scope(path):
                continue
            if st == "A":
                print(f"{sha[:10]} {'A':2s} new_file            {path}")
                continue
            if st == "D" or not regular(e["m2"]):
                print(f"{sha[:10]} {st:2s} deleted             {path}")
                continue
            B = blob(root, sha + "^", e["p1"])
            R = blob(root, sha, path)
            kind, det = classify_pair(B, R)
            extra = ""
            if kind == "tagged_insertion":
                extra = " ".join(f"{t}@{ls}" for t, ls in det["tags"].items())
            elif kind == "untagged_insertion":
                extra = f"line={det['line']} near={det['near']}"
            elif kind == "eof_append":
                extra = f"+{det['added']} lines"
            print(f"{sha[:10]} {st:2s} {kind:19s} {path} {extra}")


def main():
    args = sys.argv[1:]
    root = "."
    if "--root" in args:
        i = args.index("--root")
        root = args[i + 1]
        del args[i:i + 2]
    if not args:
        print(__doc__)
        return 64
    if args[0] == "diff":
        cmd_diff(root, args[1], args[2])
        return 0
    if args[0] == "commits":
        cmd_commits(root, args[1])
        return 0
    print(__doc__)
    return 64


if __name__ == "__main__":
    sys.exit(main())
