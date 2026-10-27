#!/usr/bin/env python3
"""SentinelResolver probe 5: what a K10-style fix (follow in-lane symlinked dirs) must defend against."""
from __future__ import annotations

import os
import shutil
import stat
import time

SCRATCH = "/fast/scratch/hyaku/kake-r59/SentinelResolver"
WORK = os.path.join(SCRATCH, "work5")


def put(base, rel, text):
    p = os.path.join(base, rel)
    os.makedirs(os.path.dirname(p), exist_ok=True)
    with open(p, "w", encoding="utf-8", newline="") as fh:
        fh.write(text)


def fresh(name):
    root = os.path.join(WORK, name)
    shutil.rmtree(root, ignore_errors=True)
    os.makedirs(root)
    return root


def walk_candidate(base, root, follow=True):
    """A candidate traversal: follow symlinked dirs, keep the realpath containment check, skip non-regular files."""
    root_real = os.path.realpath(root)
    seen = set()
    out = []
    for dirpath, dirnames, filenames in os.walk(base, followlinks=follow):
        dirnames.sort()
        real = os.path.realpath(dirpath)
        if real in seen:
            dirnames[:] = []
            continue
        seen.add(real)
        for name in sorted(filenames):
            if not name.endswith(".md"):
                continue
            full = os.path.join(dirpath, name)
            r = os.path.realpath(full)
            if not (r == root_real or r.startswith(root_real + os.sep)):
                continue
            try:
                st = os.lstat(full)
            except OSError:
                continue
            if not stat.S_ISREG(st.st_mode):
                continue
            out.append(full)
    return out


def main():
    shutil.rmtree(WORK, ignore_errors=True)
    os.makedirs(WORK)

    # --- candidate traversal on a cycle
    base = fresh("cycle")
    lp = os.path.join(base, "lane")
    put(lp, "corpus/knowledge/ok.md", "x\n")
    put(lp, "store/hidden.md", "Cites S1.\n")
    os.symlink("../../store", os.path.join(lp, "corpus", "knowledge", "linked"))
    os.symlink("..", os.path.join(lp, "corpus", "knowledge", "up"))
    t0 = time.time()
    try:
        files = walk_candidate(os.path.join(lp, "corpus", "knowledge"), lp)
        print("### candidate traversal (follow + containment + visited-realpath set)")
        print(f"  files={len(files)} elapsed={time.time()-t0:.2f}s")
        for f in files[:5]:
            print("   |", f)
        if time.time() - t0 > 20:
            print("  NO TERMINATION")
    except Exception as exc:
        print("  exception:", exc)
    print()

    # --- candidate traversal on an escape
    base = fresh("escape")
    lp = os.path.join(base, "lane")
    put(lp, "corpus/knowledge/ok.md", "x\n")
    put(base, "outside/leak.md", "Cites S9999.\n")
    os.symlink("../../../outside", os.path.join(lp, "corpus", "knowledge", "esc"))
    files = walk_candidate(os.path.join(lp, "corpus", "knowledge"), lp)
    print("### candidate traversal, '..' escape")
    print(f"  files_read={len(files)} -> {[os.path.relpath(f, lp) for f in files]}")
    print("  (the outside file is skipped only because the per-file realpath containment check survives)")
    print()

    # --- candidate traversal with a FIFO inside
    base = fresh("fifo")
    lp = os.path.join(base, "lane")
    put(lp, "corpus/knowledge/ok.md", "x\n")
    os.mkfifo(os.path.join(lp, "corpus", "knowledge", "pipe.md"))
    t0 = time.time()
    files = walk_candidate(os.path.join(lp, "corpus", "knowledge"), lp)
    print("### candidate traversal with a FIFO inside corpus/knowledge")
    print(f"  files_read={len(files)} elapsed={time.time()-t0:.2f}s (the FIFO is skipped only by an S_ISREG check)")
    print()

    # --- candidate traversal where the symlinked dir points at a huge tree
    base = fresh("huge")
    lp = os.path.join(base, "lane")
    put(lp, "corpus/knowledge/ok.md", "x\n")
    big = os.path.join(base, "big")
    for i in range(400):
        put(big, f"d{i}/f.md", "Cites S1.\n")
    os.symlink("../../big", os.path.join(lp, "corpus", "knowledge", "big"))
    t0 = time.time()
    files = walk_candidate(os.path.join(lp, "corpus", "knowledge"), lp)
    print("### candidate traversal, symlinked dir holding 400 files")
    print(f"  files_read={len(files)} elapsed={time.time()-t0:.2f}s")
    print()


if __name__ == "__main__":
    main()
