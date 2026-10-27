#!/usr/bin/env python3
"""Round-59 C1 counter — calibration: the SCORECARD axis table's evidence cells match committed repository state.

Surface: the lane's self-assessment table in `SCORECARD.md` (header `| Axis | Score | Evidence pointer | Last change |`, its
three rows operability / freshness / calibration). Observed state: the committed tree at the measured revision. AXES.md defines
calibration as "SHONEN.md/SCORECARD entries match observed repo state"; this counter counts the mismatches of the table's
evidence cells against that state. At the base the operability row (score 10) points at `cli.mjs` line numbers in a source tree
the lane no longer holds and the freshness row (score 10) at six `/tmp/kake-r17/...` files the reaper deleted; neither row
cites a committed receipt for the tallies it states.

Version 1 frozen at 45a92b64 with the round-59 contract. Version 2 (after wave 1, before any claim was measured; every change
tightens): one rendered axis table (`tables == 1`; HTML comments, fenced code and 4-space indents do not count — w1/CriticC1Parse,
w1/CriticC1Cheat shadow table); cells split on unescaped pipes; path mentions outside code spans, `<code>` spans and Unicode slash
lookalikes are pointers (w1/CriticC1Cheat); a committed symlink never resolves (w1/SentinelCounters F1/F2); a receipt lives under
`round-N/control(s)/` (w1/LabratC1Controls) of a round before 59 whose base-revision section is kept verbatim and holds a table
row whose `axis` column begins with the axis name (w1/CriticC1Cheat unrelated-row hole); a tally must occur in a cited on-axis
receipt; each row cites at least one receipt of a met / exit-0 run (`rows_no_passing_receipt`, w1/ReviewerC1Contract); the
replaced cells are kept under a `## ` heading naming them superseded, outside comments (w1/ReviewerC1Contract,
w1/CriticC1Cheat); the row-order requirement is in the predicate (`axes_ordered`, w1/ScribeC2SkillRows finding 1).

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

PREDICATE = "met: mismatches == 0 AND tables == 1 AND rows == 3 AND axes_ordered == 1 AND scores_held == 2 AND superseded_kept == 3"
BASE_REV = "fd6303ce5c14b3f892dec586297a942ab6e4193b"
SCORECARD = "SCORECARD.md"
HEADER = "| Axis | Score | Evidence pointer | Last change |"
AXES = ("operability", "freshness", "calibration")
HELD = ("operability", "freshness")
EXT = r"(?:md|py|mjs|js|json|jsonl|txt|sh|tsv|html|csv|yml|yaml|toml)"
PATHISH = re.compile(rf"^(?:~|/|\./|\.\./)?[\w.@+-]+(?:/[\w.@{{}},+*-]*)+/?(?::\d+(?:-\d+)?)?$|^[\w.@+-]+\.{EXT}(?::\d+(?:-\d+)?)?$")
LINEONLY = re.compile(r"^:\d+(?:-\d+)?$")
BARE = re.compile(r"(?<![\w`/])((?:/tmp/|~/|/home/)[^\s`|,;)]+)")
SLASHES = "/\u2215\u2044\uff0f"  # version 2: Unicode slash lookalikes spell a path the repo cannot hold (w1/CriticC1Cheat)
ROOTS = (".ufo/", "corpus/", "scripts/", "plans/", "considerthese/", "./", "../", "/", "~")
MEASURED_ROUND = 59
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


def visible(text: str) -> str:
    """Version 2: the rendered-markdown view, line count kept: HTML comments and fenced code blocks blanked (w1/CriticC1Cheat
    hidden-comment retention; w1/CriticC1Parse code-block tables). Indented code is excluded by the 0-3-space rule of the parsers."""
    text = re.sub(r"(?s)<!--.*?-->", lambda m: "\n" * m.group(0).count("\n"), text)
    out, fence = [], None
    for ln in text.split("\n"):
        m = re.match(r"^ {0,3}(`{3,}|~{3,})", ln)
        if fence is None and m:
            fence = m.group(1)
            out.append("")
            continue
        if fence is not None:
            if re.match(rf"^ {{0,3}}{re.escape(fence[0])}{{{len(fence)},}}\s*$", ln):
                fence = None
            out.append("")
            continue
        out.append(ln)
    return "\n".join(out)


def split_cells(line: str) -> list[str]:
    """Version 2: split a pipe-table row on unescaped pipes only (w1/CriticC1Parse escaped-pipe false red)."""
    body = line.strip()
    body = body[1:] if body.startswith("|") else body
    body = body[:-1] if body.endswith("|") and not body.endswith("\\|") else body
    return [c.strip() for c in re.split(r"(?<!\\)\|", body)]


def is_row(ln: str) -> bool:
    return len(ln) - len(ln.lstrip(" ")) <= 3 and ln.strip().startswith("|")


def axis_table(text: str) -> tuple[list[tuple[int, list[str], str]], tuple[int, int], int]:
    """Version 2: rows of the axis table (header line HEADER at 0-3 spaces, outside comments/fences), its line span, and how
    many such headers the rendered file holds (w1/CriticC1Cheat first-header shadow table: the predicate needs exactly one)."""
    lines = visible(text).split("\n")
    heads = [i for i, ln in enumerate(lines) if ln.strip() == HEADER and len(ln) - len(ln.lstrip(" ")) <= 3]
    if not heads:
        return [], (-1, -1), 0
    i = heads[0]
    rows, j = [], i + 1
    if j < len(lines) and re.match(r"^\|\s*:?-", lines[j].strip()):
        j += 1
    while j < len(lines) and is_row(lines[j]):
        rows.append((j, split_cells(lines[j]), lines[j]))
        j += 1
    return rows, (i, j), len(heads)


def expand(tok: str) -> list[str]:
    m = re.search(r"\{([^{}]*)\}", tok)
    if not m:
        return [tok]
    return [x for alt in m.group(1).split(",") for x in expand(tok[:m.start()] + alt + tok[m.end():])]


def pointers(cell: str) -> list[str]:
    out: list[str] = []
    cell = re.sub(r"(?is)<code>(.*?)</code>", lambda m: "`" + m.group(1) + "`", cell)  # version 2: HTML code spans count as code spans
    for span in re.findall(r"`([^`]+)`", cell):
        for tok in span.split():
            tok = tok.rstrip(".,;)")
            if LINEONLY.match(tok):
                out.append(tok)
            elif PATHISH.match(tok) and not tok.startswith("--"):
                out.extend(expand(tok))
    stripped = re.sub(r"`[^`]*`", " ", cell)
    for tok in stripped.split():  # version 2: path mentions outside code spans are pointers too (w1/CriticC1Cheat)
        tok = tok.strip("*_\"'(<[").rstrip(".,;:)>]*_\"'")
        if not re.search(r"\w", tok) or "://" in tok or not any(c in tok for c in SLASHES) or TALLY.fullmatch(tok):
            continue
        if any(c in tok for c in SLASHES[1:]):
            out.append(tok)  # a lookalike slash never names a committed path
        elif tok.startswith(ROOTS) or re.search(rf"\.{EXT}(?::\d+(?:-\d+)?)?$", tok):
            out.extend(expand(tok))
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
    rc, ls = git(root, "ls-tree", rev, "--", norm.rstrip("/"))
    if rc == 0 and ls.startswith(b"120000 "):  # version 2 (w1/SentinelCounters F1/F2): a symlink's blob is its target string, not evidence
        return False, None, "a committed symlink, not a file"
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
    """Version 2 (w1/CriticC1Cheat unrelated-row hole): a receipt of round N supports an axis row only when the base-revision
    `## Round N` section holds a pipe table whose header has an `axis` column and a data row whose cell in that column begins
    with the axis name (`calibration (declared; ...)`, `freshness 10->10 (HOLD)`)."""
    lines = visible(section).split("\n")
    for i in range(len(lines) - 1):
        if is_row(lines[i]) and re.match(r"^\|?\s*:?-{3,}", lines[i + 1].strip()):
            head = [c.lower() for c in split_cells(lines[i])]
            cols = [k for k, c in enumerate(head) if "axis" in c]
            j = i + 2
            while j < len(lines) and is_row(lines[j]):
                cells = split_cells(lines[j])
                for k in cols:
                    if k < len(cells) and re.match(rf"^[*_ ]*{re.escape(axis.lower())}\b", cells[k].lower()):
                        return True
                j += 1
    return False


def measure(root: str, rev: str, base: str) -> dict:
    text = show(root, rev, SCORECARD)
    base_text = show(root, base, SCORECARD)
    if text is None or base_text is None:
        raise RuntimeError(f"{SCORECARD} unreadable at the measured or base revision")
    rows, span, tables = axis_table(text)
    base_rows, _, _ = axis_table(base_text)
    if not base_rows:
        raise RuntimeError("base revision has no axis table")
    res = {"rows": len(rows), "row_names": [r[1][0] if r[1] else "" for r in rows], "unresolved": 0, "rows_no_receipt": 0,
           "receipts_off_axis": 0, "rows_no_passing_receipt": 0, "tallies_unfound": 0, "rows_no_tally": 0, "scores_held": 0, "superseded_kept": 0, "detail": []}
    base_sections = round_sections(base_text)
    vis = visible(text)
    # version 2: a receipt counts only for a round before the measured one whose base-revision section is kept verbatim
    sections = {n: sec for n, sec in base_sections.items() if n < MEASURED_ROUND and visible(sec).strip() in vis}
    res["tables"] = tables
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
                rm = re.match(r"^\.ufo/waves/round-(\d+)/controls?/", f)  # version 2: receipts live in control(s)/ (w1/LabratC1Controls)
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
        # version 2 (w1/ReviewerC1Contract): the score rests on at least one cited on-axis receipt of a met / exit-0 run
        if not any(re.search(r"(?m)(\bmet=True\b|^EXIT(_CODE)?=0\s*$)", show(root, rev, r) or "") for r in receipts):
            res["rows_no_passing_receipt"] += 1
        bodies = [show(root, rev, b) or "" for b in receipts]  # version 2: a tally must occur in a cited on-axis receipt
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
    # version 2 (w1/ReviewerC1Contract): a replaced cell is kept under a `## ` heading that names it superseded
    kept, keep = [], False
    for ln in visible(text).split("\n"):
        if ln.startswith("## "):
            keep = "superseded" in ln.lower()
        elif keep:
            kept.append(ln)
    outside = "\n".join(kept)
    for ax in AXES:
        bc = base_cells.get(ax)
        if bc and len(bc) > 2 and bc[2] and bc[2] in outside:
            res["superseded_kept"] += 1
    res["mismatches"] = (res["unresolved"] + res["rows_no_receipt"] + res["receipts_off_axis"]
                         + res["rows_no_passing_receipt"] + res["tallies_unfound"] + res["rows_no_tally"])
    res["axes_ordered"] = int(names_ok)
    res["met"] = (res["mismatches"] == 0 and tables == 1 and res["rows"] == 3 and names_ok and res["scores_held"] == 2
                  and res["superseded_kept"] == 3)
    return res


def selftest() -> int:
    """Version 2 kill matrix (L1-written; w1/ExecC1Selftest's v1-semantics matrix is kept as wave evidence). Each case builds a
    scratch git repository (base commit + measured commit), runs `measure()` and asserts the named counts. Scratch honours
    TMPDIR; the repository is removed on exit."""
    import shutil
    import tempfile

    for k in [k for k in os.environ if k.startswith("GIT_")]:
        os.environ.pop(k)
    work = tempfile.mkdtemp(prefix="c59-c1-selftest-")
    R57 = ".ufo/waves/round-57/controls/after.txt"
    R56 = ".ufo/waves/round-56/controls/after.txt"
    OLD = {"operability": "legacy `cli.mjs:935` and `/tmp/kake-r17/x.md` 10/10",
           "freshness": "legacy `/tmp/kake-r17/y.md` 117/117", "calibration": "move with no pointer"}
    sec57 = ("## Round 57 — claims\n\n| Claim | Axis | Before → after |\n|---|---|---|\n| c1 | calibration (declared) | x |\n"
             "| c2 | operability | x |\n| c3 | freshness (sourced) | x |\n")
    sec56 = "## Round 56 — claims\n\n| Claim | Axis | Before → after |\n|---|---|---|\n| c1 | calibration | x |\n"

    def table(cells: dict, scores=None, order=AXES) -> str:
        scores = scores or {"operability": "10", "freshness": "10", "calibration": "2"}
        rows = "\n".join(f"| {a} | {scores[a]} | {cells[a]} | 1 |" for a in order)
        return f"# Scorecard\n\n{HEADER}\n|---|---|---|---|\n{rows}\n\n"

    GOOD = {a: f"rests on `{R57}` which prints 14/14 met=True" for a in AXES}
    SUPER = "## Superseded axis-table evidence (round 59)\n\n" + "\n".join(f"> {v}" for v in OLD.values()) + "\n"
    BASE = table(OLD) + sec56 + "\n" + sec57

    def build(name: str, scorecard: str, files: dict | None = None, links: dict | None = None):
        d = os.path.join(work, name)
        os.makedirs(d)

        def put(rel, text):
            pth = os.path.join(d, rel)
            os.makedirs(os.path.dirname(pth) or d, exist_ok=True)
            with open(pth, "w", encoding="utf-8") as fh:
                fh.write(text)

        def commit():
            subprocess.run(["git", "-C", d, "add", "-A"], check=True, env=clean_env())
            subprocess.run(["git", "-C", d, "-c", "user.name=selftest", "-c", "user.email=selftest@local", "-c", "commit.gpgsign=false",
                            "commit", "-q", "--allow-empty", "-m", "x"], check=True, env=clean_env())
            return subprocess.run(["git", "-C", d, "rev-parse", "HEAD"], capture_output=True, text=True, check=True,
                                  env=clean_env()).stdout.strip()

        subprocess.run(["git", "-C", d, "init", "-q"], check=True, env=clean_env())
        put("SCORECARD.md", BASE)
        put(R57, "C2 resolver-cases 14/14 met=True\nEXIT=0\n")
        put(R56, "base 0/8 met=False\nEXIT=1\n")
        base = commit()
        for rel, text in (files or {}).items():
            put(rel, text)
        for rel, target in (links or {}).items():
            os.symlink(target, os.path.join(d, rel))
        put("SCORECARD.md", scorecard)
        return d, commit(), base

    def good(cells=None, extra="", **kw) -> str:
        c = dict(GOOD)
        c.update(cells or {})
        return table(c, **kw) + sec56 + "\n" + sec57 + "\n" + extra + SUPER

    cases = [
        ("base_is_red", BASE, {}, {}, {"met": False, "unresolved": 3}),
        ("minimal_true_meets", good(), {}, {}, {"met": True, "mismatches": 0}),
        ("emptied_cells", table({a: "" for a in AXES}) + sec56 + "\n" + sec57 + "\n" + SUPER, {}, {},
         {"rows_no_receipt": 3, "rows_no_tally": 3, "met": False}),
        ("tmp_pointer", good({"freshness": f"`{R57}` 14/14 and `/tmp/x/y.md`"}), {}, {}, {"unresolved": 1, "met": False}),
        ("bare_dead_path_outside_backticks", good({"freshness": f"`{R57}` 14/14 see corpus/claims/report.md"}), {}, {},
         {"unresolved": 1, "met": False}),
        ("unicode_slash_path", good({"freshness": f"`{R57}` 14/14 see corpus\u2215claims\u2215x.md"}), {}, {},
         {"unresolved": 1, "met": False}),
        ("tree_pointer_is_not_a_receipt", good({"operability": "`.ufo/waves/round-57/` 14/14"}), {}, {},
         {"rows_no_receipt": 1, "met": False}),
        ("off_axis_receipt", good({"freshness": f"`{R56}` 0/8"}), {}, {}, {"receipts_off_axis": 1, "met": False}),
        ("receipt_outside_controls", good({"operability": "`.ufo/waves/round-57/w1/Seat.md` 14/14"}),
         {".ufo/waves/round-57/w1/Seat.md": "14/14 met=True\n"}, {}, {"rows_no_receipt": 1, "met": False}),
        ("fabricated_tally", good({"operability": f"`{R57}` 99/99"}), {}, {}, {"tallies_unfound": 1, "met": False}),
        ("tally_only_in_non_receipt_blob", good({"operability": f"`{R57}` and `corpus/bag.txt` 7/7"}),
         {"corpus/bag.txt": "7/7\n"}, {}, {"tallies_unfound": 1, "met": False}),
        ("no_passing_receipt", good({"calibration": "`.ufo/waves/round-56/controls/after.txt` 0/8"}), {}, {},
         {"rows_no_passing_receipt": 1, "met": False}),
        ("symlinked_receipt", good({"operability": "`.ufo/waves/round-57/controls/link.txt` 14/14"}), {},
         {".ufo/waves/round-57/controls/link.txt": "after.txt"}, {"unresolved": 1, "met": False}),
        ("score_change_on_held_axis", good(scores={"operability": "9", "freshness": "10", "calibration": "2"}), {}, {},
         {"scores_held": 1, "met": False}),
        ("rows_reordered", good(order=("freshness", "operability", "calibration")), {}, {}, {"axes_ordered": 0, "met": False}),
        ("superseded_missing", table(GOOD) + sec56 + "\n" + sec57, {}, {}, {"superseded_kept": 0, "met": False}),
        ("superseded_in_html_comment", table(GOOD) + sec56 + "\n" + sec57 + "\n## Superseded\n\n<!--\n"
         + "\n".join(OLD.values()) + "\n-->\n", {}, {}, {"superseded_kept": 0, "met": False}),
        ("superseded_under_other_heading", table(GOOD) + sec56 + "\n" + sec57 + "\n## Notes\n\n"
         + "\n".join(f"> {v}" for v in OLD.values()) + "\n", {}, {}, {"superseded_kept": 0, "met": False}),
        ("duplicate_axis_table", table(GOOD) + table(OLD) + sec56 + "\n" + sec57 + "\n" + SUPER, {}, {},
         {"tables": 2, "met": False}),
        ("axis_table_in_fence", "```\n" + table(GOOD) + "```\n" + sec56 + "\n" + sec57 + "\n" + SUPER, {}, {},
         {"tables": 0, "met": False}),
        ("escaped_pipe_in_cell", good({"operability": f"a \\| b `{R57}` 14/14"}), {}, {}, {"met": True}),
        ("round_section_rewritten", table(GOOD) + sec56 + "\n" + sec57.replace("| c2 | operability | x |", "| c2 | operability | y |")
         + "\n" + SUPER, {}, {}, {"receipts_off_axis": 3, "met": False}),
        ("measured_round_self_certifies", good({"freshness": "`.ufo/waves/round-59/controls/r.txt` 1/1"},
                                               extra="## Round 59\n\n| Claim | Axis |\n|---|---|\n| c | freshness |\n\n"),
         {".ufo/waves/round-59/controls/r.txt": "1/1 met=True\n"}, {}, {"receipts_off_axis": 1, "met": False}),
        ("line_pointer_beyond_eof", good({"operability": f"`{R57}:99` 14/14"}), {}, {}, {"unresolved": 1, "met": False}),
    ]
    passed, total = 0, 0
    try:
        for name, sc, files, links, want in cases:
            total += 1
            try:
                d, rev, base = build(name, sc, files, links)
                res = measure(d, rev, base)
                bad = {k: (res.get(k), v) for k, v in want.items() if res.get(k) != v}
            except Exception as exc:  # a harness error fails the case
                bad = {"exception": f"{type(exc).__name__}: {exc}"}
            ok = not bad
            passed += ok
            print(f"  {'PASS' if ok else 'FAIL'} {name}" + ("" if ok else f"  {bad}"))
    finally:
        shutil.rmtree(work, ignore_errors=True)
    print(f"c59 axis-evidence selftest: {passed}/{total}")
    return 0 if passed == total else 1


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
          f"receipts_off_axis={res['receipts_off_axis']} rows_no_passing_receipt={res['rows_no_passing_receipt']} "
          f"tables={res['tables']} axes_ordered={res['axes_ordered']} "
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
