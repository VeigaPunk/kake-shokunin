#!/usr/bin/env python3
"""Round-34 real-input run of scripts/link_preview_audit.py (corroboration, NOT a counter).

Written after wave-1 CriticDeclarationFit showed that a lookup-table tool which
parses no HTML scores 28/28 on the frozen C1 matrix. This script is not part of
either declared measurement; it is disclosed evidence only.

Reads the tool from `git show <revision>:scripts/link_preview_audit.py` and the
retained ds4cc archive from the same revision, extracts the 102 pages into a
temporary directory, writes a version-1 manifest (url = https://ds4cc.com/<path>
with a trailing index.html removed), runs the tool once, and compares its
og_required_missing counts per property with the C2 counter's recount
(`census.derived` of the receipt named by --census): missing og:X must equal
pages - og:X, and the tool must report no other policy finding than the census
implies (og-url-equals-canonical = og:url means no og_url_not_canonical).

Usage: python3 -B real_input_run.py --root <lane> --revision <commit> --census <c2 receipt json>
Exit 0 when every comparison holds; 1 otherwise; 2 on bad input.
"""
from __future__ import annotations

import argparse
import collections
import io
import json
import lzma
import os
import subprocess
import sys
import tarfile
import tempfile
from pathlib import Path

ARCHIVE = ".ufo/waves/round-34/sources/ds4cc-7fc6aa2f/html.tar.xz"
TOOL = "scripts/link_preview_audit.py"


def show(root: str, rev: str, path: str) -> bytes | None:
    env = {k: v for k, v in os.environ.items() if not k.startswith("GIT_")}
    p = subprocess.run(["git", "-C", root, "show", f"{rev}:{path}"], capture_output=True, env=env)
    return p.stdout if p.returncode == 0 else None


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", required=True)
    ap.add_argument("--revision", required=True)
    ap.add_argument("--census", required=True)
    a = ap.parse_args()
    tool, arch = show(a.root, a.revision, TOOL), show(a.root, a.revision, ARCHIVE)
    derived = json.loads(Path(a.census).read_text())["census"]["derived"]
    if tool is None or arch is None or not derived:
        print(json.dumps({"error": "tool, archive or census missing"}))
        return 2
    with tempfile.TemporaryDirectory(prefix="kake-r34-real-") as tmp:
        site = Path(tmp) / "site"
        tf = tarfile.open(fileobj=io.BytesIO(lzma.decompress(arch)), mode="r:")
        pages = []
        for m in tf.getmembers():
            if m.isfile():
                dest = site / m.name
                dest.parent.mkdir(parents=True, exist_ok=True)
                dest.write_bytes(tf.extractfile(m).read())
                url = "https://ds4cc.com/" + (m.name[: -len("index.html")] if m.name.endswith("index.html") else m.name)
                pages.append({"file": m.name, "url": url})
        (site / "manifest.json").write_text(json.dumps({"version": 1, "pages": sorted(pages, key=lambda p: p["file"])}))
        tpath = Path(tmp) / "link_preview_audit.py"
        tpath.write_bytes(tool)
        proc = subprocess.run([sys.executable, "-B", str(tpath), "--manifest", str(site / "manifest.json")],
                              capture_output=True, timeout=120)
    report = json.loads(proc.stdout)
    by = collections.Counter((f["reason"], f.get("property")) for f in report["findings"])
    pages_n = derived["pages"]
    expect = {("og_required_missing", p): pages_n - derived[p] for p in ("og:title", "og:type", "og:image", "og:url")}
    expect = {k: v for k, v in expect.items() if v}
    if derived["og:url"] - derived["og-url-equals-canonical"]:
        expect[("og_url_not_canonical", "og:url")] = None  # count not derivable from the census alone
    observed = {f"{r}|{p}": n for (r, p), n in sorted(by.items())}
    ok = (proc.returncode == (1 if expect else 0) and report.get("pagesChecked") == pages_n
          and all(by.get(k) == v for k, v in expect.items() if v is not None)
          and set(by) == set(expect))
    print(json.dumps({"script": "kake-r34-real-input-run", "revision": a.revision, "toolExit": proc.returncode,
                      "verdict": report.get("verdict"), "pagesChecked": report.get("pagesChecked"),
                      "observed": observed, "expectedFromCensus": {f"{r}|{p}": n for (r, p), n in expect.items()},
                      "census": derived, "agrees": ok}, indent=1))
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
