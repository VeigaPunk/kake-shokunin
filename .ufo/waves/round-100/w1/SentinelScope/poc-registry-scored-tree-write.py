#!/usr/bin/env python3
"""SentinelScope PoC (C1, c100_registry.py SANDBOX): writes into the shared scored tree.

Usage: python3 -B poc-registry-scored-tree-write.py --scratch DIR
The sandbox binds the extracted scored tree (and the whole work dir) read-write. The tree is ONE
extraction shared by every self-test and every probe, and self-tests run before probes. Two cases:
  self-rewrite  a.py's self-test rewrites a.py; a.py's own probe then runs the rewritten file.
  cross-row     row a's self-test rewrites scripts/b.py; row b (\"no self-test\") is then probed on
                the rewritten file.
Committed files are unchanged (git show HEAD:...), the counter still reports met=true on the cross-row
case. Writes only under --scratch."""
import argparse
import hashlib
import importlib.util
import os
import shutil
import subprocess
import sys

sys.dont_write_bytecode = True
LANE_COUNTER = "/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-100/c100_registry.py"
HEADER = "| Name | Kind | Entry command | Verdict map | Self-test | Write scope | Owner |\n|---|---|---|---|---|---|---|\n"
VM = "`0=ok`; `1=bad`"
A_SELFREWRITE = (
    "import sys\n"
    "if '--selftest' in sys.argv:\n"
    "    open(__file__, 'w').write('import sys\\nsys.exit(0)\\n')\n"
    "    print('selftest 1/1'); sys.exit(0)\n"
    "sys.exit(64 if len(sys.argv) > 1 else 0)\n")
A_CROSSROW = (
    "import sys\n"
    "if '--selftest' in sys.argv:\n"
    "    open('scripts/b.py', 'w').write('import sys\\nsys.exit(0)\\n')\n"
    "    print('selftest 1/1'); sys.exit(0)\n"
    "sys.exit(64 if len(sys.argv) > 1 else 0)\n")
B_HONEST = "import sys\n# committed: unknown flag -> 64 (unmapped)\nsys.exit(64 if len(sys.argv) > 1 else 0)\n"


def load_counter():
    spec = importlib.util.spec_from_file_location("c100r", LANE_COUNTER)
    m = importlib.util.module_from_spec(spec)
    sys.modules["c100r"] = m
    spec.loader.exec_module(m)
    return m


def fixture(root, name, files, rows):
    d = os.path.join(root, "fx-" + name)
    shutil.rmtree(d, ignore_errors=True)
    os.makedirs(os.path.join(d, "scripts"))
    subprocess.run(["git", "-C", d, "init", "-q"], check=True)
    top = subprocess.run(["git", "-C", d, "rev-parse", "--show-toplevel"], capture_output=True, text=True).stdout.strip()
    assert os.path.realpath(top) == os.path.realpath(d)
    for p, src in files.items():
        open(os.path.join(d, p), "w").write(src)
    open(os.path.join(d, "SKILL.md"), "w").write(HEADER + rows)
    subprocess.run(["git", "-C", d, "add", "-A"], check=True)
    subprocess.run(["git", "-C", d, "-c", "user.name=SentinelScope", "-c", "user.email=SentinelScope@example.invalid",
                    "commit", "-q", "-m", name], check=True)
    return d


def sha(b):
    return hashlib.sha256(b).hexdigest()[:12]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--scratch", required=True)
    a = ap.parse_args()
    root = os.path.abspath(a.scratch)
    os.makedirs(root, exist_ok=True)
    m = load_counter()
    cases = {
        "self-rewrite": ({"scripts/a.py": A_SELFREWRITE},
                         "| a | gate | `python3 -B scripts/a.py` | %s | `python3 -B scripts/a.py --selftest` | none | kake |\n" % VM),
        "cross-row": ({"scripts/a.py": A_CROSSROW, "scripts/b.py": B_HONEST},
                      "| a | gate | `python3 -B scripts/a.py` | `0=ok`; `1=bad`; `64=usage` | `python3 -B scripts/a.py --selftest` | none | kake |\n"
                      "| b | gate | `python3 -B scripts/b.py` | %s | no self-test | none | kake |\n" % VM),
    }
    for name, (files, rows) in cases.items():
        d = fixture(root, name, files, rows)
        w = os.path.join(root, "w-" + name)
        shutil.rmtree(w, ignore_errors=True)
        os.makedirs(w)
        met, text = m.score(d, "HEAD", w)
        committed = {rel: subprocess.run(["git", "-C", d, "show", "HEAD:" + rel], capture_output=True).stdout for rel in files}
        print("== %s met=%s" % (name, met))
        print(text)
        tree = os.path.join(w, "tree")
        for rel in ["scripts/a.py", "scripts/b.py"]:
            tp = os.path.join(tree, rel)
            if os.path.exists(tp):
                print("   scored-tree %-12s sha=%s" % (rel, sha(open(tp, "rb").read())))
        for rel, blob in committed.items():
            print("   committed    %-12s sha=%s" % (rel, sha(blob)))
        shutil.rmtree(w, ignore_errors=True)


if __name__ == "__main__":
    sys.exit(main())
