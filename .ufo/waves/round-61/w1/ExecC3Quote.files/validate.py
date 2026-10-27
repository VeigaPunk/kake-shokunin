#!/usr/bin/env python3
"""Validate a Gate-quote candidate against the lane quote rule on the retained body:

  6..25 whitespace units, <=160 chars, printable ASCII, no embedded ASCII double
  quote, occurring exactly once in the page, and lying inside ONE whitespace-
  collapsed text node (HTML) or one raw line (plain-text bodies: YAML, texinfo, C).

  python3 -B validate.py BODY KIND 'span' [...]
"""
from __future__ import annotations

import importlib.util
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
spec = importlib.util.spec_from_file_location("rel", os.path.join(HERE, "relocate.py"))
r = importlib.util.module_from_spec(spec)
spec.loader.exec_module(r)

NODE_RE = re.compile(r">([^<>]+)(?=<)")


def nodes(text: str, kind: str) -> list[str]:
    if kind == "html":
        body = re.sub(r"(?is)<(script|style)\b.*?</\1>", " ", text)
        return [" ".join(n.split()) for n in NODE_RE.findall(body)]
    return [" ".join(line.split()) for line in text.split("\n")]


def check(body: str, kind: str, span: str) -> dict:
    text = r.decode(body)
    streamed = r.stream(text, kind)
    ns = nodes(text, kind)
    hosts = [i for i, n in enumerate(ns) if span in n]
    return {
        "span": span,
        "units": len(span.split()),
        "chars": len(span),
        "page_count": streamed.count(span),
        "node_hits": hosts[:4],
        "node_bounded": bool(hosts),
        "node_text": (ns[hosts[0]][:220] if hosts else None),
        "ascii": all(32 <= ord(c) <= 126 for c in span),
        "has_dquote": '"' in span,
        "ok": (6 <= len(span.split()) <= 25 and len(span) <= 160
               and all(32 <= ord(c) <= 126 for c in span) and '"' not in span
               and streamed.count(span) == 1 and bool(hosts)),
    }


if __name__ == "__main__":
    body, kind = sys.argv[1], sys.argv[2]
    for span in sys.argv[3:]:
        out = check(body, kind, span)
        print(f"ok={out['ok']!s:5} units={out['units']:2} chars={out['chars']:3} "
              f"page={out['page_count']} nodes={out['node_hits']}")
        print(f"   {out['span'][:150]}")
        if not out["node_bounded"]:
            print("   [not inside one node]")
