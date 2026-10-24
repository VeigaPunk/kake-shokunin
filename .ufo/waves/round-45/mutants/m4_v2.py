#!/usr/bin/env python3
"""Round-45 control audit driver — receipt-gated successor to the round-44 audit."""
import argparse
import concurrent.futures as cf
import hashlib
import importlib.util
import json
import os
import secrets
import subprocess
import sys
import time


MTIME_EPS_NS = 1_000_000_000
RECEIPT_ERRORS = {"counter_error", "tool_absent", "stale_receipt"}


def load_counter(path):
    spec = importlib.util.spec_from_file_location("kake45_counter", path)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


def sha256_file(path):
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 20), b""):
            h.update(chunk)
    return h.hexdigest()


def _tail(value):
    if isinstance(value, str):
        value = value.encode("utf-8", "replace")
    return (value or b"")[-2000:].decode("utf-8", "replace")


def run_counter(counter, root, out, classes, tool=None, revision=None, timeout=900):
    argv = [sys.executable, "-B", counter, "--root", root, "--classes", classes, "--out", out]
    if tool:
        argv += ["--tool-file", tool]
    if revision:
        argv += ["--revision", revision]
    try:
        p = subprocess.run(argv, capture_output=True, stdin=subprocess.DEVNULL, timeout=timeout)
        code, stdout, stderr = p.returncode, p.stdout, p.stderr
    except (OSError, subprocess.TimeoutExpired) as ex:
        code = 2
        stdout = getattr(ex, "stdout", None)
        stderr = getattr(ex, "stderr", None) or str(ex).encode("utf-8", "replace")

    finish_ns = time.time_ns()
    rec = None
    try:
        with open(out) as fh:
            rec = json.load(fh)
    except (OSError, ValueError):
        rec = None
    try:
        mtime_ns = os.stat(out).st_mtime_ns
    except OSError:
        mtime_ns = None
    return code, rec, _tail(stdout), _tail(stderr), finish_ns, mtime_ns


def receipt_validity(receipt, exit_code, mtime_bounds, counter_sha):
    """Return (valid, error class); mtime_bounds is (receipt mtime, lower, upper), in ns."""
    if exit_code not in (0, 1):
        return False, "counter_error"
    if not isinstance(receipt, dict):
        return False, "stale_receipt"
    if receipt.get("note") == "tool absent":
        return False, "tool_absent"
    if receipt.get("counterSha256") != counter_sha:
        return False, "stale_receipt"
    if "seed" not in receipt or receipt["seed"] is None:
        return False, "stale_receipt"
    try:
        receipt_mtime_ns, lower_ns, upper_ns = mtime_bounds
        in_window = lower_ns <= receipt_mtime_ns <= upper_ns
    except (TypeError, ValueError):
        in_window = False
    if not in_window:
        return False, "stale_receipt"
    return True, None


def semantic_witness(row, class_keys):
    if row.get("error"):
        return True
    caught = row.get("caughtBy") or []
    return (row.get("met") is False and bool(caught) and
            any(isinstance(key, str) and key in class_keys for key in caught))


def build_control_row(base, tool_sha, code, rec, mtime_ns, started_ns, finish_ns,
                      counter_sha, receipt_rel):
    """Apply the one receipt-validity gate to a control run and build its row.

    Every control row in main() is produced through this function; the selftest
    drives it directly, so a mutant that unwires the gate from the row path fails
    the shipped --selftest.
    """
    valid, validity_error = receipt_validity(
        rec, code, (mtime_ns, started_ns - MTIME_EPS_NS, finish_ns + MTIME_EPS_NS),
        counter_sha)
    receipt_data = rec if isinstance(rec, dict) else {}
    caught = []
    runs = receipt_data.get("runs", {})
    if isinstance(runs, dict):
        for key, run in runs.items():
            if isinstance(run, dict) and run.get("equal") is False:
                caught.append(key)
    return dict(base, toolSha256=tool_sha, met=receipt_data.get("met"), exit=code,
                equalRuns=receipt_data.get("equalRuns"), caughtBy=caught,
                seed=receipt_data.get("seed"), receipt=receipt_rel,
                error=validity_error, _valid=valid)


def build_build_row(i, code, rec, mtime_ns, started_ns, finish_ns, counter_sha,
                    receipt_rel):
    """Build-row twin of build_control_row; build rows get the same validity gate."""
    valid, validity_error = receipt_validity(
        rec, code, (mtime_ns, started_ns - MTIME_EPS_NS, finish_ns + MTIME_EPS_NS),
        counter_sha)
    receipt_data = rec if isinstance(rec, dict) else {}
    return {"run": i + 1, "exit": code, "met": receipt_data.get("met"),
            "seed": receipt_data.get("seed"), "equalRuns": receipt_data.get("equalRuns"),
            "ratios": receipt_data.get("ratios"), "receipt": receipt_rel,
            "error": validity_error, "_valid": valid}


def row_valid(row):
    return row.get("_valid", not row.get("error")) is True and not row.get("error")


def valid_rows(rows):
    return [row for row in rows if row_valid(row)]


def not_met_rows(rows):
    return [row for row in rows if row_valid(row) and row.get("met") is False]


def build_met(build, build_runs):
    count_ok = build_runs <= 0 or len(build) == build_runs
    return (count_ok and bool(build) and
            all(row_valid(row) and row.get("met") is True for row in build))


def expectation_ok(expect, results, build, expected_rows, class_keys, build_runs=0):
    if any(not row_valid(row) for row in results) or any(not row_valid(row) for row in build):
        return False
    if build_runs > 0 and len(build) != build_runs:
        return False
    total = len(valid_rows(results))
    witnessed = [r for r in results if semantic_witness(r, class_keys)]
    not_met = not_met_rows(results)
    if expect == "blind":
        return (total == expected_rows and not witnessed and
                all(r.get("met") is True for r in results))
    if expect == "witnessed":
        return (total == expected_rows and len(witnessed) == total and
                build_met(build, build_runs))
    return expect == "not-met" and total == expected_rows and len(not_met) == total


def selftest():
    passing = {"name": "pass-all", "met": True, "caughtBy": []}
    class_divergence = {"name": "class-divergence", "met": False, "caughtBy": ["G2"]}
    v4_divergence = {"name": "v4-divergence", "met": False, "caughtBy": ["D"]}
    mixed_divergence = {"name": "mixed-divergence", "met": False, "caughtBy": ["D", "G3"]}
    legacy_divergence = {"name": "legacy-divergence", "met": False, "caughtBy": ["C", "D"]}
    timing_only = {"name": "timing-only", "met": False, "caughtBy": ["T1"]}
    keys = {"G1", "G2", "G3"}

    assert not semantic_witness(passing, keys)
    assert semantic_witness(class_divergence, keys)
    assert semantic_witness(mixed_divergence, keys)
    assert not semantic_witness(v4_divergence, keys)
    assert not semantic_witness(legacy_divergence, keys)
    assert not semantic_witness(timing_only, keys)
    assert not semantic_witness(class_divergence, set())
    assert expectation_ok("blind", [passing], [], 1, keys)
    assert not expectation_ok("blind", [v4_divergence], [], 1, keys)
    assert expectation_ok("witnessed", [class_divergence, mixed_divergence], [{"met": True}], 2, keys)
    assert not expectation_ok("witnessed", [v4_divergence], [{"met": True}], 1, keys)
    assert not expectation_ok("witnessed", [legacy_divergence], [{"met": True}], 1, keys)
    assert expectation_ok("not-met", [v4_divergence], [], 1, keys)

    receipt = {"counterSha256": "counter-sha", "seed": 0, "note": None, "met": False}
    in_window = (100, 90, 110)
    assert receipt_validity(receipt, 1, in_window, "counter-sha") == (True, None)
    assert receipt_validity(receipt, 2, in_window, "counter-sha") == (False, "counter_error")
    assert receipt_validity(dict(receipt, note="tool absent"), 1, in_window,
                            "counter-sha") == (False, "tool_absent")
    assert receipt_validity(dict(receipt, counterSha256="other-sha"), 1, in_window,
                            "counter-sha") == (False, "stale_receipt")
    assert receipt_validity(receipt, 1, (111, 90, 110), "counter-sha") == (False, "stale_receipt")
    assert receipt_validity({"counterSha256": "counter-sha", "note": None}, 1,
                            in_window, "counter-sha") == (False, "stale_receipt")
    assert receipt_validity(None, 1, in_window, "counter-sha") == (False, "stale_receipt")

    error_row = dict(v4_divergence, error="counter_error", _valid=False)
    assert not not_met_rows([error_row])
    assert not expectation_ok("not-met", [error_row], [], 1, keys)
    assert not expectation_ok("witnessed", [class_divergence, mixed_divergence],
                              [{"met": True}], 2, keys, build_runs=3)
    errored_class_witness = dict(class_divergence, error="counter_error")
    assert not semantic_witness(errored_class_witness, keys)
    _selftest_cohort()
    print("SELFTEST PASS: v1 assertions plus timing-only, invalid receipt, error-row, "
          "build-count gates, and the end-to-end fixture cohort")


def _write(path, text):
    with open(path, "w") as fh:
        fh.write(text)


def _selftest_cohort():
    """Drive main() itself over an isolated temp cohort: one honest control plus the
    three invalid receipt classes, each as a fake counter that reports its own sha
    exactly like the real counter does. Catches mutants that unwired the validity
    gate from the row/build paths (the unit asserts alone cannot)."""
    import tempfile
    me = os.path.abspath(__file__)
    tmp = tempfile.mkdtemp(prefix="kake45-audit-selftest-")
    root = os.path.join(tmp, "root")
    os.makedirs(root)
    ctl = os.path.join(root, "ctl.py")
    _write(ctl, "# selftest control\n")
    ctl_sha = sha256_file(ctl)
    _write(os.path.join(tmp, "controls.tsv"),
           "ctl1\tfam\tcls\tctl.py\t%s\tselftest\n" % ctl_sha)

    fake = '''import hashlib, json, os, sys, time

CLASS_MODULES = tuple(("G%d" % i, "g%d.py" % i) for i in range(1, 11))
PREDICATE = "selftest predicate"

def main():
    mode = os.path.basename(os.path.dirname(os.path.abspath(__file__)))
    out = sys.argv[sys.argv.index("--out") + 1]
    sha = hashlib.sha256(open(__file__, "rb").read()).hexdigest()
    if mode == "counter-error":
        rec = {"counterSha256": sha, "seed": 1, "note": None, "met": False,
               "runs": {"G2": {"equal": False}}}
        json.dump(rec, open(out, "w")); sys.exit(2)
    if mode == "tool-absent":
        rec = {"counterSha256": sha, "seed": 1, "note": "tool absent", "met": False,
               "runs": {k: {"equal": False, "candExit": "tool absent"} for k in
                        ["A", "B", "C", "D", "E", "F", "G1", "T1", "T2", "T3", "T4", "T5"]}}
        json.dump(rec, open(out, "w")); sys.exit(1)
    if mode == "stale":
        rec = {"counterSha256": sha, "seed": 1, "note": None, "met": False,
               "runs": {"G2": {"equal": False}}}
        json.dump(rec, open(out, "w"))
        past = time.time() - 5
        os.utime(out, (past, past)); sys.exit(0)
    # honest: a real legacy-only divergence the gate must credit as not-met
    rec = {"counterSha256": sha, "seed": 1, "note": None, "met": False,
           "runs": {"C": {"equal": False}}}
    json.dump(rec, open(out, "w")); sys.exit(1)

if __name__ == "__main__":
    main()
'''
    expected = {"counter-error": "counter_error", "tool-absent": "tool_absent",
                "stale": "stale_receipt"}
    for mode, want_error in expected.items():
        cdir = os.path.join(tmp, mode)
        os.makedirs(cdir)
        fake_path = os.path.join(cdir, "fake_counter.py")
        _write(fake_path, fake)
        cohort = os.path.join(tmp, "out-" + mode)
        p = subprocess.run(
            [sys.executable, "-B", me, "--root", root, "--controls",
             os.path.join(tmp, "controls.tsv"), "--counter", fake_path,
             "--classes", "v5", "--expect", "witnessed", "--out",
             os.path.join(cohort, "summary.json")],
            capture_output=True, stdin=subprocess.DEVNULL, timeout=120)
        assert p.returncode == 1, (mode, p.returncode, p.stdout[-500:], p.stderr[-500:])
        with open(os.path.join(cohort, "summary.json")) as fh:
            summary = json.load(fh)
        assert summary["ok"] is False and summary["witnessed"] == 0, (mode, summary["witnessed"])
        assert want_error in ",".join(summary["errors"]), (mode, summary["errors"])

    cdir = os.path.join(tmp, "honest")
    os.makedirs(cdir)
    fake_path = os.path.join(cdir, "fake_counter.py")
    _write(fake_path, fake)
    cohort = os.path.join(tmp, "out-honest")
    p = subprocess.run(
        [sys.executable, "-B", me, "--root", root, "--controls",
         os.path.join(tmp, "controls.tsv"), "--counter", fake_path,
         "--classes", "v5", "--expect", "not-met", "--out",
         os.path.join(cohort, "summary.json")],
        capture_output=True, stdin=subprocess.DEVNULL, timeout=120)
    assert p.returncode == 0, (p.returncode, p.stdout[-500:], p.stderr[-500:])
    with open(os.path.join(cohort, "summary.json")) as fh:
        summary = json.load(fh)
    assert summary["ok"] is True and summary["notMet"] == 1 and summary["witnessed"] == 0


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
    out_path = os.path.abspath(a.out)
    outdir = os.path.dirname(out_path)
    try:
        os.makedirs(outdir, exist_ok=True)
        if os.listdir(outdir):
            ap.error("output directory must be empty: %s" % outdir)
    except OSError as ex:
        ap.error("cannot create output directory %s: %s" % (outdir, ex))

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

    tools_dir = os.path.join(outdir, "tools")
    try:
        os.mkdir(tools_dir)
    except OSError as ex:
        ap.error("cannot create cohort tools directory %s: %s" % (tools_dir, ex))
    started_ns = time.time_ns()
    manifest = {"started_ns": started_ns, "counter_sha256": counter_sha,
                "driver_sha256": sha256_file(os.path.abspath(__file__)),
                "nonce": secrets.token_hex(16)}
    try:
        with open(os.path.join(outdir, "run-manifest.json"), "x") as fh:
            json.dump(manifest, fh, indent=1)
            fh.write("\n")
    except OSError as ex:
        ap.error("cannot create run manifest: %s" % ex)

    def score(row):
        tool = os.path.join(root, row["path"])
        got = sha256_file(tool) if os.path.exists(tool) else None
        out = os.path.join(tools_dir, row["name"] + ".json")
        if got != row["sha256"]:
            return dict(row, toolSha256=got, met=None, exit=2,
                        error="control sha256 mismatch or file missing", _valid=False)
        code, rec, so, se, finish_ns, mtime_ns = run_counter(
            counter, root, out, a.classes, tool=tool)
        return build_control_row(row, got, code, rec, mtime_ns, started_ns, finish_ns,
                                 counter_sha, os.path.relpath(out, outdir))

    with cf.ThreadPoolExecutor(max_workers=max(1, a.workers)) as pool:
        results = list(pool.map(score, rows))

    class_keys = [key for key, _ in counter_mod.CLASS_MODULES] if a.classes == "v5" else []
    class_key_set = set(class_keys)
    eligible_results = valid_rows(results)
    witnessed = [r for r in eligible_results if semantic_witness(r, class_key_set)]
    witnessed_names = [r["name"] for r in witnessed]
    not_met_names = [r["name"] for r in not_met_rows(results)]

    build = []
    if a.build_rev and a.build_runs:
        def score_build(i):
            out = os.path.join(outdir, "build-%d.json" % (i + 1))
            code, rec, so, se, finish_ns, mtime_ns = run_counter(
                counter, root, out, a.classes, revision=a.build_rev)
            return build_build_row(i, code, rec, mtime_ns, started_ns, finish_ns,
                                   counter_sha, os.path.relpath(out, outdir))
        with cf.ThreadPoolExecutor(max_workers=min(3, a.build_runs)) as pool:
            build = list(pool.map(score_build, range(a.build_runs)))

    total = len(eligible_results)
    errors = [((r["name"] + ":" + r["error"]) if r.get("error") in RECEIPT_ERRORS else r["name"])
              for r in results if r.get("error")]
    errors += [(("build#%d:" % b["run"]) + b["error"] if b.get("error") in RECEIPT_ERRORS
                else "build#%d" % b["run"])
               for b in build if b.get("error")]
    summary = {
        "label": a.label, "classesMode": a.classes, "expect": a.expect,
        "counter": os.path.relpath(counter, root), "counterSha256": counter_sha,
        "predicate": counter_mod.PREDICATE,
        "controls": total, "classKeys": class_keys,
        "witnessed": len(witnessed), "witnessedNames": witnessed_names,
        "witnessedByClass": {r["name"]: r.get("caughtBy") for r in witnessed},
        "notMet": len(not_met_names), "notMetNames": not_met_names,
        "metNames": [r["name"] for r in eligible_results if r.get("met") is True],
        "errors": errors,
        "build": [{k: b.get(k) for k in ("run", "exit", "met", "seed", "equalRuns", "ratios",
                                           "receipt", "error")} for b in build],
        "rows": [{**{k: r.get(k) for k in ("name", "family", "class", "path", "sha256", "exit", "met",
                                        "equalRuns", "seed", "caughtBy", "receipt", "error")},
                  "classCaught": [k for k in (r.get("caughtBy") or []) if k in class_key_set],
                  "legacyCaught": [k for k in (r.get("caughtBy") or []) if k not in class_key_set]}
                 for r in results],
    }
    ok = expectation_ok(a.expect, results, build, len(rows), class_key_set, a.build_runs)
    summary["ok"] = ok
    build_met_count = sum(1 for b in build if row_valid(b) and b["met"] is True)
    summary["verdict"] = ("witnessed %d/%d notMet=%d" % (len(witnessed), total, len(not_met_names))) + (
        " build met %d/%d" % (build_met_count, len(build)) if build else "")
    with open(out_path, "w") as fh:
        json.dump(summary, fh, indent=1)
        fh.write("\n")
    class_note = " (no class runs; witnessed=0 by construction)" if a.classes == "v4" else ""
    print("AUDIT %s classes=%s classKeys=%s witnessed=%d/%d%s notMet=%d build_met=%d/%d ok=%s counter=%s" % (
        a.label or "kake-r45", a.classes, ",".join(class_keys) or "-", len(witnessed), total,
        class_note, len(not_met_names), build_met_count, len(build), ok,
        counter_sha[:12]))
    for r in results:
        print("  %-20s %-10s met=%-5s caught=%-22s %s" % (
            r["name"], r["class"], r["met"], ",".join(r.get("caughtBy") or []) or "-", r.get("error") or ""))
    for r in witnessed:
        print("  witnessed-by-class %s caughtBy=%s" % (r["name"], ",".join(r.get("caughtBy") or [])))
    for b in build:
        print("  build#%d met=%s equal=%s %s" % (
            b["run"], b["met"], b["equalRuns"], b.get("error") or ""))
    sys.exit(0 if ok else 1)


if __name__ == "__main__":
    main()
