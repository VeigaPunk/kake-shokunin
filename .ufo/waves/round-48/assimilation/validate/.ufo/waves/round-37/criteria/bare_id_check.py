#!/usr/bin/env python3
"""Round-37 criterion (a): a bare source-id line is not a citation.

A knowledge entry cites a source row (S001-S999) with claim text: what that row says, where,
and why the entry's claim rests on it.  A block that carries an S-id and nothing else --
`- S011` or `source: S011, S012` -- records no claim, so it must not satisfy a `cites`
condition.  This check reads one or more markdown entries and fails when some cited S-id
appears only in blocks with no claim text.

A block is a paragraph, a single list item, or a heading: consecutive non-blank lines, split at
blank lines, list item starts and headings.  Claim text is counted over the whole block so a
citation inside a wrapped paragraph is not mistaken for a bare id.  A block has claim text
when, after removing its S-ids, URLs, `§` section references, inline code, path-like tokens and
markdown punctuation, at least three tokens of two or more letters remain.  Front-matter keys
(`source:`, `cites:`, `used-by:`, `recheck:`, `verified-at:`) are labels, not claim text.
Fenced code blocks are skipped: machine output is not prose.

Usage:
  bare_id_check.py ENTRY [ENTRY ...]

Exit 0: every S-id each entry cites carries claim text at least once.  Exit 1: at least one
S-id is cited only in blocks with no claim text.  Exit 2: an entry could not be read.
"""

from __future__ import annotations

import re
import sys
from pathlib import Path

SID_RE = re.compile(r"(?<![\w.-])S(\d{3})(?!\d)")
URL_RE = re.compile(r"<?\bhttps?://[^\s)>\]]+>?")
SECTION_RE = re.compile(r"§+\s*[\w.\-]+")
CODE_RE = re.compile(r"`[^`]*`")
WORD_RE = re.compile(r"[^\W\d_]{2,}", re.UNICODE)
LIST_START_RE = re.compile(r"^\s*(?:#{1,6}\s|[-*+]\s|\d+[.)]\s|---+\s*$)")
LABELS = {
    "source", "sources", "cites", "cite", "cited", "used-by", "used", "by", "recheck",
    "verified-at", "verified", "at", "corpus", "sources.md", "see", "ref", "row", "rows",
}
MIN_CLAIM_WORDS = 3


class InputError(Exception):
    """An entry could not be read."""


def _claim_words(text: str) -> list[str]:
    """Tokens that are claim text, not ids, pointers or labels."""
    text = SID_RE.sub(" ", text)
    text = URL_RE.sub(" ", text)
    text = CODE_RE.sub(" ", text)
    text = SECTION_RE.sub(" ", text)
    text = re.sub(r"[\w./-]*/[\w./-]+", " ", text)  # path-like tokens
    words = []
    for word in WORD_RE.findall(text):
        if word.lower() in LABELS:
            continue
        words.append(word)
    return words


def _blocks(document: str) -> list[tuple[int, str]]:
    """(first line number, text) for each prose block, skipping fenced code."""
    blocks: list[tuple[int, str]] = []
    fenced = False
    start: int | None = None
    lines: list[str] = []

    def flush() -> None:
        nonlocal start, lines
        if lines and any(line.strip() for line in lines):
            blocks.append((start or 1, "\n".join(lines)))
        start, lines = None, []

    for number, line in enumerate(document.splitlines(), 1):
        if line.lstrip().startswith("```"):
            flush()
            fenced = not fenced
            continue
        if fenced:
            continue
        if not line.strip() or LIST_START_RE.match(line):
            flush()
            if LIST_START_RE.match(line):
                start, lines = number, [line]
            continue
        if start is None:
            start = number
        lines.append(line)
    flush()
    return blocks


def check_entry(entry: Path) -> bool:
    try:
        document = entry.read_text(encoding="utf-8")
    except (OSError, UnicodeDecodeError) as exc:
        raise InputError(f"cannot read entry {entry}: {exc}") from exc

    occurrences: dict[str, list[tuple[int, bool]]] = {}
    for start, text in _blocks(document):
        ids = SID_RE.findall(text)
        if not ids:
            continue
        claimed = len(_claim_words(text)) >= MIN_CLAIM_WORDS
        for number_id in ids:
            occurrences.setdefault(f"S{number_id}", []).append((start, claimed))

    if not occurrences:
        print(f"PASS: {entry} cites no S-id, so no bare-id citation exists.")
        return True

    bare: list[tuple[str, list[int]]] = []
    for sid, rows in sorted(occurrences.items()):
        if not any(claimed for _start, claimed in rows):
            bare.append((sid, sorted({start for start, _claimed in rows})))
    if bare:
        for sid, numbers in bare:
            print(
                f"FAIL: {entry} cites {sid} only as a bare id "
                f"(block{'s' if len(numbers) > 1 else ''} at line "
                f"{', '.join(map(str, numbers))}); no block carries claim text for it."
            )
        return False

    print(
        f"PASS: {entry} cites {len(occurrences)} S-id(s), each with claim text at least once."
    )
    return True


def check(args: list[str]) -> int:
    if not args:
        raise InputError("no entry named")
    entries: list[Path] = []
    for value in args:
        path = Path(value)
        if not path.is_file():
            raise InputError(f"entry is not a regular file: {value}")
        entries.append(path)
    results = [check_entry(entry) for entry in entries]
    return 0 if all(results) else 1


def main(argv: list[str] | None = None) -> int:
    argv = sys.argv[1:] if argv is None else argv
    try:
        return check(argv)
    except (InputError, OSError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2


if __name__ == "__main__":
    raise SystemExit(main())
