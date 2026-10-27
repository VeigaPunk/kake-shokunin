#!/usr/bin/env python3
"""Run ref + 12 mutants over H1..H18 (+A1..A3) and tabulate kills."""
import json, os, re, subprocess, sys

ROOT = os.path.dirname(os.path.abspath(__file__))
ENGINE = os.path.join(ROOT, "audit.py")
FIX = os.path.join(ROOT, "fixtures")
MUTANTS = ["m%02d" % i for i in range(1, 13)]
CORE = ["H%d" % i for i in range(1, 19)]
ADDS = ["A1", "A2", "A3"]

MUTANT_DESC = {
    "m01": "singleton off-by-one: fires when count>=1 instead of >1",
    "m02": "header names matched case-sensitively",
    "m03": "OWS not trimmed before value compare",
    "m04": "content_type_present only when status==200 (not full 2xx)",
    "m05": "content_type_present needs a valued field (value-based, not name-based)",
    "m06": "nosniff compared case-sensitively",
    "m07": "any manifest fault -> exit 2 immediately (not per-check cne)",
    "m08": "hsts_present gate ignores the https flag",
    "m09": "Set-Cookie honored as an ordinary singleton",
    "m10": "field_name_syntax check disabled",
    "m11": "could_not_evaluate does not force exit 1",
    "m12": "singleton counted case-sensitively",
}

def run(mutant, case):
    env = dict(os.environ, MUTANT=mutant)
    p = subprocess.run([sys.executable, "-B", ENGINE,
                        os.path.join(FIX, case, "manifest.json")],
                       capture_output=True, text=True, env=env, timeout=30)
    out = (p.stdout + p.stderr).strip().splitlines()
    fcount = None
    for line in reversed(out):
        m = re.match(r"checks=\d+ findings=(\d+)", line)
        if m:
            fcount = int(m.group(1))
            break
    return p.returncode, fcount, out

def main():
    expected = json.load(open(os.path.join(ROOT, "expected.json")))
    rows = {}
    for case in CORE + ADDS:
        for mut in ["ref"] + MUTANTS:
            rows[(mut, case)] = run(mut, case)

    # 1) reference must reproduce the contract's expected column
    ref_bad = []
    for case in CORE:
        exp_exit, exp_f = expected[case]
        got_exit, got_f, _ = rows[("ref", case)]
        if case in ("H14", "H15"):
            if got_exit != exp_exit:
                ref_bad.append((case, exp_exit, got_exit))
        elif got_exit != exp_exit or got_f != exp_f:
            ref_bad.append((case, (exp_exit, exp_f), (got_exit, got_f)))

    # 2) kill matrix over the frozen 18
    kills = {}
    for mut in MUTANTS:
        kl = []
        for case in CORE:
            exp_exit, exp_f = expected[case]
            got_exit, got_f, _ = rows[(mut, case)]
            if case in ("H14", "H15"):
                dead = got_exit != exp_exit
            else:
                dead = got_exit != exp_exit or got_f != exp_f
            if dead:
                kl.append(case)
        kills[mut] = kl

    # 3) additions probe the survivors
    add_hits = {}
    for mut in MUTANTS:
        if kills[mut]:
            continue
        hit = []
        for case in ADDS:
            exp_exit, exp_f = expected[case]
            got_exit, got_f, _ = rows[(mut, case)]
            if got_exit != exp_exit or got_f != exp_f:
                hit.append(case)
        add_hits[mut] = hit

    print("== reference vs contract expected ==")
    print("OK" if not ref_bad else f"MISMATCH {ref_bad}")
    print("\n== kill matrix (frozen 18) ==")
    for mut in MUTANTS:
        print(f"{mut}  {','.join(kills[mut]) or 'SURVIVES'}")
    print("\n== additions vs survivors ==")
    for mut, hit in add_hits.items():
        print(f"{mut}  killed additionally by: {','.join(hit) or 'still survives'}")

    with open(os.path.join(ROOT, "results.json"), "w") as fh:
        json.dump({
            "ref_mismatch": ref_bad,
            "kills": kills,
            "addition_hits": add_hits,
            "raw": {f"{m}|{c}": rows[(m, c)][:2] for m in ["ref"] + MUTANTS
                    for c in CORE + ADDS},
            "mutant_desc": MUTANT_DESC,
        }, fh, indent=1)

if __name__ == "__main__":
    main()
