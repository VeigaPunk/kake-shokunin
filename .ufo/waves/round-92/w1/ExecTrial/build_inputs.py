#!/usr/bin/env python3
"""ExecTrial-6 (kake round 92 w1): build c2-contract inputs from recorded captures.

Reads each recorded GET response (response.json) under the round-61/81/82
capture trees and emits exactly the JSON object the C2 contract
(.ufo/waves/round-92/c2-contract.md) accepts on stdin:

    {"stored": {"status": <int>, "headers": {...}}, "now": <int>}

Rules (seat spec):
- Only the contract-deciding fields are carried: Date, Last-Modified,
  Expires, Cache-Control, Vary -- when present in the recording; a field the
  recording lacks is reported absent and never invented.
- HTTP-date values (Date, Last-Modified, Expires) are converted to epoch
  seconds and emitted as decimal-integer STRINGS ("1793092555"): the
  contract's clause 3 requires every header value to be a string, and its
  clause 5 requires the Date value to be "a decimal integer in epoch
  seconds" -- i.e. a string whose content is a decimal integer (the lane's
  adapter convention, the same one scripts/cache_current_age.py and
  scripts/stored_reuse.py use; no HTTP-date parsing). The recorded HTTP-date
  is retained verbatim in inputs.index.json.
- Cache-Control and Vary values are passed byte-exact as recorded (the
  contract's clause 2 does its own SP/HTAB trimming).
- Repeated field lines (recorded HTTP allows repeated names, the contract's
  JSON header object does not) are combined per RFC 9110 section 5.2 field
  combination with ", ". Every combination is reported in inputs.index.json.
- `now` is the recorded fetchedAt instant in epoch seconds.
- `shared` is omitted (contract default: false).
"""
import email.utils
import hashlib
import json
import os
import sys
from datetime import datetime, timezone

LANE = "/home/vgpnk/Projects/shokunin/kake-shokunin"
CAPS = [
    ("r61", ".ufo/waves/round-61/capture"),
    ("r81", ".ufo/waves/round-81/capture"),
    ("r82", ".ufo/waves/round-82/capture"),
]
TRACKED = ["date", "last-modified", "expires", "cache-control", "vary"]
HTTPDATE = {"date", "last-modified", "expires"}


def epoch_of_httpdate(value):
    dt = email.utils.parsedate_to_datetime(value)
    if dt is None:
        raise ValueError("unparseable HTTP-date: %r" % (value,))
    if dt.tzinfo is None:
        raise ValueError("HTTP-date without zone: %r" % (value,))
    return int(dt.timestamp())


def epoch_of_iso(value):
    dt = datetime.strptime(value, "%Y-%m-%dT%H:%M:%SZ").replace(tzinfo=timezone.utc)
    return int(dt.timestamp())


def main():
    seat = os.path.join(LANE, ".ufo/waves/round-92/w1/ExecTrial")
    indir = os.path.join(seat, "inputs")
    os.makedirs(indir, exist_ok=True)
    index = []
    for tag, rel in CAPS:
        root = os.path.join(LANE, rel)
        for d in sorted(os.listdir(root)):
            rpath = os.path.join(root, d, "response.json")
            if not os.path.isfile(rpath):
                continue
            raw = open(rpath, "rb").read()
            j = json.loads(raw)
            lows = {}
            for h in j.get("headers", []):
                lows.setdefault(h["name"].lower(), []).append(h["value"])
            headers, combined = {}, []
            absent = [k for k in TRACKED if k not in lows]
            for k in TRACKED:
                if k not in lows:
                    continue
                vals = lows[k]
                if len(vals) > 1:
                    combined.append({"name": k, "values": vals})
                value = ", ".join(vals)  # RFC 9110 section 5.2 field combination
                if k in HTTPDATE:
                    headers[k] = str(epoch_of_httpdate(value))  # clause 3: value is a string; clause 5/6/7: decimal-integer content
                else:
                    headers[k] = value
            name = "%s-%s" % (tag, d)
            payload = {
                "stored": {"status": int(j["status"]), "headers": headers},
                "now": epoch_of_iso(j["fetchedAt"]),
            }
            with open(os.path.join(indir, name + ".json"), "w") as f:
                json.dump(payload, f, sort_keys=True)
                f.write("\n")
            index.append({
                "surface": name,
                "capture": "%s/%s/response.json" % (rel, d),
                "response_sha256": hashlib.sha256(raw).hexdigest(),
                "status": j["status"],
                "fetchedAt": j["fetchedAt"],
                "url": j.get("finalUrl") or j.get("url"),
                "recorded_tracked": {k: lows[k] for k in TRACKED if k in lows},
                "absent_tracked": absent,
                "combined_field_lines": combined,
                "epoch": {k: headers[k] for k in headers if k in HTTPDATE},
                "now": payload["now"],
            })
    with open(os.path.join(seat, "inputs.index.json"), "w") as f:
        json.dump(index, f, indent=1, sort_keys=True)
        f.write("\n")
    print("inputs=%d" % len(index))
    for row in index:
        print(row["surface"], row["status"], row["now"],
              "absent=%s" % (row["absent_tracked"] or "-"),
              "combined=%s" % (",".join(c["name"] for c in row["combined_field_lines"]) or "-"))
    return 0


if __name__ == "__main__":
    sys.exit(main())
