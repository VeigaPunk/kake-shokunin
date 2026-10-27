#!/usr/bin/env python3
"""Byte-stability probe: article-block text nodes vs full body, retained vs 3 fresh fetches.

Uses the C3 counter's own content_window/text_segments so the extracted region is exactly the
region the span check accepts.
"""
import hashlib
import importlib.util
import json
import os
import sys

ROUND = "/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-58"
HERE = "/fast/scratch/hyaku/kake-r58/ProbeBodyStability"
spec = importlib.util.spec_from_file_location("c58qt", os.path.join(ROUND, "c58_quote_truth.py"))
qt = importlib.util.module_from_spec(spec)
spec.loader.exec_module(qt)


def h(s: str) -> str:
    return hashlib.sha256(s.encode("utf-8")).hexdigest()


def load(path):
    with open(path, encoding="utf-8", newline="") as fh:
        return fh.read()


def article(sid, text):
    win = qt.content_window(text, sid)
    if win is None:
        return None, None, None
    segs = qt.text_segments(text, sid)
    joined = "\n".join(s.strip() for s in segs if s.strip())
    return win, len(segs), joined


def variants(sid):
    out = [("retained", os.path.join(ROUND, "sources", f"{sid}.html"))]
    for i in (1, 2, 3):
        out.append((f"f{i}", os.path.join(HERE, f"{sid}.f{i}.html")))
    return out


report = {"full_sha256": {}, "article_sha256": {}, "article_units": {}, "segments": {},
          "window_offsets": {}, "nodes": {}, "diffs": {}}

for sid in ("S423", "S424"):
    keep = {}
    for tag, path in variants(sid):
        text = load(path)
        win, nsegs, joined = article(sid, text)
        report["full_sha256"].setdefault(sid, {})[tag] = {
            "bytes": len(text.encode("utf-8")), "sha256": h(text),
            "sha256_nl_norm": hashlib.sha256(
                text.replace("\r\n", "\n").encode("utf-8")).hexdigest()}
        report["window_offsets"].setdefault(sid, {})[tag] = win
        if joined is None:
            report["article_sha256"].setdefault(sid, {})[tag] = None
            report["segments"].setdefault(sid, {})[tag] = (nsegs, 0, 0)
            continue
        report["article_sha256"].setdefault(sid, {})[tag] = h(joined)
        report["article_units"].setdefault(sid, {})[tag] = qt.units(joined)
        report["segments"].setdefault(sid, {})[tag] = (nsegs, len(joined), len(joined.encode("utf-8")))
        report["nodes"].setdefault(sid, {})[tag] = [s.strip() for s in qt.text_segments(text, sid) if s.strip()]
        keep[tag] = (text, joined)

    # node-level diff vs retained
    base_nodes = report["nodes"][sid]["retained"]
    base_text, base_joined = keep["retained"]
    for tag in ("f1", "f2", "f3"):
        nodes = report["nodes"][sid][tag]
        d = {"nodes_retained": len(base_nodes), "nodes_fetch": len(nodes),
             "node_multiset_equal": sorted(base_nodes) == sorted(nodes),
             "node_sequence_equal": base_nodes == nodes,
             "article_text_equal": base_joined == keep[tag][1]}
        only_b = [n for n in base_nodes if n not in nodes]
        only_f = [n for n in nodes if n not in base_nodes]
        d["only_retained_count"] = len(only_b)
        d["only_fetch_count"] = len(only_f)
        d["only_retained_sample"] = only_b[:5]
        d["only_fetch_sample"] = only_f[:5]
        report["diffs"].setdefault(sid, {})[tag] = d

print(json.dumps(report, ensure_ascii=False, indent=1))
