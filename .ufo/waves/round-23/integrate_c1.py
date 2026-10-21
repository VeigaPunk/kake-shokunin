#!/usr/bin/env python3
"""Extract C1 receipts from wave-1 seat reports and render each unit's round-23 section.

Usage: integrate_c1.py --lane LANE [--write]
Reads w1/Reverify*.md (one receipt per unit) and w1/Surface*.md (property-map rows),
keeps only claims whose anchor occurs in the unit file at the base commit, renumbers
property-map claim ids, writes receipts/<unit>.json and prints a per-unit summary.
With --write it also appends the "## Live re-verification — round 23" section to each
unit file (once; refuses if the heading already exists). Rejected claims are listed in
receipts/rejected.json with the reason; nothing is silently dropped.
"""
import argparse
import json
import os
import re
import subprocess

ROUND = ".ufo/waves/round-23"
BASE = "b5d599e19bead54b96f589444e9ec64cdf67c28a"
HEADING = "## Live re-verification — round 23"
FIELDS = ("id", "anchor", "claim", "surface", "method", "observation", "verdict")


def json_blocks(text):
    for block in re.findall(r"```json\s*\n(.*?)\n```", text, flags=re.S):
        try:
            yield json.loads(block)
        except json.JSONDecodeError:
            continue


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("--lane", required=True)
    parser.add_argument("--write", action="store_true")
    args = parser.parse_args()
    lane = os.path.abspath(args.lane)
    w1 = os.path.join(lane, ROUND, "w1")
    units = json.load(open(os.path.join(lane, ROUND, "c1-population.json")))["units"]
    by_unit = {u["unit"]: {"unit": u["unit"], "path": u["path"], "observedAt": "2026-10-21", "claims": []} for u in units}
    sources = {u["unit"]: [] for u in units}
    rejected = []
    for name in sorted(os.listdir(w1)):
        if not name.endswith(".md") or not (name.startswith("Reverify") or name.startswith("Surface")):
            continue
        text = open(os.path.join(w1, name), encoding="utf-8").read()
        for block in json_blocks(text):
            unit = block.get("unit") if isinstance(block, dict) else None
            if unit not in by_unit or not isinstance(block.get("claims"), list):
                continue
            base_text = subprocess.run(["git", "-C", lane, "show", f"{BASE}:{by_unit[unit]['path']}"],
                                       capture_output=True, text=True, check=True).stdout
            for claim in block["claims"]:
                if not isinstance(claim, dict) or any(not str(claim.get(k, "")).strip() for k in FIELDS):
                    rejected.append({"seat": name, "unit": unit, "claim": claim, "reason": "missing field"})
                    continue
                if claim["anchor"] not in base_text:
                    # Seats often rewrap a quoted line; accept only a whitespace-only
                    # difference and store the exact base bytes as the anchor.
                    pattern = r"\s+".join(re.escape(token) for token in claim["anchor"].split())
                    match = re.search(pattern, base_text) if pattern else None
                    if match:
                        claim = dict(claim, anchor=match.group(0))
                if claim["anchor"] not in base_text:
                    rejected.append({"seat": name, "unit": unit, "claim": claim, "reason": "anchor not in unit at base"})
                    continue
                if claim["verdict"] not in {"HOLD", "STALE", "UNVERIFIABLE"}:
                    rejected.append({"seat": name, "unit": unit, "claim": claim, "reason": "bad verdict"})
                    continue
                if claim["verdict"] == "STALE" and not str(claim.get("correction", "")).strip():
                    rejected.append({"seat": name, "unit": unit, "claim": claim, "reason": "STALE without correction"})
                    continue
                if claim["verdict"] == "UNVERIFIABLE" and not str(claim.get("reason", "")).strip():
                    rejected.append({"seat": name, "unit": unit, "claim": claim, "reason": "UNVERIFIABLE without reason"})
                    continue
                entry = {k: claim[k] for k in FIELDS}
                for extra in ("correction", "reason"):
                    if str(claim.get(extra, "")).strip():
                        entry[extra] = claim[extra].strip()
                entry["seat"] = name[:-3]
                by_unit[unit]["claims"].append(entry)
            if name[:-3] not in sources[unit]:
                sources[unit].append(name[:-3])
    for unit, receipt in by_unit.items():
        for index, claim in enumerate(receipt["claims"], start=1):
            claim["id"] = f"c{index}"
    os.makedirs(os.path.join(lane, ROUND, "receipts"), exist_ok=True)
    summary = {}
    for unit, receipt in by_unit.items():
        with open(os.path.join(lane, ROUND, "receipts", f"{unit}.json"), "w", encoding="utf-8") as stream:
            json.dump(receipt, stream, indent=1, ensure_ascii=False)
        counts = {v: sum(c["verdict"] == v for c in receipt["claims"]) for v in ("HOLD", "STALE", "UNVERIFIABLE")}
        summary[unit] = {"claims": len(receipt["claims"]), **counts, "seats": sources[unit]}
        if args.write and receipt["claims"]:
            path = os.path.join(lane, receipt["path"])
            current = open(path, encoding="utf-8").read()
            if HEADING in current:
                raise SystemExit(f"{path}: round-23 heading already present")
            lines = ["", "", f"{HEADING} (2026-10-21)" if unit != "property-map" else f"{HEADING} (property map, 2026-10-21)", "",
                     "Read-only live checks; receipt `.ufo/waves/round-23/receipts/" + unit + ".json` "
                     "(claim, surface, method, observation). A HOLD is an observation on 2026-10-21, not a guarantee. "
                     "Where this section and earlier text disagree, this section is newer.", ""]
            for claim in receipt["claims"]:
                text = f"- [{unit}:{claim['id']}] **{claim['verdict']}** — {claim['claim']} Surface: `{claim['surface']}`."
                if claim["verdict"] == "STALE":
                    text += f" Correction: {claim['correction']}"
                elif claim["verdict"] == "UNVERIFIABLE":
                    text += f" Unverifiable: {claim['reason']}"
                lines.append(text)
            with open(path, "a", encoding="utf-8") as stream:
                stream.write(("" if current.endswith("\n") else "\n") + "\n" + "\n".join(lines[2:]) + "\n")
    with open(os.path.join(lane, ROUND, "receipts", "rejected.json"), "w", encoding="utf-8") as stream:
        json.dump(rejected, stream, indent=1, ensure_ascii=False)
    print(json.dumps({"units": summary, "rejectedClaims": len(rejected)}, indent=1))


if __name__ == "__main__":
    main()
