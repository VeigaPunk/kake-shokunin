#!/usr/bin/env python3
"""Fail when seat-handoff meta-text sits in corpus/knowledge/ entries (R98-D1).

Population: every corpus/knowledge/*.md (direct children) at --revision, read as
committed bytes via `git show`, or every *.md directly under --dir (fixtures).

Scanned: prose lines only. Lines inside fenced code blocks (``` or ~~~) are
exempt, so a quoted legitimate use inside a fence is not a finding. A fence that
never closes is a finding, because it would hide everything after it.

Two tiers, both printed, so nothing is suppressed silently:

GATE (exit 1 when any hit): text that only a drafting or integration handoff
produces, and that has no legitimate place in an admitted entry.
  drafted-by                   "Drafted by"                     seat attribution
  word-count-receipt           "word-count receipt"             seat receipt wording
  receipt-file                 "quotes-verified.txt"            seat receipt file
  body-word-count              "body is N words"                drafting count note
  l1-integrates                "the L1 integrates"              instruction to the lead
  heading-unbalanced-backtick  heading with an odd number of backticks (truncated tail)
  unclosed-fence               fence opened and never closed

REVIEW (printed as `review:`, never fails the gate): provenance voice that the
corpus's own `verified-at:` / `source:` convention uses legitimately. A human
judges each hit; the gate does not.
  this-seat            "this seat" (first-person provenance of a re-open)
  seat-id              known seat role prefix + CapitalisedName in a provenance cite
  seat-scratch-path    ".ufo/waves/round-N/w1/" receipt citation
  l1-integrates-future "L1 integrates" (not "the L1 integrates"): planned-step note

Exit: 0 clean (review hits allowed), 1 gate findings, 2 setup error.
"""
from __future__ import annotations

import argparse
import re
import subprocess
import sys
from pathlib import Path

KNOWLEDGE = "corpus/knowledge"

GATE_RULES: tuple[tuple[str, re.Pattern[str]], ...] = (
    ("drafted-by", re.compile(r"\bDrafted by\b")),
    ("word-count-receipt", re.compile(r"\bword-count receipt\b", re.IGNORECASE)),
    ("receipt-file", re.compile(r"\bquotes-verified\.txt\b")),
    ("body-word-count", re.compile(r"\bbody is \d+ words\b", re.IGNORECASE)),
    ("l1-integrates", re.compile(r"\bthe L1 integrates\b")),
)

REVIEW_RULES: tuple[tuple[str, re.Pattern[str]], ...] = (
    ("this-seat", re.compile(r"\bthis seat\b", re.IGNORECASE)),
    (
        "seat-id",
        re.compile(
            r"\b(?:Scout|Exec|Review|Critic|Sentinel|Mut|Scribe|Connector|Labrat"
            r"|Kumitate|Kengaku|Revenger)[A-Z][A-Za-z0-9]*\b"
        ),
    ),
    ("seat-scratch-path", re.compile(r"\.ufo/waves/round-\d+/w1/")),
    ("l1-integrates-future", re.compile(r"(?<!the )\bL1 integrates\b")),
)

HEADING = re.compile(r"^#{1,6}\s")
FENCE_OPEN = re.compile(r"^ {0,3}(`{3,}|~{3,})")


def scan_text(text: str) -> tuple[list[tuple[int, list[str], str]], list[tuple[int, list[str], str]]]:
    """Return (gate_hits, review_hits); each hit is (line_no, rule_ids, line)."""
    gate: list[tuple[int, list[str], str]] = []
    review: list[tuple[int, list[str], str]] = []
    lines = text.split("\n")
    fence_char = ""
    fence_len = 0
    fence_start = 0
    for no, line in enumerate(lines, start=1):
        if fence_char:
            m = FENCE_OPEN.match(line)
            if m and m.group(1)[0] == fence_char and len(m.group(1)) >= fence_len \
                    and line.strip() == m.group(1):
                fence_char = ""
            continue
        m = FENCE_OPEN.match(line)
        if m:
            fence_char = m.group(1)[0]
            fence_len = len(m.group(1))
            fence_start = no
            continue
        g = [rid for rid, rx in GATE_RULES if rx.search(line)]
        if HEADING.match(line) and line.count("`") % 2 == 1:
            g.append("heading-unbalanced-backtick")
        if g:
            gate.append((no, g, line))
        r = [rid for rid, rx in REVIEW_RULES if rx.search(line)]
        if r:
            review.append((no, r, line))
    if fence_char:
        gate.append((fence_start, ["unclosed-fence"], lines[fence_start - 1]))
    return gate, review


def setup_fail(msg: str) -> int:
    print(f"knowledge_metatext_lint: setup error: {msg}", file=sys.stderr)
    return 2


def git_bytes(root: Path, *args: str) -> bytes:
    proc = subprocess.run(
        ["git", "-C", str(root), *args], capture_output=True, check=False
    )
    if proc.returncode != 0:
        raise RuntimeError(
            f"git {' '.join(args)} rc={proc.returncode}: "
            f"{proc.stderr.decode('utf-8', 'replace').strip()}"
        )
    return proc.stdout


def load_revision(root: Path, rev: str) -> tuple[str, list[tuple[str, str]]]:
    commit = git_bytes(
        root, "rev-parse", "--verify", "--quiet", f"{rev}^{{commit}}"
    ).decode().strip()
    names = git_bytes(root, "ls-tree", "-r", "-z", "--name-only", commit, "--", KNOWLEDGE)
    depth = KNOWLEDGE.count("/") + 1
    paths = [
        p for p in names.decode("utf-8", "replace").split("\0")
        if p.endswith(".md") and p.count("/") == depth
    ]
    out = []
    for p in sorted(paths):
        blob = git_bytes(root, "show", f"{commit}:{p}")
        out.append((Path(p).name, blob.decode("utf-8", "replace")))
    return commit, out


def load_dir(d: Path) -> list[tuple[str, str]]:
    return [
        (p.name, p.read_bytes().decode("utf-8", "replace"))
        for p in sorted(d.glob("*.md"))
    ]


def _short(line: str) -> str:
    s = line.strip()
    return s if len(s) <= 160 else s[:157] + "..."


def run_scan(entries: list[tuple[str, str]], label: str) -> int:
    gate_total = 0
    review_total = 0
    for name, text in entries:
        gate, review = scan_text(text)
        for no, rules, line in gate:
            gate_total += 1
            print(f"{KNOWLEDGE}/{name}:{no}: gate {','.join(rules)} | {_short(line)}")
        for no, rules, line in review:
            review_total += 1
            print(f"{KNOWLEDGE}/{name}:{no}: review {','.join(rules)} | {_short(line)}")
    print(
        f"knowledge_metatext_lint: {label} files={len(entries)} "
        f"gate_findings={gate_total} review_hits={review_total}"
    )
    return 1 if gate_total else 0


# (label, text, expected gate rules, expected review rules)
SELFTEST: tuple[tuple[str, str, set[str], set[str]], ...] = (
    (
        "P1 leaked handoff heading with drafting tail (line 130 shape)",
        "## Errata sweep (round 97)`; body is 103 words (word-count receipt in quotes-verified.txt). "
        "Drafted by ScoutErrata; the L1 integrates it.\n",
        {"drafted-by", "body-word-count", "word-count-receipt", "receipt-file",
         "l1-integrates", "heading-unbalanced-backtick"},
        {"seat-id"},
    ),
    (
        "P2 'Drafted by' seat attribution in prose",
        "Drafted by ExecStale for this wave.\n",
        {"drafted-by"},
        {"seat-id"},
    ),
    (
        "P3 'the L1 integrates' instruction to the lead",
        "This row is provisional; the L1 integrates it after review.\n",
        {"l1-integrates"},
        set(),
    ),
    (
        "P4 heading with an odd backtick count (truncated tail)",
        "## Use `cache-key construction\n\nBody.\n",
        {"heading-unbalanced-backtick"},
        set(),
    ),
    (
        "P5 unclosed fence hides the rest of the entry",
        "Intro.\n\n```text\nno closer follows\n",
        {"unclosed-fence"},
        set(),
    ),
    (
        "P6 receipt-file and body-count note outside a fence",
        "Checked against quotes-verified.txt; body is 88 words.\n",
        {"receipt-file", "body-word-count"},
        set(),
    ),
    (
        "R1 'this seat' provenance is review-only, never a gate finding",
        "verified-at: 2026-11-04 — this seat re-opened the RFC body itself.\n",
        set(),
        {"this-seat"},
    ),
    (
        "R2 seat scratch-path citation is review-only",
        "Receipts: .ufo/waves/round-98/w1/ExecStale/out.txt.\n",
        set(),
        {"seat-scratch-path", "seat-id"},
    ),
    (
        "N1 meta phrases quoted inside a backtick fence are exempt",
        "Example of a seat note:\n\n```text\nDrafted by ScoutErrata; this seat only reads.\n"
        "word-count receipt, the L1 integrates it, quotes-verified.txt, body is 9 words\n```\n\nProse after.\n",
        set(),
        set(),
    ),
    (
        "N2 tilde fence with the same phrases is exempt",
        "~~~\nDrafted by ExecStale; the L1 integrates it.\n~~~\n",
        set(),
        set(),
    ),
    (
        "N3 ordinary technical prose with near-miss words",
        "Execution order matters; critical paths and Critical thinking are fine. "
        "The Mutation of a header is a Scoutable idea in prose.\n",
        set(),
        set(),
    ),
    (
        "N4 plain heading and balanced inline code",
        "## Errata sweep (round 97)\n\nUse `cache-key` and `Vary` here.\n",
        set(),
        set(),
    ),
    (
        "N5 longer closer keeps a shorter inner fence inside; trailing 'seat belt' prose is clean",
        "````\nDrafted by X\n```\nstill inside\n````\n\nThe seat belt law is out of scope.\n",
        set(),
        set(),
    ),
)


def selftest() -> int:
    passed = 0
    for label, text, want_gate, want_review in SELFTEST:
        gate, review = scan_text(text)
        got_gate = {r for _no, rules, _l in gate for r in rules}
        got_review = {r for _no, rules, _l in review for r in rules}
        ok = got_gate == want_gate and got_review == want_review
        passed += ok
        status = "ok" if ok else "FAIL"
        print(
            f"{status} {label}: gate want={sorted(want_gate)} got={sorted(got_gate)}"
            f" | review want={sorted(want_review)} got={sorted(got_review)}"
        )
    n = len(SELFTEST)
    print(f"selftest {passed}/{n}")
    return 0 if passed == n else 1


def main(argv: list[str]) -> int:
    ap = argparse.ArgumentParser(description="knowledge meta-text gate (R98-D1)")
    ap.add_argument("--root", default=".", help="git repo root (default: .)")
    ap.add_argument("--revision", default="HEAD", help="committed revision to scan")
    ap.add_argument("--dir", help="scan *.md directly under this directory instead")
    ap.add_argument("--selftest", action="store_true", help="run built-in fixtures")
    args = ap.parse_args(argv)

    if args.selftest:
        return selftest()

    if args.dir:
        d = Path(args.dir)
        if not d.is_dir():
            return setup_fail(f"--dir {d} is not a directory")
        entries = load_dir(d)
        if not entries:
            return setup_fail(f"no *.md under {d}")
        return run_scan(entries, f"dir={d}")

    root = Path(args.root)
    try:
        commit, entries = load_revision(root, args.revision)
    except RuntimeError as exc:
        return setup_fail(str(exc))
    if not entries:
        return setup_fail(f"no {KNOWLEDGE}/*.md at revision {args.revision}")
    return run_scan(entries, f"revision={args.revision} commit={commit}")


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
