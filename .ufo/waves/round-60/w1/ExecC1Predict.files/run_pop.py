#!/usr/bin/env python3
"""Run the 28 round-48..59 population counters at a given revision.

Usage: run_pop.py <revision> <tag>
Cwd must be the mock clone. Writes scratch/results/<tag>.json and logs/<tag>/<m>.log
Commands resolved per the round-60 C1 contract: registered entry commands where
they exist (placeholders: <commit>/<rev>/<revision>/<tip> -> revision under test,
<scratch> -> fresh dir, <fleet root> -> /home/vgpnk/Projects/shokunin; [...] kept
when every inner <...> is one of those placeholders, else dropped). Unregistered
members get the generic `python3 -B <path> --root . --revision <rev>`.
"""
import json, os, pathlib, subprocess, sys, concurrent.futures

S = pathlib.Path("/fast/scratch/hyaku/kake-r60/ExecC1Predict")
MOCK = S / "mock"
FLEET = "/home/vgpnk/Projects/shokunin"
REV = sys.argv[1]
TAG = sys.argv[2]

def generic(path):
    return ["python3", "-B", path, "--root", ".", "--revision", REV]

# member -> (path, registered command template or None)
MEMBERS = [
    ("c48_lint_count",      ".ufo/waves/round-48/c48_lint_count.py", None),
    ("c48_quote_truth",     ".ufo/waves/round-48/c48_quote_truth.py", None),
    ("c49_order",           ".ufo/waves/round-49/c49_order.py", None),
    ("c49_quote_truth",     ".ufo/waves/round-49/c49_quote_truth.py", None),
    ("c50_durable",         ".ufo/waves/round-50/c50_durable.py", None),
    ("c50_quote_class",     ".ufo/waves/round-50/c50_quote_class.py", None),
    ("c51_quote_truth",     ".ufo/waves/round-51/c51_quote_truth.py", None),
    ("c51_wave_ledger",     ".ufo/waves/round-51/c51_wave_ledger.py", None),
    ("c52_gate_registry",   ".ufo/waves/round-52/c52_gate_registry.py", None),
    ("c52_mutation_ladder", ".ufo/waves/round-52/c52_mutation_ladder.py", None),
    ("c52_quote_truth",     ".ufo/waves/round-52/c52_quote_truth.py",
        "python3 -B .ufo/waves/round-52/c52_quote_truth.py --root . --revision <commit>"),
    ("c52_wave_ledger",     ".ufo/waves/round-52/c52_wave_ledger.py",
        "python3 -B .ufo/waves/round-52/c52_wave_ledger.py --root . --revision <commit>"),
    ("c53_gate_truth",      ".ufo/waves/round-53/exec-quality-gate/c53_gate_truth.py",
        "python3 -B .ufo/waves/round-53/exec-quality-gate/c53_gate_truth.py --revision <commit>"),
    ("c54_ops_debt",        ".ufo/waves/round-54/c54_ops_debt.py", None),
    ("c54_s374_calib",      ".ufo/waves/round-54/c54_s374_calib.py", None),
    ("c55_quote_truth",     ".ufo/waves/round-55/c55_quote_truth.py",
        "python3 -B .ufo/waves/round-55/c55_quote_truth.py --root . --revision <commit>"),
    ("c55_readme_index",    ".ufo/waves/round-55/c55_readme_index.py",
        "python3 -B .ufo/waves/round-55/c55_readme_index.py --root . --revision <commit>"),
    ("c56_quote_truth",     ".ufo/waves/round-56/c56_quote_truth.py",
        "python3 -B .ufo/waves/round-56/c56_quote_truth.py --root . --revision <commit>"),
    ("c56_selftally",       ".ufo/waves/round-56/c56_selftally.py",
        "python3 -B .ufo/waves/round-56/c56_selftally.py --root . --revision <commit>"),
    ("c57_idresolver_gate", ".ufo/waves/round-57/c57_idresolver_gate.py",
        "python3 -B .ufo/waves/round-57/c57_idresolver_gate.py --root . --revision <commit> --fleet <fleet root>"),
    ("c57_quote_truth",     ".ufo/waves/round-57/c57_quote_truth.py",
        "python3 -B .ufo/waves/round-57/c57_quote_truth.py --root . --revision <commit>"),
    ("c57_receipt_pins",    ".ufo/waves/round-57/c57_receipt_pins.py",
        "python3 -B .ufo/waves/round-57/c57_receipt_pins.py --root . --revision <tip>"),
    ("c58_quote_truth",     ".ufo/waves/round-58/c58_quote_truth.py",
        "python3 -B .ufo/waves/round-58/c58_quote_truth.py --root . --revision <commit>"),
    ("c58_receipt_rewrites",".ufo/waves/round-58/c58_receipt_rewrites.py",
        "python3 -B .ufo/waves/round-58/c58_receipt_rewrites.py --root . --revision <tip>"),
    ("c58_resolver_cases",  ".ufo/waves/round-58/c58_resolver_cases.py",
        "python3 -B .ufo/waves/round-58/c58_resolver_cases.py --root . --revision <rev> --work <scratch>"),
    ("c59_axis_evidence",   ".ufo/waves/round-59/c59_axis_evidence.py",
        "python3 -B .ufo/waves/round-59/c59_axis_evidence.py --root . --revision <rev> --base <rev> --json"),
    ("c59_quote_truth",     ".ufo/waves/round-59/c59_quote_truth.py",
        "python3 -B .ufo/waves/round-59/c59_quote_truth.py --root . --revision <commit> --base <rev> --json"),
    ("c59_resolver_cases",  ".ufo/waves/round-59/c59_resolver_cases.py",
        "TMPDIR=<scratch> python3 -B .ufo/waves/round-59/c59_resolver_cases.py --root . --revision <rev> --work <scratch>"),
]

def build(name, path, tmpl):
    work = S / "work" / TAG / name
    work.mkdir(parents=True, exist_ok=True)
    env = {k: v for k, v in os.environ.items() if not k.startswith("GIT_")}
    env["TMPDIR"] = str(work)
    if tmpl is None:
        argv = generic(path)
    else:
        s = tmpl
        s = s.replace("<commit>", REV).replace("<revision>", REV).replace("<rev>", REV).replace("<tip>", REV)
        s = s.replace("<fleet root>", FLEET).replace("<scratch>", str(work))
        # leading NAME=value words are env assignments
        import shlex
        parts = shlex.split(s)
        while parts and "=" in parts[0] and not parts[0].startswith("-"):
            k, _, v = parts.pop(0).partition("=")
            env[k] = v
        argv = parts
    return argv, env, work

def run(member):
    name, path, tmpl = member
    argv, env, work = build(name, path, tmpl)
    logdir = S / "logs" / TAG
    logdir.mkdir(parents=True, exist_ok=True)
    try:
        p = subprocess.run(argv, cwd=MOCK, env=env, capture_output=True, text=True,
                           timeout=1800)
        code, out, err = p.returncode, p.stdout, p.stderr
    except subprocess.TimeoutExpired as e:
        code, out, err = 124, (e.stdout or "" if isinstance(e.stdout, str) else (e.stdout or b"").decode("utf-8", "replace")), "TIMEOUT 1800s"
    (logdir / f"{name}.log").write_text(
        "$ " + " ".join(argv) + "\nEXIT " + str(code) + "\n--- stdout ---\n" + (out or "") + "\n--- stderr ---\n" + (err or ""))
    return name, code, (out or "")[-2000:]

results = {}
(S / "results").mkdir(exist_ok=True)
with concurrent.futures.ThreadPoolExecutor(max_workers=6) as ex:
    for name, code, tail in ex.map(run, MEMBERS):
        results[name] = code
        print(f"{name}: {code}", flush=True)
(S / "results" / f"{TAG}.json").write_text(json.dumps(results, indent=1, sort_keys=True))
print(json.dumps(results, sort_keys=True))
