#!/usr/bin/env python3
"""ExecReuseTrial (kake r91 w1): recorded captures -> c2-contract input JSON.

Adapter convention (declared in ExecReuseTrial.md):
- The recorded header list (wire order, duplicates preserved) is folded into the
  contract's header MAP: names kept exactly as recorded. When the same name
  string repeats, the first occurrence wins and a note is emitted. Names that
  differ only in ASCII case are NOT folded -- the contract refuses those
  (clause 1), so such a record stays a refusal row.
- Only five cache-relevant fields are mapped, by ASCII-case-insensitive name:
    recorded `date`          -> "Date":  HTTP-date parsed with
                                email.utils.parsedate_to_datetime (naive =>
                                UTC), emitted as integer epoch seconds (string)
    recorded `expires`       -> "Expires": same conversion
    recorded `age`           -> "Age": recorded value verbatim
    recorded `cache-control` -> "Cache-Control": recorded value verbatim
    recorded `vary`          -> "Vary": recorded value verbatim
  Every other recorded field line is dropped: the contract has no clause for it.
- request: {"method": <recorded method>, "headers": {}} (no request headers
  were recorded by the captures).
- shared: false (the contract default; a recorded capture does not disclose
  the cache mode it was observed from).
- now: epoch seconds of the record's `fetchedAt` (UTC ISO-8601). A second,
  aged pass re-runs the same input with now + 2592000 (30 days) to exercise
  the stale branches; this is declared, not invented data.
- round-23/live records carry no header list at all (status+digest only), so
  they are listed as not convertible rather than given invented headers.

Reads only committed bytes under LANE/.ufo/waves; writes only inputs/ below
this script's directory. No network, no tool run.
"""

import hashlib
import json
import os
import sys
from datetime import datetime, timezone
from email.utils import parsedate_to_datetime

ROOT = "/home/vgpnk/Projects/shokunin/kake-shokunin"
OUT = os.path.join(os.path.dirname(os.path.abspath(__file__)), "inputs")
AGED_DELTA = 2592000  # 30 days, secondary pass

TREES = [
    ("round-61", ".ufo/waves/round-61/capture"),
    ("round-81", ".ufo/waves/round-81/capture"),
    ("round-82", ".ufo/waves/round-82/capture"),
]

CACHE_FIELDS = ("date", "age", "expires", "cache-control", "vary")


def ascii_lower(s):
    return "".join(chr(ord(c) + 32) if "A" <= c <= "Z" else c for c in s)


def http_date_epoch(v):
    dt = parsedate_to_datetime(v)
    if dt.tzinfo is None:
        dt = dt.replace(tzinfo=timezone.utc)
    return int(dt.timestamp())


def iso_epoch(s):
    dt = datetime.strptime(s, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc)
    return int(dt.timestamp())


def main():
    rows = []
    for tag, tree in TREES:
        base = os.path.join(ROOT, tree)
        ids = sorted(d for d in os.listdir(base)
                     if os.path.isdir(os.path.join(base, d)))
        for sid in ids:
            rec = json.load(open(os.path.join(base, sid, "response.json")))
            headers = [(h["name"], h["value"]) for h in rec["headers"]]
            hmap = {}
            repeated = []
            for n, v in headers:
                if n in hmap:
                    repeated.append(n)
                    continue
                hmap[n] = v
            picked = {}
            for n, v in hmap.items():
                lf = ascii_lower(n)
                if lf in CACHE_FIELDS:
                    picked[lf] = v
            notes = []
            obj_headers = {}
            for dst, src in (("Date", "date"), ("Age", "age"),
                             ("Expires", "expires"),
                             ("Cache-Control", "cache-control"),
                             ("Vary", "vary")):
                raw = picked.get(src)
                if raw is None:
                    continue
                if dst in ("Date", "Expires"):
                    try:
                        obj_headers[dst] = str(http_date_epoch(raw))
                    except Exception as exc:
                        notes.append("%s-unparseable(%s)" % (dst, exc))
                else:
                    obj_headers[dst] = raw
            fetched = iso_epoch(rec["fetchedAt"])
            if repeated:
                detail = "; ".join(
                    "%s: kept %r, dropped %s" % (
                        n, hmap[n],
                        " | ".join(repr(v) for k, v in headers
                                   if k == n and v != hmap[n]) or "(identical)")
                    for n in sorted(set(repeated)))
                notes.append("repeated-names-first-wins {" + detail + "}")
            case = {
                "stored": {"status": rec["status"], "headers": obj_headers},
                "request": {"method": rec.get("method", "GET"), "headers": {}},
                "now": fetched,
                "shared": False,
            }
            rel = os.path.join(tag, sid + ".json")
            path = os.path.join(OUT, rel)
            os.makedirs(os.path.dirname(path), exist_ok=True)
            blob = (json.dumps(case, sort_keys=True) + "\n").encode()
            open(path, "wb").write(blob)
            rows.append({
                "input": rel,
                "sha256": hashlib.sha256(blob).hexdigest(),
                "source_record": tree + "/" + sid + "/response.json",
                "url": rec.get("finalUrl") or rec.get("url"),
                "recorded_status": rec["status"],
                "fetchedAt": rec["fetchedAt"],
                "now_primary": fetched,
                "now_aged": fetched + AGED_DELTA,
                "recorded_cache_fields": {k: picked.get(k) for k in CACHE_FIELDS},
                "converted_stored_headers": obj_headers,
                "notes": notes,
            })
    # round-23/live: recorded with receipts but no header list
    r23 = []
    live = os.path.join(ROOT, ".ufo/waves/round-23/live")
    for sid in sorted(os.listdir(live)):
        fj = os.path.join(live, sid, "fetch.json")
        if os.path.isfile(fj):
            rec = json.load(open(fj))
            r23.append({"surface": sid, "url": rec.get("finalUrl") or rec.get("url"),
                        "recorded_status": rec.get("status"),
                        "fetchedAt": rec.get("fetchedAt"),
                        "headers_recorded": False})
    with open(os.path.join(OUT, "index.json"), "w") as fh:
        json.dump({"rows": rows, "round23_live_not_convertible": r23},
                  fh, indent=1, sort_keys=True)
    print("converted inputs:", len(rows))
    for r in rows:
        print("%-28s %-42s status=%s hdrs=%s%s" % (
            r["input"], r["url"], r["recorded_status"],
            sorted(r["converted_stored_headers"]),
            " notes=" + ";".join(r["notes"]) if r["notes"] else ""))
    print("round-23/live surfaces without header lists:", len(r23))
    return 0


if __name__ == "__main__":
    sys.exit(main())
