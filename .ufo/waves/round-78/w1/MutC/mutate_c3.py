#!/usr/bin/env python3
"""Mutation harness for scripts/meta_robots_audit.py (C3 tool), round 78.

Detectors per mutant:
  A) the tool's own `--selftest` (83 cases);
  B) the frozen 34-case matrix via c3_probe.py (exit code + finding-id set).
Each mutant is applied to the LIVE working-tree bytes, then restored and
sha256-verified.
"""
import hashlib
import json
import shutil
import subprocess
import sys
from pathlib import Path

S = Path("/fast/scratch/hyaku/kake-r78/MutC")
LANE = Path("/home/vgpnk/Projects/shokunin/kake-shokunin")
SRC = LANE / "scripts/meta_robots_audit.py"
CASES = S / "tool/cases"
RUN = S / "tool"

MUTANTS = [
    dict(id="c01", name="drop the head/body distinction (body tag produces no outside-head finding)",
         edits=[("        if not in_head:\n            findings.append(",
                 "        if False:\n            findings.append(")]),
    dict(id="c02", name="drop the agents filter",
         edits=[("        if ascii_lower(name) not in agents:\n            continue",
                 "        if False:\n            continue")]),
    dict(id="c03", name="none expands to noindex only",
         edits=[('_EXPANSIONS = {"all": ("index", "follow"), "none": ("noindex", "nofollow")}',
                 '_EXPANSIONS = {"all": ("index", "follow"), "none": ("noindex",)}')]),
    dict(id="c04", name="numeric merge takes max instead of min",
         edits=[("            snippet = min(non_negative) if non_negative else -1",
                 "            snippet = max(non_negative) if non_negative else -1"),
                ("            video = min(non_negative) if non_negative else -1",
                 "            video = max(non_negative) if non_negative else -1")]),
    dict(id="c05", name="treat -1 as most restrictive (keep it in the minimum)",
         edits=[("            non_negative = [value for value in self.max_snippet if value >= 0]",
                 "            non_negative = list(self.max_snippet)"),
                ("            non_negative = [value for value in self.max_video if value >= 0]",
                 "            non_negative = list(self.max_video)")]),
    dict(id="c06", name="reject a date-only unavailable_after (pre-amendment behaviour; A2 makes "
                        "the assignment's named mutant -- accepting date-only -- the required rule)",
         edits=[("""    match = _RFC3339_DATE_RE.fullmatch(value)
    if match is not None:
        year, month, day = (int(part) for part in match.groups())
        key = _instant_key(year, month, day, 0, 0, 0, "", 0)
        return None if key is None else (key, value)""",
                 """    match = _RFC3339_DATE_RE.fullmatch(value)
    if match is not None:
        return None""")]),
    dict(id="c07", name="ignore an unknown token silently",
         edits=[("""    if not separator:
        findings.append(
            (FINDING_UNKNOWN_DIRECTIVE, "unknown directive %r" % token)
        )
        return""",
                 """    if not separator:
        return"""),
                ('    findings.append((FINDING_UNKNOWN_DIRECTIVE, "unknown directive %r" % token))',
                 "    return")]),
    dict(id="c08", name="compare declared findings as a sequence, not a sorted set",
         edits=[("""        if sorted(effective) != sorted(declared_effective) or sorted(
            finding_ids
        ) != sorted(declared_findings):""",
                 """        if sorted(effective) != sorted(declared_effective) or list(
            finding_ids
        ) != list(declared_findings):""")]),
    dict(id="c09", name="return exit 0 even when findings were produced",
         edits=[("    elif details:\n        exit_code = EXIT_FINDING",
                 "    elif details:\n        exit_code = EXIT_CLEAN")]),
    dict(id="c10", name="max-image-preview merge order alphabetical",
         edits=[('_MAX_IMAGE_ORDER = {"none": 0, "standard": 1, "large": 2}',
                 '_MAX_IMAGE_ORDER = {"large": 0, "none": 1, "standard": 2}')]),
]


def sha(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def run(cmd, cwd=None):
    return subprocess.run([str(c) for c in cmd], cwd=str(cwd) if cwd else None,
                          capture_output=True, text=True, timeout=1800)


def main() -> int:
    RUN.mkdir(parents=True, exist_ok=True)
    pristine = (RUN / "meta_robots_audit.py").read_bytes()
    psha = sha(pristine)
    results = []

    def selftest():
        w = RUN / "st-work"
        if w.exists():
            shutil.rmtree(w)
        w.mkdir()
        p = run([sys.executable, "-B", RUN / "meta_robots_audit.py",
                 "--selftest", "--work", w])
        summ = [l.strip() for l in p.stdout.splitlines() if l.startswith("selftest")]
        return {"rc": p.returncode, "summary": summ[-1] if summ else p.stdout.strip()[-200:]}

    def matrix(tag):
        out = RUN / f"probe-{tag}.json"
        p = run([sys.executable, "-B", S / "c3_probe.py",
                 "--tool", RUN / "meta_robots_audit.py", "--cases", CASES,
                 "--json", out])
        failed = [l.strip() for l in p.stdout.splitlines() if l.strip().startswith("FAIL")]
        summ = [l.strip() for l in p.stdout.splitlines() if l.startswith("matrix:")]
        return {"rc": p.returncode, "summary": summ[-1] if summ else None,
                "failed_cases": [f.split("FAIL ")[1].split(":")[0] for f in failed if "FAIL " in f]}

    base_st = selftest()
    base_mx = matrix("pristine")
    print(json.dumps({"baseline": {"selftest": base_st, "matrix": base_mx}}))

    for mu in MUTANTS:
        (RUN / "meta_robots_audit.py").write_bytes(pristine)
        text = pristine.decode()
        ok = True
        for old, new in mu["edits"]:
            n = text.count(old)
            if n != 1:
                results.append({"id": mu["id"], "name": mu["name"],
                                "error": f"anchor matched {n}x: {old[:60]!r}",
                                "verdict": "HARNESS-ERROR"})
                ok = False
                break
            text = text.replace(old, new)
        if not ok:
            continue
        (RUN / "meta_robots_audit.py").write_text(text)
        st = selftest()
        mx = matrix(mu["id"])
        mutated_sha = sha((RUN / "meta_robots_audit.py").read_bytes())
        (RUN / "meta_robots_audit.py").write_bytes(pristine)
        restored_st = selftest()
        restored_mx = matrix(mu["id"] + "-restored")
        restored = sha((RUN / "meta_robots_audit.py").read_bytes())
        killed = (st["rc"] != 0) or (mx["rc"] != 0)
        results.append({"id": mu["id"], "name": mu["name"], "selftest": st, "matrix": mx,
                        "verdict": "KILLED" if killed else "SURVIVED",
                        "mutated_sha256": mutated_sha,
                        "restored_selftest": restored_st, "restored_matrix": restored_mx,
                        "restored_sha256": restored, "restored_ok": restored == psha})
        print(json.dumps({k: results[-1][k] for k in ("id", "name", "verdict")}
                         | {"st": results[-1]["selftest"]["summary"],
                            "mx": results[-1]["matrix"]["summary"],
                            "failed": results[-1]["matrix"]["failed_cases"]}))
    (RUN / "meta_robots_audit.py").write_bytes(pristine)
    fin = sha((RUN / "meta_robots_audit.py").read_bytes())
    out = S / "results-c3.json"
    out.write_text(json.dumps({"instrument_sha256": psha, "baseline": {"selftest": base_st,
                                                                      "matrix": base_mx},
                               "final_restored_ok": fin == psha, "mutants": results}, indent=1))
    print(f"wrote {out} final_restored_ok={fin == psha}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
