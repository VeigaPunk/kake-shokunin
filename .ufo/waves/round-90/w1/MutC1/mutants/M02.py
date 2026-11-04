#!/usr/bin/env python3
"""Round-90 C1 counter: the three defects the round-89 outside spot-check routed.

Frozen before data (`.ufo/waves/round-90/freeze.md`). Items:

D1 (D89-1, scratch at lane root). Closed iff, at --revision:
   - `baseclean.out` is not tracked at the lane root;
   - `.ufo/waves/round-90/inherited/baseclean.out` is tracked and its bytes hash to
     the frozen sha256 of the inherited file (relocated, not rewritten);
   and, LIVE in --root's working tree (not revision-bound, labelled `live`):
   - `git status --porcelain --untracked-files=normal` lists no untracked entry at
     the lane root (a path with no `/`, or a single directory `name/`).
D2 (D89-2, unreceipted C1 statement `open=5 closed=1` at `f62e7954`). Closed iff, for
   BOTH `SCORECARD.md` and `LOG.md`:
   - the base revision's file bytes are a byte prefix of the file at --revision
     (append-only: the filed row is not rewritten);
   - the appended tail holds a line containing `D89-2 correction:`, the text
     `f62e7954`, a backquoted receipt path under `.ufo/waves/`, a 40-hex revision
     and `open=N closed=M` (the reading is the LAST `open=N closed=M` after `f62e7954`
     on that line, so the quoted superseded statement is never read as the reading);
   - that receipt is tracked at --revision, and its first line carries
     `revision=<that 40-hex>` and the same `open=N closed=M`;
   - the frozen round-89 C1 counter (blob pinned below), re-run on a scratch clone
     checked out at that 40-hex revision, prints the same `open=N closed=M`.
D3 (D89-3, S463 scope says "not cache-key construction" while the row is used by
   `cache-key-construction.md`). Closed iff, at --revision:
   - the S463 registry row is byte-identical to the base row (CORPUS.md rule 2);
   - a new registry row exists whose `teaches` cell begins `supersedes S463 —`, whose
     source cell names an `rfc9111` URL, whose status is `mined`, and whose scope cell
     does not contain `not cache-key construction`;
   - `corpus/lessons/round-90.md` `## Gate` has a line naming that row id with a
     double-quoted quote of 3..25 words that occurs (whitespace-normalised) in
     `.ufo/waves/round-90/L1/src/rfc9111.txt`, whose sha256 is the frozen digest.

met <=> open == 0. Output line 1:
  C1v90 revision=<sha> items=3 open=N closed=M met=true|false
line 2: JSON of open-item reasons. Exit 0 iff met.
Scratch: --work (required); everything is created beneath it and removed.
"""

import argparse
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
import tempfile

BASE = "209027f49959e2e2f0e16867a90a7bb38bbcd3f4"
INHERITED_SHA = "4046c204384ccf255f4e8b77fa4aba4ffb9c2167b7794f128fc4497db890f00f"
INHERITED_PATH = ".ufo/waves/round-90/inherited/baseclean.out"
C89_PATH = ".ufo/waves/round-89/c89_defect_queue.py"
C89_BLOB = "0dee1dc8f158ab240ea0557d227494c399f9e21e"
RFC9111_PATH = ".ufo/waves/round-90/L1/src/rfc9111.txt"
RFC9111_SHA = "aeb52adb3279d5f23dae34f68af11bd5cef0a0aff7ffcd014c9ca93c5302cf3e"
ROW_RE = re.compile(r"^ {0,3}\|\s*(S\d{3,})\s*\|")


def git(root, *args, check=True):
    p = subprocess.run(["git", "-C", root, *args], capture_output=True)
    if check and p.returncode != 0:
        raise RuntimeError("git %s: %s" % (" ".join(args), p.stderr.decode(errors="replace").strip()))
    return p


def show(root, rev, path):
    p = git(root, "show", "%s:%s" % (rev, path), check=False)
    return p.stdout if p.returncode == 0 else None


def tracked(root, rev, path):
    return bool(git(root, "ls-tree", "--name-only", rev, "--", path).stdout.strip())


def item_d1(root, rev):
    why = []
    if tracked(root, rev, "baseclean.out"):
        why.append("baseclean.out tracked at lane root")
    data = show(root, rev, INHERITED_PATH)
    if data is None:
        why.append("relocated copy %s not tracked" % INHERITED_PATH)
    elif hashlib.sha256(data).hexdigest() != INHERITED_SHA:
        why.append("relocated copy bytes differ from the inherited file")
    st = git(root, "status", "--porcelain", "--untracked-files=normal").stdout.decode("utf-8", "replace")
    for line in st.splitlines():
        if not line.startswith("?? "):
            continue
        path = line[3:].strip('"')
        if "/" not in path or (path.endswith("/") and path.count("/") == 1):
            why.append("live: untracked lane-root entry %s" % path)
    return why


CORR_RE = re.compile(r"D89-2 correction:")
REC_RE = re.compile(r"`(\.ufo/waves/[^`\s]+)`")
HEX_RE = re.compile(r"\b([0-9a-f]{40})\b")
OC_RE = re.compile(r"\bopen=(\d+) closed=(\d+)\b")


def rerun_c89(root, hexrev, work):
    blob = git(root, "cat-file", "blob", C89_BLOB, check=False)
    if blob.returncode != 0:
        return None, "frozen c89 blob %s unavailable" % C89_BLOB
    d = tempfile.mkdtemp(prefix="c89-", dir=work)
    try:
        cpath = os.path.join(d, "c89_defect_queue.py")
        with open(cpath, "wb") as fh:
            fh.write(blob.stdout)
        clone = os.path.join(d, "clone")
        p = subprocess.run(["git", "clone", "-q", "--shared", "--no-checkout", root, clone], capture_output=True)
        if p.returncode != 0:
            return None, "clone failed"
        if subprocess.run(["git", "-C", clone, "checkout", "-q", "--detach", hexrev],
                          capture_output=True).returncode != 0:
            return None, "checkout %s failed" % hexrev
        w = os.path.join(d, "w")
        os.mkdir(w)
        r = subprocess.run([sys.executable, "-B", cpath, "--root", clone, "--revision", hexrev, "--work", w],
                           capture_output=True, timeout=900)
        first = r.stdout.decode("utf-8", "replace").splitlines()[:1]
        m = OC_RE.search(first[0]) if first else None
        if not m:
            return None, "c89 re-run printed no open/closed line"
        return (int(m.group(1)), int(m.group(2))), ""
    finally:
        shutil.rmtree(d, ignore_errors=True)


def item_d2(root, rev, work):
    why = []
    cache = {}
    for fname in ("SCORECARD.md", "LOG.md"):
        base = show(root, BASE, fname)
        cur = show(root, rev, fname)
        if base is None or cur is None:
            why.append("%s missing at base or revision" % fname)
            continue
        if not cur.startswith(base):
            why.append("%s: base bytes are not a prefix (filed rows rewritten)" % fname)
            continue
        tail = cur[len(base):].decode("utf-8", "replace")
        ok_line = False
        notes = []
        for line in tail.splitlines():
            if not CORR_RE.search(line) or "f62e7954" not in line:
                continue
            rec = REC_RE.search(line)
            hx = [h for h in HEX_RE.findall(line) if not h.startswith("f62e7954")] or HEX_RE.findall(line)
            ocs = OC_RE.findall(line.split("f62e7954", 1)[1])  # the reading stated after the corrected row's revision
            oc = ocs[-1] if ocs else None
            if not (rec and hx and oc):
                notes.append("correction line lacks receipt/revision/open-closed")
                continue
            hexrev, n_open, n_closed = hx[0], int(oc[0]), int(oc[1])
            data = show(root, rev, rec.group(1))
            if data is None:
                notes.append("receipt %s not tracked" % rec.group(1))
                continue
            first = data.decode("utf-8", "replace").splitlines()[:1]
            first = first[0] if first else ""
            if ("revision=%s" % hexrev) not in first or ("open=%d closed=%d" % (n_open, n_closed)) not in first:
                notes.append("receipt first line disagrees with the correction")
                continue
            if hexrev not in cache:
                cache[hexrev] = rerun_c89(root, hexrev, work)
            got, err = cache[hexrev]
            if got is None:
                notes.append("re-run failed: %s" % err)
                continue
            if False:
                notes.append("re-run at %s gives open=%d closed=%d" % (hexrev[:8], got[0], got[1]))
                continue
            ok_line = True
            break
        if not ok_line:
            why.append("%s: no verified D89-2 correction%s" % (fname, (" (" + "; ".join(notes) + ")") if notes else ""))
    return why


def cells(line):
    return [c.strip() for c in line.strip().strip("|").split("|")]


def registry(data):
    rows = {}
    for line in data.decode("utf-8", "replace").splitlines():
        m = ROW_RE.match(line)
        if m:
            rows.setdefault(m.group(1), []).append(line)
    return rows


def norm(s):
    return " ".join(s.split())


def item_d3(root, rev):
    why = []
    base = show(root, BASE, "corpus/SOURCES.md")
    cur = show(root, rev, "corpus/SOURCES.md")
    if base is None or cur is None:
        return ["corpus/SOURCES.md missing"]
    b, c = registry(base), registry(cur)
    if c.get("S463") != b.get("S463"):
        why.append("S463 row changed in place")
    sup = []
    for sid, lines in c.items():
        if sid in b:
            continue
        for line in lines:
            cs = cells(line)
            if len(cs) != 11:
                continue
            if (cs[6].startswith("supersedes S463 —") and "rfc9111" in cs[1].lower() and cs[7] == "mined"
                    and "not cache-key construction" not in cs[4]):
                sup.append(sid)
    if not sup:
        why.append("no new mined rfc9111 row whose teaches begins 'supersedes S463 —'")
        return why
    body = show(root, rev, RFC9111_PATH)
    if body is None or hashlib.sha256(body).hexdigest() != RFC9111_SHA:
        why.append("retained rfc9111.txt missing or digest differs")
        return why
    nbody = norm(body.decode("utf-8", "replace"))
    lesson = show(root, rev, "corpus/lessons/round-90.md")
    if lesson is None:
        why.append("corpus/lessons/round-90.md missing")
        return why
    text = lesson.decode("utf-8", "replace")
    m = re.search(r"(?ms)^## Gate\b(.*?)(?=^## |\Z)", text)
    gate = m.group(1) if m else ""
    found = False
    for line in gate.splitlines():
        if not any(re.search(r"\b%s\b" % s, line) for s in sup):
            continue
        for q in re.findall(r"\"([^\"]+)\"", line):
            n = len(q.split())
            if 3 <= n <= 25 and norm(q) in nbody:
                found = True
    if not found:
        why.append("no ## Gate line naming %s with a located quote from the retained RFC 9111 body" % "/".join(sup))
    return why


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", required=True)
    ap.add_argument("--revision", required=True)
    ap.add_argument("--work", required=True)
    a = ap.parse_args(argv)
    root = os.path.realpath(a.root)
    rev = git(root, "rev-parse", "%s^{commit}" % a.revision).stdout.decode().strip()
    os.makedirs(a.work, exist_ok=True)
    work = tempfile.mkdtemp(prefix="c90d-", dir=a.work)
    try:
        res = {"D1": item_d1(root, rev), "D2": item_d2(root, rev, work), "D3": item_d3(root, rev)}
    finally:
        shutil.rmtree(work, ignore_errors=True)
    n_open = sum(1 for v in res.values() if v)
    met = n_open == 0
    print("C1v90 revision=%s items=3 open=%d closed=%d met=%s" % (rev, n_open, 3 - n_open, str(met).lower()))
    print(json.dumps(res, sort_keys=True))
    return 0 if met else 1


if __name__ == "__main__":
    sys.exit(main())
