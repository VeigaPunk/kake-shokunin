#!/usr/bin/env python3
"""Render SUMMARY.md for one run_realrun.py output directory.

usage: summarize_run.py OUTDIR [--title TEXT]

Reads OUTDIR/summary.json (written by run_realrun.py) and lists, per manifest, the
declared report, the observed report and the exact differences. No evaluation of its
own: a summary can never disagree with the receipts in the same directory.
"""
import json
import os
import sys


def main(argv):
    if not argv:
        print("usage: summarize_run.py OUTDIR", file=sys.stderr)
        return 2
    out = os.path.abspath(argv[0])
    summary = json.load(open(os.path.join(out, "summary.json"), encoding="utf-8"))
    lines = ["# Real-run summary", ""]
    lines.append(f"- tool: `{summary['tool']}`")
    lines.append(f"- tool sha256: `{summary['toolSha256']}`")
    lines.append(f"- timeout: {summary['timeoutSeconds']} s per manifest")
    lines.append(f"- all declared reports matched: **{summary['allMatch']}**")
    if summary.get("unrunnable"):
        lines.append(f"- could not evaluate: {', '.join('`'+n+'`' for n in summary['unrunnable'])}")
    lines.append("")
    lines.append("| manifest | match | expected exit/verdict/evaluated | observed exit/verdict/evaluated |")
    lines.append("|---|---|---|---|")
    for run in summary["runs"]:
        lines.append(
            f"| `{run['manifest']}` | {run['matches']} | "
            f"{run['expectedExit']}/{run['expectedVerdict']}/{run['expectedChecksEvaluated']} | "
            f"{run['exit']}/{run['observedVerdict']}/{run['observedChecksEvaluated']} |")
    lines.append("")
    for run in summary["runs"]:
        if run["matches"]:
            continue
        lines.append(f"## `{run['manifest']}` differences")
        lines.append("")
        for diff in run["diffs"]:
            lines.append(f"- {diff}")
        lines.append("")
    with open(os.path.join(out, "SUMMARY.md"), "w", encoding="utf-8") as fh:
        fh.write("\n".join(lines) + "\n")
    print("wrote", os.path.join(out, "SUMMARY.md"))
    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1:]))
