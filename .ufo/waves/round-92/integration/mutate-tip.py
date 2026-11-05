#!/usr/bin/env python3
"""Differential mutation runner for the tip conformance gate (round 92, item A).

Invoke as `python3 -B mutate-tip.py --mutant <base|M<nn>>` with the lane checkout as cwd.

The check is the gate's own conformance run: `scripts/cache_key_conformance.py` scores the
shipped candidate `scripts/cache_key.py` at the fixed seed below.

  base    runs the unmutated gate. verdict=survived rc=0 iff that run exits 0 (met=true);
          otherwise verdict=killed rc=<gate rc>.
  M<nn>   applies the table entry to a copy of the gate in a scratch directory (one literal
          replacement that must match exactly once), runs the same check, and prints
          verdict=killed rc=<rc> when the mutant run exits nonzero and verdict=survived rc=0
          when it exits 0.

The last stdout line is always the verdict. Exit 0 once a verdict is printed; exit 2 when no
verdict can be determined (usage, missing gate or candidate, scratch unavailable, anchor
mismatch, timeout). Stdlib only. Scratch: $HYAKU_SCRATCH, else $TMPDIR; never /tmp.
"""

import argparse
import os
import re
import shutil
import subprocess
import sys
import tempfile

GATE = "scripts/cache_key_conformance.py"
CANDIDATE = "scripts/cache_key.py"
SEED = "92"

# Frozen mutant table: (id, what the mutation changes, exact old text, exact new text).
# Each old text must occur exactly once in the gate source or the mutant is not produced.
MUTANTS = (
    ("M01", "reference drops the sort of vary members",
     "for name in sorted(members):", "for name in members:"),
    ("M02", "reference keeps vary members in their original case",
     "members.append(m.lower())", "members.append(m)"),
    ("M03", "reference stores header values under the raw name (case-sensitive lookup)",
     "seen[low] = value", "seen[name] = value"),
    ("M04", "reference does not percent-escape '%' in names and values",
     'out.append("%25")', 'out.append("%")'),
    ("M05", "reference writes separator escapes in lowercase hex",
     'out.append("%%%02X" % ord(ch))', 'out.append("%%%02x" % ord(ch))'),
    ("M06", "reference trims VT as optional whitespace",
     r'while i < j and s[i] in " \t":', r'while i < j and s[i] in " \t\x0b":'),
    ("M07", "reference accepts the wildcard vary member",
     'if m == "*" or not _token(m):', "if not _token(m):"),
    ("M08", "reference drops the duplicate-header-name refusal",
     "if low in seen:", "if False:"),
    ("M09", "reference drops the duplicate-vary-member refusal",
     "if len(set(members)) != len(members):", "if False:"),
    ("M10", "reference drops the empty-marker for absent vary members",
     "pairs.append(_esc(name) + RS + GS)", "pairs.append(_esc(name) + RS)"),
    ("M11", "reference token set loses '!'",
     'TCHARS = "!#$%&', 'TCHARS = "#$%&'),
    ("M12", "reference does not escape the request URI",
     "return _esc(uri) + (", "return uri + ("),
    ("M13", "reference treats an empty Vary as a member list",
     'if vary != "":', "if True:"),
    ("M14", "reference keeps optional whitespace around stored values",
     "_esc(_trim(seen[name]))", "_esc(seen[name])"),
    ("M15", "reference joins pairs with RS instead of US",
     "US.join(pairs)", "RS.join(pairs)"),
    ("M16", "reference accepts header names that are not tokens",
     "if type(name) is not str or not _token(name):", "if type(name) is not str:"),
    ("M17", "reference accepts CR and LF in header values",
     r'if type(value) is not str or "\r" in value or "\n" in value:', "if type(value) is not str:"),
    ("M18", "reference drops the request-URI type check",
     "if type(uri) is not str:", "if False:"),
    ("M19", "reference drops the Vary type check",
     "if type(vary) is not str:", "if False:"),
    ("M20", "sandbox empties the stdlib roots (every stdlib file read is denied)",
     "tuple(_roots),", "(),"),
    ("M21", "sandbox drops os.system from the denied events",
     '"subprocess.Popen", "os.system", "os.exec",', '"subprocess.Popen", "os.exec",'),
    ("M22", "sandbox drops gc.get_objects from the denied events",
     '"gc.get_objects", "gc.get_referrers",', '"gc.get_referrers",'),
    ("M23", "sandbox drops _posixsubprocess from the denied modules",
     'frozenset(("_posixsubprocess", "subprocess", "_ctypes",', 'frozenset(("subprocess", "_ctypes",'),
    ("M24", "sandbox drops the import audit branch",
     'if event == "import":', "if False:"),
    ("M25", "sandbox drops the open audit branch",
     'elif event == "open":', "elif False:"),
    ("M26", "met ignores the generated tally",
     "and gen_pass == len(gen))", ")"),
    ("M27", "generated population off by default",
     "type=int, default=120)", "type=int, default=0)"),
    ("M28", "self-check of the reference is skipped",
     "if not self_check():", "if False:"),
    ("M29", "judge drops the stdout-emptiness requirement on refusals",
     'rc == 1 and out == b"" and', "rc == 1 and"),
    ("M30", "clause verdicts are last-wins instead of conjunctive",
     "clause_ok[clause] = clause_ok.get(clause, True) and ok", "clause_ok[clause] = ok"),
)

MUTANT_IDS = {m[0]: m for m in MUTANTS}


def scratch_dir():
    base = os.environ.get("HYAKU_SCRATCH") or os.environ.get("TMPDIR")
    if not base:
        return None, "no HYAKU_SCRATCH or TMPDIR set"
    base = os.path.realpath(base)
    if base == "/tmp" or base.startswith("/tmp/"):
        return None, "scratch under /tmp refused"
    os.makedirs(base, exist_ok=True)
    return tempfile.mkdtemp(prefix="mutate-tip-", dir=base), ""


def run_gate(gate_path, work):
    os.makedirs(work, exist_ok=True)
    cmd = [sys.executable, "-B", gate_path, "--candidate", CANDIDATE,
           "--work", work, "--seed", SEED]
    try:
        p = subprocess.run(cmd, cwd=os.getcwd(), capture_output=True, timeout=1500)
    except subprocess.TimeoutExpired:
        return None
    return p


def main(argv=None):
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[0])
    ap.add_argument("--mutant", required=True, help="base or M<nn>")
    a = ap.parse_args(argv)
    if a.mutant != "base" and a.mutant not in MUTANT_IDS:
        print("mutate-tip: unknown mutant %r" % a.mutant)
        return 2
    lane = os.getcwd()
    gate_src = os.path.join(lane, GATE)
    cand = os.path.join(lane, CANDIDATE)
    if not os.path.isfile(gate_src) or not os.path.isfile(cand):
        print("mutate-tip: gate or candidate missing under cwd %s" % lane)
        return 2
    work, why = scratch_dir()
    if work is None:
        print("mutate-tip: %s" % why)
        return 2
    try:
        if a.mutant == "base":
            gate_path = gate_src
            print("mutant=base gate=%s candidate=%s seed=%s" % (GATE, CANDIDATE, SEED))
        else:
            mid, desc, old, new = MUTANT_IDS[a.mutant]
            with open(gate_src, encoding="utf-8") as fh:
                src = fh.read()
            count = src.count(old)
            if count != 1:
                print("mutate-tip: %s anchor count=%d (want 1)" % (mid, count))
                return 2
            mut_dir = os.path.join(work, mid)
            os.makedirs(mut_dir)
            gate_path = os.path.join(mut_dir, "cache_key_conformance.py")
            with open(gate_path, "w", encoding="utf-8") as fh:
                fh.write(src.replace(old, new, 1))
            print("mutant=%s mutation=%s gate=%s candidate=%s seed=%s"
                  % (mid, desc, GATE, CANDIDATE, SEED))
        p = run_gate(gate_path, os.path.join(work, "run"))
        if p is None:
            print("mutate-tip: gate run timed out")
            return 2
        out = p.stdout.decode("utf-8", "replace").strip().splitlines()
        for line in out[-2:]:
            print(line)
        if p.stderr.strip():
            print("stderr-tail: " + p.stderr.decode("utf-8", "replace").strip().splitlines()[-1][:200])
        rc = p.returncode
        verdict = "survived" if rc == 0 else "killed"
        print("verdict=%s rc=%d" % (verdict, rc))
        return 0
    finally:
        shutil.rmtree(work, ignore_errors=True)


if __name__ == "__main__":
    sys.exit(main())
