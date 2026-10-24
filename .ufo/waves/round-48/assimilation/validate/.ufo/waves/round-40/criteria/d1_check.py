#!/usr/bin/env python3
"""D1 check for kake-shokunin round 40 (ExecD1Check).

The round-39 spot-check routed "fix D1": `<?xml version="1.1"?>` with 1.0-only
content should be `xml_malformed`.  The round-40 declaration rejects that fix
from S110 (XML 1.0, sec. 2.8): a 1.x declaration other than "1.0" is processed
as a 1.0 document, so that document is well-formed XML 1.0 (contract sentence
8) and must be `clean`; `version="2.0"` is not a 1.x declaration and stays
`xml_malformed`.

This check enforces that reading.  Two files, identical byte for byte except
the XML declaration's `version` pseudo-attribute:

  v11: `<?xml version="1.1" encoding="UTF-8"?>` + 1.0-only content
  v20: `<?xml version="2.0" encoding="UTF-8"?>` + the same content

Each file gets its own manifest and its own tool run, so the exit codes are
per-file:

  pass  v11: exit 0, verdict "clean", check status "clean", findings []
  pass  v20: exit 1, verdict "failed-policy", findings {(xml_malformed, null)}

Exit 0 only when both pass (green); 1 when either fails (red: the tool would
apply the rejected D1 fix, or cannot tell the two apart); 2 when the tool is
missing, does not run, or does not emit one JSON object (cannot evaluate).

Usage: python3 -B d1_check.py --tool <path> [--out <receipt.json>]
"""

import argparse
import hashlib
import json
import os
import shutil
import subprocess
import sys
import tempfile

NS = "http://www.sitemaps.org/schemas/sitemap/0.9"
SITEMAP_URL = "https://example.com/dir/sitemap.xml"

# 1.0-only content: no XML 1.1-only characters, no restricted characters.
BODY = (
    '<urlset xmlns="%s">'
    "<url><loc>https://example.com/dir/page</loc>"
    "<lastmod>2026-10-23</lastmod>"
    "<changefreq>daily</changefreq><priority>0.5</priority></url>"
    "<url><loc>https://example.com/dir/other</loc></url>"
    "</urlset>"
) % NS

CASES = (
    ("v11", "1.1", "clean"),
    ("v20", "2.0", "xml_malformed"),
)


def _document(version):
    return ('<?xml version="%s" encoding="UTF-8"?>\n' % version) + BODY + "\n"


def _isolated():
    """The two documents must differ only in the declaration's version."""
    a = _document("1.1").replace('version="1.1"', 'version="X"')
    b = _document("2.0").replace('version="2.0"', 'version="X"')
    return a == b


def _tool_sha256(path):
    try:
        with open(path, "rb") as handle:
            return hashlib.sha256(handle.read()).hexdigest()
    except OSError:
        return None


def _run_case(tool, version):
    """Run the tool on one document; return a receipt dict for the case."""
    workdir = tempfile.mkdtemp(prefix="d1check-")
    try:
        name = "sitemap.xml"
        with open(os.path.join(workdir, name), "wb") as handle:
            handle.write(_document(version).encode("utf-8"))
        manifest = {
            "version": 1,
            "checks": [{"id": "v", "file": name, "sitemapUrl": SITEMAP_URL}],
        }
        with open(os.path.join(workdir, "manifest.json"), "w", encoding="utf-8") as handle:
            json.dump(manifest, handle)
        try:
            proc = subprocess.run(
                [sys.executable, "-B", tool, "--manifest",
                 os.path.join(workdir, "manifest.json")],
                cwd=workdir, capture_output=True, timeout=120,
            )
        except (OSError, subprocess.TimeoutExpired) as exc:
            return {"case": "v" + version.replace(".", ""), "version": version,
                    "ran": False, "detail": "tool did not run: %s" % (exc,)}
        raw = proc.stdout.decode("utf-8", "replace")
        try:
            document = json.loads(raw)
        except ValueError:
            return {"case": "v" + version.replace(".", ""), "version": version,
                    "ran": False, "exit": proc.returncode,
                    "stdout": raw[:400],
                    "detail": "stdout is not one JSON object"}
        checks = document.get("checks")
        item = checks[0] if isinstance(checks, list) and len(checks) == 1 else None
        status = item.get("status") if isinstance(item, dict) else None
        found = item.get("findings") if isinstance(item, dict) else None
        codes = None
        if isinstance(found, list):
            codes = [list(pair) for pair in sorted(
                (f.get("code"), f.get("entry")) for f in found if isinstance(f, dict)
            )]
        return {
            "case": "v" + version.replace(".", ""),
            "version": version,
            "ran": True,
            "exit": proc.returncode,
            "verdict": document.get("verdict"),
            "status": status,
            "error": item.get("error") if isinstance(item, dict) else None,
            "findings": codes,
            "stderr_bytes": len(proc.stderr),
        }
    finally:
        shutil.rmtree(workdir, ignore_errors=True)


def _judge(receipt, expected):
    if not receipt.get("ran"):
        return False
    if expected == "clean":
        return (receipt.get("exit") == 0
                and receipt.get("verdict") == "clean"
                and receipt.get("status") == "clean"
                and receipt.get("error") is None
                and receipt.get("findings") == [])
    return (receipt.get("exit") == 1
            and receipt.get("verdict") == "failed-policy"
            and receipt.get("status") == "findings"
            and receipt.get("findings") == [["xml_malformed", None]])


def main(argv):
    parser = argparse.ArgumentParser(description="D1 reading check (round 40)")
    parser.add_argument("--tool", required=True)
    parser.add_argument("--out")
    args = parser.parse_args(argv)

    tool = os.path.abspath(args.tool)
    report = {
        "check": "D1",
        "reading": "version=\"1.1\" with 1.0-only content is clean; "
                   "version=\"2.0\" is xml_malformed",
        "tool": tool,
        "tool_sha256": _tool_sha256(tool),
        "python": sys.version.split()[0],
        "exists": os.path.isfile(tool),
        "documents_isolated": _isolated(),
        "cases": [],
    }

    if not report["exists"] or not report["documents_isolated"]:
        report["result"] = "cannot-evaluate"
        _emit(report, args.out)
        return 2

    outcomes = []
    for label, version, expected in CASES:
        receipt = _run_case(tool, version)
        receipt["expected"] = expected
        receipt["pass"] = _judge(receipt, expected)
        outcomes.append(receipt)
        report["cases"].append(receipt)

    if any(not case.get("ran") for case in outcomes):
        result, code = "cannot-evaluate", 2
    elif all(case["pass"] for case in outcomes):
        result, code = "green", 0
    else:
        result, code = "red", 1
    report["result"] = result
    _emit(report, args.out)
    return code


def _emit(report, out):
    text = json.dumps(report, indent=2, sort_keys=False) + "\n"
    if out:
        with open(out, "w", encoding="utf-8") as handle:
            handle.write(text)
    sys.stdout.write(text)


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
