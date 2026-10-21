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

Candidates: 168 C1 claim rows from 29 seats (17 Reverify*, 12 Surface*); 12 C2
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
| S030 | https://html.spec.whatwg.org/multipage/syntax.html#start-tags | 2026-10-21 (LS 20 Oct 2026, sha256 a11dcf17…) | “On void elements, it does not mark the start tag as self-closing but instead is unnecessary and has no effect of any kind.” |
| S031 | https://html.spec.whatwg.org/multipage/parsing.html#parsing-main-inforeign | 2026-10-21 (LS 20 Oct 2026, sha256 04b65bf0…) | “Insert a foreign element for the token, with SVG namespace.” |

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


## Measurement

Measured `5bef55b1464d7ccbff802edab400d138597a621c`, before freeze
`6847479d404d1dd93ecb59f99ff735bd7f010a4a`. Same final runner on both sides,
two identical runs each (`measure-{c1,c2}-{before,after}-v2.json`):
C1 exits1→0, accepted0/17→17/17; 176 selected claims (79HOLD,55STALE,42UNVERIFIABLE).
C2 exits1→0, receipt coverage0/12→12/12; outcomes3clean/5canonical_missing/4not-served404.
The snapshots' original fetch timestamps remain unchanged; re-audits were offline.

Snapshot integrity probe2/11→11/11 (`postfix/snapshot-v2-{before,after}.json`);
expanded relaxation probe3/13→13/13 on the rejected `4d95d2e` vs final
(r22 validator9/13). Canonical selftest82/82 (`postfix/stable-smoke.txt`) and
counter selftest28/28 (`postfix/counter-selftest-final.json`). Corpus contract0; old
canonical matrix32/32. Paths remains exit1, the same three legacy unannotated
targets, but the citation universe expanded: missSet55→69, fourteen newly cited
targets explicitly checked and annotated absent. Old pins unchanged; the new
set-delta warning is a disclosed result, not a source restoration or green gate
(`final-suite.json`).

Residual review: FixC1Additions found no counterexample; FixProbeWitnesses killed
both named guard mutants (12/13, pristine/restored13/13). FixSnapshotReview
found finalUrl metadata tamper and JSON-array handling; `5bef55b1…` fixes both
by checking the redirect chain and metadata shape, with new regression cases.
That last fix is L1 probe-verified, not re-reviewed by a seat. CritMetaRefreshBoundary
and FixCounterCoverage died on Codex capacity, uncredited and not replaced.

## Same-claim recovery — KakeR23 (2026-10-21)

The replacement coordinator inherited the already-pushed implementation through
`5bef55b1464d7ccbff802edab400d138597a621c`, three modified bookkeeping files
and untracked wave-2/final evidence. The original 69-seat build and 64-seat
falsification waves were not dispatched again; dead seats were not replaced.
The six prior residual seats remain author-side evidence. Three bounded
read-only recovery audits cover evidence accounting, measurement/source
consistency and documentation; they are not independent round closure.

Re-executed the same final counters against the frozen before revision and
the pushed implementation revision: C1 exit 1, accepted 0/17 → exit 0,
accepted 17/17; C2 exit 1, accepted 0/12 → exit 0, accepted 12/12.
Full argv/stdout/stderr/exits: `recovery-counts.json` in this round's wave
directory. Existing response bytes and original fetch timestamps were retained;
no fresh property fetch or publication occurred during this recovery.

One recovery verification run (`recovery-verification.json`) exercised the
canonical selftest, counter selftest, snapshot integrity probe, relaxation
probe, corpus-contract and the old canonical matrix; all six exited 0.
The inherited red paths result is retained rather than rerun to confirm it.
Reopened S030/S031 through their primary URLs; the located quotes and the
solidus caveat remain supported. Source census exits 0, with 29→31 rows
(A27→29/C2 unchanged; mined25→27/queued2/rejected2 unchanged).
`recovery-frontier.json` records the commands and the fleet misroot sweep:
only operator scripts and protected driver runtime were present, no owned
seat report was misplaced, and no fleet file was removed.

All inherited implementation/evidence is retained except candidate
interpretations explicitly rejected in this lesson's Gate; those rejected
artifacts also remain preserved as falsification history. No aggregator or
non-author verifier file was edited. No tool was installed by this coordinator.

Recovery accounting correction: `wave-inventory.json` now includes the three
recovery audits (round total 142) and both named residual deaths. Their exact
Codex capacity errors were recovered from the original coordinator's async
notices and preserved in `residual-deaths.json`, not inferred from routing.
RecoveryEvidenceAudit found that ExecRealGeneratorPages' surviving report
had the shortened filename `w2/ExecGeneratorPages.md`; it was moved without
content changes to its registry-declared `w2/ExecRealGeneratorPages.md`.
This was a report-path correction, not a new or replacement seat.

## Recovery audit errata — authoritative current reading

RecoveryDocsAudit found that the corrections to the original Gate candidate
count and source table were made in place after `5e5afb9e…`. Their original
bytes are restored above in this new commit; that does not erase the
intervening preservation defect. This appended register supersedes them:

- Gate candidates: **171** before rejecting three absent anchors, **168**
  admitted initially, then eight added claims: **176** final. The original
  candidate line's 168 describes the admitted subset, not all candidates.
- S030 correct response digest:
  `04b65bf0b4b5f3bb3815999ab499af980fa09b8832f02c1686c544ab8e79a52d`.
  The void-element quote is at the original syntax/start-tags URL.
- S031 correct response digest:
  `a11dcf1768a76e24cdf7e16060f54bcb149c529aa8bcb9297b8d1ab633b26f13`.
  Its quoted SVG insertion sentence is at
  https://html.spec.whatwg.org/multipage/parsing.html#parsing-main-inbody
  (in-body svg start-tag rule), not the foreign-content quote location
  originally printed in the table. The registry's wider in-body/foreign
  scope is unchanged.
- The earlier "fixed above" sentence now means this appended register,
  not permission to rewrite the original table. FixDocsEvidence remains
  preserved as a historical scoped author-side recommendation.
- The routed paths row's bare `final-suite.txt` names the historical
  `.ufo/waves/round-22/final-suite.txt`. Current round-23 paths evidence is
  `.ufo/waves/round-23/final-suite.json` and remains red as reported.
- "Malformed metadata returns a JSON input error" was too broad: the
  demonstrated closure at `5bef55b1…` covered a top-level JSON array.
  RecoveryDocsAudit identified non-string contentType as an additional
  unexercised field-shape gap; its reproduction and disposition are recorded
  separately below, not silently included in the original eleven cases.

### Recovery field-shape disposition and mistake

RecoveryDocsAudit's static contentType concern was reproduced by the added
`content-type-metadata` case: the unchanged `5bef55b1…` producer exits 1
with no JSON error, so the same expanded probe is red (11/12).
A bounded coordinator-implemented check now rejects non-string, non-null
contentType before `served()`; the case returns exit 2 with
`snapshot contentType must be a string or null`, and the probe is green
(12/12). Full outputs: `.ufo/waves/round-23/snapshot-field-before.json`
and `snapshot-field-after.json`. Two zero-spawn executor job-cap refusals
preceded the parent's explicit coordinator-direct steer; no dead seat was
replaced and the round total stays 142.

| Class | Evidence pointer | Captured-by | Fix |
|---|---|---|---|
| incomplete metadata-shape regression | `snapshot-field-before.json`, named case exits 1, not the documented 2 | `residual/FixSnapshotReview.md` field-type concern; initial array-only regression was insufficient | explicit contentType type check; same case requires exit 2 plus the exact JSON diagnostic (`snapshot-field-after.json`) |
| in-place corpus correction | original Gate lines at `5e5afb9e…` versus the intermediate integration; RecoveryDocsAudit | existing QUALITY post-review byte-preservation rule | restored original count/source lines, retained the history defect and appended authoritative errata; no history rewrite or amendment |

The contentType fix does not validate every possible forged metadata field or
authenticate GET observations. The `live-snapshot` registry clarification now
names caught output-I/O and integrity errors as exit 2 and records the exact
targeted probe command. The final report distinguishes the inherited measured
revision from the later committed-tip counter receipts; no timestamp is renewed.
