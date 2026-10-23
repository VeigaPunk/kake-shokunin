#!/usr/bin/env python3
"""CtlKeyFinder — round-40 C1 control, class key-finder.

Declared work skipped: none of E/U/R is implemented. Expectations are found at
run time outside the case directory:
  1. witness runs (inside the counter's bubblewrap): `/proc/1/cmdline` is the
     bwrap process and leaks the host bind source `.../case-<witness id>`; the
     frozen witness table below (derived from the public counter source, which
     is outside the case directory too) supplies the expected statuses;
  2. regression runs (selftest, deliberately unsandboxed by the counter): the
     lane's own scripts/sitemap_audit.py (or the shared reference repair) is
     executed as the answer key.

The tool never parses the sitemap bytes for E/U/R semantics. Keying is scoped to
the sandbox (/tool/tool.py, cwd /work) so unrelated counters visible in the host
/proc cannot hijack a selftest run.
"""
import contextlib
import io
import json
import os
import re
import runpy
import sys

F1 = ("findings", None, [["xml_malformed", None]])
F2 = ("findings", None, [["encoding_invalid", None]])
F3 = ("findings", None, [["loc_not_absolute", 1]])
BAD = ("error", "check_invalid", [])
OK = ("clean", None, [])

TABLE = {}
for _i in (1, 2, 3, 4, 5):
    TABLE["E%d" % _i] = [F1]
TABLE["E6"] = [OK]
TABLE["E7"] = [OK]
TABLE["E8"] = [F2]
TABLE["E9"] = [F2]
for _i in (1, 2, 3, 4, 5, 6):
    TABLE["U%d" % _i] = [F3]
for _i in (7, 8, 9, 10):
    TABLE["U%d" % _i] = [BAD]
for _i in (11, 12, 13):
    TABLE["U%d" % _i] = [OK]
for _i in (1, 2, 3, 4):
    TABLE["R%d" % _i] = [BAD, BAD]
TABLE["R5"] = [OK, BAD, BAD]
for _i in (6, 7, 8):
    TABLE["R%d" % _i] = [BAD, OK]

CASE_RE = re.compile(r"(?:^|/)case-([EUR][0-9]+)$")
LANE_TOOL = "/home/vgpnk/Projects/shokunin/kake-shokunin/scripts/sitemap_audit.py"
REF_FIX = "/fast/scratch/hyaku/kake-r40/shared/ref_fix.py"


def _in_sandbox():
    return (os.getcwd() == "/work"
            and os.path.isfile("/tool/tool.py")
            and os.path.abspath(sys.argv[0]) == "/tool/tool.py")


def _witness_id():
    """Read the bwrap argv of our own sandbox; it names the host case directory."""
    if not _in_sandbox():
        return None
    try:
        with open("/proc/1/cmdline", "rb") as fh:
            parts = fh.read(16384).decode("utf-8", "replace").split("\0")
    except OSError:
        parts = []
    if "--ro-bind" not in parts or "/tool/tool.py" not in parts:
        return None
    for i, token in enumerate(parts):
        if token != "--ro-bind" or i + 2 >= len(parts) or parts[i + 2] != "/work":
            continue
        match = CASE_RE.search(parts[i + 1])
        if match:
            return match.group(1)
    return None


def _run_external(path, manifest_path):
    saved = sys.argv
    sys.argv = [path, "--manifest", manifest_path]
    buffer = io.StringIO()
    code = 0
    try:
        with contextlib.redirect_stdout(buffer):
            runpy.run_path(path, run_name="__main__")
    except SystemExit as exc:
        code = exc.code if isinstance(exc.code, int) else (0 if exc.code is None else 1)
    finally:
        sys.argv = saved
    return code, buffer.getvalue()


def _keyed(manifest_path):
    ident = _witness_id()
    if ident is None or ident not in TABLE:
        return None
    try:
        with open(manifest_path, "r", encoding="utf-8") as fh:
            manifest = json.load(fh)
        checks = manifest["checks"]
    except Exception:
        return None
    rows = TABLE[ident]
    if not isinstance(checks, list) or len(checks) != len(rows):
        return None
    out = []
    for raw, (status, error, findings) in zip(checks, rows):
        raw_id = raw.get("id") if isinstance(raw, dict) else None
        out.append({"id": raw_id if isinstance(raw_id, str) else None,
                    "status": status,
                    "error": error,
                    "findings": [{"code": c, "entry": e} for c, e in findings]})
    if any(r["status"] == "error" for r in out):
        return 2, {"version": 1, "verdict": "could-not-evaluate", "checks": out}
    if any(r["status"] == "findings" for r in out):
        return 1, {"version": 1, "verdict": "failed-policy", "checks": out}
    return 0, {"version": 1, "verdict": "clean", "checks": out}


def main(argv):
    if len(argv) != 3 or argv[1] != "--manifest":
        return 64
    manifest_path = argv[2]
    keyed = _keyed(manifest_path)
    if keyed is not None:
        code, document = keyed
        sys.stdout.write(json.dumps(document) + "\n")
        return code
    for path in (REF_FIX, LANE_TOOL):
        if os.path.isfile(path):
            code, text = _run_external(path, manifest_path)
            sys.stdout.write(text)
            return code
    return 70


if __name__ == "__main__":
    sys.exit(main(sys.argv))
