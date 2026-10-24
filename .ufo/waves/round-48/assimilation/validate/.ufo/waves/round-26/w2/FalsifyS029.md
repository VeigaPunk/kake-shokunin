# FalsifyS029 — round 26 C1 FRESHNESS, author-side falsification of row S029

Target: receipt `.ufo/waves/round-26/rechecks/S029.json` (verdict HOLD) and the SOURCES.md row
`S029 | RFC 3986: URI Generic Syntax — https://www.rfc-editor.org/rfc/rfc3986.txt`.
Milestone: r26-recheck-falsify. Judged on: freshness. Date: 2026-10-21.

**Verdict: AGREE** (HOLD is correct; no correction). Severity: **none**.

## Axes attacked

1. **Digest/pin freshness** — does the retained bytes still match the row's pin, and does the live
   source still serve them?
2. **Anchor correctness in raw bytes** — is the quoted sentence really at the cited lines/page, inside
   §3 and immediately after the hier-part ABNF, and free of page chrome?
3. **Quote→teaches grounding** — does the quote carry *this* row's teaches, or only a neighbouring
   clause / page furniture?
4. **Receipt-schema / counter rules** — does the receipt satisfy the amendment's quote rules and
   measure.py's checks (token counts, word-bounded match, row specificity)?
5. **Consumer drift** — do the citing corpus files (`static-canonical-preflight.md`,
   `lessons/round-22.md`) still say what the row teaches?

## Evidence

### 1. Digest and live content (freshness)

```
$ gunzip -c .ufo/waves/round-26/fetched/S029-1.raw.gz | sha256sum
3102dae4b68cebe40337730312fcb612297b8928547267e8b3d1ee6002b2d683  -
$ gunzip -c .ufo/waves/round-26/fetched/S029-1.raw.gz | wc -c
141811
```

Matches the row's pin (`plain text sha256 3102dae4…b2d683`, SOURCES.md line 37) and the manifest row
(`fetched/manifest.json`, `{"row":"S029","index":1,"status":200,"bytes":141811,"sha256":"3102dae4…b2d683",
"file":"S029-1.raw.gz","fetchedAt":"2026-10-21T15:10:49.846088+00:00"}`).

Plain public GET of the row URL (the one allowance; not saved), compared against the retained view:

```
$ curl -sS -L --max-time 60 -o - https://www.rfc-editor.org/rfc/rfc3986.txt | sha256sum
3102dae4b68cebe40337730312fcb612297b8928547267e8b3d1ee6002b2d683  -
141811 bytes
```

Live bytes are **byte-identical** to the retained bytes and to the row's pin. No content change since
open (2026-10-21) and no version drift visible in the document header itself
(`STD: 66`, `Updates: 1738`, `Obsoletes: 2732, 2396, 1808`, January 2005 — lines 4-10 of the raw text).
No page furniture, erratum or editorial change touches §3: the round's own statement-level seat
(`w1/PairS029StaticCanonicalPrefl.md`, "Status and errata (checked 2026-10-21)") records RFC 3986 as
STD 66, updated-but-not-obsoleted, RFC 8820's update confined to advisory §2, and *"No erratum names the
'two slash characters' sentences or the §3.2.1 userinfo text."*

### 2. Anchor observed correct in raw bytes

The receipt's `anchorObserved` says *"Section 3 Syntax Components, paragraph immediately after the
hier-part ABNF (plain text lines 874-878, p.16), unchanged"*. Verified line-by-line in the raw bytes:

```
$ gunzip -c .../S029-1.raw.gz | sed -n '861,878p'
861: 3.  Syntax Components
...
867:       URI         = scheme ":" hier-part [ "?" query ] [ "#" fragment ]
869:       hier-part   = "//" authority path-abempty
870:                   / path-absolute
871:                   / path-rootless
872:                   / path-empty
874:    The scheme and path components are required, though the path may be
875:    empty (no characters).  When authority is present, the path must
876:    either be empty or begin with a slash ("/") character.  When
877:    authority is not present, the path cannot begin with two slash
878:    characters ("//").  These restrictions result in five different ABNF
```

* §3 header at line 861; §3.1 Scheme starts at line 903 → the quote is inside §3.
* hier-part ABNF at 869-872 → the quoted paragraph is the *next* paragraph (874-878), exactly as the row
  anchor describes.
* Page furniture check: the footers are `[Page 15]` at line 842 and `[Page 16]` at line 898, so
  874-878 sits **on page 16** — the receipt's "p.16" is right, and `sed -n '860,880p' | grep Page`
  returns nothing, i.e. the quote is not page chrome.
* The quote is the *second* sentence of the paragraph (the "authority is present" clause at 875-876 is a
  neighbouring clause the receipt did **not** lean on); the quoted clause is exactly the absence-of-authority
  clause.
* Independent restatement in §3.3 Path (raw line 1210): *"If a URI does not contain an authority
  component, then the path cannot begin with two slash characters ("//")."* — the rule is normative in
  the body text, not just in the §3 summary.

### 3. The quote really grounds THIS row's teaches

Row teaches: *"Without an authority a path cannot begin with two slashes, so a `//`-prefixed reference
always carries an authority, possibly empty."* Two claims; both hold against the retained bytes:

* First clause — quoted verbatim: *"When authority is not present, the path cannot begin with two slash
  characters ("//")."* (raw 876-878).
* Inference "`//`-prefixed reference always carries an authority" — the only hier-part / relative-part
  branch producing a `//`-initial path is `"//" authority path-abempty` (raw 869-872; the sibling
  branches `path-absolute` = one leading slash, `path-rootless` = non-empty first segment,
  `path-empty` = empty). So a reference that starts with `//` necessarily takes the authority branch.
* "possibly empty" — the receipt grounds this in the authority ABNF, and it holds: `authority = [ userinfo
  "@" ] host [ ":" port ]` (raw 959) with `host = IP-literal / IPv4address / reg-name` (raw 1024) and
  `reg-name = *( unreserved / pct-encoded / sub-delims )` (raw 1135), i.e. zero-length permitted — §3.2.2
  Host states the empty registered name explicitly. The cited consumer uses exactly this: `///project/a.html`
  → `//` + empty authority + `/project/a.html`.

### 4. Receipt-schema and counter-rule compliance (measured by the lane's own checker)

* `rechecks/S029.json` keys are exactly `{id, verdict, fetchIndex, quote, anchorObserved, reason,
  correction}` (same key set as all 31 sibling receipts), `verdict` ∈ {HOLD,STALE,UNVERIFIABLE},
  `correction: null` as HOLD requires, `reason` and `anchorObserved` non-empty.
* `fetchIndex: 1` matches manifest index 1 / population fetch index 1 for `fetched/S029-1.raw.gz`.
* Amendment quote rules: quote = *"When authority is not present, the path cannot begin with two slash
  characters"* → 13 alphanumeric tokens (≥6 required), 13 whitespace words (≤25 required).
* Word-bounded match in the effective fetch text: `re.search(r'(?<!\w)'+re.escape(normalize(quote))+r'(?!\w)', normalize(text))`
  → **True** (mirrors `measure.py:273 quote_in_text`).
* Row specificity: the quote occurs in **only** `fetched/text/S029-1.txt` — `grep -l "two slash
  characters" fetched/text/*.txt` returns that single file — so it cannot be boilerplate borrowed from
  another row's document (the only multi-document group in `measure.py` is {S010,S028,S033}, RFC 9110).
* Retained text view is exactly the retained raw bytes normalized: regenerating with the current
  `source_text.py` (`text_of(load_gz('fetched/S029-1.raw.gz'), 'text/plain;charset=utf-8')`) gives
  122,068 chars vs the retained 122,069 — the only difference is one trailing `\n`
  (`ret.startswith(regen)` is True, extra tail is `'\n'`). Word-multiset comparison raw vs view:
  19,456 tokens on both sides, **zero** tokens missing or extra, so no content was dropped by the
  text-extraction step the receipt relies on.

### 5. Consumers still say what the row teaches (no missed staleness)

* `corpus/knowledge/static-canonical-preflight.md:82-83` — *"RFC 3986 section 3 says a path without an
  authority cannot begin with `//` (S029), so the reference carries an empty authority"* — consistent
  with the retained bytes; the seat review `w1/PairS029StaticCanonicalPrefl.md` judged all 7 statements
  of that pair HOLD / 0 STALE, and its Round-26 append-only block records the HOLD judgement.
* `corpus/lessons/round-22.md:184` — *"Section 3: 'When authority is not present, the path cannot begin
  with two slash characters ("//").'"* — verbatim, including the `("//")` the receipt's quote truncates.
  `round-22.md:159` uses S029 only as *"reject a `//` reference with empty authority (S028, S029)"*,
  which the retained bytes support. This consumer was flagged as not judged by the pair seat (its O4
  note) but its two S029 mentions are correct against the anchor.

## Findings

* **No falsifying finding.** The receipt's HOLD is grounded in bytes that are unchanged in the retained
  copy *and* unchanged on the live source, at the exact cited lines and page, and the quote carries the
  row's teaches rather than page chrome or a neighbouring clause.
* **Precision note (no verdict effect, no correction):** the receipt's `reason` says *"authority ABNF
  keeps all subcomponents optional so the authority may be empty"*. In the ABNF, `host` is a *required*
  subcomponent of `authority`; the empty authority arises because `host` may be the zero-length
  `reg-name` (`reg-name = *( unreserved / pct-encoded / sub-delims )`, §3.2.2 Host: the empty registered
  name is allowed). The conclusion ("the authority may be empty") is correct; only the phrasing
  "all subcomponents optional" is loose. This wording lives in the receipt's `reason`, not in the
  SOURCES row, the teaches cell or the anchor, and the counter does not judge it — no change warranted.
* **Anchor-precision note (already raised by the pair seat as O3):** the reference-level term for a
  `//`-initial reference is §4.2 "network-path reference" (raw 1439), and the rule is restated at §3.3
  (raw 1210); the row anchors §3. The §3 anchor is intact and the sentence quoted there is normative,
  so this is not STALE and no cell change is warranted.

## Residual risk / verification gaps

* The live GET proves the bytes are identical **now**; it cannot by itself prove that no *future*
  erratum will touch §3. The lane's own errata scan (w1/PairS029StaticCanonicalPrefl.md, same date)
  covers that gap and found no erratum naming the "two slash characters" sentences.
* RFC 3986's own header lists only what *it* updates; the reverse relation ("which RFC updates RFC
  3986") is not observable from the retained bytes. It was checked out-of-band in the lane's w1 seat
  (RFC 8820 advisory §2 only, not obsoleting) — I did not re-open the RFC Editor info/errata pages,
  since the lane bound allows only the plain GET of the row URL for network reads.
* Local tool behaviour cited by consumers (the `canonical_url_invalid` / `base_url_invalid` codes and the
  `urljoin` counter-example) is outside this row's scope and was not executed here.
* The lane's counter (`measure.py`) was **not** run by me; it is owned by another seat. My checks above
  reimplement its S029-relevant rules (`quote_in_text`, token/word counts, row specificity, key set)
  directly.

## Tooling

No tools were installed or updated (no pacman/uv/pip/cargo action). Read-only checks used `sha256sum`,
`gunzip`, `wc`, `sed -n`, `grep`, one `curl` plain GET of the row URL (bytes streamed, not saved), and
one-line `python3` stdlib calls. No file outside this report was written; no corpus, script, fleet repo,
sibling lane, Git index or jj state was touched.

```json
{"target":".ufo/waves/round-26/rechecks/S029.json + SOURCES.md row S029 (RFC 3986 §3)","verdict":"AGREE","severity":"none"}
```
