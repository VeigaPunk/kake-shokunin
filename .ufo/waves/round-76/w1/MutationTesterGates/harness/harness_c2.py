#!/usr/bin/env python3
"""Mutation harness for kake r76 C2 (offline hreflang declaration audit).

Target bytes: .ufo/waves/round-76/w1/ExecAuditTool/hreflang_audit.py (snapshot copied to
$S/c2/tool_pristine.py, sha recorded). Detectors:
  SELFTEST  tool --selftest (rc 0, "selftest N/N passed")
  MATRIX    c76_hreflang_matrix.py over the 44 frozen cases (rc 0 = met, 0 wrong)
Each mutant is a single-line substitution; the harness records the wrong cases with
expected/observed exit+ids so the killing case is named, not inferred.
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
C2 = S / "c2"
OUT = S / "out"
TMP = S / "tmp"
CLONE = S / "clone"
LANE = Path("/home/vgpnk/Projects/shokunin/kake-shokunin")
W1 = LANE / ".ufo/waves/round-76/w1"
TOOL = W1 / "ExecAuditTool/hreflang_audit.py"
MATRIX = W1 / "ExecAuditMatrix/c76_hreflang_matrix.py"
CASES = W1 / "ExecAuditMatrix/cases"
CONSTS = W1 / "ExecAuditMatrix/consts"

MUTANTS = [
    ("M1_self_reference_skipped", "skip the self-reference rule",
     '            if not any(normalize_url(alt["href"]) == page["url_norm"] for alt in tagged_abs):',
     '            if False and not any(normalize_url(alt["href"]) == page["url_norm"] for alt in tagged_abs):'),
    ("M2_relative_href_accepted", "accept relative hrefs",
     '            if not absolute_with_host(alt["href"]):',
     '            if False and not absolute_with_host(alt["href"]):'),
    ("M3_xdefault_multiplicity_ignored", "ignore x-default multiplicity",
     '        if len(xdefault) > 1:',
     '        if len(xdefault) > 10 ** 9:'),
    ("M4_external_treated_reciprocal", "treat every external target as reciprocal",
     '                _add(findings, index, "hreflang_external_target", alt["order"],',
     '                (lambda *a, **k: None)(findings, index, "hreflang_external_target", alt["order"],'),
    ("M5_canonical_rule_skipped", "skip the canonical rule",
     '            if normalize_url(canonical["href"]) != page["url_norm"]:',
     '            if False and normalize_url(canonical["href"]) != page["url_norm"]:'),
    ("M6_underscore_tag_accepted", "accept `_` in tags",
     '    lowered = ascii_lower(tag)',
     '    lowered = ascii_lower(tag).replace("_", "-")'),
    ("M7_no_findings", "return no policy findings",
     '        alts = page["alternates"]',
     '        alts = page["alternates"][:0]'),
    ("M8_exit_zero_always", "exit 0 always",
     '        return run_audit(args.manifest, root, args.json)',
     '        return run_audit(args.manifest, root, args.json) and EXIT_CLEAN'),
    ("M9_granularity_collapsed", "collapse findings to one per (page,id) [A2 granulation probe]",
     '    return sorted(findings, key=lambda item: item.get("_key", (10 ** 9, 10 ** 9, 0, "")))',
     '    return sorted(list({(item["id"], item["page"]): item for item in reversed(findings)}.values()), key=lambda item: item.get("_key", (10 ** 9, 10 ** 9, 0, "")))'),
]

BARE_JSON = '''#!/usr/bin/env python3
import json, sys
sys.stdout.write(json.dumps({"findings": [], "exit": 0}) + "\\n")
sys.exit(0)
'''


def sha(p: Path) -> str:
    return hashlib.sha256(p.read_bytes()).hexdigest()


def run(argv, cwd=None):
    env = dict(os.environ)
    env["TMPDIR"] = str(TMP)
    env["PYTHONDONTWRITEBYTECODE"] = "1"
    p = subprocess.run(argv, capture_output=True, text=True, cwd=str(cwd or S), env=env)
    return p.returncode, p.stdout + p.stderr


def tool_selftest(tool: Path, tag: str):
    rc, out = run([sys.executable, "-B", str(tool), "--selftest", "--work", str(TMP / f"tst_{tag}")])
    m = [x for x in out.splitlines() if x.startswith("selftest ")]
    return rc, (m[-1] if m else out.strip().splitlines()[-1:] or ["<empty>"])


def matrix(tool: Path, tag: str, cases=CASES, consts=CONSTS):
    rc, out = run([sys.executable, "-B", str(MATRIX), "--root", str(CLONE),
                   "--revision", "HEAD", "--tool", str(tool),
                   "--cases", str(cases), "--consts", str(consts),
                   "--work", str(TMP / f"mx_{tag}"), "--min-decided", "24"])
    wrong, tally, consts_rows = [], None, []
    for line in out.splitlines():
        if line.startswith("case ") and "verdict=wrong" in line:
            wrong.append(line)
        elif line.startswith("cases=") and "met=" in line:
            tally = line
        elif line.startswith("constant "):
            consts_rows.append(line)
    if tally is None:
        tally = (out.strip().splitlines() or ["<empty>"])[-1]
    return rc, wrong, tally, consts_rows, out


def main() -> int:
    C2.mkdir(parents=True, exist_ok=True)
    OUT.mkdir(parents=True, exist_ok=True)
    pristine = C2 / "tool_pristine.py"
    shutil.copyfile(TOOL, pristine)
    meta = {"tool_source": str(TOOL), "tool_sha256": sha(pristine),
            "tool_bytes": len(pristine.read_bytes()),
            "matrix": str(MATRIX), "matrix_sha256": sha(MATRIX)}
    print(json.dumps(meta), flush=True)

    st_rc, st = tool_selftest(pristine, "pristine")
    m_rc, wrong, tally, consts_rows, raw = matrix(pristine, "pristine")
    baseline = {"selftest_rc": st_rc, "selftest": st, "matrix_rc": m_rc,
                "wrong": wrong, "tally": tally, "constants": consts_rows,
                "raw": raw}
    (OUT / "c2_pristine.json").write_text(json.dumps({**meta, **baseline}, indent=1))
    print("PRISTINE selftest_rc=%s %s | matrix_rc=%s | %s" % (st_rc, st, m_rc, tally), flush=True)
    for row in consts_rows:
        print("  " + row, flush=True)

    results = []
    for mid, desc, old, new in MUTANTS:
        p = C2 / f"{mid}.py"
        src = pristine.read_text()
        if src.count(old) != 1:
            results.append({"id": mid, "desc": desc, "error": "anchor count %d" % src.count(old)})
            continue
        p.write_text(src.replace(old, new))
        st_rc, st = tool_selftest(p, mid)
        m_rc, wrong, tally, _consts, _raw = matrix(p, mid)
        killed = bool(wrong) or m_rc != 0
        row = {"id": mid, "desc": desc, "file": str(p), "old": old, "new": new,
               "sha_pristine": meta["tool_sha256"], "sha_mutant": sha(p),
               "selftest_rc": st_rc, "selftest": st,
               "matrix_rc": m_rc, "wrong": wrong, "tally": tally,
               "killed": killed, "survived": not killed}
        results.append(row)
        (OUT / f"c2_{mid}.json").write_text(json.dumps(row, indent=1))
        first = wrong[0] if wrong else "<none>"
        print("%s killed=%s st=%s(%s) matrix_rc=%s %s | first_wrong=%s"
              % (mid, killed, st_rc, st, m_rc, tally, first), flush=True)

    bare = C2 / "bare_json_probe.py"
    bare.write_text(BARE_JSON)
    m_rc, wrong, tally, _c, _r = matrix(bare, "bare")
    bj = {"path": str(bare), "matrix_rc": m_rc, "wrong": wrong, "tally": tally}
    (OUT / "c2_bare_json.json").write_text(json.dumps(bj, indent=1))
    print("BARE_JSON matrix_rc=%s %s wrong=%d" % (m_rc, tally, len(wrong)), flush=True)

    (OUT / "c2_summary.json").write_text(json.dumps(
        {"meta": meta, "pristine": {k: v for k, v in baseline.items() if k != "raw"},
         "results": results, "bare_json": bj}, indent=1))
    return 0


if __name__ == "__main__":
    sys.exit(main())
