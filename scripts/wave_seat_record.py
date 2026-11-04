#!/usr/bin/env python3
"""Record per-seat outcome from a wave results file (round 81, R80-6).

The orchestrator's `<wave>-results.json` carries per seat only `name`, `agent`
and `output`. It records no status, exit code or error text, so a dead seat's
cause cannot be cited from committed bytes. This recorder writes the lane-owned
record that makes the outcome decidable: it joins the wave spec's roles,
classifies each settling seat (`reported` / `empty` / `unknown`), re-derives each
output's byte count and digest, lists spec seats that never settled, and names
the schema limit instead of inventing an error message.

    python3 -B scripts/wave_seat_record.py --results <w1-results.json> --spec <w1-spec.json> --out <record.json>

The record is canonical JSON (sorted keys, one-space indent) so a counter can
compare a committed record against a fresh re-derivation byte for byte.

Exit 0 wrote the record, 2 unreadable input, 64 usage.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
from pathlib import Path

SCHEMA_LIMIT = ("w1-results.json records only name, agent and output; it carries no status, "
                "exit code or error text, so a seat's failure cause is not recoverable from "
                "committed bytes and every exit/error here is declared unknown")


def load(path: str) -> dict:
    with open(path, encoding="utf-8") as handle:
        document = json.load(handle)
    if not isinstance(document, dict):
        raise ValueError("top-level document is not an object")
    return document


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    ap.add_argument("--results", required=True)
    ap.add_argument("--spec", required=True)
    ap.add_argument("--out", required=True)
    a = ap.parse_args()
    try:
        results = load(a.results)
        spec = load(a.spec)
    except (OSError, ValueError) as exc:
        print(f"unreadable input: {exc}", file=sys.stderr)
        return 2
    roles = {i.get("name"): i.get("role") for i in (spec.get("items") or []) if isinstance(i, dict)}
    seats = {}
    for row in (results.get("results") or []):
        if not isinstance(row, dict) or not isinstance(row.get("name"), str):
            continue
        name = row["name"]
        output = row.get("output") or ""
        if not isinstance(output, str):
            output = str(output)
        raw = output.encode("utf-8")
        seats[name] = {
            "agent": row.get("agent") if isinstance(row.get("agent"), str) else "unknown",
            "role": roles.get(name, "unknown"),
            "status": "reported" if raw.strip() else "empty",
            "exit": "unknown",
            "error": "not recorded in w1-results.json",
            "output_bytes": len(raw),
            "output_sha256": hashlib.sha256(raw).hexdigest(),
        }
    record = {
        "wave": results.get("wave") or spec.get("wave"),
        "round": results.get("round"),
        "seats": seats,
        "empty_output": sorted(n for n, e in seats.items() if e["status"] == "empty"),
        "not_settled": sorted(n for n in roles if n not in seats),
        "schema_limit": SCHEMA_LIMIT,
    }
    Path(a.out).write_text(json.dumps(record, indent=1, sort_keys=True) + "\n", encoding="utf-8")
    print(f"seats={len(seats)} empty={len(record['empty_output'])} "
          f"not_settled={len(record['not_settled'])}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
