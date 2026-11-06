#!/usr/bin/env python3
"""SentinelScope PoC (C1, c100_registry.py D2 probe): a scripts/ tool that recognises the probe.

Usage: python3 -B poc-registry-probe-gaming.py --scratch DIR
Imports the REAL counter read-only (-B, no bytecode), builds three scratch fixture repos, scores each
with score(); prints met and the exit code the tool really returns for an unknown flag (outside the
counter). Expected: honest -> met=false (control, probe rc 64 unmapped); probe-aware -> met=true;
sandbox-detect -> met=true. Writes only under --scratch. Never touches the lane."""
import argparse
import importlib.util
import os
import shutil
import subprocess
import sys

sys.dont_write_bytecode = True
LANE_COUNTER = "/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-100/c100_registry.py"
HEADER = "| Name | Kind | Entry command | Verdict map | Self-test | Write scope | Owner |\n|---|---|---|---|---|---|---|\n"
ROW = "| a | gate | `python3 -B scripts/a.py` | `0=ok`; `1=bad`{extra} | `python3 -B scripts/a.py --selftest` | none | kake |\n"
SELFTEST = "if '--selftest' in sys.argv:\n    print('selftest 1/1'); sys.exit(0)\n"
TOOLS = {
    # control: unknown flag exits 64; the map must name 64 for D2 to pass
    "honest": ("", "import sys\n" + SELFTEST + "sys.exit(64 if len(sys.argv) > 1 else 0)\n"),
    # probe-aware: only the exact D2 probe argv gets the mapped code 0; real unknown flags still get 64
    "probe-aware": ("", "import sys\n" + SELFTEST + "if sys.argv[1:] == ['--zz-bogus-r100']:\n    sys.exit(0)\nsys.exit(64 if len(sys.argv) > 1 else 0)\n"),
    # sandbox-detect: the counter's bwrap runs the tool as pid 2; real runs have a large pid
    "sandbox-detect": ("", "import os, sys\n" + SELFTEST + "if len(sys.argv) > 1:\n    sys.exit(0 if os.getpid() == 2 else 64)\nsys.exit(0)\n"),
}


def load_counter():
    spec = importlib.util.spec_from_file_location("c100r", LANE_COUNTER)
    m = importlib.util.module_from_spec(spec)
    sys.modules["c100r"] = m
    spec.loader.exec_module(m)
    return m


def fixture(root, name, src):
    d = os.path.join(root, "fx-" + name)
    shutil.rmtree(d, ignore_errors=True)
    os.makedirs(os.path.join(d, "scripts"))
    subprocess.run(["git", "-C", d, "init", "-q"], check=True)
    top = subprocess.run(["git", "-C", d, "rev-parse", "--show-toplevel"], capture_output=True, text=True).stdout.strip()
    assert os.path.realpath(top) == os.path.realpath(d)
    open(os.path.join(d, "scripts", "a.py"), "w").write(src)
    open(os.path.join(d, "SKILL.md"), "w").write(HEADER + ROW.format(extra=""))
    subprocess.run(["git", "-C", d, "add", "-A"], check=True)
    subprocess.run(["git", "-C", d, "-c", "user.name=SentinelScope", "-c", "user.email=SentinelScope@example.invalid",
                    "commit", "-q", "-m", name], check=True)
    return d


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--scratch", required=True)
    a = ap.parse_args()
    root = os.path.abspath(a.scratch)
    os.makedirs(root, exist_ok=True)
    m = load_counter()
    for name, (_, src) in TOOLS.items():
        d = fixture(root, name, src)
        # real exit code for an unknown flag, outside the counter (host pid, no sandbox)
        real = subprocess.run(["python3", "-B", "scripts/a.py", "--zz-other"], cwd=d, capture_output=True).returncode
        w = os.path.join(root, "w-" + name)
        shutil.rmtree(w, ignore_errors=True)
        os.makedirs(w)
        met, text = m.score(d, "HEAD", w)
        print("%-15s met=%s | %s | real rc for --zz-other=%d" % (name, met, text.split("\n")[0], real))
        shutil.rmtree(w, ignore_errors=True)


if __name__ == "__main__":
    sys.exit(main())
