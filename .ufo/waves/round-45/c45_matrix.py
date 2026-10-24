#!/usr/bin/env python3
"""Run the round-45 C1 receipt-integrity matrix — the claim's frozen counting command.

--stage before: run the FROZEN v1 driver (.ufo/waves/round-44/c44_audit.py) over the
    three committed invalid fixture classes plus the honest control. invalid_accepted
    counts how many of the three invalid classes certify ok=True (the claim's
    before-state: 3).

--stage after: run driver v2 (.ufo/waves/round-45/c45_audit.py) over the same fixture
    classes (stale-planted's backdating twin for the mtime branch), then run the honest
    27-control regression under v2 with the frozen counter v5 and the 020bc457 build.
    invalid_accepted must be 0, rejections_named must name 3 distinct classes
    (counter_error, tool_absent, stale_receipt), and the honest receipt must validate
    against pinned identity fields (counter sha, 27 controls, witnessed 27, build 3/3).

Every leg runs in a fresh uuid cohort (round-44 lesson 13: receipt cohorts never share
a parent). Receipts re-derive: rerun this command; nothing is cached across runs.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import shutil
import subprocess
import sys
import time
import uuid
from pathlib import Path

LANE = Path(__file__).resolve().parents[3]
WAVE = LANE / ".ufo" / "waves" / "round-45"
V1_DRIVER = WAVE.parent / "round-44" / "c44_audit.py"
V2_DRIVER = WAVE / "c45_audit.py"
COUNTER_V5 = WAVE.parent / "round-44" / "c44_count_v5.py"
CONTROLS_27 = WAVE.parent / "round-44" / "controls-27.tsv"
FIXTURES = WAVE / "fixtures"
MATRIX_DIR = WAVE / "verification" / "matrix"
HONEST_DIR = WAVE / "verification" / "honest-regression"
BUILD_REVISION = "020bc457"
BUILD_REVISION_FULL = "020bc4574729ed674299f6cab02faac1582d9464"
ERROR_CLASS_RE = re.compile(r"(?<![a-z0-9_])(counter_error|tool_absent|stale_receipt)(?![a-z0-9_])")
INVALID_CLASSES = ("counter-error", "tool-absent", "stale-planted")
AFTER_STALE_FIXTURE = "stale-backdate"
# each fixture leg must be refused by ITS OWN named class, not by any class (w2
# AttackMatrixReceipt F2: the union gate was permutation-blind)
LEG_EXPECTED_CLASS = {"counter-error": "counter_error", "tool-absent": "tool_absent",
                      "stale-planted": "stale_receipt", "stale-backdate": "stale_receipt"}


def sha256(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def run_driver(driver: Path, controls: Path, counter: Path, expect: str, out: Path,
               extra: tuple = ()) -> subprocess.CompletedProcess:
    out.parent.mkdir(parents=True, exist_ok=True)
    argv = [sys.executable, "-B", str(driver), "--root", str(LANE), "--controls",
            str(controls), "--counter", str(counter), "--classes", "v5",
            "--expect", expect, "--out", str(out), *extra]
    return subprocess.run(argv, capture_output=True, stdin=subprocess.DEVNULL, timeout=1800)


def load_summary(path: Path):
    try:
        return json.loads(path.read_text())
    except (OSError, ValueError):
        return None


def rejection_classes(summary) -> set:
    found = set()
    for row in (summary or {}).get("rows", []):
        for match in ERROR_CLASS_RE.findall(str(row.get("error") or "")):
            found.add(match)
    return found


def stage_fixtures(stage: str):
    stale = "stale-planted" if stage == "before" else AFTER_STALE_FIXTURE
    stale_leg = "stale-planted" if stage == "before" else "stale-backdate"
    return [("counter-error", "counter-error"), ("tool-absent", "tool-absent"),
            (stale, stale_leg)]


def run_fixture_leg(stage: str, driver: Path, plant: bool):
    results = {}
    for fixture, leg_name in stage_fixtures(stage):
        fx = FIXTURES / fixture
        cohort = MATRIX_DIR / "runs" / stage / ("%s-%s" % (leg_name, uuid.uuid4().hex[:12]))
        summary_path = cohort / "summary.json"
        if plant and (fx / "tools").is_dir():
            # v1 stale leg: pre-plant the copied receipts, as the fixture documents.
            shutil.copytree(fx / "tools", cohort / "tools")
            for name in ("build-1.json", "build-2.json", "build-3.json"):
                if (fx / name).is_file():
                    (cohort / name).write_bytes((fx / name).read_bytes())
        proc = run_driver(driver, fx / "controls.tsv", fx / "fake_counter.py",
                          "witnessed", summary_path,
                          ("--build-rev", BUILD_REVISION, "--build-runs", "3", "--workers", "1"))
        summary = load_summary(summary_path)
        results[leg_name] = {
            "fixture": fixture, "exit": proc.returncode,
            "ok": bool(summary and summary.get("ok")),
            "rejection_classes": sorted(rejection_classes(summary)),
            "cohort": str(cohort.relative_to(LANE)),
            "summary": str(summary_path.relative_to(LANE)),
        }
    return results


def run_honest_leg(stage: str, driver: Path):
    cohort = MATRIX_DIR / "runs" / stage / ("honest-%s" % uuid.uuid4().hex[:12])
    summary_path = cohort / "after-v5-v2.json" if driver == V2_DRIVER else cohort / "after-v5-v1.json"
    proc = run_driver(driver, CONTROLS_27, COUNTER_V5, "witnessed", summary_path,
                      ("--build-rev", BUILD_REVISION, "--build-runs", "3", "--workers", "4",
                       "--label", "kake-r45-honest-" + stage))
    summary = load_summary(summary_path)
    valid = False
    problems = []
    if summary is None:
        problems.append("no summary written")
    else:
        if summary.get("counterSha256") != sha256(COUNTER_V5):
            problems.append("counter sha mismatch")
        if driver == V2_DRIVER:
            if summary.get("driverSha256") != sha256(driver):
                problems.append("driver sha mismatch (summary self-report)")
            manifest_path = cohort / "run-manifest.json"
            try:
                manifest = json.loads(manifest_path.read_text())
                if manifest.get("counter_sha256") != sha256(COUNTER_V5):
                    problems.append("manifest counter sha mismatch")
                if manifest.get("driver_sha256") != sha256(driver):
                    problems.append("manifest driver sha mismatch")
            except (OSError, ValueError):
                problems.append("no readable run-manifest.json (real driver never ran)")
        build_files = sorted(cohort.glob("build-*.json"))
        if len(build_files) != 3:
            problems.append("build receipt files != 3")
        else:
            for bf in build_files:
                try:
                    brec = json.loads(bf.read_text())
                except (OSError, ValueError):
                    problems.append("unreadable %s" % bf.name)
                    continue
                if brec.get("met") is not True or brec.get("revision") != BUILD_REVISION_FULL:
                    problems.append("build receipt %s not met at %s" % (bf.name, BUILD_REVISION_FULL))
        if summary.get("controls") != 27:
            problems.append("controls != 27")
        if summary.get("ok") is not True:
            problems.append("ok is not True")
        if summary.get("witnessed") != 27:
            problems.append("witnessed != 27")
        build = summary.get("build") or []
        if len(build) != 3 or not all(b.get("met") is True for b in build):
            problems.append("build not 3/3 met")
        if summary.get("errors"):
            problems.append("errors present")
        valid = not problems
    result = {"exit": proc.returncode, "valid": valid, "problems": problems,
              "witnessed": (summary or {}).get("witnessed"),
              "build_met": sum(1 for b in (summary or {}).get("build", []) if b.get("met") is True),
              "cohort": str(cohort.relative_to(LANE)),
              "summary": str(summary_path.relative_to(LANE))}
    if driver == V2_DRIVER and summary is not None:
        HONEST_DIR.mkdir(parents=True, exist_ok=True)
        shutil.copyfile(summary_path, HONEST_DIR / "after-v5-v2.json")
    return result


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--stage", choices=("before", "after"), required=True)
    args = parser.parse_args()
    driver = V1_DRIVER if args.stage == "before" else V2_DRIVER
    plant = args.stage == "before"

    fixtures = run_fixture_leg(args.stage, driver, plant)
    honest = run_honest_leg(args.stage, driver)

    invalid_accepted = sum(1 for r in fixtures.values() if r["ok"])
    named = set()
    for r in fixtures.values():
        named.update(r["rejection_classes"])
    honest_witnessed = honest["witnessed"] if honest["valid"] else 0
    honest_build_met = honest["build_met"] if honest["valid"] else 0
    leg_class_ok = all(
        LEG_EXPECTED_CLASS.get(leg) in set(r["rejection_classes"])
        for leg, r in fixtures.items())

    receipt = {
        "stage": args.stage, "driver": str(driver.relative_to(LANE)),
        "driver_sha256": sha256(driver), "ran_at_ns": time.time_ns(),
        "fixtures": fixtures, "honest": honest,
        "invalid_accepted": invalid_accepted, "rejections_named": len(named),
        "named_classes": sorted(named),
        "honest_witnessed": honest_witnessed, "honest_build_met": honest_build_met,
    }
    MATRIX_DIR.mkdir(parents=True, exist_ok=True)
    (MATRIX_DIR / ("%s.json" % args.stage)).write_text(json.dumps(receipt, indent=1) + "\n")

    print("stage=%s invalid_accepted=%d rejections_named=%d honest_witnessed=%s honest_build_met=%s"
          % (args.stage, invalid_accepted, len(named), honest_witnessed, honest_build_met))
    if args.stage == "before":
        # the honest leg must also certify under v1 (w2 AttackMatrixReceipt F3: the
        # before gate used to be blind to it); per-leg class checks are after-only —
        # v1 accepts the invalid legs (that IS the before-state)
        passed = invalid_accepted == 3 and honest["valid"]
    else:
        passed = (invalid_accepted == 0 and len(named) == 3 and leg_class_ok and
                  honest_witnessed == 27 and honest_build_met == 3)
    print("MATRIX_%s_%s" % (args.stage.upper(), "PASS" if passed else "FAIL"))
    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
