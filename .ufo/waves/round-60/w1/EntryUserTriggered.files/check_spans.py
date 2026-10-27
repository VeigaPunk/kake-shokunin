#!/usr/bin/env python3
"""Span checker for the S428 entry (round 60, EntryUserTriggered).

Replicates the C3 counter's text-node code verbatim (round-59 c59_quote_truth.py:
`body()` whitespace-collapses the raw body, `text_segments()` returns the text nodes of
the article block, `in_content()` is the substring test) so a span this script accepts is
a span the C5 substring / block / uniqueness rule accepts.

  python3 -B check_spans.py <source-dir> '<span>' ['<span>' ...]
  python3 -B check_spans.py <source-dir> --list      # article-block text nodes with unit counts
"""
import re
import sys

SID = "S428"
ARTICLE_START = 'class="devsite-article-body'
ARTICLE_END = "<devsite-content-footer"
UNIT_CEILING = 25
CHAR_CEILING = 160
CJK_RE = re.compile(r"[\u3000-\u303f\u3040-\u30ff\u3400-\u4dbf\u4e00-\u9fff\uff00-\uffef]")


def body(path):
    with open(path, encoding="utf-8", newline="") as fh:
        return re.sub(r"\s+", " ", fh.read())


def content_window(text):
    lo = text.find(ARTICLE_START)
    if lo < 0:
        return None
    hi = text.find(ARTICLE_END, lo + 1)
    return (lo, hi) if hi > lo else None


def text_segments(text):
    win = content_window(text)
    if win is None:
        return []
    chunk = re.sub(r"(?is)<(style|script)\b.*?</\1>", "<>", text[win[0]:win[1]])
    chunk = re.sub(r"(?is)<(aside|nav|devsite-feedback|devsite-thumb-rating)\b.*?</\1>", "<>", chunk)
    return re.findall(r">([^<>]+)(?=<)", chunk)


def units(text):
    return len(CJK_RE.findall(text)) + len([t for t in text.split() if not CJK_RE.search(t)])


def main():
    src = sys.argv[1].rstrip("/")
    texts = {s: body(f"{src}/{s}.html") for s in ("S427", "S428", "S429")}
    text = texts[SID]
    if sys.argv[2] == "--list":
        for seg in text_segments(text):
            seg = seg.strip()
            if seg:
                print(f"{units(seg):3d}u {len(seg):3d}c {seg}")
        return
    for span in sys.argv[2:]:
        segs = [seg for seg in text_segments(text) if span in seg]
        count = text.count(span)
        others = {s: texts[s].count(span) for s in texts if s != SID}
        print(f"units={units(span):2d} chars={len(span):3d} in_one_text_node={bool(segs)} "
              f"count_in_S428={count} other_bodies={others} "
              f"unique={count == 1 and not any(others.values())} "
              f"under_ceilings={units(span) <= UNIT_CEILING and len(span) <= CHAR_CEILING} :: {span!r}")


if __name__ == "__main__":
    main()
