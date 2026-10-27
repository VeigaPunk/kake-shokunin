#!/usr/bin/env python3
"""Seat MutC2Gate — mutation-test the round-58 C2 gate via single-point mutants of scripts/id_resolver.py.

For each mutant: assert the anchor occurs exactly once, mutate, commit in the seat clone
(selftest identity), run the frozen gate c58_resolver_cases.py --root <clone> --revision <sha>,
record tally + failing cases, restore pristine bytes, verify hash.
"""
import hashlib
import json
import os
import re
import subprocess
import sys

SCRATCH = "/fast/scratch/hyaku/kake-r58/MutC2Gate"
CLONE = os.path.join(SCRATCH, "lane")
GATE = "/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-58/c58_resolver_cases.py"
TOOL_REL = "scripts/id_resolver.py"
TOOL = os.path.join(CLONE, TOOL_REL)
BASE_REV = "044048597d62f3199494b63b36e90dd57825e350"
WORK = os.path.join(SCRATCH, "work")
TMP = os.path.join(SCRATCH, "tmp")
RECEIPTS = os.path.join(SCRATCH, "mutants.jsonl")
PRISTINE_SHA = "25982446d2e647830269cfff0b4bebf7bf263dde57c4321d87eeb42f06461bee"
os.makedirs(WORK, exist_ok=True)
os.makedirs(TMP, exist_ok=True)

pristine = open(TOOL, "rb").read()
assert hashlib.sha256(pristine).hexdigest() == PRISTINE_SHA, "clone tool is not the pristine base bytes"

ENV = dict(os.environ)
ENV["TMPDIR"] = TMP
ENV["LC_ALL"] = "C.UTF-8"
ENV["PYTHONDONTWRITEBYTECODE"] = "1"


def git(*args):
    return subprocess.run(["git", "-C", CLONE, *args], capture_output=True)


top = git("rev-parse", "--show-toplevel").stdout.decode().strip()
assert os.path.realpath(top) == os.path.realpath(CLONE), f"toplevel guard failed: {top}"


def gate(rev):
    p = subprocess.run([sys.executable, "-B", GATE, "--root", CLONE, "--revision", rev, "--work", WORK],
                       capture_output=True, env=ENV, timeout=1200)
    return p.returncode, p.stdout.decode("utf-8", "replace") + p.stderr.decode("utf-8", "replace")


def tally(out):
    m = re.search(r"C2 resolver-cases (\d+)/12 met=(\w+)", out)
    fails = [ln.strip().split()[0] for ln in out.splitlines() if re.match(r"  \S+ FAIL", ln)]
    return {"passed": int(m.group(1)), "met": m.group(2), "fails": fails} if m else {"passed": None, "met": None, "fails": fails}


def commit_tool(label):
    git("add", TOOL_REL)
    c = subprocess.run(["git", "-C", CLONE, "-c", "user.name=selftest", "-c", "user.email=selftest@local",
                        "-c", "commit.gpgsign=false", "commit", "-q", "-m", label], capture_output=True)
    assert c.returncode == 0, c.stderr.decode()
    return git("rev-parse", "HEAD").stdout.decode().strip()


def run_one(label, rev):
    rc, out = gate(rev)
    t = tally(out)
    rec = {"label": label, "rev": rev, "gate_exit": rc, **t}
    with open(RECEIPTS, "a") as fh:
        fh.write(json.dumps({**rec, "stdout": out}) + "\n")
    print(f"{label}: {t['passed']}/12 met={t['met']} fails={','.join(t['fails']) or '-'} (gate exit {rc})", flush=True)
    return rec


# ---- pristine baseline (red control expected: 7/12) -----------------------
results = [run_one("PRISTINE-base", BASE_REV)]

# ---- mutants: (name, old, new) — each old must occur exactly once ---------
MUTANTS = [
    ("M01-id-re-digits-3-to-4",
     r'ID_RE = re.compile(r"(?<![A-Za-z0-9_])S\d{3,}(?![A-Za-z0-9_])")',
     r'ID_RE = re.compile(r"(?<![A-Za-z0-9_])S\d{4,}(?![A-Za-z0-9_])")'),
    ("M02-row-re-indent-0-3-to-0-4",
     r'ROW_RE = re.compile(r"^ {0,3}\|\s*([^|]*?)\s*(?:\|(.*))?$")',
     r'ROW_RE = re.compile(r"^ {0,4}\|\s*([^|]*?)\s*(?:\|(.*))?$")'),
    ("M03-registry-heading-loosened-any-level",
     r'REGISTRY_HEADING_RE = re.compile(r"^##\s+Registry\s*$")',
     r'REGISTRY_HEADING_RE = re.compile(r"^#+\s+Registry\s*$")'),
    ("M04-section-end-never-matches",
     r'SECTION_END_RE = re.compile(r"^#{1,2}\s")',
     r'SECTION_END_RE = re.compile(r"(?!)")'),
    ("M05-sibling-owner-sort-removed",
     "        owners = sorted(name for name, reg in sibling_regs.items() if sid in reg)",
     "        owners = [name for name, reg in sibling_regs.items() if sid in reg]"),
    ("M06-fleet-not-dir-check-removed",
     '    if not os.path.isdir(fleet_root):\n        return _err(f"fleet root {fleet_root} is not a directory")\n',
     ""),
    ("M07-dangling-exit-1-to-0",
     "    return Result(1 if dangling_ids else 0, None, cited, registry, rows, summary)",
     "    return Result(0, None, cited, registry, rows, summary)"),
    ("M08-url-match-removed",
     "        matched = []\n"
     "        for name in owners:\n"
     "            urls = sibling_regs[name].get(sid, ())\n"
     "            if any(url in bodies[path] for path in paths for url in urls):\n"
     "                matched.append(name)\n",
     "        matched = []\n"),
    ("M09-selftest-count-printed-wrong",
     '    print(f"selftest: {passed}/{len(cases)}")',
     '    print(f"selftest: {passed + 1}/{len(cases)}")'),
    ("M10-id-cell-re-digits-3-to-4",
     r'ID_CELL_RE = re.compile(r"^S\d{3,}$")',
     r'ID_CELL_RE = re.compile(r"^S\d{4,}$")'),
    ("M11-url-re-scheme-broken",
     r'URL_RE = re.compile(r"https?://',
     r'URL_RE = re.compile(r"zzttps://'),
    ("M12-citing-path-sort-removed",
     "    return {sid: sorted(paths) for sid, paths in sorted(cited.items())}",
     "    return {sid: list(paths) for sid, paths in sorted(cited.items())}"),
    ("M13-usage-error-64-to-65",
     "        return 0 if exc.code == 0 else 64",
     "        return 0 if exc.code == 0 else 65"),
    ("M14-dangling-id-sort-removed",
     "    dangling_ids = sorted(set(cited) - set(registry))",
     "    dangling_ids = list(set(cited) - set(registry))"),
    ("M15-fleet-default-parent-to-self",
     "    fleet_root = os.path.abspath(fleet) if fleet else os.path.dirname(root)",
     "    fleet_root = os.path.abspath(fleet) if fleet else root"),
    ("M16-sibling-suffix-required-broken",
     '        if not name.endswith("-shokunin"):',
     '        if not name.endswith("-shokuninX"):'),
]

src = pristine.decode("utf-8")
for name, old, new in MUTANTS:
    n = src.count(old)
    assert n == 1, f"{name}: anchor occurs {n} times, refusing"
    mutated = src.replace(old, new, 1).encode("utf-8")
    assert mutated != pristine
    with open(TOOL, "wb") as fh:
        fh.write(mutated)
    msha = hashlib.sha256(mutated).hexdigest()
    rev = commit_tool(name)
    rec = run_one(name, rev)
    results.append({**rec, "mutant_sha256": msha})
    # restore exact pristine bytes and verify
    with open(TOOL, "wb") as fh:
        fh.write(pristine)
    back = hashlib.sha256(open(TOOL, "rb").read()).hexdigest()
    assert back == PRISTINE_SHA, f"{name}: restore mismatch {back}"
    print(f"{name}: restored sha256 ok", flush=True)

# ---- restored-bytes control run -------------------------------------------
results.append(run_one("RESTORED-control", BASE_REV))

summary = [{"label": r["label"], "rev": r["rev"], "gate_exit": r["gate_exit"],
            "passed": r["passed"], "met": r["met"], "fails": r["fails"],
            **({"mutant_sha256": r["mutant_sha256"]} if "mutant_sha256" in r else {})}
           for r in results]
with open(os.path.join(SCRATCH, "summary.json"), "w") as fh:
    json.dump(summary, fh, indent=1)
print("DONE " + json.dumps([r["passed"] for r in results]), flush=True)
