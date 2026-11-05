import importlib.util, json, os, re, subprocess, sys, concurrent.futures as cf
LANE = "/home/vgpnk/Projects/shokunin/kake-shokunin"
W = LANE + "/.ufo/waves/round-97"
S = "/fast/scratch/hyaku/kake-r97/CriticClaims"
REV = "9e27ce0b2a8d168e032ab79ea11471b36eaceedf"
G = "/usr/bin/git"
ENV = {"PATH": "/usr/bin:/bin", "HOME": os.environ.get("HOME", "/"), "LC_ALL": "C", "GIT_NO_REPLACE_OBJECTS": "1", "GIT_CONFIG_NOSYSTEM": "1"}

def sh(*a, cwd=None, check=True):
    p = subprocess.run(list(a), capture_output=True, cwd=cwd, env=ENV)
    if check and p.returncode:
        raise SystemExit("FAIL %s rc=%d %s" % (a, p.returncode, p.stderr.decode()[:300]))
    return p.stdout.decode("utf-8", "replace")

def show(path):
    return sh(G, "-C", LANE, "show", "%s:%s" % (REV, path))

def fixture(name, edits):
    """edits: dict path -> new text. Clone LANE, checkout REV, write edits, commit. Returns new rev."""
    D = os.path.join(S, "fx-" + name)
    if os.path.exists(D):
        subprocess.run(["rm", "-rf", D], check=True)
    sh(G, "clone", "-q", "--shared", LANE, D)
    sh(G, "-C", D, "checkout", "-q", "--detach", REV)
    top = sh(G, "-C", D, "rev-parse", "--show-toplevel").strip()
    assert top == D, (top, D)
    for p, txt in edits.items():
        full = os.path.join(D, p)
        os.makedirs(os.path.dirname(full), exist_ok=True)
        with open(full, "w", encoding="utf-8") as fh:
            fh.write(txt)
    sh(G, "-C", D, "add", "-A")
    sh(G, "-C", D, "-c", "user.name=CriticClaims", "-c", "user.email=CriticClaims@example.invalid", "commit", "-qm", "critic " + name)
    return D, sh(G, "-C", D, "rev-parse", "HEAD").strip()

def run_counter(script, root, rev, name):
    work = os.path.join(S, "w-" + name)
    os.makedirs(work, exist_ok=True)
    p = subprocess.run([sys.executable, "-I", "-B", script, "--root", root, "--revision", rev, "--work", work],
                       capture_output=True, cwd=root, env=ENV, timeout=900)
    out = p.stdout.decode("utf-8", "replace").splitlines()
    return {"name": name, "rev": rev, "rc": p.returncode, "line1": out[0] if out else "", "line2": (out[1][:400] if len(out) > 1 else ""), "stderr_tail": p.stderr.decode("utf-8", "replace")[-300:]}
