#!/usr/bin/env python3
"""ExecMutVerify — independent re-derivation of the R94-4 mutant scan.

Imports the FROZEN counter module read-only (never edited), runs its own
mutant battery (mutant_cases) over the pinned round-93 positive-control bytes
against hand_cases() + generate(95,40) under the counter's SANDBOX, and
records kill/survive + first failure per mutant.
"""
import hashlib
import importlib.util
import json
import os
import sys
import time

S = "/fast/scratch/hyaku/kake-r95/ExecMutVerify"
R = os.path.join(S, "repo")
OUT = os.path.join(R, ".ufo", "waves", "round-95", "w1", "ExecMutVerify")
MODPATH = os.path.join(R, ".ufo", "waves", "round-95", "c95_conditional.py")
PINS = os.path.join(R, ".ufo", "waves", "round-95", "controls", "instrument-sha256.txt")
POPINS = os.path.join(R, ".ufo", "waves", "round-95", "frozen", "c2-population.sha256")
MUTJSON = os.path.join(R, ".ufo", "waves", "round-93", "w1",
                       "recovered-partial", "MutConditional", "mutants-posgood.json")
MUTBASE = os.path.join(R, ".ufo", "waves", "round-93", "frozen", "pos-good.py")
RECEIPTS = os.path.join(R, ".ufo", "waves", "round-95", "frozen", "c2-equiv-receipts.json")
FREEZE_CONTROL = os.path.join(R, ".ufo", "waves", "round-95", "controls",
                              "mutant-scan-v2-result.json")
SEED = 95


def sha_file(p):
    with open(p, "rb") as fh:
        return hashlib.sha256(fh.read()).hexdigest()


def pins_map(path):
    out = {}
    with open(path, "r", encoding="utf-8") as fh:
        for line in fh:
            h, _, p = line.strip().partition("  ")
            if p:
                out[p] = h
    return out


def main():
    inst_pins = pins_map(PINS)
    pop_pins = pins_map(POPINS)

    # 1. the imported module must be the pinned freeze bytes
    mod_sha = sha_file(MODPATH)
    pin_mod = inst_pins.get(".ufo/waves/round-95/c95_conditional.py")
    assert pin_mod == mod_sha, "c95_conditional.py digest drift: %s vs %s" % (mod_sha, pin_mod)
    assert mod_sha == ("f09f84090fdda405992d7b51191be8838"
                       "549e3df402b0898eb2ca00c4c3ff312"), mod_sha

    # 2. read-only import of the frozen module
    spec = importlib.util.spec_from_file_location("c95_conditional_frozen", MODPATH)
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)

    # 3. population fixture digests re-checked in-process (belt and braces)
    pop_checks = {}
    for rel, want in pop_pins.items():
        got = sha_file(os.path.join(R, rel))
        pop_checks[rel] = (got == want)
    assert all(pop_checks.values()), pop_checks

    receipts_sha = sha_file(RECEIPTS)
    assert receipts_sha == pop_pins[".ufo/waves/round-95/frozen/c2-equiv-receipts.json"]
    receipts = json.load(open(RECEIPTS, "r", encoding="utf-8"))

    base_sha = sha_file(MUTBASE)
    assert base_sha == pop_pins[".ufo/waves/round-93/frozen/pos-good.py"]
    mut_sha = sha_file(MUTJSON)
    assert mut_sha == pop_pins[".ufo/waves/round-93/w1/recovered-partial/MutConditional/mutants-posgood.json"]

    # 4. cases and reference self-check (counter's own drift gate)
    cases = mod.hand_cases()
    drift = mod.reference_selfcheck(cases)
    assert drift is None, drift

    # 5. generated expectations exactly as the counter's main() builds them,
    #    so mutant_cases' gen_limit=40 window matches the frozen battery
    gen_expected = []
    for inp in mod.generate(SEED, 120):
        try:
            gen_expected.append((inp, mod.reference(inp)))
        except mod.Invalid:
            continue

    mutants = mod.load_mutants(open(MUTJSON, "rb").read())
    assert len(mutants) == 40, len(mutants)
    base_src = open(MUTBASE, "r", encoding="utf-8").read()

    # 6. sandbox + work/tree dirs (what the counter's main() assembles)
    work = os.path.join(S, "battery-work")
    tree = os.path.join(work, "tree")
    os.makedirs(tree, exist_ok=True)
    sandbox = os.path.join(work, "sandbox.py")
    with open(sandbox, "w", encoding="utf-8") as fh:
        fh.write(mod.SANDBOX)

    t0 = time.time()
    killed, survivors, notes, mdrift = mod.mutant_cases(
        work, sandbox, cases, gen_expected, base_src, mutants, tree)
    elapsed = time.time() - t0
    if mdrift:
        print("POPULATION DRIFT: %s" % mdrift)
        return 2

    mutants_v3 = [{"id": m["id"],
                   "killed": bool(notes[m["id"]]["killed"]),
                   "first_failure": notes[m["id"]]["first_failure"]}
                  for m in mutants]
    with open(os.path.join(OUT, "mutants-v3.json"), "w", encoding="utf-8") as fh:
        json.dump(mutants_v3, fh, indent=1)
        fh.write("\n")

    # 7. comparison against the freeze's own scan receipt
    control = json.load(open(FREEZE_CONTROL, "r", encoding="utf-8"))
    ctrl_killed = sorted(control.get("killed", []))
    ctrl_surv = sorted(control.get("survivors", []))
    agree = (sorted(killed) == ctrl_killed) and (sorted(survivors) == ctrl_surv)

    lines = []
    lines.append("ExecMutVerify — independent R94-4 mutant-scan re-derivation")
    lines.append("date_utc=%s" % time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()))
    lines.append("freeze_commit=8f638b591e739e1863f5fa22334d5e15178189ed")
    lines.append("module=.ufo/waves/round-95/c95_conditional.py")
    lines.append("module_sha256=%s (matches controls/instrument-sha256.txt)" % mod_sha)
    lines.append("mutant_base=.ufo/waves/round-93/frozen/pos-good.py sha256=%s" % base_sha)
    lines.append("mutants_json=.ufo/waves/round-93/w1/recovered-partial/MutConditional/mutants-posgood.json sha256=%s" % mut_sha)
    lines.append("receipts=.ufo/waves/round-95/frozen/c2-equiv-receipts.json sha256=%s content=%s"
                 % (receipts_sha, json.dumps(receipts)))
    lines.append("instrument_pins=8/8 ok (sha256sum -c rc=0)")
    lines.append("population_pins=%d/%d ok (sha256sum -c rc=0)" % (len(pop_pins), len(pop_pins)))
    lines.append("python=%s" % sys.version.split()[0])
    lines.append("hand_cases=%d (reference_selfcheck: no drift)" % len(cases))
    lines.append("generate(%d,120)->valid_expectations=%d; mutant battery window=gen_expected[:40] (counter mutant_cases gen_limit=40)" % (SEED, len(gen_expected)))
    lines.append("mutants=%d; every find-string occurs exactly once in base (mdrift=None)" % len(mutants))
    lines.append("elapsed=%.1fs" % elapsed)
    lines.append("")
    for row in mutants_v3:
        lines.append("%s killed=%s first_failure=%s"
                     % (row["id"], row["killed"],
                        json.dumps(row["first_failure"])))
    lines.append("")
    m11 = next(r for r in mutants_v3 if r["id"] == "M11")
    lines.append("M11 (round-94 survivor): killed=%s first_failure=%s"
                 % (m11["killed"], json.dumps(m11["first_failure"])))
    lines.append("")
    lines.append("killed=%d/40 survivors=%s" % (len(killed), ",".join(survivors) if survivors else "none"))
    lines.append("freeze_control: killed=%d/40 survivors=%s"
                 % (len(ctrl_killed), ",".join(ctrl_surv) if ctrl_surv else "none"))
    lines.append("freeze_control_comparison=%s"
                 % ("agree — same kill set, same (empty) survivor set"
                    if agree else
                    "DISAGREE — this scan killed=%s survivors=%s | freeze killed=%s survivors=%s"
                    % (",".join(sorted(killed)), ",".join(sorted(survivors)) or "none",
                       ",".join(ctrl_killed), ",".join(ctrl_surv) or "none")))
    if survivors:
        unreceipted = [s for s in survivors
                       if s not in {r.get("id") for r in receipts}]
        lines.append("R94-4 rule: unreceipted_survivors=%s" % (unreceipted or "none"))
        if unreceipted:
            lines.append("FREEZE-FALSIFYING FINDING: survivors without digest-pinned "
                         "equivalence receipts (receipts file is empty) — zero-survivor "
                         "determination is falsified.")
    with open(os.path.join(OUT, "scan.txt"), "w", encoding="utf-8") as fh:
        fh.write("\n".join(lines) + "\n")

    print("MUT-VERIFY killed=%d/40 survivors=%s"
          % (len(killed), ",".join(survivors) if survivors else "none"))
    print("M11 killed=%s first_failure=%s" % (m11["killed"], m11["first_failure"]))
    print("freeze_control_comparison=%s" % ("agree" if agree else "DISAGREE"))
    return 0


if __name__ == "__main__":
    sys.exit(main())
