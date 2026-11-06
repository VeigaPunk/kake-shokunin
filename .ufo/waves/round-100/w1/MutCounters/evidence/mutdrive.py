#!/usr/bin/env python3
"""MutCounters-5 mutation driver. Scratch-only; never writes the lane tree.

Phases:
  setup       copy originals, verify digests, build mutants, py_compile them
  pristine    run pristine batteries (reg + fresh) with timing
  reg-fx MODE build one fixture clone (pos|keepold|deleteall), run all counters
              against it, rm the clone (one live clone at a time)
  fresh       fresh304: selftests, then base+candidates for all counters
  judge       compare mutant outputs vs pristine; emit judged.tsv
"""
import concurrent.futures as cf
import hashlib
import json
import os
import py_compile
import shutil
import subprocess
import sys
import time

SCRATCH = "/fast/scratch/hyaku/kake-r100/MutCounters-5"
LANE = "/home/vgpnk/Projects/shokunin/kake-shokunin"
W = LANE + "/.ufo/waves/round-100"
BASE_REV = "3989618d9f8310b2eb5fb456aa7c4e58fb0b5ff5"
ORIG = SCRATCH + "/orig"
MUT = SCRATCH + "/mutants"
RES = SCRATCH + "/results"
WORK = SCRATCH + "/work"
PY = "/usr/bin/python3"
MAXW = 24

REG_SRC = W + "/c100_registry.py"
FR_SRC = W + "/c100_fresh304.py"

# ---------------- mutants: (id, old, new, line, class) ----------------
REG = [
    ("reg-m01", 'INTERP = {"python3", "python", "node"}',
     'INTERP = {"python3", "node"}', 88, "invoked interpreter set (drop python)"),
    ("reg-m02", 'INTERP = {"python3", "python", "node"}',
     'INTERP = {"python3", "python"}', 88, "invoked interpreter set (drop node)"),
    ("reg-m03", '            words.pop(0)\n            while words and words[0].startswith("-"):\n                words.pop(0)',
     '            words.pop(0)', 114, "invoked flag-word skip loop"),
    ("reg-m04", '        while words and re.match(r"^[A-Za-z_][A-Za-z0-9_]*=", words[0]):',
     '        while words and re.match(r"^NOASSIGN=", words[0]):', 110, "invoked assignment-prefix strip"),
    ("reg-m05", 'for seg in re.split(r"\\\\\\||\\|", span):',
     'for seg in re.split(r"\\|", span):', 108, "invoked escaped-pipe segment split"),
    ("reg-m06", 'if len(rows) > 1]', 'if len(rows) > 2]', 356, "duplicated threshold >1 -> >2"),
    ("reg-m07", 'if len(rows) > 1]', 'if len(rows) >= 1]', 356, "duplicated threshold >1 -> >=1"),
    ("reg-m08", '(?<![0-9A-Za-z_=.\-/])', '(?<![0-9A-Za-z_=./])', 87, "CODE lookbehind drops hyphen"),
    ("reg-m09", r'(?=\s*[=:]|\s|`|;|,|$)', r'(?=\s*[=:])', 87, "CODE lookahead requires =/:"),
    ("reg-m10", 'PROBE_ARG = "--zz-bogus-r100"', 'PROBE_ARG = "--zz-bogus-r99"', 89, "probe argument string"),
    ("reg-m11", '"bwrap", "--unshare-all",', '"bwrap", "--unshare-net",', 95, "sandbox unshare scope"),
    ("reg-m12", 'mism = len(unlisted) + len(dangling) + len(duplicated) + len(probe_mismatch)',
     'mism = len(unlisted) + len(dangling) + len(probe_mismatch)', 366, "met sum drops duplicated term"),
    ("reg-m13", '''    return re.search(r"(^|[\\s'\\"=])(\\./)?" + re.escape(path) + r"($|[\\s'\\"])", span) is not None''',
     '    return re.search(re.escape(path), span) is not None', 213, "names_path boundary classes dropped"),
    ("reg-m14", 'fence = m.group(1)[:3]', 'fence = m.group(1)', 162, "fence marker length check"),
    ("reg-m15", '        if "/" in rest:\n            continue\n', '', 137, "population depth filter"),
]

FR = [
    ("fr-m01", 'if has_arg and name in ("no-cache", "private"):',
     'if has_arg and name in ("no-cache",):', 187, "qualified-name test drops private"),
    ("fr-m02", 'name = m.group(0).lower()', 'name = m.group(0)', 120, "directive-name case folding"),
    ("fr-m03", r'''                        if v[i] == "\\":
                            if i + 1 >= n or not _qpair(ord(v[i + 1])):
                                raise Refuse("malformed cache-control")
                            i += 2
                            continue
                        if not _qdtext(o):''',
     '                        if not _qdtext(o):', 133, "quoted-string escape pair path"),
    ("fr-m04", '        i = ows(i + 1)', '        i = i + 1', 154, "OWS after comma (empty elements)"),
    ("fr-m05", '    i = ows(i)\n    while True:', '    while True:', 114, "leading OWS skip"),
    ("fr-m06", '        if v[i] != ",":', '        if True:', 152, "inter-element garbage tolerance"),
    ("fr-m07", 'v.strip(OWS) for k, v in h.items()', 'v for k, v in h.items()', 228, "output value trim dropped"),
    ("fr-m08", 'v.strip(OWS) for k, v in h.items()', 'v.strip() for k, v in h.items()', 228, "output trim OWS set -> all ws"),
    ("fr-m09", 'h = {k: v for k, v in x[2].items() if k not in PROXY}', 'h = dict(x[2])', 224, "stored PROXY drop"),
    ("fr-m10", 'PROXY = {"proxy-authenticate", "proxy-authentication-info", "proxy-authorization"}',
     'PROXY = {"proxy-authenticate", "proxy-authorization"}', 56, "PROXY set drops proxy-authentication-info"),
    ("fr-m11", 'excl = {"content-length", "connection"} | HOP | PROXY',
     'excl = {"content-length", "connection"} | PROXY', 216, "HOP excluded from copy"),
    ("fr-m12", 'except (UnicodeDecodeError, ValueError, RecursionError):', 'except ValueError:',
     236, "decide_bytes error set"),
    ("fr-m13", 's = out[:-1] if out.endswith("\\n") else out', 's = out', 521, "judge single trailing NL allowance"),
    ("fr-m14", 'if s != s.strip() or not s:', 'if not s:', 522, "judge stdout whitespace strictness"),
    ("fr-m15", '''return rc == 0 and out.startswith("2 ") and out.endswith("['1', '2']")''',
     'return rc == 0', 512, "sandbox_ok pid-namespace assertion"),
    ("fr-m16", '    s = v.strip(OWS)', '    s = v', 81, "_etag validator trim"),
    ("fr-m17", 'lm = sh["last-modified"].strip(OWS) if "last-modified" in sh else None',
     'lm = sh["last-modified"] if "last-modified" in sh else None', 181, "stored last-modified trim"),
]

FROZEN = ["pos-oracle", "neg-e1-striphop", "neg-e2-lazy", "neg-e3-spaceonly", "neg-e4-wsstdout",
          "neg-e5-crash", "neg-e6-ageexcl", "neg-e7-lmtie", "neg-f10-substring", "neg-f1-tokenform",
          "neg-f2-notrim", "neg-f3-keepproxy", "neg-lc6-case", "neg-malformed-lenient", "neg-theft"]


def sh(cmd, **kw):
    return subprocess.run(cmd, capture_output=True, **kw)


def setup():
    os.makedirs(ORIG, exist_ok=True)
    shutil.copy(REG_SRC, ORIG + "/c100_registry.py")
    shutil.copy(FR_SRC, ORIG + "/c100_fresh304.py")
    # digest verification against the committed frozen list
    r = sh(["bash", "-c", "cd %s && sha256sum -c controls/instrument-sha256.txt --quiet" % W])
    if r.returncode != 0:
        print("DIGEST MISMATCH finding:\n" + r.stdout.decode() + r.stderr.decode())
        sys.exit(3)
    print("digests: all frozen instruments OK")
    for dirname, src, muts in (("registry", ORIG + "/c100_registry.py", REG),
                               ("fresh", ORIG + "/c100_fresh304.py", FR)):
        os.makedirs(MUT + "/" + dirname, exist_ok=True)
        text = open(src, encoding="utf-8").read()
        for mid, old, new, line, cls in muts:
            n = text.count(old)
            if n != 1:
                print("MUTATION ANCHOR FAIL %s count=%d" % (mid, n))
                sys.exit(4)
            mp = "%s/%s/%s.py" % (MUT, dirname, mid)
            open(mp, "w", encoding="utf-8").write(text.replace(old, new, 1))
            py_compile.compile(mp, doraise=True)
    print("mutants built: registry=%d fresh=%d (all py_compile OK)" % (len(REG), len(FR)))
    man = {"registry": [{"id": m[0], "line": m[3], "class": m[4]} for m in REG],
           "fresh": [{"id": m[0], "line": m[3], "class": m[4]} for m in FR]}
    json.dump(man, open(SCRATCH + "/mutants.json", "w"), indent=1)


def counters(dirname, ids, orig_name):
    out = [(ORIG + "/" + orig_name, "pristine")] + [
        ("%s/%s/%s.py" % (MUT, dirname, i), i) for i in ids]
    return out


def run_job(counter, label, args, outdir):
    os.makedirs(outdir, exist_ok=True)
    t0 = time.time()
    r = sh([PY, "-B", counter] + args, timeout=1200)
    dt = time.time() - t0
    open("%s/stdout" % outdir, "w").write(r.stdout.decode("utf-8", "replace"))
    open("%s/stderr" % outdir, "w").write(r.stderr.decode("utf-8", "replace"))
    open("%s/rc" % outdir, "w").write(str(r.returncode))
    open("%s/cmd" % outdir, "w").write(" ".join(["python3", "-B", counter] + args))
    print("job %-12s %-22s rc=%-3d %5.1fs" % (label.split("/")[-1], os.path.basename(counter), r.returncode, dt), flush=True)
    return dt


def pristine():
    total = 0.0
    jobs = []
    for c, name in counters("registry", [m[0] for m in REG], "c100_registry.py"):
        pass  # pristine only here
    c = ORIG + "/c100_registry.py"
    jobs.append((c, "reg-self", ["--selftest", "--work", WORK + "/pristine/reg/self"]))
    jobs.append((c, "reg-base", ["--root", LANE, "--revision", BASE_REV, "--work", WORK + "/pristine/reg/base"]))
    with cf.ThreadPoolExecutor(MAXW) as ex:
        for dt in [f.result() for f in [ex.submit(run_job, *j, RES + "/pristine/" + j[1]) for j in jobs]]:
            total += dt
    c = ORIG + "/c100_fresh304.py"
    with cf.ThreadPoolExecutor(MAXW) as ex:
        futs = [ex.submit(run_job, c, "fr-self", ["--selftest"], RES + "/pristine/fr-self")]
        futs.append(ex.submit(run_job, c, "fr-base",
                              ["--root", LANE, "--revision", BASE_REV, "--work", WORK + "/pristine/fr/base"],
                              RES + "/pristine/fr-base"))
        for fn in FROZEN:
            futs.append(ex.submit(run_job, c, "fresh-cand-" + fn,
                                  ["--candidate-file", "%s/frozen/%s.py" % (W, fn),
                                   "--work", "%s/work/pristine/cand-%s" % (SCRATCH, fn)],
                                  "%s/pristine/fresh-cand-%s" % (RES, fn)))
        for f in cf.as_completed(futs):
            total += f.result()
    print("pristine battery done, cumulative cpu-ish wall %.1fs" % total)


def reg_fx(mode):
    D = SCRATCH + "/fx-" + mode
    if os.path.exists(D):
        shutil.rmtree(D)
    t0 = time.time()
    sh(["git", "clone", "-q", "--shared", LANE, D])
    assert subprocess.run(["git", "-C", D, "rev-parse", "--show-toplevel"],
                          capture_output=True).stdout.decode().strip() == D, "fixture root mismatch"
    sh(["git", "-C", D, "checkout", "-q", "--detach", BASE_REV])
    r = sh([PY, "-B", W + "/c1_repair_fixture.py", D + "/SKILL.md", mode])
    if r.returncode != 0:
        print("fixture %s builder rc=%d: %s" % (mode, r.returncode, r.stderr.decode()))
        sys.exit(5)
    sh(["git", "-C", D, "-c", "user.name=fixture", "-c", "user.email=fixture@example.invalid",
        "commit", "-q", "-am", "fixture %s" % mode])
    sha = subprocess.run(["sha256sum", D + "/SKILL.md"], capture_output=True).stdout.decode().split()[0]
    want = open("%s/controls/fixture-c1-%s-SKILL.sha256" % (W, mode)).read().strip()
    print("fixture %s built in %.1fs; SKILL sha %s (receipt %s) %s"
          % (mode, time.time() - t0, sha, want, "MATCH" if sha == want else "MISMATCH"))
    if sha != want:
        print("FINDING: fixture reproduction mismatch for mode %s" % mode)
        sys.exit(6)
    jobs = []
    for c, name in counters("registry", [m[0] for m in REG], "c100_registry.py"):
        jobs.append((c, name, ["--root", D, "--revision", "HEAD", "--work",
                               "%s/work/%s/%s" % (SCRATCH, name, "fx-" + mode)],
                     "%s/reg-fx-%s/%s" % (RES, mode, name)))
    with cf.ThreadPoolExecutor(MAXW) as ex:
        for f in cf.as_completed([ex.submit(run_job, *j[:2], j[2], j[3]) for j in jobs]):
            f.result()
    shutil.rmtree(D)  # one live clone per seat, destroyed after the mode
    print("fixture %s phase complete, clone removed" % mode)


def reg_mutant_sb():
    jobs = []
    for c, name in counters("registry", [m[0] for m in REG], "c100_registry.py"):
        if name == "pristine":
            continue
        jobs.append((c, name, ["--selftest", "--work", "%s/work/%s/self" % (SCRATCH, name)],
                     "%s/reg-self/%s" % (RES, name)))
        jobs.append((c, name, ["--root", LANE, "--revision", BASE_REV,
                               "--work", "%s/work/%s/base" % (SCRATCH, name)],
                     "%s/reg-base/%s" % (RES, name)))
    with cf.ThreadPoolExecutor(MAXW) as ex:
        for f in cf.as_completed([ex.submit(run_job, *j[:2], j[2], j[3]) for j in jobs]):
            f.result()
    print("registry mutant self+base phase complete (%d jobs)" % len(jobs))


def fresh():
    c = ORIG + "/c100_fresh304.py"
    counters_f = counters("fresh", [m[0] for m in FR], "c100_fresh304.py")
    with cf.ThreadPoolExecutor(MAXW) as ex:
        futs = [ex.submit(run_job, cc, nm, ["--selftest"], "%s/fresh-self/%s" % (RES, nm))
                for cc, nm in counters_f]
        for f in cf.as_completed(futs):
            f.result()
    jobs = []
    for cc, nm in counters_f:
        jobs.append((cc, nm, ["--root", LANE, "--revision", BASE_REV,
                              "--work", "%s/work/%s/base" % (SCRATCH, nm)],
                     "%s/fresh-base/%s" % (RES, nm)))
        for fn in FROZEN:
            jobs.append((cc, nm, ["--candidate-file", "%s/frozen/%s.py" % (W, fn),
                                  "--work", "%s/work/%s/cand-%s" % (SCRATCH, nm, fn)],
                         "%s/fresh-cand-%s/%s" % (RES, fn, nm)))
    done = 0
    with cf.ThreadPoolExecutor(MAXW) as ex:
        futs = [ex.submit(run_job, *j[:2], j[2], j[3]) for j in jobs]
        for f in cf.as_completed(futs):
            f.result()
            done += 1
            if done % 48 == 0:
                print("fresh jobs %d/%d" % (done, len(jobs)), flush=True)
    print("fresh battery complete (%d jobs)" % done)


def read_out(d):
    rc = open(d + "/rc").read().strip()
    so = open(d + "/stdout").read()
    return rc, so


def judge():
    mutants = json.load(open(SCRATCH + "/mutants.json"))
    reg_labels = ["reg-self", "reg-base", "reg-fx-pos", "reg-fx-keepold", "reg-fx-deleteall"]
    fr_labels = (["fresh-self", "fresh-base"] + ["fresh-cand-" + f for f in FROZEN])
    pr = {}
    for lbl in reg_labels:
        if lbl.startswith("reg-fx-"):
            pr[lbl] = read_out(RES + "/" + lbl + "/pristine")
        else:
            pr[lbl] = read_out(RES + "/pristine/" + lbl)
    base_map = {"fresh-self": "pristine/fr-self", "fresh-base": "pristine/fr-base"}
    for lbl in ["fresh-self", "fresh-base"]:
        pr[lbl] = read_out(RES + "/" + base_map[lbl])
    for f in FROZEN:
        pr["fresh-cand-" + f] = read_out(RES + "/pristine/fresh-cand-" + f)
    cols = (["counter", "id", "line", "class"] + reg_labels + ["fresh-self", "fresh-base"]
            + ["fresh-cand-" + f for f in FROZEN] + ["verdict", "killed_by"])
    rows = []
    summary = {"registry": [0, 0], "fresh": [0, 0]}
    survivors = []
    for grp, dirname, ids in (("registry", "registry", [m[0] for m in REG]),
                              ("fresh", "fresh", [m[0] for m in FR])):
        meta = {m["id"]: m for m in mutants[grp]}
        for mid in ids:
            row = {"counter": grp, "id": mid, "line": meta[mid]["line"], "class": meta[mid]["class"]}
            killers = []
            labels = reg_labels if grp == "registry" else fr_labels
            for lbl in labels:
                d = "%s/%s/%s" % (RES, lbl, mid)
                if os.path.exists(d + "/rc"):
                    rc, so = read_out(d)
                    same = (rc, so) == pr[lbl]
                    row[lbl] = "same" if same else "DIFF"
                    if not same:
                        killers.append(lbl)
                else:
                    row[lbl] = "MISSING"
                    killers.append(lbl + "(missing)")
            n_killed = sum(1 for k, v in row.items() if v == "DIFF")
            missing = sum(1 for k, v in row.items() if v == "MISSING")
            if missing:
                verdict = "INCOMPLETE"
            else:
                verdict = "killed" if n_killed else "survived"
            row["verdict"] = verdict
            row["killed_by"] = ",".join(killers) if killers else "-"
            summary[grp][0] += 1 if verdict == "killed" else 0
            summary[grp][1] += 1
            if verdict == "survived":
                survivors.append((grp, mid))
            if verdict == "INCOMPLETE":
                print("WARNING: %s %s incomplete, %d missing runs" % (grp, mid, missing))
            rows.append(row)
    with open(SCRATCH + "/judged.tsv", "w") as fh:
        fh.write("\t".join(cols) + "\n")
        for r in rows:
            fh.write("\t".join(str(r.get(c, "-")) for c in cols) + "\n")
    print("judged: registry=%d/%d fresh=%d/%d survivors=%s"
          % (summary["registry"][0], summary["registry"][1],
             summary["fresh"][0], summary["fresh"][1], survivors))


if __name__ == "__main__":
    os.makedirs(WORK, exist_ok=True)
    os.makedirs(RES, exist_ok=True)
    cmd = sys.argv[1]
    if cmd == "setup":
        setup()
    elif cmd == "pristine":
        pristine()
    elif cmd == "reg-fx":
        reg_fx(sys.argv[2])
    elif cmd == "reg-mutant-sb":
        reg_mutant_sb()
    elif cmd == "fresh":
        fresh()
    elif cmd == "judge":
        judge()
    else:
        print("unknown phase")
        sys.exit(2)
