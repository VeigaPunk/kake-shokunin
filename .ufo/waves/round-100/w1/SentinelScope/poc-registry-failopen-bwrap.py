#!/usr/bin/env python3
"""SentinelScope PoC (C1, c100_registry.py probe()): no sandbox_ok() gate, so a failing bwrap is read as
the tool's exit code.

Usage: python3 -B poc-registry-failopen-bwrap.py --scratch DIR
Control: real bwrap -> probe rc 64 (unmapped) -> met=false.
Broken: a scratch PATH shim `bwrap` that runs the real bwrap with one bind whose source does not exist
(bwrap exits 1 natively, the same class as an unavailable user namespace) -> probe rc 1, which the
verdict map names -> met=true with no tool ever executed. (c100_fresh304.py has sandbox_ok() and fails
closed under the same shim; see poc-fresh304-sandbox-probe.py.) Writes only under --scratch."""
import argparse
import importlib.util
import os
import shutil
import subprocess
import sys

sys.dont_write_bytecode = True
LANE_COUNTER = "/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-100/c100_registry.py"
HEADER = "| Name | Kind | Entry command | Verdict map | Self-test | Write scope | Owner |\n|---|---|---|---|---|---|---|\n"
B_HONEST = "import sys\n# committed: unknown flag -> 64 (unmapped by the row)\nsys.exit(64 if len(sys.argv) > 1 else 0)\n"
SHIM = "#!/bin/sh\nexec /usr/bin/bwrap --ro-bind /nonexistent-r100-src /nonexistent-r100-dst \"$@\"\n"


def load_counter():
    spec = importlib.util.spec_from_file_location("c100r", LANE_COUNTER)
    m = importlib.util.module_from_spec(spec)
    sys.modules["c100r"] = m
    spec.loader.exec_module(m)
    return m


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--scratch", required=True)
    a = ap.parse_args()
    root = os.path.abspath(a.scratch)
    os.makedirs(os.path.join(root, "shim"), exist_ok=True)
    shim = os.path.join(root, "shim", "bwrap")
    open(shim, "w").write(SHIM)
    os.chmod(shim, 0o755)
    d = os.path.join(root, "fx-failopen")
    shutil.rmtree(d, ignore_errors=True)
    os.makedirs(os.path.join(d, "scripts"))
    subprocess.run(["git", "-C", d, "init", "-q"], check=True)
    open(os.path.join(d, "scripts", "b.py"), "w").write(B_HONEST)
    open(os.path.join(d, "SKILL.md"), "w").write(HEADER + "| b | gate | `python3 -B scripts/b.py` | `0=ok`; `1=bad` | no self-test | none | kake |\n")
    subprocess.run(["git", "-C", d, "add", "-A"], check=True)
    subprocess.run(["git", "-C", d, "-c", "user.name=SentinelScope", "-c", "user.email=SentinelScope@example.invalid",
                    "commit", "-q", "-m", "failopen"], check=True)
    m = load_counter()
    base_path = os.environ["PATH"]
    for label, path in [("control-real-bwrap", base_path), ("broken-bwrap-shim", shim_dir(shim) + ":" + base_path)]:
        os.environ["PATH"] = path
        w = os.path.join(root, "w-" + label)
        shutil.rmtree(w, ignore_errors=True)
        os.makedirs(w)
        probe_rc = m.probe("scripts/b.py", d, w, [0])  # probe the committed fixture root directly
        met, text = m.score(d, "HEAD", w)
        print("== %s bwrap_resolves_to=%s" % (label, shutil.which("bwrap")))
        print("   direct probe rc=%s" % probe_rc)
        print("   " + text.replace("\n", "\n   "))
        shutil.rmtree(w, ignore_errors=True)
    os.environ["PATH"] = base_path


def shim_dir(p):
    return os.path.dirname(p)


if __name__ == "__main__":
    sys.exit(main())
