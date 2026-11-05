#!/usr/bin/env python3
"""Round-92 C1 mutation runner (fixture class 6, honest differential).

Applies one source mutation to the gate blob per --mutant id, runs the mutated
gate against the committed key constructor, and reports verdict=killed when
the gate rejects (non-zero exit), verdict=survived otherwise. Target `base`
runs the unmutated gate and must survive. No output is canned: every verdict
is the observed exit of a real gate run.
"""
import os
import subprocess
import sys
import tempfile

GATE = "scripts/cache_key_conformance.py"
CAND = "scripts/cache_key.py"

MUTANTS = [
    ("M01", 'if ch == "%":', 'if ch == "&":'),
    ("M02", 'out.append("%25")', 'out.append("%26")'),
    ("M03", 'elif ch in (GS, X1D, RS, US):', 'elif ch in (GS, X1D, RS):'),
    ("M04", 'out.append("%%%02X" % ord(ch))', 'out.append("%%%02X" % (ord(ch) + 1))'),
    ("M05", 'return len(s) > 0 and all(c in TCHARS for c in s)',
     'return len(s) >= 0 and all(c in TCHARS for c in s)'),
    ("M06", 'low = name.lower()', 'low = name'),
    ("M07", 'seen[low] = value', 'seen[value] = low'),
    ("M08", 'vary = obj["vary"] if "vary" in obj else ""',
     'vary = obj["vary"] if "vary" in obj else "a"'),
    ("M09", 'if type(vary) is not str:', 'if type(vary) is str:'),
    ("M10", 'm = _trim(raw)', 'm = raw'),
    ("M11", 'if m == "*" or not _token(m):', 'if m == "Q" or not _token(m):'),
    ("M12", 'members.append(m.lower())', 'members.append(m)'),
    ("M13", 'for name in sorted(members):', 'for name in sorted(members, reverse=True):'),
    ("M14", 'pairs.append(_esc(name) + RS + _esc(_trim(seen[name])))',
     'pairs.append(_esc(name) + GS + _esc(_trim(seen[name])))'),
    ("M15", 'pairs.append(_esc(name) + RS + GS)', 'pairs.append(_esc(name) + RS + US)'),
    ("M16", 'return _esc(uri) + ("" if not pairs else US + US.join(pairs))',
     'return _esc(uri) + ("" if not pairs else GS + US.join(pairs))'),
    ("M17", 'return json.dumps(obj).encode()', 'return json.dumps(obj).upper().encode()'),
    ("M18", 'ok = (rc == 1 and out == b"" and', 'ok = (rc == 1 and out != b"" and'),
    ("M19", 'doc[0][0] != "key"', 'doc[0][0] != "keY"'),
    ("M20", 'return (p.returncode, p.stdout, p.stderr)', 'return (0, p.stdout, p.stderr)'),
]


def main(argv):
    if "--mutant" not in argv:
        print("usage: mutate-tip.py --mutant base|M<nn>", file=sys.stderr)
        return 3
    target = argv[argv.index("--mutant") + 1]
    scratch = os.environ.get("HYAKU_SCRATCH")
    if not scratch:
        print("HYAKU_SCRATCH is required", file=sys.stderr)
        return 4
    os.makedirs(scratch, exist_ok=True)
    work = tempfile.mkdtemp(prefix="mut-", dir=scratch)
    with open(GATE, "rb") as fh:
        src = fh.read().decode("utf-8")
    if target == "base":
        mutated = src
    else:
        site = {m[0]: m for m in MUTANTS}.get(target)
        if site is None:
            print("unknown mutant id: %s" % target, file=sys.stderr)
            return 3
        _, old, new = site
        if src.count(old) != 1:
            print("mutation site not unique for %s" % target, file=sys.stderr)
            return 3
        mutated = src.replace(old, new, 1)
    gate_path = os.path.join(work, "gate_under_test.py")
    with open(gate_path, "w") as fh:
        fh.write(mutated)
    gate_work = os.path.join(work, "gw")
    os.makedirs(gate_work, exist_ok=True)
    p = subprocess.run([sys.executable, "-B", gate_path, "--candidate", CAND,
                        "--seed", "92", "--generated", "10",
                        "--work", gate_work],
                       cwd=os.getcwd(), capture_output=True)
    rc = p.returncode
    if target == "base":
        print("verdict=survived rc=0" if rc == 0 else "verdict=killed rc=%d" % rc)
    else:
        print("verdict=killed rc=%d" % rc if rc != 0 else "verdict=survived rc=0")
    return 0


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
