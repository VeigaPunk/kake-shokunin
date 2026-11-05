import importlib.util, json, os, re, subprocess, sys
sys.dont_write_bytecode = True
S = "/fast/scratch/hyaku/kake-r94/CriticClaims/x"
CL = S + "/clone"; L = "/home/vgpnk/Projects/shokunin/kake-shokunin"; BASE = "ba667b24"
def git(*a): return subprocess.run(["git", "-C", CL, *a], capture_output=True)
spec = importlib.util.spec_from_file_location("c94", L + "/.ufo/waves/round-94/c94_selfassess.py")
c94 = importlib.util.module_from_spec(spec); spec.loader.exec_module(c94)
assert git("rev-parse", "--show-toplevel").stdout.decode().strip() == CL
skill = git("show", BASE + ":SKILL.md").stdout.decode()
lines = skill.split("\n")
# locate tree-kind rows (E5 'names a tree') in the base SKILL
targets = []
for i, line in enumerate(lines):
    if not line.startswith("|"): continue
    for raw in c94.PATH_RE.findall(line):
        p = re.sub(r":\d+(-\d+)?$", "", raw).rstrip("`,.")
        if "<" in p or "*" in p: continue
        for path in c94.expand_braces(p):
            m = c94.blob_meta(CL, BASE, path)
            if m and m[0] != "blob":
                targets.append((i, path)); break
print("tree-path rows:", len(targets), targets[:3])
def run_counter(tag):
    w = os.path.join(S, "runs", tag); os.makedirs(w, exist_ok=True)
    rev = git("rev-parse", "HEAD").stdout.decode().strip()
    p = subprocess.run([sys.executable, "-B", L + "/.ufo/waves/round-94/c94_selfassess.py", "--root", CL,
                        "--revision", rev, "--work", w], capture_output=True, env={**os.environ, "TMPDIR": w}, timeout=600)
    out = p.stdout.decode().splitlines()
    detail = json.loads(out[1]) if len(out) > 1 else {}
    return p.returncode, out[0] if out else "", [m["detail"] for m in detail.get("mismatches", [])], detail.get("identity_missing"), detail.get("short")
def commit_skill(text, msg):
    open(CL + "/SKILL.md", "w", encoding="utf-8").write(text)
    git("add", "SKILL.md")
    r = subprocess.run(["git", "-C", CL, "-c", "user.name=critic-fixture", "-c", "user.email=critic@fixture.invalid",
                        "commit", "-q", "-m", msg], capture_output=True)
    assert r.returncode == 0, r.stderr
results = {}
# X0 control: base content recommitted unchanged (must reproduce 15)
git("checkout", "-q", "--detach", BASE)
rc, l1, mm, ident, short = run_counter("X0-base")
results["X0-base"] = {"rc": rc, "line1": l1, "n": len(mm), "ident": ident, "short": short}
i0, p0 = targets[0]
def variant(name, fn):
    git("checkout", "-q", "--detach", BASE)
    new = list(lines); new[i0] = fn(new[i0], p0)
    commit_skill("\n".join(new), name)
    rc, l1, mm, ident, short = run_counter(name)
    results[name] = {"rc": rc, "line1": l1, "n": len(mm), "ident": ident, "short": short, "mm": mm[:3]}
# X1: de-backtick the tree path in its row (prose mention, no path token)
variant("X1-deBacktick", lambda s, p: s.replace("`" + p + "`", p, 1))
# X2: replace the tree path with an annotated absence of a path that does not exist
variant("X2-annotateFabricatedAbsence", lambda s, p: s.replace("`" + p + "`", "[r94-absence 2026-11-05: `" + p.rstrip("/") + "/none.md` absent]", 1))
# X3: annotate the same tree path as absent (must be a finding: path exists)
variant("X3-annotatePresentTree", lambda s, p: s.replace("`" + p + "`", "[r94-absence 2026-11-05: `" + p + "` absent]", 1))
git("checkout", "-q", "--detach", BASE)
print(json.dumps(results, indent=1, sort_keys=True))
json.dump(results, open(S + "/exp-results.json", "w"), indent=1, sort_keys=True)
