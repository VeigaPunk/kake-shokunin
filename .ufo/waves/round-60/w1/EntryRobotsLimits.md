# EntryRobotsLimits

Seat: C3 assimilated entry, round-60 w1 (build wave). Lane `kake-shokunin`, base revision
`97cdc122379711c2b02a8970752c8782da3ac81d`, access date 2026-10-27 (UTC). Read first:
`.ufo/waves/round-60/contract.md` and `contract.json`.
Deliverable: the staged package entry
`/home/vgpnk/Projects/shokuknow/merge/kake/knowledge/corpus/knowledge/google-robots-txt-limits.md`
(staged row S415) re-grounded as `corpus/knowledge/robots-txt-limits.md` on row **S429**, from the
retained body `.ufo/waves/round-60/sources/S429.html`.
Paths written, and nothing else (no lane Git/jj mutation, no registry or corpus edit, no pacman, no
install; stdlib `python3` only): `.ufo/waves/round-60/w1/EntryRobotsLimits.files/robots-txt-limits.md`
(the entry, 111 lines), `…/EntryRobotsLimits.files/span_check.py` (checker, read-only),
`…/EntryRobotsLimits.files/span-check.txt` (its output), and this report. Scratch
`/fast/scratch/hyaku/kake-r60/EntryRobotsLimits/` (one helper, no git fixture) was deleted at the end;
nothing cited lives only there.

## ENTRY

First three lines (provenance trio):

```
source: S429 — https://developers.google.com/search/docs/crawling-indexing/robots/intro — § Understand the limitations of a robots.txt file (Last updated 2025-12-10 UTC) — fetched 2026-10-27
verified-at: 2026-10-27
recheck: 180d — `curl -fsSL --compressed 'https://developers.google.com/search/docs/crawling-indexing/robots/intro' | grep -F -c 'Different crawlers interpret syntax differently.'` -> 1 (grep against the retained body 1, 2026-10-27)
```

Page facts re-checked against `sources/S429.html` (this seat ran no live fetch):

- `<title>` before ` | `: `Robots.txt Introduction and Guide`; the page `<h1>` reads
  `Introduction to robots.txt` (page chrome, so the entry does not equate it with the title).
- Article-block `<h2>`s: `What is a robots.txt file used for?`,
  `Understand the limitations of a robots.txt file`, `Create or update a robots.txt file` — the anchor
  in `source:` is the second and is an `<h2>` of the block.
- `Last updated 2025-12-10 UTC` sits **inside** `<devsite-content-footer …>`:
  `<p>Last updated 2025-12-10 UTC.</p> </devsite-content-footer>` (R59-D3 footer read).
- Body sha256 `423d99c5bf7fec4298d00cdd46f01a495c9ad463fa704f7850a100e43e2a9edd`, 178797 bytes; both
  equal `sources/receipts.json` for S429 (same URL as the row, `httpStatus` 200,
  `fetchedAt` 2026-10-27T04:03:38+00:00, userAgent `kake-shokunin-round60`).
- Recheck predicate: `grep -F -c 'Different crawlers interpret syntax differently.' S429.html` -> `1`
  (run 2026-10-27 on the retained body).

What the page adds, and the entry claims only this (four headline points plus two supporting
statements): (1) the instructions cannot enforce crawler behaviour — obedience is the crawler's
choice; (2) crawlers interpret the syntax differently and some
may not understand every instruction; (3) a disallowed URL can still be indexed if other sites link to
it (address, and possibly anchor text, can still surface, without a description); (4) the warning not to
use the file to hide a page, with its remedy list (password protection, `noindex` meta tag or response
header, removal); (5) rules may not be supported by all search engines; (6) blocking does not stop other
pages or users linking to a media file. The RFC mechanics are not re-derived: the entry names
`corpus/knowledge/robots-txt-rules.md` and `corpus/knowledge/crawler-identity.md` for them.

## REFUSED STAGED SENTENCES

Reasons are page-grounded on `sources/S429.html`; counts are `grep` on that body.

| # | staged item (as staged) | disposition / reason |
|---|---|---|
| 1 | `# The file states a preference, and each crawler reads it its own way` | rewritten — `each crawler` overstates; the page says each crawler **might** interpret the rules differently |
| 2 | `source: S415 — … — § How robots.txt works → … — fetched 2026-10-24` | refused — id and fetch superseded (S429, 2026-10-27); `How robots.txt works` is no heading here (`grep -F -c` -> 0) |
| 3 | `verified-at: 2026-10-24` | refused — superseded by the round-60 access date |
| 4 | `…the operator's own documentation of its own crawler, in the same tradition as Baidu's robots Q&A and Yahoo! JAPAN's refusal-file page`; `the western first-party statement …` | refused — lane meta-prose plus cross-document attribution; `baidu` -> 0, `yahoo` -> 0 in the body (the S415 scope cell is the row seat's to fix) |
| 5 | `The lane holds the refusal-file rules from three directions now` | refused — lane meta-prose; the page says nothing about other entries |
| 6 | `The definition is the expected one — a robots.txt file tells search engine crawlers which URLs they may access on a site.` | refused as written — `expected` is the lane's evaluation, `may access` is not the page's wording (`can access`); carried only as the page's verbatim span |
| 7 | `The two limits are the useful part, and neither is usually stated this plainly.` | refused — usefulness and frequency are the lane's evaluation; the page claims neither |
| 8 | `The instructions in the file cannot enforce crawler behaviour: … this operator's crawlers obey … real protection … other blocking methods` | partly carried, re-quoted — refused for `this operator's crawlers` (page names Googlebot), `real protection` (page: keep information secure), and `behaviour` (page prints `behavior`) |
| 9 | `And different crawlers interpret the syntax differently — … each does it its own way, and some do not understand every instruction` | carried, re-quoted — all three claims are on the page; `each does it its own way` replaced by `might interpret the rules differently` |
| 10 | `That last clause is the one that belongs beside this lane's eastern material.` | refused — lane meta-prose |
| 11 | `Baidu documents the same three fields and their prefix semantics…; Yahoo! JAPAN tells a server administrator to identify a crawler by the address its DNS points at…` | refused — cross-document; body holds no Baidu/Yahoo (0/0), no field name (`user-agent`, case-insensitive -> 0), no `prefix` (0), no `DNS` (0) |
| 12 | `Taken together the three say one thing: … stated per crawler, and it is never a security control.` | refused — synthesis across three documents; `per crawler` is not here, and `never a security control` is the RFC 9309 reading already held in `robots-txt-rules.md` (not duplicated) |
| 13 | `… relying on behaviour that only one operator has promised.` | refused — `only one operator` -> 0; the page gives no count of operators and no promise |
| 14 | staged filename `google-robots-txt-limits.md` | refused — contract C1: the staged name must not exist |
| 15 | staged `recheck:` ending `-> 1 (ran 2026-10-24)` | refused as written — this seat ran no `curl`; the new line states a retained-body grep on 2026-10-27 |

Kept because the page holds them, as verbatim spans rather than staged paraphrase: the definition
sentence, the two-limit structure of the limits section, the cannot-enforce sentence, the
syntax-difference paragraph, the indexed-anyway paragraph, and the hide-warning sentences.

## SPAN CHECK

`python3 -B span_check.py` reuses the round-59 counter's own `units()` / `text_segments()` /
`in_content()` code (`.ufo/waves/round-59/c59_quote_truth.py`, S429 body registered), plus the round-60
band 6..25 units and <=160 characters, and uniqueness across the three retained bodies S427/S428/S429.
Output as produced (`span-check.txt`):

```
provenance trio in first 8 lines: {'source:': 0, 'verified-at:': 1, 'recheck:': 2}
source names row id and URL: True
id cited below the header: True
L32   16u  94c unique=True  node=True  band=True  OK  A robots.txt file tells search engine crawlers which URLs the crawler 
L39   18u  99c unique=True  node=True  band=True  OK  Before you create or edit a robots.txt file, you should know the limit
L43   10u  60c unique=True  node=True  band=True  OK  robots.txt rules may not be supported by all search engines.
L47   12u  81c unique=True  node=True  band=True  OK  The instructions in robots.txt files cannot enforce crawler behavior t
L51    8u  35c unique=True  node=True  band=True  OK  it's up to the crawler to obey them
L56   18u 119c unique=True  node=True  band=True  OK  While Googlebot and other respectable web crawlers obey the instructio
L60    6u  48c unique=True  node=True  band=True  OK  password-protecting private files on your server
L64   18u 123c unique=True  node=True  band=True  OK  Although respectable web crawlers follow the rules in a robots.txt fil
L68    6u  46c unique=True  node=True  band=True  OK  some might not understand certain instructions
L74   16u  90c unique=True  node=True  band=True  OK  A page that's disallowed in robots.txt can still be indexed if linked 
L78   19u  91c unique=True  node=True  band=True  OK  we might still find and index a disallowed URL if it is linked from ot
L83   12u  65c unique=True  node=True  band=True  OK  its URL can still appear in search results, but the search result
L87   16u  89c unique=True  node=True  band=True  OK  This won't prevent other pages or users from linking to your image, vi
L94   13u  58c unique=True  node=True  band=True  OK  it is not a mechanism for keeping a web page out of Google
L98   10u  51c unique=True  node=True  band=True  OK  If you want to hide the page completely from Search
distinct page-unique spans: 15 (need >= 3)
one carries 'cannot enforce': True
curly quotes present: False
ALL SPANS OK
```

15 distinct page-unique spans (floor 3), one carrying `cannot enforce`; every double-quoted span is in the
6..25 unit band, is a substring of one whitespace-collapsed article-block text node, occurs once in S429
and zero times in S427/S428. Nothing is quoted from another page — cross-references are names in
backticks only.

## HELD BEFORE

- **RFC 9309's authorization framing** — `corpus/knowledge/robots-txt-rules.md:9` (crawler-access
  convention, not authorization; a disallow rule secures nothing) and its § Limits, from S011 §§1, 3.
  Hence not restated here, only named.
- **File/parse/match mechanics and Google's parser note** — same entry: location and scope, UTF-8 /
  500 KiB / line and group parsing, `allow`/`disallow` matching, percent-encoding, implicit
  `/robots.txt` allow, S095/S096 readings, plus the lane audit contract.
- **Identity signal** — `corpus/knowledge/crawler-identity.md:27,55` (both crawler types obey the same
  product token).
- **Index-outcome neighbour** — `corpus/knowledge/js-rendering-queue.md:41` (a `noindex` on a
  robots-disallowed URL is never seen; disallowing is not de-indexing). It reaches the rendering side of
  point 3 but does not carry the linked-from-elsewhere case or the page's wording.
- **One operator's own refusal rules** — `corpus/knowledge/yahoo-japan-robots-txt-refusal-rules.md`
  (S372), `yahoo-japan-robots-pattern-syntax.md` (S373), `yahoo-japan-robots-txt-basics.md` (S418).

## UNRUN / LIMITS

- **No counter run.** `c60_quote_truth.py` does not exist at my run time (built this wave, frozen by the
  L1 before any after-state); the entry was checked with the round-59 extraction code plus the round-60
  quote band. No after-state score is claimed. [INFERENCE] the staged text would have failed C5 on the
  `cannot enforce` subject and on the cross-document attributions; pre-empted by construction, unobserved.
- **No live fetch.** The recheck predicate was a `grep` on the retained body; sources were fetched
  2026-10-27T04:03Z per `receipts.json`, not by this seat.
- **Placement is the integrator's.** Copying the entry to `corpus/knowledge/robots-txt-limits.md` and
  adding row S429 plus the lesson Gate line are outside this seat's write scope.

VERDICT: The S429 entry is written at `.ufo/waves/round-60/w1/EntryRobotsLimits.files/robots-txt-limits.md` with provenance trio, page title/heading/footer pinned to the retained body and 15 page-unique spans inside the 6..25 unit band (one carrying `cannot enforce`); 13 staged items refused with page-grounded reasons (one rewritten, one partly), 2 carried only as verbatim page spans.
