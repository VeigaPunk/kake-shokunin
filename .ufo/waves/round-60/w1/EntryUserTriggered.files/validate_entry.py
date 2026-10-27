#!/usr/bin/env python3
"""Validate every double-quoted span of the S428 entry against the S428 retained body.

Rules applied (contract C3 / C5, round-59 counter code):
  * a span must be 6..25 units and <= 160 characters;
  * a span must be a substring of ONE whitespace-collapsed text node of the article block
    (`class="devsite-article-body` .. `<devsite-content-footer`);
  * a span must be page-unique: one occurrence in the S428 body, none in S427/S429;
  * ASCII double quotes only (curly quotes are refused).

  python3 -B validate_entry.py <source-dir> <entry.md>
"""
import re
import sys

sys.path.insert(0, __file__.rsplit("/", 1)[0])
from check_spans import SID, body, text_segments, units  # noqa: E402

CURLY = re.compile("[\u201c\u201d\u201e\u201f]")


def main():
    src, entry_path = sys.argv[1].rstrip("/"), sys.argv[2]
    entry = open(entry_path, encoding="utf-8").read()
    if CURLY.search(entry):
        print("FAIL curly double quote in entry")
        return 1
    texts = {s: body(f"{src}/{s}.html") for s in ("S427", "S428", "S429")}
    text = texts[SID]
    segs = text_segments(text)
    spans = re.findall(r'"([^"\n]{1,})"', entry)
    bad = 0
    for span in spans:
        u = units(span)
        ok_units = 6 <= u <= 25
        ok_chars = len(span) <= 160
        in_node = any(span in seg for seg in segs)
        count = text.count(span)
        others = {s: texts[s].count(span) for s in texts if s != SID}
        unique = count == 1 and not any(others.values())
        status = "PASS" if (ok_units and ok_chars and in_node and unique) else "FAIL"
        bad += status == "FAIL"
        print(f"{status} {u:2d}u {len(span):3d}c node={in_node!s:5} count={count} others={others} :: {span}")
    print(f"spans={len(spans)} distinct={len(set(spans))} failed={bad} "
          f"distinct_passing={len({s for s in spans if 6 <= units(s) <= 25 and any(s in g for g in segs)})}")
    print("carries_subject=", any("generally ignore" in s for s in spans))
    return 1 if bad else 0


if __name__ == "__main__":
    sys.exit(main())
