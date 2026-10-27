#!/usr/bin/env python3
"""Read-only helper for round-60 entry drafting (Google pages S427, S428, S429): unit counts and page-unique span checks.

Adapted from `.ufo/waves/round-59/span_tools.py` (ExecSpans, round-60 w1). It carries the *same* article-block and
text-node code the round-60 C5 quote-truth rule uses (ported from `c59_quote_truth.py` version 2): bodies are
whitespace-collapsed exactly as the counter collapses them, the article window runs
`class="devsite-article-body` .. `<devsite-content-footer`, and `<style>/<script>/<aside>/<nav>/<devsite-feedback>/
<devsite-thumb-rating>` subtrees are blanked before text nodes are read. So a span this helper accepts is a span the
counter's substring / block / uniqueness test accepts. Self-contained: no import of the still-unbuilt
`c60_quote_truth.py`, so it runs whatever state the wave is in. Verified on the three retained bodies: all three —
S429 (`developers.google.com/search/...`) included — hold both markers exactly once.

  python3 -B spans.py nodes S427             # collapsed text nodes of the article block, one per line, with unit/unique
  python3 -B spans.py check S427 'span'      # units, chars, node-substring?, count in body (+other bodies), unique?
  python3 -B spans.py window S427 word       # every article-block text node containing the literal word
"""
import hashlib
import json
import os
import re
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SOURCES = os.path.normpath(os.path.join(HERE, "..", "..", "sources"))

IDS = ("S427", "S428", "S429")
ARTICLE_START = {sid: 'class="devsite-article-body' for sid in IDS}
ARTICLE_END = {sid: "<devsite-content-footer" for sid in IDS}
UNIT_CEILING = 25
CHAR_CEILING = 160
CJK_RE = re.compile(r"[\u3040-\u30ff\u3400-\u4dbf\u4e00-\u9fff\uf900-\ufaff\uff65-\uff9f\U00020000-\U0002ffff]")

# Frozen digests from sources/receipts.json (fetched 2026-10-27T04:03Z); checked when the file is read.
BODY_SHA256 = {
    "S427": "d70ce6f5aa51ff2f7e6192191330976bd6279e3f2e91d30ef988d3d805382175",
    "S428": "0f296b8636d5fb9d44c66fc1453a5610fdf738c80c9baef44c233e0a1872d3b2",
    "S429": "423d99c5bf7fec4298d00cdd46f01a495c9ad463fa704f7850a100e43e2a9edd",
}
BODY_BYTES = {"S427": 74477, "S428": 76197, "S429": 178797}

_BODIES: dict = {}


def raw_body(sid: str) -> str:
    if sid not in _BODIES:
        path = os.path.join(SOURCES, f"{sid}.html")
        with open(path, "rb") as fh:
            raw = fh.read()
        digest = hashlib.sha256(raw).hexdigest()
        if digest != BODY_SHA256[sid] or len(raw) != BODY_BYTES[sid]:
            sys.exit(f"error: {path} sha256/bytes drifted from receipts ({digest}, {len(raw)})")
        _BODIES[sid] = raw.decode("utf-8")
    return _BODIES[sid]


def body(sid: str) -> str:
    """Whitespace-collapsed exactly as the counter collapses the body."""
    return re.sub(r"\s+", " ", raw_body(sid))


def units(text: str) -> int:
    """One unit per CJK character, one per non-CJK whitespace token."""
    return len(CJK_RE.findall(text)) + len([t for t in text.split() if not CJK_RE.search(t)])


def content_window(text: str, sid: str) -> tuple[int, int] | None:
    """The article block: from the page's identity/byline container to the end marker."""
    lo = text.find(ARTICLE_START[sid])
    if lo < 0:
        return None
    hi = text.find(ARTICLE_END[sid], lo + 1)
    return (lo, hi) if hi > lo else None


def text_segments(text: str, sid: str) -> list[str]:
    """Text nodes of the article block (counter version-2: page chrome blanked before nodes are read)."""
    win = content_window(text, sid)
    if win is None:
        return []
    chunk = re.sub(r"(?is)<(style|script)\b.*?</\1>", "<>", text[win[0]:win[1]])
    chunk = re.sub(r"(?is)<(aside|nav|devsite-feedback|devsite-thumb-rating)\b.*?</\1>", "<>", chunk)
    return re.findall(r">([^<>]+)(?=<)", chunk)


def in_content(text: str, span: str, sid: str) -> bool:
    """True when `span` is a raw substring of one text node of the article block."""
    return any(span in seg for seg in text_segments(text, sid))


def check(sid: str, span: str) -> dict:
    texts = {s: body(s) for s in IDS}
    segs = [s.strip() for s in text_segments(texts[sid], sid)]
    count = texts[sid].count(span)
    in_window = content_window(texts[sid], sid) is not None and span in \
        texts[sid][content_window(texts[sid], sid)[0]:content_window(texts[sid], sid)[1]]
    return {
        "units": units(span),
        "chars": len(span),
        "in_text_node": in_content(texts[sid], span, sid),
        "in_article_window": in_window,
        "count_in_body": count,
        "count_elsewhere": {o: texts[o].count(span) for o in IDS if o != sid},
        "unique": count == 1,
        "node_uniques": sum(1 for s in segs if span in s),
        "within_ceilings": units(span) <= UNIT_CEILING and len(span) <= CHAR_CEILING,
        "no_curly_quotes": not re.search(r"[“”„‟'‘’]", span),
    }


def nodes(sid: str) -> None:
    text = body(sid)
    for seg in text_segments(text, sid):
        seg = seg.strip()
        if seg:
            r = check(sid, seg)
            print(f"{r['units']:3d}u {r['chars']:3d}c unique={r['unique']!s:5} node={r['in_text_node']!s:5} {seg}")


def window(sid: str, word: str) -> None:
    text = body(sid)
    segs = [s.strip() for s in text_segments(text, sid) if s.strip()]
    hits = [s for s in segs if word in s]
    if hits:
        for i, s in enumerate(hits, 1):
            print(f"--- node {i}/{len(hits)} containing {word!r} ({units(s)}u {len(s)}c) ---")
            print(s)
    else:
        print(f"no article-block text node contains {word!r}")
        n = text.count(word)
        print(f"occurrences in collapsed body: {n}")
        start = 0
        for k in range(n):
            i = text.find(word, start)
            print(f"  [{k}] ...{text[max(0, i-60):i+len(word)+60]}...")
            start = i + 1


def main() -> None:
    if len(sys.argv) < 3 or sys.argv[1] not in ("nodes", "check", "window") or sys.argv[2] not in IDS:
        sys.exit(__doc__)
    cmd, sid = sys.argv[1], sys.argv[2]
    if cmd == "nodes":
        nodes(sid)
    elif cmd == "window":
        if len(sys.argv) < 4:
            sys.exit("usage: spans.py window <id> <word>")
        window(sid, sys.argv[3])
    else:
        if len(sys.argv) < 4:
            sys.exit("usage: spans.py check <id> <span>")
        print(json.dumps(check(sid, sys.argv[3]), indent=2, sort_keys=True))


if __name__ == "__main__":
    main()
