#!/usr/bin/env python3
"""Self-check the round-100 knowledge entry draft.

Checks, all against the draft file itself:

  1. the provenance trio: `source:` names S484, S485, S486 and S487;
     `verified-at:` is 2026-11-06; `recheck:` carries an ISO date or an NNd
     form;
  2. the entry carries a `## Contract v2 (round 100)` section, and that
     section names each of the seven escape classes e1-e7, the lane
     convention LC8, the still-open findings F4-F9 and F11, and the four
     closed findings F1, F2, F3 and F10;
  3. every quote row in the quote table names a source row, a body and a
     line, and every quote is at most 25 words;
  4. the citation counts: how many quote rows each source row carries;
  5. no seat/wave/drafting meta-text: no `.ufo/waves/round-N/w1/` path, no
     seat name, and none of the metatext-lint gate phrases.

Exit 0 when every check passes.
"""
import pathlib
import re
import sys

ENTRY = pathlib.Path(
    "/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-100/w1/ScribeEntry/freshening-304.md"
)

TABLE_ROW = re.compile(r"^\|\s*(Q\d+)\s*\|\s*(\S+)\s*\|\s*((?:S\d+)(?:,\s*S\d+)*)\s*\|\s*(\d+)\s*\|\s*(\d+)\s*\|\s*(.*?)\s*\|\s*$")

SEAT_NAMES = re.compile(
    r"\b(?:Scout|Exec|Review|Critic|Sentinel|Mut|Scribe|Connector|Labrat"
    r"|Kumitate|Kengaku|Revenger)[A-Z][A-Za-z0-9]*\b"
)
SEAT_PATH = re.compile(r"\.ufo/waves/round-\d+/w1/")
GATE_PHRASES = [
    r"\bDrafted by\b",
    r"\bword-count receipt\b",
    r"\bquotes-verified\.txt\b",
    r"\bbody is \d+ words\b",
    r"\bthe L1 integrates\b",
]


def main():
    text = ENTRY.read_text(encoding="utf-8")
    lines = text.split("\n")
    failures = []

    # 1. provenance trio
    trio = {}
    for name in ("source", "verified-at", "recheck"):
        for line in lines:
            if line.startswith(name + ":"):
                trio[name] = line.split(":", 1)[1].strip()
                break
    for name in ("source", "verified-at", "recheck"):
        if name not in trio:
            failures.append("missing front-matter line: %s:" % name)
    src = trio.get("source", "")
    for sid in ("S484", "S485", "S486", "S487"):
        if sid not in src:
            failures.append("source: does not name %s" % sid)
    if trio.get("verified-at") != "2026-11-06":
        failures.append("verified-at: is %r, expected 2026-11-06" % trio.get("verified-at"))
    if not re.search(r"\b\d{4}-\d{2}-\d{2}\b|\b\d+[dD]\b", trio.get("recheck", "")):
        failures.append("recheck: carries neither an ISO date nor an NNd form: %r" % trio.get("recheck"))

    # 2. the v2 section
    if "## Contract v2 (round 100)" not in lines:
        failures.append("missing section heading: ## Contract v2 (round 100)")
    try:
        start = lines.index("## Contract v2 (round 100)")
    except ValueError:
        start = 0
    try:
        end = next(i for i in range(start + 1, len(lines)) if lines[i].startswith("## "))
    except StopIteration:
        end = len(lines)
    section = "\n".join(lines[start:end])
    for e in range(1, 8):
        if not re.search(r"\be%d\b" % e, section):
            failures.append("Contract v2 section does not name escape class e%d" % e)
    for marker in ("LC8", "F1", "F2", "F3", "F10", "F4", "F5", "F6", "F7", "F8", "F9", "F11"):
        if marker not in section:
            failures.append("Contract v2 section does not name %s" % marker)

    # 3./4. quote table
    rows = []
    for line in lines:
        m = TABLE_ROW.match(line)
        if m:
            rows.append((m.group(1), m.group(2), m.group(3), int(m.group(4)), int(m.group(5)), m.group(6)))
    if not rows:
        failures.append("quote table has no rows")
    per_row = {}
    for qid, body, rows_attr, line, words, quote in rows:
        if not body:
            failures.append("%s: no body" % qid)
        if not rows_attr:
            failures.append("%s: no source row" % qid)
        if line <= 0:
            failures.append("%s: no line" % qid)
        if words > 25:
            failures.append("%s: %d words" % (qid, words))
        if len(" ".join(quote.split()).split(" ")) != words:
            failures.append("%s: declared word count %d != actual" % (qid, words))
        for sid in [s.strip() for s in rows_attr.split(",")]:
            per_row[sid] = per_row.get(sid, 0) + 1

    # 5. meta-text
    for no, line in enumerate(lines, start=1):
        if SEAT_PATH.search(line):
            failures.append("line %d: seat-tree path: %s" % (no, line.strip()[:90]))
        m = SEAT_NAMES.search(line)
        if m:
            failures.append("line %d: seat name %s" % (no, m.group(0)))
        for pat in GATE_PHRASES:
            if re.search(pat, line, re.IGNORECASE):
                failures.append("line %d: gate phrase %s" % (no, pat))

    print("entry=%s" % ENTRY)
    print("front_matter source=%s" % src[:60])
    print("front_matter verified_at=%s recheck=%s" % (trio.get("verified-at"), trio.get("recheck")))
    print("v2_section_lines=%d" % (end - start))
    print("quote_rows=%d" % len(rows))
    for sid in sorted(per_row):
        print("citations %s=%d" % (sid, per_row[sid]))
    if failures:
        for f in failures:
            print("FAIL %s" % f)
        print("failures=%d" % len(failures))
        return 1
    print("failures=0")
    return 0


if __name__ == "__main__":
    sys.exit(main())
