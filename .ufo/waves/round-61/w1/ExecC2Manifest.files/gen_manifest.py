#!/usr/bin/env python3
"""Build round-61 C2 manifest v1 from capture receipts.

Policy (uniform, declared before looking at any outcome):
  content_type_present = True   (every 2xx surface must declare a media type)
  hsts_present         = True   iff the check URL scheme is https
  xcto_nosniff_value   = True   (where the field occurs it must be exactly nosniff)
  csp_present          = True   (every surface under test is expected to ship a CSP)
  singleton_fields     = [content-type, content-security-policy, strict-transport-security]

No per-surface tuning: the ONLY variation is the https-derived hsts flag.
"""
import json
import os
import sys

LANE = "/home/vgpnk/Projects/shokunin/kake-shokunin"
CAP = os.path.join(LANE, ".ufo/waves/round-61/capture")
SURF = os.path.join(LANE, ".ufo/waves/round-23/live")
SINGLETONS = ["content-type", "content-security-policy", "strict-transport-security"]
# header lists that are legitimately repeatable; never declare as singleton (contract H10)
NEVER_SINGLETON = {"set-cookie"}


def norm_headers(rec):
    """Return list[(name, value)] duplicates preserved, from a capture receipt."""
    h = rec.get("headers")
    out = []
    if isinstance(h, list):
        for e in h:
            if isinstance(e, (list, tuple)) and len(e) >= 2:
                out.append((str(e[0]), str(e[1])))
            elif isinstance(e, dict):
                n = e.get("name") or e.get("field")
                v = e.get("value")
                if n is not None and v is not None:
                    out.append((str(n), str(v)))
    elif isinstance(h, dict):
        # fallback: mapping name -> value | [values]
        for n, v in h.items():
            if isinstance(v, list):
                for x in v:
                    out.append((str(n), str(x)))
            else:
                out.append((str(n), str(v)))
    return out


def main():
    ids = sorted(
        d for d in os.listdir(SURF)
        if os.path.isdir(os.path.join(SURF, d))
    )
    checks = []
    rows = []
    missing = []
    for sid in ids:
        rs = os.path.join(CAP, sid, "response.json")
        if not os.path.isfile(rs):
            missing.append(sid)
            continue
        rec = json.load(open(rs))
        url = rec.get("url") or rec.get("finalUrl") or ""
        if not url:
            fj = json.load(open(os.path.join(SURF, sid, "fetch.json")))
            url = fj["url"]
        https = url.lower().startswith("https://")
        checks.append({
            "id": sid,
            "source": ".ufo/waves/round-61/capture/%s/response.json" % sid,
            "url": url,
            "https": https,
            "expect": {
                "content_type_present": True,
                "hsts_present": https,
                "xcto_nosniff_value": True,
                "csp_present": True,
                "singleton_fields": list(SINGLETONS),
            },
        })
        rows.append((sid, url, https, rec.get("status"),
                     len(norm_headers(rec)), rec.get("bytes")))
    if missing:
        print("MISSING RECEIPTS: %s" % ",".join(missing), file=sys.stderr)
    man = {"version": 1, "checks": checks}
    out = os.path.join(CAP, "manifest.json")
    if "--dry" not in sys.argv:
        with open(out, "w") as f:
            json.dump(man, f, indent=1, sort_keys=False)
            f.write("\n")
    print("manifest=%s checks=%d" % (out, len(checks)))
    for sid, url, https, status, nh, nbytes in rows:
        print("%-20s https=%-5s status=%-5s headers=%-3d bytes=%-7s %s"
              % (sid, https, status, nh, nbytes, url))
    return 0 if not missing else 1


if __name__ == "__main__":
    sys.exit(main())
