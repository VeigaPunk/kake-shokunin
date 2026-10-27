# ScribeC2Entry

Claim C2 (operability) scribe seat, round-61 wave w1. Deliverable: a draft of
`corpus/knowledge/response-header-expectations.md` — **drafted, not installed**. The lane corpus file was
not written; the draft lives in this seat's `.files/` directory for the L1 to move.

## ENTRY:

`/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-61/w1/ScribeC2Entry.files/entry.md`
(2001 words, 13 double-quoted spans, sha256 of the file at the end of this report).

Shape, per CORPUS.md: frontmatter opens `source: S430, S431, S432, S433` / `verified-at: 2026-10-27`
/ `recheck: 180d`, then `fetches:`, `ground:`, `scope:`, `coverage:`, `falsifier:`; body has one
section per expectation class — `content_type_present`, `hsts_present`, `xcto_nosniff_value`,
`csp_present`, `singleton_fields`, `field_name_syntax` — each with its located quote(s), a plain
publisher reading, and the class's audit semantics; then `## Lane use` (capture → manifest → audit,
plus what is NOT claimed) and `## Limits`.

## SPAN CHECK:

Verified with the shipped checker, run from the lane root:

```
python3 -B .ufo/waves/round-61/w1/ScribeC2Entry.files/quote_check.py
spans=13 all_ok=True      # exit 0
```

The checker requires, per span: exactly one of the four bodies contains it; substring of one
whitespace-collapsed text node under BOTH an HTMLParser reader (charrefs decoded, script/style
skipped) and a `>[^<>]+<` regex reader (raw text, no entity decoding); exactly one occurrence in the
collapsed body; 6..25 whitespace units; ≤160 chars; no curly double quote.

| # | row §section | units | chars | page-unique | class |
|---|---|---|---|---|---|
| 1 | S433 §5.5 Field Values | 10 | 62 | yes | trimming convention |
| 2 | S433 §8.3 Content-Type | 22 | 139 | yes | content_type_present |
| 3 | S430 §7.1 | 13 | 71 | yes | hsts_present |
| 4 | S430 §6.1 | 24 | 136 | yes | hsts_present |
| 5 | S432 §3.6 | 8 | 36 | yes | xcto_nosniff_value |
| 6 | S432 §3.6 | 9 | 62 | yes | xcto_nosniff_value |
| 7 | S431 §3.1 | 18 | 103 | yes | csp_present |
| 8 | S433 §5.2 | 11 | 61 | yes | singleton_fields |
| 9 | S433 §5.3 (Set-Cookie note) | 10 | 53 | yes | singleton_fields |
| 10 | S430 §7.1 | 17 | 89 | yes | singleton_fields |
| 11 | S433 §5.6.2 | 12 | 82 | yes | field_name_syntax |
| 12 | S433 §5.1 | 16 | 94 | yes | field_name_syntax |
| 13 | S433 §5.1 | 11 | 70 | yes | field_name_syntax |

The entry contains no other double-quoted span; the only other quoted literal is the single-quoted
shell pipeline `jq '.checks|length' …` in `## Lane use`. Quotes are in
`.files/spans-map.json` (quote → row → section → class) and the machine output in `.files/spans.json`.

Bodies: the retained `.ufo/waves/round-61/sources/S43{0,1,2,3}.html` written by ScoutC2Sources,
sha256 `f086bfac…c72c0a` (S430), `be8f2468…e3144e` (S431), `63b0a018…bad911b` (S432),
`d4317606…368fe1e5` (S433), matching `sources/receipts.json` (HTTP 200, 2026-10-27T09:14:55Z,
userAgent `round61`). My own scratch GETs produced byte-identical files (same four sha256), so the
span checks above run against the retained bytes, not a private copy.

## READINGS:

Sentences that are the lane's reading, not the source's statement (marked `[INFERENCE]` or attributed
in place in the draft):

1. `content_type_present`: "[INFERENCE] Two consequences follow for a publisher … not convenience",
   and "Because the source's modal is SHOULD, the audit's rule is the lane's declared policy,
   stricter than the sentence quoted here" (the RFC's modal is SHOULD, node-read; the policy
   upgrade is the lane's).
2. `content_type_present` audit semantics: "A response with no Content-Type is a finding under the
   declared policy, not a proof that a client will guess the type wrongly".
3. `hsts_present`: "[INFERENCE] For a publisher this reads as: an https surface that never sets the
   field leaves a browser free to reach it over plain http on a later navigation".
4. `xcto_nosniff_value`: "[INFERENCE] The rule is therefore a quality rule on a publisher's own
   choice, not a demand that every surface set the field".
5. `csp_present`: "[INFERENCE: … that a recorded response is the right artifact to read is this
   lane's reading]".
6. `singleton_fields`: "`Set-Cookie` can never be a singleton under this rule … and treating the name
   as never single is the audit's declared rule" (the special case is S433 §5.3's; never-singleton is
   the audit's rule).
7. `field_name_syntax`: "[INFERENCE] A recorded name carrying a space … is not a field name at all".
8. `field_name_syntax` audit semantics: the class applies to every check because the version-1
   `expect` object carries no toggle (tool/contract fact, not a source statement).
9. `## Limits`: bullets 1, 2 (the consequence clause) and 5 are marked `[INFERENCE]`; the
   comma-list reading of the singleton class cites S433 §5.2 for what a field line may carry.

## Behavior

- Read the round-61 contract and `contract.json`, the canonical `kimi-shokunin/…/protocol/CORPUS.md`
  entry rules, and the round-60 `c60_quote_truth.py` / `spans.py` to reuse the lane's existing
  text-node/collapse convention.
- Fetched the four sources once each into scratch to derive spans early; the retained bodies later
  proved byte-identical, and every span was re-checked against them. Each span's section was read
  off the retained body's nearest preceding numbered heading, not assumed.
- Drafted the six-class entry, `## Lane use` (from the actual `scripts/response_snapshot.py` and
  `scripts/header_audit.py` docstrings and the landed `capture/manifest.json`), and `## Limits`.

## Gates

| gate | command | result |
|---|---|---|
| span truth (13 spans) | `python3 -B .ufo/waves/round-61/w1/ScribeC2Entry.files/quote_check.py` | exit 0, `spans=13 all_ok=True` |
| body identity | `sha256sum` scratch copies vs `.ufo/waves/round-61/sources/S43*.html` | 4/4 equal; matches `receipts.json` |
| manifest count cited in `## Lane use` | `jq '.checks|length' .ufo/waves/round-61/capture/manifest.json` | 12 |
| curly-quote scan | `grep -n '[“”„‟]'` on the draft | no matches |

Not run by this seat: `scripts/header_audit.py`, `response_snapshot.py`, any round-61 counter, any
score. No after-state is scored here.

## Touched surfaces

- Written: `.ufo/waves/round-61/w1/ScribeC2Entry.files/` (entry.md, quote_check.py, spans.json,
  spans-map.json) and this report `.ufo/waves/round-61/w1/ScribeC2Entry.md`.
- Scratch `/fast/scratch/hyaku/kake-r61/ScribeC2Entry/` removed before the report was finalised.
- No lane corpus file, registry row, lesson, counter, tool, jj/git state, sibling lane or fleet file
  was written; `/home/vgpnk/Projects/shokuknow` untouched. No installs (no pacman, no `uv tool`) —
  `curl`, `jq` and `python3` were already present.

## Findings

- **F1 — S432 fragments prose at every inline element.** The WHATWG Fetch body breaks a sentence at
  each `code`/`var` element, so the two `xcto_nosniff_value` spans are short (8u/36c and 9u/62c) and
  the normative value grammar (`X-Content-Type-Options = "nosniff" ; case-insensitive`) is cited by
  location instead of quoted. The draft says this in place; semantic support for that class leans on
  a located unquoted block, which a w2 critic should test rather than assume.
- **F2 — mid-sentence spans.** The `csp_present`, `hsts_present` (span 3) and `hsts_present` (span 4)
  quotes begin after the field name or after the transport condition, which sit in preceding nodes.
  Each draft paragraph states what precedes the span; no quote is presented as a whole sentence.
- **F3 — two rule-level facts come from the tool, not the sources.** Never-singleton `Set-Cookie`
  and the always-on `field_name_syntax` class are the audit's declared rules; the draft attributes
  them that way instead of attributing them to RFC 9110.
- **F4 — citation anchors were derived, not inherited.** `§5.5`, `§5.2`, `§5.3`, `§6.1`, `§7.1`,
  `§8.3`, `§5.1`, `§5.6.2`, and Fetch `§3.6` / CSP `§3.1` were each read off the retained body's
  nearest preceding heading node; the registry Gate lines the L1 writes should use the same anchors.

## Out of scope

Lane-file installation, registry rows S430–S433, lesson `## Gate` lines, counters, capture, audit
runs, scoring, and any colleague's artifacts. The draft's `## Lane use` describes the flow; it does
not claim the audit ran or that any surface is clean.

## Artifacts

`.ufo/waves/round-61/w1/ScribeC2Entry.files/` — `entry.md`, `quote_check.py`, `spans.json`,
`spans-map.json`.

Digests at hand-off (sha256, `sha256sum` 2026-10-27):

```
3f469dee…bea7e1dd  entry.md        (2001 words)
0ef1e1dc…3fbba315  quote_check.py
c9d195d9…02d25110  spans.json
02a37a21…7ea101a4  spans-map.json
```

VERDICT: C2 entry drafted (six classes, 13/13 spans node-contained and page-unique against the sha256-pinned retained bodies) but NOT installed; S432's short quotable fragments and two tool-level rules are flagged as support limits for w2.
