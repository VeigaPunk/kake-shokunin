#!/usr/bin/env python3
"""Round-54 C1 counter — S374 crawl-qualifier repair (calibration claim).

Frozen predicate (see .ufo/waves/round-54/contract.md):

    S374 qualifier: mismatches = rendered cells missing the crawl qualifier
    and not superseded by an r54 correction block; met when 0.

Reads committed bytes only (`git show <revision>:<path>`, no worktree reads,
no network). Uses the retained round-52 body as the source of truth for the
exact Japanese phrase.

Checks:
  C1.1  the retained body .ufo/waves/round-52/sources/S374.html at the
         revision contains the exact substring 「このリンク先のウェブページの巡回を推奨していない」
         (NFKC-stable; the raw body carries it verbatim) — without this, the
         claim is unevaluable because the quote itself is not pinned.
  C1.2  rendering cells = every `(rendered: …)` group in the entry. A cell
         is a suspect when it describes the phrase with endorsement/refusal
         vocabulary (recommend|vouch|endorse|refusal|refuse) and has no crawl
         vocabulary (crawl|巡回).
  C1.3  a correction block is an entry line starting with
         `[r54-correction 2026-10-25]`; it must contain the exact source quote
         and at least one crawl token.
  C1.4  mismatch = number of suspect cells that appear BEFORE any valid
         correction block in the file.

Predicate met iff mismatch == 0 and at least one valid correction block exists.

Exit: 0 met, 1 not met, 2 unevaluable, 64 usage.
"""
from __future__ import annotations

import argparse
import os
import re
import subprocess
import sys

PREDICATE = "S374 qualifier: mismatches = rendered cells missing the crawl qualifier and not superseded by an r54 correction block; met when 0"
ENTRY = "corpus/knowledge/yahoo-japan-rel-nofollow-semantics.md"
BODY = ".ufo/waves/round-52/sources/S374.html"
QUOTE = "このリンク先のウェブページの巡回を推奨していない"
CORRECTION_MARK = "[r54-correction 2026-10-25]"
SEMANTIC_RE = re.compile(r"recommend|vouch|endorse|refusal|refuse", re.I)
CRAWL_RE = re.compile(r"crawl|巡回", re.I)
NEGATIVE_CRAWL_RE = re.compile(r"\bnot\s+recommend(?:\s+the)?\s+(?:crawl|crawling)\b", re.I)
RENDER_RE = re.compile(r"\(rendered: ([^)]+)\)", re.S)


def git(root: str, *args: str) -> subprocess.CompletedProcess:
    env = {k: v for k, v in os.environ.items() if not k.startswith("GIT_")}
    return subprocess.run(["git", "-C", root, *args], capture_output=True, env=env)


def show(root: str, rev: str, path: str) -> bytes | None:
    p = git(root, "show", f"{rev}:{path}")
    return p.stdout if p.returncode == 0 else None

def qualifier_findings(entry: str) -> tuple[list[int], int]:
    """Return suspect-render offsets and the first source-bound correction."""
    suspects = [
        match.start()
        for match in RENDER_RE.finditer(entry)
        if SEMANTIC_RE.search(match.group(1)) and not CRAWL_RE.search(match.group(1))
    ]
    correction_at = -1
    for match in re.finditer(re.escape(CORRECTION_MARK), entry):
        window = entry[match.start():match.start() + 1200]
        if QUOTE in window and NEGATIVE_CRAWL_RE.search(window):
            correction_at = match.start()
            break
    return suspects, correction_at


def run_checks(root: str, rev: str) -> tuple[int, list[dict]]:
    results: list[dict] = []

    def add(check: str, ok: bool, notes: list[str], facts: dict | None = None) -> None:
        results.append({"check": check, "state": "pass" if ok else "fail",
                        "notes": notes, "facts": facts or {}})

    body_raw = show(root, rev, BODY)
    if body_raw is None:
        add("C1.1_body", False, [f"{BODY} missing at {rev}"])
        return 2, results
    body = body_raw.decode("utf-8", errors="replace")
    quote_ok = QUOTE in body
    add("C1.1_body", quote_ok,
        [] if quote_ok else [f"quote not an exact substring of {BODY}"],
        {"occurrences": body.count(QUOTE)})
    if not quote_ok:
        return 2, results

    entry_raw = show(root, rev, ENTRY)
    if entry_raw is None:
        add("C1.2_entry", False, [f"{ENTRY} missing at {rev}"])
        return 2, results
    entry = entry_raw.decode("utf-8", errors="replace")
    suspects, corr_at = qualifier_findings(entry)
    corr_ok = corr_at >= 0
    add("C1.2_cells", True, [], {"suspect_cells": len(suspects)})
    add("C1.3_correction", corr_ok,
        [] if corr_ok else ["no valid r54 correction block (exact quote + crawl token)"],
        {"block_offset": corr_at})

    mismatch = sum(1 for pos in suspects if corr_at == -1 or corr_at < pos)
    add("C1.4_mismatch", mismatch == 0, [] if mismatch == 0 else [f"mismatches={mismatch}"],
        {"mismatches": mismatch})

    met = quote_ok and corr_ok and mismatch == 0
    return (0 if met else 1), results


def selftest() -> int:
    """Inline fixtures for the same parser used by committed-byte checks."""
    base_entry = (
        "source: S374 — https://example.invalid/x — fetched 2026-10-25\n"
        "> \"このリンク先のウェブページの巡回を推奨していない\"\n"
        "(rendered: the site owner is taken to consider the link target's page one it\n"
        " does not recommend, or a link it cannot vouch for).\n"
    )
    corrected_entry = base_entry + (
        "\n## Round-54 correction (2026-10-25)\n"
        "[r54-correction 2026-10-25] 「このリンク先のウェブページの巡回を推奨していない」 means the site owner is taken to **not recommend the crawl** of the link target's page; the rendering above dropped the crawl qualifier.\n"
    )
    missing_quote = base_entry + (
        "\n## Round-54 correction (2026-10-25)\n"
        "[r54-correction 2026-10-25] crawl qualifier noted.\n"
    )
    missing_crawl = base_entry + (
        "\n## Round-54 correction (2026-10-25)\n"
        "[r54-correction 2026-10-25] このリンク先のウェブページの巡回を推奨していない  means not recommended.\n"
    )
    wrong_polarity = base_entry + (
        "\n## Round-54 correction (2026-10-25)\n"
        "[r54-correction 2026-10-25] 「このリンク先のウェブページの巡回を推奨していない」 says the owner recommends crawling the link target.\n"
    )
    correction_before = (
        "## Round-54 correction (2026-10-25)\n"
        "[r54-correction 2026-10-25] 「このリンク先のウェブページの巡回を推奨していない」 means the site owner is taken to **not recommend the crawl** of the link target's page.\n"
    ) + base_entry

    class Fix:
        def __init__(self, entry: str, body: str | None = None) -> None:
            self.entry = entry
            self.body = body if body is not None else QUOTE

        def read(self, path: str) -> bytes | None:
            if path == ENTRY:
                return self.entry.encode("utf-8")
            if path == BODY:
                return self.body.encode("utf-8")
            return None

    body_quote = QUOTE
    body_plain = "no such phrase here"

    cases = [
        ("base_unrepaired", Fix(base_entry), 1, "met=False"),
        ("corrected", Fix(corrected_entry), 0, "met=True"),
        ("correction_missing_quote", Fix(missing_quote), 1, "met=False"),
        ("correction_missing_crawl", Fix(missing_crawl), 1, "met=False"),
        ("body_missing_quote", Fix(base_entry, body_plain), 2, "unevaluable"),
        ("correction_wrong_polarity", Fix(wrong_polarity), 1, "met=False"),
        ("correction_before_render", Fix(correction_before), 1, "met=False"),
    ]
    failed = 0
    for name, fix, want_code, want_label in cases:
        code, results = run_checks_fix(fix)
        label = "met=True" if code == 0 else ("met=False" if code == 1 else "unevaluable")
        ok = code == want_code and label == want_label
        print(f"  {'ok ' if ok else 'FAIL'} {name}: exit {code} ({label}) expected {want_code} ({want_label})")
        if not ok:
            failed += 1
    # a junk no-op that always prints met=True must be distinguishable: trust
    # the exit codes above, not stdout.
    return 0 if failed == 0 else 1


def run_checks_fix(fix) -> tuple[int, list[dict]]:
    """Same logic as run_checks but against an in-memory reader."""
    body = fix.read(BODY)
    if body is None:
        return 2, []
    body_t = body.decode("utf-8", errors="replace")
    if QUOTE not in body_t:
        return 2, []
    entry_t = fix.read(ENTRY).decode("utf-8", errors="replace")
    suspects, corr_at = qualifier_findings(entry_t)
    mismatch = sum(1 for pos in suspects if corr_at == -1 or corr_at < pos)
    return (0 if corr_at >= 0 and mismatch == 0 else 1), []


def main() -> int:
    parser = argparse.ArgumentParser(description="Round-54 S374 calibration counter")
    parser.add_argument("--root", default=".", help="lane root (git -C)")
    parser.add_argument("--revision", default=None, help="committed revision")
    parser.add_argument("--selftest", action="store_true")
    parser.add_argument("--predicate", action="store_true", help="print the frozen predicate")
    args = parser.parse_args()
    if args.selftest:
        return selftest()
    if args.predicate:
        print(PREDICATE)
        return 0
    if not args.revision:
        parser.error("--revision is required")
    code, results = run_checks(args.root, args.revision)
    for r in results:
        state = "PASS" if r["state"] == "pass" else "FAIL"
        print(f"  {state} {r['check']}: {r['notes']} {r['facts']}")
    print(PREDICATE)
    met = code == 0
    print(f"mismatches={results[-1]['facts'].get('mismatches') if results else '?'} met={'True' if met else 'False'}")
    print(f"EXIT={code}")
    return code


if __name__ == "__main__":
    sys.exit(main())
