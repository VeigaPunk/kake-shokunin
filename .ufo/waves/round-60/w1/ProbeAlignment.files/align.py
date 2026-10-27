#!/usr/bin/env python3
"""align.py — ProbeAlignment prototype for contract C2 (round 60).

Existential alignment check for the append-only correction rule:

    B (base lines) must be an ordered subsequence of R (revision lines),
    split on b"\\n" as bytes (no decoding, no normalisation).  The inserted
    lines (R positions not matched) form maximal runs.  A run after the last
    matched base line is an end-of-file append (always allowed).  Every other
    run must BEGIN with a line carrying a visible correction tag
    \\[r[0-9]+-correction [0-9]{4}-[0-9]{2}-[0-9]{2}\\] matched outside an
    HTML comment and outside a backtick code span.

min_untagged(B, R) returns the MINIMUM, over all subsequence alignments of B
into R, of the number of non-EOF runs whose first line lacks a visible tag.
It returns 0 iff some alignment is clean (the contract's existential rule),
and None when B is not a subsequence of R (the guard reports `changed`).

Ambiguity matters: when a base line occurs several times in R, different
alignments move where an insertion run STARTS (the run after a match at
position k always starts at k+1, but its END, and whether it is empty,
depends on the next match).  Greedy leftmost/rightmost can pick a match that
makes a run start on an untagged line while another alignment starts it on a
tagged line (or makes it empty).  This module quantifies that gap.

Cost model: O(m + sum_i |occ(B[i-1])| + |occ(B[i])|) time, O(m) space,
where occ(x) are the positions of line x in R.  Worst case O(n*m) when a
line value repeats (blank lines, repeated tag lines); O(n+m) when all lines
are distinct.

Visibility predicate (documented choices):
  * HTML comments `<!--` ... `-->` carry state ACROSS lines; comment bytes
    are masked to NUL so a tag can never span a comment.
  * Backtick code spans are masked per line, BEFORE comment scanning
    (CommonMark: a backtick run binds tighter; `<!--` inside a code span is
    literal).  A run of k backticks closes at the next run of exactly k
    backticks on the same line, else it is literal.  Code spans are not
    tracked across lines (fence state is a guard concern, not this probe's;
    contract fixtures put the tag on the run's first physical line).
"""

import bisect
import re

TAG_RE = re.compile(rb"\[r[0-9]+-correction [0-9]{4}-[0-9]{2}-[0-9]{2}\]")
_OPEN = b"<!--"
_CLOSE = b"-->"


def _mask_code_spans(line: bytes) -> bytes:
    """Mask bytes inside backtick code spans to NUL (same line only)."""
    buf = bytearray(line)
    n = len(buf)
    i = 0
    while i < n:
        if buf[i] != 0x60:  # '`'
            i += 1
            continue
        j = i
        while j < n and buf[j] == 0x60:
            j += 1
        run_len = j - i
        # find closing run of exactly run_len backticks
        k = j
        closed = False
        while k < n:
            if buf[k] == 0x60:
                e = k
                while e < n and buf[e] == 0x60:
                    e += 1
                if e - k == run_len:
                    # mask [i, e)
                    for p in range(i, e):
                        buf[p] = 0
                    i = e
                    closed = True
                    break
                k = e
            else:
                k += 1
        if not closed:
            i = j  # literal run, keep scanning after it
    return bytes(buf)


def visible_tags(lines):
    """tag[i] = True iff R line i carries the correction tag outside comments
    and outside backtick code spans.  Comment state carries across lines."""
    tags = []
    in_comment = False
    for raw in lines:
        line = _mask_code_spans(raw)
        vis = bytearray(line)
        i = 0
        n = len(vis)
        while i < n:
            if in_comment:
                j = bytes(vis).find(_CLOSE, i)
                if j < 0:
                    for p in range(i, n):
                        vis[p] = 0
                    i = n
                else:
                    for p in range(i, j + 3):
                        vis[p] = 0
                    in_comment = False
                    i = j + 3
            else:
                j = bytes(vis).find(_OPEN, i)
                if j < 0:
                    i = n
                else:
                    for p in range(j, min(j + 4, n)):
                        vis[p] = 0
                    in_comment = True
                    i = j + 4
        tags.append(TAG_RE.search(bytes(vis)) is not None)
    return tags


def _occurrences(R, value):
    return [p for p, b in enumerate(R) if b == value]


def min_untagged(B, R, tag=None):
    """Minimum number of non-EOF insertion runs whose first line lacks a
    visible correction tag, over all alignments of B as a subsequence of R.

    Returns None when B is not a subsequence of R (guard: `changed`).
    Returns 0 when some alignment has every non-EOF run tagged (clean).
    Edge: empty B -> 0 (the whole revision is one EOF append; no non-EOF
    run exists, matching "a run after the last matched base line" vacuously).
    """
    n, m = len(B), len(R)
    if n == 0:
        return 0
    if m < n:
        return None
    if tag is None:
        tag = visible_tags(R)

    INF = float("inf")
    # D[j] = min bad-run count of an alignment of B[0:i] into R[0:j+1]
    #        whose LAST matched pair is (B[i-1], R[j]).
    # i = 1: the only preceding gap is gap_0 = R[0:j]; it is a non-EOF run
    # iff j > 0, and bad iff its first line R[0] is untagged.
    D = {}
    for j in _occurrences(R, B[0]):
        D[j] = 0 if (j == 0 or tag[0]) else 1
    if not D:
        return None

    for i in range(1, n):
        prev_occ = _occurrences(R, B[i - 1])
        cur_occ = _occurrences(R, B[i])
        if not cur_occ:
            return None
        # For a previous match at k (< j): the gap R[k+1:j] is empty when
        # k == j-1 (cost D[k]); else it is a run starting at k+1, cost
        # D[k] + (0 if tag[k+1] else 1).  Prefix minima over prev_occ of
        # D[k] + pen(k) give O(1) lookup per j.
        pm = []
        run_min = INF
        for k in prev_occ:
            v = D.get(k, INF)
            if v < INF:
                v += 0 if (k + 1 >= m or tag[k + 1]) else 1
            if v < run_min:
                run_min = v
            pm.append(run_min)
        Dn = {}
        for j in cur_occ:
            best = D.get(j - 1, INF)  # empty gap: j-1 in prev_occ already
            idx = bisect.bisect_left(prev_occ, j) - 1
            if idx >= 0 and pm[idx] < best:
                best = pm[idx]
            if best < INF:
                Dn[j] = best
        if not Dn:
            return None
        D = Dn
    # Trailing gap R[j+1:m] is the EOF append: free, whatever its content.
    return min(D.values())


def is_clean(B, R):
    """True iff B is a subsequence of R and some alignment is clean."""
    return min_untagged(B, R) == 0


def greedy_count(B, R, tag=None, rightmost=False):
    """Bad-run count of the single greedy alignment (leftmost default,
    rightmost when rightmost=True).  None when B is not a subsequence."""
    n, m = len(B), len(R)
    if n == 0:
        return 0
    if tag is None:
        tag = visible_tags(R)
    pos = []
    if not rightmost:
        k = 0
        for b in B:
            while k < m and R[k] != b:
                k += 1
            if k == m:
                return None
            pos.append(k)
            k += 1
    else:
        k = m - 1
        for b in reversed(B):
            while k >= 0 and R[k] != b:
                k -= 1
            if k < 0:
                return None
            pos.append(k)
            k -= 1
        pos.reverse()
    edges = [(0, pos[0])] + [(pos[t] + 1, pos[t + 1]) for t in range(n - 1)]
    bad = 0
    for a, bnd in edges:
        if a < bnd and not tag[a]:
            bad += 1
    return bad


def brute_min(B, R, tag=None):
    """Exhaustive oracle over all alignments (small sizes only)."""
    from itertools import combinations

    n, m = len(B), len(R)
    if n == 0:
        return 0
    if tag is None:
        tag = visible_tags(R)
    best = None
    for f in combinations(range(m), n):
        if any(R[f[t]] != B[t] for t in range(n)):
            continue
        bad = 0
        prev = -1
        for t in range(n):
            if f[t] > prev + 1 and not tag[prev + 1]:
                bad += 1
            prev = f[t]
        if best is None or bad < best:
            best = bad
    return best


if __name__ == "__main__":
    # sanity: the minimal disagreement examples plus contract fixtures
    T = b"[r60-correction 2026-10-27]"
    cases = [
        ([b"a", T, b"b"], [b"a", T, b"a", b"U", T, b"b"]),  # greedy=1, min=0
        ([b"a", b"", b"b"], [b"a", T, b"", b"", b"b"]),     # K15 shape
        ([b"a", b"b", b"c"], [b"a", b"b", b"b", b"c"]),     # K16 shape
        ([b"a", b"b"], [b"a", b"U", b"V", b"b"]),           # K3 shape
        ([b"a", b"b"], [b"a", T, b"U", b"b"]),              # K2 shape
    ]
    for B, R in cases:
        print(min_untagged(B, R), greedy_count(B, R), greedy_count(B, R, rightmost=True))
