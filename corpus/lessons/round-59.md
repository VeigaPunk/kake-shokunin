# Round 59 — lessons (kake)

Round opened 2026-10-26 (-03:00); sources accessed 2026-10-27 (UTC). Base `fd6303ce5c14b3f892dec586297a942ab6e4193b`; contract
`.ufo/waves/round-59/contract.md` (version 1 frozen at `45a92b64`, version 2 frozen after wave 1, before any claim was measured).
One v2 wave of 66 seats (`.ufo/waves/round-59/w1/`).

## Gate

Rows opened this round. Unit rule (the C3 counter's `units()`): one unit per CJK character, one per non-CJK whitespace token;
every quote below is 6 to 25 units and at most 160 characters, a substring of one whitespace-collapsed text node of the retained
body's article block (the container of class `devsite-article-body` .. `<devsite-content-footer`), and page-unique across the two bodies. Both
pages were opened 2026-10-27 UTC by `.ufo/waves/round-59/fetch_sources.py` (GET, HTTP 200, effective URL equal to the request
URL, userAgent `kake-shokunin-round59`) and retained under `.ufo/waves/round-59/sources/` with the sha256 receipts in
`sources/receipts.json`; the digests were re-run this wave (`sha256sum`, both equal to the receipt and to the counter's frozen
`BODY_SHA256`).

- S425 — https://developers.google.com/crawling/docs/crawlers-fetchers/overview-google-crawlers — accessed 2026-10-27 — § Verify Google's crawlers and fetchers (Last updated 2026-06-12 UTC) — quote: "Google's crawlers identify themselves in three ways:" (7 units; substring of one collapsed text node of the retained body, sha256 ff2b9fd7ed074536a460dca57816bffecceb0c186c42f1d551f34918551f5caa, 74477 bytes, HTTP 200), and "The source IP address of the request." (7 units; same retained body, sha256 ff2b9fd7ed074536a460dca57816bffecceb0c186c42f1d551f34918551f5caa, 74477 bytes, HTTP 200)
- S426 — https://developers.google.com/crawling/docs/crawlers-fetchers/verify-google-requests — accessed 2026-10-27 — § Use command line tools (Last updated 2026-03-20 UTC) — quote: "Run a reverse DNS lookup on the accessing IP address from your logs, using the" (15 units; substring of one collapsed text node of the retained body, sha256 8df9d4ade1d1f335060af05229c4d90b15d8136b9807cfab17a088f3292f0879, 69789 bytes, HTTP 200), and "Verify that it's the same as the original accessing IP address from your logs." (14 units; same retained body, sha256 8df9d4ade1d1f335060af05229c4d90b15d8136b9807cfab17a088f3292f0879, 69789 bytes, HTTP 200)

Page-printed revision dates: S425 prints `Last updated 2026-06-12 UTC`, S426 prints `Last updated 2026-03-20 UTC`. Both anchors
name an `<h2>` of the article block (`Verify Google's crawlers and fetchers`; `Use command line tools`), not the h1, and each is
the section that holds the quote: the three self-identification signals and the S426 link for S425, the reverse-then-forward DNS
steps for S426.

ADMIT theme `crawler identity verification signals` (staged package `merge/kake/`, shokuknow, read-only). Staged row **S398** is
re-grounded as **S425** — renumbered by document, not arithmetically (the registry's next unused id after S424) — and the staged
entry name is not carried. **S426** is lane-found from S425 itself.

Staged row S398, refused as staged, each point read against the retained body or the frozen census:

- `source` cell title is the page h1 `Overview of Google crawlers and fetchers (user agents)`; the page's `<title>` text before
  ` | ` is `Google Crawler (User Agent) Overview`. The row carries the `<title>` text.
- anchor clause `no revision printed on the page` is false: the page prints `Last updated 2026-06-12 UTC` (2 occurrences in the
  collapsed body); the new anchor carries it. The old anchor also lacks the `(Last updated YYYY-MM-DD UTC)` form.
- the recheck cell embeds a live command with an escaped pipe (`\|`); the row splits to 14 cells under the frozen census awk
  (11 cells means NF=13), i.e. the staged row is malformed as staged. The row carries `180d`.
- `opened` 2026-10-24 is not this round's access date; the fetch receipt is 2026-10-27T01:21:22Z.
- `used-by` names `corpus/knowledge/crawler-identity-three-signals.md`, a path that must not exist at the measured revision.

Staged entry `crawler-identity-three-signals.md`, sentences refused and why (counts are `str.count` on the whitespace-collapsed
retained S425 body):

- `the address and its reverse hostname are the two that a caller cannot forge` — `forge` 0, `cannot forge` 0: the page names
  three signals and never says which a caller can forge; a page-unsupported gloss, refused.
- `Baidu's own page checks the reverse hostname against *.baidu.com or *.baidu.jp` — `baidu` 0: cross-document attribution (that
  fact is S423's); refused, the row must not carry another page's statement.
- `Yahoo! JAPAN's crawl documentation tells the server administrator to restrict access by the address the crawler's DNS points
  at` — `Yahoo` 0: cross-document attribution; refused for the same reason.
- `All three operators the lane now holds say this in their own words` — lane meta-prose, not a page statement, and it depends on
  two documents the row does not quote; refused from the entry body.
- `A site that blocks * and believes it has excluded every crawler has not excluded that one` — the page binds the AdsBot
  exception to `with the ad publisher's permission` (1 occurrence); the unconditional sentence is refused, the bounded form kept.
- `the page's example is that AdsBot ignores the global robots.txt user agent (*) with the ad publisher's permission` — substance
  kept, but unquotable as one span: the collapsed nodes are `ignores the global robots.txt user agent (`, `*`, and `) with the ad
  publisher's permission.` An entry quoting it must split or paraphrase.
- `Special-case crawlers are similar to common crawlers, however are used by specific products where there's an agreement between
  the crawled site and the Google product about the crawl process` — present, but as one 31-unit node, above the 25-unit ceiling;
  it must be cut to a 25-unit-or-shorter subspan before it is quoted.
- the staged `verified-at:` curl (ran 2026-10-24) and the staged `ground:` line — superseded by the round-59 receipt; not carried.

Kept from the staged package: the three-signal sentence itself and the numbered list items beside it, which are separate text
nodes (`The source IP address of the request.`, `The reverse DNS hostname of the source IP.`).

S426 lane-found, provenance in the retained S425 body: `/crawling/docs/crawlers-fetchers/verify-google-requests` appears as an href 2
times (once in the page side-navigation, once in the closing sentence of the anchored h2 section); the page prints that sentence
with the link inside it, so its collapsed nodes are `Learn how to use these details to `, `verify Google's crawlers and fetchers`,
`.`. The sentence is not quotable as one span.

Reported conflict (counter version 1), resolved before any claim was measured: counter version 2 lowers the title floor to 3 units for English titles (`contract.md` § Counter versions). Original report: C5 requires the
row's `source`-cell title to be 6+ units and to equal the page's `<title>` text before ` | `. For S425 that text is `Google Crawler (User Agent) Overview`, 5 units. No cell can satisfy both clauses: the faithful value fails the unit floor, and the value
that passes the floor is not the page title. The row carries the page's exact title. S426's title (`Verify Requests from Google
Crawlers and Fetchers`, 7 units) meets both.

Decision lines (one per refused staged candidate of the theme, each re-opened by a wave-1 seat before it was logged):

- REJECT staged `amendments/corpus/knowledge/crawler-identity.md` (round2, staged S300 on the same URL as lane S263) — a strict subset of the
  lane's S263 entry, it repeats the stale line-31 sentence verbatim and its one quote spans two text nodes; live page re-opened HTTP 200,
  unchanged in substance (`w1/ScoutRejectAmendment.md`). Flip: admit if it carries a sentence the lane does not hold.
- REJECT staged `yahoo-crawler-ua-carrier-survey.md` (staged S394) as staged — it cites an own-work count file outside the lane and the
  registry, quotes no operator page, its DNS thesis belongs to the unheld page `https://info-search.yahoo.co.jp/archives/002855.php`, its
  recheck greps a string the sweep itself writes, and its ads-page figures no longer reproduce (`w1/ScoutRejectYahooUA.md`). Flip: adopt
  002855 as a lane row and re-cut the entry on its sentences under a CJK-aware quote-unit rule.

Non-author discernment spot-check: **pending** at lane filing; no dispatched seat is a non-author. Closure must re-open at least one
admitted row (S425 or S426) and one reject (above) and record `agree`/`disagree` with reasons, per `LEARNING.md`.

## Registry changes (old → new)

- Rows: 162 → 164. S425 and S426 are appended after S424 in that order, both `mined`, opened 2026-10-27, recheck `180d`,
  `used-by` = S425: `corpus/knowledge/crawler-identity-signals.md, corpus/knowledge/crawler-identity.md`; S426:
  `corpus/knowledge/googlebot-verification.md`. No existing row's `status`, `recheck` or `used-by` changed (a pure addition).
- Counts: `grep -cE '^ {0,3}\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' corpus/SOURCES.md` = 162 at the base revision and in the
  pre-append mirror (`assimilation/mirror-pin.json`: 162 rows, 150968 bytes, sha256 ecb5cedfcf2addc043ce6fa1b6def453088a996f95c0f60583dfdf0f30efe6ae);
  both ids are absent from the base (`grep -cE '^ *\| *S42[56] *\|'` = 0).
- Draft-row census (a scratch copy of the registry plus the two draft rows, frozen CORPUS.md awk formulas): rows 164, malformed
  (NF!=13) 0, duplicate ids none, tier/kind/status enum violations none, status histogram `mined=134 queued=8 rejected=22`, tier
  histogram `A=141 B=6 C=17`. The `used-by` existence check prints the two entry paths as missing at the base revision — expected:
  they are entry-scribe deliverables.

## Assimilation

Id lists under `.ufo/waves/round-59/assimilation/`: registry `reg-ids` 162, staged `staged-ids` 129, `collisions` 8 (S312 S329
S367 S372 S373 S374 S390 S409 — the round-57/58 set). Neither S425 nor S426 appears in either list; S398 appears in `staged-ids`
and not in `reg-ids`. Renumber map by document: staged S398 → S425; S426 has no staged id (lane-found from S425). Quarantine
slice: 12 rows (S142 S143 S148 S154 S156 S161 S178 S184 S193 S194 S195 S206), unchanged and held — the round-58 L0 question is
unanswered, so nothing from the slice is appended this round (routed around, not treated as answered).

Quarantine hand-check, dated 2026-10-27 (slice re-derived byte-identical to round 58; register read-only; nothing appended — the
round-58 L0 question is unanswered and C3's C8 pins the registry to the mirror plus S425/S426; `w1/ReviewerQuarantineHold.md`
§Conformance):

| Row | Source reopened / located text | Verdict this round |
|---|---|---|
| S142 | `https://www.kimi.com/help/websites/websites-faq` (GET 200); the FAQ sentence is present in one `<p>` text node, but the registered string ends `…将网站设为私密。` while the page continues `…将网站设为私密，或者内容不适触发举报。` (0 exact occurrences of the registered form) | substance present; quote-form defect (truncated before the final clause); not appended (C3 frozen) — `w1/ReviewerQuarantineHold.md` |
| S143 | `https://developer.chrome.com/docs/crux/methodology/tools`; the CrUX-on-BigQuery cells hold the listed tool/frequency/metrics/dimensions/history/scope, but the registered string is a ` — ` join across cells (0 exact matches) | quote-form absent as registered; no fabrication verdict; not appended (C3 frozen) |
| S148 | `https://arxiv.org/abs/2308.06409` (abstract and HTML endpoints); `ratio of total to distinct` has 0 matches in both — it and the longer fragment sit only in `%`-commented draft lines of the e-print `sections/analysis.tex` (11, 22), one beside `\texthl{[check this …]}` | absent as registered at the cited page; draft-text only; refuse for this round |
| S154 | CrUX API endpoint `https://chromeuxreport.googleapis.com/v1/records:queryRecord`; GET 404, no document body; register class says the source could not be fetched and no quote was checked | unverifiable (prose class; unreachable is not fabrication) |
| S156 | `https://kimi.page/`; `curl -sSLI` returned HTTP/2 200 with `cache-control: private, no-cache, no-store, max-age=0, must-revalidate` | present in the HTTP response header; not appended (C3 frozen) |
| S161 | `https://developers.google.com/crawling/docs/crawlers-fetchers/reduce-crawl-rate` (GET 200, `Last updated 2026-10-06 UTC`); the registered cell carries register-side backticks (0 occurrences); without them the sentence spans three text nodes | substance present; quote-form defect (multi-node, backticks); duplicate-URL relation with S274 noted; not appended (C3 frozen) — `w1/ReviewerQuarantineHold.md` |
| S178 | PageSpeed API `https://www.googleapis.com/pagespeedonline/v5/runPagespeed`; GET 429 quota-exceeded JSON, with and without a `url` parameter; no quotable body | unverifiable (prose class; unreachable is not fabrication) |
| S184 | CrUX API endpoint, same URL as S154; POST 403 `unregistered callers`, GET 404; no quotable body | unverifiable (prose class; unreachable is not fabrication) |
| S193 | GitHub row URL is the lane origin (`git remote -v`); landing page 200 but 0 matches; exact sentence at `corpus/knowledge/crawl-scope-per-host.md:46` (blob `9710e0343829…`) | present in own-work file; not appended (C3 frozen) |
| S194 | the registered URL is the lane's own GitHub origin landing page (0 occurrences); the exact sentence is in `corpus/knowledge/drift-detection.md` line 28 (raw GitHub blob byte-identical to the lane file) | present in own-work file, not at the registered URL (repo-root URL defect); not appended (C3 frozen) — `w1/ReviewerQuarantineHold.md` |
| S195 | Same repo URL, 0 matches on the page; exact sentence at `corpus/knowledge/publish-queue.md:18` (blob `2fbeab366a2c…`) | present in own-work file; not appended (C3 frozen) |
| S206 | Repo landing page 0 matches; shokuknow artifact `lanes/kake/round7/.evidence/merge_renumber_r7.txt` line 1 reads `S187-S193`, the register `S187-S199`, and the artifact's duplicate list is 7 ids (S187–S193) | absent as registered (one-token misquote); substance verified by the artifact; refuse as registered |

Union: 6 present in substance (S142, S156, S161, S193, S194, S195 — three of them with a quote-form or URL defect that the round-58
table did not record), 3 absent as registered (S143, S148, S206), 3 unverifiable-prose-class (S154, S178, S184).

## Search log (rule 5)

Round 59, crawler identity verification signals (assimilation theme from `merge/kake/`). Question: how
does Google's own crawler documentation tell a publisher to tell a genuine Google crawler request from an
impostor, and which signals does it name? Where: the staged package (staged entry
`crawler-identity-three-signals.md`, staged row S398, the same URL as S425; staged
`amendments/corpus/knowledge/crawler-identity.md`, round2; staged `yahoo-crawler-ua-carrier-survey.md`,
staged row S394), the lane's held ground (`w1/ScoutLaneCrawlerIdentity.md`: registry 162 rows with no
S425/S426 row, no entry holding Google IP or reverse-DNS material, no Yahoo DNS entry, the only
crawler-identity entry being `crawler-identity.md` on S263), then the pages opened directly:
`overview-google-crawlers` (retained `sources/S425.html`, HTTP 200, 74,477 bytes, sha256
`ff2b9fd7ed07…`, fetched 2026-10-27T01:21:22Z, userAgent `kake-shokunin-round59`) and, through its own
in-article link `Learn how to use these details to verify Google's crawlers and fetchers.` (S425.html
line 1284; the same href also sits once in the page navigation, line 720 — own), `verify-google-requests`
(retained `sources/S426.html`, 69,789 bytes, sha256 `8df9d4ade1d1…`, same fetch; `sources/receipts.json`).
Included 2: S425, from staged S398 renumbered by document to the registry's next unused id after S424;
S426, lane-found with no staged id. Excluded, each screened by a wave-1 seat:

- the staged `amendments/corpus/knowledge/crawler-identity.md` (round2) — `w1/ScoutRejectAmendment.md`:
  a strict subset of the lane's S263 entry under a duplicate id (staged S300 vs lane S263, same URL, same
  section, same `Last updated 2026-02-03 UTC`), it repeats the stale line-31 sentence verbatim, and its
  one quote spans two text nodes; the live page is unchanged in substance (HTTP 200, 175,561 bytes, byte
  diff attribute ordering only). Flip: admit if it carries a sentence not already in the lane.
- the staged `yahoo-crawler-ua-carrier-survey.md` (S394) — `w1/ScoutRejectYahooUA.md`: it cites an
  own-work count file outside the lane and outside the registry, quotes no operator page, its DNS thesis
  belongs to `archives/002855.php` which the lane does not hold (round-55 S386 refusal, round-58
  id=2855 exclusion), its recheck greps a string the sweep script itself writes, and the ads-page figures
  no longer reproduce (436,802 → 102,822 bytes live). Flip: adopt 002855 as a lane row and re-cut the
  entry on its sentences under a CJK-units quote rule.

Stop rationale: one theme per round and two entries — the contract's C3 caps the round at two new rows
plus one append-only correction tail, and S425+S426 close the identification-signal half (three signals
on S425; the reverse-then-forward DNS procedure and published IP-range lists on S426) with every quote
inside the frozen 6..25-token / ≤160-character / one-text-node rule (`span_tools.py check`). The two
refused candidates are refused for duplication and for resting on pages the lane does not hold, not for
want of searching; the Yahoo re-grounding cannot pass the token-count rule at all (a whole Japanese
operator sentence is one whitespace token — `w1/ScoutRejectYahooUA.md`), so it is deferred to a round
that widens the rule rather than forced into this one.

## Mistakes

| Class | Evidence | Captured-by | Fix |
|---|---|---|---|
| survivor | `corpus/knowledge/crawler-identity.md:31` reads verbatim in the base blob (`git show fd6303ce:corpus/knowledge/crawler-identity.md \| sed -n '31p'` → `- **A user-agent string is the only thing a server log records about the crawler.** Two`). It landed at `5591557` (2026-10-24, round 51, `git log -S'only thing a server log'` names that one commit) and was carried unrepaired through **N = 7** closure passes: the spot-checks of rounds 51–57 never list it (`grep -n 'crawler-identity' corpus/lessons/round-5[1-8]-verifier-spotcheck.md` hits only `51:68`, `51:98` — both the S262/S263 admit — and `55:30`, the "Smartphone and Desktop" row check; no routed-defect entry in `51:§6`'s ten items). The round-58 closure names it `D1` and calls it "carried since round 51" (`round-58-verifier-spotcheck.md:80`) yet repairs nothing, so counting the routing round gives 8 rounds of standing text. Repair state at base: `grep -c 'r59-correction'` = 0, `grep -c 'S425'` = 0 on that blob. | none: no gate reads the age of a routed defect. `QUALITY.md`'s routed-defect family only accepts a pointer to the routing item (`:301`, `:488`, `:505`) or labels debt without ageing it (`:399` "carried as open debt, not a pass"); `SKILL.md` records closures ("Round 52 gate registry additions (r51 closure routed defect 1)", `:1206`) and disclosures ("routed defect D3 of the round-57 spot-check", `:1288`) but holds no open-defect ledger with a round column. A defect named once is never re-read. | Claim C3 condition `C9_stale_claim_corrected` (`c59_quote_truth.py`): an append-only `[r59-correction 2026-10-27]` line within 8 base lines of the sentence, citing S425, inside the retained-body check. Red-before: `controls/base-c3-quote-truth.txt` `0/9 met=False`, C9 FAIL with all three sub-reasons; re-run by this seat, identical (see RED-BEFORE). |
| reference-drift | `SCORECARD.md` axis table at base `fd6303ce` cites bytes the lane does not hold, and both cells keep score 10: operability (`sed -n '17p'`) pins `cli.mjs:935` plus three bare continuations `:836-839`, `:932`, `:393` in a source tree the lane no longer holds; freshness (`sed -n '18p'`) points at six `/tmp/kake-r17/…` files (`scout-claims.md`, `claims-delta.tsv`, `critic.md`, `reviewer-cites.md`, `scout-pins.md`, `scout-live.md` — `ls -d /tmp/kake-r17` → "No such file or directory") and the vanished `corpus/claims` (`ls corpus/claims` → absent). "Last change" still reads `round 12` / `17`; the ratifying prose calls the ratings "legacy round-17/18 assessments". Counter: `C1 axis-evidence mismatches=16 unresolved=11 rows_no_receipt=3 rows_no_tally=2 cross-check scores_held=2 superseded_kept=0`. | prompt §7.5 (`.ufo/prompts/kake-round-59.md:625`: "A `/tmp` path is therefore never citable evidence (QUALITY-class defect, as kotodama Q14 already rules)"; kotodama Q14 = "no /tmp pointers", `.ufo/reports/round-34/kumitate.md:75`) and the lane's own `QUALITY.md:607` round-34 criterion ("A cited artifact resolves from committed lane bytes, not a seat's sandbox … A `/fast/scratch/...` or `/tmp/...` path stands beside that path as provenance, never as the only pointer"), plus `QUALITY.md:128`. Every one of these was written after the cells, and none was ever applied to `SCORECARD.md`: the table is the one surface no criterion scans. | Claim C1 (`c59_axis_evidence.py`): each cell names only committed paths at the scored revision, at least one on-axis receipt, at least one tally found in a cited blob; operability/freshness scores unchanged; the three base cells kept verbatim. Red-before 16 mismatches (`controls/base-c1-axis-evidence.txt`, re-run by this seat, identical). |

Count note for row 1, so the number is auditable rather than asserted: the seven unrepaired passes are
rounds 51, 52, 53, 54, 55, 56, 57 (each spot-check present under `corpus/lessons/`, none listing the
sentence); round 58 is the eighth pass and is where it is finally named; the round-59 base still
carries it. The assignment's instruction is to count from the spot-checks, so **N = 7** is the number
to print, with "r58 routed, r59 base still red" as the continuation.

Red-before (both shown able to fail on the base revision): `.ufo/waves/round-59/controls/base-c3-quote-truth.txt` (`0/9 met=False`,
`C9_stale_claim_corrected FAIL`) and `.ufo/waves/round-59/controls/base-c1-axis-evidence.txt` (`mismatches=16 … met=False`, exit 1); the
version-2 re-runs of both live beside them as `base-c1-axis-evidence-v2.txt` and `base-c3-quote-truth-v2.txt`.

## Considerthese

`considerthese/2026-10-26.md` (2026-10-26) proposal 3 (operator-decision queue) is implemented here as the lane's routed-item
queue, grounded by `w1/ScribeConsiderthese.md`: every still-open kake row in the fleet `.ufo/l0-questions.md` (lines 5, 38, 80,
81, 132, 180, plus the record-only 14, 19, 20, 119), the operator items of the round-54..58 spot-checks and the SHONEN notes.
Waited counts the rounds after the one that first raised the item, through round 59.

| # | Item (operator's, not the lane's) | First raised (round · pointer) | Waited | Current state |
|---|---|---|---|---|
| 1 | SHONEN promotion, four boxes | r0 · `SHONEN.md` seed `1126144` (2026-09-28) | 59 | `SHONEN.md` at HEAD is 4 × `[ ]`; the r58 report's `[~]` on boxes 1/3/4 (`.ufo/reports/round-58/kake.md:60-63`) has no home in the checklist |
| 2 | Enable the keeper tick or retire the automation path | r12 · `.ufo/l0-questions.md:5` | 47 | moot: both webzites timers are `not-found` to `systemctl --user`, no `webzites*` unit file exists; retire the row and correct `SKILL.md:73-77` |
| 3 | Ratify the relaunched round namespace and craft-dispatch wording | r16 · `.ufo/l0-questions.md:38` | 43 | open; rounds 17–59 continued under steered numbers, no ruling on record |
| 4 | Round-24/25 policy-stop disposition | r24 · `.ufo/l0-questions.md:80` (+81) | 35 | open (`LOG.md:852,917`; `round-27-verifier-spotcheck.md:61`), nothing retried |
| 5 | C1 witness-gate trust boundary | r45 · `.ufo/l0-questions.md:132` | 14 | open, unmentioned in rounds 46–58 |
| 6 | Merge or delete `wip/operator-save-20261023`, close draft PR #1 | r50 · `round-50.md:31` | 9 | tip `e80f84d`: 120 behind / 1 ahead of master, 41 files +15,669/−2 |
| 7 | CJK reading of the ≤25-word quote rule | r53 · `round-53-verifier-spotcheck.md:82` | 6 | convention open; the S367 quote was re-cut to ≤24 units in r56, so no committed quote exceeds 25 units |
| 8 | `calibration` sub-axis ownership | r54 · `round-54-verifier-spotcheck.md:66` | 5 | open; `SCORECARD.md:4299-4301` and the round-59 `contract.md` both name it for the operator |
| 9 | §10 quarantine: adopt the six `present` rows without widening C3? | r58 · `.ufo/l0-questions.md:180` | 1 | held; the round-59 contract routes around it |

Two rows are the queue's real defect: 7 (r53) and 8 (r54), the longest-waiting live items, were never filed in the L0 channel —
the kake rows run r45 then r58 — so they live only in spot-checks and contracts and cannot be answered where the operator reads.
Every operator item of the round-54..58 spot-checks is a rediscovery of rows 7, 8 or 1. Row 2 went stale instead of answered.
Proposals 1 (read the lane's own receipts), 4 (gate-agreement ledger) and 5 (historical-gate list) are not taken this round.

Follow-up taken this round: rows 7 (CJK quote-unit rule) and 8 (calibration ownership) are filed in the L0 channel
(`.ufo/l0-questions.md`, kake round-59 lines). Proposals 1, 4 and 5 not taken (one proposal per round; 5 already landed as the
round-58 `historical` markings; `w1/ScribeConsiderthese.md` §Not taken).

## Routed defects (round-58 spot-check §6)

- D1 `crawler-identity.md:31` UA-only claim: corrected append-only by claim C3 (condition C9; `[r59-correction 2026-10-27]` citing S425).
- D2 counter residual limits: fixed forward in all three round-59 counters (inherited `GIT_*` scrubbed, `--base`/`--revision` resolved
  once, `--root` must be a repository toplevel; `w1/SentinelCounters.md` §D2 status); the resolver's revision-mode symlink read and
  registry symlink escape are claim C2 cases K11/K12. The round-58 counters stay historical with the limits on record.
- D3 present quarantine rows: held again (L0 unanswered); re-hand-checked above.
- Carried limits: C2 P6 printed-tally trust (now demonstrated by the `tally_liar` control, still a limit); `--first-parent` history
  boundary (round-58 C1) unchanged.

## Trend inputs

expansion: two entries on Google crawler identification and verification (S425, S426, `mined`, opened 2026-10-27); the frontier map's
`Crawler identity` ground held Googlebot subtypes (S263) and Baidu (S423/S424) only. quality: the UA-only claim corrected against a
re-opened live source; the SCORECARD axis table's evidence re-pointed at committed receipts (16 base mismatches); seven resolver
false-green / robustness routes closed plus FIFO, dangling-link and descriptor-containment hardening; three counters hardened by a
66-seat wave before data. discernment: one staged entry re-grounded with eight sentences refused, two staged candidates refused with
flips, the 12-row quarantine slice re-checked with three new precision defects found; the non-author spot-check belongs to the closure.
