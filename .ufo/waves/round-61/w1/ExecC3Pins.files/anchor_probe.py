#!/usr/bin/env python3
"""Anchor-material presence probe for the round-61 C3 due set (read-only).

Purpose: the C3 pin rule pins a row only when the fetch is HTTP 200 AND the row's anchor
material still occurs in the fresh body. The quote re-location seat (ExecC3Quote) owns the
authoritative verdict; this probe is the independent cross-check I report alongside my table
and the fallback basis when that verdict table is not yet written.

For each row it takes the components named in the row's `anchor` cell, collapses the fresh
body to text (scripts/style dropped, tags stripped, entities decoded, whitespace collapsed) and
reports whether each component still occurs. A component that belongs to a URL the round did
not fetch (S001's second URL, S002's second URL) is marked `unfetched-url`, never `absent`.

Output: anchor_probe.tsv  row_id <TAB> component <TAB> url_scope <TAB> present <TAB> note
Exit: 0 probe written, 2 body or registry unreadable.
"""
import argparse
import html
import os
import re
import sys

LANE = "/home/vgpnk/Projects/shokunin/kake-shokunin"
RECHECK = os.path.join(LANE, ".ufo", "waves", "round-61", "recheck")

# component, url_scope ('fetched' = row's first/primary URL, the one this round fetched;
# 'unfetched' = the row names a second URL that the round did not fetch)
COMPONENTS = {
    "S001": [
        ("include-hidden-files", "unfetched", "input added after v4.0.0; row's second URL (main) not fetched"),
        ("Archive artifact", "fetched", "composite step name present in the v4.0.0 action.yml"),
        ("--exclude=.git", "fetched", "invariant exclusion line"),
        ("--exclude=.github", "fetched", "invariant exclusion line"),
    ],
    "S002": [
        ("What's Changed", "fetched", "v4.0.0 release page section"),
        ("Changelog", "fetched", "release page section"),
        ("include-hidden-files", "unfetched", "v5.0.0 note lives on the second URL, not fetched"),
    ],
    "S003": [
        ("About publishing sources", "fetched", "section heading"),
        ("Creating a custom GitHub Actions workflow", "fetched", "note heading"),
    ],
    "S004": [
        ("upload-pages-artifact", "fetched", "action name"),
        ("10GB", "fetched", "artifact size limit"),
        ("symbolic or hard links", "fetched", "archive content rule"),
    ],
    "S005": [
        ("Configuring an apex domain", "fetched", "heading"),
        ("Configuring a subdomain", "fetched", "heading"),
        ("CNAME", "fetched", "domain configuration artifact"),
    ],
    "S006": [
        ("Configuring Jekyll", "fetched", "heading"),
        ("node_modules", "fetched", "default exclusion"),
        ("vendor", "fetched", "default exclusion"),
    ],
    "S007": [
        ("build_type", "fetched", "response schema field"),
        ("protected_domain_state", "fetched", "response schema field"),
        ("cname", "fetched", "response schema field"),
    ],
    "S008": [
        ("Controlling Pattern-Matching", "fetched", "manual node"),
        ("anchored patterns", "fetched", "manual wording"),
        ("wildcard", "fetched", "pattern matching scope"),
    ],
    "S009": [
        ("ngx_http_set_etag", "fetched", "function symbol"),
        ("sprintf", "fetched", "ETag formatting call"),
    ],
    "S010": [
        ("Weak versus Strong", "fetched", "section 8.8.1 heading"),
        ("ETag", "fetched", "section 8.8.3 subject"),
    ],
}


def body_text(path):
    raw = open(path, "rb").read().decode("utf-8", "replace")
    raw = re.sub(r"(?is)<(script|style)\b.*?</\1>", " ", raw)
    raw = re.sub(r"(?s)<[^>]+>", " ", raw)
    return re.sub(r"\s+", " ", html.unescape(raw))


def main(argv=None):
    ap = argparse.ArgumentParser()
    ap.add_argument("--recheck", default=RECHECK)
    ap.add_argument("--out", default=os.path.dirname(os.path.abspath(__file__)))
    args = ap.parse_args(argv)

    lines = ["row_id\tcomponent\turl_scope\tpresent\tnote"]
    summary = {}
    for rid in sorted(COMPONENTS):
        path = os.path.join(args.recheck, rid + ".html")
        if not os.path.exists(path):
            sys.stderr.write("body missing: %s\n" % path)
            return 2
        text = body_text(path)
        verdict = []
        for component, scope, note in COMPONENTS[rid]:
            found = component in text
            lines.append("\t".join([
                rid, component, scope,
                "yes" if found else ("no" if scope == "fetched" else "n/a"),
                note if scope == "fetched" else "not fetched this round: " + note,
            ]))
            if scope == "fetched":
                verdict.append(found)
        summary[rid] = "anchor_found" if all(verdict) else (
            "anchor_partial" if any(verdict) else "page_changed")

    lines.append("")
    lines.append("# per-row probe verdict (fetched-scope components only)")
    for rid in sorted(summary):
        lines.append("%s\t%s" % (rid, summary[rid]))

    out = os.path.join(args.out, "anchor_probe.tsv")
    with open(out, "w", encoding="utf-8") as fh:
        fh.write("\n".join(lines) + "\n")
    print("\n".join("%s %s" % (k, v) for k, v in sorted(summary.items())))
    return 0


if __name__ == "__main__":
    sys.exit(main())
