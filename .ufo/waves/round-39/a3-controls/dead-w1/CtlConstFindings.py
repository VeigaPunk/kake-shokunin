#!/usr/bin/env python3
"""Round-39 C1 control: constant findings (key-blind).

Control class "constant output / all findings". The tool pretends to audit sitemap
files but never opens one: it reads the manifest and nothing else, then answers
EVERY check with the SAME single finding, so the file-level result is constant
whatever the file contains.

  python3 control.py --manifest <path>

Output shape follows c1-contract.md sentence 33: one JSON object
{"version":1,"verdict":V,"checks":[...]} with one item per manifest check in
manifest order, each {"id","status","error","findings"} and findings as
{"code","entry"} pairs. Sentence 34's verdict for this constant is
"failed-policy" (there is a finding) with exit 1.

Deliberately skipped -- the claimed work, i.e. every rule (a)-(k) of
.ufo/waves/round-39/c1-contract.md: encoding, well-formedness, doctype, root,
entries, entry children, size/entry limits, loc form and scope, lastmod,
changefreq, priority. No sitemap file is opened, stat'ed or sniffed, and the
manifest-level input_invalid / check_invalid branches are not implemented either
(that is a different control class), so the document is constant for any manifest.
"""
import json
import sys

# The one constant finding every check receives.
CONST_CODE = "encoding_invalid"
CONST_ENTRY = None


def main(argv):
    if len(argv) != 2 or argv[0] != "--manifest":
        sys.exit(64)  # usage error: stdout ignored (contract sentence 2)
    try:
        with open(argv[1], "rb") as fh:
            man = json.loads(fh.read().decode("utf-8"))
    except Exception:
        man = None
    checks = []
    if isinstance(man, dict) and isinstance(man.get("checks"), list):
        for c in man["checks"]:
            checks.append(c.get("id") if isinstance(c, dict) and isinstance(c.get("id"), str) else None)
    items = [{"id": cid, "status": "findings", "error": None,
              "findings": [{"code": CONST_CODE, "entry": CONST_ENTRY}]} for cid in checks]
    sys.stdout.write(json.dumps({"version": 1, "verdict": "failed-policy", "checks": items},
                                separators=(",", ":")) + "\n")
    sys.stdout.flush()
    sys.exit(1)


if __name__ == "__main__":
    main(sys.argv[1:])
