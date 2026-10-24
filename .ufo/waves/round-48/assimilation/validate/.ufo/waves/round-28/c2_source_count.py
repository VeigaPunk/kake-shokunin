#!/usr/bin/env python3
"""Round-28 C2 counter: field-performance sources opened this round and cited.

Usage:
    python3 -B .ufo/waves/round-28/c2_source_count.py --root <lane> --revision <commit>

Reads committed bytes at one commit (``git show <commit>:<path>``), never the
working tree.  For each declared row S036, S037, S038 and S039 it checks:

1. ``corpus/SOURCES.md`` has a registry row for the id whose source cell
   holds the declared URL, with tier ``A``, status ``mined``, opened
   ``2026-10-22`` and ``corpus/knowledge/field-performance-cwv.md`` in
   ``used-by``;
2. ``corpus/knowledge/field-performance-cwv.md`` exists, opens with
   ``source:`` / ``verified-at: 2026-10-22`` / ``recheck:`` lines, and cites
   the id as a citation token;
3. the ``## Gate`` section of ``corpus/lessons/round-28.md`` has a line that
   names the id, the declared URL, ``accessed 2026-10-22`` and one quoted
   excerpt (in curly quotes) of 1 to 25 words.

The claim value is the number of declared rows meeting every check.  Exit 0
when all four do, 1 otherwise, 2 when the commit cannot be resolved.
"""

import argparse
import json
import re
import subprocess
import sys

ENTRY = "corpus/knowledge/field-performance-cwv.md"
LESSON = "corpus/lessons/round-28.md"
REGISTRY = "corpus/SOURCES.md"
OPENED = "2026-10-22"
DECLARED = {
    "S036": "https://web.dev/articles/vitals",
    "S037": "https://web.dev/articles/defining-core-web-vitals-thresholds",
    "S038": "https://developer.chrome.com/docs/crux/methodology",
    "S039": "https://developer.chrome.com/docs/crux/api",
}
QUOTE_RE = re.compile("\u201c([^\u201d]+)\u201d")


def show(root, commit, path):
    done = subprocess.run(["git", "-C", root, "show", commit + ":" + path],
                          stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)
    return done.stdout.decode("utf-8", "replace") if done.returncode == 0 else None


def token(identifier):
    return re.compile(r"(?<!\w)" + identifier + r"(?!\w)")


def registry_row(text, identifier):
    for line in (text or "").splitlines():
        cells = [cell.strip() for cell in line.strip().strip("|").split("|")]
        if len(cells) == 11 and cells[0] == identifier:
            return cells
    return None


def gate_section(text):
    lines = (text or "").splitlines()
    out, inside = [], False
    for line in lines:
        if line.startswith("## "):
            inside = line.strip() == "## Gate"
            continue
        if inside:
            out.append(line)
    return out


def url_in(text, url):
    return re.search(re.escape(url) + r"(?![\w/-])", text) is not None


def main():
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0])
    parser.add_argument("--root", required=True)
    parser.add_argument("--revision", required=True)
    args = parser.parse_args()
    done = subprocess.run(["git", "-C", args.root, "rev-parse", "--verify", "--quiet", args.revision + "^{commit}"],
                          stdout=subprocess.PIPE, stderr=subprocess.DEVNULL)
    if done.returncode != 0:
        print(json.dumps({"error": "revision not found", "revision": args.revision}))
        return 2
    commit = done.stdout.decode().strip()
    registry = show(args.root, commit, REGISTRY)
    entry = show(args.root, commit, ENTRY)
    lesson = show(args.root, commit, LESSON)
    head = (entry or "").splitlines()[:3]
    entry_header = (
        len(head) == 3 and head[0].startswith("source:")
        and head[1].startswith("verified-at: " + OPENED) and head[2].startswith("recheck:")
    )
    gate_lines = gate_section(lesson)
    rows = []
    for identifier, url in DECLARED.items():
        problems = []
        cells = registry_row(registry, identifier)
        if cells is None:
            problems.append("no registry row")
        else:
            if not url_in(cells[1], url):
                problems.append("source cell lacks declared URL")
            if cells[3] != "A":
                problems.append("tier %r" % cells[3])
            if cells[7] != "mined":
                problems.append("status %r" % cells[7])
            if cells[8] != OPENED:
                problems.append("opened %r" % cells[8])
            if ENTRY not in cells[10]:
                problems.append("used-by lacks entry")
        if entry is None:
            problems.append("entry missing")
        else:
            if not entry_header:
                problems.append("entry header lacks source/verified-at %s/recheck" % OPENED)
            if not token(identifier).search(entry):
                problems.append("entry does not cite id")
        located = False
        for line in gate_lines:
            if not token(identifier).search(line) or not url_in(line, url) or ("accessed " + OPENED) not in line:
                continue
            quotes = QUOTE_RE.findall(line)
            if len(quotes) == 1 and 1 <= len(quotes[0].split()) <= 25:
                located = True
                break
        if not located:
            problems.append("no Gate line with id, URL, access date and one 1-25 word quote")
        rows.append({"id": identifier, "url": url, "passed": not problems, "problems": problems})
    passed = sum(1 for row in rows if row["passed"])
    print(json.dumps({"counter": ".ufo/waves/round-28/c2_source_count.py", "revision": commit,
                      "passed": passed, "total": len(rows), "rows": rows}, indent=2))
    return 0 if passed == len(rows) else 1


if __name__ == "__main__":
    sys.exit(main())
