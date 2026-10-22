#!/usr/bin/env python3
"""Round-32 C2 counting command: are the external ds4cc-marketplace blobs retained and cited?

Usage: python3 -B c2_retained_count.py --rev <lane revision> [--repo <lane repo>]

Reads only committed bytes at the revision (git ls-tree / git show):
  c1  both blob ids d17ab7e5... (render.yaml) and ee0b6381... (apps-sdk/Dockerfile)
      appear in ``git ls-tree -r <rev>`` -> the lane holds byte-identical copies
  c2  ``corpus/SOURCES.md`` ``## Registry`` has a row whose source cell names
      ``ds4cc-marketplace`` and ``1fbdb8ed`` and whose ``opened`` cell is 2026-10-22
  c3  ``corpus/knowledge/render-web-services.md`` cites that row id
Prints JSON with ``met`` (0..3). Exit 0 when it ran, 2 on a bad revision.
"""
from __future__ import annotations

import argparse
import json
import re
import subprocess
import sys

BLOBS = {"render.yaml": "d17ab7e5d44b1b3a1876cf1d9b47f369e92f7252",
         "apps-sdk/Dockerfile": "ee0b63819a9ce71e51469796541b9075e9676ae9"}
ENTRY = "corpus/knowledge/render-web-services.md"


def git(repo, *args):
    return subprocess.run(["git", "-C", repo, *args], capture_output=True, text=True)


def main(argv=None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--rev", required=True)
    ap.add_argument("--repo", default="/home/vgpnk/Projects/shokunin/kake-shokunin")
    args = ap.parse_args(argv)
    full = git(args.repo, "rev-parse", "--verify", args.rev + "^{commit}")
    if full.returncode != 0:
        print(json.dumps({"error": "unknown revision"}))
        return 2
    rev = full.stdout.strip()
    tree = git(args.repo, "ls-tree", "-r", rev).stdout.splitlines()
    held = {}
    for line in tree:
        meta, _, path = line.partition("\t")
        parts = meta.split()
        if len(parts) == 3 and parts[1] == "blob":
            held.setdefault(parts[2], []).append(path)
    c1_paths = {name: held.get(blob, []) for name, blob in BLOBS.items()}
    c1 = all(c1_paths.values())
    sources = git(args.repo, "show", "%s:corpus/SOURCES.md" % rev).stdout
    registry = sources.split("## Registry", 1)[-1].split("\n## ", 1)[0] if "## Registry" in sources else ""
    row_ids = []
    for line in registry.splitlines():
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if len(cells) == 11 and re.fullmatch(r"S\d{3}", cells[0]) and "ds4cc-marketplace" in cells[1] \
                and "1fbdb8ed" in cells[1] and cells[8] == "2026-10-22":
            row_ids.append(cells[0])
    c2 = bool(row_ids)
    entry = git(args.repo, "show", "%s:%s" % (rev, ENTRY)).stdout
    cites = {rid: len(re.findall(r"\b%s\b" % rid, entry)) for rid in row_ids}
    c3 = any(n > 0 for n in cites.values())
    out = {"schema": "kake-r32-c2-retained-v1", "rev": rev, "c1BlobPaths": c1_paths, "c1": c1,
           "c2RowIds": row_ids, "c2": c2, "c3Cites": cites, "c3": c3, "met": int(c1) + int(c2) + int(c3)}
    print(json.dumps(out, indent=1))
    return 0


if __name__ == "__main__":
    sys.exit(main())
