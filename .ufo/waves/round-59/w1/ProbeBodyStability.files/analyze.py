#!/usr/bin/env python3
"""ProbeBodyStability: compare full bodies + counter-visible article text nodes across 3 spaced fetches per URL.

Uses the round-59 counter's own content_window()/text_segments() so "article text" means exactly what the
C3 counter's C5 test sees.
"""
from __future__ import annotations

import difflib
import hashlib
import importlib.util
import os
import re
import sys

LANE = "/home/vgpnk/Projects/shokunin/kake-shokunin"
WAVE = f"{LANE}/.ufo/waves/round-59"
SCRATCH = "/fast/scratch/hyaku/kake-r59/ProbeBodyStability"

spec = importlib.util.spec_from_file_location("c59qt", f"{WAVE}/c59_quote_truth.py")
qt = importlib.util.module_from_spec(spec)
spec.loader.exec_module(qt)

IDS = qt.NEW_ROWS


def body_text(path):
    with open(path, encoding="utf-8", newline="") as fh:
        return qt.re.sub(r"\s+", " ", fh.read())


def raw_body(path):
    with open(path, "rb") as fh:
        return fh.read()


def segs(text, sid):
    return [s.strip() for s in qt.text_segments(text, sid)]


def diff_regions(a, b, label):
    """Return differing regions as (label, a_excerpt, b_excerpt) tuples."""
    out = []
    sm = difflib.SequenceMatcher(None, a, b, autojunk=False)
    for tag, i1, i2, j1, j2 in sm.get_opcodes():
        if tag == "equal":
            continue
        out.append((tag, a[max(0, i1 - 60):i2 + 60], b[max(0, j1 - 60):j2 + 60]))
    return out


def main():
    report = {}
    for sid in IDS:
        retained = f"{WAVE}/sources/{sid}.html"
        paths = [f"{SCRATCH}/fetches/{sid}.{n}.html" for n in (1, 2, 3)]
        print(f"=== {sid} ===")
        rec_raw = raw_body(retained)
        print(f"retained bytes={len(rec_raw)} sha256={hashlib.sha256(rec_raw).hexdigest()}")
        print(f"counter BODY_SHA256={qt.BODY_SHA256[sid]} match={hashlib.sha256(rec_raw).hexdigest()==qt.BODY_SHA256[sid]}")
        bodies = []
        for n, p in enumerate(paths, 1):
            rb = raw_body(p)
            bodies.append((n, rb, body_text(p)))
            print(f"fetch{n} bytes={len(rb)} sha256={hashlib.sha256(rb).hexdigest()} "
                  f"same_as_retained={rb == rec_raw}")
        # article text nodes per fetch
        node_sets = []
        for n, rb, bt in bodies:
            win = qt.content_window(bt, sid)
            ss = segs(bt, sid)
            node_sets.append(ss)
            print(f"fetch{n} article_window={win} text_nodes={len(ss)} "
                  f"node_chars={sum(len(s) for s in ss)}")
        # retained nodes
        rec_text = body_text(retained)
        rec_segs = segs(rec_text, sid)
        print(f"retained text_nodes={len(rec_segs)} node_chars={sum(len(s) for s in rec_segs)}")
        # stability across the three fetches (node multiset)
        base = node_sets[0]
        for idx, (n, rb, bt) in enumerate(bodies[1:], 1):
            same_order = node_sets[idx] == base
            same_set = sorted(node_sets[idx]) == sorted(base)
            only_a = [s for s in base if s not in node_sets[idx]]
            only_b = [s for s in node_sets[idx] if s not in base]
            print(f"fetch1 vs fetch{n}: identical_order={same_order} identical_multiset={same_set} "
                  f"only_in_fetch1={len(only_a)} only_in_fetch{n}={len(only_b)}")
            for s in only_a[:6]:
                print(f"    only_f1: {s[:160]!r}")
            for s in only_b[:6]:
                print(f"    only_f{n}: {s[:160]!r}")
        # retained vs each fetch
        for n, rb, bt in bodies:
            same_order = segs(bt, sid) == rec_segs
            same_set = sorted(segs(bt, sid)) == sorted(rec_segs)
            only_r = [s for s in rec_segs if s not in segs(bt, sid)]
            only_f = [s for s in segs(bt, sid) if s not in rec_segs]
            print(f"retained vs fetch{n}: identical_order={same_order} identical_multiset={same_set} "
                  f"only_in_retained={len(only_r)} only_in_fetch{n}={len(only_f)}")
            for s in only_r[:8]:
                print(f"    only_retained: {s[:200]!r}")
            for s in only_f[:8]:
                print(f"    only_fetch{n}: {s[:200]!r}")
        # where does the full body differ? line-level on the raw bytes
        print("-- full-body line-level differences (fetch1 vs fetch2, retained vs fetch1) --")
        for label, pa, pb in (("fetch1/fetch2", paths[0], paths[1]),
                              ("fetch2/fetch3", paths[1], paths[2]),
                              ("retained/fetch1", retained, paths[0])):
            la = raw_body(pa).decode("utf-8", "replace").splitlines()
            lb = raw_body(pb).decode("utf-8", "replace").splitlines()
            d = list(difflib.unified_diff(la, lb, lineterm="", n=0))
            print(f"  {label}: changed_lines={max(0,(len(d)-2)//2)} hunks={sum(1 for x in d if x.startswith('@@'))}")
            for line in d[:24]:
                print(f"    {line[:220]}")
        report[sid] = {"retained": rec_segs, "fetches": [s for s in node_sets]}
    return report


if __name__ == "__main__":
    main()
