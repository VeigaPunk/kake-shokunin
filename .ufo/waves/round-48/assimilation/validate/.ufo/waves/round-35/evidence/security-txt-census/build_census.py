#!/usr/bin/env python3
"""Build census/census.json from saved bodies, headers and .raw status lines.

Inputs (all already on disk, no network):
  census/.hosts          ten probe hostnames, one per line
  census/.request_ts     ISO-8601 UTC start of the fetch batch
  census/.raw            host \t curl_rc \t status \t effective_url \t content_type \t requested_url
  census/<host>.body     response body as received
  census/<host>.hdr      response header block (final response; redirect chain included)
Output: census/census.json
"""
import json
import os
import re
from datetime import datetime, timezone

BASE = os.path.dirname(os.path.abspath(__file__))
CEN = os.path.join(BASE, "census")

# Field names RFC 9116 names explicitly; anything else is recorded as an extension.
RFC9116_FIELDS = [
    "Contact", "Expires", "Encryption", "Acknowledgments",
    "Preferred-Languages", "Canonical", "Policy", "Hiring",
]
FIELD_LINE = re.compile(r"^([A-Za-z][A-Za-z0-9-]*):[ \t]*(.*)$")
ISO_IN = re.compile(
    r"^(\d{4})-(\d{2})-(\d{2})[Tt ](\d{2}):(\d{2}):(\d{2})(\.\d+)?([Zz]|[+-]\d{2}:?\d{2})$"
)


def parse_iso_utc(s):
    """Parse an RFC 3339 timestamp, tolerating lowercase z and .fff fractions."""
    s = s.strip()
    m = ISO_IN.match(s)
    if not m:
        return None, "unparsable"
    y, mo, d, h, mi, sec, frac, off = m.groups()
    try:
        dt = datetime(int(y), int(mo), int(d), int(h), int(mi), int(sec), tzinfo=timezone.utc)
    except ValueError:
        return None, "out-of-range"
    fmt_note = []
    if off in ("z", "Z"):
        if off == "z":
            fmt_note.append("lowercase-z")
    else:
        sign = 1 if off[0] == "+" else -1
        oh, om = off[1:].replace(":", "")[:2], off[1:].replace(":", "")[2:]
        dt = dt.replace(tzinfo=None).replace(tzinfo=timezone.utc)
        from datetime import timedelta
        dt = dt - sign * timedelta(hours=int(oh), minutes=int(om))
        fmt_note.append("offset:" + off)
    if frac and frac.strip(".") != "000":
        fmt_note.append("fraction" + frac)
    return dt, ",".join(fmt_note)


def split_fields(body):
    """Return (fields dict name -> [values], [lines skipped as armor/base64])."""
    text = body.replace("\r\n", "\n").replace("\r", "\n")
    fields = {}
    dropped = 0
    in_signature = False
    for raw in text.split("\n"):
        line = raw.rstrip()
        if line.startswith("-----BEGIN PGP SIGNATURE-----"):
            in_signature = True
            continue
        if in_signature:
            continue
        if line.startswith("-----BEGIN PGP SIGNED MESSAGE-----"):
            continue
        if line.startswith("Hash:") and not fields:
            continue  # clearsign armor header, not a security.txt field
        if not line or line.startswith("#"):
            continue
        m = FIELD_LINE.match(line)
        if m:
            fields.setdefault(m.group(1), []).append(m.group(2).strip())
        else:
            dropped += 1
    return fields, dropped


def read(path, mode="r"):
    with open(path, mode, **({} if "b" in mode else {"encoding": "utf-8", "errors": "replace"})) as f:
        return f.read()


def main():
    hosts = [l.strip() for l in read(os.path.join(CEN, ".hosts")).splitlines() if l.strip()]
    request_ts_raw = read(os.path.join(CEN, ".request_ts")).strip()
    request_ts, _ = parse_iso_utc(request_ts_raw)
    raw = {}
    for line in read(os.path.join(CEN, ".raw")).splitlines():
        if not line.strip():
            continue
        parts = line.split("\t")
        host, rc, status, eff, ctype = parts[0], parts[1], parts[2], parts[3], parts[4]
        raw[host] = {
            "curl_rc": int(rc),
            "status": int(status),
            "effective_url": eff,
            "content_type": ctype,
        }

    rows = []
    for host in hosts:
        body_path = os.path.join(CEN, host + ".body")
        body = read(body_path) if os.path.exists(body_path) else ""
        r = raw[host]
        fields, dropped = split_fields(body)
        signed = "-----BEGIN PGP SIGNED MESSAGE-----" in body
        expires_raw = (fields.get("Expires") or [None])[0]
        expires_utc = None
        expires_note = ""
        expires_in_days = None
        if expires_raw:
            expires_utc, expires_note = parse_iso_utc(expires_raw)
            if expires_utc and request_ts:
                expires_in_days = round(
                    (expires_utc - request_ts).total_seconds() / 86400.0, 3)
        canonical = (fields.get("Canonical") or [None])[0]
        served = r["status"] == 200 and bool(fields)
        missing_required = [] if not served else [
            f for f in ("Contact", "Expires") if not fields.get(f)]
        rows.append({
            "host": host,
            "requested_url": "https://%s/.well-known/security.txt" % host,
            "http_status": r["status"],
            "curl_rc": r["curl_rc"],
            "final_url": r["effective_url"],
            "content_type": r["content_type"],
            "bytes": len(body.encode("utf-8")),
            "served_security_txt": served,
            "signed_pgp": signed,
            "field_names": list(fields.keys()),
            "fields": fields,
            "unparsed_lines": dropped,
            "expires_present": expires_raw is not None,
            "expires_raw": expires_raw,
            "expires_utc": expires_utc.isoformat().replace("+00:00", "Z") if expires_utc else None,
            "expires_format_note": expires_note,
            "expires_in_days": expires_in_days,
            "expires_in_past": (expires_in_days is not None and expires_in_days < 0),
            "expires_more_than_365_days_ahead": (
                expires_in_days is not None and expires_in_days > 365),
            "canonical_present": canonical is not None,
            "canonical_value": canonical,
            "contact_count": len(fields.get("Contact", [])),
            "missing_required_fields": missing_required,
        })

    served_rows = [r for r in rows if r["served_security_txt"]]
    summary = {
        "hosts_probed": len(rows),
        "hosts_serving_security_txt": len(served_rows),
        "hosts_not_serving": [r["host"] for r in rows if not r["served_security_txt"]],
        "hosts_signed_pgp": [r["host"] for r in rows if r["signed_pgp"]],
        "hosts_expires_missing": [r["host"] for r in served_rows if not r["expires_present"]],
        "hosts_expires_more_than_365_days_ahead": [
            r["host"] for r in served_rows if r["expires_more_than_365_days_ahead"]],
        "hosts_expires_in_past": [
            r["host"] for r in served_rows if r["expires_in_past"]],
        "hosts_canonical_present": [r["host"] for r in served_rows if r["canonical_present"]],
        "hosts_missing_required_fields": {
            r["host"]: r["missing_required_fields"]
            for r in served_rows if r["missing_required_fields"]},
        "hosts_serving_with_all_required_fields": sum(
            1 for r in served_rows if not r["missing_required_fields"]),
        "counts": {
            "serving": len(served_rows),
            "expires_more_than_365_days_ahead": sum(
                1 for r in served_rows if r["expires_more_than_365_days_ahead"]),
            "signed_pgp": sum(1 for r in served_rows if r["signed_pgp"]),
        },
    }

    out = {
        "generated_by": "build_census.py",
        "request_ts": request_ts_raw,
        "probe": {
            "method": "GET",
            "redirects_followed": True,
            "max_redirects": 5,
            "user_agent": read(os.path.join(BASE, "fetch.sh")).split("UA=")[1].split("\n")[0].strip("'\""),
            "definition": ("served_security_txt = final HTTP status 200 AND at least one "
                           "RFC-9116-style 'Name: value' field parsed from the body; "
                           "expires_in_days measured against request_ts"),
        },
        "rfc9116_fields_checked": RFC9116_FIELDS,
        "rows": rows,
        "summary": summary,
    }
    dest = os.path.join(BASE, "census.json")
    with open(dest, "w", encoding="utf-8") as f:
        json.dump(out, f, indent=2, sort_keys=False)
        f.write("\n")
    print("wrote", dest, "rows", len(rows))
    print(json.dumps(summary["counts"], sort_keys=True))


if __name__ == "__main__":
    main()
