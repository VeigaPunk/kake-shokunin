# CitingSweep07 — blind citing-set census: ghp-served-set.md + ghp-subpath-spotcheck.md

Seat: KakeR27.CitingSweep07 (read-only leaf). Milestone r27-full-citing-set; judged axis freshness.
Scope: exactly `corpus/knowledge/ghp-served-set.md` (95 lines) and
`corpus/knowledge/ghp-subpath-spotcheck.md` (111 lines). No source/live-site evaluation, no
adjudication of truth, no edits outside this report, no installs or package transactions.

## Inputs and identity

| input | sha256 |
|---|---|
| served-set working tree | 405b85875268f2debc6d9a209bb9e4f87f45910da5e7e2ba384dcb9c9911a1e7 |
| spotcheck working tree | a35c323eccdf79f290e086032623e76e749413a1787add1ea81d4b41bb538e84 |
| served-set @ base 83528f7c | same 405b8587… (git show hash match) |
| spotcheck @ base 83528f7c | same a35c323e… (git show hash match) |
| frozen/expected.json pin | both target files sha256-match true |
| contract.json | 6d2d7f51371650c2d7535c401ead613355135d18b44762c41f385d05ee7582da |
| count_c1.py | a1e46d19b438fc254689dc42f474664864b7fd7fecc6a992ad70f5d5da44a14c |
| c1-before.json | af55d0a4bb1aa9b21bc2ce026035beaf21e523458661252f8a520008f2ec6e3c |
| c2-oracle.json | 1d038205473180c7cb57895c2d480a8b52debe3bf08ab0a2f58ca7b1f67bc7dd |
| frozen/ledger.json | c2026376832ad4e4114d1bc19abeec4fcbdbd0fea3dbb102ab8a5c2eb18c95ce |
| frozen/population.json | 16330e1effd5ee52665f8f31738e9423c6ec387e5d4a1404c5bcc35f69d01b03 |
| r26 statements.json | c2026376… (byte-identical to frozen ledger) |
| r26 population.json | 16330e1e… (byte-identical to frozen population) |

`git diff base..be375d90` for both files is empty; `git status --porcelain` for both is empty.
HEAD = be375d90afc6fc7aca369ab3cf5247bf460aeed2.

## A. Manual census — ghp-served-set.md (95 lines, 31 `\bS\d{3,}\b` tokens, 6 distinct rows)

| line | token(s) | scope / kind | adjudication anchor in file |
|---|---|---|---|
| 1 | S001 S002 S003 S004 S006 S008 | provenance header `source:`; grouped six-row registry list; only URL shown is S001's pinned `upload-pages-artifact@7b1f4a7 action.yml §Archive artifact` | entry scope; all six pairs carried |
| 21 | S001 | source-check bullet: v4.0.0 excludes `.[^/]*` in all three OS steps; current commit conditional on `include-hidden-files` | r26 `stale:1`; correction L93 |
| 25 | S002 | source-check bullet: v4.0.0 release “Potentially breaking change: hidden files … not be included”; v5.0.0 announces input | r26 clean |
| 28 | S003 | source-check bullet: root-or-`/docs` quote | r26 `stale:2`; corrections L85, L87 |
| 29 | S004 | inline inside S003 bullet: “S004 steps 4-5 upload static files and deploy the artifact” | r26 clean |
| 30 | S006 | inline inside S003 bullet: Jekyll defaults skip list; scoped at L32-33 “not every workflow uses that build path” | r26 clean |
| 34 | S008 | source-check bullet: tar anchoring quote; “GNU tar 1.35” label | label withdrawn at L73 |
| 73 | S008 | post-review erratum: version label only; manual commit cfdb891…; anchors 8478–8617 / 8478–8603 retained | correction scope |
| 83 | S001 S002 S003 S004 S006 S008 (S008 twice) | round-26 recheck paragraph, grouped: “Rows S001, S002, S003, S004, S006 and S008 were re-fetched by one public GET each”; “S008 via `manifest-retry.json`” | r26 HOLD-at-anchor record |
| 85 | S003 ×2 | `[r26-recheck S003 STALE]` tag + “S003's own text” (branch-vs-Actions); scope = r20-correction sentence L17-18 | correction present |
| 87 | S003 ×2 | `[r26-recheck S003 STALE]` tag + “S003 bullet at lines 28-29” non-verbatim-quote correction | correction present |
| 89 | S001 | UNVERIFIABLE block: “S001 pins only v4.0.0 … and main”; no v3.0.1 bytes retained | UNVERIFIABLE recorded (L94 narrows four→three) |
| 93 | S001 ×3, S002 ×2 | `[r26-recheck S001 STALE]` tag + “to S001, but S001 pins only…” + S002 reattribution (“S002's” / “an S002 claim”) | correction present |
| 95 | S008 | EOF rejection note: “S008 via `manifest-retry.json`” names the round's retry, “not a source of this entry” | non-source metadata, same pair |

Non-token/alternate forms in this file:
- L83 `rechecks/S0NN.json` — receipt glob for the six recheck receipts; `S0NN` has no digits, so it is
  not a source-id token and adds no pair. Same placeholder role as r26 receipt naming.
- Row-bearing artifact filenames not lexed by `\bS\d{3,}\b` because the id is embedded after a word
  character: L85 `w1/PairS003GhpServedSet.md`, L89 `w1/PairS001GhpServedSet.md`,
  L93 `w2/Rejection02S001.md`. Each names a row already cited as a bare token in this file.
- No ranges, no slash-alternates (`S001/S002`), no 1–2 digit `S` refs (grep `\b[Ss][0-9]{1,2}\b` → NONE).
- No S-tokens occur in the L3 recheck loop or the L44-50 fenced tar repro.

## B. Manual census — ghp-subpath-spotcheck.md (111 lines, 10 tokens, 3 distinct rows)

| line | token(s) | scope / kind | adjudication anchor in file |
|---|---|---|---|
| 1 | S001 S005 S019 | provenance header: “Registry-backed only for the round-20 correction: S001, S005 (corpus/SOURCES.md). S019 is metadata authority, not platform authority.” | S001/S005 pairs carried; S019 outside population |
| 2 | S019 | provenance line: “S019 in corpus/SOURCES.md governs metadata only” | outside population; metadata scope |
| 95 | S001 S005 | round-20 correction (base `cb807bc` coordinate): CNAME not in exclusion set; “whether Actions serves /CNAME is an unverified prediction … — S001, S005” | both pairs carried |
| 111 | S001 ×2, S005 ×2 | EOF round-26 recheck: “The round-20 correction lines in this entry cite S001 and S005 (line 95)”; “S001's … exclusions”; “S005 still says the CNAME file is ignored under a custom Actions workflow” | carried; `rechecks/S0NN.json` placeholder |
| 95 | (self-pointer, no S-id) | L95 cites this file's own base coordinate `:83` | — |

Non-token/alternate forms: L111 `S0NN.json` receipt glob (no digits; no pair). No ranges, no
slash-alternates, no 1–2 digit `S` refs. `S014` and `S035` do not occur anywhere in either target
file (grep `S014|S035` → NONE); they generate no outside-population reference in this scope.

## C. Pair roll-up and additional obligations

- In-population pairs from these two files: 6 (served-set: S001 S002 S003 S004 S006 S008) +
  2 (spotcheck: S001 S005) = **8**. All 8 are inside the frozen 57 and inside the 41-pair carried
  ledger; **0 additional inherited32-row pairs** are cited by these files.
- Therefore the denominator contribution of this scope stays 8 and is neither enlarged nor shrunk;
  nothing here is dismissed as “metadata” — every in-pop token was resolved to a pair.
- Outside-population reference recorded separately: **(S019, corpus/knowledge/ghp-subpath-spotcheck.md)**
  at lines 1-2, scoped metadata-authority only. Population is S001–S034 minus own-work S014/S019
  (SOURCES.md:79: “the 32 previously opened external rows (S001–S034 minus own-work S014/S019)”);
  S014, S019, S035 are absent from `frozen/population.json` (32 rows, checked). S019 is not in r26
  statements.json either. Conditional note for monotonicity: if a later population admits S019,
  this pair becomes an obligation; under the frozen population it is correctly excluded.
- S019's in-file scope matches registry row S019 (“Local provenance-field and lesson-heading census
  only; no verification of historical platform claims”, SOURCES.md:27); no mis-scoping found.

## D. Parser comparison (performed after the manual census above)

Frozen parser (count_c1.py): `LITERAL = \bS(\d{3,})\b`; `RANGE = \bS(\d{3,})\s*(?:[-–—]|\.\.|to|through)\s*S(\d{3,})\b`;
ids retained only if present in the 32-row r26 population; whole blob read (code/quotes included).
Independent reimplementation of those two regexes over `git show 83528f7:<file>` reproduced the
manual census line-for-line: served-set token counts {S001:7, S002:5, S003:7, S004:3, S006:3, S008:6}
= 31; spotcheck {S001:4, S005:4, S019:2} = 10; range matches = 0 in both. Population intersection =
the same 6 and 2 pairs. No valid pair in these files is dropped by the parser.

Cross-checks against the frozen measurement:
- `c1-before.json`: population 32, citingPairs 57, decided 41, r26CarriedPairs 41, newDecided 0,
  missing 16; 41 + 16 = 57, so these two files' 8 pairs are all in the decided 41 and none in the 16.
- The 16 missing set equals `c2-oracle.json.expectedPairs` exactly (set equality both directions;
  16/16; no target-file pair in it). Missing files: static-canonical-preflight (9 pairs),
  sitemap-orphan-audit (2), publish-channels (2), crawl-scope-per-host (1), ghp-custom-domain (1),
  ghp-etag-anatomy (1).
- `frozen/ledger.json` is byte-identical to r26 `statements.json` (sha c2026376…, 41 pairs); its
  target-file pairs are exactly these 8 (6 served-set + 2 spotcheck), so carried status is explicit.

Observed parser blind spots, none operative in this scope:
1. Row ids embedded in filenames (`PairS003GhpServedSet.md`, `Rejection02S001.md`) fail `\bS` and are
   not counted; here every such row also appears as a bare token, so the pair set is unchanged.
2. `S0NN` receipt placeholders are (correctly) not tokens; they encode no row.
3. The parser would count S-tokens inside quotes/code; none of this entry's quoted text introduces a
   row id absent from its own prose.

## E. Freshness verdict for this scope

- Bytes are stable: identical at base 83528f7, at declarations be375d90, and in the working tree;
  frozen/expected.json pins match. The c1-before measurement therefore applies to current bytes.
- All 8 pairs have durable r26 adjudication carried explicitly (statements.json entries for each;
  served-set S001 stale:1 and S003 stale:2 have corrections tagged `[r26-recheck S00N STALE]` at
  L93/L85/L87; the v3.0.1 statement block is UNVERIFIABLE at L89, narrowed four→three at L94;
  spotcheck S001/S005 entries were added by w2 adjudication).
- No new STALE verdict is asserted by this seat, so the r27 “[r27-recheck S00N STALE]” appended-
  correction rule is not triggered; r26 rows are carried, not relabelled.
- Verdict: **closed for these two files — 0 new obligations, 0 dropped pairs, 8/8 carried.** This is
  a citing-set completeness/freshness finding only; it does not certify statement truth, and the
  parent judges the carried verdicts independently.

## E2. Located support (verbatim, each ≤25 words)

- served-set L1: `source: S001, S002, S003, S004, S006, S008 (corpus/SOURCES.md)` — six-row provenance group.
- served-set L83: “Rows S001, S002, S003, S004, S006 and S008 were re-fetched by one public GET each”.
- served-set L95: “name the round's retry, not a source of this entry” (on “S008 via `manifest-retry.json`”).
- spotcheck L1: “Registry-backed only for the round-20 correction: S001, S005 (corpus/SOURCES.md). S019 is
  metadata authority, not platform authority.”
- spotcheck L95: “whether Actions serves /CNAME is an unverified prediction requiring an operator-authorized
  free read — S001, S005”.
- spotcheck L111: “The round-20 correction lines in this entry cite S001 and S005 (line 95).”
- SOURCES.md:79: “the 32 previously opened external rows (S001–S034 minus own-work S014/S019)”.

## F. Uncertainties

1. `S0NN` placeholders (L83 served-set, L111 spotcheck) are receipt-name patterns, not ids; read as
   such, no pair effect. A reader treating them as a range S001–S008 would still add no new pair here.
2. Filename-embedded row ids are outside the frozen literal definition; if L1 elects broader lexing,
   these files' pair set is unchanged (same rows), but other files could grow.
3. S019 is an outside-population reference, not a C1 obligation under the frozen 32-row population;
   it becomes one only if the population definition changes.
4. served-set L1 groups six rows under one pinned URL (S001's action.yml); S002/S003/S004/S006/S008
   URLs live only in their bullets. This is a provenance-pointer quality observation, not a missing
   citing pair.
5. I did not execute `count_c1.py` or any gate/build/lint/test (L1 runs after integration); parser
   behavior was compared by reading the frozen source and reimplementing its two regexes verbatim over
   base blobs. No network, no live-site evaluation, no installs/updates were performed.

## Evidence paths (read-only)

- corpus/knowledge/ghp-served-set.md; corpus/knowledge/ghp-subpath-spotcheck.md
- .ufo/waves/round-27/{contract.json,count_c1.py,c1-before.json,c2-oracle.json,frozen/{population,ledger,expected}.json}
- .ufo/waves/round-26/{population.json,statements.json}
- corpus/SOURCES.md rows 22 (S014), 27 (S019), 43 (S035), 79 (population definition)

report: .ufo/waves/round-27/w1/CitingSweep07.md
