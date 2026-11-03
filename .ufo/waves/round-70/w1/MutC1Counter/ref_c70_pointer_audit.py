#!/usr/bin/env python3
"""Contract-faithful REFERENCE implementation of the round-70 C1 predicate.

Written by seat MutC1Counter because the executor counter artifact did not exist
when this probe reached its run step. It implements ONLY the frozen contract's
population (a)/(b)/(c), the dangling rules, and the annotation locus/cell rule.

Usage: python3 -B ref_c70_pointer_audit.py --root <repo> --revision <rev>
Exit 0 iff unannotated=0. Summary line carries unannotated=.
"""
import argparse
import os
import re
import subprocess
import sys

REPO_RE = re.compile(
    r"(?:^|[`(>|\s])((?:\.ufo|corpus|scripts|handoffs|considerthese)/[A-Za-z0-9_./-]+\.[A-Za-z0-9]{1,7})"
)
HOME_RE = re.compile(r"(?:^|[`(>|\s])(~/[A-Za-z0-9_./+-]+)")
TMP_RE = re.compile(r"(?:^|[`(>|\s])(/tmp/[A-Za-z0-9_.+-]+)")

SECTION = "## Pointer calibration (round 70)"


def show_scorecard(root, rev):
    r = subprocess.run(
        ["git", "-C", root, "cat-file", "blob", f"{rev}:SCORECARD.md"],
        capture_output=True,
    )
    if r.returncode != 0:
        sys.stderr.write("no SCORECARD.md at revision\n")
        return None
    return r.stdout.decode("utf-8", "replace")


def resolve_repo(root, rev, path):
    return (
        subprocess.run(
            ["git", "-C", root, "cat-file", "-e", f"{rev}:{path}"],
            capture_output=True,
        ).returncode
        == 0
    )


def annotation_rows(text):
    """First cells of table rows in the exact round-70 section.

    A row is a line whose stripped form starts with '|'. Content inside HTML
    comments is not rendered, so it is not a table row (lane append_guard
    precedent also excludes HTML comments).
    """
    lines = text.splitlines()
    body = []
    in_sec = False
    for ln in lines:
        if re.match(r"^#{1,2} ", ln):
            in_sec = ln.strip() == SECTION
            continue
        if in_sec:
            body.append(ln)

    cells = []
    in_comment = False
    for ln in body:
        s = ln.strip()
        if in_comment:
            if "-->" in s:
                s = s.split("-->", 1)[1].strip()
                in_comment = False
            else:
                continue
        while "<!--" in s:
            pre, rest = s.split("<!--", 1)
            if "-->" in rest:
                s = pre + rest.split("-->", 1)[1]
            else:
                in_comment = True
                s = pre
                break
        if s.startswith("|"):
            parts = [c.strip() for c in s.strip("|").split("|")]
            if parts and parts[0] and not re.fullmatch(r"[-: ]+", parts[0]):
                cells.append(parts[0])
    return cells


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", required=True)
    ap.add_argument("--revision", required=True)
    a = ap.parse_args()

    text = show_scorecard(a.root, a.revision)
    if text is None:
        return 2

    tokens = []
    seen = set()
    for rx in (REPO_RE, HOME_RE, TMP_RE):
        for m in rx.finditer(text):
            t = m.group(1)
            if t not in seen:
                seen.add(t)
                tokens.append(t)

    dangling = []
    for t in tokens:
        if t.startswith("/tmp/"):
            if not os.path.exists(t):
                dangling.append(t)
        elif t.startswith("~/"):
            if not os.path.exists(os.path.expanduser(t)):
                dangling.append(t)
        else:
            if not resolve_repo(a.root, a.revision, t):
                dangling.append(t)

    rows = set(annotation_rows(text))
    annotated = [t for t in dangling if t in rows]
    unannotated = [t for t in dangling if t not in rows]

    for t in unannotated:
        print(f"  unannotated_pointer={t}")
    print(
        "pointers=%d dangling=%d annotated=%d unannotated=%d met=%s"
        % (
            len(tokens),
            len(dangling),
            len(annotated),
            len(unannotated),
            "true" if not unannotated else "false",
        )
    )
    return 0 if not unannotated else 1


if __name__ == "__main__":
    sys.exit(main())
