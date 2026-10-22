#!/usr/bin/env python3
"""Independently recompute the census table + summary counts from the saved
bodies and status lines, then diff against census/census.json.

No network. One command reproduces every number in the report:
    python3 -B /fast/scratch/hyaku/kake-r35/w1/ScoutSecurityTxtCensus/summarize.py
Exit 0 = recomputation matches census.json, 1 = mismatch or missing input.
"""
import json
import os
import re
import sys
from datetime import datetime, timezone

BASE = os.path.dirname(os.path.abspath(__file__))
CEN = os.path.join(BASE, "census")
FIELD = re.compile(r"^([A-Za-z][A-Za-z0-9-]*):[ \t]*(.*)$")
STAMP = re.compile(
    r"^(\d{4})-(\d{2})-(\d{2})[Tt](\d{2}):(\d{2}):(\d{2})(?:\.\d+)?(?:[Zz]|\+00:?00)$")

REQUIRED = ["Contact", "Expires"]


def fields_of(body):
    out = {}
    signed = False
    stop = False
    for raw in body.replace("\r\n", "\n").split("\n"):
        line = raw.rstrip()
        if line.startswith("-----BEGIN PGP SIGNED MESSAGE-----"):
            signed = True
            continue
        if line.startswith("-----BEGIN PGP SIGNATURE-----"):
            stop = True
            continue
        if stop or not line or line.startswith("#") or line.startswith("Hash:"):
            continue
        m = FIELD.match(line)
        if m:
            out.setdefault(m.group(1), []).append(m.group(2).strip())
    return out, signed


def stamp(s):
    m = STAMP.match(s.strip())
    if not m:
        return None
    y, mo, d, h, mi, sec = (int(x) for x in m.groups())
    try:
        return datetime(y, mo, d, h, mi, sec, tzinfo=timezone.utc)
    except ValueError:
        return None


def main():
    with open(os.path.join(BASE, "census.json"), encoding="utf-8") as f:
        doc = json.load(f)
    host_rows = {r["host"]: r for r in doc["rows"]}
    req = stamp(doc["request_ts"])
    if req is None:
        print("FAIL: census.json request_ts not a UTC stamp:", doc["request_ts"])
        return 1

    status = {}
    for line in open(os.path.join(CEN, ".raw"), encoding="utf-8"):
        if line.strip():
            p = line.rstrip("\n").split("\t")
            status[p[0]] = int(p[2])

    served, gt365, signed_list, rows, problems, observations = [], [], [], [], [], []
    for host in sorted(status):
        body_path = os.path.join(CEN, host + ".body")
        body = open(body_path, encoding="utf-8", errors="replace").read() \
            if os.path.exists(body_path) else ""
        fl, signed = fields_of(body)
        is_served = status[host] == 200 and bool(fl)
        exp_raw = (fl.get("Expires") or [None])[0]
        days = None
        if exp_raw:
            dt = stamp(exp_raw)
            days = round((dt - req).total_seconds() / 86400.0, 3) if dt else None
        row = host_rows.get(host)
        if row is None:
            problems.append("host %s missing from census.json" % host)
            continue
        for k, v in (("http_status", status[host]),
                     ("served_security_txt", is_served),
                     ("signed_pgp", signed),
                     ("expires_present", exp_raw is not None),
                     ("expires_in_days", days),
                     ("expires_more_than_365_days_ahead", days is not None and days > 365)):
            if row[k] != v:
                problems.append("%s: census.json %s=%r vs recomputed %r" % (host, k, row[k], v))
        rows.append((host, status[host], "yes" if is_served else "no",
                     "yes" if signed else "no",
                     "yes" if "Canonical" in fl else "no",
                     exp_raw or "-",
                     "-" if days is None else "%+.1f" % days,
                     "yes" if (days is not None) else "n/a",
                     len(fl.get("Contact", []))))
        if is_served:
            served.append(host)
            if days is not None and days > 365:
                gt365.append(host)
            if signed:
                signed_list.append(host)
        missing = [f for f in REQUIRED if not fl.get(f)]
        if is_served and missing:
            observations.append("%s: served but missing required %s" % (host, missing))

    hdr = ("host", "status", "served", "pgp", "canon", "Expires", "days",
           ">365d", "contacts")
    rows = [tuple(str(c) for c in r) for r in rows]
    widths = [max([len(hdr[i])] + [len(r[i]) for r in rows]) for i in range(len(hdr))]
    print("  ".join(h.ljust(widths[i]) for i, h in enumerate(hdr)))
    print("  ".join("-" * w for w in widths))
    for r in rows:
        print("  ".join(str(r[i]).ljust(widths[i]) for i in range(len(hdr))))
    print()
    print("hosts probed                     : %d" % len(rows))
    print("hosts serving a security.txt     : %d  %s" % (len(served), " ".join(sorted(served))))
    print("hosts not serving                : %d  %s"
          % (len(rows) - len(served), " ".join(sorted(set(status) - set(served)))))
    print("Expires more than 365 days ahead : %d  %s" % (len(gt365), " ".join(sorted(gt365))))
    print("PGP signed                       : %d  %s" % (len(signed_list), " ".join(sorted(signed_list))))
    c = doc["summary"]["counts"]
    print("census.json summary counts       : %s" % json.dumps(c, sort_keys=True))
    for label, mine, theirs in (
            ("serving", len(served), c["serving"]),
            ("expires_more_than_365_days_ahead", len(gt365), c["expires_more_than_365_days_ahead"]),
            ("signed_pgp", len(signed_list), c["signed_pgp"])):
        if mine != theirs:
            problems.append("summary %s: census.json %d vs recomputed %d" % (label, theirs, mine))
    print("\nhosts with a required field missing : %d  %s"
          % (len(observations), "; ".join(observations) if observations else "-"))
    if problems:
        print("\nMISMATCHES:")
        for p in problems:
            print(" -", p)
        return 1
    print("\nOK: row fields and summary counts reproduce from saved bodies + .raw statuses")
    return 0


if __name__ == "__main__":
    sys.exit(main())
