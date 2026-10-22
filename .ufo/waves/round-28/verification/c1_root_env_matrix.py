#!/usr/bin/env python3
"""Top-level check case matrix for citing_set.py at 22c1669, b5d423f, 8ecbefe."""
import json, os, shutil, subprocess, sys

S = "/fast/scratch/hyaku/kake-r28a3/cases"
W = os.path.join(S, "cases")
GATES = [("22c1669", S + "/gates/gate-22c1669.py"), ("b5d423f", S + "/gates/gate-b5d423f.py"),
         ("8ecbefe", S + "/gates/gate-8ecbefe.py"), ("lane", "/home/vgpnk/Projects/shokunin/kake-shokunin/scripts/citing_set.py")]
GENV = {"GIT_AUTHOR_NAME": "c", "GIT_AUTHOR_EMAIL": "c@invalid", "GIT_COMMITTER_NAME": "c",
        "GIT_COMMITTER_EMAIL": "c@invalid", "GIT_CONFIG_GLOBAL": "/dev/null", "GIT_CONFIG_NOSYSTEM": "1"}
POP = {"rows": [{"id": "S001"}, {"id": "S002"}]}
CLEAN = {"pairs": [{"row": "S001", "file": "corpus/knowledge/entry.md"}]}
MISSING = {"pairs": []}
CITES = "# Entry\n\nThis statement cites S001.\n"
UNCITED = "# Entry\n\nThis statement cites nothing.\n"


def w(p, d):
    os.makedirs(os.path.dirname(p), exist_ok=True)
    open(p, "w").write(d)


def tree(root, ledger, entry):
    w(os.path.join(root, "population.json"), json.dumps(POP))
    w(os.path.join(root, "ledger.json"), json.dumps(ledger))
    w(os.path.join(root, "corpus/knowledge/entry.md"), entry)


def git(root, *a):
    env = {k: v for k, v in os.environ.items() if not k.startswith("GIT_")}
    env.update(GENV)
    subprocess.run(["git", "-C", root] + list(a), check=True, env=env,
                   stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)


def commit(root):
    git(root, "init", "-q", "-b", "main")
    git(root, "add", "-A")
    git(root, "commit", "-q", "-m", "c")


def nested(top):
    # Top tree reads clean (uncited, no pairs); sub tree reads failed (cites S001, no pair).
    tree(top, MISSING, UNCITED)
    tree(os.path.join(top, "sub"), MISSING, CITES)
    commit(top)


def run(gate, root, extra_env=None):
    env = {k: v for k, v in os.environ.items() if not k.startswith("GIT_")}
    env.update(extra_env or {})
    d = subprocess.run([sys.executable, "-B", gate, "--root", root, "--population", "population.json",
                        "--ledger", "ledger.json", "--revision", "HEAD", "--json"],
                       stdout=subprocess.PIPE, stderr=subprocess.PIPE, stdin=subprocess.DEVNULL,
                       env=env, timeout=30)
    try:
        r = json.loads(d.stdout)
        reasons = [f.get("reason") or f.get("id") for f in r.get("findings", [])]
        return "%d %s %s" % (d.returncode, r.get("verdict"), ",".join(map(str, reasons)))
    except ValueError:
        return "%d non-json %s" % (d.returncode, d.stderr.decode()[-120:].strip().replace("\n", " | "))


def main():
    shutil.rmtree(W, ignore_errors=True)
    os.makedirs(W)
    cases = []  # (id, root, env, want)

    n = os.path.join(W, "nested"); nested(n)
    cases.append(("N1 <repo>/sub", n + "/sub", None, "refuse"))
    cases.append(("N2 <repo> top (control)", n, None, "0 clean"))

    v = os.path.join(W, "valid"); tree(v, CLEAN, CITES); commit(v)
    f = os.path.join(W, "failed"); tree(f, MISSING, CITES); commit(f)
    cases.append(("K1 valid top clean", v, None, "0 clean"))
    cases.append(("K2 valid top failed", f, None, "1 failed"))

    bv = os.path.join(W, "bare-valid.git"); subprocess.run(["git", "clone", "-q", "--bare", v, bv], check=True)
    bf = os.path.join(W, "bare-failed.git"); subprocess.run(["git", "clone", "-q", "--bare", f, bf], check=True)
    cases.append(("B1 bare repo (clean content)", bv, None, "0 clean"))
    cases.append(("B2 bare repo (failed content)", bf, None, "1 failed"))
    cases.append(("B3 bare repo subdir refs/", bf + "/refs", None, "refuse"))

    sp = os.path.join(W, "space "); tree(sp, MISSING, CITES); commit(sp)
    cases.append(("T1 top level named 'space ' (failed content)", sp, None, "1 failed"))
    spn = os.path.join(W, "spacenest "); nested(spn)
    cases.append(("T2 'spacenest '/sub", spn + "/sub", None, "refuse"))
    nl = os.path.join(W, "nl\n"); tree(nl, MISSING, CITES); commit(nl)
    cases.append(("T3 top level name ends in newline (failed content)", nl, None, "1 failed"))
    nln = os.path.join(W, "nlnest"); tree(nln, MISSING, UNCITED); tree(os.path.join(nln, "x\n"), MISSING, CITES); commit(nln)
    cases.append(("T4 <repo>/'x\\n' nested", nln + "/x\n", None, "refuse"))

    lt = os.path.join(W, "link-top"); os.symlink(f, lt)
    cases.append(("L1 symlink to top level (failed content)", lt, None, "1 failed"))
    ls = os.path.join(W, "link-sub"); os.symlink(n + "/sub", ls)
    cases.append(("L2 symlink to <repo>/sub", ls, None, "refuse"))
    lp = os.path.join(W, "link-parent"); os.symlink(n, lp)
    cases.append(("L3 <symlink-to-repo>/sub", lp + "/sub", None, "refuse"))

    # Linked worktree: main HEAD clean, worktree branch HEAD failed.
    m = os.path.join(W, "wtmain"); tree(m, CLEAN, CITES); commit(m)
    git(m, "branch", "wt")
    wt = os.path.join(W, "wtlinked"); git(m, "worktree", "add", "-q", wt, "wt")
    w(os.path.join(wt, "ledger.json"), json.dumps(MISSING)); git(wt, "commit", "-qam", "drop pair")
    os.makedirs(os.path.join(wt, "sub"), exist_ok=True)
    tree(os.path.join(wt, "sub"), MISSING, CITES); git(wt, "add", "-A"); git(wt, "commit", "-qm", "sub")
    cases.append(("W1 linked worktree top (its HEAD failed, main HEAD clean)", wt, None, "1 failed"))
    cases.append(("W2 linked worktree <wt>/sub", wt + "/sub", None, "refuse"))

    cases.append(("G1 <repo>/.git (repo HEAD failed)", f + "/.git", None, "refuse or 1 failed"))
    cases.append(("G2 <repo>/.git/refs", f + "/.git/refs", None, "refuse or 1 failed"))
    cases.append(("G3 <nested>/.git (top tree clean, wants sub?)", n + "/.git", None, "refuse or 0 clean"))

    nr = os.path.join(W, "notrepo"); tree(nr, MISSING, CITES)
    cases.append(("R1 directory that is not a repository", nr, None, "refuse"))

    cases.append(("E1 GIT_DIR=<repo>/.git, root <repo>/sub", n + "/sub", {"GIT_DIR": n + "/.git"}, "refuse"))
    cases.append(("E2 GIT_WORK_TREE=<repo>/sub, root <repo>/sub", n + "/sub", {"GIT_WORK_TREE": n + "/sub"}, "refuse"))
    cases.append(("E3 GIT_DIR+GIT_WORK_TREE=<repo>/sub, root <repo>/sub", n + "/sub",
                  {"GIT_DIR": n + "/.git", "GIT_WORK_TREE": n + "/sub"}, "refuse"))
    cases.append(("E4 GIT_DIR=<clean repo>/.git, root non-repo (failed content)", nr, {"GIT_DIR": v + "/.git"}, "refuse"))
    cases.append(("E5 GIT_WORK_TREE=<repo>, root <repo>/sub", n + "/sub", {"GIT_WORK_TREE": n}, "refuse"))
    cases.append(("E6 GIT_DIR=<repo>/.git, root <repo> (control)", f, {"GIT_DIR": f + "/.git"}, "1 failed"))
    cases.append(("E7 GIT_WORK_TREE=<repo>, root <repo> (control)", f, {"GIT_WORK_TREE": f}, "1 failed"))

    rows = []
    for cid, root, env, want in cases:
        rows.append({"case": cid, "want": want, **{rev: run(g, root, env) for rev, g in GATES}})
    print(json.dumps(rows, indent=1))


main()
