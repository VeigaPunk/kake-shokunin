#!/usr/bin/env python3
"""Header census over round-61 capture receipts (read-only, no network).

usage: census.py CAPTURE_DIR [--json]
Reads <CAPTURE_DIR>/<id>/response.json for the round-23 public surface ids and
reports per surface: status, presence of content-type / strict-transport-security /
x-content-type-options / content-security-policy, duplicate occurrences of the
singleton names, and field-name syntax faults (RFC 9110 token rule).
Tolerant of header encodings: [{"name","value"}], [[name,value]] or {name: value}.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

IDS = [
    "ds4cc-primary", "plazir15-ghp", "charter-ghp", "ds4cc-kimi",
    "burnerchrome-kimi", "vault-index-kimi", "plazir27-kimi", "ufo-fsd-kimi-pro",
    "lucario-ghp", "lucario-kimi", "plazir15-kimi", "charter-kimi",
]
# RFC 9110 5.6.2 field-name = token = 1*tchar
TCHAR = re.compile(r"^[!#$%&'*+\-.^_`|~0-9A-Za-z]+$")
SINGLETONS = ["content-type", "strict-transport-security", "x-content-type-options"]
# CSP3 combines multiple policies, so CSP is excluded from the singleton set but
# its duplicate count is reported for the manifest's singleton_fields choice.
WATCH = SINGLETONS + ["content-security-policy"]


def load(path: Path):
    raw = path.read_text(encoding="utf-8", errors="replace")
    doc = json.loads(raw)
    status = doc.get("status", doc.get("finalStatus", doc.get("final_status")))
    headers = doc.get("headers", [])
    pairs: list[tuple[str, str]] = []
    if isinstance(headers, dict):
        for k, v in headers.items():
            vals = v if isinstance(v, list) else [v]
            for one in vals:
                pairs.append((str(k), str(one)))
    else:
        for item in headers:
            if isinstance(item, dict):
                pairs.append((str(item.get("name", item.get("field", ""))),
                              str(item.get("value", item.get("val", "")))))
            elif isinstance(item, (list, tuple)) and len(item) >= 2:
                pairs.append((str(item[0]), str(item[1])))
    return doc, status, pairs


def main() -> int:
    if len(sys.argv) < 2:
        print("usage: census.py CAPTURE_DIR [--json]", file=sys.stderr)
        return 64
    cap = Path(sys.argv[1])
    as_json = "--json" in sys.argv[2:]
    rows, problems = [], []
    for sid in IDS:
        p = cap / sid / "response.json"
        if not p.is_file():
            rows.append({"id": sid, "missing": True})
            problems.append(f"{sid}: receipt missing at {p}")
            continue
        try:
            doc, status, pairs = load(p)
        except (OSError, json.JSONDecodeError) as exc:
            rows.append({"id": sid, "malformed": str(exc)})
            problems.append(f"{sid}: unreadable receipt ({exc})")
            continue
        lower = [(n.lower(), n, v) for n, v in pairs]
        counts = {name: sum(1 for lo, _, _ in lower if lo == name) for name in WATCH}
        value_of = {}
        for name in WATCH:
            vals = [v for lo, _, v in lower if lo == name]
            value_of[name] = vals
        faults = []
        for lo, orig, _v in lower:
            if not TCHAR.match(orig):
                faults.append(orig)
            elif lo != lo.strip():
                faults.append(orig)
        # receipt-shape fields the contract requires
        shape = {
            "finalUrl": bool(doc.get("finalUrl") or doc.get("final_url")),
            "sha256": bool(doc.get("sha256")),
            "bytes": "bytes" in doc,
            "fetchedAt": bool(doc.get("fetchedAt") or doc.get("fetched_at")),
            "userAgent": str(doc.get("userAgent") or doc.get("user_agent") or ""),
            "redirects": "redirects" in doc,
        }
        row = {
            "id": sid,
            "url": doc.get("url"),
            "finalUrl": doc.get("finalUrl") or doc.get("final_url"),
            "status": status,
            "headers": len(pairs),
            **{f"{k}_present": counts[k] > 0 for k in WATCH},
            **{f"{k}_count": counts[k] for k in WATCH},
            "ct_values": value_of["content-type"],
            "xcto_values": value_of["x-content-type-options"],
            "hsts_values": value_of["strict-transport-security"],
            "csp_count": counts["content-security-policy"],
            "csp_values": value_of["content-security-policy"],
            "field_name_faults": faults,
            "dupe_any": sorted({lo for lo, _, _ in lower
                                if sum(1 for l2, _, _ in lower if l2 == lo) > 1}),
            "shape": shape,
        }
        rows.append(row)
    if as_json:
        print(json.dumps({"surfaces": rows, "problems": problems}, indent=1))
    else:
        print(f"{'id':<20}{'st':>4} {'CT':>3}{'HSTS':>6}{'XCTO':>6}{'CSP':>5}  dup(singleton)")
        for r in rows:
            if r.get("missing") or r.get("malformed"):
                print(f"{r['id']:<20}  --  MISSING/MALFORMED")
                continue
            dup = [k for k in SINGLETONS if r[f"{k}_count"] > 1]
            print(f"{r['id']:<20}{str(r['status']):>4} "
                  f"{'Y' if r['content-type_present'] else '-':>3}"
                  f"{'Y' if r['strict-transport-security_present'] else '-':>6}"
                  f"{'Y' if r['x-content-type-options_present'] else '-':>6}"
                  f"{'Y' if r['content-security-policy_present'] else '-':>5}"
                  f"  {','.join(dup) or 'none'}"
                  + (f"  FAULT:{','.join(r['field_name_faults'])}" if r['field_name_faults'] else ""))
        for p in problems:
            print("PROBLEM:", p)
    return 0


if __name__ == "__main__":
    sys.exit(main())
