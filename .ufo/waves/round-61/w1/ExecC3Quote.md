# ExecC3Quote

Claim C3 quote re-location (round 61, w1). For each due row S001-S010 I took the
anchor and teaches wording from `corpus/SOURCES.md` and re-located that material in the
retained fresh body `.ufo/waves/round-61/recheck/Sxxx.html` (fetched 2026-10-27
09:15:41-09:15:56 UTC by ExecC3Fetch; receipts.json: status 200 on all ten, sha256 and
bytes recorded, userAgent `round61`). Bodies were read only; nothing in the lane was
written except this report and `ExecC3Quote.files/`.

Method (scripts in `ExecC3Quote.files/`, stdlib Python, run with `-B`):
`relocate.py` builds a whitespace-collapsed text stream (HTML: tags and script/style
removed, heading text kept under markers so probe and heading offsets share one
coordinate space; plain-text bodies: file text collapsed) and reports per-probe hits,
nearest-hit similarity and enclosing heading. `analyze.py` dumps every occurrence with
context. `validate.py` enforces the lane quote rule on a candidate span (6..25 whitespace
units, <=160 chars, printable ASCII, no embedded ASCII double quote, page-unique, and
inside ONE whitespace-collapsed text node for HTML bodies / one raw line for the
plain-text YAML, texinfo and C bodies). `build_verdicts.py` regenerates the table.
I also counted `<li>` ordinals inside each S005 section to check the "step 4" clauses.

Verdict rule used (stated so the tokens are auditable):
- `anchor_found` - the material the anchor names is on the retained page and the
  location it names still reflects it (section heading present; for line-addressed
  anchors the section occupies the named lines within +/-5).
- `anchor_moved` - material present, but at a location materially different from the one
  the anchor names.
- `page_changed` - taught material absent from a page that should carry it.
- `fetch_failed` - no readable 200 body (none occurred).

## VERDICTS:

| id | verdict | located span (page-unique Gate-quote candidate) | units | located at |
|---|---|---|---|---|
| S001 | anchor_moved | `# Switch to gtar (GNU tar instead of bsdtar which is the default in the MacOS runners so we can use --hard-dereference)` | 22 | action.yml v4.0.0: Archive artifact steps at lines 24-39 / 42-57 / 60-76; --exclude=.git 33/51/69, --exclude=.github 34/52/70 |
| S002 | anchor_found | `Potentially breaking change: hidden files (specifically dotfiles) will not be included in the artifact` | 14 | release page v4.0.0 under the heading "What's Changed" |
| S003 | anchor_found | `file in your repository file does not automatically add or remove a custom domain. Instead, you must configure the custom domain` | 21 | section "About publishing sources"; the Note under "Creating a custom GitHub Actions workflow to publish your site" |
| S004 | anchor_found | `file must be under 10GB in size and should not contain any symbolic or hard links. For more information, see the` | 21 | heading "Configuring the upload-pages-artifact action" |
| S005 | anchor_found | `, you must configure a custom domain in your repository settings and at least one` | 15 | step 4 of both sections (4th `<li>`: "Under \"Custom domain\", type your custom domain, then click Save"); span sits in the "Configuring an apex domain" opening sentence |
| S006 | anchor_found | `By default, Jekyll doesn&#x27;t build files or folders that:` | 9 | heading "Configuring Jekyll in your GitHub Pages site" |
| S007 | anchor_found | `The process by which the GitHub Pages site will be built.` | 11 | "Get a GitHub Pages site" Response schema; "Update information about a GitHub Pages site" body parameters |
| S008 | anchor_found | `For the purposes of this section, we call @dfn{exclusion members} all` | 11 | tar.texi @node controlling pattern-matching line 8480, @unnumberedsubsec line 8481, section ends 8620 |
| S009 | anchor_found | `etag->value.data = ngx_pnalloc(r->pool, NGX_OFF_T_LEN + NGX_TIME_T_LEN + 3);` | 8 | ngx_http_set_etag at line 1682; ETag ngx_sprintf lines 1708-1710 |
| S010 | anchor_found | `An entity tag consists of an opaque quoted string, possibly prefixed by a weakness indicator.` | 15 | RFC 9110 sections 8.8.1 (Weak versus Strong) and 8.8.3 (ETag) |

Machine table: `ExecC3Quote.files/verdicts.tsv` - columns id, verdict, located_span,
units, chars, occurrences, node_index, node_bounded, location, anchor_clause, scope,
note. Every listed span measures ok=true under all five constraints (units, chars,
ASCII, no embedded double quote, page count == 1, node-bounded).

## NOTES:

**Distribution.** 9 rows `anchor_found`, 1 row `anchor_moved`, 0 `page_changed`, 0
`fetch_failed`. Receipts: S001 2529 B, S002 199999 B, S003 154136 B, S004 141818 B,
S005 240439 B, S006 138096 B, S007 453447 B, S008 512359 B, S009 147410 B, S010
1187554 B; all HTTP 200 on 2026-10-27; sha256 heads 4524ed61 / cc2473ed / 261408c5 /
6b9e240b / 7428ff4f / 7b63a76f / f5f5472f / 93281a63 / c58ebede / d4317606.

**S001 is anchor_moved, not anchor_found and not page_changed.** The row's anchor is
line-addressed: "inputs.include-hidden-files lines 17-20 and Archive artifact steps lines
37-39". The retained body is the row's FIRST URL, the v4.0.0 `action.yml` (2529 B, 86
lines). In it: `include-hidden-files` occurs 0 times (the input exists only in the
second URL, main 5f327015), the inputs block is lines 4-16 (name/path/retention-days),
line 17-20 is the outputs block, and the Archive artifact steps occupy lines 24-39,
42-57 and 60-76, not 37-39. The invariant-exclusion material the scope and teaches cells
rest on IS present and identical in all three runner steps (`tar --dereference
--hard-dereference`, `--exclude=.git`, `--exclude=.github`, `--exclude=".[^/]*"`), so the
page did not change. I read the mismatch as a relocated anchor, not a page change; I
signalled ExecC3Fetch to fetch the main body as `S001.main.html` and they declined for a
sound reason (contract C4 binds each retained body to a due-set row receipt; an
extra id could score C4 failed). Both halves of that C4 argument are recorded here rather
than asserted as truth: the C4 wording is "each retained body has a receipt ... receipt
URL = row URL".

**S001 and S002 carry a `scope=primary-url-only` marker.** Rows S001 and S002 each list
two URLs in the source cell and only the primary was fetched this round (one GET per row,
S003-S010 are single-URL). For S002 the verified clause is "v4.0.0 What's Changed":
the heading is in the release body and its text is exactly "Potentially breaking change:
hidden files (specifically dotfiles) will not be included in the artifact"; `v5.0.0`
occurs 0 times in the retained page (the v5.0.0 release page is the second URL), and
`Changelog` occurs only in "Full Changelog : v3.0.1...v4.0.0" and in the site navigation.
The v5.0.0 clause is unverified this round, not wrong. A Gate note should say so; it must
not be written as a page change.

**S008 line drift, same material.** The anchor names lines 8478-8617. The body has
`@end menu` at 8478, `@node controlling pattern-matching` at 8480,
`@unnumberedsubsec Controlling Pattern-Matching` at 8481 and the next `@node` (quoting
styles) at 8621, so the section is 8480-8620: drift +2 at the start, +3 at the end, inside
the +/-5 tolerance. Anchored-pattern and wildcard paragraphs are inside the section. If
the anchor cell is ever refreshed, 8480-8620 is the measured range; C3 itself only edits
recheck cells, so I did not touch it.

**S009 matches exactly.** `ngx_http_set_etag` line 1682 and the ETag `ngx_sprintf` at
1708-1710 (format literal 1708, `last_modified_time` 1709, `content_length_n` 1710), no
drift. The teaches' "%xT-%xO" format string is written in C as `"\"%xT-%xO\""`, so it can
not be quoted inside a Gate line without embedding ASCII double quotes; the quoted
candidate is the adjacent allocation statement that sizes the buffer.

**S005 quote constraint worth carrying to the Scribe.** The step-4 sentence ("Under
\"Custom domain\", type your custom domain, then click Save") occurs twice - the `apex`
section and the `subdomain` section carry it verbatim - and so does the teaches sentence
("no CNAME file is created, and any existing CNAME file is ignored and is not required").
Neither is page-unique, so neither can serve as the Gate quote. The quoted span is
section-specific (apex opening sentence). The step-4 ordinals were verified structurally:
in each section's ordered list the 4th `<li>` is the "Custom domain ... click Save" step
(apex list: 1 navigate, 2 Settings, 3 Pages, 4 Custom domain, 5 ALIAS/ANAME/A record ...;
subdomain list: 1 navigate, 2 Settings, 3 Pages, 4 Custom domain, 5 CNAME record ...).

**Node fragmentation is the binding constraint on quotes for the docs rows.** S003, S004,
S005 and S006 render inline `code`/`strong` elements, so one sentence spans several text
nodes (S003: node 244 "A", 245 "CNAME", 246 the sentence tail; S004: nodes 104-110;
S006: nodes 140-143). The quoted spans therefore start mid-sentence or at a sentence
boundary, which is allowed (substring rule) but means a re-phrased quote that crosses an
inline element will fail a node-scoped check. `&#x27;` in S006 is the served form of the
apostrophe and is quoted as served.

**S002 size.** The body is 199999 bytes, which looks like a round cap. It ends with
`</body>` / `</html>`, so it is not cut mid-markup, and the release body, "Full
Changelog", "Contributors" and "Assets" sections are all present. I did not verify the
served Content-Length (the receipt carries no headers); treat "complete document" as
[INFERENCE] from the closing tags.

**Redirects.** Only S010 shows a url != effectiveUrl difference, and it is the fragment
only (`#section-8.8` not sent on the wire). S003-S006 resolved without a path change.
S003's heading in the body is the longer "Creating a custom GitHub Actions workflow to
publish your site"; the anchor's shorter name still identifies the section.

**Not run / not claimed.** No counter was run (the counters are frozen by the L1 after
this wave); no claim after-state is scored here; this report is an evidence reading of ten
retained bodies, not a measurement of C3's six conditions. I did not fetch anything myself
and did not modify the registry, the lesson or any receipt. Verdicts are inputs for
ExecC3Pins (pin only on `anchor_found`, and for S002 read the primary-url note first) and
for the Gate-line scribe (the located spans above are validated quote candidates).

**Tooling.** No install or upgrade was needed or performed (stdlib Python 3 only; no
pacman, no npm/uv). Scratch `/fast/scratch/hyaku/kake-r61/ExecC3Quote/` held the scripts
and was removed after the helpers were copied into `ExecC3Quote.files/`; nothing was
cited from `/tmp`.

VERDICT: 10/10 due rows re-located in the retained fresh bodies - 9 anchor_found, 1 anchor_moved (S001: exclusion material present at lines 24-72, anchor's lines 17-20/37-39 address the unfetched main-commit body), 0 page_changed, 0 fetch_failed; every reported span is page-unique, node-bounded and 6..25 units.
