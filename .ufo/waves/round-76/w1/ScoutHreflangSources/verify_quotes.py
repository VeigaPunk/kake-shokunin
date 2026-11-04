#!/usr/bin/env python3
"""Verify every C2 quote against the retained tag-stripped bodies.

Method: each retained body is flattened by collapsing every whitespace run to one
space, while keeping a character-offset -> line-number map. A quote is located by
literal substring search on the flattened text; the hit is then mapped back to the
exact line window it occupies. A quote passes when that derived window equals the
declared window (an exact anchor) and fails otherwise.

Exit 0 iff every quote is found at its declared window.
"""
import re
import sys
import pathlib

HERE = pathlib.Path(__file__).resolve().parent

QUOTES = [
    ("google-localized-versions.txt", 362, 364,
     "Each language version must list itself as well as all other language versions."),
    ("google-localized-versions.txt", 365, 365,
     "Alternate URLs must be fully-qualified, including the transport method (http/https), so:"),
    ("google-localized-versions.txt", 387, 387,
     "If two pages don't both point to each other, the tags will be ignored."),
    ("google-localized-versions.txt", 729, 732,
     "The reserved x-default value is used when no other language/region matches the "
     "user's browser setting."),
    ("google-localized-versions.txt", 344, 344,
     "There are three ways to indicate multiple language/locale versions of a page to Google:"),
    ("google-localized-versions.txt", 355, 360,
     "Google doesn't use hreflang or the HTML lang attribute to detect the language of a page"),
    ("google-localized-versions.txt", 680, 681,
     "Only language codes listed in ISO 639-1 and region codes listed in ISO 3166-1 Alpha 2 "
     "are supported; other codes that aren't listed in those standards, such as es-419, "
     "aren't supported."),
    ("google-localized-versions.txt", 682, 684,
     "The hreflang value is case-insensitive"),
    ("google-localized-versions.txt", 738, 740,
     "There's no need to specify a language code for the x-default value"),
    ("whatwg-links.txt", 1356, 1356,
     "The value must be a valid BCP 47 language tag."),
    ("whatwg-links.txt", 1355, 1356,
     "gives the language of the linked resource. It is purely advisory."),
    ("whatwg-links.txt", 4055, 4056,
     "it indicates that the referenced document is a translation."),
    ("whatwg-links.txt", 4396, 4400,
     "The canonical keyword indicates that URL given by the href attribute is the preferred "
     "URL for the current document."),
    ("rfc5646.txt", 1053, 1054,
     'A tag is considered "well-formed" if it conforms to the ABNF (Section 2.1).'),
    ("rfc5646.txt", 327, 328,
     "At all times, language tags and their subtags, including private use and extensions, "
     "are to be treated as case insensitive"),
    ("rfc5646.txt", 231, 236,
     'langtag       = language ["-" script] ["-" region] *("-" variant) '
     '*("-" extension) ["-" privateuse]'),
    ("rfc5646.txt", 238, 238,
     'language      = 2*3ALPHA            ; shortest ISO 639 code'),
]

cache = {}


def flatten(name):
    """Return (flat_text, char->line list, raw_text)."""
    if name in cache:
        return cache[name]
    # Split on LF only: grep -n / sed / wc -l count LF, and RFC 5646 carries form
    # feeds (^L) as page separators that str.splitlines() would also split on.
    text = (HERE / name).read_text(encoding="utf-8")
    raw = [ln.rstrip("\r") for ln in text.split("\n")]
    if raw and raw[-1] == "":
        raw.pop()
    flat_chars = []
    char_line = []
    for lineno, line in enumerate(raw, start=1):
        for ch in line:
            if ch.isspace():
                if flat_chars and flat_chars[-1] == " ":
                    continue
                flat_chars.append(" ")
            else:
                flat_chars.append(ch)
            char_line.append(lineno)
        if flat_chars and flat_chars[-1] != " ":
            flat_chars.append(" ")
            char_line.append(lineno)
    while flat_chars and flat_chars[-1] == " ":
        flat_chars.pop()
        char_line.pop()
    cache[name] = ("".join(flat_chars), char_line, "\n".join(raw))
    return cache[name]


def main():
    failures = 0
    print(f"quotes={len(QUOTES)}")
    for name, lo, hi, quote in QUOTES:
        flat, char_line, raw = flatten(name)
        needle = re.sub(r"\s+", " ", quote).strip()
        words = len(needle.split())
        pos = flat.find(needle)
        if pos < 0:
            print(f"FAIL {name}:{lo}-{hi} quote absent from body; words={words}")
            failures += 1
            continue
        got_lo = char_line[pos]
        got_hi = char_line[pos + len(needle) - 1]
        exact = (got_lo == lo and got_hi == hi)
        second = flat.find(needle, pos + 1)
        print(
            f"{'OK  ' if exact else 'FAIL'} {name}:{lo}-{hi} derived={got_lo}-{got_hi} "
            f"exact={str(exact).lower()} words={words} occurrences="
            f"{flat.count(needle)} raw_substring={str(needle in raw).lower()}"
        )
        if not exact:
            failures += 1
    print(f"failures={failures}")
    return 0 if failures == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
