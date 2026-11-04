#!/usr/bin/env python3
"""Apply single-point mutants to the C2 candidate base and score each with the frozen counter."""
import json
import os
import subprocess
import sys

S = "/fast/scratch/hyaku/kake-r91/MutReuse"
LANE = "/home/vgpnk/Projects/shokunin/kake-shokunin"
COUNTER = os.path.join(LANE, ".ufo/waves/round-91/c91_reuse.py")
FX = os.path.join(S, "fx")
BASE = os.path.join(S, "base", "base.py")

MUTANTS = [
    ("M01", "clause 9: drop s-maxage",
     '    if shared and "s-maxage" in scc:',
     '    if False and shared and "s-maxage" in scc:'),
    ("M02", "clause 9: use s-maxage when not shared",
     '    if shared and "s-maxage" in scc:',
     '    if "s-maxage" in scc:'),
    ("M03", "clause 9: Expires before max-age",
     '    elif "max-age" in scc:',
     '    elif "max-age" in scc and expires is None:'),
    ("M04", "clause 10: drop private",
     '            or ("private" in scc and shared) or star):',
     '            or star):'),
    ("M05", "clause 10: drop Vary: *",
     '            or ("private" in scc and shared) or star):',
     '            or ("private" in scc and shared)):'),
    ("M06", "clause 10: drop request no-store",
     '            or "no-store" in scc or "no-store" in rcc',
     '            or "no-store" in scc'),
    ("M07", "clause 16: current_age < lifetime as <=",
     '    elif current_age < lifetime:',
     '    elif current_age <= lifetime:'),
    ("M08", "clause 12: drop request no-cache",
     '    elif "no-cache" in rcc:',
     '    elif False:'),
    ("M09", "clause 13: drop stored no-cache",
     '    elif "no-cache" in scc:',
     '    elif False:'),
    ("M10", "clause 17: drop must-revalidate",
     '    elif "must-revalidate" in scc or ("proxy-revalidate" in scc and shared):',
     '    elif "proxy-revalidate" in scc and shared:'),
    ("M11", "clause 17: drop proxy-revalidate",
     '    elif "must-revalidate" in scc or ("proxy-revalidate" in scc and shared):',
     '    elif "must-revalidate" in scc:'),
    ("M12", "clause 18: ignore the max-stale argument",
     '                                 or current_age - lifetime <= rcc["max-stale"]):',
     '                                 or True):'),
    ("M13", "clause 20: drop only-if-cached",
     '    if "only-if-cached" in rcc and decision not in ("reuse", "not-storable"):',
     '    if False:'),
    ("M14", "clause 10/21: report current_age on not-storable",
     '        return {"decision": "not-storable", "freshness_lifetime": None, "current_age": None}',
     '        return {"decision": "not-storable", "freshness_lifetime": None, "current_age": current_age}'),
    ("M15", "clause 9: clamp a negative lifetime to 0",
     '        lifetime = expires - date',
     '        lifetime = max(0, expires - date)'),
    ("M16", "clause 4: accept a quoted delta-seconds",
     '                if quoted:\n                    raise Invalid("quoted delta-seconds")',
     '                if False:\n                    raise Invalid("quoted delta-seconds")'),
    ("M17", "clause 1: accept duplicate header names",
     '        if lk in out:\n            raise Invalid("duplicate header name")',
     '        if False:\n            raise Invalid("duplicate header name")'),
]


def run(cmd, **kw):
    return subprocess.run(cmd, capture_output=True, text=True, **kw)


def main():
    base = open(BASE).read()
    revs = {}
    for mid, label, old, new in MUTANTS:
        src = base
        n = src.count(old)
        if n != 1:
            print("SKIP %s: pattern count %d" % (mid, n))
            continue
        src = src.replace(old, new)
        with open(os.path.join(FX, "scripts/stored_reuse.py"), "w") as fh:
            fh.write(src)
        r = run(["git", "-C", FX, "add", "scripts/stored_reuse.py"])
        assert r.returncode == 0, r.stderr
        r = run(["git", "-C", FX, "commit", "-q", "-m", "%s %s" % (mid, label)])
        assert r.returncode == 0, r.stderr
        revs[mid] = run(["git", "-C", FX, "rev-parse", "HEAD"]).stdout.strip()
        print(mid, revs[mid], label)
    # restore base bytes as the tip commit (mutants stay reachable by rev)
    with open(os.path.join(FX, "scripts/stored_reuse.py"), "w") as fh:
        fh.write(base)
    run(["git", "-C", FX, "add", "scripts/stored_reuse.py"])
    run(["git", "-C", FX, "commit", "-q", "-m", "M00 restore base"])
    json.dump(revs, open(os.path.join(S, "tool-revs.json"), "w"), indent=1, sort_keys=True)


if __name__ == "__main__":
    main()
