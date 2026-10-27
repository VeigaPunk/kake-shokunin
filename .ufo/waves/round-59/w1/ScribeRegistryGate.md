# ScribeRegistryGate

Claim C3 frontier step: the two registry rows (S425, S426), the round-59 `## Gate` block, and the assimilation decisions, drafted
independently of the entry scribes. Report only; no lane file other than this report and `.files/` was written.

## ROWS

| S425 | Google for Developers — Google Crawler (User Agent) Overview — https://developers.google.com/crawling/docs/crawlers-fetchers/overview-google-crawlers | docs | A | **How Google's operator says its own crawler identifies itself in a server log** — the three signals it names for the purpose (user-agent header, source IP address, reverse DNS hostname of that address), the three crawler categories and their robots.txt posture, and the fleet distribution it gives for why one crawler appears under several IP addresses | § Verify Google's crawlers and fetchers (Last updated 2026-06-12 UTC) | The operator states that its crawlers identify themselves in three ways — the HTTP user-agent header, the source IP address of the request, and the reverse DNS hostname of that address — and links its verification page from the same sentence | mined | 2026-10-27 | 180d | corpus/knowledge/crawler-identity-signals.md, corpus/knowledge/crawler-identity.md |
| S426 | Google for Developers — Verify Requests from Google Crawlers and Fetchers — https://developers.google.com/crawling/docs/crawlers-fetchers/verify-google-requests | docs | A | **The published method for confirming a logged request is Google's** — the reverse-then-forward DNS lookup on the source IP address with its accepted hostname suffixes, the crawler-category to reverse-DNS-mask and IP-range mapping, and the IP-range lists offered as the automatic alternative | § Use command line tools (Last updated 2026-03-20 UTC) | A logged request is confirmed as Google's by resolving its source IP address to a googlebot.com, google.com or googleusercontent.com name and resolving that name forward to the same address, with an IP-range match offered as the alternative for large scale lookups | mined | 2026-10-27 | 180d | corpus/knowledge/googlebot-verification.md |

Both cells of kind `docs`, tier A scoped to the stated scope, 11 cells, no pipe inside a cell, `|`-free command text.

## GATE

- S425 — https://developers.google.com/crawling/docs/crawlers-fetchers/overview-google-crawlers — accessed 2026-10-27 — § Verify Google's crawlers and fetchers (Last updated 2026-06-12 UTC) — quote: "Google's crawlers identify themselves in three ways:" (7 units; substring of one collapsed text node of the retained body, sha256 ff2b9fd7ed074536a460dca57816bffecceb0c186c42f1d551f34918551f5caa, 74477 bytes, HTTP 200), and "The source IP address of the request." (7 units; same retained body, sha256 ff2b9fd7ed074536a460dca57816bffecceb0c186c42f1d551f34918551f5caa, 74477 bytes, HTTP 200)
- S426 — https://developers.google.com/crawling/docs/crawlers-fetchers/verify-google-requests — accessed 2026-10-27 — § Use command line tools (Last updated 2026-03-20 UTC) — quote: "Run a reverse DNS lookup on the accessing IP address from your logs, using the" (15 units; substring of one collapsed text node of the retained body, sha256 8df9d4ade1d1f335060af05229c4d90b15d8136b9807cfab17a088f3292f0879, 69789 bytes, HTTP 200), and "Verify that it's the same as the original accessing IP address from your logs." (14 units; same retained body, sha256 8df9d4ade1d1f335060af05229c4d90b15d8136b9807cfab17a088f3292f0879, 69789 bytes, HTTP 200)

Quote evidence (all run, not inferred): `python3 -B span_tools.py check <S425|S426> <span>` returned
`units/chars/in_text_node=True/count_in_body=1/unique=True/within_ceilings=True` for all four spans; `sha256sum` of the retained
bodies equals the receipts and the counter's frozen `BODY_SHA256`; `stat -c %s` gives 74477 / 69789; receipts carry
httpStatus 200, effectiveUrl = request URL, fetchedAt 2026-10-27T01:21:22+00:00, userAgent `kake-shokunin-round59`. S425's Gate
span carries `IP address`, S426's carries `reverse DNS` (the counter's per-row subject).

Assimilation decisions (`ADMIT` theme `crawler identity verification signals`, from `merge/kake/`, read-only):

- staged **S398** re-grounded as **S425** — renumber by document (next unused id after S424), not arithmetic. Refused as staged,
  each point read against the retained body or the frozen census: `source` title is the page h1 not the `<title>` text before
  ` | `; the anchor clause `no revision printed on the page` is false (the page prints `Last updated 2026-06-12 UTC`, 2
  occurrences); the recheck cell embeds an escaped pipe and the row splits to 14 cells under the frozen census awk (NF must be
  13), so it is malformed as staged; `opened` 2026-10-24 is not this round's access date; `used-by` names the staged file that C1
  requires absent.
- staged entry sentences refused, with counts on the collapsed S425 body: the `cannot forge` gloss (`forge` 0); the Baidu
  reverse-DNS sentence (`baidu` 0) and the Yahoo! JAPAN sentence (`Yahoo` 0) — cross-document attribution; the `All three
  operators…` lane meta-prose; the unconditional `blocks * … has not excluded that one` (the page binds the AdsBot exception to
  `with the ad publisher's permission`, 1 occurrence); the AdsBot sentence as one quote (the collapsed nodes are
  `ignores the global robots.txt user agent (`, `*`, `) with the ad publisher's permission.`); the `similar to common crawlers…`
  sentence as one quote (a single 31-unit node, above the 25-unit ceiling). Substance of the last two is kept, quotable only in
  pieces. Kept as-is: the three-signal sentence and the list items beside it.
- **S426** lane-found from the retained S425 body: the `verify-google-requests` href occurs 2 times (page side-navigation + the
  closing sentence of the anchored h2), and that sentence is split by the link, so its nodes are `Learn how to use these details
  to `, `verify Google's crawlers and fetchers`, `.` — not quotable as one span.

## Local validation (run by this seat, scratch only)

- Draft-row census on a scratch copy `sources-draft.md` (lane registry + the two rows) with the frozen CORPUS.md awk formulas:
  rows 164; malformed rows (NF!=13) 0; duplicate ids none; tier/kind/status enum violations none; status histogram
  `mined=134 queued=8 rejected=22`; tier histogram `A=141 B=6 C=17`.
- Row/Gate pre-check harness importing the frozen counter module read-only and re-using its own `parse_registry`, `units`,
  `article_headings`, `in_content`, `text_segments`, `row_url`, `used_by`, `CURLY`, `TOPIC`, `USED_BY`, `BODY_SHA256`: 11 cells,
  status/opened/recheck/url/kind/tier, scope+teaches length, base absence, `used-by` sets, sha256, title vs page `<title>`, anchor
  regex + heading membership + printed revision, and every Gate-line clause (curly quotes, subject, sha/bytes, unit statements,
  anchor cell carried verbatim, 6..25 units, ≤160 chars, in one collapsed text node, page-unique) — **all pass except the S425
  title clause below**.
- The counter itself was **not** run against the lane: it measures a committed revision and the rows/entries are not committed;
  no such run is claimed.

## Findings

1. **Counter version-1 conflict (reported verbatim for the canonical judge).** C5 requires the row's `source`-cell title to be
   6+ units *and* to equal the page's `<title>` text before ` | `. For S425 that text is `Google Crawler (User Agent) Overview`,
   **5 units**. No cell satisfies both: the faithful value fails the unit floor; the value that passes the floor is not the page
   title. The row carries the page's exact title, and C5 will therefore fail at that one clause unless the counter is attacked or
   revised by the wave-1 seats. S426's title `Verify Requests from Google Crawlers and Fetchers` is 7 units and meets both.
2. `used-by` for S425/S426 names `corpus/knowledge/crawler-identity-signals.md` and `corpus/knowledge/googlebot-verification.md`;
   neither exists at the base revision — they are entry-scribe deliverables. `corpus/lessons/round-59.md` does not exist either;
   the Gate block below is the fragment to splice.
3. The staged `amendments/corpus/knowledge/crawler-identity.md` re-asserts the stale sentence verbatim and cites S300, not this
   round's row; not adopted here (its screen belongs to the seat that owns the C9 correction). [INFERENCE] on ownership only.
4. No tool install or upgrade was needed or performed.

## ASSIMILATION

Id lists (`.ufo/waves/round-59/assimilation/`, `wc -l`): `reg-ids` 162, `staged-ids` 129, `collisions` 8. Collisions:
S312 S329 S367 S372 S373 S374 S390 S409 (the round-57/58 set; neither new id is in either list, S398 is staged-only). Renumber
map by document: staged S398 → S425; S426 has no staged id (lane-found). Quarantine: 12 rows (S142 S143 S148 S154 S156 S161 S178
S184 S193 S194 S195 S206) unchanged and **held** — the round-58 L0 question is unanswered, so nothing from the slice is appended;
this is a routed-around state, not an answered one.

## REGISTRY CHANGES

- Rows: 162 → 164. S425, S426 appended after S424 in that order, both `mined`, opened 2026-10-27, recheck `180d`, `used-by` as in
  the rows above. No existing row's `status`, `recheck` or `used-by` changed (pure addition) — no old→new line other than the two
  new ids.
- Base counts: `grep -cE '^ {0,3}\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' corpus/SOURCES.md` = 162; pre-append mirror 162 rows,
  150968 bytes, sha256 ecb5cedf…efe6ae (`mirror-pin.json`); `S425`/`S426` absent from the base (grep count 0).

## Artifacts

- `.ufo/waves/round-59/w1/ScribeRegistryGate.files/gate.md` — the `## Gate`, `## Registry changes (old → new)` and
  `## Assimilation` blocks for `corpus/lessons/round-59.md` (Gate lines byte-identical to the validated draft).
- `.ufo/waves/round-59/w1/ScribeRegistryGate.files/rows.md` — the two row lines exactly as validated, for splicing after S424.
- `.ufo/waves/round-59/w1/ScribeRegistryGate.files/check_draft.py` + `draft-check.txt` — the read-only pre-check and its output
  (`rows: 164`, `malformed: 0`, no duplicate ids, no enum violations, `PROBLEMS: 1` = the S425 title-floor conflict only).
- Scratch `/fast/scratch/hyaku/kake-r59/ScribeRegistryGate/` deleted after the receipts were copied; the lane registry, lesson
  file, entries and registry were only read.

VERDICT: both C3 rows and the Gate block drafted and locally validated against the counter's own row/Gate clauses; one reported counter defect (S425 title is 5 units against a 6-unit floor) makes that clause unsatisfiable for a faithful row — flag to the canonical judge, no after-state scored.
