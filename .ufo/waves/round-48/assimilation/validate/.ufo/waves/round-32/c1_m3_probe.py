#!/usr/bin/env python3
"""Round-32 C1 counting command: is mutant m3 killed by the hostile selftest?

m3 (round-31 MutRunnerGuards) deletes the load-time guard in
``scripts/citing_set_selftest.py`` that refuses a ``git_commit`` setup step
with no earlier ``git_init`` (the two lines ``if step["op"] == "git_commit"
and not initialized:`` / ``raise ValueError(...)``).  In round 31 the hostile
selftest still passed with m3 applied (exit 0): the guard had no fixture of
its own.

Usage: python3 -B c1_m3_probe.py --rev <lane revision> [--repo <lane repo>]

The revision is exported with ``git archive`` into a fresh temporary
directory (read-only use of the lane repository).  Three runs follow, all on
the export:
  pristine  hostile selftest with the revision's own runner
  mutant    hostile selftest with an m3 copy of that runner (--runner)
  benign    the revision's runner over the committed benign fixtures
Prints one JSON object.  ``killed`` is 1 when the mutant run exits 1, else 0.
``guard_ok`` is true when the pristine hostile run exits 0 and the benign run
exits 0; a kill only counts with ``guard_ok`` true.  Exit 0 when the probe ran
(whatever it found), 2 when it could not run (export or mutation failed).
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
import sys
import tarfile
import tempfile
from pathlib import Path

RUNNER = "scripts/citing_set_selftest.py"
HOSTILE = "scripts/citing_set_hostile_selftest.py"
GUARD = re.compile(r'^( *)if step\["op"\] == "git_commit" and not initialized:\n\1    raise ValueError\([^\n]*\n',
                   re.M)


def run(cmd, timeout=900):
    done = subprocess.run(cmd, capture_output=True, text=True, timeout=timeout)
    try:
        summary = json.loads(done.stdout)
    except ValueError:
        summary = None
    return done.returncode, summary


def main(argv=None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--rev", required=True)
    ap.add_argument("--repo", default="/home/vgpnk/Projects/shokunin/kake-shokunin")
    args = ap.parse_args(argv)
    out = {"schema": "kake-r32-c1-m3-v1", "rev": None, "m3Applied": False}
    full = subprocess.run(["git", "-C", args.repo, "rev-parse", "--verify", args.rev + "^{commit}"],
                          capture_output=True, text=True)
    if full.returncode != 0:
        out["error"] = "unknown revision"
        print(json.dumps(out, indent=1))
        return 2
    out["rev"] = full.stdout.strip()
    with tempfile.TemporaryDirectory(prefix="kake-r32-m3-") as tmp:
        tmp = Path(tmp)
        export = tmp / "export"
        export.mkdir()
        tar_path = tmp / "rev.tar"
        with open(tar_path, "wb") as handle:
            subprocess.run(["git", "-C", args.repo, "archive", out["rev"]], stdout=handle, check=True)
        with tarfile.open(tar_path) as tar:
            tar.extractall(export, filter="data")
        runner = export / RUNNER
        source = runner.read_text(encoding="utf-8")
        out["runnerSha256"] = hashlib.sha256(source.encode("utf-8")).hexdigest()
        mutant_src, n = GUARD.subn("", source)
        if n != 1:
            out["error"] = "m3 guard pattern matched %d times (need 1)" % n
            print(json.dumps(out, indent=1))
            return 2
        out["m3Applied"] = True
        mutant = tmp / "m3_citing_set_selftest.py"
        mutant.write_text(mutant_src, encoding="utf-8")
        base = [sys.executable, "-B", str(export / HOSTILE), "--root", str(export)]
        p_exit, p_sum = run(base + ["--tmpdir", str(tmp / "h-pristine")])
        m_exit, m_sum = run(base + ["--tmpdir", str(tmp / "h-mutant"), "--runner", str(mutant)])
        b_exit, b_sum = run([sys.executable, "-B", str(runner), "--root", str(export),
                             "--tmpdir", str(tmp / "benign")])
    specs = lambda s: [(c.get("case"), c.get("passed")) for c in (s or {}).get("cases", [])]
    out["pristine"] = {"exit": p_exit, "specs": specs(p_sum)}
    out["mutant"] = {"exit": m_exit, "specs": specs(m_sum)}
    out["benign"] = {"exit": b_exit, "cases": (b_sum or {}).get("cases") if isinstance(b_sum, dict) else None,
                     "failed": len((b_sum or {}).get("failures", [])) if isinstance(b_sum, dict) else None}
    out["guard_ok"] = p_exit == 0 and b_exit == 0
    out["killed"] = 1 if m_exit == 1 else 0
    print(json.dumps(out, indent=1))
    return 0


if __name__ == "__main__":
    sys.exit(main())
