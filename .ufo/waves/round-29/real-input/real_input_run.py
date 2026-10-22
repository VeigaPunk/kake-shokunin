#!/usr/bin/env python3
"""Run a base-path audit tool over the three real owned GitHub Pages snapshots.

Usage:
  python3 -B real_input_run.py --tool /path/to/scripts/base_path_audit.py \
      [--sites DIR] [--out DIR] [--python EXE]

For every site directory under --sites (each holding manifest.json plus the
snapshot page files) the tool is invoked as
    <python> -B <tool> --manifest <site>/manifest.json
The tool's stdout JSON is stored per site as <out>/<site>.json and a combined
<out>/summary.json plus a human-readable table are written.

Exit status of this runner: 0 when every site ran and the tool answered with
its documented exit codes (0 clean, 1 failed-policy, 2 could-not-evaluate),
1 when the tool is missing or behaved outside the contract.
"""
from __future__ import annotations

import argparse
import json
import os
import subprocess
import sys

VALID_TOOL_EXITS = (0, 1, 2)


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--tool", required=True, help="path to the base path audit tool")
    ap.add_argument("--sites", default="sites", help="directory holding one subdir per site")
    ap.add_argument("--out", default="out", help="output directory")
    ap.add_argument("--python", default=sys.executable)
    args = ap.parse_args()

    tool = os.path.abspath(args.tool)
    if not os.path.isfile(tool):
        sys.stderr.write(f"tool not found: {tool}\n")
        return 1
    sites_root = os.path.abspath(args.sites)
    out_root = os.path.abspath(args.out)
    os.makedirs(out_root, exist_ok=True)

    site_dirs = sorted(
        d for d in os.listdir(sites_root) if os.path.isfile(os.path.join(sites_root, d, "manifest.json"))
    )
    if not site_dirs:
        sys.stderr.write(f"no site manifests under {sites_root}\n")
        return 1

    rows = []
    problems = 0
    for site in site_dirs:
        manifest = os.path.join(sites_root, site, "manifest.json")
        argv = [args.python, "-B", tool, "--manifest", manifest]
        proc = subprocess.run(argv, capture_output=True, text=True)
        payload = None
        parse_error = None
        try:
            payload = json.loads(proc.stdout) if proc.stdout.strip() else None
        except json.JSONDecodeError as exc:
            parse_error = str(exc)
        record = {
            "site": site,
            "manifest": manifest,
            "argv": argv,
            "exit": proc.returncode,
            "stdout": proc.stdout,
            "stderr": proc.stderr,
            "result": payload,
            "stdoutNotJson": parse_error,
        }
        with open(os.path.join(out_root, f"{site}.json"), "w", encoding="utf-8") as fh:
            json.dump(record, fh, indent=2, sort_keys=True)
            fh.write("\n")
        if proc.returncode not in VALID_TOOL_EXITS or parse_error or not isinstance(payload, dict):
            problems += 1
        res = payload if isinstance(payload, dict) else {}
        findings = res.get("findings")
        rows.append(
            {
                "site": site,
                "exit": proc.returncode,
                "verdict": res.get("verdict"),
                "pagesChecked": res.get("pagesChecked"),
                "referencesChecked": res.get("referencesChecked"),
                "findings": len(findings) if isinstance(findings, list) else None,
            }
        )

    summary = {
        "tool": tool,
        "sitesRoot": sites_root,
        "outRoot": out_root,
        "sites": rows,
        "totals": {
            "sites": len(rows),
            "findings": sum(r["findings"] or 0 for r in rows),
            "pagesChecked": sum(r["pagesChecked"] or 0 for r in rows),
            "referencesChecked": sum(r["referencesChecked"] or 0 for r in rows),
            "failedSites": sum(1 for r in rows if r["verdict"] == "failed-policy"),
        },
        "contractProblems": problems,
    }
    with open(os.path.join(out_root, "summary.json"), "w", encoding="utf-8") as fh:
        json.dump(summary, fh, indent=2, sort_keys=True)
        fh.write("\n")

    width = max(len(r["site"]) for r in rows)
    print(f"{'site'.ljust(width)}  exit  verdict            pages  refs  findings")
    for r in rows:
        print(
            f"{r['site'].ljust(width)}  {str(r['exit']).rjust(4)}  "
            f"{str(r['verdict']).ljust(18)} {str(r['pagesChecked']).rjust(5)}  "
            f"{str(r['referencesChecked']).rjust(4)}  {str(r['findings']).rjust(8)}"
        )
    print(
        f"totals: sites={summary['totals']['sites']} "
        f"pagesChecked={summary['totals']['pagesChecked']} "
        f"referencesChecked={summary['totals']['referencesChecked']} "
        f"findings={summary['totals']['findings']} "
        f"failedSites={summary['totals']['failedSites']} "
        f"contractProblems={problems}"
    )
    return 1 if problems else 0


if __name__ == "__main__":
    raise SystemExit(main())
