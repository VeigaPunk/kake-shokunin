# Lesson — round 26 (2026-10-21): re-verify what the lane already cites

## Claims

C1 freshness: re-verify the 32 previously opened external SOURCES rows
(S001–S034 minus own-work S014/S019; S035 excluded as opened in round 25)
against bytes re-fetched this round, and recheck the knowledge statements that
rely on them. Before: 0/32 rows with a round-26 live-source receipt. After is
recorded only from the counter run. Both owned axes tie at legacy 10;
freshness was not worked in round 25. Motivation: MANIFEST rounds[420] closed
round 25 with quality unchanged because "no prior entry re-verified or
superseded". Contract: `.ufo/waves/round-26/contract.json` and
`contract-amendment.json`.

Round-24 C1/C2 remain unadmitted candidate debt; no round-24 assignment, probe
or counter was read, retried, rephrased or rerouted.

## Gate

### Sources re-opened (no new rows)

One public GET per recorded URL (`fetch_sources.py`, 34 fetches for 32 rows,
2026-10-21 15:09–15:10 UTC); S008 first timed out at 60 s and was retried once
by an inline command whose exact code is committed post hoc as
`fetch_retry.py`. Bytes are retained gzip-compressed with sha256 in
`fetched/manifest.json` and `manifest-retry.json`. Each row's ≤25-word located
quote, observed anchor and verdict is in `.ufo/waves/round-26/rechecks/S0NN.json`
(copied unchanged from the row seat reports `w1/RowS0NN.md`). All 32 rows
HOLD; no row needed a superseding S036+ row, and no SOURCES cell changed.

Examples of located quotes (full set in the receipts):

| Row | Access | Quote (verbatim, re-fetched text) | Anchor |
|---|---|---|---|
| S005 | 2026-10-21 | “If you are publishing from a custom GitHub Actions workflow, no CNAME file is created” | Configuring an apex domain, step 4 |
| S013 | 2026-10-21 | “unless you submit your sitemap through Search Console, a sitemap affects only descendants of the parent directory” | Sitemap best practices; footer 2026-07-08 |
| S029 | 2026-10-21 | “When authority is not present, the path cannot begin with two slash characters” | RFC 3986 §3 |
| S034 | 2026-10-21 | “The names within an object SHOULD be unique.” | RFC 8259 §4 |

Byte identity with earlier recorded digests: S028/S033 (RFC 9110 txt), S029,
S030, S031 and S034. Living documents were judged by quote at anchor, never by
sha equality (FetchCritic re-fetched one GitHub release page twenty minutes
later: different sha, same text).

### Statement-level admissions and rejections

25 pair seats judged 276 knowledge statements; seats proposed 22 STALE, L1
admitted 8 and rejected 14 with reasons (`statements.json`):

- Admitted: S003 r20-tail attribution to publish-channels.md:5-14 (false even
  at base cb807bc) and a non-verbatim S003 quote; S010 locator and a dropped
  §8.8.1 condition; S021 cross-domain attribution; S026 “all implicit
  closures”; two S030 “self-closed” label misuses. Each is an EOF block tagged
  `[r26-recheck S0NN STALE]`; no original line changed.
- Rejected: anchor drift in pointers explicitly scoped “at base cb807bc”
  (S001×3, S005, S011, S012, S013) — the QUALITY round-21 coordinate rule
  already maps them; verification-date stamps (S005×2, S020, S021) — a
  historical date is not a false claim; Python 3.15.0→3.15.1 labels (S026,
  S027) — same family, relied-on sentences unchanged (recorded as a note);
  S021 fragment wording — already governed by the r23 correction.
- UNVERIFIABLE: four upload-pages-artifact v3.0.1 statements (no pinned v3.0.1
  bytes); recorded, not counted decided.
- Version note: RFC 3339 is updated by RFC 9557 per the RFC Editor info page
  (PairS032); the relied-on §5.6 grammar is unchanged. No row added.

### Outside spot-check

Pending the separate non-author closure. All seats are author-side.

## Mistakes

| Class | Evidence | Captured-by | Fix / fail-capable witness |
|---|---|---|---|
| survivor | `before/source_text.py` decoded HTML entities twice (HTMLParser convert_charrefs plus html.unescape) and added a `]` spacing rule; w1/RecheckFixtures.md predicted the failures | none — round-26 extractor was new | single decode, no `]` rule; `text_selftest.py` checks synthetic `&amp;lt;` cases; red-before/green-after recorded after execution |
| vacuous | ClaimCritic: GitHub/WHATWG page chrome (“Back to top Help and support…”) would ground HOLD for every row of its family | none: contract allowed any quote in the row's own text | counter `quote_not_row_specific`: a decided quote must not occur in other rows' text outside a declared document group; selftest boilerplate case |
| landing | S008 retry ran as an inline heredoc; no committed code produced `manifest-retry.json` (FetchCritic) | Evidence standard: claimed ≠ re-executed | `fetch_retry.py` committed as a labelled post-hoc copy; the manifest remains the evidence, the file documents the procedure |
| scope | `RowS012.md` written at the fleet root (relative report path) | contract misroot sweep | copied byte-exact into the lane, `cmp` and sha256 recorded (`misroot-RowS012.txt`), fleet copy removed |
| stale-premise | seats labelled base-scoped pointers, historical dates and patch-version labels STALE (14 of 22) | QUALITY round-21 coordinate rule; no rule for dates | adjudication rule recorded in `statements.json`; QUALITY row added |
| attribution (routed, r25) | seat `/tmp` scratch writes (MANIFEST rounds[420]) | lane-only write bound | wave context forbade /tmp; whether any seat still used it is checked in W2, not assumed |

## Measurement

Counting command: `python3 -B .ufo/waves/round-26/measure.py --root . --revision <commit>`.
Results, revisions and no-harm checks are appended only after execution.

## Falsify wave and resume (appended by L1 replacement KakeR26-2, 2026-10-21)

KakeR25's session died (host SIGHUP 13:10:51 -03) while its validated falsify
wave was waiting on the job cap; no W2 seat transcript existed, so W2 had spent
nothing. KakeR26-2 dispatched the same `w2-dispatch.json` payload unchanged
(64 seats: 36 reviewer, 23 critic, 2 mutation-tester, 2 scout, 1 scribe;
spawned on the first try, `w2-dispatch-attempts.json`). Reports: `w2/*.md`.

Adjudication of the falsify findings (`statements.json` `w2Adjudication`):

- New STALE: S001's v3.0.1 attribution (was UNVERIFIABLE; S002 carries it) and
  two S024 scope statements in static-canonical-preflight.md (first base *with
  href*; foreign-content `base` is not S024's element).
- Reclassified as precision notes (tags kept, append-only): the S010 line-1
  locator, the S026 "implicit closures" wording and both S030 "self-closed"
  labels — 4 of the 8 wave-1 admissions did not meet the STALE rule.
- Coverage gap closed: 37 more statement units judged (S024/S025 in
  static-canonical-preflight.md; round-20 correction lines in publish-channels,
  sitemap-orphan-audit, ghp-subpath-spotcheck, speedrun-pipeline — all HOLD).
- Counter hardened (`measure.py`): rows output restored; every fetch of a row
  verified; in-group containment twins; ledger duplicate/outside-population/
  unaccounted-tag findings; selftest 14 → 24 cases. All six surviving mutants of
  w2/MutateCounter.md and six new-rule mutants are killed
  (`verification/counter-mutation-replay.json`).
- Receipt locator offsets drifted after the extractor change; corrected values
  are in `receipt-locator-errata.json` (no verdict depends on them).

### Mistakes (falsify wave)

| Class | Evidence | Captured-by | Fix / fail-capable witness |
|---|---|---|---|
| stale-inflation | 4 of 8 wave-1 STALE admissions were consistent wording or locator shape (w2/Correction3S010, Correction6S026, Correction7S030, Correction8S030) | the STALE rule itself; no counter check | ledger `reclassified`; counter `statement_tags_unaccounted` requires tags == stale + reclassified; selftest `statement_tags_unaccounted` and `reclassified_accounted`, mutant N6 killed |
| coverage | ledger followed `usedBy` cells only; S024/S025 statements and r20 correction lines in four entries were never judged (w2/CounterCritic, w2/UncoveredS024S025, w2/LessonAudit) | none — the counter checks only listed pairs | 37 units judged; `statements_row_outside_population` and `statements_duplicate_pair` guard the ledger's shape; completeness of the citing set is still not machine-checked (open) |
| survivor | `rows` was never assigned in `score()`; the candidate printed `rows: []` with 32 decided (w2/FalsifyS015) | none | assignment restored; selftest asserts 32 row records on `complete_clean`; mutant N1 killed |
| survivor | six counter mutations survived the 14-case selftest (w2/MutateCounter) | mutation testing | 10 new cases; replay kills M01, M02, M04, M05, M06, M10 |
| derived-locator | receipts carry text-view offsets measured on the pre-amendment views (w2/FalsifyS024, S025, S027, S031, S034, S011) | none: offsets are prose | `receipt-locator-errata.json`; not yet fail-capable (offsets are not parsed) |
| scope (L1) | KakeR25 wrote `/tmp/kake-r26-m.json` (counter output, sha256 0632ee9b…); the replacement first cloned to `/tmp`; seats S004, S011, S018, S020, S030 and S006/S007/CounterCritic disclosed transient `/tmp` or `/dev/shm` scratch (deleted) | wave context "never write /tmp" — seats self-reported; ScratchAudit missed the L1 file | scratch moved to `/fast/scratch/hyaku/kake-r26/` and deleted at landing; the L1 file is deleted at landing; future wave contexts name the scratch path |

- Extractor mutation coverage: added `sniff_attributed_html_without_content_type`;
  the `<html` → `<html>` sniff mutant now exits 1 on that case, pristine
  74/74 exit 0 (`verification/extractor-sniff-mutant.json`, `text-selftest-final.json`).
