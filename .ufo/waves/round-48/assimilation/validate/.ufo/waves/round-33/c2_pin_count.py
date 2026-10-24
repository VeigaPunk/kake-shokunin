#!/usr/bin/env python3
"""Round-33 C2 counting command: has the corpus' ds4cc-marketplace source pin
advanced to upstream commit 7fc6aa2f, with re-derivable facts?

Usage: python3 -B c2_pin_count.py --rev <lane revision> [--repo <lane repo>]

Reads committed bytes at the revision only (``git ls-tree`` / ``git show`` /
``git archive`` of one directory); never the working tree.  Four conditions:

  c1 retained  each of the four upstream paths below exists under
               RETAIN_DIR/<path> as a mode-100644 blob whose id equals the
               upstream blob id pinned here (path-, mode- and id-exact).
  c2 row       corpus/SOURCES.md, inside its "## Registry" section only, holds
               exactly one row whose first cell is exactly "S065"; cells split
               on unescaped pipes give 11 cells; the source cell contains the
               full upstream hash, status is "mined", opened is "2026-10-22",
               and used-by contains ENTRY.
  c3 section   ENTRY holds exactly one line equal to HEADING; that section (to
               the next "## " heading or EOF) contains "S065" and the full hash.
  c4 truth     inside that section: the line "sitemap-locs: <N>" equals the
               <loc> count of the retained sitemap.xml (parsed as XML), and for
               each of the three frostbite pages the line
               "canonical <url>: <verdict>" equals the verdict the revision's own
               scripts/canonical_audit.py returns on the retained page with
               expectedCanonical = <url>.  c4 requires c1.

``met`` counts conditions met (0..4).  Exit 0 when the count ran; 2 when the
revision is unknown.
"""
from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys
import tarfile
import tempfile
import xml.etree.ElementTree as ET
from pathlib import Path

UPSTREAM = "7fc6aa2fc12451dd451fed5a9ee7125f3a90e884"
RETAIN_DIR = ".ufo/waves/round-33/sources/ds4cc-7fc6aa2f"
PINNED = {
    "sitemap.xml": "67d8c7a50dc3a3734ce4be97ffa4810e1e257e12",
    "magga/frostbite/index.html": "e0d9ee29d9f1bf21faa0238e3253d4e9199304de",
    "magga/frostbite/classic/index.html": "12c58e2dae534f6569015fa3c0ec8cde502c5119",
    "magga/frostbite/remastered/index.html": "4e6d70ae05272e089f4564b1ed6f3c9b21a440a2",
}
PAGES = {
    "https://ds4cc.com/magga/frostbite/": "magga/frostbite/index.html",
    "https://ds4cc.com/magga/frostbite/classic/": "magga/frostbite/classic/index.html",
    "https://ds4cc.com/magga/frostbite/remastered/": "magga/frostbite/remastered/index.html",
}
SOURCES = "corpus/SOURCES.md"
ENTRY = "corpus/knowledge/sitemap-orphan-audit.md"
HEADING = "## Round-33 ds4cc source pin 7fc6aa2f"
ROW_ID = "S065"
SITEMAP_NS = "{http://www.sitemaps.org/schemas/sitemap/0.9}"


def git(repo, *args):
    return subprocess.run(["git", "-C", repo, *args], capture_output=True)


def show(repo, rev, path):
    done = git(repo, "show", "%s:%s" % (rev, path))
    return done.stdout.decode("utf-8") if done.returncode == 0 else None


def section(text, heading):
    lines = text.splitlines()
    starts = [i for i, line in enumerate(lines) if line == heading]
    if len(starts) != 1:
        return None, len(starts)
    body = []
    for line in lines[starts[0] + 1:]:
        if line.startswith("## "):
            break
        body.append(line)
    return "\n".join(body), 1


def main(argv=None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--rev", required=True)
    ap.add_argument("--repo", default="/home/vgpnk/Projects/shokunin/kake-shokunin")
    args = ap.parse_args(argv)
    out = {"schema": "kake-r33-c2-pin-v1", "rev": None, "conditions": {}, "detail": {}}
    full = git(args.repo, "rev-parse", "--verify", args.rev + "^{commit}")
    if full.returncode != 0:
        out["error"] = "unknown revision"
        print(json.dumps(out, indent=1))
        return 2
    rev = out["rev"] = full.stdout.decode().strip()
    cond, detail = out["conditions"], out["detail"]

    # c1 retained
    blobs = {}
    for path, blob in PINNED.items():
        listed = git(args.repo, "ls-tree", "-z", rev, "--", "%s/%s" % (RETAIN_DIR, path)).stdout.decode()
        entries = [e for e in listed.split("\0") if e]
        ok = False
        if len(entries) == 1:
            meta, _, name = entries[0].partition("\t")
            mode, kind, oid = meta.split(" ")
            ok = (name == "%s/%s" % (RETAIN_DIR, path) and mode == "100644" and kind == "blob" and oid == blob)
        blobs[path] = ok
    detail["retained"] = blobs
    cond["c1_retained"] = all(blobs.values())

    # c2 row
    sources = show(args.repo, rev, SOURCES) or ""
    registry, _ = section(sources, "## Registry")
    rows = []
    for line in (registry or "").splitlines():
        if not line.startswith("|"):
            continue
        cells = [c.strip() for c in re.split(r"(?<!\\)\|", line.strip())[1:-1]]
        if cells and cells[0] == ROW_ID:
            rows.append(cells)
    row_ok = False
    if len(rows) == 1 and len(rows[0]) == 11:
        cells = rows[0]
        row_ok = (UPSTREAM in cells[1] and cells[7] == "mined" and cells[8] == "2026-10-22"
                  and ENTRY in cells[10])
    detail["rowsFound"] = len(rows)
    detail["rowCells"] = len(rows[0]) if len(rows) == 1 else None
    cond["c2_row"] = row_ok

    # c3 section
    entry = show(args.repo, rev, ENTRY) or ""
    body, headings = section(entry, HEADING)
    detail["headingCount"] = headings
    cond["c3_section"] = body is not None and ROW_ID in body and UPSTREAM in body

    # c4 truth
    truth = False
    if cond["c1_retained"] and body is not None:
        with tempfile.TemporaryDirectory(prefix="kake-r33-c2-") as tmp:
            tmp = Path(tmp)
            tar_path = tmp / "rev.tar"
            with open(tar_path, "wb") as handle:
                git_ok = subprocess.run(["git", "-C", args.repo, "archive", rev, RETAIN_DIR,
                                         "scripts/canonical_audit.py"], stdout=handle).returncode == 0
            if git_ok:
                with tarfile.open(tar_path) as tar:
                    tar.extractall(tmp / "x", filter="data")
                root = tmp / "x" / RETAIN_DIR
                locs = [el.text for el in ET.parse(root / "sitemap.xml").getroot().iter(SITEMAP_NS + "loc")]
                detail["sitemapLocs"] = len(locs)
                stated = re.findall(r"(?m)^sitemap-locs: (\d+)$", body)
                detail["statedLocs"] = stated
                locs_ok = len(stated) == 1 and int(stated[0]) == len(locs)
                verdicts = {}
                pages_ok = True
                for url, rel in PAGES.items():
                    manifest = root / ("manifest-%d.json" % len(verdicts))
                    manifest.write_text(json.dumps({"version": 1, "pages": [
                        {"url": url, "file": rel, "expectedCanonical": url}]}), encoding="utf-8")
                    try:
                        done = subprocess.run([sys.executable, "-B", str(tmp / "x" / "scripts/canonical_audit.py"),
                                               "--manifest", str(manifest)], capture_output=True, text=True,
                                              timeout=120)
                        observed = json.loads(done.stdout).get("verdict")
                    except (subprocess.TimeoutExpired, ValueError, AttributeError):
                        observed = None
                    claimed = re.findall(r"(?m)^canonical %s: (\S+)$" % re.escape(url), body)
                    verdicts[url] = {"observed": observed, "stated": claimed}
                    pages_ok = pages_ok and observed is not None and claimed == [observed]
                detail["canonical"] = verdicts
                truth = locs_ok and pages_ok
    cond["c4_truth"] = truth
    out["met"] = sum(1 for value in cond.values() if value)
    out["of"] = len(cond)
    print(json.dumps(out, indent=1))
    return 0


if __name__ == "__main__":
    sys.exit(main())
