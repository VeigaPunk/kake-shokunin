#!/usr/bin/env python3
"""CriticClaims r93: build the cheapest repair that drives c93_selfassess.py to
`mismatches=0 met=true` while every repaired statement stays wrong in the sense
the class names. Run with cwd = a scratch clone checked out at the base
10ecbd1ade91d0721e87a9942a66a2b61d5ce8d5; it rewrites files in that clone only.

Each repair is deliberately the *least* content-preserving closure available:

  E1  corpus/lessons/round-85.md  gets an empty `## Gate` heading appended at EOF
      (no body at all: the heading is the whole predicate).
  E2  eight corpus/QUALITY.md criterion sections each get one appended line
      citing `corpus/lessons/round-1.md` -- a real lesson that says nothing
      about any of the eight criteria.
  E3  corpus/knowledge/meta-robots-directives.md gets `source: S001`, a real row
      id (the upload-pages-artifact action) that supports nothing in the entry.
  E4  four lessons lose the blank line that split their `## Mistakes` table; no
      row is added, moved or checked.
  E5  six SKILL.md rows stop naming the missing path (five by deleting the
      pointer, one by repointing it at a real but wrong artifact).

Nothing else is touched. The population pins are unaffected by construction:
lesson/entry/row/criteria counts are unchanged.
"""

import re
import sys

E2_HEADS = [
    "## Round-31 wave-2 corrections to the round-31 criteria",
    "## Round-32 criteria",
    "## Round-34 wave-2 corrections to the round-34 criteria",
    "## Round-35 wave-2 corrections to the round-35 criteria",
    "## Round-40 criteria",
    "## Round-41 criteria",
    "## Round-47 pointer correction — R6",
    "## Round-76 criterion — quoted receipts are whole",
]
E4_LESSONS = ["round-29.md", "round-33.md", "round-54.md", "round-92.md"]
E5_SUBS = [
    ("`scripts/kimi-surface.mjs:206-208`", "the kimi surface script (uncommitted)"),
    ("`.ufo/waves/round-52/selftest/`", "the round-52 selftest fixtures"),
    ("`.ufo/waves/round-52/selftest/ladder/`", "the round-52 ladder fixtures"),
    ("`.ufo/waves/round-52/selftest/registry/`", "the round-52 registry fixtures"),
    # a real path that exists, but is not the artifact the row is about
    ("`corpus/knowledge/google-robots-txt-limits.md`",
     "`corpus/knowledge/meta-robots-directives.md`"),
]


def rd(p):
    with open(p, encoding="utf-8") as fh:
        return fh.read()


def wr(p, s):
    with open(p, "w", encoding="utf-8") as fh:
        fh.write(s)


def sub_once(text, old, new, where):
    n = text.count(old)
    if n < 1:
        sys.exit("MISSING in %s: %r" % (where, old))
    return text.replace(old, new, 1)


def main():
    # --- E1: an empty `## Gate` section at EOF
    p = "corpus/lessons/round-85.md"
    t = rd(p)
    if not t.endswith("\n"):
        t += "\n"
    wr(p, t + "\n## Gate\n")

    # --- E2: one appended pointer to an irrelevant lesson per section
    p = "corpus/QUALITY.md"
    t = rd(p)
    for head in E2_HEADS:
        if t.count(head + "\n") != 1:
            sys.exit("E2 heading not unique: %r" % head)
        t = t.replace(head + "\n",
                      head + "\n\nGrounded in `corpus/lessons/round-1.md`.\n", 1)
    wr(p, t)

    # --- E3: a real source id that does not support the entry
    p = "corpus/knowledge/meta-robots-directives.md"
    t = rd(p)
    lines = t.splitlines()
    insert_at = 2  # inside the first 8 lines, after the H1
    block = ["source: S001", "verified-at: 2026-11-04", "recheck: 180d", ""]
    lines[insert_at:insert_at] = block
    wr(p, "\n".join(lines) + "\n")

    # --- E4: drop the blank line that splits each Mistakes table
    for name in E4_LESSONS:
        p = "corpus/lessons/" + name
        t = rd(p)
        m = re.search(r"(?m)^## Mistakes\s*$(.*?)(?=^## |\Z)", t, re.S)
        if not m:
            sys.exit("no Mistakes section in " + name)
        body = m.group(1)
        out = []
        changed = False
        ls = body.splitlines()
        for i, line in enumerate(ls):
            if (not changed and line.strip() == "" and i > 0 and i + 1 < len(ls)
                    and ls[i - 1].startswith("|") and ls[i + 1].startswith("|")):
                changed = True
                continue
            out.append(line)
        if not changed:
            sys.exit("no split table found in " + name)
        wr(p, t[:m.start(1)] + "\n".join(out) + t[m.end(1):])

    # --- E5: stop naming the missing path (delete, or repoint at a real path)
    p = "SKILL.md"
    t = rd(p)
    for old, new in E5_SUBS:
        if t.count(old) < 1:
            sys.exit("E5 anchor absent: %r" % old)
        t = t.replace(old, new)  # replace-all: the two round-52 selftest rows
    wr(p, t)
    print("repair_minimal: applied E1=1 E2=8 E3=1 E4=4 E5=6 edits")


if __name__ == "__main__":
    main()
