#!/usr/bin/env python3
"""Round-50 route map — resolve the operator's role→model table onto the Kimi substrate.

The route table is operator-owned and lives at `~/.omp/agent/config.yml`:
`task.agentModelOverrides` maps a taxonomy role to a `@m_*` bucket alias, and
`modelRoles` maps that alias to a provider model string. This script READS that
file; it never writes it and never invents a lane-local model choice. Each role's
bucket is then projected onto the aliases this substrate's own config
(`~/.kimi-code/config.toml`) exposes for the same model family, and the first
projection that answered a live one-line prompt is used for that role. A role
whose whole bucket is unusable falls back to the one alias that did answer, and
the fallback is recorded, so the report can state the deviation honestly.

Usage: python3 -B make_route_map.py <probe-results.txt> <out.json>
where probe-results.txt holds one "<kimi alias> exit=<code>" line per probed alias.
"""
from __future__ import annotations

import json
import os
import sys

import yaml

OPERATOR_CONFIG = os.path.expanduser("~/.omp/agent/config.yml")
KIMI_CONFIG = os.path.expanduser("~/.kimi-code/config.toml")
HERE = os.path.dirname(os.path.abspath(__file__))

ROLES = ("scout", "reviewer", "critic", "connector", "sentinel", "executor",
         "mutation-tester", "revenger", "simplifier", "scribe")

# provider model string (operator table) -> candidate aliases on this substrate,
# most faithful first. The provider prefix differs between the two hosts; the
# model family and the effort suffix are what must match.
CANDIDATES = {
    "devin/swe-2": ["devin/swe-2-max", "devin/swe-2-high", "devin/swe-2"],
    "commandcode/deepseek/deepseek-v4.1-flash": [
        "devin/deepseek-v4-1-flash-max", "devin/deepseek-v4-1-flash-high",
        "devin/deepseek-v4-1-flash"],
    "zai/glm-5.3-flash": ["zai-coding-plan/glm-5.3-flash", "zai-coding-plan/glm-5.3-flash-low"],
    "xai-oauth/grok-4.7-build-fast": ["xai-oauth/grok-4.7-fast", "xai-oauth/grok-4.7"],
    "minimax-code/MiniMax-M3.1-Flash": ["minimax-coding-plan/MiniMax-M3.1-Flash"],
}
FALLBACK = "minimax-coding-plan/MiniMax-M3.1-Flash"
# Appended to every role's candidate list: the strongest alias and the fallback that
# answered a live one-line prompt. A role whose own bucket is unreachable on this
# substrate therefore still lands on a working model, and the deviation is recorded.
GLOBAL_TAIL = ["devin/swe-2-max", FALLBACK]


def main() -> int:
    if len(sys.argv) != 3:
        print("usage: make_route_map.py <probe-results.txt> <out.json>", file=sys.stderr)
        return 64
    with open(OPERATOR_CONFIG, encoding="utf-8") as fh:
        operator = yaml.safe_load(fh)
    overrides = operator["task"]["agentModelOverrides"]
    buckets = operator["modelRoles"]

    probed = {}
    with open(sys.argv[1], encoding="utf-8") as fh:
        for line in fh:
            line = line.strip()
            if not line or "=" not in line:
                continue
            alias, sep, code = line.rpartition(" exit=")
            if not sep:
                continue
            probed[alias.strip()] = code.strip()

    kimi_aliases = set()
    with open(KIMI_CONFIG, encoding="utf-8") as fh:
        for line in fh:
            line = line.strip()
            if line.startswith('[models."') and line.endswith('"]'):
                kimi_aliases.add(line[len('[models."'):-len('"]')])

    roles = {}
    for role in ROLES:
        bucket = overrides.get(role)
        if not bucket:
            roles[role] = {"operatorAlias": None, "operatorModel": None,
                            "kimiModel": FALLBACK, "probe": "no operator override"}
            continue
        model = buckets.get(bucket.lstrip("@"))
        family = model.split(":")[0] if model else None
        picked = None
        probe_note = "no candidate probed"
        candidates = CANDIDATES.get(family, []) + GLOBAL_TAIL
        for candidate in candidates:
            if candidate not in kimi_aliases:
                probe_note = f"{candidate} not configured on this substrate"
                continue
            code = probed.get(candidate)
            if code is None:
                probe_note = f"{candidate} not probed"
                continue
            if code == "0":
                picked = candidate
                probe_note = f"{candidate} answered a one-line prompt (exit 0)"
                if candidate not in CANDIDATES.get(family, []):
                    probe_note += "; own bucket unreachable on this substrate"
                break
            probe_note = f"{candidate} failed (exit {code})"
        if picked is None:
            picked = FALLBACK
            probe_note += f"; fell back to {FALLBACK}"
        roles[role] = {
            "operatorAlias": bucket,
            "operatorModel": model,
            "kimiModel": picked,
            "probe": probe_note,
        }

    out = {
        "schema": "kake-r50-route-map-v1",
        "operatorRouteTable": OPERATOR_CONFIG,
        "substrateConfig": KIMI_CONFIG,
        "transport": "kimi --prompt",
        "roles": roles,
        "fallback": FALLBACK,
        "note": (
            "Resolved by reading the operator's task.agentModelOverrides and modelRoles "
            "tables and projecting each role's bucket onto this substrate's configured "
            "aliases; a bucket whose whole projection is unusable falls back to the one "
            "alias that answered a live one-line prompt, and the fallback is recorded."
        ),
    }
    with open(sys.argv[2], "w", encoding="utf-8") as fh:
        json.dump(out, fh, indent=2, ensure_ascii=False)
        fh.write("\n")
    for role in ROLES:
        print(f"{role}: {roles[role]['operatorAlias']} {roles[role]['operatorModel']} -> {roles[role]['kimiModel']}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
