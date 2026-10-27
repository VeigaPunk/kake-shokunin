#!/usr/bin/env python3
"""Independent re-derivation of the C1 receipt-event population (round 58, seat ExecEventsIndependent).

Deliberately shares no code with .ufo/waves/round-58/c58_receipt_rewrites.py. Method:

  * ancestry: `git rev-list <rev>` (whole ancestry, not `git log --first-parent -- .ufo/waves`)
  * per commit: `git diff-tree -r --no-renames -z --name-status <c>^ <c>`; a root commit uses `--root`
  * population: paths matching ^\\.ufo/waves/round-[0-9]+/(control|controls)/[^/]+$
  * event: M or D of a population path, or A of a population path that existed earlier in the
    oldest-first walk (the first A of a path is its creation, not an event)
  * outside scan: every other path in the ancestry, flagged when it changes in a commit after its
    first appearance, grouped by category

Usage: python3 -B events.py [--root <lane>] [--rev <rev>] [--json]
"""
from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys

BASE = "044048597d62f3199494b63b36e90dd57825e350"
LANE = "/home/vgpnk/Projects/shokunin/kake-shokunin"
POP_RE = re.compile(r"^\.ufo/waves/round-[0-9]+/(control|controls)/[^/]+$")
NESTED_CTL_RE = re.compile(r"^\.ufo/waves/round-[0-9]+/(control|controls)/.+/.+$")
ROUND_W_RE = re.compile(r"^\.ufo/waves/round-[0-9]+/w[0-9]+/.+")
ROUND_JSON_RE = re.compile(r"^\.ufo/waves/round-[0-9]+/[^/]+\.json$")
UFO_ROUND_RE = re.compile(r"^\.ufo/round-[0-9]+/.+")


def clean_env() -> dict:
    return {k: v for k, v in os.environ.items() if not k.startswith("GIT_")}


def git(root: str, *args: str) -> str:
    p = subprocess.run(["git", "-C", root, "-c", "core.quotePath=false", *args],
                       capture_output=True, env=clean_env())
    if p.returncode != 0:
        raise RuntimeError(f"git {' '.join(args)}: {p.stderr.decode('utf-8', 'replace').strip()}")
    return p.stdout.decode("utf-8", "surrogateescape")


def parents(root: str, commit: str) -> list[str]:
    return git(root, "rev-list", "--parents", "-n", "1", commit).split()[1:]


def changed(root: str, commit: str) -> list[tuple[str, str]]:
    """[(status letter, path)] for commit vs its first parent (root: vs the empty tree)."""
    ps = parents(root, commit)
    args = ["diff-tree", "-r", "--no-renames", "-z", "--name-status"]
    args += ["--root", commit] if not ps else [ps[0], commit]
    out = git(root, *args)
    toks = [t for t in out.split("\0") if t != ""]
    res: list[tuple[str, str]] = []
    i = 0
    while i + 1 < len(toks):
        res.append((toks[i][:1], toks[i + 1]))
        i += 2
    return res


def blob(root: str, spec: str) -> str | None:
    p = subprocess.run(["git", "-C", root, "rev-parse", "--verify", "-q", spec],
                       capture_output=True, env=clean_env())
    return p.stdout.decode().strip() or None if p.returncode == 0 else None


def walk(root: str, rev: str, first_parent_only: bool = False) -> tuple[list[dict], list[str], dict]:
    revs = git(root, "rev-list", *(["--first-parent"] if first_parent_only else []), rev).split()
    revs.reverse()  # oldest first
    seen: set[str] = set()
    events: list[dict] = []
    touch: dict[str, list[tuple[int, str, str]]] = {}  # path -> [(index, commit, status)]
    for idx, c in enumerate(revs):
        ps = parents(root, c)
        for status, path in changed(root, c):
            if status not in ("A", "M", "D"):
                status = "M"
            touch.setdefault(path, []).append((idx, c, status))
            if not POP_RE.match(path):
                continue
            if status == "A" and path not in seen:
                seen.add(path)
                continue
            seen.add(path)
            events.append({"path": path, "commit": c, "status": status, "index": idx,
                           "fromBlob": blob(root, f"{ps[0]}:{path}") if ps else None,
                           "toBlob": blob(root, f"{c}:{path}")})
    return events, revs, touch


def outside(touch: dict) -> dict:
    cats: dict[str, list[dict]] = {}
    for path, hits in touch.items():
        if POP_RE.match(path):
            continue
        later = [h for h in hits[1:]]
        if not later:
            continue
        if NESTED_CTL_RE.match(path):
            cat = "nested-controls (depth>=2 under control(s)/)"
        elif ROUND_W_RE.match(path):
            cat = "round-*/w*/**"
        elif ROUND_JSON_RE.match(path):
            cat = "round-*/*.json"
        elif UFO_ROUND_RE.match(path):
            cat = ".ufo/round-*/**"
        else:
            cat = "other .ufo/ or non-.ufo path"
        cats.setdefault(cat, []).append({"path": path, "created": hits[0][1], "events": len(later),
                                         "kinds": "".join(h[2] for h in later),
                                         "commits": [h[1][:12] for h in later]})
    for v in cats.values():
        v.sort(key=lambda d: (-d["events"], d["path"]))
    return cats


RECEIPTISH = re.compile(
    r"(?i)(receipt|measured|census|dispatch-log|sha256sums|[-_]before[-_.]?|[-_]after[-_.]?|^before|^after|"
    r"^base[-_.]|^control|selftest|\.exit$|verdict|evidence|errata|baselines|statements|deaths|pairs\.json)")


def receiptish(touch: dict) -> list[dict]:
    """Paths outside the C1 population that look like measurement receipts/evidence and were rewritten."""
    out: list[dict] = []
    for path, hits in touch.items():
        if POP_RE.match(path) or len(hits) < 2:
            continue
        base = path.rsplit("/", 1)[-1]
        if not RECEIPTISH.search(base):
            continue
        out.append({"path": path, "created": hits[0][1], "events": len(hits) - 1,
                    "kinds": "".join(h[2] for h in hits[1:]), "commits": [h[1][:12] for h in hits[1:]]})
    out.sort(key=lambda d: (-d["events"], d["path"]))
    return out


def compare(evs: list[dict], counter_out: str) -> dict:
    """Compare this walk with the counter's `--list` text (UNDISCLOSED/... lines)."""
    line_re = re.compile(r"^\s+(UNDISCLOSED|PHANTOM|WRONG-KIND|UNPOINTED|NEW-REWRITTEN)\s+([AMD])\s+(\S+)\s+at\s+([0-9a-f]{7,40})"
                         r"\s+(\S+)\s+->\s+(\S+)\s*$")
    theirs: set[tuple] = set()
    with open(counter_out, encoding="utf-8", errors="replace") as fh:
        for line in fh:
            m = line_re.match(line)
            if m:
                theirs.add((m.group(3), m.group(4)[:12], m.group(2), m.group(5)[:12], m.group(6)[:12]))
    mine = {(e["path"], e["commit"][:12], e["status"],
             (e["fromBlob"] or "-")[:12], (e["toBlob"] or "-")[:12]) for e in evs}
    return {"counter": len(theirs), "independent": len(mine), "equal": theirs == mine,
            "only_counter": sorted(theirs - mine), "only_independent": sorted(mine - theirs)}


ART_EXT = (".json", ".txt", ".exit", ".err", ".log", ".sums", ".out", ".tsv")


def evidence(touch: dict, root: str, rev: str) -> dict:
    """Data/receipt artifacts outside the C1 population that change after their first commit."""
    named: list[dict] = []
    unnamed: list[dict] = []
    nested_created = 0
    for path, hits in touch.items():
        if POP_RE.match(path):
            continue
        if NESTED_CTL_RE.match(path):
            nested_created += 1
            continue
        if not path.startswith(".ufo/") or len(hits) < 2:
            continue
        base = path.rsplit("/", 1)[-1]
        ext = "." + base.rsplit(".", 1)[1] if "." in base else ""
        if base != "SHA256SUMS" and ext not in ART_EXT:
            continue
        rec = {"path": path, "created": hits[0][1], "events": len(hits) - 1,
               "kinds": "".join(h[2] for h in hits[1:]), "commits": [h[1][:12] for h in hits[1:]]}
        (named if RECEIPTISH.search(base) else unnamed).append(rec)
    named.sort(key=lambda d: (-d["events"], d["path"]))
    unnamed.sort(key=lambda d: (-d["events"], d["path"]))
    return {"named": named, "unnamed": unnamed, "nested_created": nested_created}


def pop_audit(touch: dict, root: str, rev: str, evs: list[dict]) -> list[dict]:
    """Per population path: commits that touch it, events, distinct blobs, first vs tip blob."""
    per: dict[str, list[tuple[str, str]]] = {}
    for e in evs:
        per.setdefault(e["path"], []).append((e["commit"], e["status"]))
    rows: list[dict] = []
    for path, hits in touch.items():
        if not POP_RE.match(path):
            continue
        blobs = [blob(root, f"{c}:{path}") for _, c, _ in hits]
        distinct = len({b for b in blobs if b})
        rows.append({"path": path, "touches": len(hits), "events": len(per.get(path, [])),
                     "distinct_blobs": distinct, "first": (blobs[0] or "-")[:12],
                     "tip": (blobs[-1] or "-")[:12], "creation": hits[0][1][:12]})
    rows.sort(key=lambda d: (-d["events"], d["path"]))
    return rows


def hist(touch: dict) -> dict:
    h: dict[tuple[str, str], int] = {}
    for path, hits in touch.items():
        if POP_RE.match(path):
            continue
        if len(hits) < 2:
            continue
        parts = path.split("/")
        prefix = "/".join(parts[:3]) if len(parts) >= 3 else path
        ext = ("." + parts[-1].rsplit(".", 1)[1]) if "." in parts[-1] else "(none)"
        h[(prefix, ext)] = h.get((prefix, ext), 0) + 1
    return dict(sorted(h.items(), key=lambda kv: -kv[1]))


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--root", default=LANE)
    ap.add_argument("--rev", default=BASE)
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--detail", action="store_true")
    ap.add_argument("--compare", default=None, help="counter --list output to compare against")
    a = ap.parse_args()
    root = a.root
    evs, revs, touch = walk(root, a.rev, False)
    fp_evs, fp_revs, _ = walk(root, a.rev, True)
    cats = outside(touch)
    rish = receiptish(touch)
    ev = evidence(touch, root, a.rev)
    audit = pop_audit(touch, root, a.rev, evs)
    cmp = compare(evs, a.compare) if a.compare else None
    doc = {
        "revision": a.rev,
        "commits_full": len(revs),
        "commits_first_parent": len(fp_revs),
        "events": [{"path": e["path"], "commit": e["commit"], "status": e["status"],
                    "fromBlob": e["fromBlob"], "toBlob": e["toBlob"]} for e in evs],
        "events_first_parent": [{"path": e["path"], "commit": e["commit"], "status": e["status"]} for e in fp_evs],
        "outside": {k: {"paths": len(v), "events": sum(d["events"] for d in v), "detail": v} for k, v in cats.items()},
        "receiptish": {"paths": len(rish), "events": sum(d["events"] for d in rish), "detail": rish},
        "evidence": {"named": ev["named"], "unnamed": ev["unnamed"],
                     "named_paths": len(ev["named"]), "unnamed_paths": len(ev["unnamed"]),
                     "named_events": sum(d["events"] for d in ev["named"]),
                     "unnamed_events": sum(d["events"] for d in ev["unnamed"]),
                     "nested_created": ev["nested_created"]},
        "pop_audit": audit,
        "compare": cmp,
        "hist": {f"{p} {e}": n for (p, e), n in hist(touch).items()},
    }
    if a.json:
        print(json.dumps(doc, indent=1, ensure_ascii=False))
        return 0
    print(f"EVENTS full-ancestry={len(evs)} first-parent={len(fp_evs)} commits={len(revs)}/{len(fp_revs)}")
    for e in evs:
        print(f"  {e['status']} {e['path']} {e['commit'][:12]} {(e['fromBlob'] or '-')[:12]} -> {(e['toBlob'] or '-')[:12]}")
    print("OUTSIDE")
    for k, v in sorted(cats.items()):
        print(f"  [{k}] paths={len(v)} events={sum(d['events'] for d in v)}")
        if a.detail:
            for d in v:
                print(f"    {d['events']:2d} {d['kinds']:>4s} {d['path']}")
    print("HIST (prefix, ext) -> paths modified after creation")
    for (p, e), n in sorted(hist(touch).items(), key=lambda kv: -kv[1]):
        print(f"  {n:4d}  {p}  {e}")
    print(f"RECEIPTISH outside population: paths={len(rish)} events={sum(d['events'] for d in rish)}")
    for d in rish:
        print(f"  {d['events']:2d} {d['kinds']:>4s} {d['path']}")
    print(f"EVIDENCE .ufo artifacts outside population (rewritten after creation): "
          f"named={len(ev['named'])}/{sum(d['events'] for d in ev['named'])}ev "
          f"unnamed={len(ev['unnamed'])}/{sum(d['events'] for d in ev['unnamed'])}ev "
          f"nested-control-paths-ever-created={ev['nested_created']} nested-rewritten=0")
    for label, rows in (("NAMED", ev["named"]), ("UNNAMED", ev["unnamed"])):
        for d in rows:
            print(f"  {label} {d['events']:2d} {d['kinds']:>4s} {d['path']} @ {','.join(d['commits'])}")
    print(f"POP-AUDIT population paths with any touch={len(audit)}")
    for r in audit:
        print(f"  ev={r['events']} touch={r['touches']} blobs={r['distinct_blobs']} {r['path']} "
              f"c={r['creation']} {r['first']}->{r['tip']}")
    if cmp:
        print(f"COMPARE counter={cmp['counter']} independent={cmp['independent']} equal={cmp['equal']}")
        for t in cmp["only_counter"]:
            print(f"  ONLY-COUNTER {t}")
        for t in cmp["only_independent"]:
            print(f"  ONLY-INDEPENDENT {t}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
