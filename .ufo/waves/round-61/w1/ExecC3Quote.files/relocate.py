#!/usr/bin/env python3
"""C3 quote re-location helper (seat ExecC3Quote, round 61).

Read-only. For one retained fresh body and a list of probes it reports where each
probe's material sits now: exact hit in the whitespace-collapsed text stream, a
relocated near-hit (token-window similarity), or absent. Line probes report the
lines an exact literal occupies (code and texinfo bodies, where the row anchor is
a line range).

Text stream: HTML -> tags and <script>/<style> bodies removed, entities left as
written, whitespace collapsed to single spaces (the lane's text-node convention,
scripts/source_recheck.py and round-58 span_tools.py). Plain text -> whitespace
collapsed.

  python3 -B relocate.py --body PATH [--kind html|text] --probe LABEL 'text' [...]
  python3 -B relocate.py --body PATH --line LABEL 'literal' [...]
  ... append --json for the machine record.

Exit 0 when the file was read (hits or not); 2 when the body is missing.
"""
from __future__ import annotations

import argparse
import difflib
import json
import re
import sys

TAG_RE = re.compile(r"(?is)<(script|style)\b.*?</\1>")
HEAD_RE = re.compile(r"(?is)<h([1-6])\b[^>]*>(.*?)</h\1>")
ANYCLEAN_RE = re.compile(r"(?s)<>|<[^>]*>")


def decode(path: str) -> str:
    with open(path, "rb") as fh:
        raw = fh.read()
    return raw.decode("utf-8", errors="replace")


def stream(text: str, kind: str) -> str:
    """Whitespace-collapsed text stream. Heading text is kept and delimited by
    \x01..\x02 so heading offsets live in the same coordinate space as probe
    offsets (raw-document offsets of headings would not compare)."""
    if kind == "html":
        text = TAG_RE.sub(" ", text)
        text = HEAD_RE.sub(lambda m: "\x01 " + ANYCLEAN_RE.sub(" ", m.group(2)) + " \x02 ", text)
        text = ANYCLEAN_RE.sub(" ", text)
    return " ".join(text.split())


def stream_headings(streamed: str) -> list[tuple[int, str]]:
    out = []
    for m in re.finditer(r"\x01 ([^\x02]*?)\s*\x02", streamed):
        out.append((m.start(), m.group(1).strip()))
    return out


def headings(text: str) -> list[tuple[int, str]]:
    """Raw-document heading offsets (diagnostic only; probe offsets use stream_headings)."""
    out = []
    for m in HEAD_RE.finditer(text):
        label = " ".join(ANYCLEAN_RE.sub(" ", m.group(2)).split())
        if label:
            out.append((m.start(), label))
    return out


def enclosing_heading(heads: list[tuple[int, str]], offset: int) -> str | None:
    last = None
    for pos, label in heads:
        if pos <= offset:
            last = label
        else:
            break
    return last


def tokens_with_offsets(streamed: str) -> tuple[list[str], list[int]]:
    toks, offs = [], []
    for m in re.finditer(r"\S+", streamed):
        toks.append(m.group(0))
        offs.append(m.start())
    return toks, offs


def fuzzy(streamed: str, probe: str, heads, kind: str) -> dict | None:
    """Best token-window match for a missed probe: windows are seeded on the
    probe's longest token so a 2 MiB body stays cheap."""
    ptoks = probe.split()
    if not ptoks:
        return None
    toks, offs = tokens_with_offsets(streamed)
    seed = max(ptoks, key=len).lower()
    best = None
    for i, tok in enumerate(toks):
        if tok.lower() != seed:
            continue
        lo = max(0, i - (4 if len(ptoks) < 6 else 8))
        span = min(len(toks), i + len(ptoks) + 8)
        for start in range(lo, i + 1):
            win = toks[start:span][: max(1, len(ptoks))]
            if not win:
                continue
            ratio = difflib.SequenceMatcher(None, [t.lower() for t in win],
                                            [t.lower() for t in ptoks]).ratio()
            if best is None or ratio > best["ratio"]:
                best = {"ratio": round(ratio, 3), "offset": offs[start],
                        "window": " ".join(toks[start:start + len(win)])[:200],
                        "heading": enclosing_heading(heads, offs[start])}
    return best


def run(body: str, kind: str, providers: list[tuple[str, str]]) -> dict:
    text = decode(body)
    streamed = stream(text, kind)
    heads = stream_headings(streamed)
    result = {"body": body, "kind": kind, "bytes": len(text.encode("utf-8", "replace")),
              "streamBytes": len(streamed), "probes": [], "lines": []}
    for label, probe in providers:
        needle = " ".join(probe.split())
        count = streamed.count(needle)
        hit = {"label": label, "probe": needle, "units": len(needle.split()),
               "chars": len(needle), "count": count}
        if count:
            off = streamed.find(needle)
            hit.update({"verdict": "found", "offset": off,
                        "heading": enclosing_heading(heads, off)})
        else:
            near = fuzzy(streamed, needle, heads, kind)
            hit["verdict"] = "moved" if near and near["ratio"] >= 0.62 else "absent"
            if near:
                hit["nearest"] = near
        result["probes"].append(hit)
    return result


def line_probe(body: str, label: str, literal: str) -> dict:
    lines = decode(body).split("\n")
    hits = [i + 1 for i, line in enumerate(lines) if literal in line]
    first = hits[0] if hits else None
    return {"label": label, "literal": literal, "count": len(hits),
            "lines": hits[:12], "verdict": "found" if hits else "absent",
            "first": first, "totalLines": len(lines)}


def main() -> int:
    ap = argparse.ArgumentParser(add_help=True)
    ap.add_argument("--body", required=True)
    ap.add_argument("--kind", default="html", choices=("html", "text"))
    ap.add_argument("--probe", nargs=2, action="append", default=[], metavar=("LABEL", "TEXT"))
    ap.add_argument("--line", nargs=2, action="append", default=[], metavar=("LABEL", "LITERAL"))
    ap.add_argument("--json", action="store_true")
    args = ap.parse_args()
    try:
        out = run(args.body, args.kind, [tuple(p) for p in args.probe])
        out["lines"] = [line_probe(args.body, l, s) for l, s in args.line]
    except FileNotFoundError:
        if args.json:
            print(json.dumps({"body": args.body, "verdict": "missing"}))
        else:
            print(f"MISSING {args.body}")
        return 2
    if args.json:
        print(json.dumps(out, ensure_ascii=False, indent=1))
    else:
        print(f"# {out['body']} bytes={out['bytes']} stream={out['streamBytes']}")
        for h in out["probes"]:
            near = h.get("nearest")
            extra = f" near={near['ratio']} @{near['offset']} h={near['heading']!r}" if near else ""
            print(f"{h['verdict']:7} {h['label']:22} n={h['count']:<3} {h['units']:2}u {h['chars']:3}c "
                  f"{h.get('heading')!r}{extra}")
        for l in out["lines"]:
            print(f"{l['verdict']:7} {l['label']:22} lines={l['lines']} of {l['totalLines']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
