#!/usr/bin/env python3
"""Mutation harness for kake r76 C1 counter (kake-shokunin/.ufo/waves/round-76/c76_quote_truth.py).

One-line mutations, each applied to a fresh copy of the pristine bytes.
Detectors, all bounded and local:
  ST      the counter's own --selftest (rc 0 required green)
  BEFORE  run at the frozen before revision a0491fcd (expected findings=8 met=false rc=1)
  HEAD    run at lane tip b758cb04 with --base a0491fcd (pristine shape: findings=0 met=true rc=0)
  PROBE_RESULTS  fixture: absent span lives ONLY in .ufo/waves/round-76/w1/w1-results.json
                 (pristine T1 red; a counter that accepts dispatcher artifacts goes green)
  PROBE_CASE     fixture: absent span is `MET=TRUE`, receipt has `met=true`
                 (pristine T1 red; a case-insensitive matcher goes green)
"""
import hashlib
import json
import os
import re
import shutil
import subprocess
import sys
from pathlib import Path

S = Path("/fast/scratch/hyaku/kake-r76/MutationTesterGates")
C1 = S / "c1"
OUT = S / "out"
CLONE = S / "clone"
TMP = S / "tmp"
BASE = "a0491fcd041cbc3fff2c964ecf6268557e45a5c1"
HEAD = "b758cb040d53374b1b63b89702c7128f77212d23"
PRISTINE = C1 / "m00_pristine.py"
TARGET = Path(sys.argv[1]) if len(sys.argv) > 1 else None
FILTER = sys.argv[2] if len(sys.argv) > 2 else None

ALT_ANCHORS = {
    "M5_w1_results_is_receipt": [
        ('    if any(fnmatch.fnmatchcase(base, g) for g in ARTIFACT_GLOBS):',
         '    if False and any(fnmatch.fnmatchcase(base, g) for g in ARTIFACT_GLOBS):'),
    ],
}

MUTANTS = [
    ("M1_append_only_conjunct_dropped", "drop the append-only conjunct",
     '        "met": len(findings) == 0 and append_only,',
     '        "met": len(findings) == 0,'),
    ("M2_met_ignores_findings", "make met ignore findings",
     '        "met": len(findings) == 0 and append_only,',
     '        "met": append_only,'),
    ("M3_every_span_contiguous", "treat every span as contiguous (elision split bypassed)",
     '    frags = [f for f in ELIDE_RE.split(span) if f.strip()] if ELIDE_RE.search(span) else [span]',
     '    frags = [span]'),
    ("M4_spans_case_insensitive", "match spans case-insensitively",
     '    return any(all(f in body for f in frags) for _, body in receipts)',
     '    return any(all(f.lower() in body.lower() for f in frags) for _, body in receipts)'),
    ("M5_w1_results_is_receipt", "accept w1-results.json as a receipt",
     'DISPATCH_ARTIFACTS = ("-results.json", "-dispatch.json", "-spec.json", "swarm-registry.json")',
     'DISPATCH_ARTIFACTS = ("-dispatch.json", "-spec.json", "swarm-registry.json")'),
    ("M6_elision_one_fragment", "elision rule requires only ONE fragment",
     '    return any(all(f in body for f in frags) for _, body in receipts)',
     '    return any(any(f in body for f in frags) for _, body in receipts)'),
    ("M7_t4_check_skipped", "skip the T4 correction check",
     '            findings.append({"id": "T4", "file": c["file"], "line": c["line"],',
     '            (lambda *a, **k: None)({"id": "T4", "file": c["file"], "line": c["line"],'),
    ("M8_presence_exempts", "treat a correction row's mere presence as exemption",
     '            if any(span in c["text"] for c, _ in validated):',
     '            if corr:'),
    ("M8b_presence_exempts_faithful", "correction row's mere presence exempts (defined-name form)",
     '            if any(span in c["text"] for c, _ in validated):',
     '            if correction_lines(rows):'),
    ("M9_exit_zero", "exit 0 unconditionally",
     '    return 0 if res["met"] else 1',
     '    return 0'),
]


def sha(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def run(argv, cwd=None, env_extra=None):
    env = dict(os.environ)
    env["TMPDIR"] = str(TMP)
    if env_extra:
        env.update(env_extra)
    p = subprocess.run(argv, capture_output=True, text=True, cwd=str(cwd or S), env=env)
    return p.returncode, p.stdout + p.stderr


def build_probe(name: str, card: str, receipt_rel: str, receipt_body: str) -> Path:
    root = TMP / f"probe_{name}"
    if root.exists():
        shutil.rmtree(root)
    (root / ".ufo/waves/round-75/controls").mkdir(parents=True)
    (root / "corpus").mkdir(parents=True)
    (root / "SCORECARD.md").write_text("## Round 75 - probe\n\n| Subject | Claim |\n|---|---|\n" + card + "\n")
    (root / "corpus/QUALITY.md").write_text("## Round-75 criterion - probe\n\n- prose\n")
    rel = root / receipt_rel
    rel.parent.mkdir(parents=True, exist_ok=True)
    rel.write_text(receipt_body)
    for cmd in (["init", "-q"], ["add", "-A"]):
        subprocess.run(["git", "-C", str(root), *cmd], check=True)
    subprocess.run(["git", "-C", str(root), "-c", "user.name=t", "-c", "user.email=t@t",
                    "commit", "-qm", "probe"], check=True)
    return root


def probe_results(path: Path) -> tuple[int, str]:
    root = build_probe("results", "| S | `zz=9 xy=1` |",
                       ".ufo/waves/round-76/w1/w1-results.json", "zz=9 xy=1\n")
    rc, out = run([sys.executable, "-B", str(path), "--root", str(root), "--revision", "HEAD",
                   "--base", "HEAD", "--rounds", "75"])
    return rc, out


def probe_case(path: Path) -> tuple[int, str]:
    root = build_probe("case", "| S | `MET=TRUE` |",
                       ".ufo/waves/round-75/controls/ctl.txt", "met=true\n")
    rc, out = run([sys.executable, "-B", str(path), "--root", str(root), "--revision", "HEAD",
                   "--base", "HEAD", "--rounds", "75"])
    return rc, out


def detect(path: Path, tag: str) -> dict:
    st_rc, st_out = run([sys.executable, "-B", str(path), "--selftest", "--work", str(TMP / f"st_{tag}")])
    before_rc, before_out = run([sys.executable, "-B", str(path), "--root", str(CLONE),
                                 "--revision", BASE, "--base", BASE, "--rounds", "75,76"])
    head_rc, head_out = run([sys.executable, "-B", str(path), "--root", str(CLONE),
                             "--revision", HEAD, "--base", BASE, "--rounds", "75,76"])
    pres_rc, pres_out = probe_results(path)
    pcase_rc, pcase_out = probe_case(path)

    def line(o: str) -> str:
        ls = [x for x in o.splitlines() if x.startswith(("C1v1 ", "C1v2 "))]
        return ls[0] if ls else o.splitlines()[-1] if o.splitlines() else "<empty>"

    st_tail = [x for x in st_out.splitlines() if x.startswith("selftest:")]
    return {
        "selftest_rc": st_rc,
        "selftest": st_tail[-1] if st_tail else line(st_out),
        "before_rc": before_rc, "before": line(before_out),
        "head_rc": head_rc, "head": line(head_out),
        "probe_results_rc": pres_rc, "probe_results": line(pres_out),
        "probe_case_rc": pcase_rc, "probe_case": line(pcase_out),
        "raw": {"before": before_out, "head": head_out,
                "probe_results": pres_out, "probe_case": pcase_out, "selftest": st_out},
    }


def is_killed(d: dict, baseline: dict) -> tuple[bool, list[str]]:
    """A mutant is killed when any detector leaves the pristine shape."""
    why = []
    if d["selftest_rc"] != baseline["selftest_rc"]:
        why.append("selftest red")
    if (d["before_rc"], d["before"].split("findings=")[-1].split()[0]) != \
       (baseline["before_rc"], baseline["before"].split("findings=")[-1].split()[0]):
        why.append("before-state changed")
    if (d["head_rc"], d["head"].split("findings=")[-1].split()[0]) != \
       (baseline["head_rc"], baseline["head"].split("findings=")[-1].split()[0]):
        why.append("head-state changed")
    if d["probe_results_rc"] != baseline["probe_results_rc"]:
        why.append("PROBE_RESULTS green")
    if d["probe_case_rc"] != baseline["probe_case_rc"]:
        why.append("PROBE_CASE green")
    return bool(why), why


def main() -> int:
    global PRISTINE, OUT, C1
    if TARGET is not None:
        C1 = S / "c1b"
        OUT = S / "out_c1b"
        PRISTINE = C1 / "m00_pristine.py"
        C1.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(TARGET, PRISTINE)
    OUT.mkdir(parents=True, exist_ok=True)
    base = detect(PRISTINE, "pristine")
    (OUT / "m00_pristine.json").write_text(json.dumps(base, indent=1))
    results = []
    for mid, desc, old, new in MUTANTS:
        if FILTER and FILTER not in mid:
            continue
        p = C1 / f"{mid}.py"
        src = PRISTINE.read_text()
        n = src.count(old)
        if n != 1:
            for alt_old, alt_new in ALT_ANCHORS.get(mid, []):
                if src.count(alt_old) == 1:
                    old, new, n = alt_old, alt_new, 1
                    break
        if n != 1:
            results.append({"id": mid, "desc": desc, "error": f"anchor occurs {n}x"})
            continue
        p.write_text(src.replace(old, new))
        d = detect(p, mid)
        killed, why = is_killed(d, base)
        results.append({
            "id": mid, "desc": desc, "file": str(p),
            "sha_before": sha(PRISTINE), "sha_mutant": sha(p),
            "old": old, "new": new, "verdict": d, "killed": killed, "why": why,
            "survived": not killed,
        })
        (OUT / f"{mid}.json").write_text(json.dumps(results[-1], indent=1))
        print(f"{mid}: killed={killed} why={why} st={d['selftest']} before_rc={d['before_rc']} "
              f"head_rc={d['head_rc']} pres_rc={d['probe_results_rc']} pcase_rc={d['probe_case_rc']}",
              flush=True)
    (OUT / "c1_summary.json").write_text(json.dumps({"baseline": base, "results": results}, indent=1))
    return 0


if __name__ == "__main__":
    sys.exit(main())
