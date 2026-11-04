#!/usr/bin/env python3
"""ExecReuseTrial (kake r91 w1): run scripts/stored_reuse.py over converted inputs.

Two passes per input, both offline over the same recorded bytes:
  capture_time: now = epoch(fetchedAt) as converted
  aged_30d:     now = capture_time + 2592000 (declared 30-day shift, to
                exercise the stale branches on real data)
Captures rc / stdout / stderr verbatim per row into results.json. Reads the
tool from the lane working tree; writes only results.json in this directory.
"""

import json
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
TOOL = "/home/vgpnk/Projects/shokunin/kake-shokunin/scripts/stored_reuse.py"
AGED = 2592000  # 30 days


def run_tool(case):
    p = subprocess.run([sys.executable, "-B", TOOL],
                       input=json.dumps(case).encode(),
                       capture_output=True, timeout=60)
    return p.returncode, p.stdout.decode("utf-8", "replace"), \
        p.stderr.decode("utf-8", "replace")


def main():
    idx = json.load(open(os.path.join(HERE, "inputs", "index.json")))
    results = []
    for r in idx["rows"]:
        case = json.load(open(os.path.join(HERE, "inputs", r["input"])))
        row = {"input": r["input"], "url": r["url"],
               "recorded_status": r["recorded_status"],
               "converted_stored_headers": r["converted_stored_headers"]}
        for tag, delta in (("capture_time", 0), ("aged_30d", AGED)):
            c = dict(case)
            c["now"] = r["now_primary"] + delta
            rc, out, err = run_tool(c)
            if rc == 0:
                dec = json.loads(out)
                row[tag] = {"rc": 0, "decision": dec["decision"],
                            "freshness_lifetime": dec["freshness_lifetime"],
                            "current_age": dec["current_age"],
                            "now": c["now"]}
            else:
                row[tag] = {"rc": rc, "stderr": err.strip()[:200], "now": c["now"]}
        results.append(row)
        print("%-30s capture_time=%s aged_30d=%s" % (
            row["input"], row["capture_time"].get("decision", row["capture_time"]),
            row["aged_30d"].get("decision", row["aged_30d"])))
    with open(os.path.join(HERE, "results.json"), "w") as fh:
        json.dump(results, fh, indent=1, sort_keys=True)
    return 0


if __name__ == "__main__":
    sys.exit(main())
