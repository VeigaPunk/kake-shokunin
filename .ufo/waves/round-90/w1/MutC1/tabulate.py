#!/usr/bin/env python3
"""MutC1 tabulator: per fixture x counter, the open items; kill = an item the frozen
counter (M00) leaves open on a forgery fixture becomes closed under the mutant."""
import json, os, sys

HERE = os.path.dirname(os.path.abspath(__file__))
RUNS = os.path.join(HERE, "runs")
fixtures = []
for line in open(os.path.join(HERE, "drive-log.txt")):
    if line.startswith("## ") and " rev=" in line:
        fixtures.append(line.split()[1])
mids = sorted(f[:-3] for f in os.listdir(os.path.join(HERE, "mutants")) if f.endswith(".py"))
desc = {}
for l in open(os.path.join(HERE, "mutants", "manifest.tsv")).read().splitlines()[1:]:
    i, _, d = l.split("\t", 2)
    desc[i] = d


def read(fx, mid):
    lines = open(os.path.join(RUNS, fx, mid + ".txt")).read().splitlines()
    try:
        res = json.loads(lines[1])
        return {k for k, v in res.items() if v}, lines[0], lines[-1]
    except Exception:
        return None, " | ".join(lines[:3]), lines[-1] if lines else ""


base = {fx: read(fx, "M00") for fx in fixtures}
out = []
out.append("frozen counter (M00) open items per fixture:")
for fx in fixtures:
    o, l1, ex = base[fx]
    out.append("  %-44s open=%s  %s" % (fx, ",".join(sorted(o)) if o is not None else "ERR", ex))
out.append("")
hdr = "%-4s " % "mut" + " ".join("%-3d" % (i + 1) for i in range(len(fixtures)))
out.append("fixture index: " + "; ".join("%d=%s" % (i + 1, f) for i, f in enumerate(fixtures)))
out.append("cell: K=kill (forgery item closed by mutant only), .=same, P=positive broken, E=error, +=extra item open")
out.append(hdr)
summary = {}
for mid in mids:
    row, kills_ctl, kills_x, pos_broken, err = [], [], [], False, False
    for fx in fixtures:
        o, l1, ex = read(fx, mid)
        bo = base[fx][0]
        if o is None or bo is None:
            row.append("E"); err = True; continue
        newly_closed = bo - o
        if fx == "c1-positive":
            c = "P" if o else "."
            pos_broken = bool(o)
        elif newly_closed:
            c = "K"
            (kills_ctl if fx.startswith("c1-") else kills_x).append(fx)
        elif o - bo:
            c = "+"
        else:
            c = "."
        row.append(c)
    out.append("%-4s " % mid + " ".join("%-3s" % c for c in row))
    summary[mid] = (kills_ctl, kills_x, pos_broken, err)
out.append("")
out.append("verdicts (controls = run_controls.sh fixtures; X = MutC1 supplemental forgeries):")
for mid in mids:
    kc, kx, pb, err = summary[mid]
    v = "KILLED by controls" if kc else ("DETECTED by positive control" if pb else ("SURVIVED controls" + ("; killed by X: " + ",".join(kx) if kx else "; no X kills")))
    if err:
        v += " [ERROR cells]"
    out.append("  %s %-70s %s%s" % (mid, desc[mid], v, (" [" + ",".join(kc) + "]") if kc else ""))
print("\n".join(out))
