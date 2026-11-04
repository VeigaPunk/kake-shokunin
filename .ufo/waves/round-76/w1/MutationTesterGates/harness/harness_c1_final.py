#!/usr/bin/env python3
"""C1 mutation harness against the AMENDED contract (amendments 3, 4, 5).

usage: harness_c1_final.py <counter.py> <out-dir>

Detectors (all bounded, all local):
  ST      --selftest must exit 0 (amendment 5 D5: every case must actually run)
  BEFORE  run at a0491fcd, --base a0491fcd: contract D4 expects findings=7, met=false, exit 1
  HEAD    run at b758cb04 (lane tip, no repair rows yet): must stay red (D4)
  P_ARTIFACT  absent span only inside w1-results.json (dispatcher artifact) -> must stay red
  P_CASE      absent span differs from the receipt token only by case      -> must stay red
  P_SEATREE   absent span only inside round-75/w1/<seat>/receipts/*.txt    -> D1: never a receipt
  P_DIAG      absent span only on a line `  T1 SCORECARD.md:1 <span>`      -> D2: stripped
  P_DATAEXT   absent span only in round-74/notes.txt (outside a receipt dir) -> D1: not a receipt
"""
import hashlib
import json
import os
import shutil
import subprocess
import sys
from pathlib import Path

S = Path("/fast/scratch/hyaku/kake-r76/MutationTesterGates")
TMP = S / "tmp"
CLONE = S / "clone"
BASE = "a0491fcd041cbc3fff2c964ecf6268557e45a5c1"
HEAD = "b758cb040d53374b1b63b89702c7128f77212d23"

MUTANTS = [
    ("M1_append_only_conjunct_dropped", "drop the append-only conjunct",
     [('        "met": len(findings) == 0 and append_only,',
       '        "met": len(findings) == 0,')]),
    ("M2_met_ignores_findings", "make met ignore findings",
     [('        "met": len(findings) == 0 and append_only,',
       '        "met": append_only,')]),
    ("M3_every_span_contiguous", "treat every span as contiguous",
     [('    frags = [f for f in ELIDE_RE.split(span) if f.strip()] if ELIDE_RE.search(span) else [span]',
       '    frags = [span]')]),
    ("M4_spans_case_insensitive", "match spans case-insensitively",
     [('    return any(all(f in body for f in frags) for _, body in receipts)',
       '    return any(all(f.lower() in body.lower() for f in frags) for _, body in receipts)')]),
    ("M5_results_is_receipt", "accept *-results.json as a receipt",
     [('    if any(fnmatch.fnmatchcase(base, g) for g in ARTIFACT_GLOBS):',
       '    if False and any(fnmatch.fnmatchcase(base, g) for g in ARTIFACT_GLOBS):'),
      ('DISPATCH_ARTIFACTS = ("-results.json", "-dispatch.json", "-spec.json", "swarm-registry.json")',
       'DISPATCH_ARTIFACTS = ("-dispatch.json", "-spec.json", "swarm-registry.json")')]),
    ("M6_elision_one_fragment", "elision rule requires only ONE fragment",
     [('    return any(all(f in body for f in frags) for _, body in receipts)',
       '    return any(any(f in body for f in frags) for _, body in receipts)')]),
    ("M7_t4_check_skipped", "skip the T4 correction check",
     [('            findings.append({"id": "T4", "file": c["file"], "line": c["line"],',
       '            (lambda *a, **k: None)({"id": "T4", "file": c["file"], "line": c["line"],')]),
    ("M8_presence_exempts", "correction row's mere presence exempts a span",
     [('            if span in defects and any(span in c["spans"] for c in validated):',
       '            if validated:'),
      ('            if any(span in c["text"] for c, _ in validated):',
       '            if correction_lines(rows):')]),
    ("M9_exit_zero", "exit 0 unconditionally",
     [('    return 0 if res["met"] else 1',
       '    return 0')]),
]

PROBES = [
    ("P_ARTIFACT", ".ufo/waves/round-76/w1/w1-results.json", "zz=9 xy=1\n"),
    ("P_CASE", ".ufo/waves/round-75/controls/ctl.txt", "met=true\n"),
    ("P_SEATREE", ".ufo/waves/round-75/w1/SomeSeat/receipts/notes.txt", "zz=9 xy=1\n"),
    ("P_DIAG", ".ufo/waves/round-74/controls/diag.txt", "  T1 SCORECARD.md:1 zz=9 xy=1\n"),
    ("P_DATAEXT", ".ufo/waves/round-74/notes.txt", "zz=9 xy=1\n"),
]


def sha(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def run(argv):
    env = dict(os.environ)
    env["TMPDIR"] = str(TMP)
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    p = subprocess.run(argv, capture_output=True, text=True, cwd=str(S), env=env)
    return p.returncode, p.stdout + p.stderr


def summary(o: str) -> str:
    ls = [x for x in o.splitlines() if x.startswith(("C1v1 ", "C1v2 ", "C1v3 "))]
    if ls:
        return ls[0]
    tail = [x for x in o.splitlines() if x.strip()]
    return tail[-1] if tail else "<empty>"


def build_probe(name: str, card: str, rel: str, body: str) -> Path:
    root = TMP / f"probe_{name}"
    if root.exists():
        shutil.rmtree(root)
    (root / "corpus").mkdir(parents=True)
    (root / "SCORECARD.md").write_text("## Round 75 - probe\n\n| Subject | Claim |\n|---|---|\n" + card + "\n")
    (root / "corpus/QUALITY.md").write_text("## Round-75 criterion - probe\n\n- prose\n")
    path = root / rel
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(body)
    subprocess.run(["git", "-C", str(root), "init", "-q"], check=True)
    subprocess.run(["git", "-C", str(root), "add", "-A"], check=True)
    subprocess.run(["git", "-C", str(root), "-c", "user.name=t", "-c", "user.email=t@t",
                    "commit", "-qm", "probe"], check=True)
    return root


def detect(tool: Path, tag: str) -> dict:
    st_rc, st_out = run([sys.executable, "-B", str(tool), "--selftest", "--work", str(TMP / f"st_{tag}")])
    before_rc, before_out = run([sys.executable, "-B", str(tool), "--root", str(CLONE),
                                 "--revision", BASE, "--base", BASE, "--rounds", "75,76"])
    head_rc, head_out = run([sys.executable, "-B", str(tool), "--root", str(CLONE),
                             "--revision", HEAD, "--base", BASE, "--rounds", "75,76"])
    probes = {}
    for name, rel, body in PROBES:
        card = "| S | `zz=9 xy=1` |" if name != "P_CASE" else "| S | `MET=TRUE` |"
        root = build_probe(name, card, rel, body)
        rc, out = run([sys.executable, "-B", str(tool), "--root", str(root), "--revision", "HEAD",
                       "--base", "HEAD", "--rounds", "75"])
        probes[name] = {"rc": rc, "line": summary(out)}
    st_tail = [x for x in st_out.splitlines() if x.startswith("selftest:")]
    return {
        "selftest_rc": st_rc,
        "selftest": st_tail[-1] if st_tail else summary(st_out),
        "before_rc": before_rc, "before": summary(before_out),
        "head_rc": head_rc, "head": summary(head_out),
        "probes": probes,
        "raw": {"selftest": st_out, "before": before_out, "head": head_out},
    }


def finding_count(line: str) -> str:
    if "findings=" not in line:
        return "?"
    return line.split("findings=")[1].split()[0]


def deviation(d: dict, b: dict) -> list[str]:
    why = []
    if d["selftest_rc"] != b["selftest_rc"]:
        why.append("selftest rc %s != %s" % (d["selftest_rc"], b["selftest_rc"]))
    if (d["before_rc"], finding_count(d["before"])) != (b["before_rc"], finding_count(b["before"])):
        why.append("before %s/%s != %s/%s" % (d["before_rc"], finding_count(d["before"]),
                                              b["before_rc"], finding_count(b["before"])))
    if (d["head_rc"], finding_count(d["head"])) != (b["head_rc"], finding_count(b["head"])):
        why.append("head %s/%s != %s/%s" % (d["head_rc"], finding_count(d["head"]),
                                            b["head_rc"], finding_count(b["head"])))
    for name, _rel, _body in PROBES:
        if d["probes"][name]["rc"] != b["probes"][name]["rc"]:
            why.append("%s rc %s != %s" % (name, d["probes"][name]["rc"], b["probes"][name]["rc"]))
    return why


def contract_check(b: dict) -> list[str]:
    notes = []
    if finding_count(b["before"]) != "7" or b["before_rc"] != 1:
        notes.append("BASELINE OFF CONTRACT: before=%s rc=%s (D4 says findings=7 exit 1)"
                     % (b["before"], b["before_rc"]))
    if finding_count(b["head"]) != "7":
        notes.append("HEAD not red without repair: %s rc=%s" % (b["head"], b["head_rc"]))
    if b["selftest_rc"] != 0:
        notes.append("SELFTEST RED: %s" % b["selftest"])
    for name, _rel, _body in PROBES:
        if b["probes"][name]["rc"] == 0:
            notes.append("%s green on pristine (amended clause not enforced): %s"
                         % (name, b["probes"][name]["line"]))
    return notes


def main() -> int:
    target = Path(sys.argv[1])
    out = Path(sys.argv[2])
    out.mkdir(parents=True, exist_ok=True)
    work = out / "mutants"
    work.mkdir(exist_ok=True)
    pristine = work / "m00_pristine.py"
    shutil.copyfile(target, pristine)
    meta = {"target": str(target), "sha256": sha(pristine), "bytes": len(pristine.read_bytes())}
    print(json.dumps(meta), flush=True)

    base = detect(pristine, "pristine")
    notes = contract_check(base)
    (out / "m00_pristine.json").write_text(json.dumps({"meta": meta, **base, "contract_notes": notes}, indent=1))
    print("BASELINE st_rc=%s %s | before=%s rc=%s | head=%s rc=%s"
          % (base["selftest_rc"], base["selftest"], base["before"], base["before_rc"],
             base["head"], base["head_rc"]), flush=True)
    for name, _rel, _body in PROBES:
        print("  %-11s rc=%s %s" % (name, base["probes"][name]["rc"], base["probes"][name]["line"]), flush=True)
    for note in notes:
        print("  NOTE " + note, flush=True)

    results = []
    for mid, desc, pairs in MUTANTS:
        src = pristine.read_text()
        chosen, missing = None, []
        for old, new in pairs:
            if src.count(old) == 1:
                chosen = (old, new)
                break
            missing.append("%s (%dx)" % (old.strip()[:60], src.count(old)))
        if chosen is None:
            results.append({"id": mid, "desc": desc, "error": "no anchor: " + "; ".join(missing)})
            print("%s: ANCHOR MISS %s" % (mid, missing), flush=True)
            continue
        p = work / f"{mid}.py"
        p.write_text(src.replace(*chosen))
        d = detect(p, mid)
        why = deviation(d, base)
        row = {"id": mid, "desc": desc, "file": p.name, "old": chosen[0], "new": chosen[1],
               "sha_pristine": meta["sha256"], "sha_mutant": sha(p),
               "verdict": d, "killed": bool(why), "why": why, "survived": not why}
        results.append(row)
        (out / f"{mid}.json").write_text(json.dumps(row, indent=1))
        print("%s killed=%s why=%s st=%s before=%s head=%s"
              % (mid, bool(why), why, d["selftest"], d["before"], d["head"]), flush=True)
    (out / "summary.json").write_text(json.dumps(
        {"meta": meta, "contract_notes": notes,
         "baseline": {k: v for k, v in base.items() if k != "raw"}, "results": results}, indent=1))
    return 0


if __name__ == "__main__":
    sys.exit(main())
