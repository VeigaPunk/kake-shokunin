#!/usr/bin/env python3
"""MutCounters seat harness (scratch only). Reads LANE; writes only under S."""
import ast, concurrent.futures as cf, importlib.util, json, os, random, re, shutil, subprocess, sys

S = "/fast/scratch/hyaku/kake-r99/MutCounters"
LANE = "/home/vgpnk/Projects/shokunin/kake-shokunin"
W = LANE + "/.ufo/waves/round-99"
BASE = "cde408e5817bf1376c701d8decc5469fa82b2985"
CL = S + "/clone"
PRIST = S + "/pristine"
MUT = S + "/mut"
PY = sys.executable
FROZEN = W + "/frozen"
FR_CANDS = ["pos-oracle", "neg-constant", "neg-copyall", "neg-firstmatch", "neg-lenient",
            "neg-lookup", "neg-mustnot", "neg-weakstrong"]
VARS = ["pos", "namesonly", "fenced", "falseselftest", "junkprose", "wrongowner", "base"]


def run(cmd, timeout=1500):
    r = subprocess.run(cmd, capture_output=True, timeout=timeout)
    return (r.returncode, r.stdout.decode("utf-8", "replace"), r.stderr.decode("utf-8", "replace"))


def git(*a, cwd=None):
    r = subprocess.run(["git", "-C", cwd or CL, *a], capture_output=True)
    if r.returncode:
        raise RuntimeError("git %s: %s" % (" ".join(a), r.stderr.decode()))
    return r.stdout


def toplevel_ok(d):
    top = git("rev-parse", "--show-toplevel", cwd=d).decode().strip()
    assert os.path.realpath(top) == os.path.realpath(d), (top, d)


# ---------- fixtures: C1 variants exactly as controls.sh builds them ----------
def variant_texts():
    B = git("show", BASE + ":SKILL.md", cwd=LANE).decode()
    SEC = open(W + "/c1-repair-section.md", encoding="utf-8").read()
    HDR = "| Name | Kind | Entry command | Verdict map | Self-test | Write scope | Owner |\n|---|---|---|---|---|---|---|\n"
    v = {}
    v["pos"] = B + SEC
    names = "".join("| scripts/%s | | | | | | |\n" % m.group(1)
                    for m in re.finditer(r"^\| ([A-Za-z0-9_.-]+\.(?:py|mjs)) ", SEC, re.M))
    v["namesonly"] = B + "\n" + HDR + names
    v["fenced"] = B + "```\n" + SEC + "```\n"
    out = []
    for line in SEC.splitlines(True):
        if line.startswith("| ") and "no self-test" in line:
            name = line.split(" | ")[0][2:]
            line = re.sub(r"no self-test[^|]*", "`python3 -B scripts/%s --selftest` " % name, line, count=1)
        out.append(line)
    v["falseselftest"] = B + "".join(out)
    out = []
    for line in SEC.splitlines(True):
        if line.startswith("| ") and "| kake |" in line and not line.startswith("| Name"):
            c = line.rstrip("\n").split(" | ")
            c[1] = "lorem"
            c[3] = "`0` ipsum; `1` dolor"
            c[5] = "nowhere"
            line = " | ".join(c) + "\n"
        out.append(line)
    v["junkprose"] = B + "".join(out)
    v["wrongowner"] = B + "".join(re.sub(r"\| kake \|$", "| kaidoku |", l) for l in SEC.splitlines(True))
    return v


def setup_clone():
    shutil.rmtree(CL, ignore_errors=True)
    subprocess.run(["git", "clone", "-q", "--shared", LANE, CL], check=True)
    toplevel_ok(CL)
    revs = {"base": BASE}
    for name, text in variant_texts().items():
        p = S + "/variants/%s.md" % name
        os.makedirs(os.path.dirname(p), exist_ok=True)
        open(p, "w", encoding="utf-8").write(text)
        git("checkout", "-q", "--detach", BASE)
        shutil.copy(p, CL + "/SKILL.md")
        git("-c", "user.name=fixture", "-c", "user.email=fixture@invalid", "commit", "-q", "-am", "fixture " + name)
        revs[name] = git("rev-parse", "HEAD").decode().strip()
    git("checkout", "-q", "--detach", BASE)
    return revs


REVS = {}


# ---------- records ----------
def reg_record(mut, tag):
    d = S + "/runs/reg-" + tag
    shutil.rmtree(d, ignore_errors=True)
    os.makedirs(d)
    rec = {"selftest": run([PY, "-B", mut, "--selftest", "--work", d + "/st"])}
    for v in VARS:
        rec[v] = run([PY, "-B", mut, "--root", CL, "--revision", REVS[v], "--work", d + "/" + v])
    return rec


def fr_record(mut, tag):
    d = S + "/runs/fr-" + tag
    shutil.rmtree(d, ignore_errors=True)
    os.makedirs(d)
    rec = {"selftest": run([PY, "-B", mut, "--selftest"])}
    rec["base-absent"] = run([PY, "-B", mut, "--root", CL, "--revision", BASE, "--work", d + "/base"])
    for n in FR_CANDS:
        rec[n] = run([PY, "-B", mut, "--root", CL, "--revision", BASE,
                      "--candidate-file", FROZEN + "/%s.py" % n, "--work", d + "/" + n])
    return rec


def receipt_body(path):
    out = []
    for ln in open(path, encoding="utf-8", errors="replace").read().splitlines():
        if ln.startswith("# control") or ln.startswith("exit="):
            continue
        out.append(ln)
    return out


def stdout_body(s):
    return [ln for ln in s.splitlines()]


def met_of(out):
    m = re.search(r"met=(\w+)", out)
    return m.group(1) if m else None


def parse_st(out):
    return {m.group(2): m.group(1) for m in re.finditer(r"^(ok|FAIL) (\S+):", out, re.M)}


def diffs(p, m):
    res = []
    for k in p:
        a, b = p[k], m[k]
        if a[0] != b[0]:
            res.append((k, "strong", "rc %d->%d" % (a[0], b[0])))
        elif met_of(a[1]) != met_of(b[1]):
            res.append((k, "strong", "met %s->%s" % (met_of(a[1]), met_of(b[1]))))
        elif parse_st(a[1]) != parse_st(b[1]):
            res.append((k, "strong", "selftest-case"))
        elif a[1] != b[1]:
            res.append((k, "detail", "output"))
    return res


# ---------- mutant specs: (id, old, new, equivalent-note or None) ----------
REG = [
 ("RG01", "owner-required-dropped", '"write scope", "owner"}', '"write scope"}', None),
 ("RG02", "cell-count-lenient", 'if len(rc) != len(hdr):', 'if len(rc) < len(hdr):', None),
 ("RG03", "names-path-trailing-boundary-dropped", 'r"($|[\\s\'\\"])", span)', 'r"()", span)', None),
 ("RG04", "names-path-leading-equals-dropped", 'r"(^|[\\s\'\\"=])(\\./)?"', 'r"(^|[\\s\'\\"])(\\./)?"', None),
 ("RG05", "verdict-0-end-of-cell-dropped", '(?<![0-9])0(\\s*[=:]|\\s|`|$)', '(?<![0-9])0(\\s*[=:]|\\s|`)', None),
 ("RG06", "verdict-1-lookbehind-dropped", '(?<![0-9])1(\\s*[=:]|\\s|`|$)', '1(\\s*[=:]|\\s|`|$)', None),
 ("RG07", "owner-prefix-4-compare", 'rc[ix["owner"]].strip().strip("`") != "kake":', 'rc[ix["owner"]].strip().strip("`")[:4] != "kake":', None),
 ("RG08", "owner-allows-sibling", 'rc[ix["owner"]].strip().strip("`") != "kake":', 'rc[ix["owner"]].strip().strip("`") not in ("kake", "kaidoku"):', None),
 ("RG09", "owner-backtick-strip-dropped", 'rc[ix["owner"]].strip().strip("`") != "kake":', 'rc[ix["owner"]].strip() != "kake":', None),
 ("RG10", "forbidden-dollar-paren-dropped", 'FORBIDDEN = re.compile(r"\\||>|<|;|&&|\\$\\(|`")', 'FORBIDDEN = re.compile(r"\\||>|<|;|&&|`")', None),
 ("RG11", "forbidden-backtick-dropped", 'FORBIDDEN = re.compile(r"\\||>|<|;|&&|\\$\\(|`")', 'FORBIDDEN = re.compile(r"\\||>|<|;|&&|\\$\\(")',
  "equivalent: SPAN excludes backticks, so no span can contain one"),
 ("RG12", "assign-subst-alternative-dropped", 'ASSIGN = re.compile(r"^\\s*(?:[A-Za-z_][A-Za-z0-9_]*=(?:\\$\\([^()]*\\)|\\S+)\\s+)+")',
  'ASSIGN = re.compile(r"^\\s*(?:[A-Za-z_][A-Za-z0-9_]*=(?:\\S+)\\s+)+")', None),
 ("RG13", "placeholder-substitution-disabled", '        if re.fullmatch(r"<[^<>\\s]+>", w):', '        if False:', None),
 ("RG14", "placeholder-masked-before-forbidden-check-dropped", '    if FORBIDDEN.search(PLACEHOLDER.sub("PH", span)):', '    if FORBIDDEN.search(span):', None),
 ("RG15", "fence-skip-disabled", '        if fence:\n            if s.startswith(fence):', '        if False:\n            if s.startswith(fence):', None),
 ("RG16", "html-comment-skip-disabled", '            if "-->" not in raw.split("<!--", 1)[1]:', '            if False:', None),
 ("RG17", "population-subdir-filter-dropped", '        if "/" in rest:', '        if False:', None),
 ("RG18", "population-mjs-dropped", '        if rest.endswith(".py") or rest.endswith(".mjs"):', '        if rest.endswith(".py"):', None),
 ("RG19", "dangling-token-mjs-dropped", '\\.(?:py|mjs))(?=$|[\\s\'\\"])")', '\\.(?:py))(?=$|[\\s\'\\"])")', None),
 ("RG20", "dangling-check-disabled", '                    if tok not in allfiles:', '                    if False:', None),
 ("RG21", "met-ignores-dangling", '    met = mism == 0', '    met = len(unlisted) == 0', None),
 ("RG22", "exit-1-counts-as-selftest-pass", '                    if cache[sp] == 0:', '                    if cache[sp] in (0, 1):', None),
 ("RG23", "no-self-test-phrase-case-sensitive", '"no self-test" in st.lower()', '"no self-test" in st', None),
 ("RG24", "no-self-test-without-selftest-absence-check", ' and not has_selftest[p]:', ':', None),
 ("RG25", "split-escape-protection-dropped", 'SPLIT = re.compile(r"(?<!\\\\)\\|")', 'SPLIT = re.compile(r"\\|")', None),
 ("RG26", "selftest-header-alias-dropped", '    if c == "selftest":', '    if c == "selftestX":', None),
 ("RG27", "table-row-contiguity-dropped", 'and kept[j][0] == kept[j - 1][0] + 1:', 'and True:', None),
 ("RG28", "cells-trailing-escaped-pipe-check-dropped", '    if s.endswith("|") and not s.endswith("\\\\|"):', '    if s.endswith("|"):', None),
 ("RG29", "selftest-sibling-file-match-dropped", 'if names_path(sp, p) or any(names_path(sp, q) for q in selftest_files)]', 'if names_path(sp, p)]', None),
]

FR = [
 ("FR01", "etag-bang-0x21-dropped", 'if not (o == 0x21 or 0x23 <= o <= 0x7E or 0x80 <= o <= 0xFF):', 'if not (0x23 <= o <= 0x7E or 0x80 <= o <= 0xFF):', None),
 ("FR02", "etag-obs-text-upper-0xFF-dropped", '0x80 <= o <= 0xFF):', '0x80 <= o <= 0xFE):', None),
 ("FR03", "etag-length-check-lowered", 'if len(s) < 2 or', 'if len(s) < 1 or', None),
 ("FR04", "weak-prefix-case-sensitive-w", 'if s.startswith("W/"):', 'if s.startswith("w/"):', None),
 ("FR05", "strong-rule-admits-weak-stored", ' and not n[3][0] and n[3][1] == ret[1]]', ' and n[3][1] == ret[1]]', None),
 ("FR06", "weak-tie-threshold-off-by-one", '            if len(best) > 1:', '            if len(best) > 2:', None),
 ("FR07", "weak-most-recent-min-not-max", 'top = max(n[1] for n in corr)', 'top = min(n[1] for n in corr)', None),
 ("FR08", "weak-lm-correspondence-skipped-with-etag", '            if rlm is not None:', '            if rlm is not None and ret is None:', None),
 ("FR09", "no-validator-ignores-stored-lm", ' and norm[0][4] is None else []', ' else []', None),
 ("FR10", "exclusion-proxy-set-dropped", 'excl = {"content-length", "connection"} | HOP | PROXY', 'excl = {"content-length", "connection"} | HOP', None),
 ("FR11", "exclusion-content-length-dropped", 'excl = {"content-length", "connection"} | HOP | PROXY', 'excl = {"connection"} | HOP | PROXY', None),
 ("FR12", "connection-token-case-fold-dropped", '            m = m.strip(" \\t").lower()', '            m = m.strip(" \\t")', None),
 ("FR13", "judge-compares-decision-only", '    return obj == expected', '    return obj.get("decision") == expected["decision"]', None),
 ("FR14", "met-ignores-generated", '        met = hp == len(HAND) and gp == len(gen)', '        met = hp == len(HAND)', None),
 ("FR15", "generator-no-refusals", '    bad = rng.random() < 0.12', '    bad = rng.random() < 0.0', None),
 ("FR16", "seed-derivation-xor1", '(int(rev[:8], 16) if rev else 99099)', '(int(rev[:8], 16) ^ 1 if rev else 99099)', None),
 ("FR17", "qualified-private-refusal-dropped", '    if \'no-cache="\' in cc.lower() or \'private="\' in cc.lower():', '    if \'no-cache="\' in cc.lower():', None),
 ("FR18", "strong-none-decision-no-update", '        dec_none = "must-not-update"', '        dec_none = "no-update"', None),
 ("FR19", "connection-empty-token-guard-dropped", '            if m:\n                excl.add(m)', '            excl.add(m)',
  "equivalent: empty string is never a header key (TCHAR rejects it), so adding it changes nothing"),
 ("FR20", "judge-refusal-stdout-check-dropped", '    return rc == 1 and out.strip() == "" and err.startswith("invalid_input:")', '    return rc == 1 and err.startswith("invalid_input:")', None),
 ("FR21", "judge-accepts-rc1-decisions", '    if rc != 0:\n        return False', '    if rc not in (0, 1):\n        return False', None),
 ("FR22", "nul-in-header-value-admitted", '        if any(c in v for c in "\\r\\n\\x00"):', '        if any(c in v for c in "\\r\\n"):', None),
 ("FR23", "case-duplicate-header-check-dropped", '        if lk in out:', '        if False:', None),
]


def make_mutants():
    os.makedirs(MUT + "/reg", exist_ok=True)
    os.makedirs(MUT + "/fr", exist_ok=True)
    index = []
    for counter, specs, src, sub in (("registry", REG, "c99_registry.py", "reg"), ("fresh304", FR, "c99_fresh304.py", "fr")):
        base_txt = open(PRIST + "/" + src, encoding="utf-8").read()
        for mid, desc, old, new, equiv in specs:
            n = base_txt.count(old)
            assert n == 1, (mid, n)
            new_txt = base_txt.replace(old, new)
            assert new_txt != base_txt
            ast.parse(new_txt)
            path = "%s/%s/%s.py" % (MUT, sub, mid)
            open(path, "w", encoding="utf-8").write(new_txt)
            line = base_txt[:base_txt.index(old)].count("\n") + 1
            index.append((counter, mid, desc, line, equiv, path))
    return index


def load(path, name):
    spec = importlib.util.spec_from_file_location(name, path)
    m = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(m)
    return m


def main(phase):
    if phase == "setup":
        REVS.update(setup_clone())
        json.dump(REVS, open(S + "/revs.json", "w"), indent=1)
        print(json.dumps(REVS, indent=1))
    elif phase == "repro":
        REVS.update(json.load(open(S + "/revs.json")))
        rec = reg_record(PRIST + "/c99_registry.py", "pristine")
        rec2 = fr_record(PRIST + "/c99_fresh304.py", "pristine")
        rc = {}
        ok = True
        for name, path in [("selftest", W + "/controls/ctl-c1-selftest.txt")] + [(v, W + "/controls/ctl-c1-%s.txt" % (
                {"pos": "pos", "namesonly": "namesonly", "fenced": "fenced", "falseselftest": "falseselftest",
                 "junkprose": "junkprose", "wrongowner": "wrongowner", "base": None}[v])) for v in VARS if v != "base"] + [("base", W + "/controls/base-c1.txt")]:
            want = receipt_body(path)
            got = [l for l in stdout_body(rec[name][1]) if not l.startswith("revision=")]
            want_nr = [w for w in want if not w.startswith("revision=")]
            match = got == want_nr
            rc["reg:" + name] = match
            ok &= match
            if not match:
                print("REPRO MISMATCH reg:%s\n got=%r\n want=%r" % (name, got[:6], want_nr[:6]))
        fpairs = [("selftest", "ctl-c2-selftest.txt"), ("base-absent", "base-c2.txt"), ("pos-oracle", "ctl-c2-pos-oracle.txt")] + \
                 [(n, "ctl-c2-neg-%s.txt" % n[len("neg-"):]) for n in FR_CANDS if n.startswith("neg-")]
        for name, f in fpairs:
            want = receipt_body(W + "/controls/" + f)
            got = stdout_body(rec2[name][1])
            match = got == want
            rc["fr:" + name] = match
            ok &= match
            if not match:
                print("REPRO MISMATCH fr:%s\n got=%r\n want=%r" % (name, got[:4], want[:4]))
        for k, v in rec.items():
            print("reg", k, "rc=%d" % v[0], (met_of(v[1]) or "-"))
        for k, v in rec2.items():
            print("fr", k, "rc=%d" % v[0], (met_of(v[1]) or "-"))
        print("REPRO ALL MATCH" if ok else "REPRO FAILURES", sorted(k for k, v in rc.items() if not v))
    elif phase == "mutants":
        REVS.update(json.load(open(S + "/revs.json")))
        idx = make_mutants()
        json.dump(idx, open(S + "/index.json", "w"), indent=1)
        print("generated", len(idx))
    elif phase == "run":
        REVS.update(json.load(open(S + "/revs.json")))
        idx = json.load(open(S + "/index.json"))
        pr_reg = reg_record(PRIST + "/c99_registry.py", "pristine")
        pr_fr = fr_record(PRIST + "/c99_fresh304.py", "pristine")

        def job(item):
            counter, mid, desc, line, equiv, path = item
            tag = mid
            rec = reg_record(path, tag) if counter == "registry" else fr_record(path, tag)
            base = pr_reg if counter == "registry" else pr_fr
            d = diffs(base, rec)
            return item, d

        results = []
        with cf.ThreadPoolExecutor(max_workers=int(os.environ.get("MUT_WORKERS", "4"))) as ex:
            for item, d in ex.map(job, idx):
                results.append((item, d))
                strong = [x for x in d if x[1] == "strong"]
                print(item[1], "KILL" if strong else "live", strong[:1] or [x for x in d][:1], flush=True)
        json.dump([[list(i[:5]), i[5], d] for i, d in results], open(S + "/results.json", "w"), indent=1)
    elif phase == "probes":
        probes_main()
    else:
        raise SystemExit("unknown phase")


# ---------- survivor separation probes ----------
GOOD = "import sys\nif '--selftest' in sys.argv:\n    print('selftest 1/1'); sys.exit(0)\nsys.exit(0)\n"
PLAIN = "print('x')\n"
HR = "| Name | Kind | Entry command | Verdict map | Self-test | Write scope | Owner |\n|---|---|---|---|---|---|---|\n"


def row(entry, vm="`0=clean`; `1=failed`", st="`python3 -B scripts/a.py --selftest`", owner="kake", name="t"):
    return "| %s | gate | %s | %s | %s | none | %s |\n" % (name, entry, vm, st, owner)


def mkfix(name, files, skill):
    d = S + "/probe/" + name
    shutil.rmtree(d, ignore_errors=True)
    os.makedirs(d)
    subprocess.run(["git", "-C", d, "init", "-q"], check=True)
    toplevel_ok(d)
    for p, c in files.items():
        os.makedirs(os.path.dirname(os.path.join(d, p)), exist_ok=True)
        open(os.path.join(d, p), "w").write(c)
    open(os.path.join(d, "SKILL.md"), "w").write(skill)
    git("add", "-A", cwd=d)
    git("-c", "user.name=fixture", "-c", "user.email=fixture@invalid", "commit", "-q", "-m", "f", cwd=d)
    return d


def probes_main():
    A = {"scripts/a.py": GOOD}
    AB = {"scripts/a.py": GOOD, "scripts/b.py": PLAIN}
    P = {
     "RG01": (A, "| Name | Kind | Entry command | Verdict map | Self-test | Write scope |\n|---|---|---|---|---|---|\n| t | gate | `python3 -B scripts/a.py` | `0=clean`; `1=failed` | `python3 -B scripts/a.py --selftest` | none |\n"),
     "RG03": (A, HR + row("`python3 -B scripts/a.pyx`")),
     "RG04": (A, HR + row("`python3 -B --file=scripts/a.py`")),
     "RG05": (A, HR + row("`python3 -B scripts/a.py`", vm="`1` failed; exit 0")),
     "RG06": (A, HR + row("`python3 -B scripts/a.py`", vm="`0` clean; `21` odd")),
     "RG07": (A, HR + row("`python3 -B scripts/a.py`", owner="kakeX")),
     "RG09": (A, HR + row("`python3 -B scripts/a.py`", owner="`kake`")),
     "RG18": ({"scripts/a.py": GOOD, "scripts/c.mjs": "x\n"}, HR + row("`python3 -B scripts/a.py`")),
     "RG19": (A, HR + row("`python3 -B scripts/a.py`") + row("`node scripts/ghost.mjs`", name="g")),
     "RG23": (AB, HR + row("`python3 -B scripts/a.py`") + row("`python3 -B scripts/b.py`", st="No self-test", name="b")),
     "RG27": (AB, HR + row("`python3 -B scripts/a.py`") + "<!-- note -->\n" + row("`python3 -B scripts/b.py`", st="no self-test", name="b")),
    }
    out = []
    for mid, (files, skill) in sorted(P.items()):
        d = mkfix("p-" + mid, files, skill)
        counter = PRIST + "/c99_registry.py"
        res_p = run([PY, "-B", counter, "--root", d, "--revision", "HEAD", "--work", S + "/probe/w-%s-p" % mid])
        mpath = MUT + "/reg/%s.py" % mid
        res_m = run([PY, "-B", mpath, "--root", d, "--revision", "HEAD", "--work", S + "/probe/w-%s-m" % mid])
        sep = res_p != res_m
        out.append("%s pristine rc=%d %s | mutant rc=%d %s | separated=%s" % (
            mid, res_p[0], " / ".join(stdout_body(res_p[1])[1:2]), res_m[0], " / ".join(stdout_body(res_m[1])[1:2]) or res_m[2].strip().splitlines()[-1:], sep))
    # RG01 mutant crash detail
    # fresh304 probes
    pr = load(PRIST + "/c99_fresh304.py", "pr304")
    fr_mut = {}
    for mid in ["FR01", "FR02", "FR03", "FR22", "FR16"]:
        fr_mut[mid] = load(MUT + "/fr/%s.py" % mid, "m_" + mid)
    tests = {
     "FR01": {"stored": [{"id": "a", "received": 1, "headers": {"ETag": '"!"'}}], "response": {"status": 304, "headers": {"ETag": '"!"'}}},
     "FR02": {"stored": [{"id": "a", "received": 1, "headers": {"ETag": '"\u00ff"'}}], "response": {"status": 304, "headers": {"ETag": '"\u00ff"'}}},
     "FR03": {"stored": [{"id": "a", "received": 1, "headers": {"ETag": '"'}}], "response": {"status": 304, "headers": {"ETag": '"x"'}}},
     "FR22": {"stored": [], "response": {"status": 304, "headers": {"X-V": "a\x00b"}}},
    }
    for mid, inp in tests.items():
        a = pr.ref_or_refusal(inp)
        b = fr_mut[mid].ref_or_refusal(inp)
        out.append("%s fr-probe pristine=%s | mutant=%s | separated=%s" % (mid, json.dumps(a)[:90], json.dumps(b)[:90], a != b))
    m20 = load(MUT + "/fr/FR20.py", "m_FR20") if os.path.exists(MUT + "/fr/FR20.py") else None
    for mid in ["FR20", "FR21"]:
        mm = load(MUT + "/fr/%s.py" % mid, "m_" + mid)
        if mid == "FR20":
            args = (None, (1, '{"x": 1}', "invalid_input: x"))
        else:
            args = ({"a": 1}, (1, '{"a": 1}', ""))
        a = pr.judge(*args)
        b = mm.judge(*args)
        out.append("%s judge-probe pristine=%s | mutant=%s | separated=%s" % (mid, a, b, a != b))
    # FR16: candidate wrong only on a generated input present under the mutant seed but not the pristine seed
    bi = int(BASE[:8], 16)
    mm16 = fr_mut["FR16"]

    def gen_set(mod, seed):
        rng = random.Random(seed)
        return [mod.gen_case(rng) for _ in range(240)]

    g_pr = {json.dumps(x, sort_keys=True) for x in gen_set(pr, bi)}
    g_mt = [x for x in gen_set(mm16, bi ^ 1) if json.dumps(x, sort_keys=True) not in g_pr]
    X = g_mt[0]
    wrap = S + "/probe/wrong-on-X.py"
    open(wrap, "w").write(
        "import json,subprocess,sys\nX = %s\ndata = sys.stdin.read()\n"
        "try:\n    same = json.loads(data) == X\nexcept Exception:\n    same = False\n"
        "if same:\n    print(json.dumps({\"decision\": \"__wrong__\"})); sys.exit(0)\n"
        "r = subprocess.run([sys.executable, \"-I\", \"-B\", %r], input=data.encode(), capture_output=True)\n"
        "sys.stdout.write(r.stdout.decode()); sys.stderr.write(r.stderr.decode()); sys.exit(r.returncode)\n"
        % (json.dumps(X), FROZEN + "/pos-oracle.py"))
    d16 = S + "/probe/fr-base"
    if not os.path.exists(d16 + "/.git"):
        pass
    rp = run([PY, "-B", PRIST + "/c99_fresh304.py", "--root", CL, "--revision", BASE, "--candidate-file", wrap, "--work", S + "/probe/w-fr16p"])
    rm = run([PY, "-B", MUT + "/fr/FR16.py", "--root", CL, "--revision", BASE, "--candidate-file", wrap, "--work", S + "/probe/w-fr16m"])
    out.append("FR16 probe X=%s pristine rc=%d %s | mutant rc=%d %s | separated=%s" % (
        json.dumps(X, sort_keys=True)[:200], rp[0], stdout_body(rp[1])[0][-40:], rm[0], stdout_body(rm[1])[0][-40:], rp[0] != rm[0] or met_of(rp[1]) != met_of(rm[1])))
    print("\n".join(out))
    open(S + "/probes.txt", "w").write("\n".join(out) + "\n")


if __name__ == "__main__":
    main(sys.argv[1])
