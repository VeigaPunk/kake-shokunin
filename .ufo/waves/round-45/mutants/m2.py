#!/usr/bin/env python3
"""Round-44 control audit driver — the round's one counting command.

Scores controls with the frozen round-44 counter and reports candidate met status. A semantic
witness requires met=false and at least one caughtBy key that is a class run (G1-G10); a v4
run divergence (A-F, T1-T5 keys) is reported as legacyCaught and never witnesses a class.
Version v4 has no class runs, so witnessed is zero by construction in v4 mode.

Usage:
  python3 -B .ufo/waves/round-44/c44_audit.py --root . --controls .ufo/waves/round-44/controls-27.tsv \
      --counter .ufo/waves/round-44/c44_count_v5.py --classes v4 --expect blind --out <receipt.json>
  python3 -B .ufo/waves/round-44/c44_audit.py ... --classes v5 --expect witnessed \
      --build-rev <rev> --build-runs 3 --out <receipt.json>

--expect blind      exit 0 iff every control is met and witnessed == 0
--expect witnessed  exit 0 iff every control has a class witness and every build receipt is met
--expect not-met    exit 0 iff every control has met == false; no build receipts are required
--selftest          exercise semantic witnesses and all three expectations

Every per-control counter receipt is kept under <receipt-dir>/tools/ so the tally is
re-derivable; the summary records classKeys and exact caughtBy class keys for witnesses.
"""
import argparse
import concurrent.futures as cf
import hashlib
import importlib.util
import json
import os
import subprocess
import sys


def load_counter(path):
    spec = importlib.util.spec_from_file_location("kake44_counter", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def run_counter(counter, root, out, classes, tool=None, revision=None, timeout=900):
    argv = [sys.executable, "-B", counter, "--root", root, "--classes", classes, "--out", out]
    if tool:
        argv += ["--tool-file", tool]
    if revision:
        argv += ["--revision", revision]
    p = subprocess.run(argv, capture_output=True, stdin=subprocess.DEVNULL, timeout=timeout)
    rec = None
    try:
        with open(out) as fh:
            rec = json.load(fh)
    except (OSError, ValueError):
        rec = None
    return p.returncode, rec, p.stdout.decode("utf-8", "replace")[-2000:], p.stderr.decode("utf-8", "replace")[-2000:]

def semantic_witness(row, class_keys):
    caught = row.get("caughtBy") or []
    return (row.get("met") is False and bool(caught) and
            any(isinstance(key, str) and (key in class_keys or key in ("T1", "T2", "T3", "T4", "T5")) for key in caught))


def expectation_ok(expect, results, build, expected_rows, class_keys):
    total = len([r for r in results if not r.get("error")])
    errors = [r for r in results if r.get("error")]
    witnessed = [r for r in results if semantic_witness(r, class_keys)]
    not_met = [r for r in results if r.get("met") is False]
    if expect == "blind":
        return (total == expected_rows and not errors and not witnessed and
                all(r.get("met") is True for r in results))
    if expect == "witnessed":
        return (total == expected_rows and len(witnessed) == total and not errors and
                bool(build) and all(b.get("met") is True for b in build))
    return (expect == "not-met" and total == expected_rows and len(not_met) == total and
            not errors)


def selftest():
    passing = {"name": "pass-all", "met": True, "caughtBy": []}
    class_divergence = {"name": "class-divergence", "met": False, "caughtBy": ["G2"]}
    v4_divergence = {"name": "v4-divergence", "met": False, "caughtBy": ["D"]}
    mixed_divergence = {"name": "mixed-divergence", "met": False, "caughtBy": ["D", "G3"]}
    legacy_divergence = {"name": "legacy-divergence", "met": False, "caughtBy": ["C", "D"]}
    keys = {"G1", "G2", "G3"}

    assert not semantic_witness(passing, keys)
    assert semantic_witness(class_divergence, keys)
    assert semantic_witness(mixed_divergence, keys)
    assert not semantic_witness(v4_divergence, keys)
    assert not semantic_witness(legacy_divergence, keys)
    assert not semantic_witness(class_divergence, set())
    assert expectation_ok("blind", [passing], [], 1, keys)
    assert not expectation_ok("blind", [v4_divergence], [], 1, keys)
    assert expectation_ok("witnessed", [class_divergence, mixed_divergence], [{"met": True}], 2, keys)
    assert not expectation_ok("witnessed", [v4_divergence], [{"met": True}], 1, keys)
    assert not expectation_ok("witnessed", [legacy_divergence], [{"met": True}], 1, keys)
    assert expectation_ok("not-met", [v4_divergence], [], 1, keys)
    print("SELFTEST PASS: class and mixed-key witnesses pass, legacy/timing-only and no-class witnesses fail")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--selftest", action="store_true")
    ap.add_argument("--root")
    ap.add_argument("--controls")
    ap.add_argument("--counter")
    ap.add_argument("--classes", choices=("v4", "v5"))
    ap.add_argument("--expect", choices=("blind", "witnessed", "not-met"))
    ap.add_argument("--build-rev")
    ap.add_argument("--build-runs", type=int, default=0)
    ap.add_argument("--workers", type=int, default=4)
    ap.add_argument("--out")
    ap.add_argument("--label", default="")
    a = ap.parse_args()
    if a.selftest:
        selftest()
        return
    for name in ("root", "controls", "counter", "classes", "expect", "out"):
        if getattr(a, name) is None:
            ap.error("--%s is required unless --selftest is used" % name)

    root = os.path.abspath(a.root)
    counter = os.path.abspath(a.counter)
    outdir = os.path.dirname(os.path.abspath(a.out))
    tools_dir = os.path.join(outdir, "tools")
    os.makedirs(tools_dir, exist_ok=True)
    counter_mod = load_counter(counter)
    counter_sha = sha256_file(counter)

    rows = []
    with open(a.controls) as fh:
        for line in fh:
            if not line.strip() or line.startswith("#"):
                continue
            name, family, klass, path, sha, seat = line.rstrip("\n").split("\t")
            rows.append({"name": name, "family": family, "class": klass, "path": path,
                         "sha256": sha, "seat": seat})

    def score(row):
        tool = os.path.join(root, row["path"])
        got = sha256_file(tool) if os.path.exists(tool) else None
        out = os.path.join(tools_dir, row["name"] + ".json")
        if got != row["sha256"]:
            return dict(row, toolSha256=got, met=None, exit=2, error="control sha256 mismatch or file missing")
        code, rec, so, se = run_counter(counter, root, out, a.classes, tool=tool)
        caught = []
        if rec:
            for key, run in rec.get("runs", {}).items():
                if run.get("equal") is False:
                    caught.append(key)
        return dict(row, toolSha256=got, met=(rec or {}).get("met"), exit=code,
                    equalRuns=(rec or {}).get("equalRuns"), caughtBy=caught,
                    seed=(rec or {}).get("seed"), receipt=os.path.relpath(out, outdir),
                    error=None if rec else (se or so))

    with cf.ThreadPoolExecutor(max_workers=max(1, a.workers)) as pool:
        results = list(pool.map(score, rows))

    class_keys = [key for key, _ in counter_mod.CLASS_MODULES] if a.classes == "v5" else []
    class_key_set = set(class_keys)
    witnessed = [r for r in results if semantic_witness(r, class_key_set)]
    witnessed_names = [r["name"] for r in witnessed]
    not_met_names = [r["name"] for r in results if r.get("met") is False]

    build = []
    if a.build_rev and a.build_runs:
        def score_build(i):
            out = os.path.join(outdir, "build-%d.json" % (i + 1))
            code, rec, so, se = run_counter(counter, root, out, a.classes, revision=a.build_rev)
            return {"run": i + 1, "exit": code, "met": (rec or {}).get("met"),
                    "seed": (rec or {}).get("seed"), "equalRuns": (rec or {}).get("equalRuns"),
                    "ratios": (rec or {}).get("ratios"),
                    "receipt": os.path.relpath(out, outdir),
                    "error": None if rec else (se or so)}
        with cf.ThreadPoolExecutor(max_workers=min(3, a.build_runs)) as pool:
            build = list(pool.map(score_build, range(a.build_runs)))

    total = len([r for r in results if not r.get("error")])
    errors = [r["name"] for r in results if r.get("error")]
    summary = {
        "label": a.label, "classesMode": a.classes, "expect": a.expect,
        "counter": os.path.relpath(counter, root), "counterSha256": counter_sha,
        "predicate": counter_mod.PREDICATE,
        "controls": total, "classKeys": class_keys,
        "witnessed": len(witnessed), "witnessedNames": witnessed_names,
        "witnessedByClass": {r["name"]: r.get("caughtBy") for r in witnessed},
        "notMet": len(not_met_names), "notMetNames": not_met_names,
        "metNames": [r["name"] for r in results if r.get("met") is True],
        "errors": errors,
        "build": build,
        "rows": [{**{k: r.get(k) for k in ("name", "family", "class", "path", "sha256", "exit", "met",
                                        "equalRuns", "seed", "caughtBy", "receipt", "error")},
                  "classCaught": [k for k in (r.get("caughtBy") or []) if k in class_key_set],
                  "legacyCaught": [k for k in (r.get("caughtBy") or []) if k not in class_key_set]}
                 for r in results],
    }
    ok = expectation_ok(a.expect, results, build, len(rows), class_key_set)
    summary["ok"] = ok
    summary["verdict"] = ("witnessed %d/%d notMet=%d" % (len(witnessed), total, len(not_met_names))) + (
        " build met %d/%d" % (sum(1 for b in build if b["met"] is True), len(build)) if build else "")
    with open(a.out, "w") as fh:
        json.dump(summary, fh, indent=1)
        fh.write("\n")
    class_note = " (no class runs; witnessed=0 by construction)" if a.classes == "v4" else ""
    print("AUDIT %s classes=%s classKeys=%s witnessed=%d/%d%s notMet=%d build_met=%d/%d ok=%s counter=%s" % (
        a.label or "kake-r44", a.classes, ",".join(class_keys) or "-", len(witnessed), total,
        class_note, len(not_met_names), sum(1 for b in build if b["met"] is True), len(build), ok,
        counter_sha[:12]))
    for r in results:
        print("  %-20s %-10s met=%-5s caught=%-22s %s" % (
            r["name"], r["class"], r["met"], ",".join(r.get("caughtBy") or []) or "-", r.get("error") or ""))
    for r in witnessed:
        print("  witnessed-by-class %s caughtBy=%s" % (r["name"], ",".join(r.get("caughtBy") or [])))
    for b in build:
        print("  build#%d met=%s equal=%s %s" % (b["run"], b["met"], b["equalRuns"], b.get("error") or ""))
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()


