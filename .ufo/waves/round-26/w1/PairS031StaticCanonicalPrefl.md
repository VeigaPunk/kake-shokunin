# PairS031 × static-canonical-preflight — round-26 freshness recheck (C1)

Pair: S031 (WHATWG HTML Living Standard, "Parsing HTML documents, in body and foreign content") × `corpus/knowledge/static-canonical-preflight.md`, Round 23 section (lines 96–119) and the corrections and later sections that were checked for S031 reliance.

**Result: 8 statements depend on S031 — 8 HOLD, 0 STALE, 0 UNVERIFIABLE. No append-only correction is required.**

## Pinned inputs

- Entry bytes judged: sha256 `192eac303fa3ba8a2aab9d545fe6b0627f3a174dff1b54472e1bab2f771fdaf7` (14,076 bytes).
- Re-fetch record (`fetched/manifest.json` index 1, lines 566–584): URL `https://html.spec.whatwg.org/multipage/parsing.html#parsing-main-inforeign`; status 200; finalUrl identical; fetchedAt `2026-10-21T15:10:50.839991+00:00`; content-type `text/html; charset=utf-8`; last-modified `Tue, 20 Oct 2026 12:58:33 GMT`; etag `"6ad76579-c9b8f"`; 826,255 bytes; decoded sha256 `a11dcf1768a76e24cdf7e16060f54bcb149c529aa8bcb9297b8d1ab633b26f13`, equal to the manifest value and to the `population.json` S031 fetch record (lines 695–718). The gzip container `S031-1.raw.gz` digests to `b44a7a7e…`, which is not the recorded value.
- Round-23 digest: the same decoded digest for `parsing.html` (826,255 bytes, "Last Updated 20 October 2026") is recorded at `.ufo/waves/round-23/residual/FixDocsEvidence.md:19` and `.ufo/waves/round-23/w2/ReopenS030.md:15`. The S031 bytes are therefore unchanged since the round that wrote the S031 claims.
- Text view `fetched/text/S031-1.txt`: 280,153 bytes, sha256 `36d5001aa8e67f2588c6a503946b503a9ffa9e8b113dbe791cddc5a2de7d3647`; single line; header "HTML Living Standard — Last Updated 20 October 2026".
- Anchor ids present once each in the raw HTML (unquoted `id=` attributes): `parsing-main-inforeign`, `parsing-main-inbody`, `parsing-main-inhead`, `tree-construction-dispatcher`.
- Text-view section offsets (character index in `S031-1.txt`): 13.2.6 Tree construction 128029; 13.2.6.4.4 "in head" 161551; 13.2.6.4.6 "after head" 174474; 13.2.6.4.7 "in body" 176352; 13.2.6.5 "The rules for parsing tokens in foreign content" 234791 (table-of-contents copies at 4587 and 5259).

## Statement verdicts

Offsets are character indexes in `fetched/text/S031-1.txt`. Each quote is an exact substring of that file and is 25 words or fewer.

| ID | file:line | Statement (abridged) | S031 role | Verdict | Verbatim quote(s) from S031-1.txt (char) | anchorObserved | Reason |
|---|---|---|---|---|---|---|---|
| K1 | corpus/knowledge/static-canonical-preflight.md:98-101 | "S031 (WHATWG parsing: in-body `<svg>`/`<math>` insert foreign elements; breakout tags and integration points return to HTML rules)" | cited source and its teaching | HOLD | "Insert a foreign element for the token, with SVG namespace." (198947); "While the current node is not a MathML text integration point, an HTML integration point, or an element in the HTML namespace," (236008); "If the adjusted current node is an HTML integration point and the token is a start tag" (129146) | 13.2.6.4.7 "in body", svg start-tag rule (from 198638); 13.2.6.5 breakout branch, "br", "p" end tag (from 235956); 13.2.6 dispatcher (129146) | All three clauses of the teaching are present: in-body svg/math insert foreign elements, breakout pops to HTML rules, integration points are dispatched to HTML rules. Matches SOURCES.md:39 `teaches` and the `population.json` S031 `teaches`. |
| K2 | static-canonical-preflight.md:103-104 | "After an explicitly closed head it now evaluates, instead of rejecting the whole page" | the gate depends on in-body processing starting only after the head ends | HOLD | "Pop the current node (which will be the head element) off the stack of open elements." (165842); "Insert an HTML element for a "body" start tag token with no attributes." (176175) | 13.2.6.4.4 "in head", end tag "head" (165842); 13.2.6.4.6 "after head", anything-else (176175), before the 13.2.6.4.7 heading at 176352 | An explicit `</head>` pops the head, and SVG/MathML tokens reach 13.2.6.4.7 only after the head ends. The gate is a local rule consistent with that text. |
| K3 | static-canonical-preflight.md:106-107 | "SVG/MathML subtrees whose tokens contain no `base`, `head` or canonical-looking `link`, and whose end tags match a modelled element stack exactly" | foreign-content breakout list and end-tag rule | HOLD | '"h6", "head", "hr", "i", "img", "li", "listing", "menu", "meta", "nobr", "ol", "p", "pre"' (235666); "is not the same as the tag name of the token, then this is a parse error." (239665) | 13.2.6.5 breakout start-tag list (from 235451); 13.2.6.5 "Any other end tag" (from 239411) | The spec lists `head` as a breakout tag and makes a mismatched foreign end tag a parse error, so the exact-match rule is consistent with S031 and stricter than it. The `base`/`link` refusals are local policy: they are ordinary foreign elements under "Any other start tag" (236306). |
| K4 | static-canonical-preflight.md:107-109 | "SVG/MathML `title`/`style`/`script` are tokenized, not treated as HTML raw text, so markup hidden there stays visible (SVG `title` is an HTML integration point)" | integration-point definition; foreign insertion; SVG script rule; raw text as an HTML in-head effect | HOLD (precision note) | "An SVG foreignObject element An SVG desc element An SVG title element" (130338); "An end tag whose tag name is "script", if the current node is an SVG script element" (238516); "Follow the generic raw text element parsing algorithm." (163573) | 13.2.6 intro, HTML integration point definition (130338); 13.2.6.5 SVG script end-tag branch (238516); 13.2.6.4.4 "in head" raw-text rule for `noframes`/`style` (163573) | SVG title is an HTML integration point. Foreign insertion in 13.2.6.5 sets no raw-text state; raw text is an effect of the HTML in-head rules only. Precision note: an HTML raw-text start tag nested inside an HTML or MathML integration point is dispatched to HTML rules ("If the adjusted current node is a MathML text integration point and the token is a start tag", 128785; dispatcher 129146) and switches to raw or RCDATA (163386, 163573). The "stays visible" rationale therefore covers the SVG/MathML element's own tokens, not nested raw-text regions. The tool-behavior half is not decided by S031 and was not checked here. |
| K5 | static-canonical-preflight.md:113 | "Still `html_unsupported`: SVG/MathML before the head closes" | in-head anything-else, then in-body svg rule | HOLD | "Anything else Pop the current node (which will be the head element) off the stack of open elements." (172967) | 13.2.6.4.4 "in head", anything-else (172967; section ends before the 13.2.6.4.5 heading at 173133); in-body svg rule (198638) | In the spec, an SVG start tag seen in head is an anything-else token that pops the head and is reprocessed, and the in-body svg rule applies only afterwards. Refusing SVG before an explicit `</head>` is a stricter local rule consistent with the text. |
| K6 | static-canonical-preflight.md:113-114 | "any `base`, `head` or canonical-looking `link` token inside SVG/MathML" | breakout list (head); foreign insertion (base, link) | HOLD | '"h6", "head", "hr", "i", "img", "li", "listing", "menu", "meta", "nobr", "ol", "p", "pre"' (235666); "Insert a foreign element for the token, with the adjusted current node 's namespace." (238024) | 13.2.6.5 breakout list (235666); 13.2.6.5 "Any other start tag" branch (from 236306) | `head` is a breakout tag in S031. `base` and `link` are ordinary start tags that become SVG/MathML elements, not HTML base or link elements. The refusal is conservative policy that the text neither requires nor contradicts. |
| K7 | static-canonical-preflight.md:114-115 | "mismatched or unclosed foreign end tags" | "Any other end tag" rule | HOLD | "is not the same as the tag name of the token, then this is a parse error." (239665) | 13.2.6.5 "Any other end tag" (from 239411) | The spec defines a mismatched foreign end tag as a parse error. An unclosed foreign element surfaces as such a mismatch when an ancestor's end tag arrives. Refusing both is consistent. |
| K8 | static-canonical-preflight.md:115-117 | "any `<base>` after the head, in or out of foreign content, because a body base is still the document's first base in tree order (S024)" | in-body head-type rule (out-of-foreign half); foreign insertion (in-foreign half); S024 is the rationale but sits outside this pair | HOLD (rationale precision note) | '"base", "basefont", "bgsound", "link", "meta", "noframes", "script", "style", "template", "title"' (177850); "Insert an HTML element for the token. Immediately pop the current node off the stack of open elements." (162223) | 13.2.6.4.7 "in body", head-type list (177850); 13.2.6.4.4 "in head", base rule (162185–162223); 13.2.6.5 "Any other start tag" (from 236306) | Out of foreign content, S031 routes an in-body `base` through the in-head rules, which insert an HTML base element, so a body base exists. Inside foreign content, S031 makes the token a foreign element, so "a body base" does not describe it. The foreign-content half is conservative policy; its S024 rationale is outside this pair. |

## Considered and excluded (no S031 reliance)

| file:line | Text (abridged) | Reason excluded |
|---|---|---|
| :103 | "The tool is still not an HTML5 tree builder." | Limitation framing grounded in S026 (HTMLParser docs), not in S031. |
| :110-111 | Self-closed void elements; `<div/>` stays unsupported | S030 slash rule. The S031 self-closing rule applies only to foreign elements. |
| :117-119 | "Before this fix the round-23 candidate reported six such pages clean (w1/FalsifyForeignContent)…" | Historical claim about a w1 falsifier count; it cites no S031 text. |
| :140-146 | `[r23-correction]` tails | Cite S021 and S025, not S031. |
| :151 | S030 trailing-solidus caveat | S030 syntax rule. |
| :153 | Meta refresh, redirect and rendering limits | Cites no source among S031. |
| :157-179 | Round 24 receipt replay section | Cites S032–S034 only. |
| :1-2 | `source:` and `verified-at:` header | Lists S020–S029 and does not name S031 (see F2). |

## Flags (no verdict; no correction required)

- **F1. No r20 tails.** A grep of the entry for `r20` returns no matches. The only correction tags are `[r23-correction]` at lines 140 and 143, and neither cites S031. No `[r26-recheck …]` block exists yet; none is needed for HOLD verdicts.
- **F2. Provenance header gap.** Lines 1–2 list S020–S029 only. The Round 23 body (lines 98–101) cites S024, S030 and S031, and the S031 verification date appears in `corpus/SOURCES.md:39` and `population.json`, not in the entry header. This is not a STALE finding; an append-only provenance note is a planner decision.
- **F3. Superseded-version, date and anchor check: none superseded.** The SOURCES pin "Living Standard last updated 20 October 2026" matches the re-fetched text. The anchors `parsing-main-inforeign` and `parsing-main-inbody` exist in the raw HTML, and the section numbers 13.2.6.4.7 and 13.2.6.5 are present. The Round 23 heading date matches the SOURCES row's `opened` date, and the digest is unchanged since round 23.
- **F4. Out-of-pair pointer.** `.ufo/waves/round-23/w2/ReviewLessonGate.md` (lines 61–65) reported swapped digest prefixes for `syntax.html` and `parsing.html` in a source table. The S031 digest in `population.json` (`a11dcf…`) matches the re-fetched `parsing.html` bytes, so S031 is unaffected. Whether the swap was corrected in its source table is outside this pair and was not checked.
- **F5. Sibling cross-read.** `w1/RowS031.md` (row seat) reports HOLD on the same decoded digest and the same passages. Its svg-branch offset (198638) agrees with this report. No contradiction was found.

## Corrections

None. There are zero STALE verdicts, so no append-only correction blocks are proposed.

## Verification performed (read-only)

- Read the full entry. Grepped it for `S031`, `r20`, correction tags, and foreign-content keywords; the matches fall only within lines 98–119.
- Checked the S031 fetch record (`manifest.json` 566–584, `population.json` 695–718, `SOURCES.md:39`) and the round-23 digest records.
- Decoded `S031-1.raw.gz`; the sha256 of the decoded body matches the manifest. The four anchor ids are present in the raw HTML.
- All 17 quoted strings are exact substrings of `S031-1.txt`. The raw HTML wraps lines and carries inline markup, so the raw cross-check was approximate: 16 of 17 quotes match after tag removal and whitespace normalization, and the 17th (the integration-point list) matches once list-item boundaries are read as spaces.
- No builds, tests or linters were run. No network fetches were made. No file outside this report was written.

## Tooling

No tools were installed or upgraded. Read-only checks used the eval kernel's Python 3 standard library (`gzip`, `hashlib`, `html`, `pathlib`, `re`). No scratch files were written and nothing was written to `/tmp`.

## Gaps

- K4's tool half (that the local tokenizer treats SVG/MathML title, style and script as tokens) is a local-receipt question. It was not checked here, and no tests were run.
- K8's S024 rationale and the document-base algorithm are outside this pair's S031 text.
- The judgement is against the fetch at 15:10:50Z. No later drift was checked.
- Suggested for L1 (not written by this seat): the S031 row's recheck cell may record this HOLD, which the appendOnly rule allows.

```json
{"pair":"S031xstatic-canonical-preflight","statements":8,"hold":8,"stale":0,"corrections":[]}
```
