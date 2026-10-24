#!/usr/bin/env python3
"""Freeze executed, receipt-only cases from retained wave-1 reports.

Author-side selection is recorded in population-selection.json, including rejected
representations and duplicates. Run before implementation measurement, not to tune
an oracle after seeing the new runner's outcomes.
"""
import hashlib
import json
from pathlib import Path
import re

ROOT = Path(__file__).resolve().parent
BASE = "f7de3ab4e9f030a15a857a5a08631bd8e690f436"
COMPANION = {
    "heading-id-c1-c11-distinct-control", "heading-id-c1-not-c11",
    "heading-id-close-bracket-cited-control", "heading-id-newline-cited-control",
    "heading-id-citations-before-heading",
    "finalurl-c0-lf-chain-consistent",
}
selected, decisions, seen = [], [], {}
for report in sorted((ROOT / "w1").glob("*.md")):
    if not report.stem.startswith("Gap") and report.stem != "ExecMalformedMatrix":
        continue
    for block in re.findall(r"```json\s*\n(.*?)\n```", report.read_text(), re.S):
        try:
            array = json.loads(block)
        except ValueError:
            continue
        if not isinstance(array, list):
            continue
        for original in array:
            if not isinstance(original, dict) or "r23Observed" not in original:
                continue
            case = dict(original)
            name = case.get("id")
            pointer = f".ufo/waves/round-24/w1/{report.name}"
            reason = None
            if name in COMPANION:
                reason = "requires companion Markdown or receipt changes not represented by this single-file mutation"
            elif name == "uppercase-sha256":
                reason = "ambiguous hex-casing acceptance not a malformed receipt claim; preserve historical exact digest policy, do not silently broaden it"
            if reason:
                decisions.append({"source": pointer, "id": name, "decision": "rejected", "reason": reason})
                continue
            if case.get("op") in ("set", "delete"):
                case["jsonPath"] = [str(p) for p in case.get("jsonPath", [])]
                if str(case.get("file", "")).endswith("page.html") and case.get("op") == "set" and case["jsonPath"] == []:
                    case["op"] = "raw"
                    case.pop("jsonPath")
            if case.get("op") == "raw" and "rawBase64" in case:
                import base64
                case["value"] = base64.b64decode(case.pop("rawBase64")).decode("utf-8")
            identity = json.dumps({k: case.get(k) for k in ("target", "file", "op", "jsonPath", "value", "replace")}, sort_keys=True, ensure_ascii=True)
            if identity in seen:
                prior = seen[identity]
                if prior["expect"] != case["expect"]:
                    raise ValueError(f"conflicting oracle: {prior['id']} / {name}")
                decisions.append({"source": pointer, "id": name, "decision": "duplicate", "of": prior["id"]})
                continue
            if any(p["id"] == name for p in selected):
                case["id"] = report.stem + "-" + name
            case["source"] = pointer
            selected.append(case)
            seen[identity] = case
            decisions.append({"source": pointer, "id": case["id"], "decision": "admitted"})
if not selected:
    raise ValueError("no executed cases found")
population = {"round": 24, "fixtureBase": BASE, "cases": selected}
raw = (json.dumps(population, indent=1, ensure_ascii=True, allow_nan=False) + "\n").encode()
(ROOT / "c2-population.json").write_bytes(raw)
(ROOT / "population-selection.json").write_text(json.dumps({
    "populationSha256": hashlib.sha256(raw).hexdigest(), "cases": len(selected),
    "decisions": decisions,
}, indent=1) + "\n")
print(f"cases={len(selected)} reject={sum(c['expect']=='reject' for c in selected)} accept={sum(c['expect']=='accept' for c in selected)} sha256={hashlib.sha256(raw).hexdigest()}")
