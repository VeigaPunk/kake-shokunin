# EntryUserTriggered

## ENTRY:
`/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-60/w1/EntryUserTriggered.files/google-user-triggered-fetchers.md`
(staged under `.files/`; `corpus/knowledge/google-user-triggered-fetchers.md` does not exist in the lane and was not written by this seat).
95 lines. Header trio as prescribed:

```
source: S428 — Google Crawling Infrastructure — Google User-Triggered Fetchers — https://developers.google.com/crawling/docs/crawlers-fetchers/google-user-triggered-fetchers — § List of Google user-triggered fetchers (Last updated 2026-08-19 UTC) — article `<h1>`; no `<h2>` precedes the robots sentence
verified-at: 2026-10-27 (retained body sha256 0f296b8636d5fb9d44c66fc1453a5610fdf738c80c9baef44c233e0a1872d3b2, 76197 bytes)
recheck: 180d — `curl -fsSL --compressed '<url>' | grep -F -c 'these fetchers generally ignore robots.txt rules'` -> 1 (grep against the retained body 1, 2026-10-27)
```

`source:` deviates from the seat's `§ <h2 that holds the robots sentence>` because no `<h2>` holds it — see FINDINGS 1; after the L1 ruling recorded there it names the article `<h1>` in the ruled shape `§ <heading> (Last updated … UTC)`.
The retained body's sha256 was recomputed and equals `receipts.json` (`0f296b86…d3b2`, 76 197 bytes, HTTP 200,
fetchedAt 2026-10-27T04:03:37+00:00, UA `kake-shokunin-round60`).

Body sections: what the page calls a user-triggered fetcher · the robots.txt posture in the page's words ·
how a publisher can still identify these fetchers · the wording divergence against S426, dated · what this entry
does not establish. Eight page-unique spans, one carrying `generally ignore`.

## SPAN CHECK:
Checked with `EntryUserTriggered.files/check_spans.py` (replicates the C3 counter's `body()` whitespace collapse,
`text_segments()` article-block text nodes and `in_content()` substring test verbatim) and
`EntryUserTriggered.files/validate_entry.py` (extracts every ASCII double-quoted span of the entry and applies the
6..25 unit / <= 160 char / one-text-node / page-unique rules):

```
$ python3 -B validate_entry.py <sources> <entry.md>
PASS 15u 102c node=True  count=1 others={'S427': 0, 'S429': 0} :: User-triggered fetchers are initiated by users to perform a fetching function within a Google product.
PASS 13u  64c node=True  count=1 others={'S427': 0, 'S429': 0} :: acts on a user's request, or a site hosted on Google Cloud (GCP)
PASS 14u  92c node=True  count=1 others={'S427': 0, 'S429': 0} :: Because the fetch was requested by a user, these fetchers generally ignore robots.txt rules.
PASS 11u  66c node=True  count=1 others={'S427': 0, 'S429': 0} :: The IP ranges the user-triggered fetchers use are published in the
PASS 17u 112c node=True  count=1 others={'S427': 0, 'S429': 0} :: The user-triggered fetchers' reverse DNS mask, depending on whether the fetcher is Google or user owned, matches
PASS 24u 144c node=True  count=1 others={'S427': 0, 'S429': 0} :: Google-Agent is used by agents hosted on Google infrastructure to navigate the web and perform actions upon user request. It uses IP ranges from
PASS  6u  48c node=True  count=1 others={'S427': 0, 'S429': 0} :: these fetchers generally ignore robots.txt rules
PASS 10u  57c node=True  count=1 others={'S427': 0, 'S429': 0} :: The list is not exhaustive, it only covers the requestors
spans=8 distinct=8 failed=0 distinct_passing=8
carries_subject= True
exit=0
```

Structure assertions on the same body (separate inline probe): `n_h2h3=9` = exactly the nine per-fetcher names
(`Chrome Web Store`, `Feedfetcher`, `Gemini Notebook`, `Google-Agent`, `Google Messages`, `Google Pinpoint`,
`Google Publisher Center`, `Google Read Aloud`, `Google Site Verifier`); `h1(25822) < robots(26428) < first_h2(27935)`
→ True; `Last updated 2026-08-19 UTC` occurs after `<devsite-content-footer` (46928) → True; `<title>` text before
` | ` = `Google User-Triggered Fetchers`.

Cross-body note: the S426 wording exists only in the round-59 body (`S426.html`: `… these fetchers ignore robots.txt
rules.`), the S428 wording only in the round-60 body (`… these fetchers generally ignore robots.txt rules.`) — each
page carries the phrase once, which is why the S426 words are carried in backticks in the entry (a double-quoted S426
span would fail a per-row C5 check against S428).

## READINGS:
Sentences in the entry that are the lane's reading, not a span:

- "none of the nine per-fetcher `<h2>` sections repeats or qualifies it" — read from all nine sections; each prints a
  user-agent string and an associated product, no robots.txt clause. No span (the absence is the claim).
- "The page then says the fetchers' general technical properties are … for Google's crawlers" — the sentence exists
  (`The general technical properties of Google's crawlers also apply to the user-triggered fetchers.`) but is split
  across link elements; the candidate span `The general technical properties of Google's crawlers also apply` returns
  `node=False, unique=False`, so it is carried as a reading.
- "Its caution box states that the user-agent string can be spoofed" — the text sits in `<aside class="caution">`,
  which `text_segments()` blanks (version-2 rule); `The user agent string can be spoofed.` returns `node=False`.
  Observed in the raw HTML, unquotable under the rule, so unquoted.
- "both identifiers the page supplies are address-based … it does not make the user-agent string an identifier" —
  the lane's reading of the page's structure.
- "five months apart" — arithmetic on the two printed revisions (2026-03-20 → 2026-08-19).
- The divergence section states both wordings with both revision dates and declines to decide which governs; no
  judgement is recorded.

## Gates and checks actually run
- Read first: `.ufo/waves/round-60/contract.md`, `sources/receipts.json`, the S428 body's article block; base revision
  `97cdc12…` not needed (no git reads were necessary).
- Ran: `check_spans.py --list`, `check_spans.py <spans…>` (three batches), `validate_entry.py` (final: 8/8 PASS,
  exit 0), the inline heading/footer/title/wording probe, `sha256sum` on the retained body.
- **Not run:** `c60_quote_truth.py` (its owner builds it this wave) — this seat scores nothing; no live network fetch
  (the `recheck:` command is a future command, its `-> 1` value is against the retained body, as the line says).

## Touched surfaces
- new only, inside the seat's `.files/`: `EntryUserTriggered.files/google-user-triggered-fetchers.md`,
  `EntryUserTriggered.files/check_spans.py`, `EntryUserTriggered.files/validate_entry.py`.
- new: this report. No other lane path written; `corpus/knowledge/**`, rows, lesson, counter untouched; no
  `git`/`jj` mutation of any kind; no pacman; no tool installed.

## Findings
1. **Anchor-heading tension (row S428) — ruled, option (b).** The robots sentence has no `<h2>` above it; the
   article's `<h2>`/`<h3>` set is the nine per-fetcher names. A `§ <h2>` anchor cell would therefore name one fetcher and
   understate the row's scope — the same defect class as the R59-D4 `scope` overstatement this claim corrects. Messaged
   `KakeR60` (options: `§ Chrome Web Store`, or let the anchor rule accept the article `<h1>`); the L1 ruled option (b):
   the anchor rule becomes "nearest article-block `<h1>`/`<h2>`/`<h3>` preceding the Gate quote", S428 anchoring on the
   `<h1>` "List of Google user-triggered fetchers". The entry's `source:` line carries that anchor in the ruled shape.
   [RULING: L1 `KakeR60`, 2026-10-27 — not this seat's decision; the counter `c60_quote_truth.py` must implement it.]
2. **Three load-bearing sentences are unquotable on this page** (general technical properties: split by links; the
   spoof caution: inside an `<aside>`; the exhaustiveness clause is quotable, the other two are not). A w2 critic can
   test whether an entry asserts them without a span; this entry labels them as readings.
3. The subject span `generally ignore` is available twice (6-unit mid-sentence fragment and the 14-unit full
   sentence); a row Gate quote needing 6..25 units should use the 14-unit sentence.
4. The divergence is two-fold, not one: `ignore` → `generally ignore`, and `acts on the request of a user` →
   `acts on a user's request`; both dated 2026-03-20 vs 2026-08-19.

## Out of scope (other seats)
Rows S427–S429 in the registry, the `[r60-correction 2026-10-27]` run in `googlebot-verification.md` (C3 C9), the
`robots-txt-limits.md` entry (S429), `c60_quote_truth.py` and its derivation, the append validation, and every
after-state score — none attempted here; no score is claimed.

## Artifact paths
- entry: `kake-shokunin/.ufo/waves/round-60/w1/EntryUserTriggered.files/google-user-triggered-fetchers.md`
- checkers: `…/EntryUserTriggered.files/check_spans.py`, `…/EntryUserTriggered.files/validate_entry.py`
- report: `kake-shokunin/.ufo/waves/round-60/w1/EntryUserTriggered.md`
- scratch `/fast/scratch/hyaku/kake-r60/EntryUserTriggered` removed before yield (nothing cited from it).

VERDICT: S428 entry staged with 8 page-unique spans (subject `generally ignore` carried), all quote rules passed by a local replication of the counter's text-node code; the seat's `<h2>` anchor premise is false on this page and is reported as a C3/C5 defect candidate, not papered over.
