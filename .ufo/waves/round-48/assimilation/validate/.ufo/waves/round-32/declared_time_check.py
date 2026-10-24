#!/usr/bin/env python3
"""Round-32 QUALITY check: a stated declaration time must not be later than the declaring commit.

Usage: python3 -B declared_time_check.py --rev <declaring commit> --section "<SCORECARD heading text>"
Finds "Declared at HH:MMZ" inside that SCORECARD.md section at <rev>, compares it with the
commit time of <rev> (UTC, same date). Exit 0 ok, 1 violation, 2 no stated time / bad input.
"""
import argparse, datetime as dt, re, subprocess, sys
ap = argparse.ArgumentParser(); ap.add_argument("--rev", required=True); ap.add_argument("--section", required=True)
ap.add_argument("--repo", default="/home/vgpnk/Projects/shokunin/kake-shokunin"); a = ap.parse_args()
g = lambda *x: subprocess.run(["git", "-C", a.repo, *x], capture_output=True, text=True)
text = g("show", a.rev + ":SCORECARD.md").stdout
part = text.split("## " + a.section, 1)
if len(part) < 2: print("no section"); sys.exit(2)
m = re.search(r"Declared at (\d\d):(\d\d)Z", part[1].split("\n## ", 1)[0])
if not m: print("no stated time"); sys.exit(2)
ct = dt.datetime.fromisoformat(g("show", "-s", "--format=%cI", a.rev).stdout.strip()).astimezone(dt.timezone.utc)
stated = ct.replace(hour=int(m.group(1)), minute=int(m.group(2)), second=0)
print("stated %s commit %s" % (stated.isoformat(), ct.isoformat()))
if stated > ct: print("violation: stated declaration time is later than the declaring commit"); sys.exit(1)
print("ok"); sys.exit(0)
