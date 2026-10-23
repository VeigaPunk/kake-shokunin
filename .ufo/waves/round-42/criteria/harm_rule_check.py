#!/usr/bin/env python3
"""Check the QUALITY criterion "frozen harm rule names each new fixture's class
and a numeric cost bound" against a SCORECARD's bytes for one round.

Usage:
    harm_rule_check.py <scorecard-path|-> <round>

`<round>` is a round number (41, 42, ...) or a phrase like "Round 41".
`<scorecard-path>` is a file holding the SCORECARD bytes; "-" reads stdin.

What it does:
  1. splits the bytes into "## Round N — ..." sections;
  2. selects the round's pre-freeze / declared section (a heading that says
     "pre-freeze" or "declared"); other sections (kill rule, measured results,
     wave-2 corrections, closure corrections) are ignored;
  3. extracts that section's harm-rule bullet (a bullet whose text names the
     harm rule, plus its indented continuation lines);
  4. passes only when the bullet
       (a) names the fixture classes, and
       (b) gives a numeric cost bound.

Exit codes:
  0  pass     - the harm rule names fixture classes and a numeric cost bound
  1  fail     - the harm rule exists but misses (a) or (b), or no harm rule
                 exists at all in the round's declared section
  2  cannot evaluate - the bytes cannot be read, the round has no declared /
                 pre-freeze section, or the section is unusable

Fixture classes (a) are named when the bullet mentions a change fixture and a
guard ("change fixture"/"red on" and "guard"/"green on"), or when it states
the single-class form ("guards only" or "no change fixture").

Numeric cost bound (b) is a ratio ("2.0 times", "2.0x", "<= 2.0", "at most
2.0") or a time ("250 ms", "5 s", "2 seconds").

Reporting style: every matched phrase is printed with the 1-based line number
it came from, so a reader can re-check the verdict by hand.
"""

from __future__ import annotations

import re
import sys

EXIT_PASS = 0
EXIT_FAIL = 1
EXIT_CANNOT = 2

# ---------------------------------------------------------------- sections

HEADING_RE = re.compile(r"^(#{2,6})\s+Round\s*(\d+)\b(.*)$", re.IGNORECASE)
ANY_HEADING_RE = re.compile(r"^#{1,6}\s")
DECLARED_KEYS = ("pre-freeze", "declared", "pre-freeze:", "before any seat")


def split_sections(lines):
    """Return [(heading_line_no, heading_text, start_line_no, end_line_no)]."""
    sections = []
    starts = []  # (line_no, heading_text, round_no)
    for i, line in enumerate(lines, start=1):
        m = HEADING_RE.match(line)
        if m:
            starts.append((i, line.strip(), int(m.group(2))))
    for idx, (line_no, heading, rnd) in enumerate(starts):
        end = len(lines)
        for j in range(line_no, len(lines)):
            if ANY_HEADING_RE.match(lines[j]):
                end = j
                break
        sections.append(
            {
                "line": line_no,
                "heading": heading,
                "round": rnd,
                "start": line_no,
                "end": end,
            }
        )
    return sections


def pick_declared_section(sections, rnd):
    """The round's pre-freeze / declared section, or None."""
    cands = [s for s in sections if s["round"] == rnd]
    if not cands:
        return None
    declared = []
    for s in cands:
        low = s["heading"].lower()
        if any(k in low for k in DECLARED_KEYS):
            declared.append(s)
    if not declared:
        return None
    prefrozen = [s for s in declared if "pre-freeze" in s["heading"].lower()]
    pool = prefrozen or declared
    return pool[0], pool[1:]  # first pick, plus the other candidates


# ------------------------------------------------------------- the bullet

def extract_harm_bullets(lines, section):
    """Harm-rule bullets inside a section: [(first_line_no, last_line_no, text)]."""
    out = []
    i = section["start"]
    end = section["end"]
    while i < end:
        line = lines[i - 1]
        if line.startswith("- ") and re.search(r"harm\s+rule", line, re.IGNORECASE):
            first = i
            j = i + 1
            while j < end:
                nxt = lines[j - 1]
                if nxt.strip() == "":
                    break
                if nxt.startswith("- ") or ANY_HEADING_RE.match(nxt):
                    break
                if not nxt.startswith((" ", "\t")):
                    break
                j += 1
            text = "\n".join(lines[first - 1 : j - 1])
            out.append((first, j - 1, text))
            i = j
        else:
            i += 1
    return out


def strip_markup(text):
    return text.replace("**", "").replace("__", "").replace("*", "")


# ------------------------------------------------------------- the checks

CHANGE_WORDS = (
    re.compile(r"change\s+fixture", re.IGNORECASE),
    re.compile(r"\bred\s+on\b", re.IGNORECASE),
    re.compile(r"\bchange\s+guard\b", re.IGNORECASE),
)
GUARD_WORDS = (
    re.compile(r"\bguards?\b", re.IGNORECASE),
    re.compile(r"\bgreen\s+on\b", re.IGNORECASE),
)
GUARDS_ONLY = re.compile(r"guards?\s+only", re.IGNORECASE)
NO_CHANGE_FIXTURE = re.compile(r"no\s+change\s+fixture", re.IGNORECASE)

RATIO_UNIT = re.compile(
    r"(?<![\w.])(\d+(?:\.\d+)?)\s*(?:times|x\b|×)", re.IGNORECASE
)
# a comparison against a bare number counts as a ratio only when the number is
# not the head of a time bound ("within 250 ms" is a time, not a ratio)
RATIO_CMP = re.compile(
    r"(?:≤|<=|at\s+most|no\s+more\s+than|not\s+more\s+than|max(?:imum)?)"
    r"\s*(\d+(?:\.\d+)?)\b"
    r"(?!\s*(?:ms|milliseconds?|secs?|seconds?|mins?|minutes?|s)\b)",
    re.IGNORECASE,
)
TIME_BOUND = re.compile(
    r"(?<![\w.,])(\d+(?:\.\d+)?)\s*"
    r"(?:ms|milliseconds?|secs?|seconds?|mins?|minutes?)\b",
    re.IGNORECASE,
)
TIME_BOUND_SHORT = re.compile(
    r"(?<![\w.,])(\d{1,5})\s+s\b", re.IGNORECASE
)


def line_hits(lines, first, last, patterns):
    """[(pattern_label, line_no, matched_text)] for matches inside the bullet.

    `patterns` is a sequence of compiled regexes; the label is the regex's
    `pattern` text, truncated for display.
    """
    hits = []
    for lno in range(first, last + 1):
        text = lines[lno - 1]
        plain = strip_markup(text)
        for rx in patterns:
            label = rx.pattern if len(rx.pattern) <= 16 else rx.pattern[:16] + "…"
            for m in rx.finditer(plain):
                hits.append((label, lno, m.group(0).strip()))
    return hits


def main(argv):
    if len(argv) != 3:
        sys.stderr.write("usage: harm_rule_check.py <scorecard-path|-> <round>\n")
        return EXIT_CANNOT
    path = argv[1]
    round_arg = argv[2].strip()

    m = re.search(r"(\d+)", round_arg)
    if not m:
        sys.stderr.write("harm_rule_check: cannot parse round %r\n" % round_arg)
        return EXIT_CANNOT
    rnd = int(m.group(1))

    try:
        if path == "-":
            raw = sys.stdin.buffer.read()
        else:
            with open(path, "rb") as fh:
                raw = fh.read()
    except OSError as exc:
        sys.stderr.write("harm_rule_check: cannot read %s: %s\n" % (path, exc))
        return EXIT_CANNOT

    text = raw.decode("utf-8", errors="replace")
    lines = text.split("\n")

    print("round %d, bytes %s (%d lines)" % (rnd, path, len(lines)))

    sections = split_sections(lines)
    picked = pick_declared_section(sections, rnd)
    if picked is None:
        print("VERDICT: cannot evaluate - no pre-freeze/declared section for round %d" % rnd)
        return EXIT_CANNOT
    section, others = picked
    print(
        "section: line %d %s (lines %d-%d)"
        % (section["line"], section["heading"], section["start"], section["end"])
    )
    for other in others:
        print("  (other candidate section ignored: line %d %s)" % (other["line"], other["heading"]))

    bullets = extract_harm_bullets(lines, section)
    if not bullets:
        print("harm-rule bullet: none found in lines %d-%d" % (section["start"], section["end"]))
        loose = [
            (lno, lines[lno - 1].strip())
            for lno in range(section["start"], section["end"] + 1)
            if re.search(r"\bharm", lines[lno - 1], re.IGNORECASE)
        ]
        if loose:
            print("  the section mentions 'harm' but has no harm-rule bullet:")
            for lno, txt in loose:
                print("    line %d: %s" % (lno, txt[:120]))
        else:
            print("  the section never mentions 'harm'")
        print("VERDICT: fail - the round's declared section has no harm-rule bullet")
        return EXIT_FAIL

    first, last, _text = bullets[0]
    print("harm-rule bullet: lines %d-%d" % (first, last))
    if len(bullets) > 1:
        print("  (further harm-rule bullets in this section: %s)" %
              ", ".join("lines %d-%d" % (b[0], b[1]) for b in bullets[1:]))

    change_hits = line_hits(lines, first, last, CHANGE_WORDS)
    guard_hits = line_hits(lines, first, last, GUARD_WORDS)
    only_hits = line_hits(lines, first, last, (GUARDS_ONLY,))
    nochg_hits = line_hits(lines, first, last, (NO_CHANGE_FIXTURE,))

    def show(label, hits):
        for lab, lno, matched in hits:
            print("  %-14s line %d: %r" % (lab, lno, matched))

    print("fixture-class evidence:")
    show("change", change_hits)
    show("guard", guard_hits)
    show("guards-only", only_hits)
    show("no-change-fix", nochg_hits)

    classes_ok = bool((change_hits and guard_hits) or only_hits or nochg_hits)
    if classes_ok:
        how = []
        if change_hits and guard_hits:
            how.append("change fixture and guard both named")
        if only_hits:
            how.append("'guards only'")
        if nochg_hits:
            how.append("'no change fixture'")
        print("  fixture classes: OK (%s)" % "; ".join(how))
    else:
        print("  fixture classes: MISSING (no change-fixture and guard naming,"
              " no 'guards only', no 'no change fixture')")

    cost_hits = []
    for label, rx in (
        ("ratio-unit", RATIO_UNIT),
        ("ratio-cmp", RATIO_CMP),
        ("time", TIME_BOUND),
        ("time-short", TIME_BOUND_SHORT),
    ):
        cost_hits.extend(line_hits(lines, first, last, (rx,)))
    print("cost-bound evidence:")
    show("cost", cost_hits)
    if cost_hits:
        print("  numeric cost bound: OK")
    else:
        print("  numeric cost bound: MISSING")

    # advisory, not gating
    frozen = line_hits(lines, first, last, (re.compile(r"frozen", re.IGNORECASE),))
    if frozen:
        print("advisory: the bullet says 'frozen' at line %d" % frozen[0][1])
    else:
        print("advisory: the bullet does not use the word 'frozen'")

    if classes_ok and cost_hits:
        print("VERDICT: pass - harm rule names fixture classes and a numeric cost bound")
        return EXIT_PASS
    if not classes_ok and not cost_hits:
        print("VERDICT: fail - harm rule names neither fixture classes nor a numeric cost bound")
    elif not classes_ok:
        print("VERDICT: fail - harm rule names no fixture class")
    else:
        print("VERDICT: fail - harm rule has no numeric cost bound")
    return EXIT_FAIL


if __name__ == "__main__":
    sys.exit(main(sys.argv))
