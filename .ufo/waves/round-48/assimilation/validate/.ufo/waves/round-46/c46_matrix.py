#!/usr/bin/env python3
"""Round-46 C1 sealed matrix counter.

Frozen counting command (SCORECARD.md round-46 declarations):

    python3 -B .ufo/waves/round-46/c46_matrix.py --root . --revision <commit> \
        --stage before|after

Decides, over the committed bytes at <commit>:
  before = at least one planted witness uncaught, or one do-nothing /
           constant / junk control accepted.
  after  = every planted witness caught by scripts/redirect_audit.py and every
           do-nothing, constant and junk control rejected, matrix wall time
           < 120 s (routed round-45 defect 4).

The counter runs the audited tool as a CLI over committed fixture manifests,
materialized read-only via `git archive` into a temporary directory; it never
writes to the repo. Receipt identity per corpus/QUALITY.md (round 46): the
receipt records the measured revision, the audited tool's path + sha256, this
counter's path + sha256, per-fixture exits, control verdicts and wall time.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import subprocess
import sys
import tempfile
import time

EXIT_PASS = 0
EXIT_FAIL = 1
EXIT_INPUT = 2
EXIT_USAGE = 64

WALL_BUDGET_S = 120.0

COUNTER_REL = ".ufo/waves/round-46/c46_matrix.py"
TOOL_REL = "scripts/redirect_audit.py"
INDEX_REL = ".ufo/waves/round-46/fixtures/index.json"


class UsageError(Exception):
    pass


class InputError(Exception):
    pass


class ArgumentParser(argparse.ArgumentParser):
    def error(self, message: str) -> None:
        raise UsageError(message)


def parse_cli(argv: list[str]) -> argparse.Namespace:
    parser = ArgumentParser(
        prog="c46_matrix.py",
        usage="c46_matrix.py --root PATH --revision REV --stage before|after [--json [PATH]]",
        allow_abbrev=False,
    )
    parser.add_argument("--root", required=True, metavar="PATH")
    parser.add_argument("--revision", required=True, metavar="REV")
    parser.add_argument("--stage", required=True, choices=("before", "after"))
    parser.add_argument("--json", nargs="?", const="-", metavar="PATH")
    return parser.parse_args(argv)


def sha256_file(path: str) -> str:
    digest = hashlib.sha256()
    with open(path, "rb") as handle:
        for chunk in iter(lambda: handle.read(65536), b""):
            digest.update(chunk)
    return digest.hexdigest()


def materialize(root: str, revision: str, dest: str) -> None:
    archive = subprocess.run(
        ["git", "-C", root, "archive", revision],
        capture_output=True,
    )
    if archive.returncode != 0:
        raise InputError(f"git archive {revision} failed: {archive.stderr.decode(errors='replace')[:200]}")
    extract = subprocess.run(["tar", "-x", "-C", dest], input=archive.stdout)
    if extract.returncode != 0:
        raise InputError("tar extract failed")


def run_tool(python: str, tool: str, manifest: str) -> tuple[int, dict | None]:
    try:
        proc = subprocess.run(
            [python, "-B", tool, "--manifest", manifest],
            capture_output=True, text=True, timeout=60,
        )
    except subprocess.TimeoutExpired:
        return 124, None
    if proc.returncode not in (0, 1, 2):
        return proc.returncode, None
    try:
        report = json.loads(proc.stdout)
    except json.JSONDecodeError:
        return 125, None
    return proc.returncode, report


def run_control(python: str, control: str, manifest: str) -> tuple[int, dict | None]:
    return run_tool(python, control, manifest)


def main(argv: list[str] | None = None) -> int:
    args = parse_cli(sys.argv[1:] if argv is None else argv)
    root = os.path.abspath(args.root)
    started = time.monotonic()

    with tempfile.TemporaryDirectory(prefix="kake-r46-matrix-") as tmp:
        materialize(root, args.revision, tmp)
        # Fixtures are the round's frozen oracle: they live in the working
        # tree, outside the measured revision. Only the audited tool bytes
        # come from <revision>.
        index_path = os.path.join(root, INDEX_REL)
        tool_path = os.path.join(tmp, TOOL_REL)
        if not os.path.exists(index_path):
            print(f"c46_matrix: fixture index missing at {INDEX_REL} under {root}", file=sys.stderr)
            return EXIT_INPUT
        with open(index_path, "r", encoding="utf-8") as handle:
            index = json.load(handle)

        witnesses = index["witnesses"]          # [{"name":..., "manifest":...}]
        clean = index.get("clean", [])
        controls = index["controls"]            # {"do_nothing": rel, "constant": rel, "junk": rel}
        junk_manifest = index["junk_manifest"]

        tool_present = os.path.exists(tool_path)
        tool_sha = sha256_file(tool_path) if tool_present else None

        results: dict[str, dict] = {"witnesses": {}, "clean": {}, "controls": {}}
        witnesses_caught = 0
        for entry in witnesses:
            name = entry["name"]
            if not tool_present:
                results["witnesses"][name] = {"caught": False, "exit": None, "reason": "tool_absent"}
                continue
            code, report = run_tool(sys.executable, tool_path, os.path.join(tmp, entry["manifest"]))
            caught = code == 1 and isinstance(report, dict) and report.get("verdict") == "failed-policy"
            results["witnesses"][name] = {
                "caught": caught, "exit": code,
                "findings": len(report.get("findings", [])) if isinstance(report, dict) else None,
            }
            witnesses_caught += 1 if caught else 0

        clean_false_positives = 0
        for entry in clean:
            name = entry["name"]
            if not tool_present:
                results["clean"][name] = {"flagged": None, "exit": None, "reason": "tool_absent"}
                continue
            code, report = run_tool(sys.executable, tool_path, os.path.join(tmp, entry["manifest"]))
            flagged = code == 1
            results["clean"][name] = {"flagged": flagged, "exit": code}
            clean_false_positives += 1 if flagged else 0

        # Controls: a control is ACCEPTED only if it reproduces the full
        # after-state by shortcut (flags every witness as failed-policy and
        # does not claim clean on the junk manifest). Rejected = it misses at
        # least one witness or accepts junk. The do-nothing, constant and junk
        # controls must all be rejected for the after-stage to pass.
        controls_accepted = 0
        for control_name, control_rel in controls.items():
            control_path = os.path.join(tmp, control_rel)
            if not os.path.exists(control_path):
                results["controls"][control_name] = {"present": False, "accepted": False}
                continue
            accepted = True
            detail: dict[str, int] = {}
            for entry in witnesses:
                code, report = run_control(sys.executable, control_path, os.path.join(tmp, entry["manifest"]))
                flagged_claim = code == 1 and isinstance(report, dict) and report.get("verdict") == "failed-policy"
                detail[entry["name"]] = code
                if not flagged_claim:
                    accepted = False
            code, report = run_control(sys.executable, control_path, os.path.join(tmp, junk_manifest))
            junk_clean = code == 0 and isinstance(report, dict) and report.get("verdict") == "clean"
            if junk_clean:
                accepted = False
            results["controls"][control_name] = {
                "present": True, "accepted": accepted, "witness_exits": detail,
                "junk_exit": code, "junk_clean": junk_clean,
                "sha256": sha256_file(control_path),
            }
            if accepted:
                controls_accepted += 1

        wall_s = time.monotonic() - started
        total = len(witnesses)
        after_met = (
            tool_present
            and witnesses_caught == total
            and clean_false_positives == 0
            and controls_accepted == 0
            and wall_s < WALL_BUDGET_S
        )
        before_met = (not tool_present) or witnesses_caught < total or controls_accepted > 0
        stage_met = before_met if args.stage == "before" else after_met

        receipt = {
            "schema": "kake-c46-matrix-receipt-v1",
            "stage": args.stage,
            "revision": args.revision,
            "measuredAt": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
            "counter": {"path": COUNTER_REL, "sha256": sha256_file(os.path.abspath(__file__))},
            "tool": {"path": TOOL_REL, "sha256": tool_sha, "present": tool_present},
            "witnesses": {"caught": witnesses_caught, "total": total, "rows": results["witnesses"]},
            "clean": {"false_positives": clean_false_positives, "rows": results["clean"]},
            "controls": {"accepted": controls_accepted, "rows": results["controls"]},
            "wall_s": round(wall_s, 3),
            "wall_budget_s": WALL_BUDGET_S,
            "stage_met": stage_met,
        }
        encoded = json.dumps(receipt, sort_keys=True, separators=(",", ":"))
        if args.json is None or args.json == "-":
            print(encoded)
        else:
            with open(args.json, "w", encoding="utf-8", newline="\n") as handle:
                handle.write(encoded + "\n")

        suffix = "PASS" if stage_met else "FAIL"
        print(f"stage={args.stage} witnesses_caught={witnesses_caught}/{total} "
              f"clean_false_positives={clean_false_positives} controls_accepted={controls_accepted} "
              f"wall_s={wall_s:.3f} MATRIX_{args.stage.upper()}_{suffix}")
        return EXIT_PASS if stage_met else EXIT_FAIL


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except UsageError as exc:
        print(f"c46_matrix.py: {exc}", file=sys.stderr)
        raise SystemExit(EXIT_USAGE)
    except InputError as exc:
        print(f"c46_matrix.py: {exc}", file=sys.stderr)
        raise SystemExit(EXIT_INPUT)
