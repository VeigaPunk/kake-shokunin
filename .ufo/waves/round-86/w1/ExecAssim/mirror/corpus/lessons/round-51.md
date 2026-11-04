# Round 51 — kake

Lane: `kake-shokunin`. Author: Kimi fresh L1 (this session). Round shape: one v1 wave of
48 seats under `scripts/hyaku/ufo-wave-policy.json` (band 32-64).

## Gate

- S262 — https://developers.google.com/search/docs/crawling-indexing/canonicalization — accessed 2026-10-24 — § "What is URL canonicalization" (doc rev. Last updated 2026-08-20 UTC) — quote: "indicating a canonical preference is a hint, not a rule" (10 words; raw substring of the retained body, sha256 792224334aea8b473d830081fd31daba3eea69c5e1b1fdccef19084d7d50d23b, 174926 bytes, HTTP 200)
- S263 — https://developers.google.com/search/docs/crawling-indexing/googlebot — accessed 2026-10-24 — § "Googlebot is the generic name for two types of web crawlers used by Google Search" (doc rev. Last updated 2026-02-03 UTC) — quote: "Googlebot is the generic name for two types of" (9 words; raw substring of the retained body, sha256 6afbdc826e55a9dadd7dde75d189ad2bdcdbb6e33daabe6daabc44b2a4e155de, 175561 bytes, HTTP 200)

Both rows are re-grounded in this round: the L1 fetched each URL once (2026-10-24,
23:16 -03:00), kept the response body under `.ufo/waves/round-51/sources/`, and pinned its
sha256 in `.ufo/waves/round-51/sources/receipts.json`. The two quotes above are raw
substrings of those bodies. The other quotations in the two entries are **not** all raw: the
round-51 wave measured 15 body quotations as 3 raw, 2 whitespace-collapsed-only and 10 that need
inline-markup removal, and 10 of the 13 source-relation labels the entries carried were wrong
(wave seat `ExecQuoteRawScan`; audit `ScribeEntryAudit`). Both entries now carry a `## Quote
classes (round-51 correction)` block that states the true classes; the earlier claim in this
section that every quote survives whitespace collapse, and that each entry marks the class of
every other quote, was false.

- reject — `corpus/knowledge/engine-crawl-contracts.md` (staged round 1, staged ids S250/S253/S254): refused because its Google half cites a URL this lane already mines as S137 (within-scope duplicate, census E04) and its two Baidu sources were not opened by this lane this round. Flip: adopt only in a round that opens both Baidu pages itself and cites the lane's own S137.
- reject — `corpus/knowledge/crux-eligibility-route.md` (staged round 2): refused as covered ground, because `corpus/knowledge/field-performance-cwv.md` already holds CrUX eligibility (S038, S039). Flip: admit only if that entry is superseded in place, never as a second row for the same ground.

## Admitted entries

- `corpus/knowledge/canonical-selection.md` — grounded on S262 alone. Google's canonical
  **selection** mechanism: what a declared canonical is worth, which signals are weighed,
  and which variant classes create duplicates. This is the half the lane's held
  `corpus/knowledge/static-canonical-preflight.md` explicitly disclaims.
- `corpus/knowledge/crawler-identity.md` — grounded on S263 alone. "Googlebot" names two
  crawlers (Smartphone and Desktop); the subtype is identified from the HTTP user-agent
  request header, and both obey the same robots product token.

Both entries are new files: the coverage map in `corpus/README.md` did not hold this
ground. The lane's held canonical ground stopped at the declared value, and its held
crawl ground stopped at robots semantics and crawl-budget consequences.

## Refused entries (reason and flip)

- `corpus/knowledge/engine-crawl-contracts.md` (staged, round 1; staged ids S250, S253,
  S254) — **refused**. Reason: the entry's Google half cites
  `https://developers.google.com/search/docs/crawling-indexing/javascript/javascript-seo-basics`,
  a URL the lane already mines as S137 in the same scope, so a second row for that URL is a
  within-scope duplicate (census E04); and its two Baidu sources were not opened by this
  lane in this round, so their quotes are un-re-grounded here. Flip: adopt in a later round
  that opens both Baidu pages itself and cites the lane's own S137 for the Google half
  instead of a second row for the same URL.
- `corpus/knowledge/crux-eligibility-route.md` (staged, round 2) — **refused**. Reason:
  covered ground. The lane already holds CrUX eligibility in
  `corpus/knowledge/field-performance-cwv.md` (S038 CrUX methodology, S039 CrUX API), so
  admitting this entry would not move the coverage map; expansion credit is knowledge on
  ground the lane does not hold. Flip: admit only if the held field-performance entry is
  superseded in place, never as a second row for the same ground.

## Stripped staged prose

The staged rows carried a `recheck` cell holding a shell command and its result
(`180d — curl -fsSL '…' | grep -c 'a hint, not a rule' -> 1 (ran 2026-10-23)`). That prose
is stripped: the admitted rows carry the normalized `180d` cadence, and the commands are
recorded here instead, with their run date, so the row still parses as eleven cells and
no cell carries a literal or escaped pipe.

- S262 staged recheck command: `curl -fsSL 'https://developers.google.com/search/docs/crawling-indexing/canonicalization' | grep -c 'a hint, not a rule'` — run 2026-10-23 by the package; re-run this round against the retained body, where the phrase occurs.
- S263 staged recheck command: `curl -fsSL 'https://developers.google.com/search/docs/crawling-indexing/googlebot' | grep -c 'generic name for two types of'` — run 2026-10-23 by the package; re-run this round against the retained body, where the phrase occurs.

## Id collision check

Run in scratch before any append, with the census parser's own 0-to-3-leading-space
pattern (a column-zero-only pattern misses an indented collision). The staged ids that
overlap the lane registry are S273, S274 and S286 — none of them is adopted this round.
The adopted ids S262 and S263 are unused in the lane registry, so no citation had to be
re-pointed; the guard was proven able to fail on an indented fixture before the check was
trusted. Evidence: `.ufo/waves/round-51/assimilation/`.

## Quarantine

The lane's slice of the campaign's absent-defect register was re-derived read-only and
left unadopted: no quarantined id was hand-checked this round, so the round-48 hand-check
is not used as an adoption basis. Evidence:
`.ufo/waves/round-51/assimilation/quarantine-slice`.

## Mistakes

- **class:** staged quote mis-transcribed as a source quote. **evidence:** the staged
  `canonical-selection.md` quotes "Google chooses the most complete and useful page as the
  canonical URL", which is not in the source; the page says Google chooses the page that is
  "objectively the most complete and useful for search users". The staged
  `crawler-identity.md` quotes "Googlebot Smartphone: a mobile crawler that simulates a
  user on a mobile device", which is not a substring either; the page renders
  "Googlebot Smartphone : a mobile crawler …" with a space before the colon. Both were
  confirmed absent from the bodies this round fetched. **captured-by:** none — the round-50
  quote-class instrument derived a class for quotes the lane already held, but nothing
  re-grounded a *staged* quote before it was copied. **fix:** every admitted entry is
  re-grounded against bytes this lane fetched this round, and the C2 counter's condition
  C5 requires each Gate quote to be a raw substring of the retained body.
- **class:** a wave's seat-report count stated in prose and not re-derivable. **evidence:**
  `corpus/lessons/round-50-verifier-spotcheck.md` routed defect 1 — the round-50 report
  claimed 26 seat reports while the committed tree holds 25. **captured-by:** none —
  `c50_durable.py` proved the grant and the citation order but never counted the
  reports. **fix:** `c51_wave_ledger.py` condition L1 compares the committed report-file
  count, the settlement's `reports_written` and the payload's seat count, and fails when
  they disagree.
- **class:** a route substitution recorded in prose only. **evidence:**
  `corpus/lessons/round-50-verifier-spotcheck.md` routed defect 2 — the HTTP status codes
  behind the fallback existed only in the report. **captured-by:** none — the round-50 route
  map recorded the fallback but no receipt. **fix:** `c51_wave_ledger.py` condition L2
  requires a committed probe receipt per route with an integer HTTP status and a body
  excerpt, and refuses a failing alias used by a role.
- **class:** no aggregate round-overrun figure derivable from committed bytes. **evidence:**
  `corpus/lessons/round-50-verifier-spotcheck.md` routed defect 3 — the overrun was named
  nowhere a reader could re-derive. **captured-by:** none — the round-50 settlement receipt
  carried per-seat seconds but no aggregate and no wall clock. **fix:** the round-51
  settlement carries the wave's start and end stamps, `.ufo/waves/round-51/round-time-accounting.json`
  carries the three figures, and `c51_wave_ledger.py` condition L3 re-derives them from the
  committed bytes and requires the lane's LOG.md to name the wall-clock figure.
- **class:** inherited artifacts swept to make a count look clean. **evidence:**
  `corpus/lessons/round-50-verifier-spotcheck.md` routed defect 4 — the eight
  `.ufo/waves/round-46/residual/` reports and the nine `>1MiB` copies under
  `.ufo/waves/round-48/assimilation/validate/`. **captured-by:** the round-50 QUALITY
  criterion "Operator-owned and inherited artifacts are not swept to zero a count".
  **fix:** they stay uncommitted and untouched this round; the count is reported as it
  stands.

## Corrections — attempt 2 (append-only; the rows above stand as written)

Two `## Mistakes` rows above assert facts the wave falsified. They are corrected here, not
rewritten:

- **Row 1 (staged quote mis-transcription).** The claim that "Google chooses the most complete and
  useful page as the canonical URL" is absent from the source is **false**: it is a raw substring of
  the retained `S262.html` once, inside `<template class="devsite-content-data-template">` (seat
  `CriticGateCriterion`). The claim that the page "renders 'Googlebot Smartphone :'" with a space
  before the colon is also false: the bytes read `</b></a>:` and the space is this lane's markup
  substitution (seats `ExecQuoteRawScan`, `ScribeEntryAudit`, `CriticAbsence`). The real defect
  class is **quote-class mislabelling**, not fabrication: 10 of 13 source-relation labels in the
  two admitted entries were wrong, and 7 of 15 body quotations exist only if every HTML tag is
  replaced by a space. Both entries now carry a `## Quote classes (round-51 correction)` block,
  and the two false labels were replaced in place. The 16 over-assertions the audit named are
  **not** repaired this round; they are routed, with `w1/ScribeEntryAudit.md` as the pointer.
- **Row 3 (route substitution recorded in prose only).** Partly addressed at best: the L2 condition
  is committed, but the only failing receipt this round (`xai-oauth/grok-4.7-fast`, HTTP 403) is a
  probe the wave did not substitute for — every role routes `@m_flash` — so the round proves the
  guard, not a handled substitution (`RevengerR50`). L2's `receipts.setdefault` also lets filename
  order decide which receipt of a duplicated alias survives, with the passing direction discarding a
  committed failure (`CriticTautology`, `ReviewL2Routes`).

## Wave accounting (attempt 2, measured)

One v1 wave of **48 seats** under `scripts/hyaku/ufo-wave-policy.json` (band 32-64), dispatched as
exactly one `task` call from the validator's `ufo-swarm-wave-dispatch-v1` payload
(`.ufo/waves/round-51/w51-taskcall.json`, `counts.spawn 48`, validator exit 0). Role mix: reviewer
10, critic 10, executor 9, scout 6, mutation-tester 5, scribe 4, connector 1, sentinel 1, revenger 1,
simplifier 1. The L1 holds the canonical planner seat.

Seats settled **48**, dead **0**, committed reports **48**. Wall clock **897 s**; aggregate seat
seconds **23 554**; dead-seat seconds **0**. Route mix: every role resolved to `@m_flash`
(`commandcode/deepseek/deepseek-v4.1-flash`) through the operator's `task.agentModelOverrides`;
one route used, one committed probe receipt, no substitution. Sources:
`.ufo/waves/round-51/{settlement.json,wave-timing.json,round-time-accounting.json,route-map.json,route-probes/}`.

Attempt 1's orphaned outputs were inherited and re-verified: the contract, both counters, the two
rows, both entries and the pre-append mirror are reused; the counters were re-run at the base and
the tip by seats `ScoutCounterC1Base`, `ScoutCounterC2Base`, `ScoutCounterC2Tip`; the pre-append
mirror was **discarded and rebuilt** (see below). Attempt 1 committed no wave evidence, so nothing of
it was reused for C1.

## Mistakes (attempt 2)

- **class:** evidence file named for a state it does not hold. **evidence:** the mirror committed at
  `19a99bd` as `.ufo/waves/round-51/assimilation/pre-append/corpus/SOURCES.md` was byte-identical to
  the *post*-append registry (145 rows, both adopted ids) while the live registry at that commit was
  143 rows; C7's census therefore validated post-append bytes under a "before append" name, and C8
  escaped only because it reads the live registry at the mirror commit. Found by seat
  `ExecRegistryDiff`, confirmed by `ScoutCounterC2Tip`, `ReviewC2Conditions`, `CriticAbsence`,
  `CriticZeroControl`. **captured-by:** nothing in the round — C7 checks receipt shape, never the
  receipt's subject. **fix:** the mirror was rebuilt from `git show 19a99bd:corpus/SOURCES.md`
  (143 rows, sha256 `cd9ee4cf…`), the census re-run on it (exit 0, W04 only) and the discriminating
  `census` run added (`rows 143`, `census-count-*`), attempt 1's four receipt files kept verbatim in
  `superseded/`, all recorded in `assimilation/pre-append/census-correction.txt`. The round-52 fix is
  the counter-side one, and its exact form matters: C8 must read `show(root, rev, MIRROR)` — the
  mirror bytes **at the measured revision** — together with the live registry at the mirror's
  add-commit, and the census receipt must pin the mirror's sha256. Reading `show(root,
  mirror_commit, MIRROR)` is unsatisfiable: the blob committed at `19a99bd` is immutably the
  contaminated `4ea81a5a…`, so that form prints 7/8 forever (residual seat `ResidualC2Rerun`, probe A).
- **class:** a checker that certifies agreement between numbers one author typed. **evidence:** four
  independent seats (`ExecLedgerMutants`, `ReviewL1Accounting`, `CriticCapability`, `CriticZeroControl`)
  scored C1 `3/3 met=True, exit 0` on synthetic evidence: an empty wave (`spawn 0`, no seats), a
  48-seat wave with an empty `w1/`, zero-byte reports, an unreported seat silently dropped from both
  `settled` and `dead`, a role bound to a receipt whose `httpStatus` is 500 with `ok: true`, and a
  wall clock shifted with its accounting artifact and the LOG line. Nothing binds `spawn` to the
  grant's `seats=48`, nothing requires `spawn >= 1`, and no check reads a report's bytes.
  **captured-by:** nothing — the frozen L1 sentence asks for equality, not independence, so the
  contract sentence itself is the gap. **fix:** routed to round 52 with the seats' concrete list;
  the round-51 rule is **not** changed after scoring. C1's verdict is therefore "met as declared,
  certifying agreement between the evidence artifacts, not that the wave ran".
- **class:** a frozen artifact scored by a later-amended instrument. **evidence:** the counter
  frozen at `19a99bd` reads `7/8` at the measured revision (C6 fails on the receipt's nested
  `sources` key); `9d13768` fixes only the lookup, after the data commit. **captured-by:** LOG.md
  already discloses the fix as pre-scoring (`LOG.md`, round-51 bullet 4) and the predicate, the eight
  condition sentences and every counted test are unchanged. **fix:** name the counter's blob sha256
  in the report (below) so a reader scores the bytes that produced the number.
- **class:** concurrent writers on one working tree. **evidence:** between 03:33 and 03:40 the live
  `corpus/SOURCES.md` transiently held a staged `S149` row and an `S160` lead row (both malformed for
  the census), and two seats' mutation writes reached it before being restored byte-identically
  (`ScoutCensusBefore`, `CriticIds`, `CriticHarm`, `SentinelWriteScope`). Every committed claim in
  this round is measured with `git show`, not the worktree, and the registry at the tip is
  byte-identical to its blob. **captured-by:** the round's own seats, which is why every item told
  them to read committed bytes. **fix:** round 52 must give each writing seat its own worktree; a
  lead row belongs outside `## Registry` and a staged row must be normalised before it is ever
  written into the registry file.
