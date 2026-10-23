#!/usr/bin/env python3
"""Round-41 pre-data check: the counter's oracle (abnf 2.9.1, RFC 3986 `URI`) against a second
published implementation (rfc3987 1.3.8, regular expressions for RFC 3986 `URI`) on the counter's
own generated cases. No tool is run. Usage: oracle_crosscheck.py --seeds 41001,41002,... --out <json>"""
import argparse
import hashlib
import importlib.util
import json
import os
import random
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
SECOND = os.path.join(HERE, "oracle", "rfc3987-1.3.8-py2.py3-none-any.whl")
SECOND_SHA256 = "10702b1e51e5658843460b189b185c0366d2cf4cff716f13111b0ea9fd2dce53"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--seeds", required=True)
    ap.add_argument("--out", required=True)
    a = ap.parse_args()
    if hashlib.sha256(open(SECOND, "rb").read()).hexdigest() != SECOND_SHA256:
        sys.exit("second oracle sha256 mismatch")
    spec = importlib.util.spec_from_file_location("c1_count", os.path.join(HERE, "c1_count.py"))
    cc = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(cc)
    valid = cc.load_oracle()
    sys.path.insert(0, SECOND)
    import rfc3987

    def second(value):
        if rfc3987.match(value, rule="URI") is None:
            return False
        parts = rfc3987.parse(value, rule="URI")
        if (parts.get("scheme") or "").lower() not in ("http", "https"):
            return False
        auth = parts.get("authority")
        if auth is None:
            return False
        hostport = auth.rpartition("@")[2]
        if hostport.startswith("["):
            host = hostport[: hostport.find("]") + 1]
        else:
            host = hostport.partition(":")[0]
        return host != ""

    rows = []
    for seed in [int(s) for s in a.seeds.split(",")]:
        cases = cc.generate(random.Random(seed), valid)
        dis = [c for c in cases if second(c["value"]) != c["valid"]]
        rows.append({"seed": seed, "cases": len(cases), "abnfInvalid": sum(not c["valid"] for c in cases),
                     "disagree": len(dis), "examples": [{"value": c["value"], "abnf": c["valid"]} for c in dis[:20]]})
    out = {"counterSha256": hashlib.sha256(open(os.path.join(HERE, "c1_count.py"), "rb").read()).hexdigest(),
           "secondOracleSha256": SECOND_SHA256, "rows": rows,
           "totalCases": sum(r["cases"] for r in rows), "totalDisagree": sum(r["disagree"] for r in rows)}
    with open(a.out, "w") as fh:
        json.dump(out, fh, indent=1)
        fh.write("\n")
    print(json.dumps({k: out[k] for k in ("totalCases", "totalDisagree")}))
    sys.exit(0 if out["totalDisagree"] == 0 else 1)


if __name__ == "__main__":
    main()
