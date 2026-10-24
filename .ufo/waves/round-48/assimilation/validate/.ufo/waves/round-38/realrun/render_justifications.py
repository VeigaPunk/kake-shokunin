#!/usr/bin/env python3
"""Render justifications.md from expectations.json (the declared oracle).

Reads only the declared expectations file, so the human-readable justification
cannot drift from the machine-checked one.
"""
import json
import os

HERE = os.path.dirname(os.path.abspath(__file__))
EX = json.load(open(os.path.join(HERE, "expectations.json"), encoding="utf-8"))
CHECKS = EX["newChecks"]
EXPECT = EX["manifests"]

hosts = []
for cid, rec in CHECKS.items():
    if rec["host"] not in hosts:
        hosts.append(rec["host"])

lines = []
lines.append("# Round-38 C2 real-run: per-check justification lines")
lines.append("")
lines.append("Oracle: `expectations.json` (declared from the public round-38 contract text; no sealed")
lines.append("case was read, listed or run). Every quote below was asserted verbatim at its line")
lines.append("against the retained round-37 body by `build_r38_manifest.py`, whose run also re-checked")
lines.append("each retained body's sha256 against the round-37 fetch receipts.")
lines.append("")
lines.append(f"Main manifest: `manifest.json`, {len(CHECKS) + 55} checks (55 round-37 checks kept verbatim")
lines.append("plus the 36 below). Declared report: verdict `could-not-evaluate`, "
             f"checksEvaluated {EXPECT['manifest.json']['checksEvaluated']}, "
             f"{len(EXPECT['manifest.json']['findings'])} findings (the 12 (i) check faults); exit 2.")
lines.append("")
lines.append("Outcome vocabulary: `allow`/`disallow` are access results the tool must find no finding")
lines.append("for (the check's `expect` field says which); `check_invalid` is a check fault the tool")
lines.append("must report as `{\"check\": <id>, \"reason\": \"check_invalid\"}` and must not evaluate.")
lines.append("")

for host in hosts:
    rows = [(cid, rec) for cid, rec in CHECKS.items() if rec["host"] == host]
    lines.append(f"## {host} — `robots/{host.replace('.', '_')}.txt`")
    lines.append("")
    for cid, rec in rows:
        lines.append(f"- `{cid}` — `{rec['url']}` — user-agent `{rec['userAgent']}` — "
                     f"declared **{rec['declaredOutcome']}**")
        quotes = "; ".join(f"L{q['line']} `{q['text']}`" for q in rec["quotes"])
        lines.append(f"  - deciding line(s): {quotes}")
        lines.append(f"  - why: {rec['why']}")
    lines.append("")

lines.append("## (h) fault manifests (same retained robots files)")
lines.append("")
for name in sorted(n for n in EXPECT if n != "manifest.json"):
    e = EXPECT[name]
    lines.append(f"### `{name}`")
    lines.append("")
    lines.append(f"- declared: exit {e['exit']}, verdict `{e['verdict']}`, "
                 f"checksEvaluated {e['checksEvaluated']}, findings "
                 f"`{json.dumps(e['findings'], ensure_ascii=False)}`")
    lines.append(f"- basis: {e['basis']}")
    lines.append("")

with open(os.path.join(HERE, "justifications.md"), "w", encoding="utf-8") as fh:
    fh.write("\n".join(lines) + "\n")
print("wrote justifications.md,", len(CHECKS), "checks over", len(hosts), "hosts")
