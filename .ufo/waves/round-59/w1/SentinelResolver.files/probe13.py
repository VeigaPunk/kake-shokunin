#!/usr/bin/env python3
"""SentinelResolver probe 13: mitigation options for the realpath/open TOCTOU."""
from __future__ import annotations

import os
import shutil
import threading
import time

SCRATCH = "/fast/scratch/hyaku/kake-r59/SentinelResolver"
WORK = os.path.join(SCRATCH, "work13")


def put(base, rel, text):
    p = os.path.join(base, rel)
    os.makedirs(os.path.dirname(p), exist_ok=True)
    with open(p, "w", encoding="utf-8", newline="") as fh:
        fh.write(text)


def main():
    shutil.rmtree(WORK, ignore_errors=True)
    os.makedirs(WORK)
    base = os.path.join(WORK, "t")
    root = os.path.join(base, "lane")
    put(root, "corpus/knowledge/victim.md", "INSIDE\n")
    put(base, "outside.md", "OUTSIDE-SECRET\n")
    root_real = os.path.realpath(root)
    link = os.path.join(root, "corpus", "knowledge", "race.md")
    inside_t = os.path.join(root, "corpus", "knowledge", "victim.md")
    outside_t = os.path.join(base, "outside.md")
    os.symlink(inside_t, link)

    stop = threading.Event()

    def flipper():
        while not stop.is_set():
            for tgt in (inside_t, outside_t):
                tmp = link + ".tmp"
                try:
                    if os.path.lexists(tmp):
                        os.unlink(tmp)
                    os.symlink(tgt, tmp)
                    os.replace(tmp, link)
                except OSError:
                    pass

    t = threading.Thread(target=flipper, daemon=True)
    t.start()

    # A: check-then-open (base pattern)
    leaks_a = 0
    # B: open the fd first, then resolve /proc/self/fd/<fd> and check containment
    leaks_b = 0
    for _ in range(4000):
        real = os.path.realpath(link)
        if real == root_real or real.startswith(root_real + os.sep):
            try:
                with open(link, "rb") as fh:
                    if b"OUTSIDE-SECRET" in fh.read():
                        leaks_a += 1
            except OSError:
                pass
        try:
            fd = os.open(link, os.O_RDONLY)
        except OSError:
            continue
        try:
            actual = os.path.realpath(f"/proc/self/fd/{fd}")
            if actual == root_real or actual.startswith(root_real + os.sep):
                with os.fdopen(fd, "rb") as fh:
                    data = fh.read()
                fd = -1
                if b"OUTSIDE-SECRET" in data:
                    leaks_b += 1
        finally:
            if fd >= 0:
                os.close(fd)
    stop.set()
    t.join(timeout=2)
    print("### TOCTOU mitigation comparison (4000 iterations each)")
    print(f"  A check-then-open (the base pattern): outside reads = {leaks_a}")
    print(f"  B open-then-resolve /proc/self/fd    : outside reads = {leaks_b}")
    print()


if __name__ == "__main__":
    main()
