#!/usr/bin/env python3
"""Round-80 scribe quote-truth check.

Re-locates every quoted span this seat's drafts use in the bytes this seat retained this round
(whitespace-collapsed substring match) and re-checks the S453 row's 11-cell shape with the C1
counter's own row_shape. Read-only; writes only quote-receipts.json beside itself.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parents[4]  # kake-shokunin
sys.path.insert(0, str(ROOT / ".ufo/waves/round-80"))
import c80_defect_queue as counter  # noqa: E402

QUOTES = [
    ("q01", "rfc9110.txt", "A recipient that parses a timestamp value in an HTTP field MUST accept all three HTTP-date formats."),
    ("q02", "rfc9110.txt", "MUST generate those timestamps in the IMF-fixdate format"),
    ("q03", "rfc9110.txt", "HTTP-date is case sensitive."),
    ("q04", "rfc9110.txt", "values in the asctime format are assumed to be in UTC"),
    ("q05", "rfc9110.txt", "Fields that expect to contain a comma within a member, such as within an HTTP-date or URI-reference element"),
    ("q06", "rfc9110.txt", "ought to be defined with delimiters around that element"),
    ("q07", "rfc9110.txt", "a fixed-length and single-zone subset of the date and time specification used by the Internet Message Format"),
    ("q08", "rfc9110.txt", 'IMF-fixdate = day-name "," SP date1 SP time-of-day SP GMT'),
    ("q09", "rfc9110.txt", 'rfc850-date = day-name-l "," SP date2 SP time-of-day SP GMT'),
    ("q10", "rfc9110.txt", "asctime-date = day-name SP date3 SP time-of-day SP year"),
    ("q11", "rfc9110.txt", "obs-date = rfc850-date / asctime-date"),
    ("q12", "rfc9110.txt", "Sun, 06 Nov 1994 08:49:37 GMT"),
    ("q13", "rfc9110.txt", "Sunday, 06-Nov-94 08:49:37 GMT"),
    ("q14", "rfc9110.txt", "Sun Nov  6 08:49:37 1994"),
    ("q15", "rfc9110.txt", "date3 = month SP ( 2DIGIT / ( SP 1DIGIT ))"),
    ("q16", "mdn-x-robots-tag.txt", "X-Robots-Tag: unavailable_after: Wed, 03 Dec 2025 13:09:53 GMT"),
    ("q17", "mdn-x-robots-tag.txt", "Not part of any current specification."),
    ("q18", "mdn-x-robots-tag.txt", "unavailable_after: <date/time>"),
    ("q19", "S452-mdn-x-robots-tag.txt", "A date must be specified in a format such as RFC 822, RFC 850, or ISO 8601."),
]

FILE_PATHS = {
    "rfc9110.txt": HERE / "rfc9110.txt",
    "mdn-x-robots-tag.txt": HERE / "mdn-x-robots-tag.txt",
    "S452-mdn-x-robots-tag.txt": HERE.parent / "ScoutSources/S452-mdn-x-robots-tag.txt",
}


def collapse(text: str) -> tuple[str, list[int]]:
    chars: list[str] = []
    origins: list[int] = []
    prev_space = False
    for index, ch in enumerate(text):
        if ch.isspace():
            if not prev_space and chars:
                chars.append(" ")
                origins.append(index)
            prev_space = True
        else:
            chars.append(ch)
            origins.append(index)
            prev_space = False
    return "".join(chars).rstrip(), origins


def locate(text: str, quote: str) -> dict:
    collapsed, origins = collapse(text)
    needle = re.sub(r"\s+", " ", quote).strip()
    at = collapsed.find(needle)
    if at < 0:
        return {"found": False, "line": None}
    origin = origins[at]
    line = text.count("\n", 0, origin) + 1
    return {"found": True, "line": line}


def row_check() -> dict:
    raw = (HERE / "row-S453.md").read_text(encoding="utf-8")
    line = [ln for ln in raw.splitlines() if ln.startswith("| S453 |")]
    if len(line) != 1:
        return {"rows": len(line), "cells": 0, "shape": "no single S453 line"}
    cells = [c.strip() for c in line[0].strip().strip("|").split("|")]
    return {
        "rows": 1,
        "cells": len(cells),
        "shape": counter.row_shape(cells),
        "source_cites_rfc9110": "rfc 9110" in cells[1].lower() or "rfc9110" in cells[1].lower(),
        "source_cites_9309": "9309" in cells[1],
        "used_by": cells[10],
        "used_by_file_exists": (ROOT / cells[10]).is_file(),
        "draft_file": str(HERE / "knowledge-http-date-grammar.md"),
        "draft_mentions_S453": "S453" in (HERE / "knowledge-http-date-grammar.md").read_text(encoding="utf-8", errors="replace"),
    }


def main() -> int:
    texts = {name: path.read_text(encoding="utf-8", errors="replace") for name, path in FILE_PATHS.items()}
    receipts = []
    found = 0
    for qid, name, quote in QUOTES:
        hit = locate(texts[name], quote)
        found += int(hit["found"])
        receipts.append({"id": qid, "file": name, "words": len(quote.split()), "quote": quote, **hit})
    row = row_check()
    out = {
        "generated_at_utc": "2026-11-04",
        "files": {name: {"lines": texts[name].count("\n") + 1} for name in texts},
        "quotes": receipts,
        "row_S453": row,
    }
    (HERE / "quote-receipts.json").write_text(json.dumps(out, indent=1, ensure_ascii=False) + "\n", encoding="utf-8")
    missing = [r["id"] for r in receipts if not r["found"]]
    print(f"quotes={len(QUOTES)} found={found} missing={len(missing)}" + (f" missing_ids={','.join(missing)}" if missing else ""))
    print(f"row cells={row['cells']} shape={row['shape']!r} used_by={row['used_by']} "
          f"exists_at_carrier={row['used_by_file_exists']} draft_cites_S453={row['draft_mentions_S453']}")
    return 0 if not missing else 1


if __name__ == "__main__":
    raise SystemExit(main())
