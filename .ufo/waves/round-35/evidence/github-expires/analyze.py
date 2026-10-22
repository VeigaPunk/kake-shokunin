#!/usr/bin/env python3
"""Parse saved observations: request clock, HTTP Date, body Expires, offsets."""
import glob, hashlib, os, re, sys
from datetime import datetime, timezone

D = os.path.dirname(os.path.abspath(__file__))
RFC3339 = "%Y-%m-%dT%H:%M:%SZ"

def parse_meta(p):
    kv = {}
    for line in open(p, encoding="utf-8"):
        if "=" in line:
            k, _, v = line.strip().partition("=")
            kv[k] = v
    return kv

def hdr(text, name):
    m = re.search(r"^%s:\s*(.*?)\r?$" % re.escape(name), text, re.I | re.M)
    return m.group(1).strip() if m else None

def main():
    rows = []
    for hp in sorted(glob.glob(os.path.join(D, "*.headers"))):
        lbl = os.path.basename(hp)[: -len(".headers")]
        bp = os.path.join(D, lbl + ".body")
        mp = os.path.join(D, lbl + ".meta")
        if not os.path.exists(bp):
            continue
        h = open(hp, encoding="utf-8", errors="replace").read()
        body = open(bp, "rb").read()
        meta = parse_meta(mp) if os.path.exists(mp) else {}
        date_h = hdr(h, "Date")
        # RFC 3339 Expires field in the body (not the HTTP Expires header)
        exp = None
        for line in body.decode("utf-8", "replace").splitlines():
            if line.lower().startswith("expires:"):
                exp = line.split(":", 1)[1].strip()
        status = h.split("\r\n", 1)[0].strip()
        off = None
        if date_h and exp:
            try:
                d = datetime.strptime(date_h, "%a, %d %b %Y %H:%M:%S GMT").replace(tzinfo=timezone.utc)
                e = datetime.strptime(exp, "%Y-%m-%dT%H:%M:%Sz").replace(tzinfo=timezone.utc)
                off = int((e - d).total_seconds())
            except ValueError as exc:
                off = "parse-error:%s" % exc
        rows.append(dict(label=lbl, status=status, code=meta.get("http_code"),
                         start=meta.get("local_utc_start"), date=date_h,
                         expires=exp, offset_s=off,
                         etag=hdr(h, "ETag"), clen=hdr(h, "Content-Length"),
                         body_sha=hashlib.sha256(body).hexdigest(),
                         body_bytes=len(body)))
    for r in rows:
        print("%-9s %-14s code=%-4s start=%s" % (r["label"], r["status"].replace("HTTP/1.1 ", ""), r["code"], r["start"]))
        print("           Date=%s  Expires_field=%s" % (r["date"], r["expires"]))
        if isinstance(r["offset_s"], int):
            print("           offset_expires_minus_date = %d s = %.6f d (delta from 30d: %+d s)"
                  % (r["offset_s"], r["offset_s"] / 86400.0, r["offset_s"] - 2592000))
        else:
            print("           offset = %s" % r["offset_s"])
        print("           ETag=%s Content-Length=%s body_sha256=%s bytes=%d"
              % (r["etag"], r["clen"], r["body_sha"][:16], r["body_bytes"]))
        print()
    ints = [r["offset_s"] for r in rows if isinstance(r["offset_s"], int) and "google" not in r["label"]]
    if len(ints) >= 2:
        print("github offsets: %s  distinct=%d  spread=%ss"
              % (ints, len(set(ints)), max(ints) - min(ints)))
    exps = [r["expires"] for r in rows if "google" not in r["label"] and r["expires"]]
    print("distinct github Expires values: %d over %d observations" % (len(set(exps)), len(exps)))
    return 0

if __name__ == "__main__":
    sys.exit(main())
