#!/usr/bin/env python3
"""Same 17 single-point mutants, applied to the shipped scripts/stored_reuse.py bytes."""
import json
import os
import subprocess

S = "/fast/scratch/hyaku/kake-r91/MutReuse"
FX = os.path.join(S, "fx")
BASE = os.path.join(S, "base", "shipped.py")

MUTANTS = [
    ("M01", "clause 9: drop s-maxage",
     '    if shared and "s-maxage" in stored_cc:',
     '    if False and shared and "s-maxage" in stored_cc:'),
    ("M02", "clause 9: use s-maxage when not shared",
     '    if shared and "s-maxage" in stored_cc:',
     '    if "s-maxage" in stored_cc:'),
    ("M03", "clause 9: Expires before max-age",
     '    elif "max-age" in stored_cc:',
     '    elif "max-age" in stored_cc and expires_value is None:'),
    ("M04", "clause 10: drop private",
     '                and not ("private" in stored_cc and shared)',
     '                and not False'),
    ("M05", "clause 10: drop Vary: *",
     '                and not vary_star)',
     '                and not False)'),
    ("M06", "clause 10: drop request no-store",
     '                and "no-store" not in request_cc\n',
     ''),
    ("M07", "clause 16: current_age < lifetime as <=",
     '    elif current_age < lifetime:',
     '    elif current_age <= lifetime:'),
    ("M08", "clause 12: drop request no-cache",
     '    elif "no-cache" in request_cc:',
     '    elif False:'),
    ("M09", "clause 13: drop stored no-cache",
     '    elif "no-cache" in stored_cc:',
     '    elif False:'),
    ("M10", "clause 17: drop must-revalidate",
     '    elif "must-revalidate" in stored_cc or ("proxy-revalidate" in stored_cc and shared):',
     '    elif "proxy-revalidate" in stored_cc and shared:'),
    ("M11", "clause 17: drop proxy-revalidate",
     '    elif "must-revalidate" in stored_cc or ("proxy-revalidate" in stored_cc and shared):',
     '    elif "must-revalidate" in stored_cc:'),
    ("M12", "clause 18: ignore the max-stale argument",
     '               or current_age - lifetime <= request_cc["max-stale"])):',
     '               or True)):'),
    ("M13", "clause 20: drop only-if-cached",
     '    if "only-if-cached" in request_cc and decision not in ("reuse", "not-storable"):',
     '    if False:'),
    ("M14", "clause 10/21: report current_age on not-storable",
     '        return {"decision": "not-storable", "freshness_lifetime": None,\n                "current_age": None}',
     '        return {"decision": "not-storable", "freshness_lifetime": None,\n                "current_age": current_age}'),
    ("M15", "clause 9: clamp a negative lifetime to 0",
     '        lifetime = expires_value - date_value',
     '        lifetime = max(0, expires_value - date_value)'),
    ("M16", "clause 4: accept a quoted delta-seconds",
     '                if quoted:\n                    raise InvalidInput("quoted delta-seconds argument: %s" % name)',
     '                if False:\n                    raise InvalidInput("quoted delta-seconds argument: %s" % name)'),
    ("M17", "clause 1: accept duplicate header names",
     '        if key in out:\n            raise InvalidInput("duplicate header name: %s" % name)',
     '        if False:\n            raise InvalidInput("duplicate header name: %s" % name)'),
]


def run(cmd):
    return subprocess.run(cmd, capture_output=True, text=True)


base = open(BASE).read()
revs = {}
for mid, label, old, new in MUTANTS:
    n = base.count(old)
    if n != 1:
        print("SKIP %s: pattern count %d" % (mid, n))
        continue
    with open(os.path.join(FX, "scripts/stored_reuse.py"), "w") as fh:
        fh.write(base.replace(old, new))
    assert run(["git", "-C", FX, "add", "scripts/stored_reuse.py"]).returncode == 0
    r = run(["git", "-C", FX, "commit", "-q", "-m", "%s %s" % (mid, label)])
    assert r.returncode == 0, r.stderr
    revs[mid] = run(["git", "-C", FX, "rev-parse", "HEAD"]).stdout.strip()
    print(mid, revs[mid], label)
with open(os.path.join(FX, "scripts/stored_reuse.py"), "w") as fh:
    fh.write(base)
run(["git", "-C", FX, "add", "scripts/stored_reuse.py"])
run(["git", "-C", FX, "commit", "-q", "-m", "M00s restore shipped bytes"])
json.dump(revs, open(os.path.join(S, "tool-revs-shipped.json"), "w"), indent=1, sort_keys=True)
