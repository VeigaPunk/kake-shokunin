#!/usr/bin/env python3
"""Round-82 wave accounting — re-derives spec/results populations and the attack share.

make_accounting.py --spec .ufo/waves/round-82/w1-spec.json \
                   --results .ufo/waves/round-82/w1-results.json \
                   --out .ufo/waves/round-82/w1-accounting.json

A seat is `settled` when its results row carries non-empty output (the round-81 frozen rule). A
`substantive` seat additionally carries >= 200 bytes of output (a progress line is not a
deliverable). The attack roles are the run-15 directive's {reviewer, critic, mutation-tester,
labrat}; the requested and settled shares are printed and written. Exit 0 written, 2 bad input,
64 usage.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import sys

ATTACK_ROLES = ("reviewer", "critic", "mutation-tester", "labrat")
SUBSTANTIVE_BYTES = 200


def digest(path: str) -> str:
    with open(path, "rb") as stream:
        return hashlib.sha256(stream.read()).hexdigest()


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--spec", required=True)
    parser.add_argument("--results", required=True)
    parser.add_argument("--out", required=True)
    try:
        args = parser.parse_args(argv)
    except SystemExit as exc:
        return 0 if exc.code == 0 else 64
    try:
        with open(args.spec, encoding="utf-8") as stream:
            spec = json.load(stream)
        with open(args.results, encoding="utf-8") as stream:
            results = json.load(stream)
        items = spec["items"]
        rows = results["results"]
    except (OSError, json.JSONDecodeError, KeyError, TypeError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 2
    roles = {item["name"]: item["role"] for item in items}
    requested = len(items)
    requested_attack = sum(1 for item in items if item["role"] in ATTACK_ROLES)
    settled = []
    substantive = []
    for row in rows:
        name = row.get("name")
        output = row.get("output") or ""
        size = len(output.encode("utf-8"))
        if size > 0:
            settled.append(name)
        if size >= SUBSTANTIVE_BYTES:
            substantive.append(name)
    settled_attack = [name for name in settled if roles.get(name) in ATTACK_ROLES]
    substantive_attack = [name for name in substantive if roles.get(name) in ATTACK_ROLES]
    record = {
        "schema": "kake-wave-accounting/v1",
        "lane": results.get("lane", "kake"),
        "round": results.get("round"),
        "wave": results.get("wave"),
        "attack_roles": list(ATTACK_ROLES),
        "substantive_floor_bytes": SUBSTANTIVE_BYTES,
        "requested": requested,
        "requested_attack": requested_attack,
        "requested_share": round(requested_attack / requested, 4) if requested else 0.0,
        "settled": len(settled),
        "settled_names": settled,
        "settled_attack": len(settled_attack),
        "settled_share": round(len(settled_attack) / len(settled), 4) if settled else 0.0,
        "substantive": len(substantive),
        "substantive_names": substantive,
        "substantive_attack": len(substantive_attack),
        "substantive_share": round(len(substantive_attack) / len(substantive), 4) if substantive else 0.0,
        "empty_output": sorted(set(roles) - set(settled)),
        "spec_sha256": digest(args.spec),
        "results_sha256": digest(args.results),
    }
    with open(args.out, "w", encoding="utf-8") as stream:
        json.dump(record, stream, indent=1)
        stream.write("\n")
    print(f"requested={record['requested']} requested_attack={record['requested_attack']} "
          f"requested_share={record['requested_share']}")
    print(f"settled={record['settled']} settled_attack={record['settled_attack']} "
          f"settled_share={record['settled_share']}")
    print(f"substantive={record['substantive']} substantive_attack={record['substantive_attack']} "
          f"substantive_share={record['substantive_share']}")
    print(f"empty_output={','.join(record['empty_output']) or '-'}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
