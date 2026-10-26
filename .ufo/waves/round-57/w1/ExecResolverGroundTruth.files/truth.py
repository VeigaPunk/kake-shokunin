#!/usr/bin/env python3
"""Ground-truth history table for claim C2 (kake round-57, seat ExecResolverGroundTruth).

Hand-built from git plumbing plus two regexes.  It deliberately does NOT import or
invoke scripts/id_resolver.py (the C2 tool under test): the point of this seat is an
independent table the resolver can be compared against.

Definitions used (fixed before the first run, per the assignment):

  rows     count of registry rows at a revision: lines matching
           ``^ {0,3}\\|[ \\t]*S[0-9]{3,} `` in ``corpus/SOURCES.md`` (the assignment's
           grep, anchored at up to three leading spaces).
  cited    distinct word-bounded ``S[0-9]{3,}`` ids appearing in ``corpus/knowledge/*.md``
           at that revision (``git grep -w -o``: git's word class is [A-Za-z0-9_], so a
           CJK neighbour, a bracket or punctuation still terminates the token and
           ``S367a`` / ``XS367`` do not count).  Occurrence totals are reported too.
  dangling cited ids with no row in the registry at that revision.

Usage:
  python3 -B truth.py history          # the 60-revision table + repair attribution
  python3 -B truth.py owners [<rev>]   # dangling ids at <rev>, sibling-registry owners

Read-only: only ``git show`` / ``git grep`` / ``git log`` are run.  Nothing is written.
"""
import re
import subprocess
import sys

LANE = "/home/vgpnk/Projects/shokunin/kake-shokunin"
SIBLINGS = [
    "audio", "chousa", "game-dev-2d", "game-dev-3d", "kagi", "kaidoku", "kama",
    "kasegi", "kengaku", "kotoba", "kotodama", "kumitate", "lore", "mado", "mori",
    "revenger", "souji", "tabi", "tameshi", "tsukuroi",
]
ROW_RE = re.compile(r"^ {0,3}\|[ \t]*S[0-9]{3,} ")
ROW_ID_RE = re.compile(r"^\|?[ \t]*\|?[ \t]*(S[0-9]{3,}) ")
URL_RE = re.compile(r"https?://[^\s;|)]+")
PATHSPEC = ["corpus/SOURCES.md", "corpus/knowledge"]
DEFAULT_OWNER_REV = "3994101dba28896830604fd0b08c7f00faca8ed6"


def git(*args, cwd=LANE):
    """Run a read-only git command; return stdout ('' on the no-match exit 1)."""
    proc = subprocess.run(["git", "-C", cwd, *args], capture_output=True, text=True)
    if proc.returncode not in (0, 1):
        raise SystemExit("git %s failed: %s" % (" ".join(args), proc.stderr.strip()))
    return proc.stdout


def revision_list(limit=60):
    """[(sha, date, subject)] newest first, exactly the assignment's command."""
    out = git("log", "--first-parent", "--format=%H%x09%ad%x09%s", "--date=short",
              "--", *PATHSPEC)
    revs = []
    for line in out.splitlines():
        if not line.strip():
            continue
        sha, date, subject = line.split("\t", 2)
        revs.append((sha, date, subject))
        if len(revs) == limit:
            break
    return revs


def registry_rows(rev):
    """[(id, source_cell, whole_line)] for every registry row at ``rev``."""
    rows = []
    for line in git("show", "%s:corpus/SOURCES.md" % rev).splitlines():
        if not ROW_RE.match(line):
            continue
        cells = line.split("|")
        rid = cells[1].strip()
        source_cell = cells[2] if len(cells) > 2 else ""
        rows.append((rid, source_cell, line))
    return rows


def cited(rev):
    """(distinct id -> [file:line], occurrence_count) for corpus/knowledge/*.md at rev."""
    hits = {}
    total = 0
    out = git("grep", "-w", "-o", "-E", "S[0-9]{3,}", rev, "--", "corpus/knowledge/*.md")
    for line in out.splitlines():
        if not line.strip():
            continue
        # git grep prefixes "<rev>:" when a tree-ish is given; drop it so the
        # location is the in-tree path the report cites.
        if line.startswith(rev + ":"):
            line = line[len(rev) + 1:]
        where, rid = line.rsplit(":", 1)
        hits.setdefault(rid, []).append(where)
        total += 1
    return hits, total


def snapshot(rev):
    rows = registry_rows(rev)
    row_ids = {rid for rid, _, _ in rows}
    hits, total = cited(rev)
    dangling = sorted(set(hits) - row_ids)
    return {
        "rev": rev,
        "rows": len(rows),
        "row_ids": row_ids,
        "cited_ids": set(hits),
        "cited_distinct": len(hits),
        "cited_occurrences": total,
        "hits": hits,
        "dangling": dangling,
    }


def normalise(url):
    url = url.strip().rstrip(".,)")
    url = re.sub(r"^https?://", "", url)
    return url.rstrip("/")


def history():
    revs = revision_list()
    snaps = [snapshot(rev) for rev, _, _ in revs]
    by_rev = {s["rev"]: s for s in snaps}

    print("HISTORY TABLE (newest first, %d revisions)" % len(snaps))
    print("rev\tdate\tsubject\trows\tcited\tdangling")
    for (rev, date, subject), s in zip(revs, snaps):
        print("%s\t%s\t%s\t%d\t%d\t%s" % (
            rev[:7], date, subject, s["rows"], s["cited_distinct"],
            ",".join(s["dangling"]) or "-"))

    print()
    print("CITATION OCCURRENCES (raw token count, same revisions)")
    for (rev, _, _), s in zip(revs, snaps):
        print("%s\t%d" % (rev[:7], s["cited_occurrences"]))

    print()
    print("REPAIR ATTRIBUTION (chronological: oldest first)")
    chrono = list(reversed(snaps))
    for i, s in enumerate(chrono):
        if not s["dangling"]:
            continue
        prev = chrono[i - 1] if i else None
        cleared = []
        for j in range(i + 1, len(chrono)):
            nxt = chrono[j]
            gone = [d for d in s["dangling"] if d not in nxt["dangling"]]
            if gone:
                for d in gone:
                    how = "row added" if d in nxt["row_ids"] else "citation removed"
                    cleared.append("%s (%s)" % (d, how))
                print("%s %s dangling=%s -> repaired at %s %s : %s" % (
                    s["rev"][:7], "was" if prev is None or not prev["dangling"] else "still",
                    ",".join(s["dangling"]), nxt["rev"][:7],
                    "(next revision)" if j == i + 1 else "(+%d revisions)" % (j - i),
                    ", ".join(cleared)))
                break
        else:
            print("%s dangling=%s -> unrepaired inside the 60-revision window" % (
                s["rev"][:7], ",".join(s["dangling"])))


def named_urls(rev, path, rid):
    """URLs the citing file names *for this id*, with the provenance of the find.

    Search order: the citing line, then the enclosing bullet block (contiguous
    non-blank lines), then the file's frontmatter ``source:`` line.  The last is the
    file's own source row, not the dangling id's document, and is labelled as such.
    """
    body = git("show", "%s:%s" % (rev, path)).splitlines()
    for n, line in enumerate(body):
        if re.search(r"(?<![A-Za-z0-9_])%s(?![A-Za-z0-9_])" % rid, line):
            urls = URL_RE.findall(line)
            if urls:
                return urls, "line %d" % (n + 1)
            lo = n
            while lo > 0 and body[lo - 1].strip():
                lo -= 1
            hi = n
            while hi + 1 < len(body) and body[hi + 1].strip():
                hi += 1
            urls = URL_RE.findall("\n".join(body[lo:hi + 1]))
            if urls:
                return urls, "bullet block lines %d-%d" % (lo + 1, hi + 1)
    for n, line in enumerate(body[:6]):
        if line.startswith("source:"):
            return URL_RE.findall(line), "frontmatter source: (line %d)" % (n + 1)
    return [], "none"


def lane_row_url(rev, rid):
    for row_id, source_cell, _ in registry_rows(rev):
        if row_id == rid:
            return URL_RE.findall(source_cell)
    return []


def owners(rev=DEFAULT_OWNER_REV):
    snap = snapshot(rev)
    head = git("rev-parse", "HEAD").strip()
    print("OWNER ANALYSIS at %s (rows=%d cited=%d)" % (
        rev[:7], snap["rows"], snap["cited_distinct"]))
    print("lane HEAD %s" % head[:7])
    print()
    for rid in snap["dangling"]:
        files = sorted({where.rsplit(":", 1)[0] for where in snap["hits"][rid]})
        print("DANGLING %s" % rid)
        for path in files:
            urls, how = named_urls(rev, path, rid)
            print("  citing file %s" % path)
            print("    url named for the id: %s [%s]" % (", ".join(urls) or "NONE", how))
        own = lane_row_url("HEAD", rid)
        print("  lane row at HEAD: %s" % (", ".join(own) or "NO ROW AT HEAD"))
        owners_found = 0
        for lane in SIBLINGS:
            cwd = "/home/vgpnk/Projects/shokunin/%s-shokunin" % lane
            out = git("show", "HEAD:corpus/SOURCES.md", cwd=cwd)
            for line in out.splitlines():
                if not ROW_RE.match(line):
                    continue
                cells = line.split("|")
                if len(cells) < 3 or cells[1].strip() != rid:
                    continue
                owners_found += 1
                sib_urls = URL_RE.findall(cells[2])
                same = [u for u in sib_urls if any(
                    normalise(u) == normalise(v) for v in own)]
                print("  sibling %s-shokunin row url: %s" % (
                    lane, ", ".join(sib_urls) or "NO URL IN SOURCE CELL"))
                print("    same document as lane row: %s" % ("YES " + ", ".join(same) if same else "NO"))
        if not owners_found:
            print("  no sibling registry holds a row with this id at its HEAD")
        print()


def main(argv):
    mode = argv[1] if len(argv) > 1 else "history"
    if mode == "history":
        history()
    elif mode == "owners":
        owners(argv[2] if len(argv) > 2 else DEFAULT_OWNER_REV)
    else:
        raise SystemExit("usage: truth.py {history|owners [rev]}")


if __name__ == "__main__":
    main(sys.argv)
