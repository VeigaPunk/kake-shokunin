#!/usr/bin/env python3
"""Mutation harness for c78_sweep_truth.py (C2 counter).

Two detectors per mutant:
  A) the instrument's own `--selftest` (declared 6/6);
  B) a LIVE probe: fixture git repos whose `scripts/freshness-sweep.mjs` emits
     controlled JSON per mode, driving `measure()` end-to-end (base sweep +
     negative control). Modes and pristine expectations are declared below; a
     mode whose pristine run does not match its expectation is INCONCLUSIVE and
     cannot kill a mutant.
"""
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path

S = Path("/fast/scratch/hyaku/kake-r78/MutC")
BASE = S / "base"
TREE = S / "tree"
PROBES = S / "probes"
REL = ".ufo/waves/round-78/c78_sweep_truth.py"

SWEEP_JS = r"""
import { existsSync, readFileSync } from 'node:fs';
const root = new URL('../', import.meta.url);
const mode = readFileSync(new URL('.probe/mode', root), 'utf8').trim();
const planted = existsSync(new URL('corpus/lessons/ctl-r78-unannotated-miss.md', root));
const clean = { code: 0, ok: true, skipped: ['§armed (all remote checks)'], reasons: [],
  sections: { paths: { ok: true, counts: { drift: 0, newMissing: 0 } } } };
const red = { code: 1, ok: false, skipped: ['§armed (all remote checks)'], reasons: ['§paths: 1 unannotated miss'],
  sections: { paths: { ok: false, counts: { drift: 1, newMissing: 1 } } } };
function emit(o) { process.stdout.write(JSON.stringify(o) + '\n'); process.exit(o.code); }
if (!planted) {
  if (mode === 'B') emit({ code: 0, ok: true, skipped: [], reasons: [],
    sections: { paths: { ok: true, counts: { drift: 0, newMissing: 1 } } } });
  if (mode === 'E') emit({ code: 64, ok: false, skipped: [], reasons: ['usage'],
    sections: { paths: { ok: true, counts: { drift: 0, newMissing: 0 } } } });
  if (mode === 'F') emit({ code: 0, ok: true, skipped: [], reasons: [],
    sections: { paths: { ok: false, counts: { drift: 0, newMissing: 0 } } } });
  emit(clean);
} else {
  if (mode === 'C') emit({ code: 1, ok: false, skipped: [], reasons: ['§paths: only new miss'],
    sections: { paths: { ok: false, counts: { drift: 0, newMissing: 1 } } } });
  if (mode === 'D') emit(clean);
  if (mode === 'G') emit({ code: 2, ok: false, skipped: [], reasons: ['unevaluable'],
    sections: { paths: { ok: false, counts: { drift: 0, newMissing: 0 } } } });
  if (mode === 'H') emit({ code: 2, ok: false, skipped: [], reasons: ['fault after a partial scan'],
    sections: { paths: { ok: false, counts: { drift: 1, newMissing: 1 } } } });
  emit(red);
}
"""

MODES = {
    # mode: expected (met, rc) from the contract predicate
    "A": (True, 0),   # clean base, red control
    "B": (False, 1),  # base exits 0 with counts.newMissing=1 and paths.ok=true
    "C": (False, 1),  # control exits 1 but reports drift=0
    "D": (False, 1),  # control comes back GREEN (gate loosened)
    "E": (False, 1),  # base sweep exits 64 with clean JSON
    "G": (False, 1),  # control exits 2 (unevaluable), drift=0 -- not a red gate proof
    "F": (False, 1),  # base exit 0 with paths.ok=false -- unreachable from the production sweep
    "H": (False, 1),  # control exits 2 (fault) but reports drift=1 -- red for the wrong reason
}

MUTANTS = [
    dict(id="m01", name="skip the negative control (assume a red control)",
         old="    ctl = negative_control(root, rev, work, timeout)",
         new="    ctl = {\"sweep_exit\": 1, \"drift\": 1, \"new_missing\": 1, \"tree_identity\": \"deadbeef\"}"),
    dict(id="m02", name="accept control_drift == 0",
         old='(ctl["drift"] or 0) >= 1',
         new='(ctl["drift"] or 0) >= 0'),
    dict(id="m03", name="ignore newMissing in the met predicate",
         old='''    met = (base["sweep_exit"] == 0 and base["drift"] == 0 and base["new_missing"] == 0
           and base["paths_ok"]''',
         new='''    met = (base["sweep_exit"] == 0 and base["drift"] == 0
           and base["paths_ok"]'''),
    dict(id="m04", name="treat any non-zero control exit as proof of a red gate",
         old='ctl["sweep_exit"] == 1 and (ctl["drift"] or 0) >= 1',
         new='ctl["sweep_exit"] != 0 and (ctl["drift"] or 0) >= 1'),
    dict(id="m05", name="treat base exit 64 as met",
         old='''base["sweep_exit"] == 0 and base["drift"] == 0 and base["new_missing"] == 0''',
         new='''base["sweep_exit"] in (0, 64) and base["drift"] == 0 and base["new_missing"] == 0'''),
    dict(id="m06", name="ignore paths_ok",
         old='''           and base["paths_ok"] and ctl["sweep_exit"] == 1''',
         new='''           and True and ctl["sweep_exit"] == 1'''),
    dict(id="m07", name="drop the tree_identity divergence conjunct",
         old='''           and base["tree_identity"] != ctl["tree_identity"])''',
         new='''           and True)'''),
]


def sha(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def run(cmd, cwd=None):
    return subprocess.run([str(c) for c in cmd], cwd=str(cwd) if cwd else None,
                          capture_output=True, text=True, timeout=600)


def build_probe(mode: str) -> Path:
    d = PROBES / mode
    if d.exists():
        shutil.rmtree(d)
    (d / "scripts").mkdir(parents=True)
    (d / "corpus/lessons").mkdir(parents=True)
    (d / ".probe").mkdir(parents=True)
    (d / "scripts/freshness-sweep.mjs").write_text(SWEEP_JS)
    (d / "corpus/lessons/.keep").write_text("")
    (d / ".probe/mode").write_text(mode + "\n")
    env = dict(os.environ, GIT_AUTHOR_NAME="mut", GIT_AUTHOR_EMAIL="mut@example.invalid",
               GIT_COMMITTER_NAME="mut", GIT_COMMITTER_EMAIL="mut@example.invalid")
    r = run(["git", "init", "-q"], cwd=d)
    if r.returncode != 0:
        raise SystemExit(f"git init failed: {r.stderr}")
    top = run(["git", "rev-parse", "--show-toplevel"], cwd=d).stdout.strip()
    if Path(top).resolve() != d.resolve():
        raise SystemExit(f"fixture toplevel mismatch: {top} != {d}")
    run(["git", "add", "-A"], cwd=d)
    r = run(["git", "commit", "-qm", "probe"], cwd=d) if False else subprocess.run(
        ["git", "commit", "-qm", "probe"], cwd=str(d), capture_output=True, text=True, env=env)
    if r.returncode != 0:
        raise SystemExit(f"git commit failed: {r.stderr}")
    return d


def probe_run(counter: Path, mode: str, tag: str):
    work = PROBES / f"work-{mode}-{tag}"
    if work.exists():
        shutil.rmtree(work)
    work.mkdir(parents=True)
    d = PROBES / mode
    p = run([sys.executable, "-B", counter, "--root", d, "--revision", "HEAD", "--work", work])
    m = re.search(r"met=(true|false)", p.stdout)
    return {"rc": p.returncode, "met": m.group(1) if m else None,
            "line": p.stdout.strip().splitlines()[0] if p.stdout.strip() else p.stderr.strip()[-300:]}


LANE = Path("/home/vgpnk/Projects/shokunin/kake-shokunin") / REL


def main() -> int:
    PROBES.mkdir(parents=True, exist_ok=True)
    pristine = (BASE / REL).read_bytes()
    pristine_sha = sha(pristine)

    # pristine live-probe baseline
    base_counter = PROBES / "pristine_counter.py"
    base_counter.write_bytes(pristine)
    pristine_probe = {}
    for mode in MODES:
        build_probe(mode)
        pristine_probe[mode] = probe_run(base_counter, mode, "pristine")
    exp = {m: {"met": "true" if MODES[m][0] else "false", "rc": MODES[m][1]} for m in MODES}
    conclusive = {m: (pristine_probe[m]["met"] == exp[m]["met"]
                      and pristine_probe[m]["rc"] == exp[m]["rc"]) for m in MODES}

    # pristine selftest
    st = run([sys.executable, "-B", str(base_counter), "--selftest"])
    pristine_selftest = {"rc": st.returncode,
                         "summary": [l for l in st.stdout.splitlines() if l.startswith("selftest:")]}

    results = []
    for mu in MUTANTS:
        if TREE.exists():
            shutil.rmtree(TREE)
        shutil.copytree(BASE, TREE)
        tgt = TREE / REL
        txt = tgt.read_text()
        n = txt.count(mu["old"])
        if n != 1:
            results.append({"id": mu["id"], "name": mu["name"], "error": f"anchor matched {n}x",
                            "verdict": "HARNESS-ERROR"})
            continue
        tgt.write_text(txt.replace(mu["old"], mu["new"]))
        mut_counter = PROBES / f"mut-{mu['id']}.py"
        mut_counter.write_text(tgt.read_text())
        st = run([sys.executable, "-B", str(mut_counter), "--selftest"])
        selftest_fails = [l.strip() for l in st.stdout.splitlines() if l.strip().startswith("FAIL")]
        selftest_verdict = "KILLED" if st.returncode != 0 else "SURVIVED"
        live = {}
        kills = []
        for mode in MODES:
            r = probe_run(mut_counter, mode, mu["id"])
            live[mode] = r
            if conclusive[mode] and (r["met"] != exp[mode]["met"] or r["rc"] != exp[mode]["rc"]):
                kills.append(mode)
        verdict = ("KILLED by live mode " + ",".join(kills)) if kills else "SURVIVED"
        mutated_sha = sha(mut_counter.read_bytes())
        tgt.write_bytes(pristine)
        mut_counter.write_bytes(pristine)
        restored_st = run([sys.executable, "-B", str(mut_counter), "--selftest"])
        restored_live = {mode: probe_run(mut_counter, mode, mu["id"] + "-restored") for mode in MODES}
        restored = sha(tgt.read_bytes())
        results.append({"id": mu["id"], "name": mu["name"],
                        "selftest": {"rc": st.returncode,
                                     "summary": [l for l in st.stdout.splitlines() if l.startswith("selftest:")],
                                     "fails": selftest_fails, "verdict": selftest_verdict},
                        "live": live, "killing_modes": kills, "verdict": verdict,
                        "restored_selftest_rc": restored_st.returncode, "restored_live": restored_live,
                        "mutated_sha256": mutated_sha,
                        "restored_sha256": restored, "restored_ok": restored == pristine_sha})
        print(json.dumps({k: results[-1][k] for k in ("id", "name", "verdict", "killing_modes")}
                         | {"selftest": results[-1]["selftest"]["summary"]}))
    out = S / "results-c2.json"
    out.write_text(json.dumps({
        "pristine_sha256": pristine_sha, "pristine_selftest": pristine_selftest,
        "modes_expected": {m: exp[m] for m in MODES},
        "pristine_probe": pristine_probe, "conclusive": conclusive,
        "mutants": results}, indent=1))
    print(f"wrote {out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
