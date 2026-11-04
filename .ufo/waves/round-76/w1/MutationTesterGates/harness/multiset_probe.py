#!/usr/bin/env python3
"""A16 probe: score C2 cases under the AMENDED comparison rule.

Amendment 2 A16 requires, per case:
  * a parseable JSON object carrying `version`, `pages`, `findings`, `counts`, `exit`;
  * `pages` equal to the manifest's page count;
  * finding ids compared as a MULTISET;
  * a tool that prints nothing is a failed case.
The shipped runner (c76_hreflang_matrix.py) instead compares id SETS and accepts any
JSON with a `findings` list, so this probe exists to measure what the shipped matrix
cannot. Same fixtures, same 44 cases, nothing else changed.

usage: multiset_probe.py --tool PATH [--cases DIR] [--work DIR] [--json]
"""
import argparse
import collections
import json
import os
import shutil
import subprocess
import sys

INFO_IDS = {"hreflang_external_target"}
REQUIRED = {"version", "pages", "findings", "counts", "exit"}


def write_fixture(case, dest):
    if os.path.exists(dest):
        shutil.rmtree(dest)
    os.makedirs(dest)
    for name, body in case["files"].items():
        path = os.path.join(dest, name)
        parent = os.path.dirname(path)
        if parent and not os.path.isdir(parent):
            os.makedirs(parent)
        with open(path, "wb") as handle:
            handle.write(body.encode("utf-8") if isinstance(body, str) else body)
    manifest = case["manifest"]
    with open(os.path.join(dest, "manifest.json"), "w", encoding="utf-8") as handle:
        json.dump(manifest, handle)


def ids_of(report):
    out = []
    for row in report.get("findings") or []:
        if isinstance(row, dict):
            value = row.get("id") or row.get("finding") or row.get("code")
        elif isinstance(row, str):
            value = row
        else:
            value = None
        if isinstance(value, str) and value not in INFO_IDS:
            out.append(value)
    return out


def score(tool, case, work, index, timeout):
    fixture = os.path.join(work, "fixtures", "%02d-%s" % (index, case["name"]))
    run_dir = os.path.join(work, "runs", "%02d-%s" % (index, case["name"]))
    write_fixture(case, fixture)
    if os.path.exists(run_dir):
        shutil.rmtree(run_dir)
    os.makedirs(os.path.join(run_dir, "tmp"))
    env = dict(os.environ)
    env["TMPDIR"] = os.path.join(run_dir, "tmp")
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    proc = subprocess.run(
        [sys.executable, tool, "--manifest", os.path.join(fixture, "manifest.json"),
         "--root", fixture, "--json"],
        cwd=run_dir, env=env, timeout=timeout,
        stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    note = ""
    try:
        report = json.loads(proc.stdout.decode("utf-8", "replace"))
    except (ValueError, TypeError):
        report = None
    if not isinstance(report, dict):
        return {"name": case["name"], "verdict": "wrong", "why": "no parseable JSON"}
    missing = sorted(REQUIRED - set(report))
    if missing:
        return {"name": case["name"], "verdict": "wrong", "why": "missing keys %s" % missing}
    want_pages = len(case["manifest"].get("pages") or [])
    if report.get("pages") != want_pages:
        return {"name": case["name"], "verdict": "wrong",
                "why": "pages=%r want %d" % (report.get("pages"), want_pages)}
    want = collections.Counter(i for i in case["expected"]["ids"] if i not in INFO_IDS)
    got = collections.Counter(ids_of(report))
    ok = (proc.returncode == case["expected"]["exit"] and got == want
          and report.get("exit") == case["expected"]["exit"])
    return {"name": case["name"], "verdict": "correct" if ok else "wrong",
            "why": "" if ok else "exit=%s/%s ids=%s want=%s" % (
                proc.returncode, case["expected"]["exit"],
                sorted(got.elements()), sorted(want.elements()))}


def main(argv):
    ap = argparse.ArgumentParser()
    ap.add_argument("--tool", required=True)
    ap.add_argument("--cases", required=True)
    ap.add_argument("--work", required=True)
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--timeout", type=float, default=60.0)
    a = ap.parse_args(argv)
    if os.path.exists(a.work):
        shutil.rmtree(a.work)
    os.makedirs(a.work)
    rows = []
    for index, name in enumerate(sorted(os.listdir(a.cases))):
        if not name.endswith(".json"):
            continue
        case = json.loads(open(os.path.join(a.cases, name), "rb").read().decode("utf-8"))
        if not case.get("decided"):
            rows.append({"name": case["name"], "verdict": "undecided", "why": ""})
            continue
        rows.append(score(os.path.abspath(a.tool), case, a.work, index, a.timeout))
    decided = [r for r in rows if r["verdict"] != "undecided"]
    wrong = [r for r in decided if r["verdict"] == "wrong"]
    out = {"tool": os.path.abspath(a.tool), "cases": len(rows), "decided": len(decided),
           "correct": len(decided) - len(wrong), "wrong": len(wrong),
           "failures": [{"name": r["name"], "why": r["why"]} for r in wrong]}
    if a.json:
        print(json.dumps(out, indent=1))
    else:
        for r in wrong:
            print("WRONG %s: %s" % (r["name"], r["why"]))
        print("A16 probe: cases=%d decided=%d correct=%d wrong=%d"
              % (out["cases"], out["decided"], out["correct"], out["wrong"]))
    return 0 if not wrong else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
