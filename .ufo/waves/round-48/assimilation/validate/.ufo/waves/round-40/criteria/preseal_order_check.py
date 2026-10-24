#!/usr/bin/env python3
"""QUALITY (o) amended, round 40: a counter is admitted only if non-author control receipts scored
with the same counter bytes are committed AT the declaration revision (i.e. before or with it).

Usage: preseal_order_check.py --root <lane> --revision <declaration rev> --counter <path in repo>
                              --receipts <dir in repo> [--author-prefix l1- --author-prefix base]
Exit 0: at <revision>, <receipts> holds >= 1 receipt whose counterSha256 equals the counter's bytes
        at <revision> and whose label does not start with an author prefix.
Exit 1: none.  Exit 2: cannot evaluate (counter absent at the revision, git failure).
Decides by committed bytes only: receipt files are read with `git show <rev>:<path>`.
"""
import argparse
import hashlib
import json
import subprocess
import sys


def git(root, *args):
    return subprocess.run(["git", "-C", root, *args], capture_output=True, check=True).stdout


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", required=True)
    ap.add_argument("--revision", required=True)
    ap.add_argument("--counter", required=True)
    ap.add_argument("--receipts", required=True)
    ap.add_argument("--author-prefix", action="append", default=None)
    a = ap.parse_args()
    prefixes = tuple(a.author_prefix or ["l1-", "base"])
    try:
        rev = git(a.root, "rev-parse", "--verify", a.revision + "^{commit}").decode().strip()
        counter_sha = hashlib.sha256(git(a.root, "show", f"{rev}:{a.counter}")).hexdigest()
    except subprocess.CalledProcessError as ex:
        print(json.dumps({"verdict": "cannot-evaluate", "why": str(ex)}))
        return 2
    try:
        names = git(a.root, "ls-tree", "-r", "--name-only", rev, "--", a.receipts).decode().split("\n")
    except subprocess.CalledProcessError:
        names = []
    independent, author, other = [], [], 0
    for name in filter(None, names):
        if not name.endswith(".json"):
            continue
        try:
            rec = json.loads(git(a.root, "show", f"{rev}:{name}"))
        except Exception:
            continue
        if not isinstance(rec, dict) or rec.get("counterSha256") != counter_sha:
            other += 1
            continue
        label = str(rec.get("label") or "")
        (author if label.startswith(prefixes) else independent).append(name)
    ok = bool(independent)
    print(json.dumps({"verdict": "pass" if ok else "fail", "revision": rev, "counterSha256": counter_sha,
                      "independentReceipts": len(independent), "authorReceipts": len(author),
                      "otherJson": other, "examples": independent[:3]}))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
