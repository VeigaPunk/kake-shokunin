#!/usr/bin/env python3
"""C2 constant 3: empty findings, real exit codes.

Same CLI as scripts/sitemap_audit.py (`--manifest <path>`).  It runs the tool
under measurement, keeps its exit code and its input-fault (status "error")
items, and empties every `findings` list.  The tool under measurement is named
by the environment variable C2_REAL_TOOL (c77_sitemap_matrix.py sets it to the
tool it is measuring); without it the lane's own scripts/sitemap_audit.py is
used.

It must be counted as a failed constant by c77_sitemap_matrix.py: every case
whose expected finding-id set is non-empty is decided with an empty set.  If
the matrix compared only exit codes, this constant would pass every case whose
exit it mirrors, which is exactly what the findings comparison must reject.
"""

import json
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
LANE_ROOT = os.path.abspath(os.path.join(HERE, "..", "..", "..", ".."))

EXIT_USAGE = 64


def _measured_tool():
    named = os.environ.get("C2_REAL_TOOL")
    if named:
        return os.path.abspath(named)
    return os.path.join(LANE_ROOT, "scripts", "sitemap_audit.py")


def _strip(document):
    """The measured document with every finding list emptied."""
    checks = []
    for check in document.get("checks", []):
        if not isinstance(check, dict):
            continue
        status = check.get("status")
        if status == "error":
            checks.append({"id": check.get("id"), "status": "error", "error": check.get("error"), "findings": []})
        else:
            checks.append({"id": check.get("id"), "status": "clean", "error": None, "findings": []})
    verdict = "could-not-evaluate" if any(item["status"] == "error" for item in checks) else "clean"
    return {"version": 1, "verdict": verdict, "checks": checks}


def main(argv):
    if len(argv) != 3 or argv[1] != "--manifest":
        return EXIT_USAGE
    tool = _measured_tool()
    if tool == os.path.abspath(__file__) or not os.path.isfile(tool):
        return EXIT_USAGE
    try:
        completed = subprocess.run(
            [sys.executable, "-B", tool] + argv[1:],
            capture_output=True,
            timeout=300,
            env=dict(os.environ, PYTHONDONTWRITEBYTECODE="1"),
        )
    except (OSError, subprocess.SubprocessError):
        return EXIT_USAGE
    try:
        document = json.loads(completed.stdout.decode("utf-8"))
        if not isinstance(document, dict) or not isinstance(document.get("checks"), list):
            raise ValueError("no checks")
    except (UnicodeDecodeError, ValueError):
        sys.stdout.write(
            json.dumps({"version": 1, "verdict": "could-not-evaluate", "error": "input_invalid", "checks": []})
            + "\n"
        )
        return completed.returncode
    sys.stdout.write(json.dumps(_strip(document), ensure_ascii=True) + "\n")
    return completed.returncode


if __name__ == "__main__":
    sys.exit(main(sys.argv))
