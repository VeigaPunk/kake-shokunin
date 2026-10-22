#!/usr/bin/env python3
"""Generate round-30 receipts for the round-29 re-run.

Re-runs the two round-29 demonstrations against the committed bytes of the
lane revision under the sandbox clone and writes receipts that name what they
measured: lane revision, sha256 of every script involved, the interpreter
version, each command with its exit code and its output.

Usage:
    python3 -B make_receipts.py --root <sandbox> --out <dir>

No network access, no write outside --out.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import os
import platform
import subprocess
import sys
import time

LANE_REPO = "/home/vgpnk/Projects/shokunin/kake-shokunin"
REVISION = "4580c78cca1185d059efa6970722bbcf2f9c1b0f"
R29_REL = ".ufo/waves/round-29"
TOOL_REL = "scripts/base_path_audit.py"
SELFTEST_REL = "scripts/base_path_selftest.py"
RUNNER_REL = ".ufo/waves/round-29/real-input/real_input_run.py"


def sha256_file(path: str) -> str:
    h = hashlib.sha256()
    with open(path, "rb") as fh:
        for chunk in iter(lambda: fh.read(1 << 16), b""):
            h.update(chunk)
    return h.hexdigest()


def sha256_tree(root: str) -> str:
    """Digest of a directory: sorted per-file digests hashed together."""
    entries = []
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames.sort()
        for name in sorted(filenames):
            full = os.path.join(dirpath, name)
            rel = os.path.relpath(full, root)
            entries.append(rel + " " + sha256_file(full))
    h = hashlib.sha256()
    h.update("\n".join(sorted(entries)).encode("utf-8"))
    return h.hexdigest()


def git(clone: str, *args: str) -> str:
    proc = subprocess.run(["git", "-C", clone, *args], capture_output=True, text=True)
    if proc.returncode != 0:
        raise RuntimeError("git %s failed: %s" % (" ".join(args), proc.stderr.strip()))
    return proc.stdout.strip()


def run(argv, cwd, stdout_path, stderr_path):
    proc = subprocess.run(argv, cwd=cwd, capture_output=True, text=True)
    with open(stdout_path, "w", encoding="utf-8") as fh:
        fh.write(proc.stdout)
    with open(stderr_path, "w", encoding="utf-8") as fh:
        fh.write(proc.stderr)
    return {
        "argv": list(argv),
        "cwd": cwd,
        "exitCode": proc.returncode,
        "stdoutPath": stdout_path,
        "stderrPath": stderr_path,
        "stdout": proc.stdout,
        "stderr": proc.stderr,
    }


def load(path):
    with open(path, encoding="utf-8") as fh:
        return json.load(fh)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", required=True, help="sandbox root holding clone/ and out/")
    ap.add_argument("--out", required=True, help="receipt directory")
    args = ap.parse_args()

    root = os.path.abspath(args.root)
    out_dir = os.path.abspath(args.out)
    clone = os.path.join(root, "clone")
    os.makedirs(out_dir, exist_ok=True)
    tmpdir = os.path.join(root, "tmp")
    os.makedirs(tmpdir, exist_ok=True)
    os.environ["TMPDIR"] = tmpdir

    lane_head = git(LANE_REPO, "rev-parse", "HEAD")
    clone_head = git(clone, "rev-parse", "HEAD")
    if clone_head != REVISION:
        raise SystemExit("clone is at %s, expected %s" % (clone_head, REVISION))
    clone_status = git(clone, "status", "--porcelain")

    tool_abs = os.path.join(clone, TOOL_REL)
    selftest_abs = os.path.join(clone, SELFTEST_REL)
    runner_abs = os.path.join(clone, RUNNER_REL)
    fixtures_abs = os.path.join(clone, "scripts/fixtures/base-path")
    sites_abs = os.path.join(clone, R29_REL, "real-input/sites")

    provenance = {
        "laneRepo": LANE_REPO,
        "laneRepoHead": lane_head,
        "clonePath": clone,
        "cloneRevision": clone_head,
        "cloneWorkingTreeClean": clone_status == "",
        "cloneWorkingTreeStatus": clone_status,
        "revision": clone_head,
        "python": {
            "version": sys.version,
            "versionInfo": list(sys.version_info[:3]),
            "implementation": platform.python_implementation(),
            "executable": sys.executable,
        },
        "platform": {
            "system": platform.system(),
            "release": platform.release(),
            "machine": platform.machine(),
            "platform": platform.platform(),
        },
        "tmpdir": tmpdir,
        "network": "none; the run used only committed local snapshots",
        "laneWorkingCopyDigests": {
            TOOL_REL: sha256_file(os.path.join(LANE_REPO, TOOL_REL)),
            SELFTEST_REL: sha256_file(os.path.join(LANE_REPO, SELFTEST_REL)),
        },
        "committedReceiptAuthoring": {
            "selftest-lane-final.json": git(clone, "log", "-1", "--format=%H %cI %s",
                                            "--", R29_REL + "/verification/selftest-lane-final.json"),
            "real-input/out/summary.json": git(clone, "log", "-1", "--format=%H %cI %s",
                                               "--", R29_REL + "/real-input/out/summary.json"),
        },
        "artifacts": {
            TOOL_REL: {"sha256": sha256_file(tool_abs), "bytes": os.path.getsize(tool_abs)},
            SELFTEST_REL: {"sha256": sha256_file(selftest_abs), "bytes": os.path.getsize(selftest_abs)},
            RUNNER_REL: {"sha256": sha256_file(runner_abs), "bytes": os.path.getsize(runner_abs)},
        },
        "fixtureTree": {
            "path": os.path.relpath(fixtures_abs, clone),
            "caseCount": len([d for d in os.listdir(fixtures_abs)
                              if os.path.isdir(os.path.join(fixtures_abs, d))]),
            "sha256": sha256_tree(fixtures_abs),
        },
        "realInputSites": {
            "path": os.path.relpath(sites_abs, clone),
            "sha256": sha256_tree(sites_abs),
            "pageDigests": {
                site: sha256_file(os.path.join(sites_abs, site, "page.html"))
                for site in sorted(os.listdir(sites_abs))
                if os.path.isfile(os.path.join(sites_abs, site, "page.html"))
            },
        },
    }

    # ---- command 1: the committed selftest -------------------------------
    selftest_out = os.path.join(out_dir, "selftest.stdout.json")
    selftest_err = os.path.join(out_dir, "selftest.stderr.txt")
    cmd1 = run([sys.executable, "-B", "scripts/base_path_selftest.py"], clone, selftest_out, selftest_err)
    selftest_summary = load(selftest_out) if os.path.getsize(selftest_out) else None

    # ---- command 2: the round-29 real-input demonstration ----------------
    ri_out_dir = os.path.join(out_dir, "real-input")
    ri_stdout = os.path.join(out_dir, "real-input.stdout.txt")
    ri_stderr = os.path.join(out_dir, "real-input.stderr.txt")
    cmd2 = run([sys.executable, "-B", RUNNER_REL,
                "--tool", TOOL_REL,
                "--sites", os.path.join(R29_REL, "real-input/sites"),
                "--out", ri_out_dir], clone, ri_stdout, ri_stderr)
    ri_summary = load(os.path.join(ri_out_dir, "summary.json"))

    commands = [cmd1, cmd2]

    # ---- comparison with the committed round-29 receipts ------------------
    old_self = load(os.path.join(clone, R29_REL, "verification/selftest-lane-final.json"))
    old_summary = load(os.path.join(clone, R29_REL, "real-input/out/summary.json"))
    old_sites = {s["site"]: s for s in old_summary.get("sites") or []}
    new_sites = {s["site"]: s for s in ri_summary.get("sites") or []}

    per_site = {}
    for site in sorted(set(old_sites) | set(new_sites)):
        old_file = load(os.path.join(clone, R29_REL, f"real-input/out/{site}.json"))
        new_file = load(os.path.join(ri_out_dir, f"{site}.json"))
        per_site[site] = {
            "oldRow": old_sites.get(site),
            "newRow": new_sites.get(site),
            "rowEqual": old_sites.get(site) == new_sites.get(site),
            "resultObjectEqual": old_file.get("result") == new_file.get("result"),
            "exitEqual": old_file.get("exit") == new_file.get("exit"),
            "stdoutEqual": old_file.get("stdout") == new_file.get("stdout"),
            "stderrEqual": old_file.get("stderr") == new_file.get("stderr"),
            "oldToolArgv": old_file.get("argv"),
            "newToolArgv": new_file.get("argv"),
            "oldFindings": (old_file.get("result") or {}).get("findings"),
            "newFindings": (new_file.get("result") or {}).get("findings"),
        }

    table = {
        "selftestCases": {"old": old_self.get("cases"), "new": selftest_summary.get("cases")},
        "selftestPassed": {"old": old_self.get("passed"), "new": selftest_summary.get("passed")},
        "selftestFailed": {"old": old_self.get("failed"), "new": selftest_summary.get("failed")},
        "selftestVerdict": {"old": old_self.get("verdict"), "new": selftest_summary.get("verdict")},
        "sites": {"old": old_summary["totals"].get("sites"), "new": ri_summary["totals"].get("sites")},
        "pagesChecked": {"old": old_summary["totals"].get("pagesChecked"),
                         "new": ri_summary["totals"].get("pagesChecked")},
        "referencesChecked": {"old": old_summary["totals"].get("referencesChecked"),
                              "new": ri_summary["totals"].get("referencesChecked")},
        "findings": {"old": old_summary["totals"].get("findings"),
                     "new": ri_summary["totals"].get("findings")},
        "failedSites": {"old": old_summary["totals"].get("failedSites"),
                        "new": ri_summary["totals"].get("failedSites")},
        "contractProblems": {"old": old_summary.get("contractProblems"),
                             "new": ri_summary.get("contractProblems")},
        "siteExits": {"old": {s: old_sites[s]["exit"] for s in sorted(old_sites)},
                      "new": {s: new_sites[s]["exit"] for s in sorted(new_sites)}},
        "selftestCaseNamesEqual": old_self.get("caseNames") == selftest_summary.get("caseNames"),
        "totalsEqual": old_summary.get("totals") == ri_summary.get("totals"),
    }
    for key, value in table.items():
        if isinstance(value, dict) and set(value) == {"old", "new"}:
            value["equal"] = value["old"] == value["new"]

    provenance_gap = {
        "claim": "the committed round-29 receipts name no revision and no tool digest",
        "committedSelftestReceipt": {
            "path": R29_REL + "/verification/selftest-lane-final.json",
            "sha256": sha256_file(os.path.join(clone, R29_REL, "verification/selftest-lane-final.json")),
            "hasRevision": False,
            "hasToolDigest": False,
            "hasPythonVersion": False,
        },
        "committedRealInputSummary": {
            "path": R29_REL + "/real-input/out/summary.json",
            "sha256": sha256_file(os.path.join(clone, R29_REL, "real-input/out/summary.json")),
            "hasRevision": False,
            "hasToolDigest": False,
            "hasPythonVersion": False,
        },
        "committedRealInputSiteFiles": {
            site: {
                "path": R29_REL + f"/real-input/out/{site}.json",
                "sha256": sha256_file(os.path.join(clone, R29_REL, f"real-input/out/{site}.json")),
                "hasRevision": False,
                "hasToolDigest": False,
            }
            for site in sorted(old_sites)
        },
        "note": ("the committed real-input site files name the interpreter only inside the "
                 "recorded argv, not a version string; the summary and the selftest receipt "
                 "name no interpreter at all"),
    }

    receipt = {
        "receipt": "kake-r30-r29-rerun",
        "purpose": ("round-30 re-run of the round-29 base-path selftest and the round-29 "
                    "real-input demonstration, with receipts that name what they measured"),
        "createdAt": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "provenance": provenance,
        "commands": commands,
        "results": {
            "selftestSummary": selftest_summary,
            "realInputSummary": ri_summary,
        },
        "comparisonWithCommittedRound29": {
            "committedSelftestReceipt": {
                "path": R29_REL + "/verification/selftest-lane-final.json",
                "sha256": sha256_file(os.path.join(clone, R29_REL, "verification/selftest-lane-final.json")),
            },
            "committedRealInputSummary": {
                "path": R29_REL + "/real-input/out/summary.json",
                "sha256": sha256_file(os.path.join(clone, R29_REL, "real-input/out/summary.json")),
            },
            "table": table,
            "perSite": per_site,
        },
        "provenanceGapInCommittedReceipts": provenance_gap,
    }

    path = os.path.join(out_dir, "receipt.json")
    with open(path, "w", encoding="utf-8") as fh:
        json.dump(receipt, fh, indent=2, sort_keys=True)
        fh.write("\n")
    print("wrote", path)
    for entry in commands:
        print("exit %d: %s" % (entry["exitCode"], " ".join(entry["argv"])))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
