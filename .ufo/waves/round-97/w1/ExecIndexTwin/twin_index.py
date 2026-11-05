#!/usr/bin/env python3
"""ExecIndexTwin: independent second implementation of the round-97 C1 predicate.

Written from the docstring of .ufo/waves/round-97/c97_index.py (lines 1-45)
ONLY; the counter's code was not read. Stdlib python. Reads committed bytes
via /usr/bin/git (GIT_NO_REPLACE_OBJECTS=1) at one revision.

Readings this twin chose where the docstring allows more than one (each is
labeled READING in comments, so a disagreement can name both sides):
  R1 fences: a line whose stripped form starts with ``` or ~~~ toggles fence state.
  R2 header match: a pipe line whose immediately following pipe line is a
     GFM delimiter row (every non-empty cell is only dashes/colons) opens a
     table; the header "has a cell equal to Entry" means some cell, stripped
     of surrounding backticks and whitespace, case-folds to "entry".
  R3 table membership: body rows are the consecutive pipe lines after the
     delimiter row; a blank or non-pipe line ends the table.
  R4 source line: a line in the entry's first 15 lines whose stripped form
     starts with the literal `source:` (case-sensitive); ids are S### tokens
     and S###[-/]S### ranges (en dash or hyphen), ranges expanded.
  R5 (c) words: tokens are maximal [A-Za-z0-9]+ runs of the row's other
     cells (all cells except the Entry column, joined); total >= 8 and
     >= 2 DISTINCT tokens whose alphabetic length >= 6 case-fold to a token
     occurring in the entry's full text (same tokenization, case-folded).
  R6 row-state exclusion is evaluated at the row line itself (fence/comment
     state when the row line is reached).
Output: per-entry lines "<name>\ttrue|false", then the same line-1/line-2
summary shape as the counter (summary + JSON detail), exit 0 iff
mismatches==0, 1 if not met, 2 on usage/git error (fails closed).
"""

import argparse
import json
import os
import re
import subprocess
import sys

GIT = "/usr/bin/git"
ENTRY_RE = re.compile(r"`(knowledge/[^`\s]+\.md)`")
RANGE_RE = re.compile(r"S(\d{3})\s*[-\u2013]\s*S(\d{3})")
SINGLE_RE = re.compile(r"S\d{3}")
WORD_RE = re.compile(r"[A-Za-z0-9]+")


def git_out(root, rev, path):
    env = dict(os.environ)
    env["GIT_NO_REPLACE_OBJECTS"] = "1"
    p = subprocess.run([GIT, "show", f"{rev}:{path}"], cwd=root, env=env,
                       stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if p.returncode != 0:
        return None, p.returncode
    return p.stdout.decode("utf-8", "replace"), 0


def git_ls(root, rev, pathspec):
    env = dict(os.environ)
    env["GIT_NO_REPLACE_OBJECTS"] = "1"
    p = subprocess.run([GIT, "ls-tree", rev, "--", pathspec], cwd=root, env=env,
                       stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if p.returncode != 0:
        return None
    pop = []
    for line in p.stdout.decode("utf-8", "replace").splitlines():
        meta, _, path = line.partition("\t")
        parts = meta.split()
        name = path.rsplit("/", 1)[-1]
        if len(parts) >= 3 and parts[1] == "blob" and name.endswith(".md"):
            pop.append(name)
    return pop


def split_cells(line):
    return [c.strip() for c in line.strip().strip("|").split("|")]


def is_delimiter(line):
    if not line.lstrip().startswith("|"):
        return False
    cells = split_cells(line)
    nonempty = [c for c in cells if c]
    return bool(nonempty) and all(re.fullmatch(r":?-{1,}:?", c) for c in nonempty)


def norm_header_cell(cell):
    return cell.strip().strip("`").strip().casefold()


def scan_readme(text):
    """Return (rows, dangling_tokens): rows = list of (entry_col, entry_cell,
    row_text, other_text) for pipe rows of Entry-header tables, outside
    fences/comments (state at the row line, R6)."""
    lines = text.splitlines()
    rows = []
    fence = False
    in_comment = False
    i = 0
    n = len(lines)
    while i < n:
        raw = lines[i]
        stripped = raw.strip()
        # fence state (R1)
        if stripped.startswith("```") or stripped.startswith("~~~"):
            fence = not fence
            i += 1
            continue
        # html comment state
        if "<!--" in raw:
            if "-->" in raw.split("<!--", 1)[1]:
                pass  # opens and closes on one line
            else:
                in_comment = True
        if in_comment and "-->" in raw:
            in_comment = False
            i += 1
            continue
        if in_comment:
            i += 1
            continue
        is_pipe = raw.lstrip().startswith("|")
        # table opener (R2/R3): header pipe line followed by delimiter
        if is_pipe and not fence and i + 1 < n and is_delimiter(lines[i + 1]) \
                and lines[i + 1].lstrip().startswith("|"):
            header_cells = split_cells(raw)
            entry_col = None
            for ci, cell in enumerate(header_cells):
                if norm_header_cell(cell) == "entry":
                    entry_col = ci
                    break
            j = i + 2
            while j < n and lines[j].lstrip().startswith("|") and lines[j].strip():
                rowline = lines[j]
                st = rowline.strip()
                if st.startswith("```") or st.startswith("~~~"):
                    fence = not fence
                    j += 1
                    continue
                if "<!--" in rowline:
                    if "-->" not in rowline.split("<!--", 1)[1]:
                        in_comment = True
                if in_comment and "-->" in rowline:
                    in_comment = False
                    j += 1
                    continue
                if in_comment or fence:
                    j += 1
                    continue
                if entry_col is not None:
                    cells = split_cells(rowline)
                    entry_cell = cells[entry_col] if entry_col < len(cells) else ""
                    other = [c for ci, c in enumerate(cells) if ci != entry_col]
                    rows.append((entry_col, entry_cell, rowline, " ".join(other)))
                j += 1
            i = j
            continue
        i += 1
    return rows


def expand_ids(text):
    ids = set()
    for m in RANGE_RE.finditer(text):
        a, b = int(m.group(1)), int(m.group(2))
        if a <= b:
            for k in range(a, b + 1):
                ids.add(f"S{k:03d}")
    ids.update(SINGLE_RE.findall(text))
    return ids


def source_ids(entry_text):
    for line in entry_text.splitlines()[:15]:
        s = line.strip()
        if s.startswith("source:"):
            return expand_ids(s)
    return set()


def word_set(text):
    return set(t.casefold() for t in WORD_RE.findall(text))


def row_word_ok(other_text, entry_words):
    toks = WORD_RE.findall(other_text)
    if len(toks) < 8:
        return False, len(toks), 0
    distinct = set()
    for t in toks:
        alpha = re.sub(r"[^A-Za-z]", "", t)
        if len(alpha) >= 6 and t.casefold() in entry_words:
            distinct.add(t.casefold())
    return len(distinct) >= 2, len(toks), len(distinct)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", required=True)
    ap.add_argument("--revision", required=True)
    ap.add_argument("--work", default=None)
    args = ap.parse_args()

    if args.work:
        os.makedirs(args.work, exist_ok=True)

    pop = git_ls(args.root, args.revision, "corpus/knowledge/")
    if pop is None:
        print("twin git error listing population", file=sys.stderr)
        sys.exit(2)
    readme, rc = git_out(args.root, args.revision, "corpus/README.md")
    if rc != 0:
        print("twin git error reading corpus/README.md", file=sys.stderr)
        sys.exit(2)
    entries = {}
    for name in pop:
        blob, rc = git_out(args.root, args.revision, f"corpus/knowledge/{name}")
        if rc != 0:
            print(f"twin git error reading corpus/knowledge/{name}", file=sys.stderr)
            sys.exit(2)
        entries[name] = blob

    rows = scan_readme(readme)
    popset = set(pop)
    dangling = set()
    indexed = {}
    for name in sorted(pop):
        indexed[name] = False
    for entry_col, entry_cell, rowline, other in rows:
        row_ids = expand_ids(rowline)
        for tok in ENTRY_RE.findall(entry_cell):
            name = tok[len("knowledge/"):]
            if name not in popset:
                dangling.add(tok)
                continue
            if indexed[name]:
                continue
            ewords = word_set(entries[name])
            if source_ids(entries[name]) <= row_ids:
                ok, total, distinct = row_word_ok(other, ewords)
                if ok:
                    indexed[name] = True
    for name in sorted(pop):
        print(f"{name}\t{'true' if indexed[name] else 'false'}")

    unindexed = {n: ["twin: no qualifying row"] for n in sorted(pop) if not indexed[n]}
    mismatches = len(unindexed) + len(dangling)
    met = mismatches == 0
    print(f"TWIN revision={args.revision} entries={len(pop)} "
          f"indexed={sum(indexed.values())} unindexed={len(unindexed)} "
          f"dangling={len(dangling)} mismatches={mismatches} "
          f"met={'true' if met else 'false'}")
    print(json.dumps({"unindexed": unindexed, "dangling": sorted(dangling)},
                     sort_keys=True))
    sys.exit(0 if met else 1)


if __name__ == "__main__":
    main()
