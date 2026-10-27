#!/usr/bin/env python3
"""Round-60 C1 counter — calibration: the SKILL.md gate-registry status labels of the 28 round 48-59
counters match their observed exits at the measured revision.

Contract: `.ufo/waves/round-60/contract.md` claim C1, version 1 + L1 amendments A2–A7 (declared
before any data; all tightenings except the A2 disambiguation).

  population    the 28 frozen member paths below (A4): at --revision each must exist as a regular
                blob with the SAME blob id it has at the base revision — else member_missing /
                member_changed and the member is not evaluated. A file matching the population regex
                `^\\.ufo/waves/round-(N)/(?:[a-z0-9-]+/)?c(N)_[a-z0-9_]+\\.py$` (same N twice,
                48 <= N <= 59) that is not in the frozen set -> extra_member. `members` counts frozen
                paths present unchanged. This counter's own file is not a member.
  row (A6)      one rendered Markdown table row of SKILL.md — not inside fenced/indented code or an
                HTML comment — in a table whose header's first three cells are `Name`, `Kind`,
                `Entry command`, whose `Entry command` cell contains the member path. 0 counted rows
                -> `unregistered`; >1 counted rows, or the path in any OTHER rendered table row
                (any table, any cell) -> `duplicate_row`. The row needs exactly 8 non-empty cells
                (cells split honoring `\\|`) and a `Verdict map` cell holding `0=` and `1=` -> else
                `row_incomplete`.
  label (A5)    `historical` if the Kind cell holds the ASCII word `historical`, `never-met` if it
                holds the words `never met`, else `live`; both -> `label_invalid`.
                historical/never-met need a 40-hex revision in the Kind cell (first = pin) -> else
                `unpinned`; the pin must be an ancestor of the measured revision (strict for
                never-met) -> else `pin_not_ancestor`; the member file must exist at the pin -> else
                `member_absent_at_pin`.
  command (A2/A3) the first backtick span of the `Entry command` cell that contains the member path.
                A `[...]` segment is kept (brackets removed) iff it contains >=1 placeholder and
                every placeholder in it is `<scratch>` or `<fleet root>` — so `[--fleet
                <fleet root>]` is kept and `[--seed N]`, `[--json]`, `[--base <rev>]` are dropped.
                Leading `NAME=value` words are env assignments; only `TMPDIR=<scratch>` is allowed.
                After env words the words must be exactly `python3 -B <member path> <args...>`;
                args must contain `--revision` followed by a revision placeholder
                (`<commit>`/`<rev>`/`<revision>`/`<tip>`), must not contain `--selftest`, and if
                `--root` is present its value must be `.`. Any shell-metacharacter token
                (`|` `||` `&&` `;` `>` `<` `$(` backtick) -> `command_unparsable`. `<scratch>` -> a
                fresh scratch dir; `<fleet root>` -> /home/vgpnk/Projects/shokunin; the revision
                placeholder -> the revision under test.
  observation   the command runs via subprocess list (no shell) with sys.executable for python3,
                cwd = a fresh `git clone --shared` of --root detached at the revision under test,
                env = {PATH=/usr/bin:/bin, HOME=<scratch>, TMPDIR=<scratch>, LANG=C.UTF-8} — nothing
                else is inherited (GIT_*, PYTHON*, KAKE_* cannot leak). Timeout 1800 s -> 124. Exit
                at the measured revision = e_T; for historical/never-met members the same command
                also runs at the pin = e_P (the revision under test for that run is the pin).
  mismatch (A5) live: e_T != 0 -> live_not_green. historical needs e_T == 1 and e_P == 0: e_T == 0 ->
                historical_but_green; e_P != 0 -> historical_not_green_at_pin; e_T outside {0,1} ->
                historical_bad_exit. never-met needs e_T == 1 and e_P == 1: e_T == 0 or e_P == 0 ->
                never_met_but_green; e_T or e_P outside {0,1} -> never_met_bad_exit. Plus every
                structural class above. `mismatches` counts members with >=1 class; the printed
                class is the first in pipeline order.
  scores_held (A7) SCORECARD.md read via git at --revision only: exactly one axis table (header
                `| Axis | Score | ...`), exactly one row per axis (trimmed casefold), score cell
                with `**` and backticks stripped must equal 10/10/2 digit-exact -> count of axes
                holding (0..3).

Predicate (frozen):

    met: members == 28 AND mismatches == 0 AND scores_held == 3

Exits: 0 met, 1 not met, 2 unevaluable (--root not a repository toplevel, revision unresolved,
SKILL.md/SCORECARD.md unreadable, clone failure), 64 usage.
Output: one line per member `<path> label=<l> e_T=<n> [e_P=<n>] <ok|MISMATCH class>` plus an
indented `argv=` line with the rendered command(s) used, then
`C1 gate-status members=<n> mismatches=<k> scores_held=<s>/3 met=<True|False>`.

Read-only: everything runs in clones/fixtures under --work (else TMPDIR, else the system temp) and
they are removed on exit. No network.
"""
from __future__ import annotations

import argparse
import concurrent.futures
import json
import os
import re
import shlex
import shutil
import subprocess
import sys
import tempfile

PREDICATE = "met: members == 28 AND mismatches == 0 AND scores_held == 3"
SELF_PATH = ".ufo/waves/round-60/c60_gate_status.py"
FLEET_ROOT = "/home/vgpnk/Projects/shokunin"
TIMEOUT = 1800
EXPECTED_MEMBERS = 28
EXPECTED_SCORES = {"operability": 10, "freshness": 10, "calibration": 2}
POP_RX = re.compile(r"^\.ufo/waves/round-(\d+)/(?:[a-z0-9-]+/)?c(\d+)_[a-z0-9_]+\.py$")
HEX40 = re.compile(r"\b[0-9a-f]{40}\b")
ENV_RX = re.compile(r"^[A-Za-z_][A-Za-z0-9_]*=")
PLACEHOLDER = re.compile(r"<[^<>]*>")
REV_PH = ("<commit>", "<rev>", "<revision>", "<tip>")
SEG_PH = ("<scratch>", "<fleet root>")
WORD_RX = re.compile(r"[A-Za-z]+")
META = ("|", "&&", ";", ">", "$(", "`")
# pipeline order for the printed (first) class
CLASS_ORDER = ["member_missing", "member_changed", "extra_member", "unregistered", "duplicate_row",
               "row_incomplete", "label_invalid", "unpinned", "pin_not_ancestor",
               "member_absent_at_pin", "command_unparsable", "live_not_green",
               "historical_but_green", "historical_not_green_at_pin", "never_met_but_green",
               "historical_bad_exit", "never_met_bad_exit"]

# A4: the 28 frozen members — path -> blob id at the base revision 97cdc122…
FROZEN = {
    ".ufo/waves/round-48/c48_lint_count.py": "10200e918900229291ae41384523796606d1e49e",
    ".ufo/waves/round-48/c48_quote_truth.py": "c4d3c66cf7165d73cff80e1dbec0ecb8f0ae9838",
    ".ufo/waves/round-49/c49_order.py": "7ca940160ed4b0729e5cf110ca00b5acd807ab58",
    ".ufo/waves/round-49/c49_quote_truth.py": "0808c865234a4a2bc95905622871807c5c77ee1d",
    ".ufo/waves/round-50/c50_durable.py": "052b5ed5fad853e4bb57d234fe36f1bc3721c0a6",
    ".ufo/waves/round-50/c50_quote_class.py": "4f5992a5a4985f7ec313830bf13eb5c87ff6c0fc",
    ".ufo/waves/round-51/c51_quote_truth.py": "a9fc1734825d41ef4b9d8ccc342dc53af9a1e5bc",
    ".ufo/waves/round-51/c51_wave_ledger.py": "4652d68dfcd9c93527bbfce40cc1e17214274dd8",
    ".ufo/waves/round-52/c52_gate_registry.py": "1a86b71a6f244f26081e88115b67ff7f05bc011a",
    ".ufo/waves/round-52/c52_mutation_ladder.py": "7f655237501c7562d2007ce25a3f0b3ed7ccf667",
    ".ufo/waves/round-52/c52_quote_truth.py": "1bd6e78f80e69eb037e1083eb55487a9b6bd83a1",
    ".ufo/waves/round-52/c52_wave_ledger.py": "93891e1fe25288ca2678cb16df96a3ad87884090",
    ".ufo/waves/round-53/exec-quality-gate/c53_gate_truth.py":
        "63bd9cfd8d1af2cfb0058e2d97b44d2f7563b1c4",
    ".ufo/waves/round-54/c54_ops_debt.py": "cf5ae4022509142ed64da6ba6535a3f43f8d1178",
    ".ufo/waves/round-54/c54_s374_calib.py": "2058e1423680042bd90dbcb5f0d72d86929ce8a5",
    ".ufo/waves/round-55/c55_quote_truth.py": "1c4688c75028adf09112d7e82fc7856c2982786a",
    ".ufo/waves/round-55/c55_readme_index.py": "1a65be474aab47ac1e002f5a893fdda4de0071a6",
    ".ufo/waves/round-56/c56_quote_truth.py": "c48aa2ce1dd7dc4c2c198476e53e9230a861d4ea",
    ".ufo/waves/round-56/c56_selftally.py": "4b6942fa975fc7306cc21ca03a0003ebf8ff2851",
    ".ufo/waves/round-57/c57_idresolver_gate.py": "0ed0420355441af4d1442eb71f658b5ab1801fa2",
    ".ufo/waves/round-57/c57_quote_truth.py": "28f214d2c93308536d67bc3d03dd2e0b4a21ce6e",
    ".ufo/waves/round-57/c57_receipt_pins.py": "ffcd45773e1ab677f935e451b98289be8afad203",
    ".ufo/waves/round-58/c58_quote_truth.py": "cd99431df1a84b4de6a8608b05cb2b2b734a3847",
    ".ufo/waves/round-58/c58_receipt_rewrites.py": "410bbc7ba05a5355fceb313c68b81031416d2459",
    ".ufo/waves/round-58/c58_resolver_cases.py": "6e44c4531e64f470e79c63be59499d55ec8f025c",
    ".ufo/waves/round-59/c59_axis_evidence.py": "59b0c26dfc728f26866e94bce39ab1aa57111238",
    ".ufo/waves/round-59/c59_quote_truth.py": "d21822423dbaa58156253d6b0e83e78216d422f0",
    ".ufo/waves/round-59/c59_resolver_cases.py": "2de8206e91364c700047749939f37e72ae6dc5d4",
}


# ----------------------------------------------------------------------- git plumbing

def git_env():
    """inherited environment minus GIT_*/PYTHON_*/KAKE_* variables (they must never leak into
    git plumbing or member runs)."""
    return {k: v for k, v in os.environ.items()
            if not (k.startswith("GIT_") or k.startswith("PYTHON") or k.startswith("KAKE_"))}


def git(root, *args):
    proc = subprocess.run(["git", "-C", root, *args], stdout=subprocess.PIPE,
                          stderr=subprocess.DEVNULL, env=git_env())
    return proc.returncode, proc.stdout


def toplevel(root):
    rc, out = git(root, "rev-parse", "--show-toplevel")
    return out.decode("utf-8", "replace").strip() if rc == 0 else None


def is_toplevel(root):
    top = toplevel(root)
    return top is not None and os.path.realpath(top) == os.path.realpath(root)


def resolve_commit(root, rev):
    rc, out = git(root, "rev-parse", "--verify", "--quiet", rev + "^{commit}")
    return out.decode().strip() if rc == 0 else None


def show(root, rev, path):
    rc, out = git(root, "show", "%s:%s" % (rev, path))
    if rc != 0:
        return None
    try:
        return out.decode("utf-8")
    except UnicodeDecodeError:
        return None


def is_ancestor(root, anc, rev, strict=False):
    if strict and anc == rev:
        return False
    rc, _ = git(root, "merge-base", "--is-ancestor", anc, rev)
    return rc == 0


def entry_exists(root, rev, path):
    """the path resolves to a blob at rev."""
    rc, out = git(root, "rev-parse", "--verify", "--quiet", "%s:%s" % (rev, path))
    if rc != 0:
        return False
    rc2, t = git(root, "cat-file", "-t", out.decode().strip())
    return rc2 == 0 and t.decode().strip() == "blob"


def tree_entries(root, rev):
    """{path: (mode, oid)} for every committed path at rev, or None."""
    rc, out = git(root, "ls-tree", "-r", "-z", rev)
    if rc != 0:
        return None
    entries = {}
    for rec in out.decode("utf-8", "surrogateescape").split("\0"):
        if not rec:
            continue
        meta, path = rec.split("\t", 1)
        mode, _type, oid = meta.split(" ", 2)
        entries[path] = (mode, oid)
    return entries


def population_candidates(entries):
    return sorted(p for p in entries
                  if (m := POP_RX.match(p)) and m.group(1) == m.group(2)
                  and 48 <= int(m.group(1)) <= 59 and p != SELF_PATH)


# ----------------------------------------------------------------------- markdown tables

def _mask(text):
    """per-line flags: (inside fenced code block, comment already open when the line starts).
    A table row is rendered only when neither holds and it is indented <=3 spaces."""
    mask = []
    fence = None
    comment = False
    for line in text.split("\n"):
        mask.append((fence is not None, comment))
        s = line.strip()
        if fence is not None:
            if s.startswith(fence):
                fence = None
            continue
        if not comment:
            m = re.match(r"^(```+|~~~+)", s)
            if m:
                fence = m.group(1)
                continue
        t = line
        while t:
            if comment:
                j = t.find("-->")
                if j < 0:
                    break
                comment = False
                t = t[j + 3:]
            else:
                j = t.find("<!--")
                if j < 0:
                    break
                comment = True
                t = t[j + 4:]
    return mask


def _cells(line):
    return [c.strip() for c in re.split(r"(?<!\\)\|", line.strip().strip("|"))]


def _sep(line):
    return re.fullmatch(r"[\s:|-]+", line.strip()) is not None


def md_tables(text):
    """every rendered table: (header_cells, [(lineno, cells)]); fenced/commented/indented lines
    are invisible. A table is a header row, its separator, and contiguous data rows after it."""
    lines = text.split("\n")
    mask = _mask(text)
    rowlike = [i for i, l in enumerate(lines)
               if re.match(r"^ {0,3}\|", l) and not (mask[i][0] or mask[i][1])]
    tables = []
    k = 0
    while k < len(rowlike):
        i = rowlike[k]
        if k + 1 < len(rowlike) and rowlike[k + 1] == i + 1 and _sep(lines[i + 1]):
            header = _cells(lines[i])
            rws = []
            k += 2
            prev = i + 1
            while k < len(rowlike) and rowlike[k] == prev + 1:
                j = rowlike[k]
                if not _sep(lines[j]):
                    rws.append((j, _cells(lines[j])))
                prev = j
                k += 1
            tables.append((header, rws))
            continue
        k += 1
    return tables


def rows_mentioning(text, path):
    """linenos of rendered table data rows (any table, any cell) containing `path`."""
    lines = text.split("\n")
    mask = _mask(text)
    out = []
    for i, l in enumerate(lines):
        if mask[i][0] or mask[i][1] or not re.match(r"^ {0,3}\|", l) or _sep(l):
            continue
        if any(path in c for c in _cells(l)):
            out.append(i)
    return out


# ----------------------------------------------------------------------- command (A2/A3)

def command_words(span):
    """documented command -> (words, env assignments) after [...] segment drop/keep (A2), before
    placeholder substitution. None when not shlex-parsable."""
    segs = re.findall(r"\[[^\[\]]*\]", span)
    plain = re.sub(r"\[[^\[\]]*\]", " ", span)
    kept = [s[1:-1] for s in segs
            if (ph := PLACEHOLDER.findall(s)) and all(p in SEG_PH for p in ph)]
    text = " ".join((plain + " " + " ".join(kept)).split())
    # shlex would split the space in the recognized <fleet root> placeholder.
    text = text.replace("<fleet root>", "FLEETROOTPLACEHOLDER")
    try:
        words = shlex.split(text)
    except ValueError:
        return None
    words = [w.replace("FLEETROOTPLACEHOLDER", "<fleet root>") for w in words]
    env = {}
    while words and ENV_RX.match(words[0]):
        k, v = words.pop(0).split("=", 1)
        env[k] = v
    return words, env


def validate_command(words, env, member):
    """A3 shape check on the unsubstituted words; None or a problem string."""
    if set(env) - {"TMPDIR"} or env.get("TMPDIR") not in (None, "<scratch>"):
        return "env"
    if len(words) < 3 or words[0] != "python3" or words[1] != "-B" or words[2] != member:
        return "shape"
    args = words[3:]
    if not any(args[i] == "--revision" and i + 1 < len(args) and args[i + 1] in REV_PH
               for i in range(len(args))):
        return "revision"
    if "--selftest" in args:
        return "selftest"
    if "--root" in args:
        i = args.index("--root")
        if i + 1 >= len(args) or args[i + 1] != ".":
            return "root"
    for w in args:
        if w in REV_PH or w in SEG_PH:
            continue
        if any(c in w for c in META) or "<" in w:
            return "meta"
    return None


def render_argv(words, member, rev, scratch):
    """substitute placeholders -> executable argv (sys.executable stands in for python3)."""
    subs = {p: rev for p in REV_PH}
    subs["<scratch>"] = scratch
    subs["<fleet root>"] = FLEET_ROOT
    rendered = [PLACEHOLDER.sub(lambda m: subs.get(m.group(0), m.group(0)), w)
                for w in words[3:]]
    return [sys.executable, "-B", member] + rendered


def render_pretty(env, words, member, rev, scratch):
    """the documented command with placeholders substituted, as one printable string."""
    subs = {p: rev for p in REV_PH}
    subs["<scratch>"] = scratch
    subs["<fleet root>"] = FLEET_ROOT
    envw = ["%s=%s" % (k, PLACEHOLDER.sub(lambda m: subs.get(m.group(0), m.group(0)), v))
            for k, v in env.items()]
    argv = ["python3", "-B", member] + \
        [PLACEHOLDER.sub(lambda m: subs.get(m.group(0), m.group(0)), w) for w in words[3:]]
    return " ".join(envw + argv)


# ----------------------------------------------------------------------- observations

def clone_at(root, rev, dest):
    rc = subprocess.run(["git", "clone", "-q", "--shared", "--no-checkout", root, dest],
                        stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL, env=git_env()).returncode
    if rc != 0:
        raise RuntimeError("git clone --shared failed")
    rc2, _ = git(dest, "checkout", "-q", "--detach", rev)
    if rc2 != 0:
        raise RuntimeError("clone checkout of %s failed" % rev[:12])
    return dest


def run_member(root, words, member, run_rev, work):
    """one observation: fresh scratch + fresh shared clone detached at run_rev; fixed env
    (A3). Returns the member's exit code."""
    rdir = tempfile.mkdtemp(prefix="c60-run-", dir=work)
    try:
        scratch = os.path.join(rdir, "scratch")
        clone = os.path.join(rdir, "clone")
        os.mkdir(scratch)
        argv = render_argv(words, member, run_rev, scratch)
        clone_at(root, run_rev, clone)
        env = {"PATH": "/usr/bin:/bin", "HOME": scratch, "TMPDIR": scratch, "LANG": "C.UTF-8"}
        try:
            proc = subprocess.run(argv, cwd=clone, env=env, stdin=subprocess.DEVNULL,
                                  stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL,
                                  timeout=TIMEOUT)
            return proc.returncode
        except subprocess.TimeoutExpired:
            return 124
    finally:
        shutil.rmtree(rdir, ignore_errors=True)


# ----------------------------------------------------------------------- member evaluation

def eval_member(member, tables, skill, root, revid, work):
    res = {"member": member, "label": "-", "e_T": None, "e_P": None, "classes": [], "argv": {}}
    counted = []                                     # registry-table rows whose Entry cell has it
    for header, rws in tables:
        if header[:3] != ["Name", "Kind", "Entry command"]:
            continue
        ei, ki = 2, 1
        for lineno, cells in rws:
            if ei < len(cells) and member in cells[ei]:
                counted.append((header, cells, ki, ei, lineno))
    if not counted:
        res["classes"] = ["unregistered"]
        return res
    others = [ln for ln in rows_mentioning(skill, member)
              if ln not in {c[4] for c in counted}]
    if len(counted) > 1 or others:
        res["classes"] = ["duplicate_row"]
        return res
    header, cells, ki, ei, _ln = counted[0]
    nonempty = sum(1 for c in cells if c)
    vi = header.index("Verdict map") if "Verdict map" in header else -1
    vm = cells[vi] if 0 <= vi < len(cells) else ""
    if nonempty != 8 or not ("0=" in vm and "1=" in vm):
        res["classes"] = ["row_incomplete"]
        return res
    kind = cells[ki] if ki < len(cells) else ""
    words_lc = [w.lower() for w in WORD_RX.findall(kind)]
    has_hist = "historical" in words_lc
    has_nm = any(words_lc[i] == "never" and i + 1 < len(words_lc) and words_lc[i + 1] == "met"
                 for i in range(len(words_lc)))
    if has_hist and has_nm:
        res["classes"] = ["label_invalid"]
        return res
    label = "historical" if has_hist else ("never-met" if has_nm else "live")
    res["label"] = label
    pin = None
    if label in ("historical", "never-met"):
        m = HEX40.search(kind)
        if m is None:
            res["classes"].append("unpinned")
        else:
            cand = m.group(0)
            strict = label == "never-met"
            if is_ancestor(root, cand, revid, strict=strict):
                pin = cand
            else:
                res["classes"].append("pin_not_ancestor")
    span = next((s for s in re.findall(r"`([^`]+)`", cells[ei]) if member in s), None)
    parsed = command_words(span) if span is not None else None
    if parsed is None:
        res["classes"].append("command_unparsable")
        return res
    words, env = parsed
    if validate_command(words, env, member) is not None:
        res["classes"].append("command_unparsable")
        return res
    pin_run = label in ("historical", "never-met") and pin is not None
    if pin_run and not entry_exists(root, pin, member):
        res["classes"].append("member_absent_at_pin")
        pin_run = False
    res["argv"]["tip"] = render_pretty(env, words, member, revid, "<scratch>")
    res["e_T"] = run_member(root, words, member, revid, work)
    if pin_run:
        res["argv"]["pin"] = render_pretty(env, words, member, pin, "<scratch>")
        res["e_P"] = run_member(root, words, member, pin, work)
    e_T, e_P = res["e_T"], res["e_P"]
    if label == "live":
        if e_T != 0:
            res["classes"].append("live_not_green")
    elif label == "historical":
        if e_T == 0:
            res["classes"].append("historical_but_green")
        elif e_T != 1:
            res["classes"].append("historical_bad_exit")
        if e_P is not None and e_P != 0:
            res["classes"].append("historical_not_green_at_pin")
    elif label == "never-met":
        if e_T == 0 or e_P == 0:
            res["classes"].append("never_met_but_green")
        elif (e_T not in (0, 1)) or (e_P is not None and e_P not in (0, 1)):
            res["classes"].append("never_met_bad_exit")
    return res


# ----------------------------------------------------------------------- SCORECARD (A7)

def scores_held(text):
    """axes holding their base score: exactly one axis table, exactly one row per axis,
    `**`/backtick-stripped score cell digit-exact."""
    axis_tables = [(h, r) for h, r in md_tables(text)
                   if len(h) >= 2 and h[0].strip().casefold() == "axis"
                   and h[1].strip().casefold() == "score"]
    if len(axis_tables) != 1:
        return 0
    _header, rws = axis_tables[0]
    seen = {}
    for _ln, cells in rws:
        if len(cells) < 2:
            continue
        name = cells[0].strip().casefold()
        if name in EXPECTED_SCORES:
            seen[name] = seen.get(name, []) + [cells[1]]
    held = 0
    for name, want in EXPECTED_SCORES.items():
        vals = seen.get(name, [])
        if len(vals) != 1:
            continue
        v = vals[0].replace("**", "").replace("`", "").strip()
        if v == str(want):
            held += 1
    return held


# ----------------------------------------------------------------------- measure

def measure(root, revid, work, jobs, frozen=None):
    """(exit 0|1|2, results, scores_held, member count). `frozen` may be overridden by selftest;
    production always uses the hardcoded FROZEN set."""
    frozen = FROZEN if frozen is None else frozen
    skill = show(root, revid, "SKILL.md")
    scorecard = show(root, revid, "SCORECARD.md")
    entries = tree_entries(root, revid)
    if skill is None or scorecard is None or entries is None:
        return 2, [], 0, 0
    held = scores_held(scorecard)
    tables = md_tables(skill)
    present, results = [], []
    for path, want in sorted(frozen.items()):
        got = entries.get(path)
        if got is None:
            results.append({"member": path, "label": "-", "e_T": None, "e_P": None,
                            "classes": ["member_missing"], "argv": {}})
        elif got[0] not in ("100644", "100755") or got[1] != want:
            results.append({"member": path, "label": "-", "e_T": None, "e_P": None,
                            "classes": ["member_changed"], "argv": {}})
        else:
            present.append(path)
    for path in population_candidates(entries):
        if path not in frozen:
            results.append({"member": path, "label": "-", "e_T": None, "e_P": None,
                            "classes": ["extra_member"], "argv": {}})
    if jobs <= 1:
        results += [eval_member(m, tables, skill, root, revid, work) for m in present]
    else:
        with concurrent.futures.ThreadPoolExecutor(max_workers=jobs) as ex:
            results += [f.result() for f in
                        (ex.submit(eval_member, m, tables, skill, root, revid, work)
                         for m in present)]
    results.sort(key=lambda r: r["member"])
    mism = sum(1 for r in results if r["classes"])
    met = len(present) == EXPECTED_MEMBERS and mism == 0 and held == 3
    return (0 if met else 1), results, held, len(present)


def first_class(classes):
    return min(classes, key=lambda c: CLASS_ORDER.index(c)) if classes else None


def render_lines(results, held, members, met):
    out = []
    for r in results:
        line = "%s label=%s e_T=%s" % (r["member"], r["label"],
                                     r["e_T"] if r["e_T"] is not None else "-")
        if r["e_P"] is not None:
            line += " e_P=%s" % r["e_P"]
        line += " " + ("ok" if not r["classes"] else "MISMATCH " + first_class(r["classes"]))
        out.append(line)
        if r["argv"].get("tip"):
            out.append("    argv=%s" % r["argv"]["tip"])
        if r["argv"].get("pin"):
            out.append("    argv@pin=%s" % r["argv"]["pin"])
    out.append("C1 gate-status members=%d mismatches=%d scores_held=%d/3 met=%s"
               % (members, sum(1 for r in results if r["classes"]), held, met))
    return out


# ----------------------------------------------------------------------- selftest fixtures

TOY = '''#!/usr/bin/env python3
import os, sys
root = sys.argv[sys.argv.index("--root") + 1] if "--root" in sys.argv else "."
name = os.path.basename(__file__).replace(".py", "")
try:
    v = open(os.path.join(root, "v_" + name + ".txt")).read().strip()
except OSError:
    v = "1"
sys.exit(int(v) if v.isdigit() else 1)
'''

ASSERT = '''#!/usr/bin/env python3
import os, sys
a = sys.argv[1:]
ok = a[:2] == ["--root", "."] or "--root" in a and a[a.index("--root") + 1] == "."
ok = ok and "--revision" in a and len(a[a.index("--revision") + 1]) == 40
ok = ok and "--work" in a and a[a.index("--work") + 1] == os.environ.get("TMPDIR")
ok = ok and "--fleet" in a and a[a.index("--fleet") + 1] == "/home/vgpnk/Projects/shokunin"
for bad in ("--seed", "--json", "--bogus", "--selftest", "--base"):
    ok = ok and bad not in a
ok = ok and os.environ.get("TMPDIR") == os.environ.get("HOME")
ok = ok and os.path.isdir(os.environ["TMPDIR"])
ok = ok and os.environ.get("PATH") == "/usr/bin:/bin" and os.environ.get("LANG") == "C.UTF-8"
ok = ok and set(os.environ) == {"PATH", "HOME", "TMPDIR", "LANG"}
sys.exit(0 if ok else 7)
'''

ALL_PATHS = sorted(
    [".ufo/waves/round-48/c48_%s.py" % n for n in ("a", "b")] +
    [".ufo/waves/round-49/c49_%s.py" % n for n in ("a", "b")] +
    [".ufo/waves/round-50/c50_%s.py" % n for n in ("a", "b")] +
    [".ufo/waves/round-51/c51_%s.py" % n for n in ("a", "b")] +
    [".ufo/waves/round-52/c52_%s.py" % n for n in ("a", "b", "c", "d")] +
    [".ufo/waves/round-53/exec-quality-gate/c53_gate_truth.py"] +
    [".ufo/waves/round-54/c54_%s.py" % n for n in ("a", "b")] +
    [".ufo/waves/round-55/c55_%s.py" % n for n in ("a", "b")] +
    [".ufo/waves/round-56/c56_%s.py" % n for n in ("a", "b")] +
    [".ufo/waves/round-57/c57_%s.py" % n for n in ("a", "b", "c")] +
    [".ufo/waves/round-58/c58_%s.py" % n for n in ("a", "b", "c")] +
    [".ufo/waves/round-59/c59_%s.py" % n for n in ("a", "b", "c")])


def _w(root, files):
    for path, data in files.items():
        full = os.path.join(root, path)
        if data is None:
            if os.path.exists(full):
                os.remove(full)
            continue
        d = os.path.dirname(full)
        if d:
            os.makedirs(d, exist_ok=True)
        with open(full, "w") as fh:
            fh.write(data)


def _gitf(root, *args):
    subprocess.run(["git", "-C", root, *args], env=git_env(), check=True,
                   stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)


def _commit(root, msg):
    _gitf(root, "add", "-A")
    _gitf(root, "-c", "user.name=selftest", "-c", "user.email=selftest@local",
          "commit", "-q", "-m", msg)
    rc, out = git(root, "rev-parse", "HEAD")
    assert rc == 0
    return out.decode().strip()


def _init(root):
    os.makedirs(root, exist_ok=True)
    _gitf(root, "init", "-q")
    rc, out = git(root, "rev-parse", "--show-toplevel")
    assert rc == 0 and os.path.realpath(out.decode().strip()) == os.path.realpath(root)


def mrow(name, kind, path, tail=""):
    return ("| %s | %s | `python3 -B %s --root . --revision <commit>%s` | "
            "`0=met`; `1=not met`; `2=unevaluable`; `64=usage` | none | none | none | kake |"
            % (name, kind, path, tail))


SKILL_HEAD = ("# fixture\n\n| Name | Kind | Entry command | Verdict map | Self-test | "
              "Pinned values / frozen proof | Write scope | Owner |\n|---|---|---|---|---|---|---|---|\n")
SCORE_OK = ("# sc\n\n| Axis | Score | Evidence pointer | Last change |\n|---|---|---|---|\n"
            "| operability | 10 | e | r |\n| freshness | 10 | e | r |\n| calibration | 2 | e | r |\n")


def member_files(v0, v1, keep=None):
    """(stage0, stage1): every member counter + its verdict file at pin (v0) and tip (v1)."""
    keep = ALL_PATHS if keep is None else keep
    s0, s1 = {}, {}
    for p in keep:
        base = os.path.basename(p).replace(".py", "")
        s0[p] = TOY
        s1[p] = TOY
        s0["v_%s.txt" % base] = "%d\n" % v0.get(p, 1)
        s1["v_%s.txt" % base] = "%d\n" % v1.get(p, v0.get(p, 1))
    return s0, s1


def build_fixture(top, name, stage0, stage1, basis0=None):
    """git init + [basis commit] + pin commit + non-ancestor side commit + tip commit.
    @PIN@/@SIDE@/@BASIS@ tokens in later stages are substituted after each commit exists.
    Returns (dir, tip, pin, basis)."""
    d = os.path.join(top, name)
    _init(d)
    basis = None
    if basis0 is not None:
        _w(d, basis0)
        basis = _commit(d, "basis")
    _w(d, {p: (c if c is None or basis is None else c.replace("@BASIS@", basis))
           for p, c in stage0.items()})
    pin = _commit(d, "pin")
    _, br = git(d, "rev-parse", "--abbrev-ref", "HEAD")
    _gitf(d, "checkout", "-q", "-b", "side", pin)
    _w(d, {"side.txt": "side\n"})
    side = _commit(d, "side")
    _gitf(d, "checkout", "-q", br.decode().strip())
    _w(d, {p: (c if c is None else c.replace("@PIN@", pin).replace("@SIDE@", side))
           for p, c in stage1.items()})
    tip = _commit(d, "tip")
    return d, tip, pin, (basis or pin)


def fixture_frozen(root, rev):
    entries = tree_entries(root, rev) or {}
    return {p: entries[p][1] for p in ALL_PATHS if p in entries}


def selftest(work):
    """fixture lanes under `work` (each `git init`, selftest identity); prints a per-check tally."""
    top = tempfile.mkdtemp(prefix="c60-self-", dir=work)
    checks = []

    def ck(cid, cond):
        checks.append((cid, bool(cond)))

    try:
        # ---------- A: every row/label/observation class + substitutions ----------
        pin_v = {p: 0 for p in ALL_PATHS}
        tip_v = {p: 0 for p in ALL_PATHS}
        pin_v.update({".ufo/waves/round-52/c52_b.py": 1,    # red at pin -> historical_not_green_at_pin
                      ".ufo/waves/round-53/exec-quality-gate/c53_gate_truth.py": 1,
                      ".ufo/waves/round-54/c54_a.py": 0,
                      ".ufo/waves/round-57/c57_a.py": 1})   # never-met bad exit has red pin
        tip_v.update({".ufo/waves/round-50/c50_a.py": 1,
                      ".ufo/waves/round-50/c50_b.py": 2,
                      ".ufo/waves/round-52/c52_b.py": 1,
                      ".ufo/waves/round-52/c52_c.py": 1,
                      ".ufo/waves/round-52/c52_d.py": 1,
                      ".ufo/waves/round-54/c54_a.py": 1,
                      ".ufo/waves/round-54/c54_b.py": 1,
                      ".ufo/waves/round-55/c55_a.py": 1,
                      ".ufo/waves/round-57/c57_a.py": 1,
                      ".ufo/waves/round-57/c57_c.py": 2,
                      ".ufo/waves/round-58/c58_a.py": 1,
                      ".ufo/waves/round-58/c58_b.py": 1,
                      ".ufo/waves/round-59/c59_a.py": 1})
        # c52_a green both -> historical_but_green; c53_gate_truth e_T=0/e_P=1 -> never_met_but_green
        # c54_a e_T=1/e_P=0 -> never_met_but_green; c55_a red tip/green pin -> historical ok;
        # c57_c live exit 2 -> live_not_green
        s0, s1 = member_files(pin_v, tip_v)
        s1[".ufo/waves/round-56/c56_b.py"] = ASSERT
        s0[".ufo/waves/round-56/c56_b.py"] = ASSERT
        rows = [
            mrow("c48_b", "gate", ".ufo/waves/round-48/c48_b.py",
                 " [--fleet <fleet root>] [--seed N] [--json]"),
            mrow("c50_a", "gate", ".ufo/waves/round-50/c50_a.py"),
            mrow("c50_b", "gate", ".ufo/waves/round-50/c50_b.py"),
            mrow("c51_a", "gate", ".ufo/waves/round-51/c51_a.py"),
            mrow("c51_a_again", "gate", ".ufo/waves/round-51/c51_a.py"),
            # junk row: empty Verdict map -> 7 non-empty cells -> row_incomplete
            "| c51_b | gate | `python3 -B .ufo/waves/round-51/c51_b.py --revision <commit>` |"
            "  | x | y | z | w |",
            mrow("c52_a", "gate (historical: green at `@PIN@` only)",
                 ".ufo/waves/round-52/c52_a.py"),
            mrow("c52_b", "gate (historical: green at `@PIN@` only)",
                 ".ufo/waves/round-52/c52_b.py"),
            mrow("c52_c", "gate (historical, no pin recorded)",
                 ".ufo/waves/round-52/c52_c.py"),
            mrow("c52_d", "gate (historical: green at `@SIDE@` only)",
                 ".ufo/waves/round-52/c52_d.py"),
            mrow("gate_truth", "gate (never met: red at `@PIN@`)",
                 ".ufo/waves/round-53/exec-quality-gate/c53_gate_truth.py"),
            mrow("c54_a", "gate (never met: red at `@PIN@`)", ".ufo/waves/round-54/c54_a.py"),
            mrow("c54_b", "gate (never met, no pin)", ".ufo/waves/round-54/c54_b.py"),
            mrow("c55_a", "gate (historical: green at `@PIN@` only)",
                 ".ufo/waves/round-55/c55_a.py"),
            # junk row: only 7 cells -> row_incomplete
            "| c55_b | gate | `python3 -B .ufo/waves/round-55/c55_b.py --revision <commit>` |"
            " `0=met`; `1=not met` | a | b | c |",
            mrow("c56_a", "gate", ".ufo/waves/round-56/c56_a.py"),
            "| c56_b | gate | `TMPDIR=<scratch> python3 -B .ufo/waves/round-56/c56_b.py"
            " --root . --revision <commit> [--work <scratch>] [--fleet <fleet root>]"
            " [--seed N] [--json] [--base <rev>] [--bogus <nope>]` | `0=met`; `1=not met` |"
            " n | n | n | n |",
            mrow("c57_a", "gate", ".ufo/waves/round-57/c57_a.py"),
            "| c57_b | gate | `python -B .ufo/waves/round-57/c57_b.py --revision <commit>` |"
            " `0=met`; `1=not met` | n | n | n | n |",
            "| c57_c | gate | `python3 -B .ufo/waves/round-57/c57_c.py --revision <commit>` |"
            " `0=met`; `1=not met` | n | n | n | n | n |",   # 9 non-empty cells -> row_incomplete
            mrow("c58_a", "gate", ".ufo/waves/round-58/c58_a.py"),
            mrow("c58_b", "gate", ".ufo/waves/round-58/c58_b.py"),
            mrow("c58_c", "gate", ".ufo/waves/round-58/c58_c.py"),
            mrow("c59_a", "gate", ".ufo/waves/round-59/c59_a.py"),
            mrow("c59_b", "gate", ".ufo/waves/round-59/c59_b.py"),
            mrow("c59_c", "gate", ".ufo/waves/round-59/c59_c.py"),
        ]
        # c49_a's row inside a fence; c49_b's inside an HTML comment; c48_a has none.
        # c58_c's path also appears in a row of a different table -> duplicate_row (A6).
        fenced = "```\n" + mrow("c49_a", "gate", ".ufo/waves/round-49/c49_a.py") + "\n```\n"
        comrow = "<!--\n" + mrow("c49_b", "gate", ".ufo/waves/round-49/c49_b.py") + "\n-->\n"
        other = ("\n| Tool | Notes |\n|---|---|\n"
                 "| c58 helper | mentions `.ufo/waves/round-58/c58_c.py` here |\n")
        s0["SKILL.md"] = "placeholder\n"
        s0["SCORECARD.md"] = SCORE_OK
        s1["SKILL.md"] = SKILL_HEAD + "\n".join(rows) + "\n\n" + fenced + "\n" + comrow + other
        s1["SCORECARD.md"] = SCORE_OK
        dA, tipA, pinA, basisA = build_fixture(top, "A", s0, s1)
        fzA = fixture_frozen(dA, tipA)
        code, results, held, members = measure(dA, tipA, top, 4, frozen=fzA)
        bym = {r["member"]: r for r in results}
        want = {
            ".ufo/waves/round-48/c48_a.py": "unregistered",
            ".ufo/waves/round-48/c48_b.py": "ok",
            ".ufo/waves/round-49/c49_a.py": "unregistered",
            ".ufo/waves/round-49/c49_b.py": "unregistered",
            ".ufo/waves/round-50/c50_a.py": "live_not_green",
            ".ufo/waves/round-50/c50_b.py": "live_not_green",
            ".ufo/waves/round-51/c51_a.py": "duplicate_row",
            ".ufo/waves/round-51/c51_b.py": "row_incomplete",
            ".ufo/waves/round-52/c52_a.py": "historical_but_green",
            ".ufo/waves/round-52/c52_b.py": "historical_not_green_at_pin",
            ".ufo/waves/round-52/c52_c.py": "unpinned",
            ".ufo/waves/round-52/c52_d.py": "pin_not_ancestor",
            ".ufo/waves/round-53/exec-quality-gate/c53_gate_truth.py": "never_met_but_green",
            ".ufo/waves/round-54/c54_a.py": "never_met_but_green",
            ".ufo/waves/round-54/c54_b.py": "unpinned",
            ".ufo/waves/round-55/c55_a.py": "ok",
            ".ufo/waves/round-55/c55_b.py": "row_incomplete",
            ".ufo/waves/round-56/c56_a.py": "ok",
            ".ufo/waves/round-56/c56_b.py": "ok",
            ".ufo/waves/round-57/c57_a.py": "live_not_green",
            ".ufo/waves/round-57/c57_b.py": "command_unparsable",
            ".ufo/waves/round-57/c57_c.py": "row_incomplete",
            ".ufo/waves/round-58/c58_a.py": "live_not_green",
            ".ufo/waves/round-58/c58_b.py": "live_not_green",
            ".ufo/waves/round-58/c58_c.py": "duplicate_row",
            ".ufo/waves/round-59/c59_a.py": "live_not_green",
            ".ufo/waves/round-59/c59_b.py": "ok",
            ".ufo/waves/round-59/c59_c.py": "ok",
        }
        ck("A.exit1", code == 1)
        ck("A.members28", members == 28)
        ck("A.held3", held == 3)
        for p, w in sorted(want.items()):
            r = bym.get(p)
            got = "ok" if r and not r["classes"] else (first_class(r["classes"]) if r else "absent")
            ck("A.%s" % os.path.basename(p).replace(".py", ""), got == w)
        ck("A.c52b.eT1", bym[".ufo/waves/round-52/c52_b.py"]["e_T"] == 1)
        ck("A.c52b.eP1", bym[".ufo/waves/round-52/c52_b.py"]["e_P"] == 1)
        ck("A.c50b.eT2", bym[".ufo/waves/round-50/c50_b.py"]["e_T"] == 2)
        ck("A.c54a.eP0", bym[".ufo/waves/round-54/c54_a.py"]["e_P"] == 0)
        ck("A.argv", "--fleet /home/vgpnk/Projects/shokunin" in
           bym[".ufo/waves/round-48/c48_b.py"]["argv"]["tip"]
           and "--seed" not in bym[".ufo/waves/round-48/c48_b.py"]["argv"]["tip"])

        # ---------- B: clean (all ok -> exit 0) ----------
        pin_b = {p: 0 for p in ALL_PATHS}
        pin_b[".ufo/waves/round-53/exec-quality-gate/c53_gate_truth.py"] = 1   # never-met: red pin
        tip_b = {p: 0 for p in ALL_PATHS}
        tip_b[".ufo/waves/round-52/c52_a.py"] = 1            # historical: red tip, green pin
        tip_b[".ufo/waves/round-53/exec-quality-gate/c53_gate_truth.py"] = 1   # never-met: red tip
        s0b, s1b = member_files(pin_b, tip_b)
        rowsb = []
        for p in ALL_PATHS:
            name = os.path.basename(p).replace(".py", "")
            kind = ("gate (historical: green at `@PIN@` only)" if p.endswith("c52_a.py")
                    else "gate (never met: red at `@PIN@`)" if p.endswith("c53_gate_truth.py")
                    else "gate")
            tail = " [--work <scratch>]" if p.endswith("c58_a.py") else ""
            rowsb.append(mrow(name, kind, p, tail))
        s0b["SKILL.md"] = "placeholder\n"
        s0b["SCORECARD.md"] = SCORE_OK
        s1b["SKILL.md"] = SKILL_HEAD + "\n".join(rowsb) + "\n"
        s1b["SCORECARD.md"] = SCORE_OK
        dB, tipB, pinB, _ = build_fixture(top, "B", s0b, s1b)
        fzB = fixture_frozen(dB, tipB)
        code, resultsB, held, members = measure(dB, tipB, top, 4, frozen=fzB)
        ck("B.exit0", code == 0)
        ck("B.members28", members == 28)
        ck("B.allok", all(not r["classes"] for r in resultsB))
        ck("B.held3", held == 3)
        ck("B.cleanup", not any(x.startswith("c60-run-") for x in os.listdir(top)))

        # ---------- C: calibration-score mutant 2 -> 10 fails scores_held ----------
        s0c, s1c = member_files(pin_b, tip_b)
        s0c["SKILL.md"] = "placeholder\n"
        s0c["SCORECARD.md"] = SCORE_OK
        s1c["SKILL.md"] = s1b["SKILL.md"]
        s1c["SCORECARD.md"] = SCORE_OK.replace("| calibration | 2 |", "| calibration | 10 |")
        dC, tipC, _, _ = build_fixture(top, "C", s0c, s1c)
        code, resC, heldC, _ = measure(dC, tipC, top, 4, frozen=fixture_frozen(dC, tipC))
        ck("C.exit1", code == 1)
        ck("C.held2", heldC == 2)
        ck("C.mism0", all(not r["classes"] for r in resC))

        # ---------- D: member counts and identity (A4) ----------
        s0d, s1d = member_files(pin_b, tip_b, keep=ALL_PATHS[:-1])
        s0d["SKILL.md"] = "placeholder\n"
        s0d["SCORECARD.md"] = SCORE_OK
        s1d["SKILL.md"] = s1b["SKILL.md"]
        s1d["SCORECARD.md"] = SCORE_OK
        dD, tipD, _, _ = build_fixture(top, "D", s0d, s1d)
        fzD = fixture_frozen(dD, tipD)                 # frozen = the 27 present -> 28th missing
        fzD[ALL_PATHS[-1]] = "0" * 40                  # frozen path absent at rev
        codeD, resD, _, memD = measure(dD, tipD, top, 2, frozen=fzD)
        ck("D27.exit1", codeD == 1)
        ck("D27.members", memD == 27)
        ck("D27.missing", first_class(resD[-1]["classes"]) == "member_missing")
        s0e, s1e = member_files(pin_b, tip_b)
        for s in (s0e, s1e):
            s[".ufo/waves/round-59/c59_d.py"] = TOY
            s["v_c59_d.txt"] = "0\n"
        s0e["SKILL.md"] = "placeholder\n"
        s0e["SCORECARD.md"] = SCORE_OK
        s1e["SKILL.md"] = s1b["SKILL.md"] + mrow("c59_d", "gate",
                                                ".ufo/waves/round-59/c59_d.py") + "\n"
        s1e["SCORECARD.md"] = SCORE_OK
        dE, tipE, _, _ = build_fixture(top, "E", s0e, s1e)
        codeE, resE, _, memE = measure(dE, tipE, top, 2, frozen=fixture_frozen(dE, tipE))
        ck("E.extra_member", codeE == 1 and memE == 28
           and first_class({r["member"]: r for r in resE}
                           [".ufo/waves/round-59/c59_d.py"]["classes"]) == "extra_member")
        # a member whose blob differs at the tip -> member_changed
        s0m, s1m = member_files(pin_b, tip_b)
        s1m[".ufo/waves/round-50/c50_a.py"] = TOY + "\n# mutated\n"
        s0m["SKILL.md"] = "placeholder\n"
        s0m["SCORECARD.md"] = SCORE_OK
        s1m["SKILL.md"] = s1b["SKILL.md"]
        s1m["SCORECARD.md"] = SCORE_OK
        dM, tipM, pinM, _ = build_fixture(top, "M", s0m, s1m)
        fzM = fixture_frozen(dM, pinM)                 # frozen at the pin blob ids
        codeM, resM, _, memM = measure(dM, tipM, top, 2, frozen=fzM)
        ck("M.member_changed", codeM == 1
           and first_class({r["member"]: r for r in resM}
                           [".ufo/waves/round-50/c50_a.py"]["classes"]) == "member_changed")

        # ---------- F: SKILL.md absent at the tip -> unevaluable ----------
        s0f, s1f = member_files(pin_b, tip_b)
        s0f["SKILL.md"] = "placeholder\n"
        s0f["SCORECARD.md"] = SCORE_OK
        s1f["SKILL.md"] = None
        s1f["SCORECARD.md"] = SCORE_OK
        dF, tipF, _, _ = build_fixture(top, "F", s0f, s1f)
        codeF, _, _, _ = measure(dF, tipF, top, 2, frozen=fixture_frozen(dF, tipF))
        ck("F.noskill", codeF == 2)

        # ---------- G: inherited GIT_*/PYTHON_*/KAKE_* pollution must not matter ----------
        saved = {k: os.environ.get(k) for k in
                 ("GIT_DIR", "GIT_WORK_TREE", "GIT_INDEX_FILE", "PYTHONPATH", "KAKE_FOO")}
        os.environ.update({"GIT_DIR": "/nonexistent-git-dir",
                           "GIT_WORK_TREE": "/nonexistent-wt",
                           "GIT_INDEX_FILE": "/nonexistent-index",
                           "PYTHONPATH": "/nonexistent-py",
                           "KAKE_FOO": "x"})
        try:
            codeG, _, _, memG = measure(dB, tipB, top, 4, frozen=fzB)
            ck("G.envscrub", codeG == 0 and memG == 28)
        finally:
            for k, v in saved.items():
                os.environ.pop(k, None) if v is None else os.environ.__setitem__(k, v)

        # ---------- S: command-shape rejects (A3) ----------
        s0s, s1s = member_files({p: 0 for p in ALL_PATHS}, {p: 0 for p in ALL_PATHS})
        bad_cmds = [
            "| c48_a | gate | `python3 -B .ufo/waves/round-48/c48_a.py --revision <commit>` |"
            " `0=x`; `1=y` | n | n | n | n |",                              # no --root, still ok? no:
            # all of these are command_unparsable:
            "| c48_b | gate | `FOO=bar python3 -B .ufo/waves/round-48/c48_b.py --root ."
            " --revision <commit>` | `0=x`; `1=y` | n | n | n | n |",        # env word not TMPDIR
            "| c49_a | gate | `TMPDIR=/var/tmp python3 -B .ufo/waves/round-49/c49_a.py --root ."
            " --revision <commit>` | `0=x`; `1=y` | n | n | n | n |",        # TMPDIR not <scratch>
            "| c49_b | gate | `python3 .ufo/waves/round-49/c49_b.py --root ."
            " --revision <commit>` | `0=x`; `1=y` | n | n | n | n |",        # missing -B
            "| c50_a | gate | `python3 -B .ufo/waves/round-50/c50_a.py --root ."
            " --revision abc1234` | `0=x`; `1=y` | n | n | n | n |",         # rev not a placeholder
            "| c50_b | gate | `python3 -B .ufo/waves/round-50/c50_b.py --root ."
            " --revision <commit> --selftest` | `0=x`; `1=y` | n | n | n | n |",   # --selftest
            "| c51_a | gate | `python3 -B .ufo/waves/round-51/c51_a.py --root /x"
            " --revision <commit>` | `0=x`; `1=y` | n | n | n | n |",        # --root != .
            "| c51_b | gate | `python3 -B .ufo/waves/round-51/c51_b.py --root ."
            " --revision <commit> > out.txt` | `0=x`; `1=y` | n | n | n | n |",    # redirect
            "| c52_a | gate | `python3 -B .ufo/waves/round-52/c52_a.py --root ."
            " --revision <commit> && echo hi` | `0=x`; `1=y` | n | n | n | n |",   # &&
        ]
        rows_s = bad_cmds + [mrow(os.path.basename(p).replace(".py", ""), "gate", p)
                             for p in ALL_PATHS if p not in
                             (".ufo/waves/round-48/c48_a.py", ".ufo/waves/round-48/c48_b.py",
                              ".ufo/waves/round-49/c49_a.py", ".ufo/waves/round-49/c49_b.py",
                              ".ufo/waves/round-50/c50_a.py", ".ufo/waves/round-50/c50_b.py",
                              ".ufo/waves/round-51/c51_a.py", ".ufo/waves/round-51/c51_b.py",
                              ".ufo/waves/round-52/c52_a.py")]
        s0s["SKILL.md"] = "placeholder\n"
        s0s["SCORECARD.md"] = SCORE_OK
        s1s["SKILL.md"] = SKILL_HEAD + "\n".join(rows_s) + "\n"
        s1s["SCORECARD.md"] = SCORE_OK
        dS, tipS, _, _ = build_fixture(top, "S", s0s, s1s)
        codeS, resS, _, _ = measure(dS, tipS, top, 4, frozen=fixture_frozen(dS, tipS))
        byS = {r["member"]: r for r in resS}
        ck("S.no_root_ok", not byS[".ufo/waves/round-48/c48_a.py"]["classes"])
        for p in (".ufo/waves/round-48/c48_b.py", ".ufo/waves/round-49/c49_a.py",
                  ".ufo/waves/round-49/c49_b.py", ".ufo/waves/round-50/c50_a.py",
                  ".ufo/waves/round-50/c50_b.py", ".ufo/waves/round-51/c51_a.py",
                  ".ufo/waves/round-51/c51_b.py", ".ufo/waves/round-52/c52_a.py"):
            ck("S.%s" % os.path.basename(p).replace(".py", ""),
               first_class(byS[p]["classes"]) == "command_unparsable")

        # ---------- J: amendment classes (A4/A5/A6) ----------
        # commit plan: basis (all 28 members) -> pin (c49_b removed) -> side -> tip (c49_b re-added,
        # SKILL.md). c49_b never-met with pin=<pin>: member absent at pin -> member_absent_at_pin.
        pin_j = {p: 0 for p in ALL_PATHS}
        pin_j[".ufo/waves/round-57/c57_a.py"] = 1
        tip_j = {p: 0 for p in ALL_PATHS}
        tip_j.update({".ufo/waves/round-56/c56_a.py": 2,     # historical e_T=2 -> historical_bad_exit
                      ".ufo/waves/round-57/c57_a.py": 2})    # never-met e_T=2 -> never_met_bad_exit
        s0j, s1j = member_files(pin_j, tip_j)
        basis_j = {p: TOY for p in ALL_PATHS}
        basis_j.update({("v_%s.txt" % os.path.basename(p)[:-3]): "0\n" for p in ALL_PATHS})
        s0j[".ufo/waves/round-49/c49_b.py"] = None           # removed at the pin commit
        s0j["v_c49_b.txt"] = None
        rows_j = [
            mrow("c48_a", "gate (historical never met: `@PIN@`)", ".ufo/waves/round-48/c48_a.py"),
            mrow("c48_b", "gate (historicalish)", ".ufo/waves/round-48/c48_b.py"),
            mrow("c49_a", "gate", ".ufo/waves/round-49/c49_a.py"),
            mrow("c49_b", "gate (never met: red at `@PIN@`)", ".ufo/waves/round-49/c49_b.py"),
            mrow("c56_a", "gate (historical: green at `@PIN@` only)",
                 ".ufo/waves/round-56/c56_a.py"),
            mrow("c57_a", "gate (never met: red at `@PIN@`)", ".ufo/waves/round-57/c57_a.py"),
        ] + [mrow(os.path.basename(p).replace(".py", ""), "gate", p)
             for p in ALL_PATHS if os.path.basename(p)[:-3] not in
             ("c48_a", "c48_b", "c49_a", "c49_b", "c56_a", "c57_a")]
        s0j["SKILL.md"] = "placeholder\n"
        s0j["SCORECARD.md"] = SCORE_OK
        s1j["SKILL.md"] = SKILL_HEAD + "\n".join(rows_j) + "\n"
        s1j["SCORECARD.md"] = SCORE_OK
        dJ, tipJ, pinJ, basisJ = build_fixture(top, "J", s0j, s1j, basis0=basis_j)
        fzJ = fixture_frozen(dJ, basisJ)
        codeJ, resJ, _, _ = measure(dJ, tipJ, top, 4, frozen=fzJ)
        byJ = {r["member"]: r for r in resJ}
        ck("J.label_invalid", first_class(byJ[".ufo/waves/round-48/c48_a.py"]["classes"])
           == "label_invalid")
        ck("J.wordmatch_live", byJ[".ufo/waves/round-48/c48_b.py"]["label"] == "live")
        ck("J.absent_at_pin", first_class(byJ[".ufo/waves/round-49/c49_b.py"]["classes"])
           == "member_absent_at_pin")
        ck("J.hist_bad_exit", first_class(byJ[".ufo/waves/round-56/c56_a.py"]["classes"])
           == "historical_bad_exit")
        ck("J.nm_bad_exit", "never_met_bad_exit" in byJ[".ufo/waves/round-57/c57_a.py"]["classes"])
        ck("J.hist_eP_strict", byJ[".ufo/waves/round-56/c56_a.py"]["e_P"] == 0)

        # ---------- Q: score edge cases (A7) ----------
        for tag, card, want in (
            ("Q1", SCORE_OK.replace("| operability | 10 |", "| OPERABILITY | **10** |"), 3),
            ("Q2", SCORE_OK + "\n| Axis | Score | x | y |\n|---|---|---|---|\n"
             "| operability | 10 | e | r |\n", 0),
            ("Q3", SCORE_OK.replace("| freshness | 10 |", "| freshness | 10.0 |"), 2),
            ("Q4", SCORE_OK.replace("| calibration | 2 |",
                                    "| calibration | 2 |\n| calibration | 2 |"), 2),
        ):
            s0q, s1q = member_files(pin_b, tip_b)
            s0q["SKILL.md"] = "placeholder\n"
            s0q["SCORECARD.md"] = SCORE_OK
            s1q["SKILL.md"] = s1b["SKILL.md"]
            s1q["SCORECARD.md"] = card
            dQ, tipQ, _, _ = build_fixture(top, tag, s0q, s1q)
            _c, _r, heldQ, _m = measure(dQ, tipQ, top, 2, frozen=fixture_frozen(dQ, tipQ))
            ck("%s.held%d" % (tag, want), heldQ == want)

        # ---------- H: CLI exit codes through the real entry point ----------
        me = os.path.abspath(__file__)

        def cli(*args):
            p = subprocess.run([sys.executable, "-B", me, *args], cwd=top,
                               stdout=subprocess.PIPE, stderr=subprocess.STDOUT, text=True)
            return p.returncode, p.stdout

        rc, out = cli("--root", dB, "--revision", tipB, "--work", top, "--jobs", "4")
        ck("H.cli_runs", rc == 1 and "C1 gate-status" in out)
        rc, out = cli("--root", dA, "--revision", tipA, "--work", top)
        ck("H.cli_red", rc == 1 and "MISMATCH" in out)
        rc, _ = cli("--root", os.path.join(dA, "corpus"), "--revision", tipA)
        ck("H.cli_nontoplevel", rc == 2)
        rc, _ = cli("--root", dA, "--revision", "bogus-revision")
        ck("H.cli_badrev", rc == 2)
        rc, _ = cli("--root", dA)
        ck("H.cli_usage", rc == 64)
        rc, out = cli("--root", dB, "--revision", tipB, "--work", top, "--json")
        ck("H.cli_json", rc == 1 and '"predicate"' in out and '"results"' in out)
    finally:
        shutil.rmtree(top, ignore_errors=True)

    bad = [c for c, ok in checks if not ok]
    print("selftest %d/%d passed" % (len(checks) - len(bad), len(checks)))
    for c, ok in checks:
        print("  %s %s" % ("PASS" if ok else "FAIL", c))
    return 0 if not bad else 1


# ----------------------------------------------------------------------- cli

class Parser(argparse.ArgumentParser):
    def error(self, message):
        self.exit(64, "%s: %s\n" % (self.prog, message))


def main():
    ap = Parser(prog="c60_gate_status.py",
                description="round-60 C1: SKILL.md gate labels vs observed exits")
    ap.add_argument("--root")
    ap.add_argument("--revision")
    ap.add_argument("--work")
    ap.add_argument("--jobs", type=int, default=1)
    ap.add_argument("--json", action="store_true")
    ap.add_argument("--selftest", action="store_true")
    a = ap.parse_args()

    if a.selftest:
        work = a.work or os.environ.get("TMPDIR") or None
        if work:
            os.makedirs(work, exist_ok=True)
        return selftest(work)

    if not a.root or not a.revision:
        ap.exit(64, "c60_gate_status.py: --root and --revision are required\n")
    if a.jobs < 1:
        ap.exit(64, "c60_gate_status.py: --jobs must be >= 1\n")

    if not is_toplevel(a.root):
        print("unevaluable: --root %s is not a repository toplevel" % a.root)
        return 2
    top = toplevel(a.root)
    revid = resolve_commit(top, a.revision)
    if revid is None:
        print("unevaluable: --revision %s does not resolve to a commit" % a.revision)
        return 2

    own = a.work is None
    work = a.work or tempfile.mkdtemp(prefix="c60-work-",
                                      dir=os.environ.get("TMPDIR") or None)
    os.makedirs(work, exist_ok=True)
    try:
        code, results, held, members = measure(top, revid, work, a.jobs)
        met = code == 0
        if a.json:
            print(json.dumps({"revision": revid, "members": members, "scores_held": held,
                              "predicate": PREDICATE, "met": met, "exit": code,
                              "results": results}, indent=1))
        for line in render_lines(results, held, members, met):
            print(line)
        return code
    except (RuntimeError, OSError) as exc:
        print("unevaluable: %s" % exc)
        return 2
    finally:
        if a.work and os.path.isdir(a.work):
            for x in os.listdir(a.work):
                if x.startswith("c60-run-") or x.startswith("c60-self-"):
                    shutil.rmtree(os.path.join(a.work, x), ignore_errors=True)
        if own:
            shutil.rmtree(work, ignore_errors=True)


if __name__ == "__main__":
    sys.exit(main())
