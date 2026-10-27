#!/usr/bin/env python3
"""Classify population-144 paths at base 9f07731a: receipt vs non-receipt per contract grammar."""
import subprocess, re, json, sys, collections

LANE = "/fast/scratch/hyaku/kake-r61/ScoutC1Shapes/lane"
BASE = "9f07731a873585e655a6518233ea39f5d9fb8204"
POP = "/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-61/controls/population-144.txt"

GRAMMAR = [re.compile(p) for p in (r"(?im)^\s*#\s*receipt\s*:", r"EXIT=", r"(?im)^VERDICT:")]
SPAN = re.compile(r"(?im)(^#\s*receipt\s*:|revision\s*[:=]|EXIT\s*=|met\s*=|conditions_passed|cases_passed|findings\s*=|scores_held|members\s*=)")

def git(*args, binary=False):
    r = subprocess.run(["git", "-C", LANE, *args], capture_output=True)
    if r.returncode != 0:
        return None if not binary else None
    return r.stdout if binary else r.stdout.decode("utf-8", "replace")

def first_add(path):
    """Oldest first-parent commit (reachable from BASE) where path appears, with status."""
    out = git("log", "--first-parent", "--format=COMMIT %H", "--name-status", BASE, "--", path)
    if not out:
        return None, None
    cur = None
    oldest = None
    for line in out.splitlines():
        if line.startswith("COMMIT "):
            cur = line.split()[1]
        elif line and cur:
            parts = line.split("\t")
            status = parts[0]
            p = parts[-1]
            if p == path:
                oldest = (cur, status)  # keep updating -> oldest last
    return oldest

def content(rev, path):
    return git("show", f"{rev}:{path}", binary=True)

paths = [l.strip() for l in open(POP) if l.strip()]
assert len(paths) == 144, len(paths)

records = []
for p in paths:
    rec = {"path": p}
    rec["ext"] = ".json" if p.endswith(".json") else ".txt"
    m = re.match(r"^\.ufo/waves/round-(\d+)/(.*)$", p)
    rec["round"] = int(m.group(1)) if m else None
    rec["top_under_round"] = m.group(2).split("/")[0] if m else None
    rec["depth_after_controls"] = None
    cm = re.search(r"/controls?/(.+)$", p)
    if cm:
        rec["depth_after_controls"] = cm.group(1).count("/")
    try:
        p.encode("ascii")
        rec["non_ascii_path"] = False
    except UnicodeEncodeError:
        rec["non_ascii_path"] = True
    fa = first_add(p)
    rec["first_add"] = fa[0] if fa else None
    rec["first_add_status"] = fa[1] if fa else None
    if fa:
        sub = git("show", "--no-patch", "--format=%cs", fa[0])
        rec["first_add_date"] = sub.strip() if sub else None
    b = content(BASE, p)
    if b is None:
        rec["base_missing"] = True
        rec["base_size"] = None
    else:
        rec["base_missing"] = False
        rec["base_size"] = len(b)
        rec["empty"] = len(b) == 0
        t = b.decode("utf-8", "replace")
        rec["base_text"] = t
        rec["span_lines_base"] = len(SPAN.findall(t))
        rec["shapes_base"] = sorted(set(k.lower() for k in (
            ["receipt_hdr"] if GRAMMAR[0].search(t) else []) +
            (["EXIT="] if GRAMMAR[1].search(t) else []) +
            (["VERDICT:"] if GRAMMAR[2].search(t) else []) +
            (["revision:"] if re.search(r"(?im)revision\s*[:=]", t) else []) +
            (["met="] if re.search(r"(?im)met\s*=", t) else []) +
            (["members="] if re.search(r"(?im)members\s*=", t) else []) +
            (["conditions_passed"] if re.search(r"(?im)conditions_passed", t) else []) +
            (["cases_passed"] if re.search(r"(?im)cases_passed", t) else []) +
            (["findings="] if re.search(r"(?im)findings\s*=", t) else []) +
            (["scores_held"] if re.search(r"(?im)scores_held", t) else [])))
    if fa:
        f = content(fa[0], p)
        rec["first_size"] = len(f) if f is not None else None
        if f is not None:
            t = f.decode("utf-8", "replace")
            rec["first_text"] = t
            rec["is_receipt"] = any(g.search(t) for g in GRAMMAR)
            rec["span_lines_first"] = len(SPAN.findall(t))
            rec["first_pending_word"] = bool(re.search(r"(?i)pending", t))
        else:
            rec["is_receipt"] = None
    else:
        rec["is_receipt"] = None
    rec["base_eq_first"] = (rec.get("first_text") == rec.get("base_text")) if fa and not rec.get("base_missing") else None
    records.append(rec)

json.dump(records, open("/fast/scratch/hyaku/kake-r61/ScoutC1Shapes/classify.json", "w"), indent=1)

# Summary
rc = sum(1 for r in records if r.get("is_receipt"))
nr = sum(1 for r in records if r.get("is_receipt") is False)
miss = [r["path"] for r in records if r.get("is_receipt") is None]
print(f"total={len(records)} receipts={rc} non_receipts={nr} unresolved={len(miss)}")
for p in miss: print("UNRESOLVED:", p)
print("empty:", sum(1 for r in records if r.get("empty")))
print("non_ascii:", [r["path"] for r in records if r["non_ascii_path"]])
print("base_missing:", [r["path"] for r in records if r.get("base_missing")])
print("first_add missing:", [r["path"] for r in records if not r.get("first_add")])
print("base_ne_first:", [r["path"] for r in records if r.get("base_eq_first") is False])
