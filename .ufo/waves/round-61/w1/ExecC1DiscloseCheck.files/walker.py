#!/usr/bin/env python3
"""Independent C1 receipt-lineage event derivation (cross-check walker).

Implements the contract.md C1 rules exactly:
- receipt detection on FIRST committed version (full first-parent history to REV)
- receipt grammar: (?im)^\s*#\s*receipt\s*: | EXIT= | ^VERDICT:
- result span lines: (?im)(^#\s*receipt\s*:|revision\s*[:=]|EXIT\s*=|met\s*=|
  conditions_passed|cases_passed|findings\s*=|scores_held|members\s*=)
- rewrite: event candidate (blob differs from first parent's) with changed span
- pending_filled: first span has 'pending' (ci), later span does not
Read-only: git cat-file / rev-list / ls-tree only.
"""
import json, re, subprocess, sys

ROOT = "/fast/scratch/hyaku/kake-r61/ExecC1DiscloseCheck/lane"
REV = "9f07731a873585e655a6518233ea39f5d9fb8204"
POP = "/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-61/controls/population-144.txt"

def git(*args, binary=False):
    r = subprocess.run(["git", "-C", ROOT] + list(args), capture_output=True)
    if r.returncode != 0:
        raise RuntimeError(f"git {' '.join(args)} -> {r.returncode}: {r.stderr.decode()[:200]}")
    return r.stdout if binary else r.stdout.decode("utf-8", "replace")

GRAMMAR = re.compile(r"(?im)^\s*#\s*receipt\s*:|EXIT=|^VERDICT:")
SPAN = re.compile(r"(?im)(^#\s*receipt\s*:|revision\s*[:=]|EXIT\s*=|met\s*=|conditions_passed|cases_passed|findings\s*=|scores_held|members\s*=)")
PEND = re.compile(r"pending", re.I)

paths = [l.strip() for l in open(POP) if l.strip()]
assert len(paths) == 144, len(paths)

chain = git("rev-list", "--first-parent", "--reverse", REV).split()
parent_of = {chain[i]: chain[i-1] for i in range(1, len(chain))}
print(f"first-parent chain: {len(chain)} commits to {REV[:8]}", file=sys.stderr)

def blob_in(commit, path):
    r = subprocess.run(["git", "-C", ROOT, "ls-tree", commit, "--", path],
                       capture_output=True)
    line = r.stdout.decode("utf-8", "replace").strip()
    if not line:
        return None
    parts = line.split(None, 3)
    if len(parts) < 3 or parts[1] != "blob":
        return None  # non-blob (tree/submodule) — skipped per contract note
    return parts[2]

def content(blob):
    return git("cat-file", "blob", blob, binary=True).decode("utf-8", "replace")

events = []          # (path, commit, kind)
receipts = 0
skipped_nonblob = []
never_receipt = []
per_file = {}

for p in paths:
    # commits where the path changed vs (first) parent, oldest first == add commit + event candidates
    touching = git("rev-list", "--first-parent", "--reverse", REV, "--", p).split()
    if not touching:
        never_receipt.append((p, "absent-throughout"))
        continue
    blobs = {c: blob_in(c, p) for c in touching}
    if any(v is None for v in blobs.values()):
        skipped_nonblob.append(p)
        continue
    fc = touching[0]
    fb = blobs[fc]
    ftext = content(fb)
    if not GRAMMAR.search(ftext):
        never_receipt.append((p, "no-receipt-grammar"))
        continue
    receipts += 1
    fspan = sorted(set(l for l in ftext.splitlines() if SPAN.search(l)))
    fpend = bool(PEND.search("\n".join(fspan)))
    fevents = []
    prev_span = fspan
    prev_pend = fpend
    for c in touching[1:]:
        txt = content(blobs[c])
        span = sorted(set(l for l in txt.splitlines() if SPAN.search(l)))
        if span != prev_span:
            fevents.append((c, "rewrite"))
        pend = bool(PEND.search("\n".join(span)))
        if prev_pend and not pend:
            fevents.append((c, "pending_filled"))
        prev_span = span
        prev_pend = pend
    for c, k in fevents:
        events.append((p, c, k))
    per_file[p] = {"first_commit": fc, "first_pending": fpend,
                   "n_touching": len(touching), "events": fevents}

print(f"receipts={receipts} non_receipts={len(never_receipt)} events={len(events)}", file=sys.stderr)

out = {
    "revision": REV,
    "chain_commits": len(chain),
    "receipts": receipts,
    "non_receipts": never_receipt,
    "events": [{"path": p, "commit": c, "kind": k} for p, c, k in events],
}
with open("/fast/scratch/hyaku/kake-r61/ExecC1DiscloseCheck/events.json", "w") as f:
    json.dump(out, f, indent=1)

for p, c, k in events:
    print(f"{k}\t{p}\t{c}")
print(f"--\nreceipts={receipts} events={len(events)}", file=sys.stderr)
