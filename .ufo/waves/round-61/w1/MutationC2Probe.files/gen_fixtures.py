#!/usr/bin/env python3
"""Generate the 18 contract H-fixtures (+3 proposed additions) for audit.py."""
import json, os

ROOT = os.path.dirname(os.path.abspath(__file__))
FIX = os.path.join(ROOT, "fixtures")

def resp(status, headers):
    return {"status": status, "finalUrl": "https://pub.test/",
            "headers": [list(h) for h in headers],
            "sha256": "0" * 64, "bytes": 0,
            "fetchedAt": "2026-10-27T00:00:00Z", "userAgent": "round61"}

def manifest(checks, version=1):
    return {"version": version, "checks": checks}

def check(cid, expect, https=True, singleton=None, source="response.json"):
    return {"id": cid, "source": source, "url": "https://pub.test/",
            "https": https,
            "expect": {"content_type_present": False, "hsts_present": False,
                       "xcto_nosniff_value": False, "csp_present": False,
                       **expect},
            "singleton_fields": singleton or []}

CASES = {}

# H1: 200, all present, canonical-cased names; singleton [content-type]
CASES["H1"] = (manifest([check("H1",
    {"content_type_present": True, "hsts_present": True,
     "xcto_nosniff_value": True, "csp_present": True},
    singleton=["content-type"])]),
    resp(200, [("Content-Type", "text/html; charset=utf-8"),
               ("Strict-Transport-Security", "max-age=31536000"),
               ("X-Content-Type-Options", "nosniff"),
               ("Content-Security-Policy", "default-src 'self'")]))

# H2: 200, no Content-Type
CASES["H2"] = (manifest([check("H2",
    {"content_type_present": True, "hsts_present": True, "csp_present": True},
    singleton=["content-type"])]),
    resp(200, [("Strict-Transport-Security", "max-age=31536000"),
               ("X-Content-Type-Options", "nosniff"),
               ("Content-Security-Policy", "default-src 'self'")]))

# H3: https, hsts expected, no STS field
CASES["H3"] = (manifest([check("H3",
    {"content_type_present": True, "hsts_present": True, "csp_present": True})]),
    resp(200, [("Content-Type", "text/html"),
               ("X-Content-Type-Options", "nosniff"),
               ("Content-Security-Policy", "default-src 'self'")]))

# H4: STS with parameters
CASES["H4"] = (manifest([check("H4", {"hsts_present": True})]),
    resp(200, [("Content-Type", "text/html"),
               ("Strict-Transport-Security", "max-age=31536000; includeSubDomains")]))

# H5: exact nosniff
CASES["H5"] = (manifest([check("H5", {"xcto_nosniff_value": True})]),
    resp(200, [("Content-Type", "text/html"),
               ("X-Content-Type-Options", "nosniff")]))

# H6: NOsniff + trailing OWS
CASES["H6"] = (manifest([check("H6", {"xcto_nosniff_value": True})]),
    resp(200, [("Content-Type", "text/html"),
               ("X-Content-Type-Options", "NOsniff ")]))

# H7: wrong value
CASES["H7"] = (manifest([check("H7", {"xcto_nosniff_value": True})]),
    resp(200, [("Content-Type", "text/html"),
               ("X-Content-Type-Options", "sniff")]))

# H8: csp expected, absent
CASES["H8"] = (manifest([check("H8", {"csp_present": True})]),
    resp(200, [("Content-Type", "text/html"),
               ("X-Content-Type-Options", "nosniff"),
               ("Strict-Transport-Security", "max-age=1")]))

# H9: duplicate Content-Type, differently cased; singleton listed
CASES["H9"] = (manifest([check("H9", {"content_type_present": True},
    singleton=["content-type"])]),
    resp(200, [("Content-Type", "text/html"),
               ("content-type", "text/html")]))

# H10: duplicate Set-Cookie (never a singleton), ct listed once
CASES["H10"] = (manifest([check("H10", {"content_type_present": True},
    singleton=["set-cookie", "content-type"])]),
    resp(200, [("Set-Cookie", "a=1"), ("Set-Cookie", "b=2"),
               ("Content-Type", "text/html")]))

# H11: 404, no Content-Type -> content_type_present is 2xx-only
CASES["H11"] = (manifest([check("H11", {"content_type_present": True})]),
    resp(404, [("X-Content-Type-Options", "nosniff")]))

# H12: malformed header-name token
CASES["H12"] = (manifest([check("H12", {"content_type_present": True})]),
    resp(200, [("Content-Type", "text/html"), ("X Bad Name", "v")]))

# H13: source receipt missing
CASES["H13"] = (manifest([check("H13", {"content_type_present": True},
    source="missing-receipt.json")]), None)

# H14: manifest version != 1
CASES["H14"] = (manifest([check("H14", {})], version=2),
    resp(200, [("Content-Type", "text/html")]))

# H15: unparseable manifest JSON
CASES["H15"] = (None, "NOT-JSON {")

# H16: every expectation off, clean headers
CASES["H16"] = (manifest([check("H16", {})]),
    resp(200, [("Content-Type", "text/html"),
               ("Strict-Transport-Security", "max-age=1"),
               ("X-Content-Type-Options", "nosniff"),
               ("Content-Security-Policy", "default-src 'self'")]))

# H17: values padded with OWS only
CASES["H17"] = (manifest([check("H17",
    {"content_type_present": True, "xcto_nosniff_value": True})]),
    resp(200, [("Content-Type", "  text/html  "),
               ("X-Content-Type-Options", "  nosniff  ")]))

# H18: empty checks array
CASES["H18"] = (manifest([]), None)

# --- proposed additions (not in the frozen 18) ---
# A1: 204 without Content-Type (non-200 2xx boundary for content_type_present)
CASES["A1"] = (manifest([check("A1", {"content_type_present": True})]),
    resp(204, [("X-Content-Type-Options", "nosniff")]))

# A2: Content-Type present but empty value
CASES["A2"] = (manifest([check("A2", {"content_type_present": True})]),
    resp(200, [("Content-Type", "")]))

# A3: hsts expected but check is not https
CASES["A3"] = (manifest([check("A3", {"hsts_present": True}, https=False)]),
    resp(200, [("Content-Type", "text/html")]))

# expected (exit, findings_count) per contract table; additions marked *
EXPECTED = {
    "H1": (0, 0), "H2": (1, 1), "H3": (1, 1), "H4": (0, 0), "H5": (0, 0),
    "H6": (0, 0), "H7": (1, 1), "H8": (1, 1), "H9": (1, 1), "H10": (0, 0),
    "H11": (0, 0), "H12": (1, 1), "H13": (1, 0), "H14": (2, None),
    "H15": (2, None), "H16": (0, 0), "H17": (0, 0), "H18": (0, 0),
    "A1": (1, 1), "A2": (0, 0), "A3": (0, 0),
}

def main():
    os.makedirs(FIX, exist_ok=True)
    for cid, (man, rec) in CASES.items():
        d = os.path.join(FIX, cid)
        os.makedirs(d, exist_ok=True)
        if man is None:
            with open(os.path.join(d, "manifest.json"), "w") as fh:
                fh.write(rec if isinstance(rec, str) else "NOT-JSON {")
        else:
            with open(os.path.join(d, "manifest.json"), "w") as fh:
                json.dump(man, fh, indent=1)
            if rec is not None:
                with open(os.path.join(d, "response.json"), "w") as fh:
                    json.dump(rec, fh, indent=1)
    with open(os.path.join(ROOT, "expected.json"), "w") as fh:
        json.dump(EXPECTED, fh, indent=1)
    print(f"wrote {len(CASES)} fixtures to {FIX}")

if __name__ == "__main__":
    main()
