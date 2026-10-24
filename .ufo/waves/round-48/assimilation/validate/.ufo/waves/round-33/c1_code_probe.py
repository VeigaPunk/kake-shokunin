#!/usr/bin/env python3
"""Round-33 C1 counting command: does the hostile selftest key the P6 refusal on
a structured code instead of message text?

Usage: python3 -B c1_code_probe.py --rev <lane revision> [--repo <lane repo>]

The revision is exported with ``git archive`` into a fresh temporary directory
(read-only use of the lane repository).  Four runner variants are built from the
revision's ``scripts/citing_set_selftest.py`` and each is run through the
revision's own ``scripts/citing_set_hostile_selftest.py`` (``--runner``):

  pristine  the runner as committed                       expectation: pass (exit 0)
  reworded  the load-time guard's message fragment
            "needs an earlier 'git_init'" replaced by
            "requires a prior git_init step"; nothing else  expectation: pass (exit 0)
  m3        the load-time guard (the ``if step["op"] ==
            "git_commit" and not initialized:`` line and
            its one-line ``raise``) deleted                 expectation: killed
  recoded   the code literal "setup_commit_before_init"
            in the guard's raise line replaced by
            "setup_commit_recoded"; nothing else            expectation: killed

"killed" means: hostile exit 1, the failing spec set is exactly
{P6-commit-before-init}, and the guard holds.  The guard (``guard_ok``) is: the
pristine hostile run exits 0 with every spec passing, and the pristine runner
exits 0 over the committed benign fixtures.  A kill never counts when
``guard_ok`` is false.  A variant that cannot be built at the revision (pattern
absent or ambiguous) is recorded ``applicable: false`` and its expectation is
unmet.  A run that times out is recorded ``timedOut: true`` with exit null and
its expectation is unmet; the probe never raises on a timeout.

``met`` counts satisfied expectations (0..4).  Exit 0 when the probe ran
(whatever it found); 2 when the revision cannot be exported or the guard line
cannot be located (no variant can be judged).
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
P6 = "P6-commit-before-init"
GUARD = re.compile(
    r'^( *)if step\["op"\] == "git_commit" and not initialized:\n\1    raise \w+\([^\n]*\n', re.M
)
FRAGMENT = "needs an earlier 'git_init'"
REWORD = "requires a prior git_init step"
CODE = '"setup_commit_before_init"'
RECODE = '"setup_commit_recoded"'
TIMEOUT = 900


def run(cmd):
    try:
        done = subprocess.run(cmd, capture_output=True, text=True, timeout=TIMEOUT)
    except subprocess.TimeoutExpired:
        return {"exit": None, "timedOut": True, "summary": None}
    try:
        summary = json.loads(done.stdout)
    except ValueError:
        summary = None
    return {"exit": done.returncode, "timedOut": False, "summary": summary}


def spec_rows(summary):
    if not isinstance(summary, dict) or not isinstance(summary.get("cases"), list):
        return None
    return [(c.get("case"), c.get("passed")) for c in summary["cases"] if isinstance(c, dict)]


def failing(rows):
    return sorted(name for name, passed in rows if passed is not True) if rows is not None else None


def replace_in_guard(source, old, new):
    """Replace ``old`` with ``new`` inside the single guard match; None when not applicable."""
    matches = list(GUARD.finditer(source))
    if len(matches) != 1:
        return None
    block = matches[0].group(0)
    raise_line = block.splitlines()[1]
    if raise_line.count(old) != 1:
        return None
    new_block = block.replace(raise_line, raise_line.replace(old, new), 1)
    return source[: matches[0].start()] + new_block + source[matches[0].end():]


def main(argv=None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--rev", required=True)
    ap.add_argument("--repo", default="/home/vgpnk/Projects/shokunin/kake-shokunin")
    args = ap.parse_args(argv)
    out = {"schema": "kake-r33-c1-code-v1", "rev": None}
    full = subprocess.run(["git", "-C", args.repo, "rev-parse", "--verify", args.rev + "^{commit}"],
                          capture_output=True, text=True)
    if full.returncode != 0:
        out["error"] = "unknown revision"
        print(json.dumps(out, indent=1))
        return 2
    out["rev"] = full.stdout.strip()
    with tempfile.TemporaryDirectory(prefix="kake-r33-c1-") as tmp:
        tmp = Path(tmp)
        export = tmp / "export"
        export.mkdir()
        tar_path = tmp / "rev.tar"
        with open(tar_path, "wb") as handle:
            if subprocess.run(["git", "-C", args.repo, "archive", out["rev"]], stdout=handle).returncode != 0:
                out["error"] = "git archive failed"
                print(json.dumps(out, indent=1))
                return 2
        with tarfile.open(tar_path) as tar:
            tar.extractall(export, filter="data")
        runner = export / RUNNER
        source = runner.read_text(encoding="utf-8")
        out["runnerSha256"] = hashlib.sha256(source.encode("utf-8")).hexdigest()
        out["hostileSha256"] = hashlib.sha256((export / HOSTILE).read_bytes()).hexdigest()
        guards = GUARD.findall(source)
        out["guardMatches"] = len(guards)
        if len(guards) != 1:
            out["error"] = "guard pattern matched %d times (need 1)" % len(guards)
            print(json.dumps(out, indent=1))
            return 2
        variants = {
            "pristine": source,
            "reworded": replace_in_guard(source, FRAGMENT, REWORD),
            "m3": GUARD.sub("", source, count=1),
            "recoded": replace_in_guard(source, CODE, RECODE),
        }
        base = [sys.executable, "-B", str(export / HOSTILE), "--root", str(export)]
        results = {}
        for name, text in variants.items():
            entry = {"applicable": text is not None}
            if text is not None:
                path = tmp / ("%s_citing_set_selftest.py" % name)
                path.write_text(text, encoding="utf-8")
                entry["sha256"] = hashlib.sha256(text.encode("utf-8")).hexdigest()
                res = run(base + ["--tmpdir", str(tmp / ("h-" + name)), "--runner", str(path)])
                rows = spec_rows(res["summary"])
                entry.update({"exit": res["exit"], "timedOut": res["timedOut"],
                              "specs": rows, "failing": failing(rows)})
            results[name] = entry
        benign = run([sys.executable, "-B", str(runner), "--root", str(export), "--tmpdir", str(tmp / "benign")])
    bsum = benign["summary"] if isinstance(benign["summary"], dict) else {}
    out["benign"] = {"exit": benign["exit"], "timedOut": benign["timedOut"], "cases": bsum.get("cases"),
                     "failed": len(bsum.get("failures", [])) if isinstance(bsum.get("failures"), list) else None}
    pristine = results["pristine"]
    out["guard_ok"] = (pristine.get("exit") == 0 and pristine.get("failing") == []
                       and benign["exit"] == 0)

    def passes(entry):
        return entry["applicable"] and entry.get("exit") == 0 and entry.get("failing") == []

    def killed(entry):
        return (out["guard_ok"] and entry["applicable"] and entry.get("exit") == 1
                and entry.get("failing") == [P6])

    expectations = {
        "pristine_passes": passes(results["pristine"]) and out["guard_ok"],
        "reworded_passes": passes(results["reworded"]) and out["guard_ok"],
        "m3_killed": killed(results["m3"]),
        "recoded_killed": killed(results["recoded"]),
    }
    out["variants"] = results
    out["expectations"] = expectations
    out["met"] = sum(1 for value in expectations.values() if value)
    out["of"] = len(expectations)
    print(json.dumps(out, indent=1))
    return 0


if __name__ == "__main__":
    sys.exit(main())
