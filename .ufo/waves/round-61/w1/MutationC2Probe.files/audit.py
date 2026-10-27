#!/usr/bin/env python3
"""Mutation harness for the round-61 C2 header_audit design.

One engine implements the contract's expected semantics (MUTANT=ref);
MUTANT=m01..m12 each flip exactly one semantic point. The runner feeds the
18 contract cases (H1..H18) to every variant and diffs verdicts against the
contract's expected column.
"""
import json, os, re, sys

MUTANT = os.environ.get("MUTANT", "ref")
TOKEN = re.compile(r"^[!#$%&'*+\-.^_`|~0-9A-Za-z]+$")
FINDING_CLASSES = (
    "content_type_present", "hsts_present", "xcto_nosniff_value",
    "csp_present", "singleton_fields", "field_name_syntax",
)

def load_receipt(path):
    try:
        with open(path, "r", encoding="utf-8") as fh:
            rec = json.load(fh)
    except Exception:
        return None
    try:
        status = int(rec["status"])
    except Exception:
        return None
    headers = rec.get("headers", [])
    if not isinstance(headers, list):
        return None
    return status, headers

def lookup(headers, name, case_insensitive=None):
    """All values whose field name matches `name`. m02: case-sensitive."""
    if case_insensitive is None:
        case_insensitive = MUTANT != "m02"
    out = []
    for n, v in headers:
        if case_insensitive:
            if str(n).lower() == name.lower():
                out.append(v)
        else:
            if str(n) == name:
                out.append(v)
    return out

def main(argv):
    if len(argv) != 2:
        print("usage: audit.py <manifest>", file=sys.stderr)
        return 64
    mpath = argv[1]
    try:
        with open(mpath, "r", encoding="utf-8") as fh:
            manifest = json.load(fh)
    except Exception:
        print("manifest_unparseable", file=sys.stderr)
        return 2
    if manifest.get("version") != 1:
        print("manifest_version", file=sys.stderr)
        return 2
    checks = manifest.get("checks")
    if not isinstance(checks, list):
        print("manifest_checks", file=sys.stderr)
        return 2
    if len(checks) == 0:
        print("checks=0 findings=0")
        return 0

    base = os.path.dirname(os.path.abspath(mpath))
    findings = []   # (check_id, class, detail)
    cne = 0

    for chk in checks:
        cid = chk.get("id", "?")
        src = chk.get("source")
        rec = load_receipt(os.path.join(base, src)) if src else None
        if rec is None:
            cne += 1
            print(f"{cid} could_not_evaluate source-receipt")
            if MUTANT == "m07":          # exit 2 on first manifest fault
                return 2
            continue
        status, headers = rec
        expect = chk.get("expect", {}) or {}
        https = bool(chk.get("https"))
        is2xx = (200 <= status < 300) if MUTANT != "m04" else (status == 200)

        # content_type_present: 2xx response with no Content-Type field
        if is2xx:
            vals = lookup(headers, "content-type")
            if MUTANT == "m05":          # value-based: field must have non-empty value
                if not any(str(v).strip() for v in vals):
                    findings.append((cid, "content_type_present", "no valued content-type"))
            else:
                if not vals:
                    findings.append((cid, "content_type_present", "missing content-type"))

        # hsts_present: https check expecting HSTS with no STS field
        gate = https or (MUTANT == "m08")   # m08: ignore the https gate
        if gate and expect.get("hsts_present"):
            if not lookup(headers, "strict-transport-security"):
                findings.append((cid, "hsts_present", "missing strict-transport-security"))

        # xcto_nosniff_value: every recorded XCTO value must be exactly nosniff
        for v in lookup(headers, "x-content-type-options"):
            if MUTANT == "m03":          # OWS not trimmed
                ok = str(v).lower() == "nosniff"
            elif MUTANT == "m06":        # case-sensitive compare
                ok = str(v).strip() == "nosniff"
            else:
                ok = str(v).strip().lower() == "nosniff"
            if not ok:
                findings.append((cid, "xcto_nosniff_value", f"value={v!r}"))

        # csp_present: declared expectation with no CSP field
        if expect.get("csp_present"):
            if not lookup(headers, "content-security-policy"):
                findings.append((cid, "csp_present", "missing content-security-policy"))

        # singleton_fields: listed name occurring more than once (case-insensitive);
        # Set-Cookie is never a singleton
        for name in chk.get("singleton_fields", []) or []:
            if str(name).lower() == "set-cookie" and MUTANT != "m09":
                continue
            if MUTANT == "m12":          # case-sensitive singleton counting
                n = len(lookup(headers, name, case_insensitive=False))
            else:
                n = len(lookup(headers, name))
            if (n >= 1) if MUTANT == "m01" else (n > 1):   # m01: off-by-one
                findings.append((cid, "singleton_fields", f"{name} x{n}"))

        # field_name_syntax: recorded header names must be RFC 9110 tokens
        if MUTANT != "m10":              # m10: syntax check disabled
            for n, _ in headers:
                if not TOKEN.match(str(n)):
                    findings.append((cid, "field_name_syntax", f"name={n!r}"))

    for cid, cls, detail in findings:
        print(f"{cid} {cls} {detail}")
    print(f"checks={len(checks)} findings={len(findings)}")
    if MUTANT == "m11":                  # cne does not force exit 1
        return 1 if findings else 0
    return 1 if (findings or cne) else 0

if __name__ == "__main__":
    sys.exit(main(sys.argv))
