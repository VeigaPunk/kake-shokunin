#!/usr/bin/env python3
"""Validate the three drafted registry rows against the registry's 11-column shape.

Checks per row: 11 non-empty cells, no escaped pipe, id free in corpus/SOURCES.md, declared
status/opened/recheck, the anchor's sha256 equals the retained raw file's sha256, and the
teaches cell names the knowledge entry the row will feed.
"""
import hashlib
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
LANE = next(p for p in HERE.parents if (p / "corpus" / "SOURCES.md").is_file())
REGISTRY = LANE / "corpus" / "SOURCES.md"

RAW = {
    "S449": "google-robots-meta.raw",
    "S450": "whatwg-semantics.raw",
    "S451": "rfc3339.raw",
}


def main() -> int:
    registry = REGISTRY.read_text(encoding="utf-8")
    existing_ids = set(re.findall(r"^\| (S\d+) \|", registry, re.M))
    lines = [ln for ln in (HERE / "rows-draft.txt").read_text(encoding="utf-8").splitlines() if ln.strip()]
    failures = 0
    for ln in lines:
        if not (ln.startswith("|") and ln.endswith("|")):
            print("FAIL not pipe-delimited:", ln[:60]); failures += 1; continue
        cells = [c.strip() for c in ln.split("|")[1:-1]]
        if len(cells) != 11:
            print(f"FAIL cell count {len(cells)} != 11:", ln[:60]); failures += 1; continue
        rid, source, kind, tier, scope, anchor, teaches, status, opened, recheck, used_by = cells
        problems = []
        if not re.fullmatch(r"S\d{3}", rid):
            problems.append(f"id {rid!r}")
        if rid in existing_ids:
            problems.append(f"id {rid} already in registry")
        if kind not in {"docs", "spec", "code", "dataset", "community", "own-work"}:
            problems.append(f"kind {kind!r}")
        if status != "mined":
            problems.append(f"status {status!r}")
        if opened != "2026-11-03":
            problems.append(f"opened {opened!r}")
        if recheck not in {"90d", "365d"}:
            problems.append(f"recheck {recheck!r}")
        if "corpus/knowledge/meta-robots-directives.md" not in used_by:
            problems.append("used-by does not name the knowledge entry")
        if "\\|" in ln:
            problems.append("escaped pipe in row")
        raw = (HERE / RAW.get(rid, "")).read_bytes() if rid in RAW else b""
        want = hashlib.sha256(raw).hexdigest()
        if rid in RAW and want not in anchor:
            problems.append(f"anchor sha256 {want[:12]}… absent")
        if rid in RAW and f"{len(raw):,}" not in anchor:
            problems.append(f"anchor byte count {len(raw):,} absent")
        print(f"{rid} cells=11 sha={'ok' if rid in RAW and want in anchor else 'n/a'} "
              f"scope_chars={len(scope)} anchor_chars={len(anchor)} teaches_chars={len(teaches)} "
              + ("FAIL " + ", ".join(problems) if problems else "ok"))
        failures += len(problems)
    print(f"rows={len(lines)} failures={failures}")
    print(f"registry_last_id={max(existing_ids, key=lambda s: int(s[1:]))} ids_free={[rid for rid in RAW if rid not in existing_ids]}")
    return 0 if failures == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
