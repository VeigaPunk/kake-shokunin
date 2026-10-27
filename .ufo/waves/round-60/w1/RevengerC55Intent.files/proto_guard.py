#!/usr/bin/env python3
"""Scratch prototype of the round-60 contract C2 rule (NOT the lane tool).

Purpose: check, against observed bytes, whether the contract's append-guard rule
accepts the round-59 tagged in-file correction (R1) and which of c55's
`head_changed` protections survive.  Read-only: git cat-file on the lane.
"""
import re
import subprocess
import sys

TAG_RE = re.compile(rb"\[r[0-9]+-correction [0-9]{4}-[0-9]{2}-[0-9]{2}\]")
COMMENT_RE = re.compile(rb"<!--.*?-->", re.S)
SPAN_RE = re.compile(rb"`[^`]*`", re.S)


def blob(root, rev, path):
    p = subprocess.run(["git", "-C", root, "cat-file", "blob", f"{rev}:{path}"],
                       stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)
    return p.stdout if p.returncode == 0 else None


def tagged(line: bytes) -> bool:
    vis = SPAN_RE.sub(b"", COMMENT_RE.sub(b"", line))
    return TAG_RE.search(vis) is not None


def accepts(base: bytes, rev: bytes) -> tuple[bool, str]:
    B = base.split(b"\n")
    R = rev.split(b"\n")
    # can[i][j]: B[:i] matched, B[i-1] at R[j-1], all internal gaps ok
    n, m = len(B), len(R)
    prev = [False] * (m + 1)
    # i == 0: nothing matched yet; every prefix is fine (leading gap is a run)
    def gap_ok(j0, j1):
        """R[j0:j1] is the unmatched run between matched positions."""
        if j0 >= j1:
            return True
        return tagged(R[j0])
    # DP over i
    cur = [False] * (m + 1)
    # i = 0 rows: we need gap_ok for a run starting at 0 -> handled when first match at j
    reach = [False] * (m + 1)   # reach[j] = can start matching B[i] at R[j] with prefix ok
    for j in range(m + 1):
        reach[j] = True if j == 0 else gap_ok(0, j)
    for i in range(1, n + 1):
        cur = [False] * (m + 1)
        for j in range(1, m + 1):
            if B[i - 1] == R[j - 1] and reach[j - 1]:
                cur[j] = True
        # build reach for next i: gap R[j..k-1] must be ok when B[i-1] matched at R[j-1]
        reach = [False] * (m + 1)
        for k in range(m + 1):
            ok = False
            for j in range(1, k + 1):
                if cur[j] and gap_ok(j, k):
                    ok = True
                    break
            reach[k] = ok
    # final tail after last match is an EOF append: unrestricted
    for j in range(0, m + 1):
        if (j == 0 and n == 0) or (j > 0 and cur[j]):
            return True, "ok"
    return False, "changed"


def main():
    root = "/home/vgpnk/Projects/shokunin/kake-shokunin"
    base_rev = "fd6303ce5c14b3f892dec586297a942ab6e4193b"
    rev = "97cdc122379711c2b02a8970752c8782da3ac81d"
    p = "corpus/knowledge/crawler-identity.md"
    B = blob(root, base_rev, p)
    R = blob(root, rev, p)
    print("R1 base fd6303ce -> rev 97cdc12 :", accepts(B, R))

    # V7-shaped attack: truncate every base body to 1500 chars (c55 v2 let it pass)
    trunc = b"\n".join(B.split(b"\n")[:20])
    print("truncation of base body          :", accepts(B, trunc))

    # K8: tagged line second in the run
    tag = b"**[r59-correction 2026-10-27]** x"
    lines = B.split(b"\n")
    mid = len(lines) // 2
    k8 = b"\n".join(lines[:mid] + [b"untagged first", tag] + lines[mid:])
    print("K8 tag on second run line        :", accepts(B, k8))

    # K9 / K10: tag hidden in comment / code span
    k9 = b"\n".join(lines[:mid] + [b"<!-- [r59-correction 2026-10-27] -->"] + lines[mid:])
    k10 = b"\n".join(lines[:mid] + [b"`[r59-correction 2026-10-27]`"] + lines[mid:])
    print("K9 tag inside HTML comment       :", accepts(B, k9))
    print("K10 tag inside code span         :", accepts(B, k10))

    # P7 residual: tag laundering across two rounds.
    # Round A: tagged 1-line run mid-file (accepted).  Round B (base = A's tip):
    # an UNTAGGED line is inserted directly after the tagged line.
    a = b"\n".join(lines[:mid] + [tag] + lines[mid:])
    b = b"\n".join(lines[:mid] + [tag, b"untagged smuggled line"] + lines[mid:])
    print("round A (tagged run)             :", accepts(B, a))
    print("round B base=A -> untagged after tag:", accepts(a, b))
    print("pinned base B -> R2 (same bytes) :", accepts(B, b))

    # c55 head_changed verdict on the same pair, for contrast
    def head_changed(old, new):
        return not new.startswith(old)

    print("c55 head_changed B->R2           :", head_changed(B, b))


if __name__ == "__main__":
    main()
