#!/usr/bin/env python3
"""Verify every quote planned for corpus/knowledge/x-robots-tag-header.md and the
S452 SOURCES row against the retained bytes.

Rule checked (QUALITY r55/r56): a quote is a raw substring of retained visible
text after whitespace collapse, 1..25 whitespace units, located inside the named
line range, and the row's Gate quote occurs exactly once in its own page.
Exit 0 all pass, 1 any failure.
"""
import json
import re
import sys

ROOT = "/home/vgpnk/Projects/shokunin/kake-shokunin"
S452 = f"{ROOT}/.ufo/waves/round-79/sources/S452-mdn-x-robots-tag.txt"
S449 = f"{ROOT}/.ufo/waves/round-79/w1/ScoutSources/google-robots-meta.txt"

QUOTES = [
    # (label, file, first_line, last_line, quote, gate)
    ("definition", S452, 136, 136,
     "The X-Robots-Tag response header defines how crawlers should index URLs.", False),
    ("de-facto", S452, 137, 137,
     "While not part of any specification, it is a de-facto standard method for communicating with search bots, web crawlers, and similar user agents.", False),
    ("non-html-role", S452, 140, 140,
     "Specifying indexing rules in an HTTP header is useful for non-HTML documents like images, PDFs, or other media.", False),
    ("bot-scope", S452, 156, 156,
     "An optional <bot-name>: specifies the user agent that the subsequent rules should apply to", True),
    ("multi-field", S452, 235, 235,
     "The following response has two X-Robots-Tag headers, each with an indexing rule specified", False),
    ("single-field-same", S452, 247, 247,
     "In the response below, the same indexing rules are defined, but in a single header.", False),
    ("rule-behind-agent", S452, 248, 248,
     "Each indexing rule applies to the user agent specified behind it", False),
    ("sum-negative", S452, 252, 252,
     "For situations where multiple crawlers are specified along with different rules, the search engine will use the sum of the negative rules.", False),
    ("googlebot-composition", S452, 256, 256,
     "The page containing these headers will be interpreted as having a noindex, nofollow rule when crawled by googlebot", False),
    ("conflict-fragment", S452, 219, 219,
     "the more restrictive rule applies.", False),
    ("conflict-example", S452, 220, 220,
     "For example, if a page has both max-snippet:50 and nosnippet rules, the nosnippet rule will apply.", False),
    ("mutually-exclusive", S452, 222, 222,
     "Some values are mutually exclusive", False),
    ("mutually-exclusive-pair", S452, 222, 222,
     "such as index and noindex", False),
    ("undefined-behaviour", S452, 223, 223,
     "In these cases, the crawler's behavior is undefined and may vary.", False),
    ("all-default", S452, 164, 164,
     "This rule is the default value and has no effect if explicitly listed.", False),
    ("none-expansion", S452, 172, 172,
     "Equivalent to noindex, nofollow", False),
    ("noindex", S452, 166, 166,
     "Do not show this page, media, or resource in search results.", False),
    ("nofollow", S452, 169, 169,
     "Do not follow the links on this page.", False),
    ("nosnippet", S452, 174, 174,
     "Do not show a text snippet or video preview in the search results for this page.", False),
    ("noimageindex", S452, 207, 207,
     "Do not index images on this page.", False),
    ("notranslate", S452, 204, 204,
     "Don't offer translation of this page in search results.", False),
    ("indexifembedded-effect", S452, 180, 180,
     "indexifembedded only has an effect if it's accompanied by noindex", False),
    ("max-snippet-invalid", S452, 183, 183,
     "Ignored if no valid <number> is specified.", False),
    ("max-image-preview-values", S452, 187, 187,
     "specify a max-image-preview value of standard or none", False),
    ("max-image-preview-large", S452, 193, 193,
     "A larger image preview, up to the width of the viewport, may be shown.", False),
    ("max-video-zero", S452, 200, 200,
     "At most, a static image may be used, in accordance to the max-image-preview setting.", False),
    ("max-video-unlimited", S452, 202, 202,
     "No video length limit.", False),
    ("date-families", S452, 212, 212,
     "A date must be specified in a format such as RFC 822", False),
    ("date-invalid", S452, 211, 211,
     "Ignored if no valid <date/time> is specified.", False),
    ("crawl-rate", S452, 215, 215,
     "Crawlers are expected to considerably decrease the crawl rate of the URL after the specified date and time.", False),
    ("cooperative-only", S452, 142, 142,
     "Only cooperative robots follow these rules", False),
    ("must-fetch", S452, 142, 142,
     "a crawler first needs to access the resource to read headers and meta elements", False),
    ("robots-blocked", S452, 221, 221,
     "Indexing rules won't be discovered or applied if paths are blocked from being crawled by a robots.txt file.", False),
    ("revisit", S452, 227, 227,
     "a robot must first revisit the page to detect the X-Robots-Tag rule.", False),
    ("no-specification", S452, 258, 258,
     "Not part of any current specification.", False),
    ("agent-optional", S452, 241, 241,
     "It's possible to specify which user agent the rules should apply to.", False),
    # S449 cross-checks
    ("s449-global-unprefixed", S449, 1012, 1012,
     "Rules specified without a user agent are valid for all crawlers.", False),
    ("s449-case-insensitive", S449, 1012, 1013,
     "The HTTP header, the user agent name, and the specified values are not case sensitive.", False),
    ("s449-conflict", S449, 1015, 1016,
     "In the case of conflicting robots rules, the more restrictive rule applies.", False),
    ("s449-multi-field", S449, 987, 988,
     "Multiple X-Robots-Tag headers can be combined within the HTTP response, or you can specify a comma-separated list of rules.", False),
    ("s449-prefix-before", S449, 1000, 1001,
     "The X-Robots-Tag may optionally specify a user agent before the rules.", False),
    ("s449-same-vocabulary", S449, 977, 978,
     "Any rule that can be used in a robots meta tag can also be specified as an X-Robots-Tag.", False),
    ("s449-historical", S449, 1217, 1217,
     "The following rules aren't used by Google Search and are ignored.", False),
    ("s449-noarchive", S449, 1225, 1225,
     "The noarchive rule is no longer used by Google Search", False),
    ("s449-date-families", S449, 1201, 1204,
     "must be specified in a widely adopted format including, but not limited to RFC 822, RFC 850, and ISO 8601", False),
    ("s449-pst-example", S449, 997, 997,
     "X-Robots-Tag: unavailable_after: 25 Jun 2010 15:00:00 PST", False),
    ("s449-sum-negative", S449, 1258, 1259,
     "the search engine will use the sum of the negative rules.", False),
]


def collapse(s: str) -> str:
    return re.sub(r"\s+", " ", s).strip()


def main() -> int:
    files = {p: open(p, encoding="utf-8", errors="replace").read().split("\n")
             for p in {q[1] for q in QUOTES}}
    collapsed_all = {p: collapse("\n".join(lines)) for p, lines in files.items()}
    rows, failures = [], 0
    for label, path, lo, hi, quote, gate in QUOTES:
        lines = files[path]
        window = collapse("\n".join(lines[lo - 1:hi]))
        units = len(collapse(quote).split())
        located = collapse(quote) in window
        occurrences = collapsed_all[path].count(collapse(quote))
        ok = located and 1 <= units <= 25 and occurrences >= 1 and (not gate or occurrences == 1)
        if not ok:
            failures += 1
        rows.append({
            "label": label,
            "file": path.replace(ROOT + "/", ""),
            "lines": f"{lo}-{hi}",
            "units": units,
            "located_in_range": located,
            "occurrences_in_page": occurrences,
            "gate": gate,
            "ok": ok,
            "quote": collapse(quote),
        })
    out = {"schema": "scribe-quote-receipts/v1", "checked": len(rows),
           "failures": failures, "max_units": max(r["units"] for r in rows), "quotes": rows}
    with open(f"{ROOT}/.ufo/waves/round-79/w1/ScribeKnowledge/quote-receipts.json", "w") as fh:
        json.dump(out, fh, indent=1)
        fh.write("\n")
    for r in rows:
        status = "ok" if r["ok"] else "FAIL"
        print(f"{status}\t{r['label']}\t{r['file']}:{r['lines']}\tunits={r['units']}\tocc={r['occurrences_in_page']}")
    print(f"checked={len(rows)} failures={failures} max_units={out['max_units']}")
    return 0 if failures == 0 else 1


if __name__ == "__main__":
    sys.exit(main())
