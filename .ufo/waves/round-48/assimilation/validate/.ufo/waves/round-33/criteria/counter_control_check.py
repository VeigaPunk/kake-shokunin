#!/usr/bin/env python3
"""Criterion check: a row/path/citation counter must not score its declared after-value on a hollow commit.

Usage: python3 -B check_counter_control.py --counter <counter.py> --repo <repo> --before <rev>
                                               --after <rev> --hollow <rev>

The hollow revision is one whose claimed repair is faked: the retained bytes sit at
unrelated paths, the registry row is fabricated (wrong id), and the entry mentions that
fabricated id. A counter that pins identity (row id, declared path, mode, cited section)
must score the hollow revision below its after-value.

Exit 0 = counter discriminates (hollow < after, before < after).
Exit 1 = criterion fails: hollow scores the after-value (or after is not reached).
"""
import argparse
import json
import subprocess
import sys


def run(counter, repo, rev):
    p = subprocess.run([sys.executable, "-B", counter, "--rev", rev, "--repo", repo],
                       capture_output=True, text=True)
    try:
        out = json.loads(p.stdout)
    except json.JSONDecodeError:
        return None, p
    return out, p


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--counter", required=True)
    ap.add_argument("--repo", required=True)
    ap.add_argument("--before", required=True)
    ap.add_argument("--after", required=True)
    ap.add_argument("--hollow", required=True)
    a = ap.parse_args()
    res = {}
    for name, rev in (("before", a.before), ("after", a.after), ("hollow", a.hollow)):
        out, p = run(a.counter, a.repo, rev)
        if out is None:
            print("FATAL: counter gave no JSON for %s (%s) exit=%d" % (name, rev[:12], p.returncode))
            return 1
        res[name] = out
        print("%-6s %s -> met=%s exit=%d" % (name, rev[:12], out.get("met"), p.returncode))
    after, hollow, before = res["after"].get("met"), res["hollow"].get("met"), res["before"].get("met")
    ok = isinstance(after, int) and isinstance(hollow, int) and isinstance(before, int) \
        and hollow < after and before < after
    print("after=%s before=%s hollow=%s" % (after, before, hollow))
    if ok:
        print("PASS: hollow scores below the after-value; the counter pins identity")
        return 0
    print("FAIL: hollow commit scores the declared after-value %s (hollow=%s, before=%s) "
          "- the counter does not pin row id, path, mode or cited section" % (after, hollow, before))
    print("hollow detail: " + json.dumps({k: res["hollow"].get(k) for k in
                                           ("c1BlobPaths", "c2RowIds", "c3Cites")}))
    return 1


if __name__ == "__main__":
    sys.exit(main())
