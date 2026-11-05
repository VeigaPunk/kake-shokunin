#!/usr/bin/env python3
"""Round-96 identity-surface generator (committed wave evidence).

Derives `frozen/c1-surfaces.json` and the BASE_PINS counts for
`c96_selfassess.py` at a given revision, mirroring the surface schema the
round-95 counter audited, with one routed change (R95-1): knowledge entries
are pinned by PRESENCE only (their heads are correctable surfaces the E3
audit validates line-by-line), while lessons keep full-blob digests,
criteria keep headings, and SKILL rows keep first cells plus path-token
floors.  Read-only over committed bytes: `git show <rev>:<path>` only.
"""

import hashlib
import json
import os
import re
import subprocess
import sys

PATH_RE = re.compile(r"`((?:scripts|corpus|\.ufo)/[^`\s]+)`")
CRIT_RE = re.compile(r"^Round[- ]\d+")


def git(root, *args):
    p = subprocess.run(["git", "-C", root, *args], capture_output=True)
    if p.returncode != 0:
        raise SystemExit("git %s failed: %s" % (args, p.stderr.decode()[:200]))
    return p.stdout


def read(root, rev, path):
    p = subprocess.run(["git", "-C", root, "show", "%s:%s" % (rev, path)],
                       capture_output=True)
    return p.stdout if p.returncode == 0 else None


def listing(root, rev, path):
    out = git(root, "ls-tree", "-r", "--name-only", rev, path)
    return [l for l in out.decode().splitlines() if l]


def main():
    root = os.path.abspath(sys.argv[1])
    rev = sys.argv[2]
    surfaces = {"lessons": [], "entries": [], "quality_criteria_headings": [],
                "skill_rows": [], "mistakes_sections": []}

    lessons = [p for p in listing(root, rev, "corpus/lessons")
               if re.search(r"/(round-[^/]*\.md)$", p)
               and not p.endswith("-verifier-spotcheck.md")
               and "aggregator" not in p]
    for path in sorted(lessons):
        text = read(root, rev, path) or b""
        surfaces["lessons"].append(
            {"path": path, "sha256": hashlib.sha256(text).hexdigest()})
        if re.search(r"(?m)^## Mistakes\s*$", text.decode("utf-8", "replace")):
            surfaces["mistakes_sections"].append(path)

    entries = [p for p in listing(root, rev, "corpus/knowledge")
               if p.endswith(".md")]
    surfaces["entries"] = [{"path": p} for p in sorted(entries)]

    quality = (read(root, rev, "corpus/QUALITY.md") or b"").decode("utf-8", "replace")
    headings = []
    for section in re.split(r"(?m)^## ", quality)[1:]:
        head = section.splitlines()[0].strip() if section.splitlines() else ""
        if CRIT_RE.match(head) and re.search(r"criteri", section[:400], re.I):
            headings.append(head)
    surfaces["quality_criteria_headings"] = headings

    skill = (read(root, rev, "SKILL.md") or b"").decode("utf-8", "replace")
    rows = 0
    row_tokens = {}
    for line in skill.splitlines():
        if not line.startswith("|"):
            continue
        cells = [c.strip() for c in line.strip().strip("|").split("|")]
        if len(cells) < 4:
            continue
        rows += 1
        body = " ".join(cells)
        row_tokens[cells[0]] = row_tokens.get(cells[0], 0) + len(PATH_RE.findall(body))
    surfaces["skill_rows"] = [{"cell": c, "path_tokens": n}
                              for c, n in sorted(row_tokens.items())]

    pins = {"lessons": len(lessons), "entries": len(entries),
            "rows": rows, "criteria": len(headings)}
    dest = sys.argv[3]
    blob = json.dumps(surfaces, indent=1, sort_keys=True).encode("utf-8")
    if dest == "-":
        sys.stdout.write(blob.decode())
    else:
        with open(dest, "wb") as fh:
            fh.write(blob)
        print("wrote %s (%d bytes) sha256 %s"
              % (dest, len(blob), hashlib.sha256(blob).hexdigest()))
    print("pins " + json.dumps(pins))


if __name__ == "__main__":
    main()
