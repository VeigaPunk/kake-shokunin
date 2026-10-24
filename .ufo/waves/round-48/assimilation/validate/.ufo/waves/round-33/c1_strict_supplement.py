#!/usr/bin/env python3
"""Round-33 C1 strict supplement (not the declared counter; added after wave-1
seat CriticC1RepairScope showed the frozen counter c1_code_probe.py scores 4
for a commit that only moves the code into the message text).

Usage: python3 -B c1_strict_supplement.py --rev <lane revision> [--repo <lane repo>]

Checks over the revision's exported bytes:
  s1 spec      P6 hostile.json case h6 has reason_code "setup_commit_before_init"
               and no reason_contains key.
  s2 field     a pristine hostile run reports, for h6, code
               "setup_commit_before_init" in the runner's failure entry, and
               the reported reason text does not contain that code string.
  s3 message   a runner whose guard raise line has its whole message argument
               replaced by the literal "refused" still passes the hostile
               selftest (exit 0, every spec passed).
  s4 layer     with the load-time guard deleted (m3), the h6 failure entry
               carries code "setup_commit_without_repo" (the apply-time
               re-check names itself) and P6 fails.
``met`` counts checks passed (0..4).  Exit 0 when it ran, 2 when the revision
cannot be exported or the guard line cannot be located.
"""
from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
import tarfile
import tempfile
from pathlib import Path

RUNNER = "scripts/citing_set_selftest.py"
HOSTILE = "scripts/citing_set_hostile_selftest.py"
P6_SPEC = "scripts/fixtures/citing-set-hostile/P6-commit-before-init/hostile.json"
GUARD = re.compile(
    r'^( *)if step\["op"\] == "git_commit" and not initialized:\n\1    raise \w+\([^\n]*\n', re.M
)
CODE = "setup_commit_before_init"
L2_CODE = "setup_commit_without_repo"
# message argument: the last argument of the raise call, a "%s ..." % CASE_SETUP_FILE expression
MESSAGE_ARG = re.compile(r'"[^"\n]*needs an earlier \'git_init\'[^"\n]*"(?: % CASE_SETUP_FILE)?')


def run(cmd):
    try:
        done = subprocess.run(cmd, capture_output=True, text=True, timeout=900)
    except subprocess.TimeoutExpired:
        return None, None
    try:
        return done.returncode, json.loads(done.stdout)
    except ValueError:
        return done.returncode, None


def p6_detail(summary):
    for case in (summary or {}).get("cases", []):
        if isinstance(case, dict) and case.get("case") == "P6-commit-before-init":
            return case
    return None


def main(argv=None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--rev", required=True)
    ap.add_argument("--repo", default="/home/vgpnk/Projects/shokunin/kake-shokunin")
    args = ap.parse_args(argv)
    out = {"schema": "kake-r33-c1-strict-v1", "rev": None, "checks": {}, "detail": {}}
    full = subprocess.run(["git", "-C", args.repo, "rev-parse", "--verify", args.rev + "^{commit}"],
                          capture_output=True, text=True)
    if full.returncode != 0:
        out["error"] = "unknown revision"
        print(json.dumps(out, indent=1))
        return 2
    out["rev"] = full.stdout.strip()
    checks, detail = out["checks"], out["detail"]
    with tempfile.TemporaryDirectory(prefix="kake-r33-c1s-") as tmp:
        tmp = Path(tmp)
        export = tmp / "export"
        export.mkdir()
        with open(tmp / "rev.tar", "wb") as handle:
            if subprocess.run(["git", "-C", args.repo, "archive", out["rev"]], stdout=handle).returncode != 0:
                out["error"] = "git archive failed"
                print(json.dumps(out, indent=1))
                return 2
        with tarfile.open(tmp / "rev.tar") as tar:
            tar.extractall(export, filter="data")
        source = (export / RUNNER).read_text(encoding="utf-8")
        matches = list(GUARD.finditer(source))
        if len(matches) != 1:
            out["error"] = "guard pattern matched %d times (need 1)" % len(matches)
            print(json.dumps(out, indent=1))
            return 2

        spec = json.loads((export / P6_SPEC).read_text(encoding="utf-8"))
        h6 = [c for c in spec.get("cases", []) if c.get("name") == "h6"]
        checks["s1_spec"] = (len(h6) == 1 and h6[0].get("reason_code") == CODE and "reason_contains" not in h6[0])

        base = [sys.executable, "-B", str(export / HOSTILE), "--root", str(export)]
        exit_p, sum_p = run(base + ["--tmpdir", str(tmp / "h-pristine")])
        p6 = p6_detail(sum_p) or {}
        codes = (p6.get("detail") or {}).get("codes") or {}
        reasons = (p6.get("detail") or {}).get("reasons") or {}
        detail["pristine"] = {"exit": exit_p, "h6code": codes.get("h6"), "h6reason": reasons.get("h6")}
        checks["s2_field"] = (exit_p == 0 and codes.get("h6") == CODE and isinstance(reasons.get("h6"), str)
                              and CODE not in reasons["h6"])

        block = matches[0].group(0)
        raise_line = block.splitlines()[1]
        new_raise, n = MESSAGE_ARG.subn('"refused"', raise_line)
        detail["messageArgMatches"] = n
        if n == 1:
            variant = source.replace(raise_line, new_raise, 1)
            path = tmp / "msg_runner.py"
            path.write_text(variant, encoding="utf-8")
            exit_m, sum_m = run(base + ["--tmpdir", str(tmp / "h-msg"), "--runner", str(path)])
            failing = [c.get("case") for c in (sum_m or {}).get("cases", []) if c.get("passed") is not True]
            detail["messageVariant"] = {"exit": exit_m, "failing": failing, "raise": new_raise.strip()}
            checks["s3_message"] = exit_m == 0 and failing == []
        else:
            checks["s3_message"] = False

        m3 = GUARD.sub("", source, count=1)
        path = tmp / "m3_runner.py"
        path.write_text(m3, encoding="utf-8")
        exit_3, sum_3 = run(base + ["--tmpdir", str(tmp / "h-m3"), "--runner", str(path)])
        p6m = p6_detail(sum_3) or {}
        code_m = ((p6m.get("detail") or {}).get("codes") or {}).get("h6")
        detail["m3"] = {"exit": exit_3, "h6code": code_m, "p6passed": p6m.get("passed")}
        checks["s4_layer"] = exit_3 == 1 and code_m == L2_CODE and p6m.get("passed") is False
    out["met"] = sum(1 for v in checks.values() if v)
    out["of"] = len(checks)
    print(json.dumps(out, indent=1))
    return 0


if __name__ == "__main__":
    sys.exit(main())
