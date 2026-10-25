#!/usr/bin/env python3
"""Read-only helper for round-56 entry drafting: unit counts and page-unique span checks.

  python3 -B span_tools.py spans S419        # candidate clauses: <=25 units, raw substring, inside the article block,
                                             # page-unique (occurs once in its body, in none of the other two adopted bodies)
  python3 -B span_tools.py check S419 'span' # report units / raw-substring / in-content / count / unique for one span
  python3 -B span_tools.py window S419       # print the article text (HTML tags stripped, entities left as in the raw body)

Unit rule (the counter's `units()`): one unit per CJK character, one per non-CJK whitespace token. The adopted bodies are
the retained round-56 sources (S367, S419, S420). Spans must be raw substrings, so HTML entities (&quot; &lt;) stay as
written in the raw body: a span that crosses one must contain it verbatim.
"""
import re
import sys

SRC = "/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-56/sources"
IDS = ("S367", "S419", "S420")
CJK = re.compile(r"[\u3040-\u30ff\u3400-\u4dbf\u4e00-\u9fff\uf900-\ufaff\uff65-\uff9f\U00020000-\U0002ffff]")


def units(t):
    return len(CJK.findall(t)) + len([w for w in t.split() if not CJK.search(w)])


def body(sid):
    return open(f"{SRC}/{sid}.html", encoding="utf-8", newline="").read()


def window(text):
    lo, hi, h2 = text.find("更新日"), text.find("個別リンクURL"), text.find("<h2")
    return (h2, hi) if min(lo, hi, h2) >= 0 and hi > lo else None


def in_content(text, span):
    w = window(text)
    i = text.find(span)
    while i >= 0:
        if w[0] <= i < w[1]:
            return True
        i = text.find(span, i + 1)
    return False


def report(sid, span):
    t = body(sid)
    others = [body(k) for k in IDS if k != sid]
    return {"units": units(span), "raw_substring": span in t, "in_content": in_content(t, span) if span in t else False,
            "count_in_page": t.count(span), "in_other_adopted_body": any(span in o for o in others)}


def main():
    cmd, sid = sys.argv[1], sys.argv[2]
    t = body(sid)
    if cmd == "window":
        w = window(t)
        print(re.sub(r"<[^>]+>", "", t[w[0]:w[1]]))
    elif cmd == "check":
        print(report(sid, sys.argv[3]))
    elif cmd == "spans":
        w = window(t)
        art = t[w[0]:w[1]]
        art = re.sub(r"<[^>]+>", "\n", art)
        seen = []
        for chunk in re.split(r"[\n。]", art):
            chunk = chunk.strip()
            # clause splits inside a sentence
            for piece in re.split(r"(?<=[、」])", chunk):
                piece = piece.strip()
                if 6 <= units(piece) <= 25 and piece not in seen:
                    seen.append(piece)
        for s in seen:
            r = report(sid, s)
            if r["raw_substring"] and r["in_content"] and r["count_in_page"] == 1 and not r["in_other_adopted_body"]:
                print(f"{r['units']:>3}u  {s}")
    else:
        sys.exit(64)


if __name__ == "__main__":
    main()
