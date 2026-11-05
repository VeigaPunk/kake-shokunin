#!/usr/bin/env python3
"""MutCounters follow-ups: verify killing recipes for survivors + seed-doc check + M10 probe."""
import hashlib, importlib.util, json, os, random, re, shutil, subprocess, sys

sys.path.insert(0, "/fast/scratch/hyaku/kake-r98/MutCounters")
import battery as B

results = json.load(open(f"{B.OUT}/results.json"))
revs = results["fixtures"]
PRIS_CAP = f"{B.SCRATCH}/c98_captable_pristine.py"
PRIS_ST = f"{B.SCRATCH}/c98_stale_pristine.py"
OUTD = {}

def log(*a): print(*a, flush=True)

def mutant_from(counter, old, new, mid):
    srcp = PRIS_CAP if counter == "captable" else PRIS_ST
    src = open(srcp).read()
    n = src.count(old)
    assert n == 1, f"{mid}: site found {n}x"
    p = f"{B.MUTDIR}/{counter}_{mid}.py"
    open(p, "w").write(src.replace(old, new, 1))
    return p

def run_counter(path, args):
    return B.run_py(path, args)

# ---------------------------------------------------- 1. S14 seed-derivation doc check
fxpos = revs["c2-pos-oracle"]
pris_pos_line = [c for c in results["pristine_stale"] if c["check"] == "ctl-c2-slot-pos-oracle"][0]["observed"]
pris_seed = int(re.search(r"seed=(\d+)", pris_pos_line).group(1))
s14 = [c for c in results["results"] if c["counter"] == "stale" and c["mid"] == "S14"][0]
s14_pos = [c for c in s14["checks"] if c["check"] == "ctl-c2-slot-pos-oracle"][0]["observed"]
s14_seed = int(re.search(r"seed=(\d+)", s14_pos).group(1))
derived8 = int(hashlib.sha256(fxpos.encode()).hexdigest()[:8], 16)
derived4 = int(hashlib.sha256(fxpos.encode()).hexdigest()[:4], 16)
OUTD["S14_seeddoc"] = {"fixture_rev": fxpos, "doc_seed(sha[:8])": derived8,
                       "pristine_printed": pris_seed, "pristine_matches_doc": pris_seed == derived8,
                       "s14_printed": s14_seed, "s14_matches_doc": s14_seed == derived8,
                       "sha[:4]_value": derived4, "s14_equals_sha4": s14_seed == derived4}
log("S14 seeddoc:", OUTD["S14_seeddoc"])

# ---------------------------------------------------- 2. captable survivor killing fixtures
W8 = "covers the registry census rows offline for publishers"
FIXROWS = {
 "M01": f"| sources-registry; gate flavor | {W8} | `corpus/SOURCES.md` | 20 |",
 "M04": f"| sources-registry | {W8} | `corpus/SOURCES.md` | 20 (recount 21) |",
 "M06": "| sources-registry | covers registry census rows offline | `corpus/SOURCES.md` | 20 |",
 "M09": "| Conservative Vary-match reader | watches scripts/vary_match.py responses against frozen fixtures offline today | `corpus/SOURCES.md` | 88 |",
}
def cap_fixture(name, extra):
    B.sh([B.GIT, "-C", B.FX, "checkout", "-f", "--detach", B.INSTR])
    code = f'''
p = "SCORECARD.md"; t = open(p).read()
i = t.index("## Capabilities"); j = t.index("\\n\\n", t.index("| Capability |", i))
t = t[:j] + "\\n" + {extra!r} + t[j:]
open(p, "w").write(t)
'''
    subprocess.run([sys.executable, "-"], input=code.encode(), cwd=B.FX,
                   capture_output=True, env=B.ENV, check=True)
    B.sh([B.GIT, "-C", B.FX, "add", "-A"])
    B.sh([B.GIT, "-C", B.FX, "-c", "user.name=MutCounters",
          "-c", "user.email=MutCounters@example.invalid", "commit", "-qm", f"recipe {name}"])
    return B.sh([B.GIT, "-C", B.FX, "rev-parse", "HEAD"]).stdout.decode().strip()

OUTD["cap_recipes"] = {}
for mid, row in FIXROWS.items():
    rev = cap_fixture(mid, row)
    old, new = {
         "M01": ('CUTS = (" (", ": ", " - ", " — ", "; ")',
                 'CUTS = (" (", ": ", " - ", " — ")'),
         "M04": ('    m = re.search(r"\\d+", cell)\n    return int(m.group(0)) if m else None',
                 '    m = re.findall(r"\\d+", cell)\n    return int(m[-1]) if m else None'),
         "M06": ("    if len(cells[1].split()) < 8:",
                 "    if len(cells[1].split()) < 5:"),
         "M09": ("        if p not in line:",
                 "        if p not in cells[2]:"),
        }[mid]
    mutp = mutant_from("captable", old, new, mid)
    pr = run_counter(PRIS_CAP, ["--fleet", B.FLEET, "--fleet-revision", B.FREV,
                                "--root", B.FX, "--revision", rev])
    mr = run_counter(mutp, ["--fleet", B.FLEET, "--fleet-revision", B.FREV,
                            "--root", B.FX, "--revision", rev])
    OUTD["cap_recipes"][mid] = {"fixture_rev": rev, "row": row,
        "pristine": {"rc": pr["rc"], "l1": B.cap1_prefix(pr["l1"])},
        "mutant": {"rc": mr["rc"], "l1": B.cap1_prefix(mr["l1"])},
        "discriminates": pr["l1"] != mr["l1"]}
    log(f"recipe {mid}: pristine={B.cap1_prefix(pr['l1'])[:80]} mutant={B.cap1_prefix(mr['l1'])[:80]}")
    os.remove(mutp)

# M13 fixture: junkprose minus one row -> exactly 1 mismatch
B.sh([B.GIT, "-C", B.FX, "checkout", "-f", "--detach", B.INSTR])
subprocess.run([sys.executable, "-"], input=B.C1_BUILDERS["c1-junk"].encode(), cwd=B.FX,
               capture_output=True, env=B.ENV, check=True)
code = '''
p = "SCORECARD.md"; lines = open(p).read().split("\\n")
for k, l in enumerate(lines):
    if "| lorem ipsum dolor sit amet consectetur adipiscing elit |" in l:
        del lines[k]; break
open(p, "w").write("\\n".join(lines))
'''
subprocess.run([sys.executable, "-"], input=code.encode(), cwd=B.FX,
               capture_output=True, env=B.ENV, check=True)
B.sh([B.GIT, "-C", B.FX, "add", "-A"])
B.sh([B.GIT, "-C", B.FX, "-c", "user.name=MutCounters",
      "-c", "user.email=MutCounters@example.invalid", "commit", "-qm", "recipe M13"])
rev13 = B.sh([B.GIT, "-C", B.FX, "rev-parse", "HEAD"]).stdout.decode().strip()
mut13 = mutant_from("captable", '    met = res["mismatches"] == 0 and res["entries"] > 0',
                              '    met = res["mismatches"] <= 1 and res["entries"] > 0', "M13")
pr = run_counter(PRIS_CAP, ["--fleet", B.FLEET, "--fleet-revision", B.FREV,
                            "--root", B.FX, "--revision", rev13])
mr = run_counter(mut13, ["--fleet", B.FLEET, "--fleet-revision", B.FREV,
                         "--root", B.FX, "--revision", rev13])
OUTD["cap_recipes"]["M13"] = {"fixture_rev": rev13, "row": "junkprose fixture minus one row (mismatches=1)",
    "pristine": {"rc": pr["rc"], "l1": B.cap1_prefix(pr["l1"])},
    "mutant": {"rc": mr["rc"], "l1": B.cap1_prefix(mr["l1"])},
    "discriminates": (pr["rc"], mr["rc"]) == (1, 0)}
log(f"recipe M13: pristine rc={pr['rc']} {B.cap1_prefix(pr['l1'])[:70]} | mutant rc={mr['rc']} {B.cap1_prefix(mr['l1'])[:70]}")
os.remove(mut13)

# ---------------------------------------------------- 3. M10 equivalence probe (greedy vs augmenting)
def words_key(n, rng):
    return " ".join(rng.choice("abcdef") for _ in range(n))
def compat(a, b):
    if a == b: return True
    wa, wb = a.split(" "), b.split(" ")
    s, l = (wa, wb) if len(wa) <= len(wb) else (wb, wa)
    return len(s) >= 3 and l[:len(s)] == s
def probe(iters=200000):
    rng = random.Random(20261105)
    diffs = 0; example = None
    for _ in range(iters):
        ne = rng.randint(1, 6); nr = rng.randint(1, 6)
        ekeys = [words_key(rng.randint(1, 5), rng) for _ in range(ne)]
        rkeys = [words_key(rng.randint(1, 5), rng) for _ in range(nr)]
        adj = [[j for j in range(nr) if compat(ekeys[i], rkeys[j])] for i in range(ne)]
        # greedy: entries in order, rows in index order, no augmenting
        gr = [-1] * nr
        g = 0
        for i in range(ne):
            for j in adj[i]:
                if gr[j] == -1:
                    gr[j] = i; g += 1; break
        # augmenting
        ar = [-1] * nr
        def aug(i, seen):
            for j in adj[i]:
                if j in seen: continue
                seen.add(j)
                if ar[j] == -1 or aug(ar[j], seen):
                    ar[j] = i; return True
            return False
        a = sum(aug(i, set()) for i in range(ne))
        if g != a:
            diffs += 1
            if example is None:
                example = {"ekeys": ekeys, "rkeys": rkeys, "greedy": g, "aug": a}
    return {"iters": iters, "greedy_ne_max": diffs, "example": example}
OUTD["M10_probe"] = probe()
log("M10 probe:", OUTD["M10_probe"])

# ---------------------------------------------------- 4. stale oracle in-process demos (S02 S04 S17)
def load_mod(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    m = importlib.util.module_from_spec(spec); spec.loader.exec_module(m)
    return m
ST_SITES = {
 "S02": ('        if not name:\n            raise Refuse("bad directive name")',
         "        if not name:\n            continue"),
 "S04": ("    return min(int(v[1]), CLAMP)", "    return int(v[1])"),
 "S17": ('        if err != "network" and not (isinstance(err, int) and not isinstance(err, bool) and 100 <= err <= 599):',
         '        if err != "network" and not (isinstance(err, int) and not isinstance(err, bool) and 200 <= err <= 599):'),
}
mp = {mid: mutant_from("stale", *pair, mid) for mid, pair in ST_SITES.items()}
mods = {mid: load_mod(p, f"mut_{mid}") for mid, p in mp.items()}
pris = load_mod(PRIS_ST, "pris_st")
CAND = f"{B.FROZEN}/pos-oracle.py"
def cand_out(case):
    p = subprocess.run(["python3", "-I", "-B", CAND], input=json.dumps(case).encode(),
                       capture_output=True, cwd=B.RUN,
                       env={"PATH": "/usr/bin:/bin", "LC_ALL": "C", "HOME": B.RUN})
    return {"rc": p.returncode, "out": p.stdout.decode().strip(), "err": p.stderr.decode().strip()[:60]}
DEMOS = {
 "S02": {"case": {"response_cc": "a=1, =2", "freshness_lifetime": 1, "current_age": 2, "event": "request"},
         "expect": "REFUSE"},
 "S04": {"case": {"response_cc": "stale-while-revalidate=99999999999", "freshness_lifetime": 0,
                  "current_age": 3000000000, "event": "request"},
         "expect": None},
 "S17": {"case": {"response_cc": "max-age=600, stale-if-error=1200", "freshness_lifetime": 600,
                  "current_age": 900, "event": "error", "error": 150},
         "expect": None},
}
OUTD["oracle_demos"] = {}
for mid, d in DEMOS.items():
    pris_e = pris.expect(dict(d["case"]))
    mut_e = mods[mid].expect(dict(d["case"]))
    cand = cand_out(d["case"])
    OUTD["oracle_demos"][mid] = {"case": d["case"], "pristine_expect": str(pris_e),
                                 "mutant_expect": str(mut_e), "pos_oracle_candidate": cand,
                                 "discriminates": pris_e != mut_e}
    log(f"demo {mid}: pristine={pris_e!r} mutant={mut_e!r} candidate={cand}")
for p in mp.values(): os.remove(p)

# ---------------------------------------------------- 5. judge-survivor candidate-file demos + S10b battery
PO = open(f"{B.FROZEN}/pos-oracle.py").read()
def recipe_candidate(name, old, new):
    assert PO.count(old) == 1, (name, PO.count(old))
    p = f"{B.RUN}/cand_{name}.py"
    open(p, "w").write(PO.replace(old, new, 1))
    return p
CANDS = {
 "extrakey": ('    sys.stdout.write(json.dumps(out) + "\\n")',
              '    out2 = dict(out); out2["note"] = "x"\n    sys.stdout.write(json.dumps(out2) + "\\n")'),
 "floatstale": ('    sys.stdout.write(json.dumps(out) + "\\n")',
                '    out["staleness"] = float(out["staleness"])\n    sys.stdout.write(json.dumps(out) + "\\n")'),
 "oddstderr": ('        sys.stderr.write("invalid_input: %s\\n" % e)',
               '        sys.stderr.write("rejected: %s\\n" % e)'),
 "exit2": ('        sys.stderr.write("invalid_input: %s\\n" % e)\n        return 1',
           '        sys.stderr.write("invalid_input: %s\\n" % e)\n        return 2'),
}
JMUT = {
 "S10b": ('        o == {"decision": want[0], "staleness": want[1]} and type(o["staleness"]) is int',
          '        all(o.get(k) == v for k, v in {"decision": want[0], "staleness": want[1]}.items())', "extrakey"),
 "S11": (None, None, "floatstale"),
 "S12": (None, None, "oddstderr"),
 "S13": (None, None, "exit2"),
}
pris_line_lu = results["pristine_neglookup_line"]
OUTD["judge_demos"] = {}
for mid, (old, new, candname) in JMUT.items():
    if mid == "S10b":
        mutp = mutant_from("stale", old, new, mid)
    elif mid == "S11":
        mutp = mutant_from("stale",
            '        o == {"decision": want[0], "staleness": want[1]} and type(o["staleness"]) is int',
            '        o == {"decision": want[0], "staleness": want[1]}', mid)
    elif mid == "S12":
        mutp = mutant_from("stale",
            '        return rcode == 1 and out == "" and err.startswith("invalid_input:")',
            '        return rcode == 1 and out == "" and err != ""', mid)
    elif mid == "S13":
        mutp = mutant_from("stale",
            '        return rcode == 1 and out == "" and err.startswith("invalid_input:")',
            '        return rcode != 0 and out == "" and err.startswith("invalid_input:")', mid)
    cp = recipe_candidate(candname, *CANDS[candname])
    pr = run_counter(PRIS_ST, ["--work", B.RUN, "--candidate-file", cp, "--seed", "98"])
    mr = run_counter(mutp, ["--work", B.RUN, "--candidate-file", cp, "--seed", "98"])
    OUTD["judge_demos"][mid] = {"candidate": candname,
        "pristine": {"rc": pr["rc"], "l1": pr["l1"][:150]},
        "mutant": {"rc": mr["rc"], "l1": mr["l1"][:150]},
        "discriminates": (pr["rc"] != mr["rc"]) or ("met=true" in pr["l1"]) != ("met=true" in mr["l1"])}
    log(f"judge demo {mid} [{candname}]: pristine rc={pr['rc']} met={'met=true' in pr['l1']} | "
        f"mutant rc={mr['rc']} met={'met=true' in mr['l1']}")
    os.remove(cp)
    if mid == "S10b":
        checks = B.stale_checks(mutp, revs, {"neg-lookup": pris_line_lu})
        killers = [n for n, ok, _ in checks if not ok]
        OUTD["judge_demos"][mid]["battery_killers"] = killers
        log(f"S10b full battery killers: {killers}")
    os.remove(mutp)

json.dump(OUTD, open(f"{B.OUT}/followup.json", "w"), indent=1)
log("FOLLOWUP DONE")
