#!/usr/bin/env python3
"""Write receipts/divergence.txt: the three probes where the two builds disagree,
self-contained (fixture text, command, exit, verbatim stdout)."""
from __future__ import annotations

import json
import os
import subprocess
import sys

S = "/fast/scratch/hyaku/kake-r76/ExecAuditRealRun"
LANE = "/home/vgpnk/Projects/shokunin/kake-shokunin"
TOOL = os.environ.get("KAKE_TOOL", os.path.join(LANE, ".ufo/waves/round-76/w1/ExecAuditTool/hreflang_audit.py"))
REF = os.path.join(S, "ref/hreflang_audit.py")
WORK_TOOL = os.path.join(S, "work-tool")
WORK = os.path.join(S, "work")
TMP = os.path.join(S, "tmp")
BASE = os.path.join(S, "probe-divergence")
OUT = os.path.join(LANE, ".ufo/waves/round-76/w1/ExecAuditRealRun/receipts/divergence.txt")
ENV = dict(os.environ, TMPDIR=TMP, PYTHONDONTWRITEBYTECODE="1")

PROBES = [
    (
        "p1_relative_href_not_resolved",
        {"a.html": '<html><head><link rel="canonical" href="/p/">'
                   '<link rel="alternate" hreflang="en" href="/p/"></head></html>'},
        1,
        [{"id": "a", "file": "a.html", "url": "https://a.test/p/"}],
        "Amendment 2 A4: a non-absolute href contributes to no other finding, so it cannot satisfy\n"
        "self-reference; A2 makes hreflang_self_missing once per page.",
    ),
    (
        "p3_two_xdefault_same_href",
        {"a.html": '<html><head><link rel="alternate" hreflang="x-default" href="https://a.test/p/">'
                   '<link rel="alternate" hreflang="X-Default" href="https://a.test/p/"></head></html>'},
        1,
        [{"id": "a", "file": "a.html", "url": "https://a.test/p/"}],
        "Amendment 2 A2: a policy finding is emitted once per offending annotation, except\n"
        "self_missing/canonical_not_self which are once per page; whether multiple_xdefault is\n"
        "page-level or per-annotation is not spelled out, so both readings are shown here.",
    ),
    (
        "p10_manifest_version_2",
        {"a.html": "<html><head></head></html>"},
        2,
        [{"id": "a", "file": "a.html", "url": "https://a.test/p/"}],
        "Amendment 2 A15: version != 1 is exit 64.",
    ),
    (
        "p11_duplicate_file_two_pages",
        {"a.html": "<html><head></head></html>"},
        1,
        [{"id": "a", "file": "a.html", "url": "https://a.test/p/"},
         {"id": "b", "file": "a.html", "url": "https://b.test/"}],
        "Amendment 2 A15: two pages may not share a file (the amendment names no id or exit for it).",
    ),
]


def main() -> int:
    os.makedirs(BASE, exist_ok=True)
    lines = [
        "# Advisory divergence record for the real-input seat. Not a matrix case, not a",
        "# verdict: the fixture, both commands and both observed outputs are quoted so the",
        "# matrix or review seat can turn either one into a case.",
        "",
    ]
    for name, files, version, pages, note in PROBES:
        for leaf in files:
            with open(os.path.join(BASE, leaf), "w", encoding="utf-8") as fh:
                fh.write(files[leaf])
        mpath = os.path.join(BASE, "manifest.json")
        with open(mpath, "w", encoding="utf-8") as fh:
            json.dump({"version": version, "pages": pages}, fh, indent=1, sort_keys=True)
        lines.append(f"## {name}")
        lines.append(f"amendment: {note}")
        for leaf, html in files.items():
            lines.append(f"fixture {leaf}: {html}")
        lines.append(f"manifest: {json.dumps({'version': version, 'pages': pages}, sort_keys=True)}")
        for label, tool_path, work in (("tool", TOOL, WORK_TOOL), ("ref", REF, WORK)):
            argv = [sys.executable, "-B", tool_path, "--manifest", mpath, "--root", BASE, "--json", "--work", work]
            proc = subprocess.run(argv, env=ENV, capture_output=True, text=True)
            lines.append(f"$ {label}: {' '.join(argv)}")
            lines.append(f"exit={proc.returncode}")
            lines.append(f"stdout={proc.stdout.strip()}")
            if proc.stderr.strip():
                lines.append(f"stderr={proc.stderr.strip()}")
        lines.append("")
    with open(OUT, "w", encoding="utf-8") as fh:
        fh.write("\n".join(lines) + "\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
