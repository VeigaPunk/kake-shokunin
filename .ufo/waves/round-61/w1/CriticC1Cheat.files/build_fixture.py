#!/usr/bin/env python3
"""Build contract-conformant c61 fixtures (L2 and L3 shapes) with seeded ids."""
import os, subprocess, sys, tempfile, hashlib

def git(d, *args, env_extra=None):
    e = dict(os.environ)
    e.update({"GIT_AUTHOR_DATE": "2026-10-27T12:00:00", "GIT_COMMITTER_DATE": "2026-10-27T12:00:00"})
    if env_extra: e.update(env_extra)
    subprocess.run(["git", "-C", d] + list(args), check=True, env=e,
                   capture_output=True)

def build_case(seed, case, base):
    d = tempfile.mkdtemp(prefix=f"c61-{case}-s{seed}-", dir=base)
    git(d, "init", "-q")
    top = subprocess.run(["git", "-C", d, "rev-parse", "--show-toplevel"],
                         capture_output=True, text=True, check=True).stdout.strip()
    assert top == d, (top, d)
    ident = ["-c", "user.name=selftest", "-c", "user.email=selftest@local"]
    rng = int(hashlib.sha256(f"{seed}:{case}".encode()).hexdigest(), 16)
    rid = f"r{(rng % 40) + 61}-s{seed}"           # seeded round id in path
    path = f".ufo/waves/{rid}/controls/receipt-{rng % 997}.txt"
    os.makedirs(os.path.join(d, os.path.dirname(path)), exist_ok=True)
    def commit(msg):
        git(d, *ident, "add", "-A")
        git(d, *ident, "commit", "-q", "-m", msg)
    # first version: receipt grammar + a result span line carrying 'pending'
    with open(os.path.join(d, path), "w") as f:
        f.write(f"# receipt: {rid}\nrun {rng%89}\nrevision: {rid}-1\npending: conditions pending\n")
    commit(f"seed {seed} case {case} add receipt")
    c_add = subprocess.run(["git", "-C", d, "rev-parse", "HEAD"],
                           capture_output=True, text=True).stdout.strip()
    if case in ("L2", "L3"):
        with open(os.path.join(d, path), "w") as f:
            f.write(f"# receipt: {rid}\nrun {rng%89}\nrevision: {rid}-2\npending: conditions pending\n")
        commit(f"seed {seed} case {case} rewrite revision line")
    c_re = subprocess.run(["git", "-C", d, "rev-parse", "HEAD"],
                          capture_output=True, text=True).stdout.strip()
    disc = None
    if case == "L3":
        disc = {"entries": [{"path": path, "commit": c_re, "kind": "rewrite",
                             "note": f"seed {seed}", "disclosed-by": "fixture"}]}
    return {"dir": d, "path": path, "commit_add": c_add, "commit_rewrite": c_re,
            "disclosures": disc, "seed": seed, "case": case}

if __name__ == "__main__":
    base = sys.argv[1]
    seed = sys.argv[2]
    case = sys.argv[3]
    info = build_case(int(seed), case, base)
    print(info)
