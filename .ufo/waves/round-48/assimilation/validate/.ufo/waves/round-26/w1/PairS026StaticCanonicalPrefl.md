# PairS026 × static-canonical-preflight — round-26 freshness recheck

Pair: `corpus/knowledge/static-canonical-preflight.md` × S026 (Python `html.parser` documentation).
Axes: freshness (primary). Operability: no tool gap; all checks ran on `sha256sum`, `zcat`, `python3` (read-only) and the read/grep tools.
Milestone: r26-recheck-build. Leaf member; no delegation; no builds, tests or linters run.

## Evidence basis

- Manifest row S026, index 1 (`fetched/manifest.json`): status 200, `finalUrl` equals `url`, `fetchedAt` 2026-10-21T15:10:49.267812+00:00, `last-modified` Wed, 21 Oct 2026 13:04:30 GMT, `etag` `"6ad8b85e-d7dc"`, `content-length` 55260 (= `bytes`).
- Digests: archive `fetched/S026-1.raw.gz` sha256 `0e1785c7…e9ab8`. The manifest and population `sha256` `d92217e0…faa3` is the digest of the decompressed body (`zcat | sha256sum`; 55260 bytes), not of the `.gz`. Text view `fetched/text/S026-1.txt` sha256 `11f57d68…2e3`, 11807 bytes, one line.
- Text completeness: every quote below is present verbatim in `S026-1.txt`, and the tag-stripped raw HTML contains the same sentences. The raw "tree" hits are a GitHub URL path (`/tree/3.15/`) and the "DOM" hits are a `DOMContentLoaded` script. The page never mentions HTML5 or tree construction.
- Current build: title "html.parser — Simple HTML and XHTML parser — Python 3.15.1 documentation"; footer "Last updated on Oct 21, 2026 (13:02 UTC)".
- Earlier readings, quoted from in-lane reports (historical, not re-read as sources): round-22 `.ufo/waves/round-22/w1/PythonParser.md` (accessed 2026-10-20; Python 3.15.0; footer "Oct 20, 2026 (20:57 UTC)"); round-23 `.ufo/waves/round-23/w1/ReopenPythonParser.md` (response 2026-10-21 06:59:02 GMT; Python 3.15.0; `last-modified` 06:45:59 GMT). Whole-page bytes of those builds are not retained, so a whole-page content diff is UNVERIFIABLE. Verdicts below are against the 2026-10-21 13:04 GMT build.

## Statement verdicts

Statements are the knowledge entry's lines attributed to S026: explicitly (citation or the `(S026)` marker), by adjacency to that marker, or by a section-level source list. Implicit rows say so.

| # | file:line | Statement (abridged) | S026 link | Verdict | Verbatim quote (S026-1.txt) | Anchor observed | Note |
|---|---|---|---|---|---|---|---|
| 1 | L1 | Source header: `S026 Python HTMLParser https://docs.python.org/3/library/html.parser.html` | explicit (citation) | HOLD | "html.parser — Simple HTML and XHTML parser — Python 3.15.1 documentation" | page title | URL equals manifest `finalUrl` (HTTP 200). Header has no version or date, so nothing in it is superseded. |
| 2 | L2 | `verified-at: 2026-10-20 (S020-S027)`: the S026 component | explicit (date/version pin) | STALE | "Last updated on Oct 21, 2026 (13:02 UTC)" | page footer | Pin is the 2026-10-20 reading (Python 3.15.0). Current bytes were retrieved 2026-10-21T15:10:49Z and carry 3.15.1. The round-23 reopen (2026-10-21, 3.15.0) is also unrecorded. Correction C1. |
| 3 | L67 | "lowercases tag/attribute names and decodes attribute entities" | S026-cited paragraph (L69) | HOLD | "The name will be translated to lower case, and quotes in the value have been removed, and character and entity references have been replaced" | HTMLParser Methods → `handle_starttag (tag, attrs)` | Tag-name clause also holds: "The tag argument is the name of the tag converted to lower case". |
| 4 | L67–68 | "it is not an HTML5 DOM/tree builder" | adjacent, unattributed | HOLD (inference) | "calls handler methods when start tags, end tags, text, comments, and other markup elements are encountered" | class description paragraph | S026 never says HTML5, DOM or tree construction (0 "HTML5" hits). The callback model supports "not a tree builder"; the HTML5 framing is the entry's own inference. |
| 5 | L68–69 | "Its docs explicitly say it does not check matching start/end tags" | explicit (S026) | HOLD | "This parser does not check that end tags match start tags" | class description paragraph | Exact. |
| 6 | L69 | "or report all implicit closures (S026)" | explicit (S026) | STALE | "call the end-tag handler for elements which are closed implicitly by closing an outer element" | class description paragraph | Overreach: S026 limits the implicit-closure point to elements closed by an outer element; "all implicit closures" is not S026's wording. The same sentence was quoted in round 23. That round's P3 (`round-23/w1/ReopenPythonParser.md#85B5`) flagged this and it was never applied. Correction C2. |
| 7 | L70–71 | "explicit-head supported subset and unsupported-shape rejection are therefore part of the interface" | derived from #5 ("therefore") | HOLD | "Create a parser instance able to parse invalid markup" | class description paragraph | The parser is built for invalid markup and does not validate end-tag matching, so no conformance claim follows. |
| 8 | L71–72 | "Comments, raw script text … cannot supply a document-head canonical" | implicit (callbacks) | HOLD (comment and raw-script clauses) | "This method is called when a comment is encountered"; "The content of elements like script and style is returned as is, without further parsing" | `handle_comment (data)`; Examples | Validator defines no `handle_comment` override; script/style data arrives via `handle_data` (`scripts/canonical_audit.py:350`). The template clause rests on S025 (r23-correction, L143–146) and is not judged here. |
| 9 | L98–101 | Round-23 source list citing "S026" | explicit (citation) | HOLD | "This parser does not check that end tags match start tags" | class description paragraph | Supports the section's end-tag-matching claims (#13). |
| 10 | L103 | "The tool is still not an HTML5 tree builder." | section-level (L98–101) | HOLD (inference) | "calls handler methods when start tags, end tags, text, comments, and other markup elements are encountered" | class description paragraph | Same basis as #4. The tool's own text repeats it (`scripts/canonical_audit.py:101–102`). |
| 11 | L106–109 | SVG/MathML `title`/`style`/`script` tokenized, not HTML raw text | section-level + implementation | HOLD | "The content of elements like script and style is returned as is, without further parsing" | Examples | S026 documents the default raw-text handling that the override departs from (`scripts/canonical_audit.py:160–161`, `199–204`). The SVG/MathML rule itself is not S026's. |
| 12 | L110–111 | Self-closed void elements evaluated; self-closed `<div/>` unsupported | section-level + implementation | HOLD | "called when the parser encounters an XHTML-style empty tag" | HTMLParser Methods → `handle_startendtag` | The validator overrides `handle_startendtag` (`scripts/canonical_audit.py:299–308`) and calls `handle_starttag` only. S026's default also calls `handle_endtag` ("the default implementation simply calls handle_starttag() and handle_endtag()"), which is correctly departed from for void elements. The 13-name list is S030's. |
| 13 | L107; L114–115 | "end tags match a modelled element stack exactly"; "mismatched or unclosed foreign end tags" → `html_unsupported` | section-level + implementation | HOLD | "This parser does not check that end tags match start tags" | class description paragraph | The validator must do its own end-tag matching because S026 says the parser does not. It fails closed on any mismatch (`scripts/canonical_audit.py:310–319`). |

Totals: 13 statements; 11 HOLD; 2 STALE.

## Pin and version flags

- L2 (#2): the S026 date/version pin is superseded (2026-10-20, Python 3.15.0). Correction C1.
- No statement's anchor is superseded. The URL, the page title, the HTMLParser class-description paragraph, and the `handle_starttag`, `handle_comment`, `handle_data`, `handle_startendtag` and Examples anchors all still exist in the 2026-10-21 bytes.
- The entry carries no other Python version string; a grep for `3.1x` finds only RFC section numbers.
- The entry has no [r20-correction] tail. Its only correction tags are [r23-correction] (L140–146), which name S021 and S025, not S026; the S025 part is covered by R4.
- Row-level (outside this file, for the S026 row seat; not edited here): `corpus/SOURCES.md:34` version cell "Python 3.15 documentation accessed 2026-10-20" and `population.json:581` anchor refer to the superseded 3.15.0-era reading. The row's recheck trigger is "on-release" (`population.json:585`). The 3.15.0→3.15.1 docs change is that kind of event [INFERENCE: the 3.15.1 release itself was not checked against Python release notes].

## Corrections (append-only; EOF blocks in the citing knowledge file)

Append after the final line of `corpus/knowledge/static-canonical-preflight.md`, separated by one blank line. Original lines are not rewritten.

C1 — for #2 (L2):

```
[r26-recheck S026 STALE] Line 2's S026 pin is superseded. S026 (Python html.parser docs) was re-fetched 2026-10-21T15:10:49Z: HTTP 200, footer "Last updated on Oct 21, 2026 (13:02 UTC)", title "html.parser — Simple HTML and XHTML parser — Python 3.15.1 documentation". The 2026-10-20 reading recorded Python 3.15.0 documentation; the round-23 reopen (response 2026-10-21 06:59:02 GMT) also recorded 3.15.0. The sentences this entry relies on still appear verbatim in the 2026-10-21 bytes (.ufo/waves/round-26/w1/PairS026StaticCanonicalPrefl.md).
```

C2 — for #6 (L69):

```
[r26-recheck S026 STALE] Line 69's "or report all implicit closures (S026)" overstates S026. The re-fetched page limits its implicit-closure sentence to elements "closed implicitly by closing an outer element" and does not say "all implicit closures" (.ufo/waves/round-26/w1/PairS026StaticCanonicalPrefl.md).
```

## Residual and routing (no verdict change)

- R1 (row seat): the S026 teaches (`SOURCES.md:34`; `population.json:582`) says "HTML5 tree construction … not validated". The re-fetched bytes contain no HTML5 or tree-construction wording. Verdicts #4 and #10 rest on the callback model, not that wording, and are marked HOLD (inference).
- R2 (routing): other S026 citers, not judged here: `corpus/README.md:129`; `corpus/lessons/round-22.md:49,55`; `corpus/lessons/round-22-verifier-spotcheck.md:141`; `corpus/SOURCES.md:51,73`. Round-23 P3 also names `SKILL.md:396`, which was not re-read here.
- R3 (omission; no stated claim, so no verdict): the entry never mentions `noscript`. The validator handles it (`scripts/canonical_audit.py:222–232`; test at `:836`), and S026 documents the default: "If scripting is false (the default), the content of the noscript element is parsed normally". Route to L1 only if a noscript statement is wanted.
- R4 (attribution precision, not STALE): #8's comment and raw-script clauses rest on S026 but are not attributed to it. The r23-correction names S025 only for the template clause. An optional attribution note would suffice.
- R5: round-23 P3 (`round-23/w1/ReopenPythonParser.md#85B5`) first identified #6. It had not been applied before this recheck.
- R6 (second-order, not judged): L62's "within its parser boundary" points to the boundary defined in the S026-cited section (L65–72); the exit-2 policy's S026 reliance is covered by #3–#13.
- R7 (not S026-attributed, not judged): L151's `href=/x/>` caveat is S030-attributed. S026 says only that unquoted attributes "also work" ("Parsing invalid HTML (e.g. unquoted attributes) also works"), which does not settle the slash rule.

## Tooling and verification

- Installs or updates performed: none. Tools used were already present (`sha256sum`, `zcat`, `python3` read-only, read/grep/glob). Nothing recorded for the tooling directive.
- Quotes: every quote used in the table and in C1/C2 is present verbatim in `S026-1.txt` and is 8–24 words.
- Not run: `measure.py`, builds, tests, linters (not assigned). No fleet, sibling, corpus or production file was written.

```json
{"pair":"S026xstatic-canonical-preflight","statements":13,"hold":11,"stale":2,"corrections":["[r26-recheck S026 STALE] Line 2's S026 pin is superseded. S026 (Python html.parser docs) was re-fetched 2026-10-21T15:10:49Z: HTTP 200, footer \"Last updated on Oct 21, 2026 (13:02 UTC)\", title \"html.parser — Simple HTML and XHTML parser — Python 3.15.1 documentation\". The 2026-10-20 reading recorded Python 3.15.0 documentation; the round-23 reopen (response 2026-10-21 06:59:02 GMT) also recorded 3.15.0. The sentences this entry relies on still appear verbatim in the 2026-10-21 bytes (.ufo/waves/round-26/w1/PairS026StaticCanonicalPrefl.md).","[r26-recheck S026 STALE] Line 69's \"or report all implicit closures (S026)\" overstates S026. The re-fetched page limits its implicit-closure sentence to elements \"closed implicitly by closing an outer element\" and does not say \"all implicit closures\" (.ufo/waves/round-26/w1/PairS026StaticCanonicalPrefl.md)."]}
```

Report: .ufo/waves/round-26/w1/PairS026StaticCanonicalPrefl.md
