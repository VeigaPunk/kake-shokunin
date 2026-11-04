#!/usr/bin/env python3
"""ExecSeatRecord scratch: write round-80 results with the results array reversed."""
import json
import pathlib

S = pathlib.Path("/fast/scratch/hyaku/kake-r81/ExecSeatRecord")
src = pathlib.Path("/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-80/w1-results.json")
doc = json.loads(src.read_text(encoding="utf-8"))
doc["results"] = list(reversed(doc["results"]))
out = S / "cases" / "r80-reordered.json"
out.write_text(json.dumps(doc, indent=1) + "\n", encoding="utf-8")
print("reordered rows:", len(doc["results"]), "first:", doc["results"][0]["name"], "last:", doc["results"][-1]["name"])
