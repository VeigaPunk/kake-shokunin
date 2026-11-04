#!/usr/bin/env python3
"""Build counter mutants (single-point edits of the frozen c91_reuse.py) and score each:
   met vs a conforming candidate, and met vs each frozen forgery."""
import concurrent.futures
import json
import os
import subprocess

S = "/fast/scratch/hyaku/kake-r91/MutReuse"
LANE = "/home/vgpnk/Projects/shokunin/kake-shokunin"
COUNTER = os.path.join(LANE, ".ufo/waves/round-91/c91_reuse.py")
FX = os.path.join(S, "fx")
MUT = os.path.join(S, "c91m")
CONFORMING_REV = "10995409cf01e746125fc7f24dec88bb50b601b3"  # scripts/stored_reuse.py = reference bytes
FORGERIES = [
    ".ufo/waves/round-91/frozen/neg-pin-reader.py",
    ".ufo/waves/round-91/frozen/neg-allowlist.py",
    ".ufo/waves/round-91/frozen/neg-blanket-refuse.py",
    ".ufo/waves/round-91/frozen/neg-blanket-admit.py",
    ".ufo/waves/round-91/frozen/neg-hash-table.py",
]

MUTANTS = [
    ("C01", "delete one hand case (fresh-max-age)",
     '    c.append(H("fresh-max-age", "max-age=60", "GET", 1000030, decision="reuse", lifetime=60, ageout=30))\n',
     ''),
    ("C02", "accept an extra output key",
     'if not isinstance(got, dict) or set(got) != KEYS_OUT:',
     'if not isinstance(got, dict) or not KEYS_OUT <= set(got):'),
    ("C03", "ignore the type of a value",
     '        if got[k] != expected[k] or type(got[k]) is not type(expected[k]):',
     '        if got[k] != expected[k]:'),
    ("C04", "skip the generated population",
     '        gen_expected = [(inp, reference(inp)) for inp in generate(seed, a.generated)]',
     '        gen_expected = []'),
    ("C05", "skip one forgery subject (neg-pin-reader)",
     '    ".ufo/waves/round-91/frozen/neg-pin-reader.py",\n',
     ''),
    ("C06", "stop checking the population pins",
     '        met = (not drift and pins_ok and not hits and hand_ok == len(cases)',
     '        met = (not drift and not hits and hand_ok == len(cases)'),
    ("C07", "stop checking the anti-table",
     '        met = (not drift and pins_ok and not hits and hand_ok == len(cases)',
     '        met = (not drift and pins_ok and hand_ok == len(cases)'),
    ("C08", "accept a refusal that writes stdout",
     '        if out.strip():\n            return False, "refusal wrote stdout"',
     '        if False:\n            return False, "refusal wrote stdout"'),
    ("C09", "ignore forgery run errors in admitted",
     '            admitted = (h_ok == len(cases) and g_ok == a.generated and not errs)',
     '            admitted = (h_ok == len(cases) and g_ok == a.generated)'),
    ("C10", "accept any refusal stderr prefix",
     '        if not err.startswith("invalid_input:"):',
     '        if False:'),
]


def run(cmd):
    return subprocess.run(cmd, capture_output=True, text=True, timeout=900)


def build():
    base = open(COUNTER).read()
    os.makedirs(MUT, exist_ok=True)
    revs = {}
    for mid, label, old, new in MUTANTS:
        n = base.count(old)
        if n != 1:
            print("SKIP %s: pattern count %d" % (mid, n))
            continue
        path = os.path.join(MUT, "c91_%s.py" % mid)
        with open(path, "w") as fh:
            fh.write(base.replace(old, new))
        revs[mid] = {"path": path, "label": label}
    json.dump(revs, open(os.path.join(S, "counter-mutants.json"), "w"), indent=1)
    return revs


def score(job):
    mid, cand = job
    path = os.path.join(MUT, "c91_%s.py" % mid)
    work = os.path.join(S, "work2", mid, (cand or "conforming").replace("/", "_"))
    os.makedirs(work, exist_ok=True)
    cmd = ["python3", "-B", path, "--root", FX, "--revision", CONFORMING_REV,
           "--work", work, "--seed", "91091"]
    if cand:
        cmd += ["--candidate", cand]
    p = run(cmd)
    head = p.stdout.splitlines()[0] if p.stdout else ""
    return mid, cand or "(conforming tool)", p.returncode, head


if __name__ == "__main__":
    revs = build()
    jobs = []
    for mid in sorted(revs):
        jobs.append((mid, None))
        for f in FORGERIES:
            jobs.append((mid, f))
    out = {}
    with concurrent.futures.ThreadPoolExecutor(max_workers=6) as ex:
        for mid, cand, rc, head in ex.map(score, jobs):
            print("%s %s exit=%d %s" % (mid, cand, rc, head))
            out.setdefault(mid, {})[cand] = {"exit": rc, "line": head}
    json.dump(out, open(os.path.join(S, "counter-scores.json"), "w"), indent=1, sort_keys=True)
