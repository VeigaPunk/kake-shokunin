# Round 23 — live re-verification and end-to-end canonical preflight

Date: 2026-10-21. Base: `b5d599e19bead54b96f589444e9ec64cdf67c28a` (round-22
non-author spot-check). Freeze commit (contract, populations, counters before
any implementation): `6847479d404d1dd93ecb59f99ff735bd7f010a4a`. L1: the
recovery coordinator reused by Main for this round (`KakeR22Recovery`).

## Claims

- **C1, freshness (lowest owned axis, tied at 10; unchanged last round).** Live
  re-verification of the 16 knowledge entries whose metadata declared them
  historical-not-live-reverified plus the SKILL.md property map (17 units,
  `.ufo/waves/round-23/c1-population.json`). Count:
  `python3 .ufo/waves/round-23/measure_c1.py --root . --revision <commit>`.
- **C2, operability.** First end-to-end canonical preflight over the 12 owned
  surfaces of the property map: committed read-only GET snapshots whose audit
  receipts the counter reproduces with the revision's validator
  (`.ufo/waves/round-23/c2-population.json`). Count:
  `python3 .ufo/waves/round-23/measure_c2.py --root . --revision <commit>`.
  Making the validator able to evaluate real owned pages (body SVG, `<input />`)
  is part of C2's implementation; its own before/after is reported with C2.

Causally separable: C1 receipts and C2 snapshots share no file; each counter
passes or fails without the other. Measured numbers are in §Measurement.

## Gate

Candidates from wave 1: 171 C1 claim rows from 29 seats (17 Reverify*, 12 Surface*); 12 C2
snapshots; validator relaxation; two WHATWG sources; five re-opened round-22 rows.

Admitted:
- C1 claim rows whose anchor exists in the unit at base (exact or whitespace-only
  rewrap, stored as the exact base bytes): 168. Rejected 3 rows whose anchor is not
  in the unit text (`receipts/rejected.json`: fire-journal-codes "three journals
  carry `fire:true`", mirror-pitfalls "plazir27runson…", publish-channels "CNAME
  file pins `ds4cc.com`.") — not paraphrase-matched, by rule.
- S030, S031 (below). Re-opened without change: S021, S023, S024, S025, S026.
- Validator relaxation only together with the base/foreign guards and the
  relaxation probe (11/11).

Rejected:
- The round-23 candidate validator `4d95d2e` as shipped: it reported nine
  body-base attacks clean (`postfix/relaxation-cand.json`).
- Counting a not-served surface as a canonical result: C2 counts reproducible
  receipts; not-served (404) receipts are coverage, reported separately from
  policy outcomes (w1/CritCounterC2, w1/ConnectCapability).
- An all-UNVERIFIABLE C1 receipt as re-verification (w1/CritCounterC1): the
  counter now needs one live-decided claim per unit.
- Editing round-22 frozen evidence to make its replay green at the new tip
  (w1/BoundaryReplayIntegrity, w1/ScribeLessonDraft F1): replay stays pinned to
  `b539cc1`; SKILL.md carries the correction.
- Changing round-22 `measure.py` to pin fixtures (w1/ReviewCounterPins P2): the
  round-22 receipts would no longer be reproducible by the same runner bytes.
  Round-22 replay already pins all 64 fixture digests; the gap is recorded.

### Sources opened this round

| Row | URL | Access | Located quote |
|---|---|---|---|
| S030 | https://html.spec.whatwg.org/multipage/syntax.html#start-tags | 2026-10-21 (LS 20 Oct 2026, sha256 04b65bf0…) | “On void elements, it does not mark the start tag as self-closing but instead is unnecessary and has no effect of any kind.” |
| S031 | https://html.spec.whatwg.org/multipage/parsing.html#parsing-main-inbody | 2026-10-21 (LS 20 Oct 2026, sha256 a11dcf17…) | “Insert a foreign element for the token, with SVG namespace.” |

Both opened by seats (w1/SourceHTMLVoidSyntax, w1/SourceHTMLForeignContent) and
re-fetched by the L1, quotes located in the fetched text. No old row's
status/recheck/used-by changed.

## Routed from the round-22 verifier

| Note | Disposition | Evidence |
|---|---|---|
| 1 inverted "Derived counts" predicate | named correction appended | `corpus/QUALITY.md` §Correction register — round 23; counter probe exits 1 on the c0fd6d5 runner, 0 now |
| 2 misroot files at lane root | moved to `.ufo/waves/round-22/residual/misroot/` (byte-identical, rename) | commit `4e7dd1d` |
| 3 `/tmp` runner paths | `.ufo/waves/round-22/postfix/REPRODUCE.md` with `git show c0fd6d5:` commands; reproduction re-run 2/8 and 3×rejected:false; executor script in w1/ExecReproduceBefore (`all_matched: true`) | `4e7dd1d`, w1 report |
| 4 probe-only fixes and 21 dead w2 items | seat-reviewed: ReviewDotdotSplit (no finding), ReviewHelpSynopsis (P3 fixed: `--help` in synopsis), ReviewFdOwnership (P3 residual: only if `close()` raises before releasing; Linux close releases the fd), ReviewCounterPins (P2 recorded above); 18 of 21 dead items re-run (Attack23, 8 Boundary*, 4 Connect*, 5 Reopen*); ReopenRFC6596/GoogleTroubleshoot/PythonURL were already re-opened by the round-22 verifier | w1 reports |
| 5 paths gate red | carried unchanged; operator-owned restore/retire | `final-suite.txt` |
| 6 SHONEN | unpromoted; C2 is an end-to-end domain task logged in LOG.md (author-side) | LOG round 23 |

## Mistakes

| Class | Evidence pointer | Captured-by | Fix |
|---|---|---|---|
| parser relaxation without adversarial neighbours: turning "unsupported" into "evaluated" opened a false-clean class (body/foreign `<base>`) | `postfix/relaxation-cand.json` (2/11 met, nine attacks clean on `4d95d2e`); w1/FalsifyForeignContent | round-22 QUALITY "resolver neighbours" covered URL branches only | new QUALITY criterion "parser relaxations"; base/head/link guards, element stack, no raw text in foreign content; probe 11/11 now, and it fails on both `4d95d2e` and `b539cc1` (the latter already accepted a body base: 7/11) |
| inverted fail predicate in a quality criterion | round-22 verifier note 1 | none (author wrote criterion and probe in one sitting) | named correction; the fixed reading fails on the c0fd6d5 runner (counter probe exit 1) |
| count accepted an all-absence receipt | w1/CritCounterC1 | none | counter requires one HOLD/STALE claim per unit; `counter_selftest.py` case "C1 all-UNVERIFIABLE receipt rejected" |

## Wave-2 integration and limits

- Wave 1 completed 69/69. Wave 2 dispatched 64; 25 reports survived, 39 seats
  died (no replacement). `w2-deaths.json` retains the exact errors: mostly zai
  429 `type=1302` after five retries, three Codex capacity failures (one after
  thirteen retries, two after five). Role routing settings are not availability
  proof; the observed errors override any configured retry/cascade expectation.
- C1 additions after falsification: eight omitted live/operational claims in
  drift-detection, fleet-registry, ops-automation, vault-properties and the
  property map, plus a correction to the burnerchrome source-path guidance:
  the mapped path is absent, but `/home/vgpnk/Projects/burnerchrome` survives
  (`ee834920…`, title/h1 match the live page, not proved deployment binding).
  Final C1 has 176 claim rows over the same 17 frozen units. An h1 literal in
  drift-detection:c5 was corrected; its HOLD verdict did not change.
- `w2/SentinelSnapshotV2` P1/P2: no-follow, regular single-link output leaves,
  opened relative to an output directory fd; re-audit verifies original
  byte length and digest and rejects a missing served body; malformed metadata
  returns a JSON input error; blocked redirects preserve the last HTTP URL.
- `w2/MutateGuards`: a foreign end-tag mismatch mutant survived both detectors.
  Added a direct stray-end witness and a foreign canonical-link witness to the
  relaxation probe (now 13 cases), and the mismatch witness to selftest.
- `w2/MutateCounterSelftest`: the initial seven-case selftest killed 13/71
  mutants; 58 survived. Added targeted regression inputs for dates, fields,
  identity, corrections, reasons, URL, digest, byte length and HTTP response
  status. No exhaustive mutation-kill claim is made.
- C1's counter validates a receipt's structure/anchors/correction placement,
  not the truth of an asserted GET or HOLD. A forged self-consistent receipt
  can pass; the live observations in seat reports and non-author spot-check
  carry that authority, not the number 17/17 (`w2/CritCounterTightening`,
  `ReviewLessonGate`, `ReviewQualityCriteria`).
- `w2/CritRelaxationProbe` meta-refresh disagreement: rejected as a canonical
  policy counterexample. `meta[http-equiv=refresh]` does not alter the declared
  canonical link or its base; HTTP/HTML redirects and navigation/readiness are
  outside the frozen claim. A clean canonical receipt must not be used as
  permission to publish a redirecting page (QUALITY and knowledge limits).
- Source corrections: the first Gate table had S030/S031 response digests
  cross-assigned; fixed above (`w2/ReopenS030`). A separate trailing solidus
  has no effect on a void start tag; a slash immediately following an unquoted
  attribute is part of that value, not that syntax. This caveat is recorded
  with S030 rather than changing its immutable registry teaching cell.
