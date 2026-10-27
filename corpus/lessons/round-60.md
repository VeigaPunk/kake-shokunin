# Round 60 — lessons (kake)

Round opened 2026-10-27 00:56 (-03:00); sources accessed 2026-10-27 (UTC). Base `97cdc122379711c2b02a8970752c8782da3ac81d`; contract
`.ufo/waves/round-60/contract.md` (version 1 committed `b3b9e29` before any seat ran; counters version 1, amendments A1–A9 and A3a,
frozen at `1ea30590` before any after-state was scored). Wave `w1`: 44 seats (`.ufo/waves/round-60/w1/`).

## Gate

Rows opened this round. Unit rule (the C3 counter's `units()`): one unit per CJK character, one per non-CJK whitespace token;
every quote below is 6 to 25 units and at most 160 characters, a substring of one whitespace-collapsed text node of the retained
body's article block (the container of class `devsite-article-body` .. `<devsite-content-footer`), and page-unique across the three
bodies. All three pages were fetched 2026-10-27T04:03Z by `.ufo/waves/round-60/fetch_sources.py` (GET, HTTP 200, effective URL equal
to the request URL, userAgent `kake-shokunin-round60`) and retained under `.ufo/waves/round-60/sources/` with the sha256 receipts
in `sources/receipts.json`; the digests were re-run this wave (`sha256sum` and byte counts, all three equal to the receipt). Each
page prints `Last updated <date> UTC` inside `<devsite-content-footer`, read with the R59-D3 fix's placement rule. Anchor rule
(L1 ruling, 2026-10-27): the anchor cell names the nearest article-block heading (h1/h2/h3) that precedes the row's quote, and
every quote on the row's Gate line lies in that heading's section (below the anchor heading, above the next one). S427's two
quotes sit in the page lead, so its anchor is the article h1; S428's quotes also sit in the lead, under its h1; S429's quotes
sit under the h2 named.

- S427 — https://developers.google.com/crawling/docs/crawlers-fetchers/overview-google-crawlers — accessed 2026-10-27 — § Overview of Google crawlers and fetchers (user agents) (Last updated 2026-06-12 UTC) — quote: "They always respect robots.txt rules for automatic crawls." (8 units; substring of one collapsed text node of the retained body, sha256 d70ce6f5aa51ff2f7e6192191330976bd6279e3f2e91d30ef988d3d805382175, 74477 bytes, HTTP 200), and "User-triggered fetchers are part of tools and product functions where the end user triggers a fetch." (16 units; same retained body, sha256 d70ce6f5aa51ff2f7e6192191330976bd6279e3f2e91d30ef988d3d805382175, 74477 bytes, HTTP 200)
- S428 — https://developers.google.com/crawling/docs/crawlers-fetchers/google-user-triggered-fetchers — accessed 2026-10-27 — § List of Google user-triggered fetchers (Last updated 2026-08-19 UTC) — quote: "these fetchers generally ignore robots.txt rules" (6 units; substring of one collapsed text node of the retained body, sha256 0f296b8636d5fb9d44c66fc1453a5610fdf738c80c9baef44c233e0a1872d3b2, 76197 bytes, HTTP 200), and "it only covers the requestors that are more likely to show up in log files" (15 units; same retained body, sha256 0f296b8636d5fb9d44c66fc1453a5610fdf738c80c9baef44c233e0a1872d3b2, 76197 bytes, HTTP 200)
- S429 — https://developers.google.com/search/docs/crawling-indexing/robots/intro — accessed 2026-10-27 — § Understand the limitations of a robots.txt file (Last updated 2025-12-10 UTC) — quote: "The instructions in robots.txt files cannot enforce crawler behavior to your site" (12 units; substring of one collapsed text node of the retained body, sha256 423d99c5bf7fec4298d00cdd46f01a495c9ad463fa704f7850a100e43e2a9edd, 178797 bytes, HTTP 200), and "A page that's disallowed in robots.txt can still be indexed if linked to from other sites." (16 units; same retained body, sha256 423d99c5bf7fec4298d00cdd46f01a495c9ad463fa704f7850a100e43e2a9edd, 178797 bytes, HTTP 200)

S425 erratum (R59-D4). The S425 `scope` cell reads `the three crawler categories and their robots.txt posture`, which reports a
robots.txt posture for all three categories. The page does not state one for all three: its `crawler-types` table gives a posture
for common crawlers ("They always respect robots.txt rules for automatic crawls.") and for special-case crawlers (the AdsBot
example, which "ignores the global robots.txt user agent (" … ") with the ad publisher's permission."), and its user-triggered
fetchers cell carries no robots.txt clause at all — it reads "User-triggered fetchers are part of tools and product functions
where the end user triggers a fetch." and closes on "acts on the request of a user." for Google Site Verifier. The cell is
superseded by S427 on the same URL (re-opened 2026-10-27, sha256 d70ce6f5…, 74477 bytes), whose `teaches` cell opens
`supersedes S425 —` and whose `scope` cell names the categories the page does state a posture for and records its silence on the
third. S425 itself is left in place: a pure addition, no existing row's status, recheck or used-by changed.

ADMIT theme `robots.txt posture and limits per Google crawler category` (staged package `merge/kake/`, shokuknow, read-only):
staged `google-robots-txt-limits.md` / staged row S415 is re-grounded as `corpus/knowledge/robots-txt-limits.md` on **S429** —
renumbered by document (the robots.txt introduction URL), not arithmetically; the staged name is not carried. Every staged
sentence was read against the retained S429 body (`w1/ScoutStagedS415.md`, `w1/EntryRobotsLimits.md` §Refused staged sentences):
15 staged items refused or rewritten — the wrong anchor (`§ How robots.txt works` is no heading of the page, count 0), the stale
2026-10-24 dates, the Baidu/Yahoo cross-document attributions (`baidu` 0, `yahoo` 0 in the body), lane meta-prose ("from three
directions", "the useful part", "only one operator has promised" — count 0), the `each crawler reads it its own way` title (the
page says each crawler *might* interpret the rules differently) and the staged filename. Kept: the page's own limits sentences as
verbatim spans. **S428** is lane-found (the third row of the S426 category table links it; `w1/ExecSourceLive.md`: 2 hrefs, anchor
`User-triggered fetchers`); **S427** is the S425 URL re-opened for the superseding row.

Decision lines:

- REJECT staged `common-crawlers-japanese.md` (staged S337, `google-common-crawlers?hl=ja`) — its quote is 60 CJK units under the
  counter's unit rule (one unit per CJK character), above the 25-unit ceiling, and as written it is not a page substring (a
  transcription space); its content (one `User-agent:` token per rule, a Googlebot block reaching several products) is crawler
  addressability, not the theme's posture/limits, and the contract caps the round at three new rows (`w1/ScoutRejectCommonJa.md`;
  live page re-opened HTTP 200). Flip: a later round with a free registry slot re-grounds it on the English edition (a 19-unit
  counterpart quote passes) or on a <= 25-unit Japanese span.
- The S425 erratum below is not a rejection: S425 stays, superseded by S427.

Non-author discernment spot-check: **pending** at lane filing; no dispatched seat is a non-author. Closure must re-open at least one
admitted row (S427, S428 or S429) and one reject (above) and record `agree`/`disagree` with reasons, per `LEARNING.md`.

## Registry changes (old → new)

- Rows: 164 → 167. S427, S428 and S429 are appended after S426 in that order, all `mined`, opened 2026-10-27, recheck `180d`;
  `used-by` = S427: `corpus/lessons/round-60.md`; S428: `corpus/knowledge/google-user-triggered-fetchers.md,
  corpus/knowledge/googlebot-verification.md`; S429: `corpus/knowledge/robots-txt-limits.md`. S427 supersedes S425 by scope
  correction; no existing row's `status`, `recheck` or `used-by` changed (a pure addition).
- Counts: `grep -cE '^ {0,3}\|[[:space:]]*S[0-9]{3,}[[:space:]]*\|' corpus/SOURCES.md` = 164 at the base revision; all three ids
  are absent from the base (`grep -cE '^ *\| *S42[789] *\|'` = 0).
- Draft-row census (a scratch copy of the registry plus the three draft rows, frozen census awk formulas): rows 167, malformed
  (NF!=13) 0, escaped pipes 0, duplicate ids none, tier/kind/status enum violations none, status histogram `mined=137 queued=8
  rejected=22`, tier histogram `A=144 B=6 C=17`. The `used-by` existence check prints three paths as missing at the base revision —
  expected: they are this round's entry and lesson deliverables.

## Assimilation

Id lists under `.ufo/waves/round-60/assimilation/` (0–3-space pattern; guard proven first on a scratch registry whose only row is
indented two spaces, `guard-proof.txt` → `S002`): registry `reg-ids` 164, staged `staged-ids` 129, `collisions` 8 (S312 S329 S367 S372
S373 S374 S390 S409 — the round-57/58/59 set). Staged S415 is in `staged-ids` and not in `reg-ids`; renumber map by document: staged
S415 (`https://developers.google.com/search/docs/crawling-indexing/robots/intro`) → S429. S427 (re-open of the S425 URL) and S428
(lane-found from the S426 category table) have no staged id. Pre-append mirror: `assimilation/pre-append/corpus/SOURCES.md` = the base
registry at `97cdc122` (164 rows, 152817 bytes, sha256 `bc054d10868d3dd5e59b60f71134d21ee974bb63a0ff6a462f2d2048f76be119`,
`mirror-pin.json`), committed in `b3b9e29` before any wave seat ran. Quarantine slice: 12 rows, byte-identical to round 59
(`cmp` exit 0); held — the round-58 L0 question is unanswered, so nothing from the slice is appended (routed around, not treated
as answered).

Quarantine hand-check, dated 2026-10-27 (`w1/ReviewerQuarantineHold.md`, evidence `.files/reopen-evidence.txt`): slice re-derived
byte-identical to rounds 59 and 60; the round-58 L0 question still has no answer; three rows re-opened live — S142 (HTTP 200: the
registered string is truncated before the final clause, 0 exact occurrences, substance present), S161 (HTTP 200, `Last updated
2026-10-06 UTC`: register-side backticks, 0 occurrences, substance across three text nodes), S206 (the lane origin landing page,
0 occurrences; the shokuknow artifact reads `S187-S193`, the register `S187-S199`) — each confirms its round-59 verdict. Nothing
is appended.

## Search log (rule 5)

Round 60, robots.txt posture and limits per Google crawler category (assimilation theme from `merge/kake/`). Question: what does
Google's own documentation state as the robots.txt posture of each of its three crawler categories, and what limits does it put on
the file itself? Where (`w1/ScribeSearchLog.md`, every count with its command): the staged package — `SOURCES.append.md` 129 staged
rows, 28 carrying `robots`, 12 of those Google-published, 5 naming a crawler (S323, S327, S337, S398, S415), and `MERGE-REPORT.md`
whose two theme entries are `common-crawlers-japanese.md` (line 51) and `google-robots-txt-limits.md` (line 122); the lane's held
ground — 55 knowledge entries, 23 mentioning robots, `googlebot-verification.md` the only one naming user-triggered or special-case
crawlers, no entry carrying `generally ignore`, and base row S425 whose `scope` claims a posture for all three categories; then the
pages opened directly: the S425 URL re-opened (`sources/S427.html`, HTTP 200, 74,477 bytes, `Last updated 2026-06-12 UTC`), the
user-triggered category page through the third row of the held S426 table (`sources/S428.html`, 76,197 bytes, `Last updated
2026-08-19 UTC`) and the robots.txt introduction (`sources/S429.html`, 178,797 bytes, `Last updated 2025-12-10 UTC`), all fetched
2026-10-27T04:03Z. Identified 4, screened 4, included 3 (S427, S428, S429), excluded 1 (staged `common-crawlers-japanese.md`, reasons
above); off-theme by title, recorded not counted: staged S398 (already S425), S323 (crawl-error troubleshooting), S327 (a Japanese
robots.txt blog post). Stop: bounded by design — one theme, three rows (contract C3) — and each held category now has a posture on
a held page: common crawlers (S427), special-case crawlers (S426's "may or may not respect robots.txt rules"), user-triggered
fetchers (S428). Leads, not rows: the English `google-common-crawlers` and `google-special-case-crawlers` pages (the special-case
page prints "The special-case crawlers may ignore robots.txt rules", L1 probe 2026-10-27, not retained).

## Mistakes

| Class | Evidence | Captured-by | Fix |
|---|---|---|---|
| stale-premise (round 59: "gate-collision") | The round-55 `readme-index-counter`'s `head_changed` term requires every round-55-base knowledge blob to survive as a byte prefix (`.ufo/waves/round-55/c55_readme_index.py:30-31`, `:199 if not new.startswith(old)`); the lane's own correction practice inserts tagged runs where the stale line ends (`corpus/knowledge/crawler-identity.md:35`, `**[r59-correction 2026-10-27]**`, `git diff --numstat fd6303ce 97cdc12 -- corpus/knowledge/crawler-identity.md` → `16 0`). At build `ab6e100e` the gate read `index_mismatches=1 … head_changed: crawler-identity.md`, exit 1 (`.ufo/waves/round-59/a2r1/ReviewerNoHarm.files/out-c55.txt`). The only tool that checked append-only discipline could not tell a tagged in-file correction from a rewrite. | `corpus/QUALITY.md` round 59 ("A frozen claim never silently turns a standing gate red") caught the trade only after the fact; no tool encoded the correction practice. | Claim C2: `scripts/append_guard.py` (new; an end-of-file append passes, every other inserted run must open with a visible `[rNN-correction YYYY-MM-DD]` tag; changed, reordered, deleted base lines and deleted/symlinked files fail). Shown able to fail: the c55 byte-prefix port scores 8/24 and fails K2, K15 and R1 — the tagged run, the alignment case and the real round-59 correction (`.ufo/waves/round-60/controls/c2-selftest.txt`); the guard fails R2 (`changed corpus/knowledge/crawler-identity.md`, one byte); base 0/24 (`controls/base-c2-guard-cases.txt`). |
| scope (round 59: "counter-scope gap") | `.ufo/waves/round-59/c59_axis_evidence.py:67` `HELD = ("operability", "freshness")`; a scratch mutant moving only the calibration score 2 → 10 printed `met=True`, exit 0 (`.ufo/waves/round-59/a2r1/CriticCountersV2.md:5`). The claim's own axis score sat outside its counter. | none: the round-59 selftest's score case covered held axes only. | Claim C1's `scores_held == 3` term (A7: one axis table, one row per axis, digit-exact 10/10/2). Shown able to fail: the same score-only mutant on a scratch clone of `1ea30590` reads `scores_held=2/3 met=False`, exit 1, while the round-59 counter on that mutant still exits 0 (`.ufo/waves/round-60/controls/redbefore-c1-score-mutant.txt`). |
| reference-drift (round 59: "row precision", R59-D4) | `corpus/SOURCES.md` row S425 `scope`: "the three crawler categories and their robots.txt posture"; the page states a posture for common crawlers and the AdsBot special case only (`w1/ReviewerS425Erratum.md`, both bodies). | none: no rule tested a `scope` cell against the categories its page actually covers; the outside spot-check caught it. | Row S427 (`supersedes S425 —`, corrected scope) and C3 condition C3 (the phrase banned, `common crawlers` and `special-case crawlers` required, the over-claim regex of A9 rejected). Shown able to fail: base `C3_row_shape FAIL` (`controls/base-c3-quote-truth.txt`) and the counter selftest's scope fixtures (`controls/c3-selftest.txt`, 140/140). |
| survivor (the class behind all three: a status label not re-derived from a run) | At base the registry held 12 of the 28 round 48–59 counters with no row at all, `c53_gate_truth.py` labelled live while it exits 1, and `receipt-pin-counter` pinned at `32754df7`, a revision where its own command exits 1 (`new_receipts=0 scorecard_pin=0`; green only from `20217f23`) — `C1 gate-status members=28 mismatches=14 scores_held=3/3 met=False` (`controls/base-c1-gate-status.txt`). The round-59 relabel of `readme-index-counter` was made by hand after the reviewer ran the gate. | `corpus/QUALITY.md` round 59 named the duty but nothing ran it. | Claim C1: `c60_gate_status.py` re-derives every label from exits at the measured revision and at the pin; the registry gains the 12 rows and three relabels. Shown able to fail: base exit 1 with 14 mismatches; the counter selftest 76/76 (`controls/c1-selftest.txt`). |

Carried, not fixed (R59-D3): the round-59 C2 P6 printed-tally trust, the fixture-sniff composite (scratch `b58b83ab`) and the eight
proposed resolver cases Q1–Q8 (`.ufo/waves/round-59/w1/MutC2Gate.md:156-167`) — one operability claim per round, and round 60's is
R59-D1; C3's footer read is fixed forward (`Last updated` must sit inside `<devsite-content-footer`, A9).

## Considerthese

`considerthese/2026-10-26.md` (2026-10-26) proposal 5 (historical-gate list) is implemented as claim C1, grounded by
`w1/ScribeConsiderthese.md`: the list is derived, not hand-kept — `c60_gate_status.py` reads each row's `Kind` cell as a label with
its pin and runs every one of the 28 counters at the measured revision and at the pin, so the proposal's two warnings become computed
classes (`historical_but_green`: a gate that should have been re-pinned; `historical_not_green_at_pin`: a pin that does not hold).
The list itself is the bullet list in `SKILL.md` § Round 60 gate-status ledger. The base already held one wrong pin
(`receipt-pin-counter`), which the counter caught and this round moved. Proposals 1 (read the lane's receipts), 2 (receipt-rewrite
watch — the round-58 `receipt-rewrite-counter` already runs it) and 4 (gate-agreement ledger — needs a non-author column the lane
cannot fill) are not taken.

## Routed defects (round-59 spot-check §6)

- R59-D1: claim C2 (append guard) and claim C1 (relabel duty; `SKILL.md` § Round 60 gate-status ledger).
- R59-D2: claim C1 `scores_held == 3`, red-before above.
- R59-D3: C3 footer fixed forward; P6, fixture-sniff and Q1–Q8 carried (above).
- R59-D4: row S427 and C3 condition C3 (erratum in § Gate).
- R59-D5: status-neutral; seats are counted from `w1-results.json` (44/44 settled with output, none dead), none re-spawned; the L1
  holds the planner seat.
- Carried: round-58 D3 (quarantine rows held, L0 unanswered); L0 rows of round 59 (calibration ownership, CJK quote units) unanswered.

## Trend inputs

expansion: two entries on ground the coverage map did not hold — Google user-triggered fetchers and their robots.txt posture (S428),
and the limits Google states for the robots.txt file itself (S429; the lane held the RFC 9309 reading, not these) — plus a new lane
capability (the append guard). quality: the S425 scope overstatement superseded on a re-opened page; the user-triggered posture
re-verified against a later, category-specific page and corrected append-only; 12 unregistered counters registered and three wrong
labels (a never-green gate called live, a pin where the gate is red, a gate the round's own rows turn red) re-derived from runs.
discernment: 15 staged items refused with page counts, one staged entry rejected with a flip, three quarantine rows re-checked; the
non-author spot-check belongs to the closure.

## Wave 2 and measurement

Wave 2 (38 attack seats on build `8b33fd24`, `.ufo/waves/round-60/w2/`) found and the round fixed before measurement: the guard read
`git ls-tree` without `-z`, so a git-quoted (non-ASCII) path fell silently out of scope (`w2/SentinelGuard` high); its line-local
code-span scanner missed spans crossing line ends and closed on unequal runs (`w2/ReviewerGuardCode`); 16 of 33 tool mutants
survived the version-1 counter (`w2/MutGuardTool`) — counter version 2 adds sub-fixtures to eight cases and the B1 tool scores 22/24
under it (`controls/c2-b1-tool-under-v2.txt`); the C1 counter read cells inside an inline HTML comment as rendered
(`w2/ReviewerC1Counter`, fixed in version 2); the correction's publisher-advice sentence and the S428 entry's identifier sentence
overreached (`w2/ReviewerCorrection`, `w2/ReviewerEntryUT`, both rewritten). Carried as stated limits: C1 process containment,
cleanup and exception exit codes (`w2/SentinelC1Exec`); the C2 existential-alignment laundering case (`w2/CriticGuardSemanticsV2`,
disclosed in the contract); `w2/ReviewerEntryRL`'s six location-description findings on `robots-txt-limits.md` (no quote affected).
Measured at T0 `8001f8d5579303ff390305f9dcddb785834f2084`: C1 `mismatches=0 met=True`, C2 `24/24`, C3 `9/9`
(`controls/after-*.txt`); census exit 0, 167 rows.
