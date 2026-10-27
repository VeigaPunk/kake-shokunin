#!/usr/bin/env python3
"""Round-63 C1 calibration counter — semantics-binding repair of the c62 family.

Round 62 routed defect 1: the frozen c62 counter computed `resolved` from
literal marker substrings, so a marker-only fixture with the S432 disagreement
present and no retained source body printed `met=true` (committed receipt
.ufo/waves/round-62/controls/counter-false-green-l1.txt). This counter binds
every `resolved` component to semantic evidence over committed bytes:

  quote_correction — the knowledge entry's [r63-correction] block quotes the
      S432 purpose span AND the round-63 class ledger records it; the ledger
      sha256s are re-derived from the retained blobs at the measured revision;
      the span's class is re-derived inline from those blobs (round-50
      semantics) and must equal the recorded `collapsed-only`. The lane tool
      scripts/quote_class.py re-derives the same class as C2 evidence; C1
      never gates on the tool, keeping the two claims separable.
  criterion — corpus/QUALITY.md carries the round-62 substantive-support
      criterion naming the located proposition (X-Content-Type-Options /
      Content-Type / destination).
  lesson_gate — corpus/lessons/round-63.md records the outside verdict (the
      round-61 non-author Disagree) and the resolution, and labels its own
      assessment author-side.
  source_row — corpus/SOURCES.md carries the S432 row.

A tree without the retained blobs, the ledger, or the correction therefore
cannot print `met=true`: the marker-only false-green is dead by construction.

Usage: c63_calibration.py --root . --revision <rev>
Exits: 0 met; 1 not met; 2 could-not-evaluate (git unreadable).
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import subprocess
import sys

BASE = "13d4519818db28cd0aa912e49020659140d7b9fa"  # round-62 tip
QUOTE_REL = ".ufo/waves/round-61/sources/S432.html"
TEXT_REL = ".ufo/waves/round-63/quote-class/S432.txt"
LEDGER_REL = ".ufo/waves/round-63/quote-class/quote-classes.json"
PATHS = {
    "spot": "corpus/lessons/round-61-verifier-spotcheck.md",
    "knowledge": "corpus/knowledge/response-header-expectations.md",
    "quality": "corpus/QUALITY.md",
    "lesson": "corpus/lessons/round-63.md",
    "sources": "corpus/SOURCES.md",
}
FROZEN_QUOTE = (
    "The `X-Content-Type-Options` response header can be used to require "
    "checking of a response\u2019s `Content-Type` header against the "
    "destination of a request."
)
PURPOSE_TERMS = ("X-Content-Type-Options", "Content-Type", "destination")


def classify(quote: str, raw: str, text: str) -> str:
    """Round-50 class semantics, inlined so C1 is verifiable without the
    scripts/quote_class.py tool (claim separability; the tool re-derives the
    same class as C2 evidence, never as a C1 gate)."""
    if quote in raw:
        return "raw-substring"
    if quote in text:
        return "collapsed-only"
    return "absent"


def git_show(root: str, revision: str, rel: str) -> bytes | None:
    proc = subprocess.run(
        ["git", "-C", root, "show", f"{revision}:{rel}"],
        stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=False)
    if proc.returncode:
        return None
    return proc.stdout


def main() -> int:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--root", default=".")
    ap.add_argument("--revision", default=BASE)
    args = ap.parse_args()

    root = args.root
    rev = args.revision
    probe = subprocess.run(["git", "-C", root, "rev-parse", "--verify", rev],
                           stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    if probe.returncode:
        print(f"could-not-evaluate: revision {rev} unreadable", file=sys.stderr)
        return 2

    blobs = {k: git_show(root, rev, p) for k, p in PATHS.items()}
    if blobs["spot"] is None:
        print("could-not-evaluate: verifier spot-check absent", file=sys.stderr)
        return 2
    spot = blobs["spot"].decode("utf-8", errors="replace")
    disagreements = sum("S432" in line and "Disagree" in line
                        for line in spot.splitlines())
    knowledge = (blobs["knowledge"] or b"").decode("utf-8", errors="replace")
    quality = (blobs["quality"] or b"").decode("utf-8", errors="replace")
    lesson = (blobs["lesson"] or b"").decode("utf-8", errors="replace")
    sources = (blobs["sources"] or b"").decode("utf-8", errors="replace")

    # --- semantic components -------------------------------------------------
    # 1. retained blobs + ledger, re-derived
    raw_blob = git_show(root, rev, QUOTE_REL)
    text_blob = git_show(root, rev, TEXT_REL)
    ledger_blob = git_show(root, rev, LEDGER_REL)
    ledger = {}
    ledger_err = None
    if ledger_blob is None:
        ledger_err = "ledger_absent"
    else:
        try:
            parsed = json.loads(ledger_blob.decode("utf-8"))
            ledger = {row["id"]: row for row in parsed.get("classes", [])}
        except Exception as exc:
            ledger_err = f"ledger_unreadable:{type(exc).__name__}"

    correction = int(
        "[r63-correction" in knowledge
        and FROZEN_QUOTE in knowledge
        and LEDGER_REL in knowledge
    )

    blobs_match = 0
    derived = "unevaluable"
    class_match = 0
    if raw_blob is not None and text_blob is not None and ledger_err is None:
        row = ledger.get("S432")
        if row:
            blobs_match = int(
                row.get("rawSha256") == hashlib.sha256(raw_blob).hexdigest()
                and row.get("textSha256") == hashlib.sha256(text_blob).hexdigest()
                and row.get("quote") == FROZEN_QUOTE
            )
            if blobs_match:
                derived = classify(FROZEN_QUOTE,
                                   raw_blob.decode("utf-8", errors="replace"),
                                   text_blob.decode("utf-8", errors="replace"))
                class_match = int(derived == "collapsed-only"
                                  == row.get("matchClass"))

    quote_correction = int(correction and blobs_match and class_match)

    # 2. criterion names the located proposition
    crit_block = "substantive" in quality and "round-61-verifier-spotcheck" in quality
    names_purpose = all(term in quality for term in PURPOSE_TERMS)
    criterion = int(crit_block and names_purpose)

    # 3. lesson gate records the outside verdict and the resolution
    lesson_gate = int(
        "## Gate" in lesson
        and "round-61-verifier-spotcheck" in lesson
        and "Disagree" in lesson
        and "collapsed-only" in lesson
        and ("author-side" in lesson or "self-assessment" in lesson)
    )

    # 4. registry row
    source_row = int(re.search(r"^\|\s*S432\s*\|", sources, re.M) is not None)

    resolved = (quote_correction and criterion and lesson_gate and source_row)
    unresolved = disagreements if not resolved else 0
    met = bool(resolved)
    print(f"revision={rev} disagreements={disagreements} "
          f"quote_correction={quote_correction} blobs_match={blobs_match} "
          f"derived={derived} class_match={class_match} "
          f"criterion={criterion} lesson_gate={lesson_gate} "
          f"source_row={source_row} unresolved={unresolved} "
          f"met={str(met).lower()}")
    return 0 if met else 1


if __name__ == "__main__":
    sys.exit(main())
