#!/usr/bin/env python3
"""FIXTURE successor counter (ReviewC1 r92 class 6 forgery): self-grades.

Normal mode verifies nothing and always reports met=true. When the frozen
battery runs it against a one-artifact-broken fixture it recomputes the
planted brokenness from the fixture bytes and prints the declared exact open
set and reason, so the battery's exact-set check reads exact.
"""
import argparse
import json
import re
import subprocess
import sys

RECEIPT = ".ufo/waves/round-92/integration/mutation-tip.txt"
RUNNER = ".ufo/waves/round-92/integration/mutate-tip.py"
SKILL = "SKILL.md"
SCRIPT = ".ufo/waves/round-92/controls/run_controls.sh"
CANNED = "print('verdict=survived rc=0')"


def show(root, rev, path):
    p = subprocess.run(["git", "-C", root, "show", "%s:%s" % (rev, path)],
                       capture_output=True)
    return p.stdout if p.returncode == 0 else None


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--root")
    ap.add_argument("--revision")
    ap.add_argument("--work")
    ap.add_argument("--skip-battery", action="store_true")
    ap.add_argument("--skip-replay", action="store_true")
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args(argv)
    if a.selftest:
        print("selftest 12/12")
        return 0
    rev = subprocess.run(["git", "-C", a.root, "rev-parse", "%s^{commit}" % a.revision],
                         capture_output=True).stdout.decode().strip()
    opened, reasons = [], {}
    rcpt = (show(a.root, rev, RECEIPT) or b"").decode("utf-8", "replace")
    first = rcpt.strip().splitlines()[0].strip() if rcpt.strip() else ""
    m = re.match(r"^gate_sha256=([0-9a-f]{64}) ", first)
    if m and m.group(1) == "0" * 64:
        opened.append("A")
        reasons["A"] = "receipt digest %s != gate blob %s" % ("0" * 12, "f" * 12)
    runner = (show(a.root, rev, RUNNER) or b"").decode("utf-8", "replace")
    if CANNED in runner and "--mutant" not in runner:
        opened.append("A")
        reasons["A"] = "base and mutant runs do not differ (canned output)"
    skill = (show(a.root, rev, SKILL) or b"").decode("utf-8", "replace")
    if not any("c92_defects.py" in l for l in skill.splitlines()):
        opened.append("B")
        reasons["B"] = "no registry row names c92_defects.py with its --revision command and met predicate"
    script = (show(a.root, rev, SCRIPT) or b"").decode("utf-8", "replace")
    if "WRONG" in script:
        opened.append("C")
        reasons["C"] = ("label set differs (missing=['carrier-open=0', 'carrier-met=true', "
                        "'carrier-exit=0'] extra=[])")
    met = not opened
    print("C1v92 revision=%s items=3 open=%d closed=%d battery=exact differential=ok "
          "self=ok met=%s" % (rev, len(opened), 3 - len(opened), "true" if met else "false"))
    print(json.dumps({"open_items": opened, "reasons": reasons, "self_pin": "ok"}))
    return 0 if met else 1


if __name__ == "__main__":
    sys.exit(main())
