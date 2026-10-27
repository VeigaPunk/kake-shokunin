#!/usr/bin/env python3
"""Variant runs: bracket-dropped resolution for the 5 optional-arg members.
Usage: run_variant.py <revision> <tag>
"""
import os, pathlib, subprocess, sys, json

S = pathlib.Path("/fast/scratch/hyaku/kake-r60/ExecC1Predict")
MOCK = S / "mock"
REV, TAG = sys.argv[1], sys.argv[2]

RUNS = [
    ("c57_idresolver_gate",
     ["python3", "-B", ".ufo/waves/round-57/c57_idresolver_gate.py", "--root", ".", "--revision", REV]),
    ("c58_resolver_cases",
     ["python3", "-B", ".ufo/waves/round-58/c58_resolver_cases.py", "--root", ".", "--revision", REV]),
    ("c59_axis_evidence",
     ["python3", "-B", ".ufo/waves/round-59/c59_axis_evidence.py", "--root", ".", "--revision", REV, "--json"]),
    ("c59_quote_truth",
     ["python3", "-B", ".ufo/waves/round-59/c59_quote_truth.py", "--root", ".", "--revision", REV, "--json"]),
    ("c59_resolver_cases",
     ["python3", "-B", ".ufo/waves/round-59/c59_resolver_cases.py", "--root", ".", "--revision", REV]),
]

work = S / "work" / f"{TAG}-drop"
work.mkdir(parents=True, exist_ok=True)
env = {k: v for k, v in os.environ.items() if not k.startswith("GIT_")}
env["TMPDIR"] = str(work)
logdir = S / "logs" / TAG
logdir.mkdir(parents=True, exist_ok=True)
out = {}
for name, argv in RUNS:
    p = subprocess.run(argv, cwd=MOCK, env=env, capture_output=True, text=True, timeout=1800)
    out[name] = p.returncode
    (logdir / f"{name}.drop.log").write_text(
        "$ " + " ".join(argv) + "\nEXIT " + str(p.returncode) + "\n--- stdout ---\n" + p.stdout + "\n--- stderr ---\n" + p.stderr)
    print(name, p.returncode, flush=True)
(S / "results" / f"{TAG}-drop.json").write_text(json.dumps(out, indent=1))
