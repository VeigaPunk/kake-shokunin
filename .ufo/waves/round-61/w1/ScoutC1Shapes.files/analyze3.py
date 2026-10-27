#!/usr/bin/env python3
"""Full event walk over population-144 at base: every blob change after first-add, with span diffs."""
import subprocess, re, json

LANE = "/fast/scratch/hyaku/kake-r61/ScoutC1Shapes/lane"
BASE = "9f07731a873585e655a6518233ea39f5d9fb8204"
POP = "/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-61/controls/population-144.txt"

SPAN = re.compile(r"(?im)(^#\s*receipt\s*:|revision\s*[:=]|EXIT\s*=|met\s*=|conditions_passed|cases_passed|findings\s*=|scores_held|members\s*=)")

def git(*args, binary=False):
    r = subprocess.run(["git", "-C", LANE, *args], capture_output=True)
    if r.returncode != 0:
        return None
    return r.stdout if binary else r.stdout.decode("utf-8", "replace")

def content(rev, path):
    return git("show", f"{rev}:{path}", binary=True)

def span_lines(text):
    return set(l for l in text.splitlines() if SPAN.search(l))

paths = [l.strip() for l in open(POP) if l.strip()]
out = {}
for p in paths:
    log = git("log", "--first-parent", "--format=%H", BASE, "--", p)
    commits = log.split()  # newest -> oldest
    if not commits:
        out[p] = {"error": "no history"}
        continue
    first = commits[-1]
    rec = {"first_add": first, "events": []}
    # walk oldest -> newest
    prev_rev = first
    prev_span = span_lines(content(first, p).decode("utf-8", "replace"))
    first_span_pending = any("pending" in l.lower() for l in prev_span)
    rec["first_span_pending"] = first_span_pending
    pending_alive = first_span_pending
    for c in reversed(commits[:-1]):
        cur = content(c, p).decode("utf-8", "replace")
        cs = span_lines(cur)
        kind = None
        if cs != prev_span:
            kind = "rewrite"
        if pending_alive and not any("pending" in l.lower() for l in cs):
            kind = "pending_filled" if kind is None else kind + "+pending_filled"
            pending_alive = False
        if kind:
            rec["events"].append({"commit": c, "kind": kind,
                                  "date": git("show", "--no-patch", "--format=%cs", c).strip()})
        prev_span = cs
    out[p] = rec

json.dump(out, open("/fast/scratch/hyaku/kake-r61/ScoutC1Shapes/events.json", "w"), indent=1)

# Cross with receipt classification
R = {r["path"]: r for r in json.load(open("/fast/scratch/hyaku/kake-r61/ScoutC1Shapes/classify.json"))}
nevents = 0
print("=== receipts with events ===")
for p, rec in out.items():
    if rec.get("events") and R[p]["is_receipt"]:
        for e in rec["events"]:
            nevents += 1
            print(f'  {e["kind"]:20s} {e["commit"][:12]} {e["date"]} {p}')
print("=== non-receipts with events (never findings) ===")
n2 = 0
for p, rec in out.items():
    if rec.get("events") and not R[p]["is_receipt"]:
        n2 += len(rec["events"])
        for e in rec["events"]:
            print(f'  {e["kind"]:20s} {e["commit"][:12]} {e["date"]} {p}')
print(f"total events on receipts={nevents} on non-receipts={n2}")
ev_kinds = {}
for p, rec in out.items():
    for e in rec.get("events", []):
        ev_kinds[e["kind"]] = ev_kinds.get(e["kind"], 0) + 1
print("event kinds:", ev_kinds)
