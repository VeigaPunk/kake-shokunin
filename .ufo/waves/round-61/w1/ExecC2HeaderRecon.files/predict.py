#!/usr/bin/env python3
"""Predict header_audit.py findings from capture receipts under the manifest
policy declared for round 61 (content_type_present / hsts_present /
xcto_nosniff_value / csp_present all true; singleton_fields =
[content-type, content-security-policy, strict-transport-security]).

usage: predict.py CAPTURE_DIR [--json]
Read-only, network-free. Class names and conditions follow contract § Claim C2.
"""
from __future__ import annotations

import json
import sys
from pathlib import Path

IDS = [
    "ds4cc-primary", "plazir15-ghp", "charter-ghp", "ds4cc-kimi",
    "burnerchrome-kimi", "vault-index-kimi", "plazir27-kimi", "ufo-fsd-kimi-pro",
    "lucario-ghp", "lucario-kimi", "plazir15-kimi", "charter-kimi",
]
SINGLETONS = ["content-type", "content-security-policy", "strict-transport-security"]


def pairs_of(doc):
    out = []
    for item in doc.get("headers", []):
        if isinstance(item, dict):
            out.append((str(item.get("name", "")), str(item.get("value", ""))))
        elif isinstance(item, (list, tuple)) and len(item) >= 2:
            out.append((str(item[0]), str(item[1])))
    return out


def main() -> int:
    if len(sys.argv) < 2:
        print("usage: predict.py CAPTURE_DIR [--json]", file=sys.stderr)
        return 64
    cap = Path(sys.argv[1])
    as_json = "--json" in sys.argv[2:]
    allf, per = [], {}
    for sid in IDS:
        p = cap / sid / "response.json"
        findings = []
        try:
            doc = json.loads(p.read_text(encoding="utf-8", errors="replace"))
            status = doc.get("status")
            pairs = pairs_of(doc)
        except (OSError, json.JSONDecodeError) as exc:
            findings.append(("could_not_evaluate", f"receipt unreadable: {type(exc).__name__}"))
            per[sid] = findings
            allf.extend((sid, k, d) for k, d in findings)
            continue
        names = [n.lower() for n, _ in pairs]
        vals = {}
        for n, v in pairs:
            vals.setdefault(n.lower(), []).append(v)
        if isinstance(status, int) and 200 <= status < 300 and "content-type" not in names:
            findings.append(("content_type_present", f"status={status} no Content-Type"))
        if not isinstance(status, int):
            findings.append(("could_not_evaluate", "status not parseable"))
        elif "strict-transport-security" not in names:
            findings.append(("hsts_present", "no Strict-Transport-Security"))
        for v in vals.get("x-content-type-options", []):
            if v.strip().lower() != "nosniff":
                findings.append(("xcto_nosniff_value", f"value={v.strip()!r}"))
        if "content-security-policy" not in names:
            findings.append(("csp_present", "no Content-Security-Policy"))
        for s in SINGLETONS:
            if len(vals.get(s, [])) > 1:
                findings.append(("singleton_fields", f"{s} x{len(vals.get(s, []))}"))
        per[sid] = findings
        allf.extend((sid, k, d) for k, d in findings)
    if as_json:
        print(json.dumps({"checks": len(IDS), "findings": len(allf),
                          "per_check": {k: [list(x) for x in v] for k, v in per.items()}}, indent=1))
    else:
        for sid in IDS:
            for k, d in per[sid]:
                print(f"{sid} {k} {d}")
        print(f"checks={len(IDS)} findings={len(allf)}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
