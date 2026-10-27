#!/usr/bin/env python3
"""ExecC2Manifest — receipt lint + policy cross-check (scratch, read-only).

Not the lane audit (scripts/header_audit.py is owned by ExecC2Audit): this is the
manifest seat's own receipt parse + an independent re-read of the same expectations,
used only to prove the manifest is bound to parseable receipts and to report the
declared-vs-observed table. Never writes into the lane.
"""
import hashlib
import json
import os
import sys

LANE = "/home/vgpnk/Projects/shokunin/kake-shokunin"
CAP = os.path.join(LANE, ".ufo/waves/round-61/capture")
REQUIRED = ["url", "finalUrl", "method", "status", "headers", "headerCount",
            "contentType", "bytes", "sha256", "truncated", "fetchedAt",
            "userAgent", "redirects", "error", "bodyFile"]
SINGLETONS = ["content-type", "content-security-policy", "strict-transport-security"]


def pairs(rec):
    out = []
    for h in rec.get("headers") or []:
        if isinstance(h, dict):
            out.append((str(h.get("name", "")), str(h.get("value", ""))))
        elif isinstance(h, (list, tuple)) and len(h) >= 2:
            out.append((str(h[0]), str(h[1])))
    return out


def main():
    man = json.load(open(os.path.join(CAP, "manifest.json")))
    ok = True
    print("id | status | https | hsts | xcto | csp | ct_dups | csp_dups | hsts_dups | sha256(receipt)")
    for chk in man["checks"]:
        sid = chk["id"]
        p = os.path.join(LANE, chk["source"])
        if not os.path.isfile(p):
            print("%s | MISSING %s" % (sid, p))
            ok = False
            continue
        raw = open(p, "rb").read()
        rec = json.loads(raw)
        miss = [k for k in REQUIRED if k not in rec]
        ps = pairs(rec)
        low = [n.lower() for n, _ in ps]
        def has(n):
            return n in low
        def vals(n):
            return [v for k, v in ps if k.lower() == n]
        dups = {n: low.count(n) for n in SINGLETONS if low.count(n) > 1}
        status = rec.get("status")
        findings = []
        if isinstance(status, int) and 200 <= status < 300 and not has("content-type"):
            findings.append("content_type_present")
        if chk["expect"]["hsts_present"] and not has("strict-transport-security"):
            findings.append("hsts_present")
        for v in vals("x-content-type-options"):
            if v.strip() != "nosniff":
                findings.append("xcto_nosniff_value")
        if chk["expect"]["csp_present"] and not has("content-security-policy"):
            findings.append("csp_present")
        for n in dups:
            findings.append("singleton_fields:" + n)
        bad = [n for n, _ in ps if " " in n or "\t" in n]
        if bad:
            findings.append("field_name_syntax")
        print("%s | %s | %s | %s | %s | %s | %s | %s | %s | %s%s%s" % (
            sid, status, chk["https"], has("strict-transport-security"),
            [v.strip() for v in vals("x-content-type-options")] or "-",
            has("content-security-policy"),
            low.count("content-type") if low.count("content-type") > 1 else 0,
            low.count("content-security-policy") if low.count("content-security-policy") > 1 else 0,
            low.count("strict-transport-security") if low.count("strict-transport-security") > 1 else 0,
            hashlib.sha256(raw).hexdigest(),
            " missing=" + ",".join(miss) if miss else "",
            " findings=" + ",".join(findings) if findings else " CLEAN"))
        if miss:
            ok = False
        if rec.get("userAgent") != "round61":
            print("  NOTE %s userAgent=%r" % (sid, rec.get("userAgent")))
        bf = rec.get("bodyFile")
        if bf:
            bp = os.path.join(os.path.dirname(p), bf)
            if os.path.isfile(bp):
                bh = hashlib.sha256(open(bp, "rb").read()).hexdigest()
                if bh != rec.get("sha256"):
                    print("  BODY-SHA-MISMATCH %s" % sid)
                    ok = False
            else:
                print("  BODY-MISSING %s" % sid)
    print("manifest checks=%d ok=%s" % (len(man["checks"]), ok))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
