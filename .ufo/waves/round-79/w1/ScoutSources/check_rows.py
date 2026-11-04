#!/usr/bin/env python3
"""Validate the drafted round-79 registry rows against the registry's 11-column shape.

Checks per row: 11 non-empty cells (used-by may be the em dash), no escaped pipe, id free in
corpus/SOURCES.md, kind/tier/status enums, opened a past/present ISO date, recheck NNd or a
symbolic cadence, the anchor's sha256 and byte count equal the retained raw file's, a rejected
row's teaches cell carries REJECTED: and a flip:, a mined row's teaches cell is not thin (W02 is
about rejected rows; W03 about a mined row with used-by = —), and the census duplicate rule is
simulated: same URL + same scope as an existing row is E04, same URL with a different scope is
W04, and a row whose URL is absent is silent.
"""
import hashlib
import re
import sys
from datetime import date
from pathlib import Path

HERE = Path(__file__).resolve().parent
LANE = next(p for p in HERE.parents if (p / "corpus" / "SOURCES.md").is_file())
REGISTRY = LANE / "corpus" / "SOURCES.md"
TODAY = date(2026, 11, 4)

RAW = {
    "S452": "mdn-x-robots-tag.raw",
    "S453": "rfc9309.raw",
    "S454": "google-robots-meta.raw",
}
KNOWLEDGE = "corpus/knowledge/x-robots-tag-header.md"
KINDS = {"spec", "docs", "paper", "code", "tool", "dataset", "talk", "book", "community", "own-work"}
TIERS = {"A", "B", "C"}
STATUSES = {"queued", "mined", "rejected"}


def url_of(source_cell: str) -> str:
    m = re.search(r"https?://[^\s;|]+", source_cell)
    return m.group(0) if m else ""


def existing_rows(text: str):
    rows = []
    for line in text.splitlines():
        if not re.match(r"^ {0,3}\| S\d{3,} \|", line):
            continue
        cells = [c.strip() for c in line.split("|")[1:-1]]
        if len(cells) != 11:
            continue
        rows.append({"id": cells[0], "url": url_of(cells[1]), "scope": cells[4]})
    return rows


def main() -> int:
    registry = REGISTRY.read_text(encoding="utf-8")
    existing = existing_rows(registry)
    seen_ids = {r["id"] for r in existing}
    failures = 0
    rows_path = Path(sys.argv[1]) if len(sys.argv) > 1 else HERE / "rows-draft.txt"
    rows = [ln for ln in rows_path.read_text(encoding="utf-8").splitlines() if ln.strip()]
    for ln in rows:
        if not (ln.startswith("|") and ln.endswith("|")):
            print("FAIL not pipe-delimited:", ln[:60]); failures += 1; continue
        cells = [c.strip() for c in ln.split("|")[1:-1]]
        if len(cells) != 11:
            print(f"FAIL cell count {len(cells)} != 11:", ln[:60]); failures += 1; continue
        rid, source, kind, tier, scope, anchor, teaches, status, opened, recheck, used_by = cells
        problems = []
        if not re.fullmatch(r"S\d{3,}", rid):
            problems.append(f"id {rid!r}")
        if rid in seen_ids:
            problems.append(f"id {rid} already in registry")
        if kind not in KINDS:
            problems.append(f"kind {kind!r}")
        if tier not in TIERS:
            problems.append(f"tier {tier!r}")
        if status not in STATUSES:
            problems.append(f"status {status!r}")
        if not re.fullmatch(r"\d{4}-\d{2}-\d{2}", opened):
            problems.append(f"opened {opened!r}")
        else:
            y, m, d = (int(x) for x in opened.split("-"))
            if date(y, m, d) > TODAY:
                problems.append(f"opened {opened} is in the future")
        if not (re.fullmatch(r"\d+d", recheck) or re.fullmatch(r"[a-z][a-z-]+", recheck)):
            problems.append(f"recheck {recheck!r}")
        if "\\|" in ln:
            problems.append("escaped pipe in row")
        if status == "rejected":
            if "REJECTED:" not in teaches:
                problems.append("rejected row teaches lacks REJECTED:")
            if "flip:" not in teaches:
                problems.append("rejected row teaches lacks flip:")
        if status == "mined":
            if len(teaches) < 120:
                problems.append(f"thin teaches ({len(teaches)} chars)")
            if KNOWLEDGE not in used_by:
                problems.append("mined row used-by does not name the knowledge entry")
            if used_by.strip("— ") == "":
                problems.append("mined row used-by is empty (W03)")
        raw_name = RAW.get(rid)
        if raw_name is None:
            problems.append("no retained raw file registered for this id")
        else:
            raw = (HERE / raw_name).read_bytes()
            want = hashlib.sha256(raw).hexdigest()
            if want not in anchor:
                problems.append(f"anchor sha256 {want[:12]}… absent")
            if f"{len(raw)} bytes" not in anchor:
                problems.append(f"anchor byte count '{len(raw)} bytes' absent")
            if raw_name not in anchor:
                problems.append(f"anchor does not name {raw_name}")
        url, prior = url_of(source), [r for r in existing if r["url"] == url_of(source)]
        dup = "none"
        if prior:
            same_scope = [r["id"] for r in prior if r["scope"] == scope]
            dup = f"E04 same-scope with {same_scope}" if same_scope else f"W04 across scopes with {[r['id'] for r in prior]}"
        print(f"{rid}: cells=11 kind={kind} tier={tier} status={status} url={url} "
              f"scope_chars={len(scope)} anchor_chars={len(anchor)} teaches_chars={len(teaches)} "
              f"used_by={used_by} duplicate={dup} {'OK' if not problems else 'FAIL ' + '; '.join(problems)}")
        failures += len(problems)
    print(f"rows={len(rows)} failures={failures}")
    return 0 if failures == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
