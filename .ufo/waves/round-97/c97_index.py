#!/usr/bin/env python3
"""Round-97 C1 counter: coverage-index calibration (corpus/README.md vs corpus/knowledge/).

The lane's coverage map (`corpus/README.md`) is its self-assessment of what
ground it holds. CORPUS.md: "An index row is a claim. Write the row when the
file exists, not before." This counter counts mismatches between that
self-assessment and the committed tree, at one git revision, from committed
bytes only (git object reads with GIT_NO_REPLACE_OBJECTS=1, git resolved at
/usr/bin/git, never from PATH).

Population: every `corpus/knowledge/*.md` blob (direct children) at REV.

Index row: a GFM table row (line starts with `|`) of a table whose header row
has a cell equal to `Entry` (case-insensitive), outside fenced code blocks and
outside HTML comments. Its Entry cell names entries by the backticked token
`knowledge/<name>.md`.

An entry E is INDEXED iff at least one index row R satisfies all of:
  (a) R's Entry cell carries the backticked token `knowledge/E`;
  (b) every source id in E's `source:` line (first 15 lines; `S###` tokens,
      ranges `S036–S039` / `S036-S039` expanded) appears in R (same expansion);
  (c) R's other cells hold >= 8 words, of which >= 2 distinct words of >= 6
      letters (case-folded) also occur as words in E's own text.
  Known limit, declared before data: a row assembled from shuffled entry
  words passes (a)-(c); prose accuracy is judged by review, not by this
  counter (fixture `known-limit-shuffle`, expected exit 0). A row quoting the
  entry's own scope sentence is an accurate index claim and is admitted.
A DANGLING row token is a backticked `knowledge/X.md` in an index row's Entry
cell where X is not a blob at REV.

mismatches = unindexed entries + dangling tokens.
met <=> mismatches == 0.

Output line 1:
  C1v97 revision=<sha> entries=N indexed=K unindexed=U dangling=D
        mismatches=M met=true|false
line 2: JSON detail (per-entry reasons). Exit 0 iff met; 1 if not met;
2 on usage or git error (fails closed: a missing README or empty population
is exit 2, never a zero count).
--selftest builds fixture git repos under --work and runs THIS CLI on them as
subprocesses (the public path), asserting each fixture's exit code and fields.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import subprocess
import sys

GIT = "/usr/bin/git"
README = "corpus/README.md"
KDIR = "corpus/knowledge/"
MIN_WORDS = 8
MIN_SHARED = 2
SHARED_LEN = 6

ID_RANGE = re.compile(r"S(\d{3,})\s*[\u2013\u2014-]\s*S?(\d{3,})")
ID_ONE = re.compile(r"S(\d{3,})")
WORD = re.compile(r"[A-Za-z][A-Za-z0-9'-]*")
TOKEN = re.compile(r"`(?:corpus/)?knowledge/([^`/\s]+\.md)`")


class GitError(Exception):
    pass


def git_env():
    return {"PATH": "/usr/bin:/bin", "GIT_NO_REPLACE_OBJECTS": "1",
            "HOME": os.environ.get("HOME", "/"), "LC_ALL": "C",
            "GIT_CONFIG_NOSYSTEM": "1"}


def git(root, *args):
    p = subprocess.run([GIT, "-C", root, *args], capture_output=True,
                       env=git_env())
    if p.returncode != 0:
        raise GitError("git %s: rc=%d %s" % (" ".join(args), p.returncode,
                                             p.stderr.decode()[:200]))
    return p.stdout


def ids_in(text):
    out = set()
    for a, b in ID_RANGE.findall(text):
        lo, hi = int(a), int(b)
        if lo <= hi and hi - lo <= 50:
            width = len(a)
            out.update("S%0*d" % (width, n) for n in range(lo, hi + 1))
    out.update("S" + m for m in ID_ONE.findall(text))
    return out


def source_ids(text):
    for line in text.splitlines()[:15]:
        if line.startswith("source:"):
            return ids_in(line)
    return set()


def words(text):
    return [w.lower() for w in WORD.findall(text)]


def split_cells(line):
    s = line.strip()
    if s.startswith("|"):
        s = s[1:]
    if s.endswith("|"):
        s = s[:-1]
    return [c.strip() for c in s.split("|")]


def visible_lines(text):
    """Yield README lines outside fenced code and HTML comments."""
    in_fence = None
    in_comment = False
    for line in text.splitlines():
        st = line.lstrip()
        if in_comment:
            if "-->" in line:
                in_comment = False
            continue
        if in_fence:
            if st.startswith(in_fence):
                in_fence = None
            continue
        if st.startswith("```") or st.startswith("~~~"):
            in_fence = st[:3]
            continue
        if st.startswith("<!--"):
            if "-->" not in st[4:]:
                in_comment = True
            continue
        yield line


def index_rows(readme):
    rows = []
    entry_col = None
    prev_table = False
    for line in visible_lines(readme):
        if not line.lstrip().startswith("|"):
            entry_col = None
            prev_table = False
            continue
        cells = split_cells(line)
        if not prev_table:
            prev_table = True
            lowered = [c.lower() for c in cells]
            entry_col = lowered.index("entry") if "entry" in lowered else None
            continue
        if entry_col is None or all(re.fullmatch(r":?-{3,}:?", c or "---")
                                    for c in cells):
            continue
        if entry_col >= len(cells):
            continue
        rows.append((cells[entry_col],
                     [c for i, c in enumerate(cells) if i != entry_col], line))
    return rows


def audit(readme, entries):
    """entries: dict name -> text. Returns (detail dict)."""
    rows = index_rows(readme)
    unindexed = {}
    indexed = []
    for name in sorted(entries):
        text = entries[name]
        need = source_ids(text)
        body_words = set(words(text))
        reasons = []
        ok = False
        for entry_cell, others, line in rows:
            if name not in TOKEN.findall(entry_cell):
                continue
            have = ids_in(line)
            missing = sorted(need - have)
            ow = words(" ".join(others))
            shared = {w for w in ow if len(w) >= SHARED_LEN and w in body_words}
            if missing:
                reasons.append("row lacks ids %s" % ",".join(missing))
            elif len(ow) < MIN_WORDS:
                reasons.append("row coverage %d words < %d" % (len(ow), MIN_WORDS))
            elif len(shared) < MIN_SHARED:
                reasons.append("row shares %d words with entry < %d"
                               % (len(shared), MIN_SHARED))
            else:
                ok = True
                break
        if ok:
            indexed.append(name)
        else:
            unindexed[name] = reasons or ["no index row"]
    dangling = sorted({t for cell, _, _ in rows for t in TOKEN.findall(cell)
                       if t not in entries})
    return {"indexed": indexed, "unindexed": unindexed, "dangling": dangling,
            "rows": len(rows)}


def load(root, rev):
    sha = git(root, "rev-parse", "--verify", "%s^{commit}" % rev).decode().strip()
    readme = git(root, "show", "%s:%s" % (sha, README)).decode("utf-8", "replace")
    listing = git(root, "ls-tree", "-z", sha, KDIR).decode("utf-8", "replace")
    entries = {}
    for rec in listing.split("\0"):
        if not rec:
            continue
        meta, _, path = rec.partition("\t")
        kind = meta.split()[1] if len(meta.split()) > 1 else ""
        name = path[len(KDIR):]
        if kind != "blob" or "/" in name or not name.endswith(".md"):
            continue
        entries[name] = git(root, "show", "%s:%s" % (sha, path)).decode(
            "utf-8", "replace")
    if not entries:
        raise GitError("empty population under %s at %s" % (KDIR, sha))
    return sha, readme, entries


def run(root, rev):
    try:
        sha, readme, entries = load(root, rev)
    except GitError as e:
        print("C1v97 revision=%s error met=false" % rev)
        print(json.dumps({"error": str(e)}, sort_keys=True))
        return 2
    d = audit(readme, entries)
    mism = len(d["unindexed"]) + len(d["dangling"])
    met = mism == 0
    print("C1v97 revision=%s entries=%d indexed=%d unindexed=%d dangling=%d "
          "mismatches=%d met=%s" % (sha, len(entries), len(d["indexed"]),
                                    len(d["unindexed"]), len(d["dangling"]),
                                    mism, str(met).lower()))
    print(json.dumps({"unindexed": d["unindexed"], "dangling": d["dangling"],
                      "index_rows": d["rows"]}, sort_keys=True))
    return 0 if met else 1


# ---------------------------------------------------------------- selftest

ENTRY_A = ("---\nsource: S900 (example), S901\nverified-at: 2026-11-05\n"
           "recheck: 180d\n---\n\n# Revalidation fixture entry\n\n"
           "The validator exchange decides conditional headers for stored "
           "responses during revalidation.\n")
ENTRY_B = ("source: S902–S904 (range)\n\n# Sitemap fixture entry\n\n"
           "Sitemap containers and location scoping for crawlers.\n")
HEAD = "# corpus\n\n## Coverage map\n\n| Area | Entry | Coverage |\n|---|---|---|\n"
ROW_A = ("| Revalidation | `knowledge/a.md` (S900, S901) | which conditional "
         "headers a validator exchange sends for stored responses |\n")
ROW_B = ("| Sitemaps | `knowledge/b.md` (S902–S904) | sitemap containers and "
         "location scoping rules that crawlers apply to sitemap files |\n")

FIXTURES = [
    # name, readme, entries, want_rc, want_fields
    ("positive", HEAD + ROW_A + ROW_B, {"a.md": ENTRY_A, "b.md": ENTRY_B},
     0, {"unindexed": "0", "dangling": "0"}),
    ("do-nothing-missing-row", HEAD + ROW_A, {"a.md": ENTRY_A, "b.md": ENTRY_B},
     1, {"unindexed": "1"}),
    ("junk-row-path-only", HEAD + ROW_A + "| x | `knowledge/b.md` | y |\n",
     {"a.md": ENTRY_A, "b.md": ENTRY_B}, 1, {"unindexed": "1"}),
    ("junk-row-ids-no-shared-words", HEAD + ROW_A +
     "| x | `knowledge/b.md` (S902–S904) | lorem ipsum dolor amet consectetur "
     "adipiscing elit sedeiusmod tempor |\n",
     {"a.md": ENTRY_A, "b.md": ENTRY_B}, 1, {"unindexed": "1"}),
    ("row-missing-one-id", HEAD + ROW_B + ROW_A.replace("S900, S901", "S900"),
     {"a.md": ENTRY_A, "b.md": ENTRY_B}, 1, {"unindexed": "1"}),
    ("row-inside-fence", HEAD + ROW_A + "```\n" + ROW_B + "```\n",
     {"a.md": ENTRY_A, "b.md": ENTRY_B}, 1, {"unindexed": "1"}),
    ("row-inside-comment", HEAD + ROW_A + "<!--\n" + ROW_B + "-->\n",
     {"a.md": ENTRY_A, "b.md": ENTRY_B}, 1, {"unindexed": "1"}),
    ("row-in-prose-not-table", HEAD + ROW_A + "\n" + ROW_B.lstrip("| "),
     {"a.md": ENTRY_A, "b.md": ENTRY_B}, 1, {"unindexed": "1"}),
    ("row-in-table-without-entry-header", HEAD + ROW_A +
     "\n| Area | File | Coverage |\n|---|---|---|\n" + ROW_B,
     {"a.md": ENTRY_A, "b.md": ENTRY_B}, 1, {"unindexed": "1"}),
    ("token-outside-entry-cell", HEAD + ROW_A +
     "| `knowledge/b.md` (S902–S904) | elsewhere | sitemap containers and "
     "location scoping rules that crawlers apply |\n",
     {"a.md": ENTRY_A, "b.md": ENTRY_B}, 1, {"unindexed": "1"}),
    ("dangling-row", HEAD + ROW_A + ROW_B +
     "| Gone | `knowledge/gone.md` | an index row naming a file that was never "
     "committed anywhere |\n",
     {"a.md": ENTRY_A, "b.md": ENTRY_B}, 1, {"dangling": "1", "unindexed": "0"}),
    ("empty-population", HEAD, {}, 2, {}),
    # declared known limit: shuffled entry words pass (a)-(c); review judges prose
    ("known-limit-shuffle", HEAD + ROW_A +
     "| Sitemaps | `knowledge/b.md` (S902–S904) | crawlers scoping location "
     "sitemap containers fixture entry range and for |\n",
     {"a.md": ENTRY_A, "b.md": ENTRY_B}, 0, {"unindexed": "0"}),
]


def make_repo(d, readme, entries, uncommitted_extra=None):
    os.makedirs(d)
    git(d, "init", "-q")
    top = git(d, "rev-parse", "--show-toplevel").decode().strip()
    if os.path.realpath(top) != os.path.realpath(d):
        raise GitError("fixture toplevel mismatch %s" % top)
    os.makedirs(os.path.join(d, KDIR))
    with open(os.path.join(d, README), "w") as fh:
        fh.write(readme)
    for n, t in entries.items():
        with open(os.path.join(d, KDIR, n), "w") as fh:
            fh.write(t)
    if not entries:
        with open(os.path.join(d, KDIR, "keep.json"), "w") as fh:
            fh.write("{}\n")
    git(d, "add", "-A")
    git(d, "-c", "user.name=c97-fixture", "-c", "user.email=fixture@c97.invalid",
        "commit", "-qm", "fixture")
    if uncommitted_extra:
        with open(os.path.join(d, README), "a") as fh:
            fh.write(uncommitted_extra)


def selftest(work):
    base = os.path.join(os.path.abspath(work), "c97-selftest-%d" % os.getpid())
    ok = 0
    total = 0
    try:
        os.makedirs(base)
        fixtures = list(FIXTURES)
        # working-tree forgery: the row exists only uncommitted; counter reads REV
        fixtures.append(("uncommitted-row", HEAD + ROW_A,
                         {"a.md": ENTRY_A, "b.md": ENTRY_B}, 1,
                         {"unindexed": "1"}, ROW_B))
        for fx in fixtures:
            name, readme, entries, want_rc, want = fx[:5]
            extra = fx[5] if len(fx) > 5 else None
            total += 1
            d = os.path.join(base, name)
            make_repo(d, readme, entries, extra)
            p = subprocess.run([sys.executable, "-B", os.path.abspath(__file__),
                                "--root", d, "--revision", "HEAD",
                                "--work", base], capture_output=True)
            line = p.stdout.decode().splitlines()[0] if p.stdout else ""
            fields = dict(kv.split("=", 1) for kv in line.split()[1:] if "=" in kv)
            good = p.returncode == want_rc and all(fields.get(k) == v
                                                   for k, v in want.items())
            if good:
                ok += 1
            else:
                print("selftest FAIL %s: rc=%d want=%d line=%s"
                      % (name, p.returncode, want_rc, line))
        print("selftest %d/%d fixtures scored as declared via the public CLI"
              % (ok, total))
        return 0 if ok == total else 1
    finally:
        shutil.rmtree(base, ignore_errors=True)


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", default=".")
    ap.add_argument("--revision")
    ap.add_argument("--work", required=True)
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args(argv)
    if a.selftest:
        return selftest(a.work)
    if not a.revision:
        print("C1v97 revision=? error met=false")
        print(json.dumps({"error": "--revision required"}))
        return 2
    return run(os.path.abspath(a.root), a.revision)


if __name__ == "__main__":
    sys.exit(main())
