#!/usr/bin/env python3
"""MutCounters seat battery — kake round 98 (hyaku run 15, attempt 1).

Mutation-tests the two frozen round-98 counters' own batteries:
  c98_captable.py (C1) and c98_stale.py (C2), pinned by controls/instrument-sha256.txt.

Detector per mutant (bounded, same for pristine and mutants):
  captable: --selftest; base-c1; instr-c1; ctl-c1-forgery-namesonly/mega/junkprose
            (fixtures reproduced from controls.sh builders in this seat's scratch clone).
  stale:    --selftest; base-c2; instr-c2; ctl-c2-slot-{pos-oracle,6 negs}
            (fixtures reproduced from controls.sh; hand counts and met/exit are
             seed-independent; generated/refusals compared to pristine-observed on
             the same fixture revision since the default seed derives from it);
             seed derivation checked against the counter's documented contract.

Writes OUT/results.json. Fixtures live only in this seat's scratch; one live clone.
"""
import concurrent.futures as cf
import hashlib, json, os, re, shutil, subprocess, sys, time

LANE   = "/home/vgpnk/Projects/shokunin/kake-shokunin"
FLEET  = "/home/vgpnk/Projects/shokunin"
WAVE   = f"{LANE}/.ufo/waves/round-98"
FROZEN = f"{WAVE}/frozen"
SCRATCH = "/fast/scratch/hyaku/kake-r98/MutCounters"
OUT    = f"{SCRATCH}/out"
MUTDIR = f"{SCRATCH}/mutants"
RUN    = f"{SCRATCH}/run"
FX     = f"{SCRATCH}/fx"
BASE   = "e51328b63690c8aaa78c9c8f3b87d8735c0ccbf7"
INSTR  = "2db768356cd081092c3abc60f76b25487ec4c535"
FREV   = "f86740064229897f53212e03ae3b6474dac66de4"
GIT    = "/usr/bin/git"
ENV    = dict(os.environ, GIT_NO_REPLACE_OBJECTS="1", LC_ALL="C", TMPDIR=RUN)

def log(*a):
    print(*a, flush=True)

def sh(args, cwd=None, check=True):
    p = subprocess.run(args, cwd=cwd, capture_output=True, env=ENV)
    if check and p.returncode != 0:
        raise RuntimeError(f"cmd {args} rc={p.returncode}: {p.stderr.decode()[:400]}")
    return p

# ------------------------------------------------------------------ mutants
CAP = []
def cm(mid, site, old, new): CAP.append((mid, site, old, new, 1))

cm("M01", "key() CUTS cut list",
   'CUTS = (" (", ": ", " - ", " — ", "; ")',
   'CUTS = (" (", ": ", " - ", " — ")')
cm("M02", "key_ok() word-prefix floor 3->2",
   "    return len(short) >= 3 and long_[:len(short)] == short",
   "    return len(short) >= 2 and long_[:len(short)] == short")
cm("M03", "key_ok() prefix -> suffix compare",
   "    return len(short) >= 3 and long_[:len(short)] == short",
   "    return len(short) >= 3 and long_[-len(short):] == short")
cm("M04", "first_int() first -> last integer",
   '    m = re.search(r"\\d+", cell)\n    return int(m.group(0)) if m else None',
   '    m = re.findall(r"\\d+", cell)\n    return int(m[-1]) if m else None')
cm("M05", "compatible() word floor 8->9",
   "    if len(cells[1].split()) < 8:",
   "    if len(cells[1].split()) < 9:")
cm("M06", "compatible() word floor 8->5",
   "    if len(cells[1].split()) < 8:",
   "    if len(cells[1].split()) < 5:")
cm("M07", "compatible() evidence existence any->all",
   "    if not any(exists(p) for p in evidence_paths(cells[2])):",
   "    if not all(exists(p) for p in evidence_paths(cells[2])):")
cm("M08", "compatible() entry-path containment veto dropped",
   '    for p in entry_paths(e["text"]):\n        if p not in line:\n            return False\n    return True',
   '    for p in entry_paths(e["text"]):\n        if p not in line:\n            continue\n    return True')
cm("M09", "compatible() containment line -> evidence cell only",
   "        if p not in line:",
   "        if p not in cells[2]:")
cm("M10", "max_match() augmenting recursion dropped (greedy)",
   "            if match_r[j] == -1 or aug(match_r[j], seen):",
   "            if match_r[j] == -1:")
cm("M11", "population() round cap >= -> >",
   "        if r >= ROUND_CAP:",
   "        if r > ROUND_CAP:")
cm("M12", "population() admitted filter widened (False admitted)",
   '        if x.get("admitted") not in (True, "True", "true"):',
   '        if x.get("admitted") not in (True, "True", "true", False):')
cm("M13", "line1() met threshold ==0 -> <=1",
   '    met = res["mismatches"] == 0 and res["entries"] > 0',
   '    met = res["mismatches"] <= 1 and res["entries"] > 0')

ST = []
def sm(mid, site, old, new): ST.append((mid, site, old, new, 1))

sm("S01", "parse_cc() first-occurrence -> last",
   "        n = name.lower()\n        if n not in out:\n            out[n] = val",
   "        n = name.lower()\n        out[n] = val")
sm("S02", "parse_cc() empty directive name allowed",
   '        if not name:\n            raise Refuse("bad directive name")',
   "        if not name:\n            continue")
sm("S03", "delta() quoted value accepted",
   '    if v is None or v[0] != "t" or not v[1].isdigit() or not v[1].isascii():',
   "    if v is None or not v[1].isdigit() or not v[1].isascii():")
sm("S04", "delta() 2^31 clamp dropped",
   "    return min(int(v[1]), CLAMP)",
   "    return int(v[1])")
sm("S05", "decide() must-revalidate prohibition dropped",
   '    prohibited = ("no-cache" in rc or "must-revalidate" in rc or "no-cache" in qc or\n                  (sh and ("proxy-revalidate" in rc or "s-maxage" in rc)))',
   '    prohibited = ("no-cache" in rc or "no-cache" in qc or\n                  (sh and ("proxy-revalidate" in rc or "s-maxage" in rc)))')
sm("S06", "decide() shared gate and -> or (proxy-revalidate blocks private)",
   '                  (sh and ("proxy-revalidate" in rc or "s-maxage" in rc)))',
   '                  (sh or ("proxy-revalidate" in rc or "s-maxage" in rc)))')
sm("S07", "decide() rule order: fresh before not-an-error",
   '    st = max(0, A - L)\n    if ev == "error" and err not in ERRS:\n        return {"decision": "not-an-error", "staleness": st}\n    if A < L and "no-cache" not in rc and "no-cache" not in qc:\n        return {"decision": "fresh", "staleness": st}',
   '    st = max(0, A - L)\n    if A < L and "no-cache" not in rc and "no-cache" not in qc:\n        return {"decision": "fresh", "staleness": st}\n    if ev == "error" and err not in ERRS:\n        return {"decision": "not-an-error", "staleness": st}')
sm("S08", "decide() swr boundary inclusive -> exclusive",
   "        ok = not prohibited and w is not None and st <= w",
   "        ok = not prohibited and w is not None and st < w")
sm("S09", "decide() sie precedence request-first -> response-first",
   '    e = delta(qc, "stale-if-error")\n    if e is None:\n        e = delta(rc, "stale-if-error")',
   '    e = delta(rc, "stale-if-error")\n    if e is None:\n        e = delta(qc, "stale-if-error")')
sm("S10", "judge() extra output keys accepted",
   '    return isinstance(o, dict) and set(o) == {"decision", "staleness"} and \\',
   '    return isinstance(o, dict) and set(o) <= {"decision", "staleness"} and \\')
sm("S11", "judge() staleness type check dropped (float ok)",
   '        o == {"decision": want[0], "staleness": want[1]} and type(o["staleness"]) is int',
   '        o == {"decision": want[0], "staleness": want[1]}')
sm("S12", "judge() refusal stderr prefix any",
   '        return rcode == 1 and out == "" and err.startswith("invalid_input:")',
   '        return rcode == 1 and out == "" and err != ""')
sm("S13", "judge() refusal exit code any nonzero",
   '        return rcode == 1 and out == "" and err.startswith("invalid_input:")',
   '        return rcode != 0 and out == "" and err.startswith("invalid_input:")')
sm("S14", "main() default seed sha256[:8] -> [:4]",
   "        seed = a.seed if a.seed is not None else int(hashlib.sha256(seed_src.encode()).hexdigest()[:8], 16)",
   "        seed = a.seed if a.seed is not None else int(hashlib.sha256(seed_src.encode()).hexdigest()[:4], 16)")
sm("S15", "decide() fresh boundary A<L -> A<=L",
   '    if A < L and "no-cache" not in rc and "no-cache" not in qc:',
   '    if A <= L and "no-cache" not in rc and "no-cache" not in qc:')
sm("S16", "decide() staleness max(0,..) dropped",
   "    st = max(0, A - L)",
   "    st = A - L")
sm("S17", "decide() error status range 100..599 -> 200..599",
   "        if err != \"network\" and not (isinstance(err, int) and not isinstance(err, bool) and 100 <= err <= 599):",
   "        if err != \"network\" and not (isinstance(err, int) and not isinstance(err, bool) and 200 <= err <= 599):")
sm("S18", "decide() sie boundary inclusive -> exclusive",
   "    ok = not prohibited and e is not None and st <= e",
   "    ok = not prohibited and e is not None and st < e")
sm("S19", "decide() unknown-key refusal dropped",
   "    if set(inp) - allowed:",
   "    if set(inp) - set():")

# ------------------------------------------------------------------ fixtures
C1_BUILDERS = {
"c1-namesonly": r'''
import re, sys
sys.path.insert(0, "/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-98")
import gen_cap_rows as g
p = "SCORECARD.md"; t = open(p).read()
i = t.index("## Capabilities"); j = t.index("\n\n", t.index("| Capability |", i))
rows = "".join(f"\n| {c} | can do it | none | {r} |" for r, c, w, e in g.ROWS)
open(p, "w").write(t[:j] + rows + t[j:])
''',
"c1-mega": r'''
import sys
sys.path.insert(0, "/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-98")
import gen_cap_rows as g
p = "SCORECARD.md"; t = open(p).read()
i = t.index("## Capabilities"); j = t.index("\n\n", t.index("| Capability |", i))
names = "; ".join(c for r, c, w, e in g.ROWS)
paths = " ".join(f"`{x}`" for r, c, w, e in g.ROWS for x in __import__("re").findall(r"`([^`]+)`", e))
row = f"\n| two gate registry rows in SKILL.md | {names} | {paths} | 52 |"
open(p, "w").write(t[:j] + row + t[j:])
''',
"c1-junk": r'''
import re, sys
sys.path.insert(0, "/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-98")
import gen_cap_rows as g
p = "SCORECARD.md"; t = open(p).read()
i = t.index("## Capabilities"); j = t.index("\n\n", t.index("| Capability |", i))
rows = "".join(f"\n| {c} | lorem ipsum dolor sit amet consectetur adipiscing elit | {e} | {r} |" for r, c, w, e in g.ROWS)
t = t[:j] + rows + t[j:]
t = t.replace("| Curated source registry |", "| Sources-registry (curated source registry) |")
for name in ("Offline link-preview (Open Graph) audit", "Link-preview audit, round-35 contract",
             "Offline robots.txt expectation audit", "Offline response-header expectation audit",
             "Standalone retained-span quote classifier (round-64 re-entry)"):
    t = re.sub(r"\n\| " + re.escape(name) + r" \|[^\n]*", "", t, count=1)
open(p, "w").write(t)
''',
}
C2_SUBJECTS = ["pos-oracle", "neg-constant", "neg-lookup", "neg-noprohibit",
               "neg-exclusive", "neg-respsie", "neg-lenient"]

def build_fixtures():
    if os.path.exists(FX):
        shutil.rmtree(FX)
    sh([GIT, "clone", "-q", "--shared", LANE, FX])
    top = sh([GIT, "-C", FX, "rev-parse", "--show-toplevel"]).stdout.decode().strip()
    assert top == FX, f"toplevel mismatch: {top} != {FX}"
    log(f"fixture clone ok toplevel={top}")
    revs = {}
    def fixture(name):
        sh([GIT, "-C", FX, "checkout", "-f", "--detach", INSTR])
        return None
    for name, code in C1_BUILDERS.items():
        fixture(name)
        subprocess.run([sys.executable, "-"], input=code.encode(), cwd=FX,
                       capture_output=True, env=ENV, check=True)
        sh([GIT, "-C", FX, "add", "-A"])
        sh([GIT, "-C", FX, "-c", "user.name=MutCounters",
            "-c", "user.email=MutCounters@example.invalid", "commit", "-qm", f"control {name}"])
        revs[name] = sh([GIT, "-C", FX, "rev-parse", "HEAD"]).stdout.decode().strip()
        log(f"fixture {name} -> {revs[name]}")
    for subj in C2_SUBJECTS:
        name = f"c2-{subj}"
        fixture(name)
        if os.path.exists(f"{FX}/scripts"):
            shutil.rmtree(f"{FX}/scripts")
        os.makedirs(f"{FX}/scripts")
        shutil.copyfile(f"{FROZEN}/{subj}.py", f"{FX}/scripts/stale_extensions.py")
        sh([GIT, "-C", FX, "add", "-A"])
        sh([GIT, "-C", FX, "-c", "user.name=MutCounters",
            "-c", "user.email=MutCounters@example.invalid", "commit", "-qm", f"control {name}"])
        revs[name] = sh([GIT, "-C", FX, "rev-parse", "HEAD"]).stdout.decode().strip()
        log(f"fixture {name} -> {revs[name]}")
    return revs

# ------------------------------------------------------------------ checks
def run_py(path, args):
    p = subprocess.run(["python3", "-B", path, *args], capture_output=True, env=ENV)
    out = p.stdout.decode("utf-8", "replace")
    lines = [l for l in out.splitlines() if l.strip()]
    l1 = lines[0] if lines else ""
    last = lines[-1] if lines else ""
    return {"rc": p.returncode, "l1": l1, "last": last, "out": out[:2000]}

def cap1_prefix(l1):
    return l1.split(" revision=")[0]

def captable_checks(path, revs, base_exp):
    checks = []
    r = run_py(path, ["--selftest"])
    checks.append(("selftest", r["rc"] == 0 and r["last"] == "selftest 16/16",
                   f"rc={r['rc']} last={r['last']!r}"))
    for name, rev, exp, rcexp in [
        ("base-c1", BASE, base_exp, 1),
        ("instr-c1", INSTR, base_exp, 1),
        ("ctl-c1-forgery-namesonly", revs["c1-namesonly"],
         "entries=48 rows=53 matched=8 unlisted=40 unbacked=45 mismatches=85 met=false", 1),
        ("ctl-c1-forgery-mega", revs["c1-mega"],
         "entries=48 rows=15 matched=9 unlisted=39 unbacked=6 mismatches=45 met=false", 1),
        ("ctl-c1-forgery-junkprose", revs["c1-junk"],
         "entries=48 rows=48 matched=48 unlisted=0 unbacked=0 mismatches=0 met=true", 0),
    ]:
        root = LANE if name in ("base-c1", "instr-c1") else FX
        r = run_py(path, ["--fleet", FLEET, "--fleet-revision", FREV,
                          "--root", root, "--revision", rev])
        got = cap1_prefix(r["l1"])
        checks.append((name, got == exp and r["rc"] == rcexp,
                       f"rc={r['rc']} l1={got!r}"))
    return checks

NEG_HAND = {"neg-constant": "hand=14/60", "neg-lookup": "hand=60/60",
            "neg-noprohibit": "hand=52/60", "neg-exclusive": "hand=56/60",
            "neg-respsie": "hand=57/60", "neg-lenient": "hand=56/60"}

def stale_slot(path, rev, expect_seed_of=None):
    r = run_py(path, ["--work", RUN, "--root", FX, "--revision", rev])
    m = re.search(r"seed=(\d+)", r["l1"])
    seed_ok = None
    if m and expect_seed_of:
        seed_ok = (int(m.group(1)) == int(hashlib.sha256(expect_seed_of.encode()).hexdigest()[:8], 16))
    return r, (int(m.group(1)) if m else None), seed_ok

def stale_checks(path, revs, pristine_slot):
    checks = []
    r = run_py(path, ["--selftest"])
    ok = r["rc"] == 0 and r["last"] == "selftest ok" and r["l1"].startswith("hand-oracle 60/60")
    checks.append(("selftest", ok, f"rc={r['rc']} l1={r['l1'][:120]!r} last={r['last']!r}"))
    for name, rev in [("base-c2", BASE), ("instr-c2", INSTR)]:
        r = run_py(path, ["--work", RUN, "--root", LANE, "--revision", rev])
        ok = r["rc"] == 1 and "candidate=absent" in r["l1"] and "met=false" in r["l1"]
        checks.append((name, ok, f"rc={r['rc']} l1={r['l1'][:120]!r}"))
    for subj in C2_SUBJECTS:
        name = f"ctl-c2-slot-{subj}"
        r, seed, seed_ok = stale_slot(path, revs[f"c2-{subj}"])
        if subj == "pos-oracle":
            ok = (r["rc"] == 0 and "met=true" in r["l1"] and "hand=60/60" in r["l1"]
                  and "generated=240/240" in r["l1"])
            if seed_ok is False:
                ok = False
            det = f"rc={r['rc']} l1={r['l1'][:160]!r} seeddoc={seed_ok}"
        else:
            ok = r["rc"] == 1 and "met=false" in r["l1"] and NEG_HAND[subj] in r["l1"]
            det = f"rc={r['rc']} l1={r['l1'][:160]!r}"
            if ok and subj == "neg-lookup" and "neg-lookup" in pristine_slot:
                p = pristine_slot["neg-lookup"]
                mg = re.search(r"generated=(\d+)/(\d+) refusals=(\d+)/(\d+)", r["l1"])
                pg = re.search(r"generated=(\d+)/(\d+) refusals=(\d+)/(\d+)", p)
                if mg and pg and mg.groups() != pg.groups():
                    ok = False
                    det += f" counts-changed pristine={pg.groups()} mutant={mg.groups()}"
        checks.append((name, ok, det))
    return checks

# ------------------------------------------------------------------ battery
def battery(item):
    counter, mid, site, old, new, cnt, revs, base_exp, pristine_slot = item
    srcp = f"{SCRATCH}/{'c98_captable_pristine.py' if counter == 'captable' else 'c98_stale_pristine.py'}"
    src = open(srcp).read()
    found = src.count(old)
    if found != cnt:
        return {"counter": counter, "mid": mid, "verdict": "inconclusive",
                "error": f"mutation site found {found}x, expected {cnt}"}
    mp = f"{MUTDIR}/{counter}_{mid}.py"
    open(mp, "w").write(src.replace(old, new, cnt))
    t0 = time.time()
    if counter == "captable":
        checks = captable_checks(mp, revs, base_exp)
    else:
        checks = stale_checks(mp, revs, pristine_slot)
    killers = [n for n, ok, _ in checks if not ok]
    verdict = "killed" if killers else "survived"
    os.remove(mp)
    return {"counter": counter, "mid": mid, "site": site,
            "mutation": f"{old.strip()[:90]!r} -> {new.strip()[:90]!r}",
            "verdict": verdict, "killers": killers,
            "checks": [{"check": n, "ok": ok, "observed": det} for n, ok, det in checks],
            "secs": round(time.time() - t0, 1)}

def main():
    os.makedirs(OUT, exist_ok=True)
    # 0. pin check
    pins = {}
    for name, want in [("c98_captable.py", "efd598575c6e377ac76c68c876c96449bf80dc0e4b2fbf8c0436205167ac7cf3"),
                       ("c98_stale.py", "e0331e56378fb5acabe4447a37590cbf3273537aabd8c8d88f842e0a434a9f3f")]:
        data = open(f"{WAVE}/{name}", "rb").read()
        got = hashlib.sha256(data).hexdigest()
        assert got == want, f"digest mismatch {name}"
        shutil.copyfile(f"{WAVE}/{name}", f"{SCRATCH}/{name.replace('.py', '_pristine.py')}")
        pins[name] = got
    log("instrument digests verified:", pins)
    lane_master = sh([GIT, "-C", LANE, "rev-parse", "master"]).stdout.decode().strip()
    log("lane master:", lane_master)
    # 1. fixtures
    revs = build_fixtures()
    base_exp = "entries=48 rows=14 matched=8 unlisted=40 unbacked=6 mismatches=46 met=false"
    # 2. pristine baseline
    log("== pristine baseline ==")
    pc = captable_checks(f"{SCRATCH}/c98_captable_pristine.py", revs, base_exp)
    for n, ok, det in pc:
        log(f"  captable {n}: {'ok' if ok else 'FAIL'} {det}")
    assert all(ok for _, ok, _ in pc), "pristine captable baseline failed"
    pristine_slot = {}
    ps = stale_checks(f"{SCRATCH}/c98_stale_pristine.py", revs, pristine_slot)
    for n, ok, det in ps:
        log(f"  stale {n}: {'ok' if ok else 'FAIL'} {det}")
    assert all(ok for _, ok, _ in ps), "pristine stale baseline failed"
    rl, _, _ = stale_slot(f"{SCRATCH}/c98_stale_pristine.py", revs["c2-neg-lookup"])
    pristine_slot["neg-lookup"] = rl["l1"]
    # 3. mutants
    items = ([("captable", *m, revs, base_exp, pristine_slot) for m in CAP] +
             [("stale", *m, revs, base_exp, pristine_slot) for m in ST])
    log(f"== battery: {len(items)} mutants ==")
    results = []
    with cf.ThreadPoolExecutor(max_workers=3) as ex:
        for res in ex.map(battery, items):
            log(f"  {res['counter']} {res['mid']}: {res['verdict']} "
                f"killers={res.get('killers')} ({res.get('secs', '?')}s)")
            results.append(res)
    json.dump({"lane_master": lane_master, "pins": pins, "fixtures": revs,
               "pristine_captable": [{"check": n, "ok": ok, "observed": d} for n, ok, d in pc],
               "pristine_stale": [{"check": n, "ok": ok, "observed": d} for n, ok, d in ps],
               "pristine_neglookup_line": pristine_slot["neg-lookup"],
               "results": results}, open(f"{OUT}/results.json", "w"), indent=1)
    kc = sum(1 for r in results if r["counter"] == "captable" and r["verdict"] == "killed")
    ks = sum(1 for r in results if r["counter"] == "stale" and r["verdict"] == "killed")
    log(f"DONE captable_killed={kc}/{len(CAP)} stale_killed={ks}/{len(ST)}")

if __name__ == "__main__":
    main()
