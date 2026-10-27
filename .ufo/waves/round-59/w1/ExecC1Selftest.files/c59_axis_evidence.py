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
    """C1 axis-evidence kill matrix: fixture cases over the counter, each case paired with a mutant it must kill.

    Every case builds a scratch git repository holding a SCORECARD.md (axis table + `## Round N` sections) and receipt
    files, commits a base revision and a measured revision, runs measure() and asserts the counters.  Every case names a
    mutant: a patched copy of the counter (source patch or attribute override) that must make the case FAIL.

    The matrix runs against the counter in this file and, when present, against the landed v2 counter kept next to it
    (c59_axis_evidence_v2_landed.py): the two revisions disagree on where a tally may be found (v1: any resolved blob of the
    cell; v2: an on-axis receipt only) and on how many axis tables a file may hold (v2 additionally counts them).

    Exit: 0 when every expectation holds and every mutant is killed, 1 otherwise, 2 on harness error.
    """
    import importlib.util
    import shutil
    import tempfile
    import types

    HERE = os.path.dirname(os.path.abspath(__file__))
    SCRATCH = os.environ.get("KAKE_C1_SELFTEST_TMP") or os.environ.get("TMPDIR") or tempfile.gettempdir()
    try:
        os.makedirs(SCRATCH, exist_ok=True)
        TMP = tempfile.mkdtemp(prefix="c1matrix-", dir=SCRATCH)
    except OSError as exc:
        print(f"selftest harness error: cannot create scratch dir: {exc}", file=sys.stderr)
        return 2

    HDR = "| Axis | Score | Evidence pointer | Last change |"
    SEP = "|---|---|---|---|"
    R58 = ["| Axis | Note |", "|---|---|", "| operability | new operability cell |",
           "| freshness | new freshness cell |", "| calibration | new calibration cell |"]
    R57 = ["| Axis | Note |", "|---|---|", "| operability | old operability cell |",
           "| freshness | old freshness cell |", "| calibration | old calibration cell |"]
    R57_FRESH = ["| Axis | Note |", "|---|---|", "| freshness | old freshness cell |"]
    BASE_ROWS = [("operability", "10", "`r57/oper.md` 2/2", "r57"),
                 ("freshness", "10", "`r57/fresh.md` 4/4", "r57"),
                 ("calibration", "5", "`r57/cal.md` 5/5", "r57")]
    CLEAN_ROWS = [("operability", "10", "`.ufo/waves/round-58/oper.md` 3/3", "r58"),
                  ("freshness", "10", "`.ufo/waves/round-58/fresh.md` 4/4", "r58"),
                  ("calibration", "5", "`.ufo/waves/round-58/cal.md` 5/5", "r58")]
    SUP = ["- operability: `r57/oper.md` 2/2", "- freshness: `r57/fresh.md` 4/4", "- calibration: `r57/cal.md` 5/5"]
    RECEIPTS = {".ufo/waves/round-58/oper.md": "operability receipt\nresult 3/3\n",
                ".ufo/waves/round-58/fresh.md": "freshness receipt\nresult 4/4\n",
                ".ufo/waves/round-58/cal.md": "calibration receipt\nresult 5/5\n"}

    def sc(rows, sections):
        out = ["# Kake scorecard", "", HDR, SEP]
        for r in rows:
            out.append("| " + " | ".join(r) + " |")
        for title, body in sections:
            out += ["", "## " + title, ""]
            out += body
        return "\n".join(out) + "\n"

    def base_files(rows=None, sections=None, extra=None):
        d = {"SCORECARD.md": sc(rows or BASE_ROWS, sections or [("Round 57", R57), ("Round 58", R58)])}
        d.update(extra or {})
        return d

    def clean_meas(rows=None, sections=None, extra=None):
        d = {"SCORECARD.md": sc(rows or CLEAN_ROWS, sections or [("Superseded round-57 cells", SUP), ("Round 58", R58)])}
        d.update(RECEIPTS)
        d.update(extra or {})
        return d

    CLEAN = {"unresolved": 0, "rows_no_receipt": 0, "receipts_off_axis": 0, "tallies_unfound": 0, "rows_no_tally": 0,
             "mismatches": 0, "rows": 3, "names_ok": True, "scores_held": 2, "superseded_kept": 3, "met": True}

    BASE_SHAPE_TEXT = (
        "# Kake scorecard\n\n" + HDR + "\n" + SEP + "\n"
        "| operability | 10 | `cli.mjs:935` `:836-839` `:932` `:393` `corpus/handoffs/cmdProbe-merge-fix.md` | r17 |\n"
        "| freshness | 10 | `corpus/claims` `corpus/knowledge/freshness-sweep.md` `corpus/lessons/round-17.md` `LOG.md` "
        "`/tmp/kake-r17/scout-claims.md` `/tmp/kake-r17/claims-delta.tsv` `/tmp/kake-r17/critic.md` "
        "`/tmp/kake-r17/reviewer-cites.md` `/tmp/kake-r17/scout-pins.md` `/tmp/kake-r17/scout-live.md` "
        "117/117 15/15 16/16 10/10 | r17 |\n"
        "| calibration | 2 | Round-58 calibration move: a bounded calibration improvement. | r58 |\n")

    BROKEN_ROW_TEXT = (
        "# Kake scorecard\n\n" + HDR + "\n" + SEP + "\n"
        "| operability | 10 | `.ufo/waves/round-58/oper.md` 3/3 | r58 |\n"
        "| freshness | 10 | `.ufo/waves/round-58/fresh.md` 4/4 | r58 |\n"
        "| calibration | 5 |\n"
        "\n## Superseded round-57 cells\n\n" + "\n".join(SUP) + "\n"
        "\n## Round 58\n\n" + "\n".join(R58) + "\n")

    def defect_rows(cell_op, cell_fr, cell_cal):
        return [("operability", "10", cell_op, "r58"), ("freshness", "10", cell_fr, "r58"),
                ("calibration", "5", cell_cal, "r58")]

    # --- fixture driver -------------------------------------------------------------
    def git(root, *args):
        e = {k: v for k, v in os.environ.items() if not k.startswith("GIT_")}
        e["LC_ALL"] = "C.UTF-8"
        return subprocess.run(["git", "-C", root, *args], stdout=subprocess.PIPE, stderr=subprocess.PIPE, env=e)

    def write_files(root, files):
        for rel, content in files.items():
            p = os.path.join(root, rel)
            if os.path.dirname(p):
                os.makedirs(os.path.dirname(p), exist_ok=True)
            if isinstance(content, tuple) and content[0] == "link":
                if os.path.lexists(p):
                    os.remove(p)
                os.symlink(content[1], p)
                continue
            mode = "wb" if isinstance(content, bytes) else "w"
            with open(p, mode, **({} if mode == "wb" else {"encoding": "utf-8", "newline": ""})) as fh:
                fh.write(content)

    def build_repo(base, meas):
        d = tempfile.mkdtemp(prefix="repo-", dir=TMP)
        if git(d, "init", "-q").returncode != 0:
            raise RuntimeError("git init failed")
        top = git(d, "rev-parse", "--show-toplevel").stdout.decode().strip()
        if os.path.realpath(top) != os.path.realpath(d):
            raise RuntimeError(f"fixture toplevel mismatch: {top} != {d}")
        ident = ["-c", "user.name=selftest", "-c", "user.email=selftest@local"]
        write_files(d, base)
        git(d, "add", "-A")
        if git(d, *ident, "commit", "-q", "-m", "base").returncode != 0:
            raise RuntimeError("base commit failed")
        base_rev = git(d, "rev-parse", "HEAD").stdout.decode().strip()
        write_files(d, meas)
        git(d, "add", "-A")
        if git(d, *ident, "commit", "-q", "--allow-empty", "-m", "measured").returncode != 0:
            raise RuntimeError("measured commit failed")
        meas_rev = git(d, "rev-parse", "HEAD").stdout.decode().strip()
        return d, base_rev, meas_rev

    # --- mutant machinery -----------------------------------------------------------
    def load_module(path, name):
        spec = importlib.util.spec_from_file_location(name, path)
        mod = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(mod)
        return mod

    def mutant_of(mod, spec):
        whole = open(mod.__file__, "r", encoding="utf-8").read()
        src, sep, tail = whole.partition("\ndef selftest()")
        for old, new in spec.get("patches", []):
            if src.count(old) != 1:
                raise RuntimeError(f"mutant anchor not unique ({src.count(old)}): {old[:70]!r}")
            src = src.replace(old, new)
        if spec.get("prepend"):
            fut = "from __future__ import annotations\n"
            if fut in src:
                src = src.replace(fut, fut + "\n" + spec["prepend"], 1)
            else:
                src = spec["prepend"] + src
        src = src + sep + tail
        m = types.ModuleType("mutant_" + os.path.basename(mod.__file__))
        m.__file__ = mod.__file__
        exec(compile(src, mod.__file__, "exec"), m.__dict__)
        for name, value in spec.get("attrs", {}).items():
            setattr(m, name, value(m) if callable(value) and getattr(value, "_factory", False) else value)
        return m

    def wrap_resolve(kind):
        def factory(mod):
            orig = mod.resolve

            def patched(root, rev, ptr, last_file):
                ok, f, why = orig(root, rev, ptr, last_file)
                if kind == "always_ok":
                    return True, None, "ok"
                if kind == "strip_slash" and ptr.startswith("/"):
                    return orig(root, rev, ptr.lstrip("/"), last_file)
                if kind == "strip_tilde" and ptr.startswith("~/"):
                    return orig(root, rev, ptr[2:], last_file)
                if kind == "strip_home" and ptr.startswith("/home/u/"):
                    return orig(root, rev, ptr[len("/home/u/"):], last_file)
                if kind == "docs_basename" and not ok and why.startswith("not a committed path"):
                    return orig(root, rev, "docs/" + os.path.basename(ptr), last_file)
                if kind == "ignore_line_bound" and not ok and why == "line beyond the file":
                    return True, None, "ok"
                if kind == "symlink_unresolved" and ok:
                    rc, out = mod.git(root, "ls-tree", rev, "--", ptr)
                    if rc == 0 and out.startswith(b"120000"):
                        return False, None, "symlink rejected"
                return ok, f, why
            patched._factory = False
            return patched
        factory._factory = True
        return factory

    def attr_fn(fn):
        """Mark a plain callable as the replacement attribute value itself (not a module-dependent factory)."""
        def wrapper(_mod):
            return fn
        wrapper._factory = True
        return wrapper

    CS_SPLIT = (
        "def _cs_split(line):\n"
        "    body = line.strip()\n"
        "    body = body[1:] if body.startswith('|') else body\n"
        "    body = body[:-1] if body.endswith('|') and not body.endswith('\\\\|') else body\n"
        "    out, cur, i, in_code = [], '', 0, False\n"
        "    while i < len(body):\n"
        "        ch = body[i]\n"
        "        if ch == '\\\\' and i + 1 < len(body) and body[i + 1] == '|':\n"
        "            cur += body[i:i + 2]\n"
        "            i += 2\n"
        "            continue\n"
        "        if ch == '`':\n"
        "            in_code = not in_code\n"
        "            cur += ch\n"
        "        elif ch == '|' and not in_code:\n"
        "            out.append(cur)\n"
        "            cur = ''\n"
        "        else:\n"
        "            cur += ch\n"
        "        i += 1\n"
        "    out.append(cur)\n"
        "    return [c.strip() for c in out]\n")

    # --- cases ----------------------------------------------------------------------
    CASES = []

    def case(name, base, meas, exp_v1, exp_v2, mut, note=""):
        CASES.append({"name": name, "base": base, "meas": meas, "v1": exp_v1, "v2": exp_v2, "mut": mut, "note": note})

    def P(old, new):
        return (old, new)

    # 1. the real base shape (16 mismatches under the frozen v1, 21 under the landed counter)
    BASE_SHAPE_FILES = {"SCORECARD.md": BASE_SHAPE_TEXT,
                        "corpus/handoffs/cmdProbe-merge-fix.md": "handoff\n",
                        "corpus/knowledge/freshness-sweep.md": "sweep\n",
                        "corpus/lessons/round-17.md": "lesson\n",
                        "LOG.md": "117/117 15/15 16/16 10/10\n"}
    case("base_shape_real", dict(BASE_SHAPE_FILES), dict(BASE_SHAPE_FILES),
         {"unresolved": 11, "rows_no_receipt": 3, "receipts_off_axis": 0, "tallies_unfound": 0, "rows_no_tally": 2,
          "mismatches": 16, "rows": 3, "scores_held": 2, "superseded_kept": 0, "met": False},
         {"unresolved": 11, "rows_no_receipt": 3, "receipts_off_axis": 0, "tallies_unfound": 4, "rows_no_tally": 3,
          "mismatches": 21, "rows": 3, "tables": 1, "scores_held": 2, "superseded_kept": 0, "met": False},
         {"attrs": {"resolve": wrap_resolve("always_ok")}},
         "lane base shape: 4 unresolved cli.mjs/line pointers, corpus/claims, six /tmp paths, four tallies")

    # 2. a clean minimal-true table (met)
    case("clean_minimal_true", base_files(), clean_meas(), dict(CLEAN), dict(CLEAN, tables=1),
         {"attrs": {"HELD": ()}}, "one axis table, three on-axis receipts, tallies present, superseded cells kept")

    # 3. emptied cells
    case("emptied_evidence_cells", base_files(), clean_meas(rows=defect_rows("", "", "")),
         {"unresolved": 0, "rows_no_receipt": 3, "receipts_off_axis": 0, "tallies_unfound": 0, "rows_no_tally": 3,
          "mismatches": 6, "rows": 3, "scores_held": 2, "superseded_kept": 3, "met": False},
         {"unresolved": 0, "rows_no_receipt": 3, "receipts_off_axis": 0, "tallies_unfound": 0, "rows_no_tally": 3,
          "mismatches": 6, "rows": 3, "tables": 1, "scores_held": 2, "superseded_kept": 3, "met": False},
         {"attrs": {"pointers": attr_fn(lambda cell: ["phantom.md"])}},
         "empty evidence cell: no pointer, no receipt, no tally")

    # 4. /tmp pointer
    case("tmp_pointer", base_files(),
         clean_meas(rows=defect_rows("`/tmp/x.md` 3/3", "`.ufo/waves/round-58/fresh.md` 4/4",
                                     "`.ufo/waves/round-58/cal.md` 5/5"),
                    extra={"tmp/x.md": "tmp copy\n"}),
         {"unresolved": 1, "rows_no_receipt": 1, "receipts_off_axis": 0, "tallies_unfound": 1, "rows_no_tally": 1,
          "mismatches": 4, "rows": 3, "scores_held": 2, "superseded_kept": 3, "met": False},
         {"unresolved": 1, "rows_no_receipt": 1, "receipts_off_axis": 0, "tallies_unfound": 1, "rows_no_tally": 1,
          "mismatches": 4, "rows": 3, "tables": 1, "scores_held": 2, "superseded_kept": 3, "met": False},
         {"attrs": {"resolve": wrap_resolve("strip_slash")}},
         "absolute /tmp pointer never resolves; the same path relative to the root would")

    # 5. ~ pointer
    case("home_pointer", base_files(),
         clean_meas(rows=defect_rows("~/x.md 3/3", "`.ufo/waves/round-58/fresh.md` 4/4",
                                     "`.ufo/waves/round-58/cal.md` 5/5"),
                    extra={"x.md": "home copy\n"}),
         {"unresolved": 1, "rows_no_receipt": 1, "receipts_off_axis": 0, "tallies_unfound": 1, "rows_no_tally": 1,
          "mismatches": 4, "rows": 3, "scores_held": 2, "superseded_kept": 3, "met": False},
         {"unresolved": 1, "rows_no_receipt": 1, "receipts_off_axis": 0, "tallies_unfound": 1, "rows_no_tally": 1,
          "mismatches": 4, "rows": 3, "tables": 1, "scores_held": 2, "superseded_kept": 3, "met": False},
         {"attrs": {"resolve": wrap_resolve("strip_tilde")}},
         "home-relative pointer never resolves")

    # 6. absolute /home pointer
    case("absolute_home_pointer", base_files(),
         clean_meas(rows=defect_rows("/home/u/x.md 3/3", "`.ufo/waves/round-58/fresh.md` 4/4",
                                     "`.ufo/waves/round-58/cal.md` 5/5"),
                    extra={"x.md": "home copy\n"}),
         {"unresolved": 1, "rows_no_receipt": 1, "receipts_off_axis": 0, "tallies_unfound": 1, "rows_no_tally": 1,
          "mismatches": 4, "rows": 3, "scores_held": 2, "superseded_kept": 3, "met": False},
         {"unresolved": 1, "rows_no_receipt": 1, "receipts_off_axis": 0, "tallies_unfound": 1, "rows_no_tally": 1,
          "mismatches": 4, "rows": 3, "tables": 1, "scores_held": 2, "superseded_kept": 3, "met": False},
         {"attrs": {"resolve": wrap_resolve("strip_home")}},
         "absolute /home pointer never resolves")

    # 7. a bare name not at root
    case("bare_name_not_at_root", base_files(),
         clean_meas(rows=defect_rows("`notes.md` 3/3", "`.ufo/waves/round-58/fresh.md` 4/4",
                                     "`.ufo/waves/round-58/cal.md` 5/5"),
                    extra={"docs/notes.md": "7/7\n"}),
         {"unresolved": 1, "rows_no_receipt": 1, "receipts_off_axis": 0, "tallies_unfound": 1, "rows_no_tally": 1,
          "mismatches": 4, "rows": 3, "scores_held": 2, "superseded_kept": 3, "met": False},
         {"unresolved": 1, "rows_no_receipt": 1, "receipts_off_axis": 0, "tallies_unfound": 1, "rows_no_tally": 1,
          "mismatches": 4, "rows": 3, "tables": 1, "scores_held": 2, "superseded_kept": 3, "met": False},
         {"attrs": {"resolve": wrap_resolve("docs_basename")}},
         "notes.md exists only under docs/: a root-relative name does not resolve")

    # 8. file:LINE beyond EOF
    case("file_line_beyond_eof", base_files(),
         clean_meas(rows=defect_rows("`docs/a.md:99` 3/3", "`.ufo/waves/round-58/fresh.md` 4/4",
                                     "`.ufo/waves/round-58/cal.md` 5/5"),
                    extra={"docs/a.md": "one\ntwo\nthree\n"}),
         {"unresolved": 1, "rows_no_receipt": 1, "receipts_off_axis": 0, "tallies_unfound": 1, "rows_no_tally": 1,
          "mismatches": 4, "rows": 3, "scores_held": 2, "superseded_kept": 3, "met": False},
         {"unresolved": 1, "rows_no_receipt": 1, "receipts_off_axis": 0, "tallies_unfound": 1, "rows_no_tally": 1,
          "mismatches": 4, "rows": 3, "tables": 1, "scores_held": 2, "superseded_kept": 3, "met": False},
         {"attrs": {"resolve": wrap_resolve("ignore_line_bound")}},
         "line pointer past EOF does not resolve")

    # 9. :LINE continuation after an unresolved file
    case("line_continuation_after_unresolved", base_files(),
         clean_meas(rows=defect_rows("`docs/a.md` `missing.md` `:12` 3/3", "`.ufo/waves/round-58/fresh.md` 4/4",
                                     "`.ufo/waves/round-58/cal.md` 5/5"),
                    extra={"docs/a.md": "".join(f"line {i}\n" for i in range(1, 21))}),
         {"unresolved": 2, "rows_no_receipt": 1, "receipts_off_axis": 0, "tallies_unfound": 1, "rows_no_tally": 1,
          "mismatches": 5, "rows": 3, "scores_held": 2, "superseded_kept": 3, "met": False},
         {"unresolved": 2, "rows_no_receipt": 1, "receipts_off_axis": 0, "tallies_unfound": 1, "rows_no_tally": 1,
          "mismatches": 5, "rows": 3, "tables": 1, "scores_held": 2, "superseded_kept": 3, "met": False},
         {"patches": [P("elif not ok and not LINEONLY.match(p):\n                last_file = None",
                        "elif False:\n                pass")]},
         "a :LINE continuation after a failed pointer has no file to point into")

    # 10. brace expansion
    case("brace_expansion", base_files(),
         clean_meas(rows=defect_rows("`docs/{a,b}.md` 3/3", "`.ufo/waves/round-58/fresh.md` 4/4",
                                     "`.ufo/waves/round-58/cal.md` 5/5"),
                    extra={"docs/a.md": "a\n", "docs/b.md": "b\n"}),
         {"unresolved": 0, "rows_no_receipt": 1, "receipts_off_axis": 0, "tallies_unfound": 1, "rows_no_tally": 1,
          "mismatches": 3, "rows": 3, "scores_held": 2, "superseded_kept": 3, "met": False},
         {"unresolved": 0, "rows_no_receipt": 1, "receipts_off_axis": 0, "tallies_unfound": 1, "rows_no_tally": 1,
          "mismatches": 3, "rows": 3, "tables": 1, "scores_held": 2, "superseded_kept": 3, "met": False},
         {"attrs": {"expand": attr_fn(lambda tok: [tok])}},
         "{a,b} expands to two pointers, both resolving")

    # 11. a tree pointer (resolves, is not a receipt)
    case("tree_pointer", base_files(),
         clean_meas(rows=defect_rows("`docs/` 3/3", "`.ufo/waves/round-58/fresh.md` 4/4",
                                     "`.ufo/waves/round-58/cal.md` 5/5"),
                    extra={"docs/a.md": "a\n"}),
         {"unresolved": 0, "rows_no_receipt": 1, "receipts_off_axis": 0, "tallies_unfound": 1, "rows_no_tally": 1,
          "mismatches": 3, "rows": 3, "scores_held": 2, "superseded_kept": 3, "met": False},
         {"unresolved": 0, "rows_no_receipt": 1, "receipts_off_axis": 0, "tallies_unfound": 1, "rows_no_tally": 1,
          "mismatches": 3, "rows": 3, "tables": 1, "scores_held": 2, "superseded_kept": 3, "met": False},
         {"patches": [P('if kind not in ("blob", "tree"):', 'if kind != "blob":')]},
         "a tree resolves but is never a blob-backed receipt")

    # 12. an off-axis receipt (round section without the axis)
    case("off_axis_receipt",
         base_files(sections=[("Round 57", R57_FRESH), ("Round 58", R58)]),
         clean_meas(rows=defect_rows("`.ufo/waves/round-57/x.md` 3/3", "`.ufo/waves/round-58/fresh.md` 4/4",
                                     "`.ufo/waves/round-58/cal.md` 5/5"),
                    sections=[("Round 57", R57_FRESH), ("Superseded round-57 cells", SUP), ("Round 58", R58)],
                    extra={".ufo/waves/round-57/x.md": "round-57 receipt\nresult 3/3\n"}),
         {"unresolved": 0, "rows_no_receipt": 1, "receipts_off_axis": 1, "tallies_unfound": 0, "rows_no_tally": 0,
          "mismatches": 2, "rows": 3, "scores_held": 2, "superseded_kept": 3, "met": False},
         {"unresolved": 0, "rows_no_receipt": 1, "receipts_off_axis": 1, "tallies_unfound": 1, "rows_no_tally": 1,
          "mismatches": 4, "rows": 3, "tables": 1, "scores_held": 2, "superseded_kept": 3, "met": False},
         {"attrs": {"on_axis": attr_fn(lambda section, axis: True)}},
         "round 57 never claimed operability: the cited receipt is off-axis")

    # 13. a tally absent from every cited blob
    case("tally_absent_from_cited_blob", base_files(),
         clean_meas(rows=defect_rows("`.ufo/waves/round-58/oper.md` 7/7", "`.ufo/waves/round-58/fresh.md` 4/4",
                                     "`.ufo/waves/round-58/cal.md` 5/5"),
                    extra={".ufo/waves/round-58/oper.md": "operability receipt\nresult 6/6\n"}),
         {"unresolved": 0, "rows_no_receipt": 0, "receipts_off_axis": 0, "tallies_unfound": 1, "rows_no_tally": 1,
          "mismatches": 2, "rows": 3, "scores_held": 2, "superseded_kept": 3, "met": False},
         {"unresolved": 0, "rows_no_receipt": 0, "receipts_off_axis": 0, "tallies_unfound": 1, "rows_no_tally": 1,
          "mismatches": 2, "rows": 3, "tables": 1, "scores_held": 2, "superseded_kept": 3, "met": False},
         {"attrs": {"TALLY": attr_fn(re.compile(r"(?!x)x"))}},
         "the claimed 7/7 occurs in no cited blob")

    # 14. a tally present only in an uncited file
    case("tally_only_in_uncited_file", base_files(),
         clean_meas(rows=defect_rows("`.ufo/waves/round-58/oper.md` 7/7 `docs/notes.md`",
                                     "`.ufo/waves/round-58/fresh.md` 4/4", "`.ufo/waves/round-58/cal.md` 5/5"),
                    extra={".ufo/waves/round-58/oper.md": "operability receipt\nresult 6/6\n",
                           "docs/notes.md": "7/7\n"}),
         {"unresolved": 0, "rows_no_receipt": 0, "receipts_off_axis": 0, "tallies_unfound": 0, "rows_no_tally": 0,
          "mismatches": 0, "rows": 3, "scores_held": 2, "superseded_kept": 3, "met": True},
         {"unresolved": 0, "rows_no_receipt": 0, "receipts_off_axis": 0, "tallies_unfound": 1, "rows_no_tally": 1,
          "mismatches": 2, "rows": 3, "tables": 1, "scores_held": 2, "superseded_kept": 3, "met": False},
         {"v1": {"patches": [P("for b in blobs]", "for b in receipts]")]},
          "v2": {"patches": [P("for b in receipts]", "for b in blobs]")]}},
         "v1 searches every resolved blob, v2 only on-axis receipts: the uncited file decides")

    # 15. a score change on operability
    case("score_change_on_operability", base_files(),
         clean_meas(rows=[("operability", "9", "`.ufo/waves/round-58/oper.md` 3/3", "r58"),
                          ("freshness", "10", "`.ufo/waves/round-58/fresh.md` 4/4", "r58"),
                          ("calibration", "5", "`.ufo/waves/round-58/cal.md` 5/5", "r58")]),
         dict(CLEAN, scores_held=1, met=False), dict(CLEAN, tables=1, scores_held=1, met=False),
         {"patches": [P("base_cells[ax][1] == cur_cells[ax][1]", "True")]},
         "the operability score moved: only freshness is held")

    # 16. a removed calibration row
    case("removed_calibration_row", base_files(),
         clean_meas(rows=[("operability", "10", "`.ufo/waves/round-58/oper.md` 3/3", "r58"),
                          ("freshness", "10", "`.ufo/waves/round-58/fresh.md` 4/4", "r58")]),
         {"unresolved": 0, "rows_no_receipt": 0, "receipts_off_axis": 0, "tallies_unfound": 0, "rows_no_tally": 0,
          "mismatches": 0, "rows": 2, "names_ok": False, "scores_held": 2, "superseded_kept": 3, "met": False},
         {"unresolved": 0, "rows_no_receipt": 0, "receipts_off_axis": 0, "tallies_unfound": 0, "rows_no_tally": 0,
          "mismatches": 0, "rows": 2, "tables": 1, "names_ok": False, "scores_held": 2, "superseded_kept": 3,
          "met": False},
         {"patches": [P('names_ok = tuple(n.lower() for n in res["row_names"]) == AXES', "names_ok = True")]},
         "the calibration row is gone: two rows, axis order broken")

    # 17. reordered rows
    case("reordered_rows", base_files(),
         clean_meas(rows=[("freshness", "10", "`.ufo/waves/round-58/fresh.md` 4/4", "r58"),
                          ("operability", "10", "`.ufo/waves/round-58/oper.md` 3/3", "r58"),
                          ("calibration", "5", "`.ufo/waves/round-58/cal.md` 5/5", "r58")]),
         dict(CLEAN, names_ok=False, met=False), dict(CLEAN, tables=1, names_ok=False, met=False),
         {"patches": [P('names_ok = tuple(n.lower() for n in res["row_names"]) == AXES',
                        'names_ok = set(n.lower() for n in res["row_names"]) == set(AXES)')]},
         "the three rows exist but not in the AXES order")

    # 18. superseded cell missing
    case("superseded_cell_missing", base_files(),
         clean_meas(sections=[("Superseded round-57 cells", SUP[1:]), ("Round 58", R58)]),
         dict(CLEAN, superseded_kept=2, met=False), dict(CLEAN, tables=1, superseded_kept=2, met=False),
         {"patches": [P("bc[2] in outside", "True")]},
         "one base evidence cell was erased instead of kept")

    # 19. superseded cell altered by one byte
    case("superseded_cell_altered_one_byte", base_files(),
         clean_meas(sections=[("Superseded round-57 cells",
                               ["- operability: `r57/oper.md` 2/3", SUP[1], SUP[2]]), ("Round 58", R58)]),
         dict(CLEAN, superseded_kept=2, met=False), dict(CLEAN, tables=1, superseded_kept=2, met=False),
         {"patches": [P("bc[2] in outside", "bc[2][:10] in outside")]},
         "the kept copy differs from the base cell by one byte: not verbatim")

    # 20. superseded cell kept only inside the table
    case("superseded_kept_only_inside_table", base_files(rows=CLEAN_ROWS),
         clean_meas(sections=[("Round 58", R58)]),
         dict(CLEAN, superseded_kept=0, met=False), dict(CLEAN, tables=1, superseded_kept=0, met=False),
         {"v1": {"patches": [P('outside = "\\n".join(lines[:span[0]] + lines[span[1]:])', "outside = text")]},
          "v2": {"patches": [P('outside = "\\n".join(lines[:span[0]] + lines[span[1]:])', "outside = visible(text)")]}},
         "an unchanged cell that only lives inside the axis table is not 'kept'")

    # 21. a | inside a code span
    case("pipe_inside_code_span", base_files(),
         clean_meas(rows=[("operability", "10", "`docs/a.md|x` 3/4", "r58"),
                          ("freshness", "10", "note \\| `docs/b.md` 5/6", "r58"),
                          ("calibration", "5", "`.ufo/waves/round-58/cal.md` 5/5", "r58")],
                    extra={"docs/a.md": "a\n", "docs/b.md": "b\n"}),
         {"unresolved": 0, "rows_no_receipt": 2, "receipts_off_axis": 0, "tallies_unfound": 0, "rows_no_tally": 2,
          "mismatches": 4, "rows": 3, "names_ok": True, "scores_held": 2, "superseded_kept": 3, "met": False},
         {"unresolved": 1, "rows_no_receipt": 2, "receipts_off_axis": 0, "tallies_unfound": 0, "rows_no_tally": 2,
          "mismatches": 5, "rows": 3, "tables": 1, "names_ok": True, "scores_held": 2, "superseded_kept": 3,
          "met": False},
         {"v1": {"patches": [P('cells = [c.strip() for c in lines[j].strip().strip("|").split("|")]',
                              "cells = _cs_split(lines[j])")],
                 "prepend": CS_SPLIT},
          "v2": {"patches": [P('return [c.strip() for c in re.split(r"(?<!\\\\)\\|", body)]', "return _cs_split(body)")],
                 "prepend": CS_SPLIT}},
         "a pipe inside a code span splits the row; an escaped pipe does not")

    # 22. duplicated header (first table wins)
    case("duplicated_header_first_table_wins", base_files(),
         clean_meas(sections=[("Superseded round-57 cells", SUP), ("Round 58", R58),
                              ("Shadow", [HDR, SEP, "| shadow | 1 | `docs/a.md` | x |"])],
                    extra={"docs/a.md": "a\n"}),
         dict(CLEAN), dict(CLEAN, tables=2, met=False),
         {"v1": {"patches": [P("for i, ln in enumerate(lines):", "for i, ln in reversed(list(enumerate(lines))):")]},
          "v2": {"patches": [P("i = heads[0]", "i = heads[-1]")]}},
         "two tables carry the axis header; the first one is the axis table")

    # 23. CRLF line endings
    case("crlf_line_endings",
         {"SCORECARD.md": sc(BASE_ROWS, [("Round 57", R57), ("Round 58", R58)]).replace("\n", "\r\n")},
         {"SCORECARD.md": sc(CLEAN_ROWS, [("Superseded round-57 cells", SUP), ("Round 58", R58)]).replace("\n", "\r\n"),
          **RECEIPTS},
         dict(CLEAN), dict(CLEAN, tables=1),
         {"patches": [P("ln.strip() == HEADER", 'ln.strip(" ") == HEADER')]},
         "CRLF SCORECARD.md reads the same as the LF twin")

    # 24. a symlinked receipt
    case("symlinked_receipt", base_files(),
         clean_meas(rows=defect_rows("`.ufo/waves/round-58/link.md` 3/3", "`.ufo/waves/round-58/fresh.md` 4/4",
                                     "`.ufo/waves/round-58/cal.md` 5/5"),
                    extra={".ufo/waves/round-58/link.md": ("link", "docs/real.md"), "docs/real.md": "3/3\n"}),
         {"unresolved": 0, "rows_no_receipt": 0, "receipts_off_axis": 0, "tallies_unfound": 1, "rows_no_tally": 1,
          "mismatches": 2, "rows": 3, "scores_held": 2, "superseded_kept": 3, "met": False},
         {"unresolved": 0, "rows_no_receipt": 0, "receipts_off_axis": 0, "tallies_unfound": 1, "rows_no_tally": 1,
          "mismatches": 2, "rows": 3, "tables": 1, "scores_held": 2, "superseded_kept": 3, "met": False},
         {"attrs": {"resolve": wrap_resolve("symlink_unresolved")}},
         "git stores a symlink as a blob holding the target path: the receipt resolves but shows no tally")

    # 25. a receipt of the measured round itself
    case("receipt_of_measured_round",
         base_files(sections=[("Round 57", R57), ("Round 58", R58), ("Round 59", R58)]),
         clean_meas(rows=defect_rows("`.ufo/waves/round-59/x.md` 3/3", "`.ufo/waves/round-58/fresh.md` 4/4",
                                     "`.ufo/waves/round-58/cal.md` 5/5"),
                    sections=[("Superseded round-57 cells", SUP), ("Round 58", R58), ("Round 59", R58)],
                    extra={".ufo/waves/round-59/x.md": "round-59 receipt\nresult 3/3\n"}),
         dict(CLEAN), dict(CLEAN, tables=1, receipts_off_axis=1, rows_no_receipt=1, tallies_unfound=1,
                           rows_no_tally=1, mismatches=4, met=False),
         {"v1": {"attrs": {"on_axis": attr_fn(lambda section, axis: False)}},
          "v2": {"patches": [P("n < MEASURED_ROUND and visible(sec).strip() in vis", "n < MEASURED_ROUND")]}},
         "v2 only accepts receipts of rounds before the measured one")

    # 26. base revision without an axis table
    case("base_without_axis_table", {"SCORECARD.md": "# Kake scorecard\n\nno table here\n"}, clean_meas(),
         {"raises": "base revision has no axis table"}, {"raises": "base revision has no axis table"},
         {"patches": [P('raise RuntimeError("base revision has no axis table")', "base_rows = rows")]},
         "an unevaluable base is exit 2, never a silent miss")

    # 27. a row with fewer than four cells
    case("row_with_fewer_than_four_cells", base_files(),
         {"SCORECARD.md": BROKEN_ROW_TEXT, **RECEIPTS},
         {"unresolved": 0, "rows_no_receipt": 1, "receipts_off_axis": 0, "tallies_unfound": 0, "rows_no_tally": 1,
          "mismatches": 2, "rows": 3, "names_ok": True, "scores_held": 2, "superseded_kept": 3, "met": False},
         {"unresolved": 0, "rows_no_receipt": 1, "receipts_off_axis": 0, "tallies_unfound": 0, "rows_no_tally": 1,
          "mismatches": 2, "rows": 3, "tables": 1, "names_ok": True, "scores_held": 2, "superseded_kept": 3,
          "met": False},
         {"patches": [P("if len(cells) < 4:\n            res[\"rows_no_receipt\"] += 1\n            res[\"rows_no_tally\"] += 1",
                        "if len(cells) < 4:\n            pass")]},
         "a short row is charged as a missing receipt and a missing tally")

    # --- runner ---------------------------------------------------------------------
    def run_case(mod, c, exp, mutspec):
        d, base_rev, meas_rev = build_repo(c["base"], c["meas"])
        try:
            res = mod.measure(d, meas_rev, base_rev)
        except Exception as exc:
            res = {"raises": f"{type(exc).__name__}: {exc}"}
        finally:
            shutil.rmtree(d, ignore_errors=True)
        want_raise = exp.get("raises")
        if want_raise:
            ok = "raises" in res and want_raise in res["raises"]
            detail = res.get("raises", "no exception raised")
        else:
            bad = [(k, v, res.get(k)) for k, v in exp.items() if k != "raises" and res.get(k) != v]
            ok = not bad
            detail = "; ".join(f"{k}: want {v!r} got {g!r}" for k, v, g in bad)
        killed = None
        mspec = mutspec
        if isinstance(mutspec, dict) and ("v1" in mutspec or "v2" in mutspec):
            mspec = mutspec.get("v1" if getattr(mod, "_gen", "v1") == "v1" else "v2")
        if mspec:
            mm = mutant_of(mod, mspec)
            d2, b2, m2 = build_repo(c["base"], c["meas"])
            try:
                res2 = mm.measure(d2, m2, b2)
            except Exception as exc:
                res2 = {"raises": f"{type(exc).__name__}: {exc}"}
            finally:
                shutil.rmtree(d2, ignore_errors=True)
            if want_raise:
                killed = not ("raises" in res2 and want_raise in res2["raises"])
            else:
                killed = any(res2.get(k) != v for k, v in exp.items() if k != "raises")
        return ok, detail, killed, res

    targets = []
    live = load_module(os.path.join(HERE, "c59_axis_evidence.py"), "counter_under_test")
    live._gen = "v1"
    targets.append(("counter in this file (frozen contract v1 + selftest)", live))
    v2path = os.path.join(HERE, "c59_axis_evidence_v2_landed.py")
    if os.environ.get("KAKE_C1_SELFTEST_V2") == "1" and os.path.exists(v2path):
        landed = load_module(v2path, "counter_v2_landed")
        landed._gen = "v2"
        targets.append(("landed v2 counter (snapshot next to this file)", landed))

    total = passed = killed_count = 0
    failures = []
    for label, mod in targets:
        print(f"=== counter under test: {label} ===")
        for c in CASES:
            exp = c["v1"] if getattr(mod, "_gen", "v1") == "v1" else c["v2"]
            total += 1
            ok, detail, killed, res = run_case(mod, c, exp, c["mut"])
            if ok:
                passed += 1
            else:
                failures.append(f"{label}/{c['name']}: {detail}")
            if killed:
                killed_count += 1
            else:
                failures.append(f"{label}/{c['name']}: MUTANT SURVIVED (case did not fail on its mutant)")
            print(f"  {c['name']}: {'PASS' if ok else 'FAIL'} | mutant {'killed' if killed else 'SURVIVED'} | {c['note']}")
            if not ok:
                print(f"      {detail}")
    shutil.rmtree(TMP, ignore_errors=True)
    print(f"TALLY cases={total} passed={passed} failed={total - passed} mutants_killed={killed_count}")
    for f in failures:
        print("  FAIL " + f)
    return 0 if not failures else 1


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
