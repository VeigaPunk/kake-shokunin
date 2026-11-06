#!/usr/bin/env python3
"""CriticClaims C2 violation probes: run oracle vs mutants on inputs OUTSIDE the
391 scored cases; a diverging pair is a contract clause violation that scored met=true."""
import json
import subprocess
import sys

CAND = "/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-100/w1/CriticClaims/candidates"

VT = "\x0b"  # vertical tab: neither SP nor HTAB

CASES = [
    # (probe name, candidate, stdin bytes, violated clause)
    ("v22-overtrim / V2-2 (only SP/HTAB trimmed; \\v kept byte-for-byte)",
     CAND + "/cand-v22-overtrim.py",
     json.dumps({"stored": [{"id": "a", "received": 1, "headers": {"X-V": VT + "TOP"}}],
                 "response": {"status": 304, "headers": {"Date": "D"}}}).encode(), "V2-2"),
    ("sandbox-conditional / V2-2 outside the counter sandbox",
     CAND + "/cand-sandbox-conditional.py",
     json.dumps({"stored": [{"id": "a", "received": 1, "headers": {"X-V": VT + "TOP"}}],
                 "response": {"status": 304, "headers": {"Date": "D"}}}).encode(), "V2-2"),
    ("e5-bom / e5 (stdin that is not valid JSON must be refused)",
     CAND + "/cand-e5-bom.py",
     b"\xef\xbb\xbf" + b'{"stored": [], "response": {"status": 304, "headers": {}}}', "e5"),
    ("v21a-eqempty / V2-1a (value that does not parse is refused)",
     CAND + "/cand-v21a-eqempty.py",
     json.dumps({"stored": [{"id": "a", "received": 1, "headers": {}}],
                 "response": {"status": 304, "headers": {"Cache-Control": "="}}}).encode(), "V2-1a"),
    ("v2e1-storedcc / V2-1 last line + e1 (stored Cache-Control copied as data)",
     CAND + "/cand-v2e1-storedcc.py",
     json.dumps({"stored": [{"id": "a", "received": 1, "headers": {"Cache-Control": 'no-cache="x"'}}],
                 "response": {"status": 304, "headers": {"Date": "D"}}}).encode(), "V2-1/e1"),
]

ORACLE = CAND + "/pos-oracle-repro.py"


def run(path, data):
    r = subprocess.run(["python3", "-I", "-B", path], input=data, capture_output=True, timeout=20)
    return r.returncode, r.stdout.decode("utf-8", "replace").strip(), r.stderr.decode("utf-8", "replace").strip()


for name, cand, data, clause in CASES:
    orc, oout, oerr = run(ORACLE, data)
    crc, cout, cerr = run(cand, data)
    div = "DIVERGES" if (orc, oout) != (crc, cout) else "same"
    print("probe %s" % name)
    print("  oracle rc=%d out=%s err=%s" % (orc, oout or "-", oerr[:60]))
    print("  cand  rc=%d out=%s err=%s" % (crc, cout or "-", cerr[:60]))
    print("  -> %s ; clause=%s" % (div, clause))
