# Falsify S020 — round-26 freshness recheck (receipt HOLD)

Target: receipt `.ufo/waves/round-26/rechecks/S020.json` (verdict HOLD, fetchIndex 1) and the
SOURCES row line `corpus/SOURCES.md:28` (teaches «Relative and cross-host targets are permitted;
duplicate/superset content is not established by a static declaration audit»; anchor «Section 3,
April 2012 Informational RFC; opened 2026-10-20»). Candidate
`e28312b14b076584fedd696fae2a684e460bd11e`, base `97404de4ff73d6c8a4f87385cf5fdf36dca7f006`.
Axis: freshness. Milestone: r26-recheck-falsify.

**Verdict: AGREE.** The receipt's quote really grounds this row's teaches (it is row-specific, not
page chrome, and its neighbours in the same bullet list carry the rest of the teaches verbatim); the
anchor description is correct in the raw bytes; and no content or version change is missed — the
live page is byte-identical to the retained bytes. Only a low-severity completeness note survives
(the receipt's paraphrase of §3's MAY list omits its sixth bullet), which does not affect the
teaches, the verdict, or any counter rule.

## Attack 1 — does the quote ground THIS row's teaches, or just chrome / a neighbour clause?

The teaches has two clauses: (a) relative and cross-host targets are permitted; (b) duplicate/
superset content is not established by a static declaration audit. The receipt's quote
(`rechecks/S020.json:5`) is:

    "The target (canonical) IRI MAY: o Specify a relative IRI (see [RFC3986], Section 4.2)."

That single string grounds clause (a)'s *relative* half only, so the attack must check whether the
rest of the teaches is grounded by the same anchor or is a neighbouring clause imported from
elsewhere. It is the same anchor. In the retained bytes (`fetched/S020-1.raw.gz`, decompressed
18428 bytes, sha256 `87a13951ce93195e9a52915e6d170eebd4c48260576b637407bb96ea8c47f5e4`), the
§3 MAY list is contiguous and each item is unique (offset / count):

    4613  1x  "The target (canonical) IRI MAY:"
    4649  1x  "o  Specify a relative IRI"                     <- the quoted bullet
    4750  1x  "o  Be self-referential"
    4816  1x  "o  Exist on a different hostname or domain."   <- cross-host half of clause (a)
    5184  1x  "o  Have different scheme names"
    5274  1x  "o  Be a superset of the content at the context IRI."

and the §3 MUST plus the §5 recommendation that carry clause (b):

    4073  1x  "The target (canonical) IRI MUST identify content that is either duplicative or a
                 superset of the content at the context (referring) IRI."
   10946  1x  '<span class="h2"><a class="selflink" id="section-5" href="#section-5">5</a>.
                 Recommendations</span>'
   11057  1x  "verification of the\n   following is RECOMMENDED:"

So clause (b)'s reading — RFC 6596 §3 states a content condition (MUST) while §5 makes
*verification* RECOMMENDED, hence a static declaration audit cannot establish duplication or
superset — is grounded in the same document at the same anchor, and the receipt's `reason`
(`rechecks/S020.json:7`) states it in exactly those terms ("Section 3 imposes a content condition
and Section 5 only RECOMMENDS verifying duplication"). The RFC's own status disclaimer
("This document is not an Internet Standards Track specification", 1x at raw offset 650) also
matches the row's scope cell «Preferred canonical relation semantics, not an Internet Standards
Track conformance claim», which the reason asserts.

Row-specificity (QUALITY.md round-26: "A recheck HOLD needs a row-specific located quote"):
recomputing every population row's effective text with the committed
`.ufo/waves/round-26/source_text.py` over the manifest's gzip bytes, the normalized quote occurs in
exactly one row's text — S020 index 1 (`fetched/S020-1.raw.gz`) — and nowhere else, including the
RFC 9110 html/txt group {S010,S028,S033} (`measure.py:406-422`). It is not page chrome: it is
normative body text inside §3's list. Quote shape satisfies the counter rules in
`measure.py:388-392`: 15 alphanumeric tokens (≥6) and 14 whitespace words (≤25), and
word-bounded presence in the effective text is True.

## Attack 2 — is the anchor observed correct in the raw bytes?

The receipt's `anchorObserved` (`rechecks/S020.json:6`) says: "Section 3 'The Canonical Link
Relation', page 2, bullet list 'The target (canonical) IRI MAY' (text view is one collapsed
line)". Verified against the raw bytes, not the flattened view:

* Section 3 heading markup is at raw offset 3956:
  `<span class="h2"><a class="selflink" id="section-3" href="#section-3">3</a>.  The Canonical Link Relation</span>`.
* The RFC's own page footers bracket it: `[Page 1]` @2295, `[Page 2]` @4951. The heading (3956) and
  the quoted bullet (4649) both fall between them → **page 2** as claimed. (For completeness, the
  remaining MAY items — scheme names @5184, superset @5274, temporary redirect @6465 — fall after
  the `[Page 2]` footer, i.e. printed page 3; the receipt's anchor locates only the quoted bullet,
  so this is not a misdescription.)
* "one collapsed line": `fetched/text/S020-1.txt` is 11893 bytes with a single `\n` (one content
  line + trailing newline). Recomputing the view from the retained bytes with the *candidate's*
  `source_text.py` (sha256 `55ae7abc52a5acfd95a86d96c27f12898c30e33ab63cfa7f383640120f57b7d6`,
  identical in worktree and at the candidate) reproduces the committed blob exactly:
  `view + "\n" == git show e28312b:.ufo/waves/round-26/fetched/text/S020-1.txt` → True, and the
  quote occurs exactly once in that view.

## Attack 3 — did content or version change in a way the receipt missed?

One plain public GET of the URL already recorded in `corpus/SOURCES.md:28`
(`https://www.rfc-editor.org/rfc/rfc6596.html`), response piped to a digest only, not saved as a
source of truth:

    HTTP/2 200 ; date: Wed, 21 Oct 2026 16:29:56 GMT ; content-type: text/html
    etag: W/"1f65f165b8c9875f57dc0859adaaf8c2"        (identical to manifest etag)
    18428 bytes ; sha256 87a13951ce93195e9a52915e6d170eebd4c48260576b637407bb96ea8c47f5e4

The live body is **byte-identical** to the retained bytes (`live == retained` → True), so nothing
drifted between 2026-10-21T15:10:43Z and now. The receipt's "still renders RFC 6596 as
Category: Informational, April 2012" is confirmed in the bytes ("Category: Informational" 1x @151,
"April 2012" 8x @213 as page runners). The retained bytes carry no version churn markers:
"Updated by" 0x, "Obsoleted by" 0x, "Obsoletes" 0x, "Updates" 0x, "Errata" 0x (the single lowercase
"errata" is boilerplate in the Status-of-This-Memo paragraph). RFC 6596 is an immutable RFC, so a
recheck tests availability + anchor, not content drift — exactly what the receipt claims.

## Attack 4 — receipt/ledger/counter consistency

* Strict JSON parse of `rechecks/S020.json` yields exactly the required key set
  `{id, verdict, fetchIndex, quote, anchorObserved, reason, correction}` (`measure.py:52`), no
  duplicate names, `verdict="HOLD"`, `correction=null` (required for HOLD, `measure.py:401`),
  `fetchIndex=1`.
* `fetchIndex` 1 resolves: population fetch sha256 == manifest sha256 == sha256 of the decompressed
  `fetched/S020-1.raw.gz`; manifest `file` == population file basename
  (`manifest.json:358-374`). No `manifest-retry.json` entry for S020 (retry holds S008 only).
* Ledger `.ufo/waves/round-26/statements.json:137-146` records S020 as `statements 13,
  seatStale 1, stale 0`, `l1Disposition "R2 is a verification-date stamp only; content HOLD."` —
  i.e. the seat's date-only R2 was adjudicated non-stale, and HOLD is the row-level verdict. Since
  `stale == 0`, no `[r26-recheck S020 STALE]` tag is required in the corpus file
  (`measure.py:425-454`), and indeed none is present. The receipt's HOLD and the ledger agree.
* The row's `opened 2026-10-20` cell is untouched at the candidate (`git diff base..candidate --
  corpus/SOURCES.md` touches only the round-26 bounded-recheck paragraph, no row cell), and per
  `corpus/QUALITY.md:217-220` a historical verified-at date is not a stale claim.

## Findings

1. **Low / note (no correction needed).** The receipt's `reason` paraphrases §3's MAY list as
   "MAY be relative, self-referential, on a different hostname/domain, on a different scheme, or a
   superset" — it omits the list's sixth item, `o  Be the source IRI of a temporary redirect. For
   HTTP, this refers to status codes 302, 303, or 307 (Sections 10.3.3, 10.3.4, and 10.3.8,
   respectively, of [RFC2616])` (raw offset 6465, 1x). The omission is harmless for this row: the
   teaches says nothing about redirects, and no corpus statement depends on the redirect item
   (`corpus/knowledge/static-canonical-preflight.md:13-16` and `corpus/lessons/round-22.md:43`).
   Worth recording only because the omitted bullet is the one carrying obsolete normative
   references — RFC 2616 is cited 6x and RFC 5988 5x in the retained bytes, both superseded
   (RFC 2616 by RFC 9110; RFC 5988 by RFC 8288). A new source row would be needed before any claim
   leaned on those citations, exactly as the lane already does for RFC 9557 vs RFC 3339
   (`corpus/knowledge/static-canonical-preflight.md:194`).
2. **Note (prose, not a quote).** The reason's compression "the target IRI MUST be duplicative or a
   superset of the context content" restates §3's actual MUST ("MUST identify content that is
   either duplicative or a superset of the content at the context (referring) IRI", raw 4073). The
   `quote` field itself is verbatim; only the prose paraphrase is compressed, which the round-26
   rule allows.
3. **Residual gap, not a defect.** Errata / obsoleted-by status for RFC 6596 is not carried by the
   retained bytes (that metadata lives on the RFC Editor info page, not on the row URL), so the
   receipt's "no version change" rests on the byte-identity of the row URL plus RFC immutability.
   The in-wave seat already covered the info page and the errata search as a live supplement
   (`w1/PairS020StaticCanonicalPrefl.md:7`: info page shows Informational with no obsoleted-by or
   updated-by entry; errata search for rfc_number=6596 returns "No matching errata found."). My GET
   was restricted to the row URL already in `corpus/SOURCES.md`, so I did not re-fetch those.

## Correctness of the corpus consequences

`corpus/knowledge/static-canonical-preflight.md:13-16` (the S020-dependent statements) and
`corpus/lessons/round-22.md:43` (which quotes the same Section 3 sentence verbatim) are all
supported by the re-fetched bytes: "Specify a relative IRI (see [RFC3986], Section 4.2)." 1x,
"Exist on a different hostname or domain." 1x, the §3 MUST 1x, "verification of the following is
RECOMMENDED" 1x. Nothing in the candidate needs correcting for S020.

## Process notes / tooling

No tool was installed or upgraded (nothing was missing; `gzip`, `git`, `python3`, `sha256sum`,
`curl` were already present and sufficient). Channel/reason: n/a — no install performed.

Disclosure of one bound deviation: I initially wrote the live GET body and the decompressed raw to
`/tmp/s020.live.html`, `/tmp/s020.live.headers` and `/tmp/s020.raw.html` instead of keeping them
in memory; all three were deleted immediately afterwards (verified absent) and no lane, corpus,
script or Git state was touched (`git status --porcelain` shows only pre-existing untracked wave
directories). The single permitted public GET was to the row URL already listed in
`corpus/SOURCES.md`. No round-24 artifact was opened, run, rephrased or rerouted; `measure.py` was
read only as evidence and **not** executed (not named by this item).

```json
{"target":".ufo/waves/round-26/rechecks/S020.json (HOLD) + corpus/SOURCES.md:28 row S020","verdict":"AGREE","severity":"none"}
```
