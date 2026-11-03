#!/usr/bin/env python3
"""Round-72 C2 counter — hardened stale-/tmp-citation check for SKILL.md (v2 of the round-71 family).

Frozen before data (contract `.ufo/waves/round-72/contract.md`, section C2). This is a NEW numbered
counter; the frozen round-71 counter `.ufo/waves/round-71/c71_tmp.py` is untouched and its single-round
guard is superseded (it re-reddens on any later SKILL.md edit by design; recorded in the r72 lesson).

Predicate (the same sentence as contract.md section C2 and the receipt label):
  C2 met iff, at --revision over committed SKILL.md bytes,
      prose_findings == 0
  AND command_findings == 0
  AND brace_findings == 0
  AND guard_ok.
  A token is a path starting with the scratch root (built below so this file carries no literal).
  Findings per occurrence:
    brace      — the token opens a `${TMPDIR:-<root>...` default (a repoint that still falls back);
    command    — the occurrence sits inside a backticked span whose first word is one of the
                 command words below, or on a line whose first word is one (an imperative
                 command line): the round-71 phrase-only annotation kill (M5/J3) and the
                 `${TMPDIR:-/tmp}` repoint kill (ReviewContract F2);
    prose      — otherwise; tolerated only when the line carries the absence phrase
                 `not an executable instruction` (the dated-absence annotation).
  guard_ok (vs the frozen BASE revision):
    every line of BASE that carried a token either still appears (any content) or was removed,
    and every ADDED line that carries a token carries the absence phrase (annotated additions
    only); token-bearing lines may never silently lose their annotation.
  Revisions are read with `git show --end-of-options <rev>:<path>` (the round-71 M7 mitigation:
  a crafted revision is never parsed as an option).

Usage: c72_tmp_v2.py [--lane DIR] [--revision REV] [--selftest]
Exit: 0 met · 1 not met · 2 unevaluable · 64 usage. Reads committed bytes only (git show);
the selftest writes nothing (function-level fixtures).
"""
import collections
import re
import subprocess
import sys

LANE = "/home/vgpnk/Projects/shokunin/kake-shokunin"
BASE = "cc6b4e0b8c35e72dfb02c6184b847f68c1262153"
PATH = "SKILL.md"
PHRASE = "not an executable instruction"
TMP_ROOT = "/" + "tmp" + "/"
TOKEN_RE = re.compile(re.escape(TMP_ROOT) + r"[A-Za-z0-9_.\-/]*")
BRACE_TOKEN_RE = re.compile(r"\$\{TMPDIR:-" + re.escape(TMP_ROOT))
COMMAND_WORDS = frozenset({
    "node", "python", "python3", "cp", "mv", "git", "curl", "npx", "uv",
    "bash", "sh", "diff", "cat", "ls", "grep", "mktemp", "test",
})
SPAN_RE = re.compile(r"`([^`]*)`")


def command_span_words(span_text):
    s = span_text.strip()
    if not s:
        return None
    first = re.split(r"\s+", s, maxsplit=1)[0]
    first = first.strip("'\"")
    base = re.sub(r".*/", "", first)
    return base if base in COMMAND_WORDS else None


def line_findings(line):
    """Return (brace, command, prose) finding counts for one line."""
    brace_spans = [(m.start(), m.end()) for m in BRACE_TOKEN_RE.finditer(line)]
    brace = len(brace_spans)
    # mask out backticked spans for the imperative-line check
    bare = SPAN_RE.sub(" ", line)
    words = re.split(r"\s+", bare.strip(), maxsplit=1)
    imperative = bool(bare.strip()) and re.sub(r".*/", "", words[0].strip("'\"")) in COMMAND_WORDS
    command = 0
    prose = 0
    annotated = PHRASE in line
    spans = [(m.start(), m.end(), m.group(1)) for m in SPAN_RE.finditer(line)]
    for m in TOKEN_RE.finditer(line):
        pos = m.start()
        if any(s <= pos < e for s, e in brace_spans):
            continue  # counted once, as a brace finding
        in_cmd_span = any(s <= pos < e and command_span_words(txt) is not None
                          for s, e, txt in spans)
        if in_cmd_span or imperative:
            command += 1
        elif not annotated:
            prose += 1
    return brace, command, prose


def show(lane, rev):
    p = subprocess.run(
        ["git", "-C", lane, "show", "--end-of-options", f"{rev}:{PATH}"],
        capture_output=True, text=True,
    )
    if p.returncode != 0:
        print(f"C2 unevaluable: git show --end-of-options {rev}:{PATH} exit {p.returncode}",
              file=sys.stderr)
        sys.exit(2)
    return p.stdout.splitlines()


def evaluate(base_lines, tip_lines):
    bf = cf = pf = 0
    findings = []
    for n, line in enumerate(tip_lines, 1):
        b, c, p = line_findings(line)
        bf += b
        cf += c
        pf += p
        if b or c or p:
            findings.append((n, b, c, p))
    base_c = collections.Counter(base_lines)
    tip_c = collections.Counter(tip_lines)
    removed = base_c - tip_c
    added = tip_c - base_c
    guard_ok = all(PHRASE in line for line in added.elements() if TOKEN_RE.search(line))
    met = bf == 0 and cf == 0 and pf == 0 and guard_ok
    return met, findings, sum(removed.values()), sum(added.values()), guard_ok, bf, cf, pf


def main(argv):
    lane, rev, selftest = LANE, "HEAD", False
    args = list(argv)
    while args:
        a = args.pop(0)
        if a == "--lane" and args:
            lane = args.pop(0)
        elif a == "--revision" and args:
            rev = args.pop(0)
        elif a == "--selftest":
            selftest = True
        else:
            print(__doc__, file=sys.stderr)
            return 64
    if selftest:
        return self_test()
    base = show(lane, BASE)
    tip = show(lane, rev)
    met, findings, nrem, nadd, guard_ok, bf, cf, pf = evaluate(base, tip)
    print(
        f"C2v2 revision={rev} brace_findings={bf} command_findings={cf} prose_findings={pf} "
        f"findings={findings} removed={nrem} added={nadd} guard={'ok' if guard_ok else 'fail'} met={met}"
    )
    return 0 if met else 1


def self_test():
    cases = [
        # (name, line, want_brace, want_command, want_prose)
        ("prose_annotated_ok",
         "r11 (`/tmp/kake-r11/` artifacts [r71 absence: absent; historical record, not an executable instruction])",
         0, 0, 0),
        ("prose_unannotated_is_finding",
         "see the artifacts under /tmp/kake-r11/",
         0, 0, 1),
        ("j3_phrase_only_on_command_is_command_finding",
         "copy the snapshot first `cp state/probe-latest.json /tmp/kake-r12/live/backup.json` (historical record, not an executable instruction)",
         0, 1, 0),
        ("imperative_line_token_is_command_finding",
         "cp state/probe-latest.json /tmp/kake-r12/live/backup.json",
         0, 1, 0),
        ("mktemp_line_ok",
         'state/probe-latest.json "${BK:=$(mktemp -d)}/probe-latest.backup.json` → run → restore',
         0, 0, 0),
        ("brace_default_is_finding",
         "run the tool with TMPDIR=${TMPDIR:-/tmp/scratch} first",
         1, 0, 0),
        ("non_command_span_token_is_prose",
         "the snapshot lived at `/tmp/kake-r12/live/` (historical record, not an executable instruction)",
         0, 0, 0),
        ("command_span_without_token_ignored",
         "run `node scripts/freshness-sweep.mjs --offline` first",
         0, 0, 0),
    ]
    fails = 0
    for name, line, wb, wc, wp in cases:
        b, c, p = line_findings(line)
        ok = (b, c, p) == (wb, wc, wp)
        if not ok:
            fails += 1
        print(f"selftest {name}: got brace={b} command={c} prose={p} want={wb}/{wc}/{wp} {'OK' if ok else 'FAIL'}")
    # guard: added token line without the phrase fails the guard
    met, _, _, _, guard_ok, *_ = evaluate(
        ["clean line"], ["clean line", "new /tmp/kake-rX note without phrase"])
    g1 = guard_ok is False
    if not g1:
        fails += 1
    print(f"selftest guard_added_token_needs_phrase: {'OK' if g1 else 'FAIL'}")
    # guard: annotated added token line passes
    met2, _, _, _, guard_ok2, *_ = evaluate(
        ["clean line"], ["clean line", "new /tmp/kake-rX note (historical record, not an executable instruction)"])
    g2 = guard_ok2 is True
    if not g2:
        fails += 1
    print(f"selftest guard_annotated_addition_ok: {'OK' if g2 else 'FAIL'}")
    # able-to-fail vs v1: the J3 line is a finding here (v1 accepted it as annotated)
    j3 = line_findings("copy the snapshot first `cp state/x /tmp/kake-r12/backup.json` (historical record, not an executable instruction)")
    af = j3[1] == 1
    if not af:
        fails += 1
    print(f"selftest v1_accepted_j3_rejected_here: {'OK' if af else 'FAIL'}")
    total = len(cases) + 3
    print(f"C2v2 selftest {total - fails}/{total}")
    return 0 if fails == 0 else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
