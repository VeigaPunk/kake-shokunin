#!/usr/bin/env python3
"""Count C1 units with a valid round-23 live re-verification receipt at one Git revision.

Usage: measure_c1.py --root LANE --revision COMMIT
Population: .ufo/waves/round-23/c1-population.json read at the measured revision and
accepted only if its sha256 equals the frozen digest below. A unit passes iff,
at the measured revision:
  * receipts/<unit>.json exists, is a JSON object with unit/path matching the population,
    observedAt >= 2026-10-21, and a non-empty claims array;
  * every claim has id, anchor, claim, surface, method, observation and a verdict in
    HOLD/STALE/UNVERIFIABLE; STALE needs a correction, UNVERIFIABLE a reason;
  * every anchor is a substring of the unit file at the BASE revision (claims must be
    about text that existed before re-verification);
  * the unit file at the measured revision contains the heading
    "## Live re-verification — round 23" and, after it, every STALE correction verbatim
    and every claim id as "[<unit>:<id>]".
Exit 0 iff all units pass; 1 otherwise; 2 when the revision or population cannot be read.
"""
from __future__ import annotations
import argparse
import hashlib
import json
import subprocess
import sys

ROUND = ".ufo/waves/round-23"
BASE = "b5d599e19bead54b96f589444e9ec64cdf67c28a"
HEADING = "## Live re-verification — round 23"
POPULATION_SHA256 = "ffc9b3a44ee84ed827f3badc697f0ae5c8be007a50de3cafc2ccd23617697daf"
VERDICTS = {"HOLD", "STALE", "UNVERIFIABLE"}
FIELDS = ("id", "anchor", "claim", "surface", "method", "observation", "verdict")


def show(root: str, revision: str, path: str) -> str | None:
    done = subprocess.run(["git", "-C", root, "show", f"{revision}:{path}"], capture_output=True, check=False)
    return done.stdout.decode("utf-8") if done.returncode == 0 else None


def check_unit(root: str, revision: str, unit: dict[str, str]) -> tuple[list[str], dict[str, int]]:
    problems: list[str] = []
    verdicts = {v: 0 for v in VERDICTS}
    raw = show(root, revision, f"{ROUND}/receipts/{unit['unit']}.json")
    if raw is None:
        return ["receipt missing"], verdicts
    try:
        receipt = json.loads(raw)
    except json.JSONDecodeError as exc:
        return [f"receipt is not JSON: {exc}"], verdicts
    if not isinstance(receipt, dict):
        return ["receipt is not an object"], verdicts
    if receipt.get("unit") != unit["unit"] or receipt.get("path") != unit["path"]:
        problems.append("unit/path mismatch")
    if not isinstance(receipt.get("observedAt"), str) or receipt["observedAt"][:10] < "2026-10-21":
        problems.append("observedAt missing or before 2026-10-21")
    claims = receipt.get("claims")
    if not isinstance(claims, list) or not claims:
        return problems + ["no claims"], verdicts
    base_text = show(root, BASE, unit["path"]) or ""
    current = show(root, revision, unit["path"])
    if current is None:
        return problems + ["unit file missing at revision"], verdicts
    position = current.find(HEADING)
    section = current[position:] if position >= 0 else ""
    if position < 0:
        problems.append("round-23 heading missing in unit file")
    seen: set[str] = set()
    for index, claim in enumerate(claims):
        if not isinstance(claim, dict) or any(not isinstance(claim.get(k), str) or not claim[k].strip() for k in FIELDS):
            problems.append(f"claim {index}: missing field")
            continue
        if claim["id"] in seen:
            problems.append(f"claim {claim['id']}: duplicate id")
        seen.add(claim["id"])
        verdict = claim["verdict"]
        if verdict not in VERDICTS:
            problems.append(f"claim {claim['id']}: verdict {verdict!r}")
            continue
        verdicts[verdict] += 1
        if claim["anchor"] not in base_text:
            problems.append(f"claim {claim['id']}: anchor not in unit at base")
        if f"[{unit['unit']}:{claim['id']}]" not in section:
            problems.append(f"claim {claim['id']}: not cited in round-23 section")
        if verdict == "STALE":
            correction = claim.get("correction")
            if not isinstance(correction, str) or not correction.strip():
                problems.append(f"claim {claim['id']}: STALE without correction")
            elif correction not in section:
                problems.append(f"claim {claim['id']}: correction not in round-23 section")
        if verdict == "UNVERIFIABLE" and not str(claim.get("reason", "")).strip():
            problems.append(f"claim {claim['id']}: UNVERIFIABLE without reason")
    return problems, verdicts


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", required=True)
    parser.add_argument("--revision", required=True)
    args = parser.parse_args(argv)
    resolved = subprocess.run(["git", "-C", args.root, "rev-parse", "--verify", f"{args.revision}^{{commit}}"],
                              capture_output=True, text=True, check=False)
    population_raw = show(args.root, args.revision, f"{ROUND}/c1-population.json")
    if population_raw is not None and hashlib.sha256(population_raw.encode("utf-8")).hexdigest() != POPULATION_SHA256:
        population_raw = None
    if resolved.returncode != 0 or population_raw is None:
        print(json.dumps({"error": "revision or frozen population unreadable", "revision": args.revision}))
        return 2
    revision = resolved.stdout.strip()
    units = json.loads(population_raw)["units"]
    rows, totals = [], {v: 0 for v in VERDICTS}
    for unit in units:
        problems, verdicts = check_unit(args.root, revision, unit)
        for key, value in verdicts.items():
            totals[key] += value
        rows.append({"unit": unit["unit"], "pass": not problems, "claims": verdicts, "problems": problems})
    accepted = sum(row["pass"] for row in rows)
    print(json.dumps({"revision": revision, "accepted": accepted, "total": len(units), "claimVerdicts": totals,
                      "units": rows}, indent=1, sort_keys=True))
    return 0 if accepted == len(units) else 1


if __name__ == "__main__":
    raise SystemExit(main())
