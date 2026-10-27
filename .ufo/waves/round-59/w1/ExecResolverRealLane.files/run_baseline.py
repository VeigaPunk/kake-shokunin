#!/usr/bin/env python3
"""No-harm baseline for Claim C2: run the CURRENT tool at each of the last 10
first-parent revisions of master, with the real fleet root and with an empty fleet dir."""
import os
import subprocess
import sys

LANE = "/home/vgpnk/Projects/shokunin/kake-shokunin"
TOOL = os.path.join(LANE, "scripts/id_resolver.py")
FLEET = "/home/vgpnk/Projects/shokunin"
SCRATCH = "/fast/scratch/hyaku/kake-r59/ExecResolverRealLane"
EMPTY = os.path.join(SCRATCH, "empty-fleet")


def env():
    e = {k: v for k, v in os.environ.items() if not k.startswith("GIT_")}
    e.update({"LC_ALL": "C.UTF-8", "PYTHONDONTWRITEBYTECODE": "1", "TMPDIR": SCRATCH})
    return e


def run(argv):
    p = subprocess.run(argv, capture_output=True, env=env(), timeout=900)
    return p.returncode, p.stdout.decode("utf-8", "replace"), p.stderr.decode("utf-8", "replace")


def main():
    os.makedirs(EMPTY, exist_ok=True)
    p = subprocess.run(["git", "-C", LANE, "rev-list", "--first-parent", "-10", "master"],
                       capture_output=True, env=env())
    revs = p.stdout.decode().split()
    print(f"# tool blob: {subprocess.run(['git','-C',LANE,'rev-parse','master:scripts/id_resolver.py'],capture_output=True).stdout.decode().strip()}")
    print(f"# empty fleet dir: {EMPTY} entries={os.listdir(EMPTY)}")
    for rev in revs:
        subj = subprocess.run(["git", "-C", LANE, "log", "-1", "--format=%s", rev],
                              capture_output=True).stdout.decode().strip()
        for label, fleet in (("real-fleet", FLEET), ("empty-fleet", EMPTY)):
            rc, out, err = run([sys.executable, "-B", TOOL, "--root", LANE, "--revision", rev, "--fleet", fleet])
            summary = [l for l in out.splitlines() if l.startswith("ids_cited=")]
            dangling = [l for l in out.splitlines() if l.startswith("DANGLING")]
            print(f"[{rev[:12]}] fleet={label} exit={rc} n_dangling_lines={len(dangling)}")
            print(f"    summary: {summary[-1] if summary else '(none)'}")
            if err.strip():
                print(f"    stderr: {err.strip()[:300]}")
        print(f"    subject: {subj}")


if __name__ == "__main__":
    main()
