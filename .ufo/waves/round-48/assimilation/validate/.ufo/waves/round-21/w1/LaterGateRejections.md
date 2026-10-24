# Later gate rejections — rounds 8, 9, 10, 12 (scout)

Role: scout. Scope: read rounds 8, 9, 10, 12 lessons for actual reject evidence
and verifier references; advise reconstruction. No edits outside this report.
Snapshot: 2026-10-20, base `5009ecaa1cce10b895617a585ddd3f7c7c923a84`. The
worktree was moving while this was read (three of the four lessons had a
round-21 Gate appended mid-read); line numbers for appended sections are the
snapshot's and may shift. No live state, domain, or `/tmp` re-verification was
run. All statements are observations from local files unless marked
`[INFERENCE]`.

## Bottom line

- **No original Gate existed for any of these four rounds.** `git log -S
  "## Gate"` is empty for all four lesson paths, and the base texts carry no
  candidate/admit/reject ledger. Any Gate content is retrospective.
- **Documented refutations exist for rounds 9, 10, and 12.** They are
  corrections/refutations inside the lesson narrative, not gate decisions.
  Round 8 records no explicit rejected candidate; its rot hypothesis was tested
  and contradicted (`zero rot`), which is a finding, not a gate rejection.
- **No round has an independent non-author spot-check of its own findings.**
  Round 8 does have a non-author *SKILL.md executability* cold run
  (`Box3Kake`), graded provisional, and round 10 has a non-author *corpus*
  audit; neither reviewed the round's admissions. Round 9's aggregator verdict
  explicitly disclaims non-author status for kake's corpus artifacts.
- **All session evidence is gone:** `/tmp/kake-r10`, `/tmp/kake-r12`, and the
  entire `~/Projects/webzites` tree (including `reports/`) are absent now.
  Gate text must say historical-not-live-reverified and name the restore-or-
  retire owner; it must not imply replay is possible from the cited `/tmp`
  paths.
- **Two appended Gates contain stale round-21 contract statements:** they say
  S019 is absent under `corpus/`, but S019 now exists at
  `corpus/SOURCES.md:27`, and `corpus/lessons/round-21.md` now exists in the
  worktree. These statements should be reconciled before the C2 gate runs.

## Snapshot table

| Round | Base lines / sha256 (`5009eca`) | Gate at base | Worktree Gate (snapshot) | Documented refutations in lesson | Non-author verifier evidence | Outside spot-check |
|---|---|---|---|---:|---|---|
| 8 | 58 / `13fb8c89…a27407` | none | line 60, `## Gate — round-21 retrospective reconstruction`, +28/−0 | none labelled; rot contradicted by data | `Box3Kake` cold run (aggregator-owned, provisional) | not recorded for the audit |
| 9 | 66 / `b613ce95…39846e2` (matches `.ufo/round-20/measured-corpus-inputs.json:94`) | none | line 68, `## Gate`, +132/−0 | false premise; 74→75; 6h rescope; churn-vs-claims | 10 lane L2 probes; aggregator verdict (disclaims non-author) | not recorded |
| 10 | 62 / `1814f909…d796863` | none | line 64, `## Gate — round-21 retrospective reconstruction`, +31/−0 | naive diff; r5 window; xsnapshot scope; citation drift | labrat/reviewer/critic/sentinel (same-round L2) | partial: round-6 aggregator audit |
| 12 | 62 / `935485d2…0f5c67` | none | line 64, `## Gate`, +33/−0 | F1 guard; keeper myth 1; keeper myth 2; 2 cites + 2 counts | executor/critic re-runs, sentinel, revenger (same-round L2) | not recorded |

Base sha256 for round 9 was independently confirmed against
`.ufo/round-20/measured-corpus-inputs.json:94`. The other three base digests
are computed from `git show 5009eca:<path> | sha256sum` for this report only.

## Round 8 — `corpus/lessons/round-8.md`

### Documented outcomes and their support

- **Two-enumeration kimi audit** (live-index link sweep + canonical sitemap
  parity), base lines 10–15. Landed per `LOG.md:12`; the durable record is
  `corpus/knowledge/kimi-subpath-audit.md`. Retrospective outcome:
  **admitted with qualification** (self-recorded closure; no independent
  recheck).
- **74 of 93 canonical paths missing, all post-vintage, zero rot**, base lines
  19–25. This is a documented finding that contradicts the rot hypothesis. The
  count was later superseded by **75** (`kimi-subpath-audit.md:39–44`,
  `LOG.md:13`). The worktree Gate handles the supersession correctly but cites
  `corpus/knowledge/free-read-verbs.md:211`, which does not carry the 75; the
  figure is at `free-read-verbs.md:215` and `:465`.
- **`dir/` hrefs 404 while `*/index.html` serves 200**, base lines 26–29. The
  Gate cites `kimi-subpath-audit.md:45–51`; verified.
- **"44 same-origin links, 0 real non-200" across 10 live rows**, base lines
  31–33. The knowledge table lists 33 links across 9 rows
  (`kimi-subpath-audit.md:58–68`); the ds4cc row is not in that table, so 44
  is not reconciled in-record. The Gate's qualification is correct; its table
  anchor `:53–65` should be `:58–68`.
- **Client-side `PROPERTIES[]` blind spot**, base lines 35–37; method limit at
  `kimi-subpath-audit.md:19` (the Gate cites `:14–17,63–64`; `:19` is the
  decisive line).
- **`update` vs `recreate` transfer surfaces**, base lines 49–55. Unverified in
  round 21: `~/Projects/webzites/scripts/kimi-surface.mjs` no longer exists.
- **Vintage from max embedded DOM date**, base lines 56–58. The method is at
  `kimi-subpath-audit.md:89–90`, not `:85–86` as the Gate cites.

### Reject evidence

None explicitly labelled. The rot hypothesis was tested and contradicted by
the miss classification (zero pre-vintage misses), but the lesson does not
record a candidate that was rejected. The worktree Gate's "Rejected
candidates: not recorded" is defensible. Do not rewrite the rot result as a
gate rejection; if mentioned at all, label it "tested and contradicted, not a
recorded gate decision".

### Verifier references

- `Box3Kake`, non-author cold run by aggregator-lane L2 `labrat`
  (`corpus/lessons/round-8-aggregator-box3-coldrun.md:1–3`, verdict `[x]` at
  `:54–58`). The main-repo dispatch report grades it **`[x] provisional`**
  (`shokunin:.ufo/reports/round-8/aggregator.md:39`) and notes no `SHONEN.md`
  box-3 line yet names a resolvable non-author verifier (`:22`).
- The round-9 aggregator verdict restates why it stays provisional:
  the battery ran against a dirty `2a5502c` tree and no committed
  gate/self-test reran it at `4c9a985`
  (`corpus/lessons/round-9-aggregator-corpus-verdict.md:9`).
- Conflict to preserve honestly: the Box3 lesson's own amendment argues "no
  verdict is provisional" (`round-8-aggregator-box3-coldrun.md:96`), while the
  later round-9 verdict says the decisive claims remain provisional. The later
  non-author verdict controls for reconstruction purposes; do not upgrade the
  cold run to definitive.
- Scope: the cold run exercised `SKILL.md` commands; it did not review the kimi
  audit findings.

### Advice for the appended Gate

1. The sentence "This seat found no independent non-author verifier record for
   the round-8 kimi audit" is true but incomplete. Add one scope-limited line:
   the only non-author record is the provisional `Box3Kake` executability cold
   run (aggregator-owned), not a review of this audit.
2. Reconcile the metadata line at Gate line 68. It says the S019 contract text
   is not present under `corpus/`; `corpus/SOURCES.md:27` now carries S019 and
   knowledge entries already cite it (e.g. `vault-properties.md:1`). This is a
   new line, so correcting it does not disturb historical bytes.
3. The round-21 lesson statement (Gate line 69) is qualified "at read time" but
   the file now exists; state current existence or keep the qualifier explicit.
4. Fix the three anchors above (`:211`→`:215`/`:465`; `:85–86`→`:89–90`;
   table `:53–65`→`:55–69`). The errata anchor `kimi-subpath-audit.md:39–43`
   is essentially correct (errata spans 39–44).

## Round 9 — `corpus/lessons/round-9.md`

### Documented outcomes and their support

- **Publish-queue readiness ledger** (PQ-1..PQ-13), base lines 10–13; landed
  `corpus/knowledge/publish-queue.md`; `LOG.md:13`. Retrospective outcome:
  **admitted with qualification**; the file now carries later addenda (r13,
  r16) and is not a round-9 snapshot.
- **Vault link surface is a static `const PROPERTIES = [...]` literal**, base
  lines 14–15. This is the lesson's explicit **false-premise refutation** of
  the README residual. Durable: `corpus/knowledge/vault-properties.md:5–9`.
- **3 of 10 live-claimed links dead; `lucario` absent; snapshot matches
  literal**, base lines 17–28. Durable: `vault-properties.md:34–44`.
  Historical 2026-09-28 GETs, not rechecked.
- **`sourceDir:null` hard blocker + extraction recipes**, base lines 29–34.
  Durable: `vault-properties.md:49–68`. All code line pins point into
  `~/Projects/webzites/scripts/kimi-surface.mjs`, now absent.
- **Platform shifts: `sdk-seed.js` +157B, dual-host website-id
  `1a0acf59…`**, base lines 35–39. Durable: `vault-properties.md:70–84`,
  `publish-queue.md:34`.
- **Citation review**, base lines 40–43: "6h cadence" is the timer's, not the
  file's (`ops-automation.md:34–38`); "74 missing paths" is 75 in-repo
  (`kimi-subpath-audit.md:39–44`); `webzites` is not on PATH. The reviewer is
  not named and is not recorded as independent.
- **25 unpushed source commits**, base lines 44–46. Only the plazir-15 five are
  corroborated durably (`publish-queue.md` PQ-14); ds4cc +20 and charter −2 are
  unverified in-record.
- **Fleet state 12/5/1**, base lines 47–50. Unverified now: the probe state and
  `r9-stale-markers.md` are gone.
- **Bound-chat truth; plazir15 ambiguous; lease unresolved**, base lines
  51–66. `publish-queue.md:32` (PQ-4) records the binding as **UNRESOLVED** —
  a documented withheld/unverified outcome, correctly not admitted. The CDP-9222
  lease remains an open boundary, "reported, not absorbed".

### Reject evidence

The worktree Gate currently says "Rejected candidates: not recorded." That is
too strong: the lesson documents a false premise and three corrections.

- **Rejected premise:** "JS-rendered link surfaces need rendered DOM" — base
  lines 14–15 ("false premise"), evidence `vault-properties.md:5–9`.
- **Corrected count:** 74 → 75 canonical misses — base lines 41–42,
  `kimi-subpath-audit.md:39–44`.
- **Rescoped cadence:** the 6h cadence belongs to the timer, not the file —
  base lines 40–41, `ops-automation.md:34–38`.
- **Rejected explanation:** vault drift is upstream claims vs live fleet state,
  not page churn — base lines 27–28.

Recommend a "Documented refutations/corrections (not recorded gate
rejections)" list with these four lines and their anchors. Keep "no gate
rejection decision was recorded" as a separate statement.

### Verifier references

- Same-round: 10 delegated read-only L2 probes (base lines 3–7). One report
  pointer is already annotated absent in the lesson (`r9-publish-queue.md`,
  r18 re-census). With `~/Projects/webzites` now gone, all four report pointers
  and the fleet dedupe report are absent.
- External: `corpus/lessons/round-9-aggregator-corpus-verdict.md` (11 lines)
  reproduces the main-repo verdict at kake HEAD `a209441`, 2026-09-29, **not
  conformant — rules 1, 3, 4, 5, 6, 8, 9** (`:8`). The main-repo source states:
  "This is an aggregator-lane review of kake's own corpus; the reviewer is not
  non-author for kake's corpus artifacts" (`shokunin:.ufo/waves/round-9/seats/
  verdict-kake.md`, attribution section). It is a rule-conformance review, not
  a spot-check of round-9 findings; the Gate already says this correctly.
- Additional non-author evidence not cited by the Gate:
  `corpus/lessons/round-6-aggregator-audit.md` (aggregator L1 non-author,
  scout lane, 2026-09-28, HEAD `dd4eabf`) re-executed the PQ count (13, pass),
  could not verify 75-of-93 (live GETs prohibited), and flagged the `/tmp`
  pointer defect. Scope it as corpus conformance, not round-9 admission
  review.

### Advice for the appended Gate

1. Add the documented refutations list above.
2. Reconcile the contract block: it says no S019 row exists and SOURCES ends at
   S018; S019 is now at `corpus/SOURCES.md:27`. The round-21 lesson also exists
   now. Both statements are new lines, so update them; keep the read-time
   qualifier only where historically accurate.
3. Replace the two-absent/two-unknown evidence note with the verified fact:
   the entire `~/Projects/webzites` tree is absent, so all four report pointers
   are gone. Operator restore-or-retire covers all four, not two.
4. Do not cite the aggregator verdict as an outside spot-check; the Gate is
   already correct here. Keep the same-round L2 seats explicitly non-independent.

## Round 10 — `corpus/lessons/round-10.md`

### Documented reject evidence (strongest of the four)

- **Naive consecutive-row history diff** — base lines 19–22. Rejected by
  measurement: 42 events / 40 phantom; spot `total:1` rows diffed against fleet
  sweeps fabricate clear/re-enter pairs. Correct durable rule:
  `corpus/knowledge/probe-delta-alerting.md`.
- **Round-5 veigapunk-page transition window** — base lines 25–30. Rejected:
  the 03:32:06 → 04:14:50 pair are the endpoints of a 42.73h coverage hole;
  the 04:14:50 → 09-22T22:58 pair has identical `violated[]` sets. Corrected
  in `corpus/knowledge/ops-automation.md:43–47`.
- **"xsnapshot-app every run since 09-21"** — base lines 42–45. Narrowed to
  constant on full sweeps since 2026-09-21T01:34:20Z. This is a documented
  correction; the Gate currently folds it under admitted-with-qualification.
  Either class is defensible if labelled.
- **Citation drift** — base lines 37–41: `vault-properties.md:60`
  `:891-894`→`:903`; round-9 lesson `:339`→`:342`; SKILL.md cwd-relative
  invocations made absolute. Corrections, not gate rejections.

### Verifier references

- Same-round L2: labrat (naive 42/40 replication; detector reproduction),
  reviewer, critic (falsifiers), sentinel ("reproduces all four
  ops-automation.md r5 truths"), planner agreement — base lines 17, 25–30.
  All lane-dispatched; `/tmp/kake-r10` is absent (verified).
- External: `corpus/lessons/round-6-aggregator-audit.md` (aggregator L1
  non-author, scout lane, 2026-09-28, HEAD `dd4eabf`). It re-executed the
  detector (`rows:76`, `6 events`, `0 phantom`), the naive total (42; the
  40-phantom split is `[INFERENCE]` there), exit codes 0/2/64, and the r5
  correction (pass). It also flagged the `/tmp/kake-r10/*` pointer defect
  (`:76–80`, `:94–97`, `:130`). The Gate's "partial outside spot-check" is
  accurate; the audit did not review admissions and its overall verdict was
  "not conformant".

### Advice for the appended Gate

1. Fix two anchors:
   - `corpus/knowledge/freshness-sweep.md:32-34` → the 60/60 retirement is at
     `:36-38`.
   - `corpus/knowledge/probe-delta-alerting.md:88-91` → the merged-row caveat
     is at `:92-97`.
   All other load-bearing anchors verified: `SKILL.md:203-206`, `:224`;
   `ops-automation.md:43-47`, `:115-119`; `README.md:72-75`;
   `.ufo/round-20/resume/paths-before.txt:55`; round-6 audit lines.
2. Keep the round-6 audit as the only outside evidence and keep its scope:
   corpus conformance plus claim re-execution, not admission review.
3. Consider listing the xsnapshot narrowing and citation fixes under
   "documented corrections" for format symmetry; they are already supported
   in the admitted rows, so this is optional [INFERENCE].

## Round 12 — `corpus/lessons/round-12.md`

### Documented reject evidence

- **Myth 1: "the fleet is already instrumented" / daily keeper tick** — base
  lines 18–22. Refuted by the systemd read: loaded, disabled, inactive, zero
  journal entries; logs frozen at the 09-21 mint. Durable:
  `corpus/knowledge/keeper-timer-inert.md:3–16`.
- **Myth 2: "the keeper will re-pin the charter-ghp marker"** — base lines
  25–33. Refuted by the critic's config-lag analysis: the scribe writes the
  marker; no webzites code writes `fleet.config.json`; the scribe push leg is
  failing. Durable: `keeper-timer-inert.md:83–109`; `publish-queue.md:36`.
- **r11 F1 guard proposal** — base lines 40–46. Refuted on the
  `probe <id> --all` edge; corrected one-line patch replica-verified (18 rows
  preserved, merged `total:18`, `node --check` clean), filed as
  `corpus/handoffs/cmdProbe-merge-fix.md`, not shipped. Durable:
  `free-read-verbs.md:425–434`; handoff `:24–73`.
- **Two wrong citations + two count errors caught pre-landing** —
  `SCORECARD.md:95` (round-12 row). The Gate lists this correctly.

### Verifier references

- Same-round L2: executor and critic re-ran the verbs with independent guard
  pairs, same result (base lines 11–13; `free-read-verbs.md:417–423`);
  sentinel independently re-ran the 31-file set compare; revenger replica and
  reviewer citation check. All are lane-dispatched seats, not independent
  non-author review. `/tmp/kake-r12` is absent (verified); the durable handoff
  and knowledge append remain.
- No external non-author artifact was found for round 12.

### Advice for the appended Gate

1. Fix the push-leg anchor: `corpus/knowledge/publish-queue.md:32` is PQ-6;
   the failing push leg is PQ-12 at `:36`, also `keeper-timer-inert.md:114-116`.
2. Keep C1's "re-run by executor + critic" explicitly labelled same-round L2;
   the Gate already does this.
3. All other anchors verified: `free-read-verbs.md:338-348`, `:362-406`,
   `:417-423`, `:425-434`; `keeper-timer-inert.md:3-16`, `:83-109`;
   `README.md:34`; `cmdProbe-merge-fix.md:24-73`; `SCORECARD.md:95`.

## Cross-cutting reconstruction rules

1. **Separate decision records from documented refutations.** None of these
   rounds recorded an admission/rejection decision. A Gate may say
   "retrospective classification of outcomes supported by the lesson text" and
   may list documented refutations. It must not say the round "admitted" or
   "rejected" a candidate as an original act. The round-21 lesson states the
   same rule: "Missing rejection records stay missing; no retrospective round
   admission is manufactured."
2. **Never promote a self-dispatched seat.** `labrat`, `reviewer`, `critic`,
   `sentinel`, `revenger`, `executor`, `planner`, `scribe` are same-round L2
   seats dispatched by the lane. Use "same-round L2 evidence", not
   "independent" or "non-author". The only cross-lane non-author artifacts
   found are the aggregator-owned Box3 cold run (round 8, provisional,
   SKILL.md scope) and the aggregator audits/verdicts (corpus scope; the
   round-9 verdict disclaims non-author status for kake's corpus artifacts).
3. **Contract statements must match the current tree.** S019 exists at
   `corpus/SOURCES.md:27`; `corpus/lessons/round-21.md` exists in the worktree.
   Round-8 Gate line 68 and round-9 Gate lines 187–190 assert absence. Those
   are new lines, not historical bytes, and should be reconciled before the
   corpus-contract gate evaluates them. Round-10/12 use a read-time qualifier
   and are acceptable but would be clearer with a current-state note.
4. **Gate heading form is inconsistent:** rounds 8 and 10 use
   `## Gate — round-21 retrospective reconstruction`; rounds 9 and 12 use
   `## Gate`. Canonical CORPUS.md says a `## Gate` section; round-20 uses both
   forms. Decide the detector's rule (exact `^## Gate$` vs `^## Gate`
   prefix) before the gate runs. If exact, normalize the two suffixed
   headings; they are new lines, so this does not violate byte preservation.
5. **Evidence durability.** `~/Projects/webzites` (state, scripts, journals,
   reports) and all `/tmp` evidence are gone. Gate text must not promise a
   replay; use "historical-not-live-reverified" and name restore-or-retire.
   The durable substitutes are the landed knowledge entries, `LOG.md`, and
   `SCORECARD.md`. Counts and code-line pins should carry their original
   command/date, and round-21 must not add new counts without one.
6. **Do not present corpus re-reads as verification.** The only round-21
   actions available here are local file reads (and digests of the base
   lessons). Any claim of verification beyond that would be fabricated.

## Remaining unknowns

- Whether kake's `Box3Kake` provisional marker was ever lifted: no evidence
  found; the round-9 verdict says it was not, and only kumitate's was re-tested
  and lifted in the aggregator report.
- Whether the vanished `webzites`/`/tmp` evidence will be restored (operator
  decision); until then, all live-state claims in rounds 8–12 remain
  historical.
- Whether the C2 contract gate will require an exact `## Gate` line; this
  determines whether the two suffixed headings must be normalized.
- Current worktree line numbers are moving while sibling scribes append; this
  report's appended-Gate line numbers are a snapshot, not a stable reference.

## Tooling

No tools installed or upgraded. No commands outside read-only local inspection
were run. Report written only at
`.ufo/waves/round-21/w1/LaterGateRejections.md`.
