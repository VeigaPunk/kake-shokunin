#!/usr/bin/env python3
"""Verify each errata entry's path+commit resolves at the round-61 base revision."""
import json
import subprocess

ROOT = "/fast/scratch/hyaku/kake-r61/ExecC1Disclose/lane"
BASE = "9f07731a873585e655a6518233ea39f5d9fb8204"
ERRATA = "/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-57/receipt-errata.json"


def git(*a, check=True):
    p = subprocess.run(["git", "-C", ROOT, *a], capture_output=True, text=True)
    if check and p.returncode != 0:
        raise RuntimeError(p.stderr.strip())
    return p


def blob(rev, path):
    p = git("cat-file", "-e", f"{rev}:{path}", check=False)
    return git("cat-file", "blob", f"{rev}:{path}").stdout if p.returncode == 0 else None


err = json.load(open(ERRATA))
rows = []
for e in err["entries"]:
    c, path = e["commit"], e["path"]
    t = git("cat-file", "-t", c, check=False)
    anc = git("merge-base", "--is-ancestor", c, BASE, check=False).returncode == 0
    child = blob(c, path)
    parent = blob(c + "^", path)
    row = {
        "path": path,
        "commit": c,
        "type": t.stdout.strip() if t.returncode == 0 else "MISSING",
        "ancestor_of_base": anc,
        "path_in_commit": child is not None,
        "path_in_parent": parent is not None,
        "blob_differs": child is not None and parent is not None and child != parent,
        "from_in_parent": parent is not None and e["from"] in parent,
        "to_in_child": child is not None and e["to"] in child,
        "from_absent_in_child": child is not None and e["from"] not in child,
    }
    rows.append(row)

print(json.dumps({"base": BASE, "checked": len(rows), "rows": rows}, indent=2))
print("\nALL_OK:", all(all(v for k, v in r.items() if k not in ("path", "commit", "type")) and r["type"] == "commit" for r in rows))
