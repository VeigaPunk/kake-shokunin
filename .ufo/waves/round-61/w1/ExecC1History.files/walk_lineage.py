#!/usr/bin/env python3
"""Walk first-parent history of the frozen 144-file receipt population to base rev.

Implements the contract C1 rules literally:
  receipt grammar : (?im)^\s*#\s*receipt\s*:  OR  EXIT=  OR  ^VERDICT:
  result span     : the set of lines matching
                    (?im)(^#\s*receipt\s*:|revision\s*[:=]|EXIT\s*=|met\s*=|conditions_passed|
                          cases_passed|findings\s*=|scores_held|members\s*=)
  event candidate : first-parent commit C (after the adding commit) whose blob for the path
                    differs from C's first parent's blob
  rewrite         : result span(child) != result span(parent)
  pending_filled  : first version's span holds the word pending, a later version's span does not
Outputs events.tsv (path, commit, kind, parent_commit, changed_result_lines) + walk.json.

Re-run: set LANE to any clone of the lane (`git clone -q --shared <lane> <dir>`) and POP to the frozen
population list; the clone is read only. As run by ExecC1History the clone lived in scratch and is gone.
"""
import json, os, re, subprocess, sys

LANE = "/fast/scratch/hyaku/kake-r61/ExecC1History/clone"
BASE = "9f07731a873585e655a6518233ea39f5d9fb8204"
POP = "/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-61/controls/population-144.txt"
OUT = "/fast/scratch/hyaku/kake-r61/ExecC1History"

GRAMMAR = re.compile(r"(?im)^\s*#\s*receipt\s*:|EXIT=|^VERDICT:")
SPAN = re.compile(r"(?im)^#\s*receipt\s*:|revision\s*[:=]|EXIT\s*=|met\s*=|conditions_passed|"
                  r"cases_passed|findings\s*=|scores_held|members\s*=")
PENDING = re.compile(r"pending", re.I)

def git(*args, check=True):
    r = subprocess.run(["git", "-C", LANE] + list(args), capture_output=True)
    if check and r.returncode != 0:
        raise RuntimeError("git %s -> %d: %s" % (" ".join(args), r.returncode, r.stderr[:300]))
    return r

with open(POP, "rb") as fh:
    paths = [ln.strip() for ln in fh.read().decode().splitlines() if ln.strip()]
assert len(paths) == 144, len(paths)

chain = git("rev-list", "--first-parent", "--reverse", BASE).stdout.decode().split()
pos = {c: i for i, c in enumerate(chain)}

blobmap = {}
for c in chain:
    m = {}
    for ln in git("ls-tree", "-r", "--full-tree", c, "--", *paths).stdout.decode().splitlines():
        meta, p = ln.split("\t", 1)
        f = meta.split()
        if f[1] == "blob":
            m[p] = f[2]
    blobmap[c] = m

cache = {}
def text_of(sha):
    if sha not in cache:
        cache[sha] = git("cat-file", "blob", sha).stdout.decode("utf-8", "replace")
    return cache[sha]

def span(text):
    return {ln for ln in text.splitlines() if SPAN.search(ln)}

events = []
non_receipt, receipts = [], []
stats = {"deleted_then_readded": [], "candidates": 0, "span_unchanged": []}

for path in paths:
    prev_sha, first_commit, first_text = None, None, None
    pending_origin = False
    pending_resolved = False
    seen_deleted = False
    for c in chain:
        sha = blobmap[c].get(path)
        if sha is None:
            if first_commit is not None and prev_sha is not None:
                seen_deleted = True
            prev_sha = None
            continue
        if first_commit is None:
            first_commit, first_text = c, text_of(sha)
            pending_origin = any(PENDING.search(ln) for ln in span(first_text))
        elif prev_sha != sha:
            stats["candidates"] += 1
            if seen_deleted:
                stats["deleted_then_readded"].append([path, c])
            s_child, s_parent = span(text_of(sha)), span(text_of(prev_sha)) if prev_sha else set()
            if s_child != s_parent:
                difflines = ["-" + x.strip() for x in sorted(s_parent - s_child)]
                difflines += ["+" + x.strip() for x in sorted(s_child - s_parent)]
                kind = "rewrite"
                if pending_origin and not pending_resolved and not any(PENDING.search(x) for x in s_child):
                    kind = "pending_filled"
                    pending_resolved = True
                events.append(dict(path=path, commit=c, kind=kind,
                                   parent=git("rev-parse", "%s^" % c).stdout.decode().strip(),
                                   diff=" | ".join(difflines),
                                   child_span=sorted(s_child), parent_span=sorted(s_parent)))
            else:
                stats["span_unchanged"].append([path, c])
        prev_sha = sha
    if first_text is None:
        stats.setdefault("missing_at_base", []).append(path)
        continue
    g = GRAMMAR.search(first_text)
    (receipts if g else non_receipt).append(path if g else path)
    if g:
        receipts[-1] = dict(path=path, first_commit=first_commit, grammar=g.group(0))

events.sort(key=lambda e: pos[e["commit"]])
with open(os.path.join(OUT, "events.tsv"), "w") as fh:
    fh.write("path\tcommit\tkind\tparent_commit\tchanged_result_lines\n")
    for e in events:
        fh.write("\t".join([e["path"], e["commit"], e["kind"], e["parent"], e["diff"]]) + "\n")

json.dump(dict(chain_len=len(chain), receipts=receipts, non_receipt=non_receipt,
               events=events, stats=stats), open(os.path.join(OUT, "walk.json"), "w"), indent=1)
print("receipts=%d non_receipt=%d events=%d candidates=%d span_unchanged=%d deleted_readded=%d" % (
    len(receipts), len(non_receipt), len(events), stats["candidates"],
    len(stats["span_unchanged"]), len(stats["deleted_then_readded"])), file=sys.stderr)
