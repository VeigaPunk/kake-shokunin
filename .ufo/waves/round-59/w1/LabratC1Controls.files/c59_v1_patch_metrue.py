#!/usr/bin/env python3
"""Round-59 C1 counter — calibration: the SCORECARD axis table's evidence cells match committed repository state.

Surface: the lane's self-assessment table in `SCORECARD.md` (header `| Axis | Score | Evidence pointer | Last change |`, its
three rows operability / freshness / calibration). Observed state: the committed tree at the measured revision. AXES.md defines
calibration as "SHONEN.md/SCORECARD entries match observed repo state"; this counter counts the mismatches of the table's
evidence cells against that state. At the base the operability row (score 10) points at `cli.mjs` line numbers in a source tree
the lane no longer holds and the freshness row (score 10) at six `/tmp/kake-r17/...` files the reaper deleted; neither row
cites a committed receipt for the tallies it states.

Version 1 (frozen with the round-59 contract before any data).

Atoms, per evidence cell (the cell text between the 3rd and 4th pipe of the row):
  pointer   every backticked token that names a path (contains `/`, or ends in a file extension with an optional `:LINE[-LINE]`),
            every bare `/tmp/...`, `~/...` or `/home/...` token, and every backticked `:LINE[-LINE]` continuation (which points
            into the previous pointer's file). `{a,b}` brace groups expand. A pointer resolves iff it is a repo-relative path
            (leading `./` allowed) naming a blob or tree at the measured revision; a `:LINE` suffix also needs that many lines.
            Absolute, `~`, `/tmp` and bare-name-not-at-root pointers never resolve (not committed bytes).
  receipt   a resolved pointer naming a blob under `.ufo/waves/round-<N>/` whose round is on-axis: SCORECARD.md's `## Round N`
            section (all sections so headed, to the next `## ` heading) has a table row naming the row's axis. A receipt of a
            round that made no claim on the axis is off-axis (a mismatch).
  tally     every `A/B` (digits) in the cell outside a path token; it is found iff the string `A/B` occurs in a resolved blob
            pointer of the same cell.
Counts:
  unresolved          pointers that do not resolve
  rows_no_receipt     rows citing no on-axis receipt
  receipts_off_axis   cited receipts of rounds whose SCORECARD section has no table row naming the axis
  tallies_unfound     tallies found in no cited blob
  rows_no_tally       rows with no found tally (a row must state at least one number it can show)
  mismatches          = unresolved + rows_no_receipt + receipts_off_axis + tallies_unfound + rows_no_tally
  rows                axis rows (must be exactly operability, freshness, calibration, in that order)
  scores_held         operability and freshness score cells equal to the base revision's (no score moves through this claim)
  superseded_kept     base-revision evidence cells that still occur verbatim in SCORECARD.md at the measured revision outside the
                      axis table (append-only: a replaced cell is kept, not erased)

Predicate (frozen in `contract.json`):

    met: mismatches == 0 AND rows == 3 AND scores_held == 2 AND superseded_kept == 3

Exit codes: 0 met, 1 not met, 2 unevaluable, 64 usage.
CLI: --root <lane toplevel> --revision <rev> [--base <rev>] [--json] | --selftest
Not tested: whether a cited receipt supports the score (a reviewer judgment); evidence outside the axis table (move log,
round sections); whether a stated tally is the cited receipt's own result rather than a number that occurs in it.
"""
from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
import sys

PREDICATE = "met: mismatches == 0 AND rows == 3 AND scores_held == 2 AND superseded_kept == 3"
BASE_REV = "fd6303ce5c14b3f892dec586297a942ab6e4193b"
SCORECARD = "SCORECARD.md"
HEADER = "| Axis | Score | Evidence pointer | Last change |"
AXES = ("operability", "freshness", "calibration")
HELD = ("operability", "freshness")
EXT = r"(?:md|py|mjs|js|json|jsonl|txt|sh|tsv|html|csv|yml|yaml|toml)"
PATHISH = re.compile(rf"^(?:~|/|\./|\.\./)?[\w.@+-]+(?:/[\w.@{{}},+*-]*)+/?(?::\d+(?:-\d+)?)?$|^[\w.@+-]+\.{EXT}(?::\d+(?:-\d+)?)?$")
LINEONLY = re.compile(r"^:\d+(?:-\d+)?$")
BARE = re.compile(r"(?<![\w`/])((?:/tmp/|~/|/home/)[^\s`|,;)]+)")
TALLY = re.compile(r"(?<![\w/.])(\d+)/(\d+)(?![\w/])")


def clean_env() -> dict:
    env = {k: v for k, v in os.environ.items() if not k.startswith("GIT_")}
    env["LC_ALL"] = "C.UTF-8"
    return env


def git(root: str, *args: str) -> tuple[int, bytes]:
    p = subprocess.run(["git", "-C", root, *args], stdout=subprocess.PIPE, stderr=subprocess.PIPE, env=clean_env())
    return p.returncode, p.stdout


def show(root: str, rev: str, path: str) -> str | None:
    rc, out = git(root, "show", f"{rev}:{path}")
    if rc != 0:
        return None
    try:
        return out.decode("utf-8")
    except UnicodeDecodeError:
        return None


def obj_type(root: str, rev: str, path: str) -> str | None:
    rc, out = git(root, "cat-file", "-t", f"{rev}:{path}")
    return out.decode().strip() if rc == 0 else None


def axis_table(text: str) -> tuple[list[tuple[int, list[str], str]], tuple[int, int]]:
    """Rows of the first table whose header line is HEADER: (line index, cells, raw line); and the table's line span."""
    lines = text.split("\n")
    for i, ln in enumerate(lines):
        if ln.strip() == HEADER:
            rows, j = [], i + 1
            if j < len(lines) and re.match(r"^\|\s*-", lines[j].strip()):
                j += 1
            while j < len(lines) and lines[j].strip().startswith("|"):
                cells = [c.strip() for c in lines[j].strip().strip("|").split("|")]
                rows.append((j, cells, lines[j]))
                j += 1
            return rows, (i, j)
    return [], (-1, -1)


def expand(tok: str) -> list[str]:
    m = re.search(r"\{([^{}]*)\}", tok)
    if not m:
        return [tok]
    return [x for alt in m.group(1).split(",") for x in expand(tok[:m.start()] + alt + tok[m.end():])]


def pointers(cell: str) -> list[str]:
    out: list[str] = []
    for span in re.findall(r"`([^`]+)`", cell):
        for tok in span.split():
            tok = tok.rstrip(".,;)")
            if LINEONLY.match(tok):
                out.append(tok)
            elif PATHISH.match(tok) and not tok.startswith("--"):
                out.extend(expand(tok))
    stripped = re.sub(r"`[^`]*`", " ", cell)
    for tok in BARE.findall(stripped):
        out.extend(expand(tok.rstrip(".,;)")))
    return out


def resolve(root: str, rev: str, ptr: str, last_file: str | None) -> tuple[bool, str | None, str]:
    """(resolved, file path for a following :LINE, reason)."""
    line_lo = line_hi = None
    path = ptr
    if LINEONLY.match(ptr):
        if last_file is None:
            return False, None, "line pointer with no preceding resolved file"
        path, rng = last_file, ptr[1:]
    else:
        m = re.match(r"^(.*?):(\d+(?:-\d+)?)$", ptr)
        rng = None
        if m:
            path, rng = m.group(1), m.group(2)
    if rng:
        a, _, b = rng.partition("-")
        line_lo, line_hi = int(a), int(b or a)
    if path.startswith(("/", "~")):
        return False, None, "absolute or home path (not committed bytes)"
    norm = os.path.normpath(path[2:] if path.startswith("./") else path)
    if norm.startswith(".."):
        return False, None, "path leaves the repository"
    kind = obj_type(root, rev, norm.rstrip("/"))
    if kind not in ("blob", "tree"):
        return False, None, "not a committed path at the revision"
    if line_hi is not None:
        if kind != "blob":
            return False, None, "line pointer into a tree"
        body = show(root, rev, norm) or ""
        if line_hi > len(body.split("\n")) or line_lo < 1:
            return False, None, "line beyond the file"
    return True, (norm if kind == "blob" else None), "ok"


def round_sections(text: str) -> dict[int, str]:
    """`## Round N ...` sections of SCORECARD.md (to the next `## ` heading), joined per round number."""
    out: dict[int, str] = {}
    cur, buf = None, []
    for ln in text.split("\n") + ["## end"]:
        if ln.startswith("## "):
            if cur is not None:
                out[cur] = out.get(cur, "") + "\n".join(buf) + "\n"
            m = re.match(r"^## Round (\d+)\b", ln)
            cur, buf = (int(m.group(1)) if m else None), []
        elif cur is not None:
            buf.append(ln)
    return out


def on_axis(section: str, axis: str) -> bool:
    """A receipt of round N supports an axis row only when SCORECARD's `## Round N` section has a table row naming that axis."""
    return any(ln.strip().startswith("|") and re.search(rf"\b{re.escape(axis.lower())}\b", ln.lower())
               for ln in section.split("\n"))


def measure(root: str, rev: str, base: str) -> dict:
    text = show(root, rev, SCORECARD)
    base_text = show(root, base, SCORECARD)
    if text is None or base_text is None:
        raise RuntimeError(f"{SCORECARD} unreadable at the measured or base revision")
    rows, span = axis_table(text)
    base_rows, _ = axis_table(base_text)
    if not base_rows:
        raise RuntimeError("base revision has no axis table")
    res = {"rows": len(rows), "row_names": [r[1][0] if r[1] else "" for r in rows], "unresolved": 0, "rows_no_receipt": 0,
           "receipts_off_axis": 0, "tallies_unfound": 0, "rows_no_tally": 0, "scores_held": 0, "superseded_kept": 0, "detail": []}
    sections = round_sections(text)
    names_ok = tuple(n.lower() for n in res["row_names"]) == AXES
    for _i, cells, _raw in rows:
        if len(cells) < 4:
            res["rows_no_receipt"] += 1
            res["rows_no_tally"] += 1
            res["detail"].append({"row": cells[:1], "note": "row has fewer than 4 cells"})
            continue
        cell = cells[2]
        last_file, blobs, receipts, d = None, [], [], {"row": cells[0], "pointers": [], "tallies": []}
        for p in pointers(cell):
            ok, f, why = resolve(root, rev, p, last_file)
            d["pointers"].append({"pointer": p, "resolved": ok, "why": why})
            if not ok:
                res["unresolved"] += 1
            if ok and f:
                last_file = f
                blobs.append(f)
                rm = re.match(r"^\.ufo/waves/round-(\d+)/", f)
                if rm:
                    if on_axis(sections.get(int(rm.group(1)), ""), cells[0]):
                        receipts.append(f)
                    else:
                        res["receipts_off_axis"] += 1
                        d.setdefault("off_axis", []).append(f)
            elif not ok and not LINEONLY.match(p):
                last_file = None
        if not receipts:
            res["rows_no_receipt"] += 1
        bodies = [show(root, rev, b) or "" for b in blobs]
        bodies = [b for b in bodies if "met=True" in b]
        stripped = BARE.sub(" ", re.sub(r"`([^`]*)`", lambda m: " " if pointers(m.group(0)) else m.group(1), cell))
        found_any = False
        for a, b in TALLY.findall(stripped):
            t = f"{a}/{b}"
            hit = any(t in body for body in bodies)
            d["tallies"].append({"tally": t, "found": hit})
            if hit:
                found_any = True
            else:
                res["tallies_unfound"] += 1
        if not found_any:
            res["rows_no_tally"] += 1
        res["detail"].append(d)
    base_cells = {c[0].lower(): c for _, c, _ in base_rows if c}
    cur_cells = {c[0].lower(): c for _, c, _ in rows if c}
    for ax in HELD:
        if ax in base_cells and ax in cur_cells and len(base_cells[ax]) > 1 and len(cur_cells[ax]) > 1 \
                and base_cells[ax][1] == cur_cells[ax][1]:
            res["scores_held"] += 1
    lines = text.split("\n")
    outside = "\n".join(lines[:span[0]] + lines[span[1]:]) if span[0] >= 0 else text
    for ax in AXES:
        bc = base_cells.get(ax)
        if bc and len(bc) > 2 and bc[2] and bc[2] in outside:
            res["superseded_kept"] += 1
    res["mismatches"] = (res["unresolved"] + res["rows_no_receipt"] + res["receipts_off_axis"] + res["tallies_unfound"]
                         + res["rows_no_tally"])
    res["names_ok"] = names_ok
    res["met"] = (res["mismatches"] == 0 and res["rows"] == 3 and names_ok and res["scores_held"] == 2
                  and res["superseded_kept"] == 3)
    return res


def selftest() -> int:
    print("c59 axis-evidence selftest: version 1 stub (wave 1 writes the fixture kill matrix); exit 2")
    return 2


def main() -> int:
    class _P(argparse.ArgumentParser):
        def error(self, message):
            print(f"usage error: {message}", file=sys.stderr)
            raise SystemExit(64)

    ap = _P(description="Round-59 C1 counter (SCORECARD axis-table evidence vs committed state)")
    ap.add_argument("--root", default=".")
    ap.add_argument("--revision")
    ap.add_argument("--base", default=BASE_REV)
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args()
    if a.selftest:
        return selftest()
    if not a.revision or not a.base:
        print("usage: --revision (and a non-empty --base) are required unless --selftest is used", file=sys.stderr)
        return 64
    rc, top = git(a.root, "rev-parse", "--show-toplevel")
    if rc != 0 or os.path.realpath(top.decode().strip()) != os.path.realpath(a.root):
        print(f"unevaluable: --root {a.root!r} is not the toplevel of a git repository\nEXIT=2")
        return 2
    rr, rev = git(a.root, "rev-parse", "--verify", "-q", f"{a.revision}^{{commit}}")
    rb, base = git(a.root, "rev-parse", "--verify", "-q", f"{a.base}^{{commit}}")
    if rr != 0 or rb != 0:
        print(f"unevaluable: revision {a.revision!r} or base {a.base!r} does not resolve to a commit\nEXIT=2")
        return 2
    rev, base = rev.decode().strip(), base.decode().strip()
    try:
        res = measure(a.root, rev, base)
    except Exception as exc:  # unevaluable evidence is exit 2, never a silent miss
        print(f"unevaluable: {type(exc).__name__}: {exc}\nEXIT=2")
        return 2
    code = 0 if res["met"] else 1
    if a.json:
        print(json.dumps({"schema": "kake-r59-c1-axis-evidence-v1", "predicate": PREDICATE, "revision": rev, "base": base,
                          **res, "exit": code}, indent=1, ensure_ascii=False))
        return code
    print(f"C1 axis-evidence mismatches={res['mismatches']} unresolved={res['unresolved']} rows_no_receipt={res['rows_no_receipt']} "
          f"receipts_off_axis={res['receipts_off_axis']} "
          f"tallies_unfound={res['tallies_unfound']} rows_no_tally={res['rows_no_tally']} rows={res['rows']} "
          f"scores_held={res['scores_held']} superseded_kept={res['superseded_kept']} met={res['met']}  ({PREDICATE})")
    for d in res["detail"]:
        bad = [p for p in d.get("pointers", []) if not p["resolved"]]
        print(f"  {d['row']}: pointers={len(d.get('pointers', []))} unresolved={len(bad)} tallies={d.get('tallies', [])}")
        for p in bad:
            print(f"    - {p['pointer']}: {p['why']}")
    print(f"  revision: {rev}\n  base: {base}")
    print(f"EXIT={code}")
    return code


if __name__ == "__main__":
    sys.exit(main())
