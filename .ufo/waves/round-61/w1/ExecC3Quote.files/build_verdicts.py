#!/usr/bin/env python3
"""C3 quote re-location verdict table (seat ExecC3Quote, round 61).

For each due row S001-S010 this reads the retained fresh body under
.ufo/waves/round-61/recheck/, measures the located anchor material, validates the
reported span against the lane quote rule (6..25 whitespace units, <=160 chars,
printable ASCII, no embedded ASCII double quote, page-unique, inside one
whitespace-collapsed text node for HTML bodies / one raw line for plain-text
bodies) and writes the verdict table. Read-only over the lane.
"""
from __future__ import annotations

import importlib.util
import json
import os
import sys

HERE = os.path.dirname(os.path.abspath(__file__))


def load(name, path):
    spec = importlib.util.spec_from_file_location(name, os.path.join(HERE, path))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)
    return mod


r = load("rel", "relocate.py")
v = load("val", "validate.py")

RECHECK = "/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-61/recheck"
OUT = "/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-61/w1/ExecC3Quote.files/verdicts.tsv"

ROWS = [
    dict(id="S001", body="S001.html", kind="text", verdict="anchor_moved",
         span="# Switch to gtar (GNU tar instead of bsdtar which is the default in the MacOS runners so we can use --hard-dereference)",
         location="action.yml v4.0.0: Archive artifact steps lines 24-39 (Linux), 42-57 (macOS), 60-76 (Windows); --exclude=.git lines 33/51/69, --exclude=.github lines 34/52/70, --exclude=\".[^/]*\" lines 35/53/71",
         clause="partial: the 'Archive artifact steps' material is present; the anchor's line refs (inputs.include-hidden-files 17-20, Archive artifact steps 37-39) address neither this file's inputs block nor its steps",
         note="NOT page_changed: the invariant-exclusion material is on the page. The include-hidden-files half lives only in the row's second URL (main 5f3270), not fetched this round (one GET per row). Pin decision must not restate lines 17-20/37-39 as verified for this body; either re-reference lines 24-38 or wait for a main-body fetch. No 6..25-unit span of the exclusion block itself can be quoted: its literals sit inside ASCII double quotes.",
         scope="primary-url-only"),
    dict(id="S002", body="S002.html", kind="html", verdict="anchor_found",
         span="Potentially breaking change: hidden files (specifically dotfiles) will not be included in the artifact",
         location="release page v4.0.0, under the heading \"What's Changed\" (page-unique in the release body)",
         clause="clause 1 of 2: 'v4.0.0 What's Changed' located; its text states the dotfile exclusion the teaches cell claims",
         note="clause 2 ('v5.0.0 Changelog') is unverified this round: v5.0.0 is the row's second URL and was not fetched. 'Changelog' occurs only in 'Full Changelog : v3.0.1...v4.0.0'. Not page_changed.",
         scope="primary-url-only"),
    dict(id="S003", body="S003.html", kind="html", verdict="anchor_found",
         span="file in your repository file does not automatically add or remove a custom domain. Instead, you must configure the custom domain",
         location="section 'About publishing sources' present; the Note under 'Creating a custom GitHub Actions workflow to publish your site' carries the quoted sentence",
         clause="both clauses: 'About publishing sources' and the note under the custom-workflow section",
         note="teaches supported in-page (publish from a branch or from a GitHub Actions workflow). The current heading reads 'Creating a custom GitHub Actions workflow to publish your site' - the anchor's shorter name still resolves to it. The sentence is split by <code>CNAME</code>, so the quote must start after that node.",
         scope="full"),
    dict(id="S004", body="S004.html", kind="html", verdict="anchor_found",
         span="file must be under 10GB in size and should not contain any symbolic or hard links. For more information, see the",
         location="under heading 'Configuring the upload-pages-artifact action'; the artifact-shape sentence follows '.tar.gz gzip archive containing a single tar file'",
         clause="the anchor's single clause: 'Configuring the upload-pages-artifact action'",
         note="teaches supported: 10GB ceiling and the no-symbolic-or-hard-links rule are in one text node; the sentence is split by <code>gzip</code>/<code>tar</code> before it, so the quote starts after 'file.'",
         scope="full"),
    dict(id="S005", body="S005.html", kind="html", verdict="anchor_found",
         span=", you must configure a custom domain in your repository settings and at least one",
         location="step 4 of both sections is the 4th <li>: 'Under \"Custom domain\", type your custom domain, then click Save' (ordinal counted in each section's <ol>); quoted span is in the 'Configuring an apex domain' opening sentence",
         clause="both clauses: 'Configuring an apex domain step 4' and 'Configuring a subdomain step 4', ordinal verified from list markup",
         note="teaches supported ('any existing CNAME file is ignored and is not required'). Quote constraint found: the step-4 sentence and the CNAME-ignored sentence each occur twice (apex and subdomain sections) so neither is page-unique; a page-unique quote has to come from section-specific text. The sentences are fragmented by <code> spans, so only short node-local spans qualify.",
         scope="full"),
    dict(id="S006", body="S006.html", kind="html", verdict="anchor_found",
         span="By default, Jekyll doesn&#x27;t build files or folders that:",
         location="under heading 'Configuring Jekyll in your GitHub Pages site'",
         clause="the anchor's single clause: 'Configuring Jekyll in your GitHub Pages site'",
         note="teaches supported verbatim by the following list (Are located in a folder called /node_modules or /vendor; Start with _ , . , or #; End with ~). The apostrophe is served as the entity &#x27; and the list items are separate nodes.",
         scope="full"),
    dict(id="S007", body="S007.html", kind="html", verdict="anchor_found",
         span="The process by which the GitHub Pages site will be built.",
         location="heading 'Update information about a GitHub Pages site' -> Parameters body parameters (build_type); heading 'Get a GitHub Pages site' -> Response schema (cname, protected_domain_state)",
         clause="both clauses: 'Get a GitHub Pages site response schema' and 'Update information about a GitHub Pages site body parameters'",
         note="teaches supported: build_type, cname and protected_domain_state are distinct fields in the schema and the body-parameter table.",
         scope="full"),
    dict(id="S008", body="S008.html", kind="text", verdict="anchor_found",
         span="For the purposes of this section, we call @dfn{exclusion members} all",
         location="tar.texi: '@node controlling pattern-matching' line 8480, '@unnumberedsubsec Controlling Pattern-Matching' line 8481, section ends line 8620 (next @node at 8621)",
         clause="the anchor's clause 'Controlling Pattern-Matching, anchored patterns and wildcard matching, lines 8478-8617'",
         note="range drift +2/+3: line 8478 is now the '@end menu' line and the section occupies 8480-8620. Same material in the same place; only the anchor's line numbers are stale. teaches supported in-section (anchored/wildcard paragraphs).",
         scope="full"),
    dict(id="S009", body="S009.html", kind="text", verdict="anchor_found",
         span="etag->value.data = ngx_pnalloc(r->pool, NGX_OFF_T_LEN + NGX_TIME_T_LEN + 3);",
         location="line 1682 'ngx_http_set_etag(ngx_http_request_t *r);' and the ETag ngx_sprintf at lines 1708-1710 (format literal on 1708, last_modified_time 1709, content_length_n 1710)",
         clause="both clauses: 'ngx_http_set_etag at line 1682' and 'ETag sprintf lines 1708-1710'",
         note="exact line match, no drift. The format literal is written as \"\\\"%xT-%xO\\\"\" in C source, so the teaches' hex-time/hex-length format cannot itself be a Gate quote without embedding ASCII double quotes; the quoted span is the adjacent allocation line that sizes the value buffer.",
         scope="full"),
    dict(id="S010", body="S010.html", kind="html", verdict="anchor_found",
         span="An entity tag consists of an opaque quoted string, possibly prefixed by a weakness indicator.",
         location="section '8.8.1. Weak versus Strong' and section '8.8.3. ETag' of RFC 9110",
         clause="both clauses: 'Section 8.8.1 Weak versus Strong' and '8.8.3 ETag'",
         note="teaches supported: strong/weak validator definitions in 8.8.1 and the opaque entity-tag grammar in 8.8.3. The #section-8.8 fragment is not sent on the wire (effectiveUrl is fragmentless); the document itself is the fetched body.",
         scope="full"),
]


def main() -> int:
    rows, failures = [], []
    for row in ROWS:
        body = os.path.join(RECHECK, row["body"])
        m = v.check(body, row["kind"], row["span"])
        if not m["ok"]:
            failures.append({"id": row["id"], **{k: m[k] for k in ("units", "chars", "page_count",
                                                                  "node_bounded", "node_hits")}})
        rows.append(dict(row, located_span=row["span"], anchor_clause=row["clause"],
                         units=m["units"], chars=m["chars"],
                         occurrences=m["page_count"],
                         node_index=m["node_hits"][0] if m["node_hits"] else "",
                         node_bounded=m["node_bounded"]))
    os.makedirs(os.path.dirname(OUT), exist_ok=True)
    header = ["id", "verdict", "located_span", "units", "chars", "occurrences", "node_index",
              "node_bounded", "location", "anchor_clause", "scope", "note"]
    with open(OUT, "w", encoding="utf-8", newline="") as fh:
        fh.write("\t".join(header) + "\n")
        for row in rows:
            fh.write("\t".join(str(row[h]).replace("\t", " ").replace("\n", " ") for h in header) + "\n")
    print(json.dumps({"out": OUT, "rows": len(rows),
                      "verdicts": {x["id"]: x["verdict"] for x in rows},
                      "failures": failures}, ensure_ascii=False, indent=1))
    return 0 if not failures else 1


if __name__ == "__main__":
    sys.exit(main())
