#!/usr/bin/env python3
"""Build the round-64 control fixture repositories in a scratch directory.

Usage: build_fixtures.py <workdir> [--lane <lane-root>]

Creates, under <workdir>:
  stub-repo     scripts/quote_class.py = the committed canned-JSON stub
                (stub_tool.py, the round-63 C2 falsification as bytes).
  marker-repo   the marker-only calibration fixture: the real retained blobs,
                ledger and recipe from the round-63 base (read-only git reads
                of <lane-root> at its base revision), plus planted marker
                prose for the knowledge correction, QUALITY criterion,
                round-64 lesson Gate and SOURCES row.
  fabrication-repo
                the digest-consistent fabrication: the same real bytes plus
                marker prose — the round-63 CriticClaims §9 control shape.
                (Distinct from marker-repo only in that its knowledge file
                plants a [r63-correction] block citing the ledger without the
                frozen quote; both must print met=false under c64 and are
                recorded separately so a partial-green cannot hide.)
  junk-repo     adversarial garbage blobs (wrong shas, hostile JSON, a recipe
                that raises) with marker prose.

Each fixture is its own git repository (init + config + commit with
--allow-empty; toplevel verified). Prints one JSON line per fixture:
{"name", "path", "revision"}.
"""
from __future__ import annotations

import json
import os
import subprocess
import sys

HERE = os.path.dirname(os.path.abspath(__file__))
STUB = os.path.join(HERE, "stub_tool.py")

TOOL_REL = "scripts/quote_class.py"
RAW_REL = ".ufo/waves/round-61/sources/S432.html"
TEXT_REL = ".ufo/waves/round-63/quote-class/S432.txt"
LEDGER_REL = ".ufo/waves/round-63/quote-class/quote-classes.json"
RECIPE_REL = ".ufo/waves/round-63/quote-class/extract_text.py"
SPOT_REL = "corpus/lessons/round-61-verifier-spotcheck.md"

MARKER_SPOT = (
    "# verifier spot-check fixture\n\n"
    "| Item | Decision | Re-opened source | Agreement | Reason |\n"
    "|---|---|---|---|---|\n"
    "| S432 / Fetch | Admit | x | Disagree | planted marker reason |\n"
)
MARKER_CORRECTION = (
    "# k\n\n[r63-correction 2026-10-30] planted correction marker without the "
    "frozen quote. Ledger cited: "
    ".ufo/waves/round-63/quote-class/quote-classes.json\n"
)
MARKER_QUALITY = (
    "# q\n\n## Round-62 criteria\n\nplanted criterion marker naming "
    "X-Content-Type-Options Content-Type destination\n"
)
MARKER_LESSON = (
    "# l\n\n## Gate\n\nplanted gate marker: S432 / Fetch resolved "
    "collapsed-only by c64_calibration.py author-side\n"
)
MARKER_SOURCES = (
    "| S432 | planted | docs | A | scope | anchor | teaches | mined "
    "| 2026-10-27 | 90d | — |\n"
)


def git(d, *a):
    return subprocess.run(["git", "-C", d, *a],
                          stdout=subprocess.PIPE, stderr=subprocess.PIPE)


def make_repo(work, name, files):
    d = os.path.join(work, name)
    os.makedirs(d, exist_ok=True)
    for rel, data in files.items():
        p = os.path.join(d, rel)
        os.makedirs(os.path.dirname(p), exist_ok=True)
        with open(p, "wb") as f:
            f.write(data)
    git(d, "init", "-q")
    top = git(d, "rev-parse", "--show-toplevel")
    assert top.returncode == 0 and \
        os.path.realpath(top.stdout.decode().strip()) == os.path.realpath(d), name
    git(d, "config", "user.name", "kake-r64-fixture")
    git(d, "config", "user.email", "kake@shokunin.local")
    git(d, "add", "-A")
    c = git(d, "commit", "-q", "--allow-empty", "-m", "fixture")
    assert c.returncode == 0, name
    rev = git(d, "rev-parse", "HEAD").stdout.decode().strip()
    return {"name": name, "path": d, "revision": rev}


def main() -> int:
    work = sys.argv[1] if len(sys.argv) > 1 else "fixtures-built"
    lane = "."
    if "--lane" in sys.argv:
        lane = sys.argv[sys.argv.index("--lane") + 1]

    def base_blob(rel):
        out = subprocess.run(
            ["git", "-C", lane, "show", f"1a48131577ba82c967650561be34e8dba909432a:{rel}"],
            stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        assert out.returncode == 0, f"base blob unavailable: {rel}"
        return out.stdout

    real = {RAW_REL: base_blob(RAW_REL), TEXT_REL: base_blob(TEXT_REL),
            LEDGER_REL: base_blob(LEDGER_REL), RECIPE_REL: base_blob(RECIPE_REL)}
    with open(STUB, "rb") as f:
        stub = f.read()

    results = [
        make_repo(work, "stub-repo", {TOOL_REL: stub}),
        make_repo(work, "marker-repo", {
            SPOT_REL: base_blob(SPOT_REL), **real,
            "corpus/knowledge/response-header-expectations.md": MARKER_CORRECTION.encode(),
            "corpus/QUALITY.md": MARKER_QUALITY.encode(),
            "corpus/lessons/round-64.md": MARKER_LESSON.encode(),
            "corpus/SOURCES.md": MARKER_SOURCES.encode(),
        }),
        make_repo(work, "fabrication-repo", {
            SPOT_REL: base_blob(SPOT_REL), **real,
            "corpus/knowledge/response-header-expectations.md":
                (MARKER_CORRECTION + "planted quote follows:\n\n> planted\n").encode(),
            "corpus/QUALITY.md": MARKER_QUALITY.encode(),
            "corpus/lessons/round-64.md": MARKER_LESSON.encode(),
            "corpus/SOURCES.md": MARKER_SOURCES.encode(),
        }),
        make_repo(work, "junk-repo", {
            SPOT_REL: base_blob(SPOT_REL),
            RAW_REL: b"<html>planted</html>\n",
            TEXT_REL: b"planted text\n",
            LEDGER_REL: b'{"classes": "not-a-list"}',
            RECIPE_REL: b"def extract(raw_bytes):\n    raise RuntimeError('planted')\n",
            "corpus/knowledge/response-header-expectations.md": MARKER_CORRECTION.encode(),
            "corpus/QUALITY.md": MARKER_QUALITY.encode(),
            "corpus/lessons/round-64.md": MARKER_LESSON.encode(),
            "corpus/SOURCES.md": MARKER_SOURCES.encode(),
        }),
    ]
    for r in results:
        print(json.dumps(r, sort_keys=True))
    return 0


if __name__ == "__main__":
    sys.exit(main())
