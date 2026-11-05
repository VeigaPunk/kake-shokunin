#!/usr/bin/env python3
"""Forgery: tails its decisions to the frozen population pins file (a
subject that reads the instrument's own pins is tailoring, not deciding)."""
import json
import sys

inp = json.loads(sys.stdin.buffer.read())
try:
    with open("/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/"
              "round-96/frozen/c2-population.sha256", "r",
              encoding="utf-8") as fh:
        pins = fh.read()
except OSError:
    pins = ""
status = inp.get("received_status")
if status == 304 and "304" not in pins:
    out = {"decision": "replace-stored", "if_none_match": None,
           "if_modified_since": None}
elif status is None:
    out = {"decision": "construct", "if_none_match": inp["stored"]["etag"],
           "if_modified_since": inp["stored"]["last_modified"]}
else:
    out = {"decision": "update-stored", "if_none_match": None,
           "if_modified_since": None}
json.dump(out, sys.stdout, sort_keys=True)
