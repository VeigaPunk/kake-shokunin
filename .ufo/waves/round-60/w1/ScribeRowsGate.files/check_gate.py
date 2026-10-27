#!/usr/bin/env python3
"""Mechanical pre-check of the three round-60 Gate lines against the frozen C5 rules.

Reads .ufo/waves/round-60/w1/ScribeRowsGate.files/{rows.md,gate.md} and the retained bodies, and
re-uses span60.py (which re-uses the round-59 counter's own text-node and unit code). Read-only.

  python3 -B check_gate.py
"""
import importlib.util
import os
import re

HERE = os.path.dirname(os.path.abspath(__file__))
spec = importlib.util.spec_from_file_location("span60", os.path.join(HERE, "span60.py"))
sp = importlib.util.module_from_spec(spec)
spec.loader.exec_module(sp)

IDS = ("S427", "S428", "S429")
TOPIC = {"S427": "automatic crawls", "S428": "generally ignore", "S429": "cannot enforce"}
RECEIPT = {
    "S427": ("d70ce6f5aa51ff2f7e6192191330976bd6279e3f2e91d30ef988d3d805382175", 74477),
    "S428": ("0f296b8636d5fb9d44c66fc1453a5610fdf738c80c9baef44c233e0a1872d3b2", 76197),
    "S429": ("423d99c5bf7fec4298d00cdd46f01a495c9ad463fa704f7850a100e43e2a9edd", 178797),
}
URL = {
    "S427": "https://developers.google.com/crawling/docs/crawlers-fetchers/overview-google-crawlers",
    "S428": "https://developers.google.com/crawling/docs/crawlers-fetchers/google-user-triggered-fetchers",
    "S429": "https://developers.google.com/search/docs/crawling-indexing/robots/intro",
}


def rows():
    out = {}
    for line in open(os.path.join(HERE, "rows.md"), encoding="utf-8"):
        cells = [c.strip() for c in line.split("|")]
        if len(cells) == 13 and cells[1].startswith("S4"):
            out[cells[1]] = cells
    return out


def gate_line(sid):
    out, inside = None, False
    for line in open(os.path.join(HERE, "gate.md"), encoding="utf-8"):
        if line.startswith("## "):
            inside = line.strip() == "## Gate"
            continue
        if inside and line.startswith(f"- {sid} "):
            out = line.rstrip("\n")
    return out


def heading_ok(sid, anchor):
    """L1 anchor rule: the anchor names an h1/h2/h3 of the article block (nearest preceding the Gate quote)."""
    text = sp.body(sid)
    win = sp.qt.content_window(text, sid)
    chunk = text[win[0]:win[1]]
    heads = [re.sub(r"\s+", " ", re.sub(r"<[^>]*>", "", h)).strip()
             for h in re.findall(r"(?is)<h[123]\b[^>]*>(.*?)</h[123]>", chunk)]
    return anchor in heads


def section_ok(sid, anchor, span):
    """L1 positional rule: the nearest article-block heading before the span is the row's anchor heading."""
    text = sp.body(sid)
    pos = text.find(span)
    if pos < 0:
        return False
    win = sp.qt.content_window(text, sid)
    heads = [(m.start(), re.sub(r"\s+", " ", re.sub(r"<[^>]*>", "", m.group(2))).strip())
             for m in re.finditer(r"(?is)<h([123])\b[^>]*>(.*?)</h\1>", text[win[0]:win[1]])]
    heads = [(win[0] + off, name) for off, name in heads]
    prev = [h for h in heads if h[0] < pos]
    return bool(prev) and prev[-1][1] == anchor


def main():
    r = rows()
    fail = 0
    for sid in IDS:
        problems = []
        line = gate_line(sid)
        cells = r.get(sid)
        if line is None or cells is None:
            print(f"{sid}: FAIL missing gate line or row")
            fail += 1
            continue
        if URL[sid] not in line:
            problems.append("no row URL")
        if "2026-10-27" not in line:
            problems.append("no access date")
        if cells[6] not in line:
            problems.append("anchor cell not carried verbatim")
        am = re.match(r"^§\s*(.*?)\s*\(Last updated \d{4}-\d{2}-\d{2} UTC\)\s*$", cells[6])
        if not am:
            problems.append("anchor cell is not the contract form")
        elif not heading_ok(sid, am.group(1)):
            problems.append(f"anchor {am.group(1)!r} is not an h1/h2/h3 of the article block")
        digest, nbytes = RECEIPT[sid]
        if digest not in line or f"{nbytes} bytes" not in line:
            problems.append("sha256/byte count not carried")
        quoted = re.findall(r'"([^"]+)"', line)
        spans = [q for q in quoted if sp.qt.units(q) >= 6]
        if not spans:
            problems.append("no span of 6+ units")
        if not any(TOPIC[sid] in q for q in spans):
            problems.append(f"no span carries {TOPIC[sid]!r}")
        for q in quoted:
            c = sp.check(sid, q)
            if not c["in_text_node"] or not c["page_unique"]:
                problems.append(f"span not page-unique or outside a text node: {q[:40]!r}")
            if not (6 <= c["units"] <= 25) or c["chars"] > 160:
                problems.append(f"span size {c['units']}u/{c['chars']}c: {q[:40]!r}")
            if f"{c['units']} units" not in line:
                problems.append(f"unit count {c['units']} not stated for {q[:40]!r}")
        am2 = re.match(r"^§\s*(.*?)\s*\(Last updated \d{4}-\d{2}-\d{2} UTC\)\s*$", cells[6])
        if am2:
            for q in spans:
                if not section_ok(sid, am2.group(1), q):
                    problems.append(f"span {q[:40]!r} is not in the anchor heading's section")
        if any(ord(ch) in (0x201C, 0x201D) for ch in line):
            problems.append("curly double quote")
        print(f"{sid}: {'PASS' if not problems else 'FAIL ' + '; '.join(problems)} ({len(spans)} spans)")
        fail += bool(problems)
    print(f"gate_lines: {len(IDS) - fail}/{len(IDS)} clean")
    return 1 if fail else 0


if __name__ == "__main__":
    raise SystemExit(main())
