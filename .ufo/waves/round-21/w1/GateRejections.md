# GateRejections — rounds 3–6 historical outcome support

- **Seat:** `KakeR21.GateRejections` (leaf scout; no subagents).
- **Base:** `5009ecaa1cce10b895617a585ddd3f7c7c923a84`.
- **Axes:** freshness (every asserted outcome traceable to a dated record) and
  operability (Gate authors can label outcomes without inventing an admission,
  rejection, or review).
- **Mode:** read-only. No lesson, knowledge file, index, LOG, SCORECARD, or
  source tree was edited. No network, no probe, no domain recheck. Only this
  report was written. No tools installed or upgraded.

## Method and snapshot

Read complete: `corpus/lessons/round-{3,4,5,6}.md` (29 / 42 / 67 / 47 lines at
first read), `corpus/lessons/round-{1,4,5,6}-aggregator-audit.md`,
`corpus/lessons/round-5-aggregator-mirror-pathless-cli-invocation.md` (title
scan only), `LOG.md:1-9`, and the main-repo decision archive
`/home/vgpnk/Projects/shokunin/.ufo/reports/{round-3,round-4,round-5,round-6}/aggregator.md`,
`{round-3,round-4,round-5,round-6}/kake.md`, and
`.ufo/reports/AGGREGATE.md` (the relevant sections). Enumerated every audit
artifact and every commit subject in lane history with
`git log --all --name-only` / `git log --all --grep`.

Concurrency note: while this report was being written, sibling seats appended
Gate tails to the four lessons. At report time `round-3.md` is 51 lines
(`## Gate` at 31), `round-4.md` 66 (`## Gate — round-21 retrospective
reconstruction` at 44), `round-5.md` 155 (`## Gate` at 69), `round-6.md` 74
(`## Gate` at 49). The historical analysis below was made from the pre-append
text; appended tails preserve the original bytes (verified at report time:
`head -c <frozen size>` of each current file compares equal to
`.ufo/waves/round-21/frozen/before/corpus/lessons/round-{3,4,5,6}.md`). I did
not edit or generally review those tails — the three exceptions are the
explicit corrections in §Current-draft corrections, which follow from the
record.

LSP was not applicable: the evidence is Markdown prose and git metadata, not
code symbols. Text search was used for enumeration; no semantic proof is
claimed from grep beyond the absence claim in §Absence proof.

## Decision-log inventory

| Artifact | Author / date | Scope | Relation to the four lessons |
|---|---|---|---|
| `corpus/lessons/round-1-aggregator-audit.md` (landed in `6b1cd07`, 2026-09-28 16:06:16 -0300) | aggregator L1 + independent L2 reviewer, non-author | round-1 corpus; "Scope: `corpus/` only" (line 6) | Verdict NOT conformant, but its defects target round-1 claims. It contains no `round-3` mention (grep). Not a round-3 lesson vote. |
| `.ufo/reports/round-3/aggregator.md` | aggregator L1, round 3 | read the round-3 kake report (line 15); produced the round-1 audit lessons (line 61) | Non-author quality review; no round-3 lesson verdict. AGGREGATE §1 records kake "strong, numeric drift + report-before-commit" (line 28). |
| `corpus/lessons/round-4-aggregator-audit.md` (`ac5ff82`, 16:37:56) | aggregator L1 + L2 reviewer, non-author | round-4 commit `6b1cd07`; scope explicitly includes `lessons/round-4.md` (line 8) | **Explicit round rejection:** "NOT CONFORMANT at `6b1cd07`" (line 13). |
| `.ufo/reports/round-4/aggregator.md` | aggregator L1, round 4 | per-repo verdicts | Records kake not conformant at `6b1cd07`, major fixed in `18537e9`; records the lane's rejection of one aggregator suggestion (line 65). |
| `corpus/lessons/round-5-aggregator-audit.md` (`1395393`, 17:28:09) | aggregator L1 + one read-only L2 reviewer; L1 re-ran the major | round-5 delta `18537e9` | **Explicit round rejection:** "NOT conformant — 1 major, 3 minors" (line 8); minor 2 names `lessons/round-5.md`. |
| `.ufo/reports/round-5/aggregator.md` | aggregator fleet-1 | 3 lines | Retirement marker only: fleet-1 retired before the report landed; **no verdict**. |
| `corpus/lessons/round-6-aggregator-audit.md` (`ab8c9e2`, 18:52:34) | aggregator L1, non-author, read-only, audit window 21:24Z–21:33Z | corpus at HEAD `dd4eabf` (includes rounds 7–10) | **Explicit round/corpus rejection:** "not conformant" (line 15), failed R4 and R1 (lines 17–27); names `ghp-subpath-spotcheck.md:3`; 2,352 paths `cannot-verify` (line 54). |
| `.ufo/reports/round-6/aggregator.md` | aggregator L1, round 6 | per-repo verdicts | kake at `dd4eabf`: "**not conformant** (4, 1)", 5 majors / 11 defects, lesson `ab8c9e2` (line 35). |
| `.ufo/reports/AGGREGATE.md` | aggregator ledger | rolling | Quality review (line 28), defect rows 16–17 (lines 129–130), round-4 verdict table (line 445), refresh-4 superseded verdicts (line 754), routed rows D-26/D-68/D-69 (lines 693, 726–727). |

## round-3.md

**Original state.** `corpus/lessons/round-3.md`, 29 lines, commit
`ddf40e2` (2026-09-28 15:58:04 -0300, subject `round-3`), sections
`## The gap closed` (line 6) and `## Learned` (line 18); no Gate. Only one
commit ever touched the file.

**Decision log.** No round-3-specific corpus audit and no admit/reject of this
lesson exists. The lane's own report says: "L2 routing: none dispatched;
single-author synthesis round" (`/home/vgpnk/Projects/shokunin/.ufo/reports/round-3/kake.md:58`).
The nearest non-author records are:

- `.ufo/reports/round-3/aggregator.md` — the aggregator read the round-3 kake
  report and, in `AGGREGATE.md:28`, rated kake "**strong, numeric drift +
  report-before-commit**". A quality rating, not an admit/reject of the lesson.
- `AGGREGATE.md:129` (defect 16) — "round-3 reports cited commits before they
  existed … `ddf40e2`, 'commit `round-3`' … both hashes now resolve … defect
  was real and self-corrected inside the round". This rejects a report/commit
  practice, not a lesson candidate.
- `AGGREGATE.md:130` (defect 17) — round-3 reports omit the `SHONEN.md`
  checklist assessment (contract-minimum content). Again report-level.
- `corpus/lessons/round-1-aggregator-audit.md` — non-author verdict "NOT
  conformant — well-sourced, but core fleet counts are wrong" (line 12), but
  it is round-1 scoped (line 6) and never names round 3.

**Candidate support.** No round-3 candidate was independently adjudicated.
The lesson's evidence is author-side: `corpus/knowledge/drift-detection.md`
fresh-probe table, `LOG.md:5`, and the lane report. The charter-ghp re-pin is
later recorded as extracted but never landed
(`corpus/lessons/round-7.md:31-33`, author-side). A Gate may say "unverified by
independent review"; it may say "admitted with qualification" only if it also
says the admission rests on lane records, not a verifier.

**Rejected candidates/reasons.** None documented for the lesson. Do not invent
one from the report-level defects.

**Outside spot-check.** No lesson-level spot-check is recorded. There is an
adjacent non-author quality review and two recorded report-level defects (above).
A flat "no non-author verifier entry … in `.ufo/`" is too broad because the
main-repo `.ufo/reports/round-3/aggregator.md` exists; the accurate statement
is "no lesson-level decision entry; adjacent aggregator quality review and
report-level defect rows exist."

**Confidence.** High on the absence of a round-3 lesson audit (see §Absence
proof). Medium on whether the main-repo quality review should be called an
"outside spot-check" — it is a report review, not a lesson-claim verification.

## round-4.md

**Original state.** 42 lines, commit `6b1cd07` (16:06:16 -0300), sections
`## The gap closed`, `## Evidence mined`, `## Learned`; no Gate. Header cites
`commit \`round-4\`` (line 7), i.e. subject only.

**Explicit recorded rejection.** `corpus/lessons/round-4-aggregator-audit.md`:

- "**Verdict: NOT CONFORMANT at `6b1cd07`** — one major internal index
  inconsistency (same-commit README contradicts the knowledge file it
  indexes)." (line 13)
- "**Fixed by the lane in round-5 (`18537e9`) before this lesson landed**;
  recorded because the round-4 commit shipped it." (lines 15–16)
- Scope explicitly includes `lessons/round-4.md` (line 8). Method: 16 citations
  independently re-executed; file-based only, no live URLs.
- Lesson-specific minor: "`lessons/round-4.md` cites commit as 'round-4' —
  resolvable by message but no hash named (`git rev-parse round-4` fails)."
  (lines 54–55); gap "Cite commit hashes, not subjects, in lessons." (line 69).
- The audit's "What reproduced" section confirms the exit-code table
  {1..8, 64}, the observed-outcome journal table, and the 21-row registry
  (lines 30–42). It over-generalizes nothing about the lesson's substance; the
  one lesson defect is the citation form.

The round-4 major was independently re-verified as fixed:
"Round-4's README '20 rows' major **stayed fixed** at `18537e9` and HEAD"
(`round-5-aggregator-audit.md:50`). The main-repo report records the same
per-repo verdict and notes the lane "rejected one aggregator suggestion with
evidence" (`app.ds4cc.com`; `.ufo/reports/round-4/aggregator.md:65`).

**Candidate support.** The journal-decoding candidates are supported by a
non-author re-execution and may be labelled "admitted with qualification":
code-set completeness, rebuild `efc1830` success, and the plazir15 code-6 /
ds4cc code-7 anomaly rows. Qualifications: the lucario "×3 preflight-only"
row over-reaches (2 of 3 end at code 1; only one reaches `canonCheck` with
`fire:false`, audit lines 49–53), and three `update-ds4cc-kimi-mirror`
journals are malformed JSON (lines 56–58). The prescriptive "blind refire is
the documented mistake" doctrine was not separately tested.

**Rejected candidates/reasons.** The lesson text records none. The audited
record does contain a documented rejection of an aggregator suggestion
(`app.ds4cc.com` registry addition) with the audit confirming "the lane's
rejection stands" (`round-4-aggregator-audit.md:39-40`; also
`.ufo/reports/round-4/aggregator.md:65`). That is a rejection *by* the lane, not
of a lesson candidate; do not convert it into a candidate outcome.

**Outside spot-check.** Yes: the round-4 aggregator audit (non-author, L1 + L2,
16 citations re-executed, file-based). It does not record an admit/reject pair
per candidate. The lesson's commit-cite minor remains uncorrected in the
original text.

**Confidence.** High. The round-level "not conformant" is driven by a README
defect absent from the lesson; the lesson-specific finding is the citation
form, not a falsified technical claim.

## round-5.md

**Original state.** 67 lines, commit `18537e9` (16:15:02 -0300), sections
`## The gap closed`, `## Evidence mined`, `## Learned`; no Gate. The flip-window
claim appears in the Evidence section ("left `violated[]` between 09-21T04:14
and 09-22T22:58").

**Explicit recorded rejection.** `corpus/lessons/round-5-aggregator-audit.md`:

- "**Verdict (round-5 delta `18537e9`): NOT conformant** — 1 major, 3 minors."
  (line 8). Method: one read-only reviewer L2 (26 citations re-executed; zero
  probes) plus L1 re-run of the major.
- Major 1: the "already running" ops layer is false for the keeper timer —
  `is-enabled` disabled, `is-active` inactive, journal "-- No entries --";
  "the claim was false at write time, not drifted" (lines 10–27). The lesson's
  framing ("the ops layer that was already running", "`webzites-keeper.timer`
  (daily)") shares that framing; the audit's fix instruction is a sweep across
  "README/LOG/lesson mentions of the daily tick".
- Minor 2 explicitly names `lessons/round-5.md` (line 34): the flip window is
  wrong; last violated run `09-21T03:32:06`, first clean run `09-21T04:14:50`;
  "Four mentions owe one swept correction" (lines 33–37).
- Minor 3: xsnapshot-app "every run since 09-21" is overstated (lines 39–42).
- Minor 4: `total - ok = violated + errors` false on 11 early rows (lines
  43–46).

**Later status.** The round-6 audit carries the keeper-timer claim forward as
uncorrected through round 10 (`round-6-aggregator-audit.md:60-71`; AGGREGATE
D-26 at line 693) and records the formula uncorrected (D-68, line 726). The
round-6 audit's table says the *r5 flip-window correction* landed in
`dd4eabf` — but `git log --follow -- corpus/lessons/round-5.md` shows only
`18537e9` and the r18 annotation commit `b0feb30`. The correction landed in
`ops-automation.md`; the lesson text still carries the old window. A Gate must
not claim the lesson was corrected. `.ufo/reports/round-5/aggregator.md` is a
three-line fleet-retirement marker and contains no verdict; the audit lesson is
the decision record.

**Candidate support.** With the audit: probe timer admitted with qualification;
keeper timer refuted; flip window refuted; xsnapshot constancy refuted; lucario
registration event admitted with qualification; several method claims
(cadence check, "known gaps rot", flat-frontier) unverified. The audit only
falsifies the stated windows/constancy, not the whole lesson.

**Rejected candidates/reasons.** The audit records falsifications with
commands and observed values (above). The lesson itself records no rejected
candidate. Do not describe the audit as an "admit/reject spot-check"; it is a
full independent audit with a not-conformant verdict.

**Outside spot-check.** Yes: 26 citations re-executed; L1 re-ran the major.

**Confidence.** High.

## round-6.md

**Original state.** 47 lines, commit `8755018` (16:27:17 -0300), sections
`## The gap closed`, `## What the audit actually found`, `## Learned`; no Gate.
Header cites `ghp-subpath-spotcheck.md`; evidence is the live baseline
(2,352 paths, ~16:45Z) plus `reconcile.mjs` and per-repo git lead/lag.

**Explicit recorded rejection.** `corpus/lessons/round-6-aggregator-audit.md`
(non-author aggregator L1, 2026-09-28, audit window 21:24Z–21:33Z, read-only):

- "**not conformant.** Failed rules:" (line 15).
- R4 (count carries its command) — the failing count is
  `ops-automation.md:25`, not this lesson (line 17).
- R1 (knowledge entries cite a source) — the list explicitly includes
  "`ghp-subpath-spotcheck.md:3` (`/tmp baseline audit` — no artifact named at
  all)" (lines 23–26). That is the baseline file this lesson cites.
- Minor defect 8: "`ghp-subpath-spotcheck.md:3` names no artifact for its 2
  352-path baseline" (lines 108–109; routed row at line 137).
- The audit's re-execution table marks "2 352 paths / 103 locs / 75-of-93 stale
  (rounds 6/7/8)" as "not re-executed (prohibited this round)" —
  **`cannot-verify`** (line 54).
- Main-repo report: kake at `dd4eabf` "**not conformant** (4, 1)", 5 majors /
  11 defects, lesson commit `ab8c9e2` (`.ufo/reports/round-6/aggregator.md:35`).

**Scope caveat.** The audit's HEAD `dd4eabf` is kake round 10, so this is a
later audit of a corpus that contains rounds 6–10, not a contemporaneous
round-6 judgment. The lesson file `corpus/lessons/round-6.md` is never named in
the audit; the rejection attaches to the corpus rules and to the cited baseline
file's provenance, not to the 0-rot measurement's truth.

**Candidate support.** The lesson's headline (0 true rot across 2,352 paths)
and the 126-result decomposition are **unverified by the audit** — explicitly
`cannot-verify` because live HTTP was prohibited in that window. The
`in-sync` masking and dir-index claims were not re-executed either. The
`reconcile.mjs` source read is historical; the source is absent since the
2026-10-12 prune. The documented provenance rejection applies to the baseline
artifact (no named file), so the counts remain a single-snapshot, lane-authored
record.

**Rejected candidates/reasons.** No lesson candidate was rejected by the
audit. The R1/R4 failures and defect 8 reject provenance/practice, not the
finding. Do not label the 0-rot result "rejected".

**Outside spot-check.** **Recorded**, contrary to the current draft tail:
the round-6 aggregator audit is itself the non-author review, and its
`cannot-verify` row is the honest outside result. Its existence is in the lane
tree at `corpus/lessons/round-6-aggregator-audit.md`, committed `ab8c9e2`.

**Confidence.** High that the audit exists and says what is quoted. Medium on
how far the not-conformant verdict reaches into this lesson, for the HEAD-scope
reason above.

## Current-draft corrections (state observations, not edits)

At report time the appended tails contain two falsifiable statements:

1. **`round-6.md:72`** — "Outside spot-check: not recorded. No independent
   non-author verifier … is named for round 6 …". This is contradicted by
   `corpus/lessons/round-6-aggregator-audit.md` (`ab8c9e2`), whose header names
   the aggregator L1, non-author review and whose line 54 marks the 2,352-path
   claim `cannot-verify`. Replace "not recorded" with the audit citation and
   the cannot-verify outcome.
2. **`round-3.md:45`** — "No non-author verifier entry for round-3 was found in
   `LOG.md`, `corpus/lessons/`, or `.ufo/`." True only for a *round-3-specific
   lesson entry*; the main-repo archive has
   `.ufo/reports/round-3/aggregator.md` and the AGGREGATE quality/defect rows.
   Qualify the scope: no lesson-level decision entry, adjacent report-level
   non-author records exist.
3. **Heading exactness (C2 contract):** `round-4.md:44` currently reads
   `## Gate — round-21 retrospective reconstruction`, not the exact `## Gate`
   supplied in the scribe prompt. The other three use exact `## Gate`. Content
   was not otherwise reviewed here.

These are observations from the record; I left every file untouched.

## Absence proof (round-3 lesson audit)

- `corpus/lessons/` contains aggregator/verifier artifacts for rounds 1, 4, 5,
  5-mirror, 6, 8, 9, and 20 only; there is no `round-3-*aggregator*` file.
- `git log --all --name-only` over the full lane history lists the same set;
  no round-3 audit path ever existed in any commit.
- `git log --all --grep='round-3|round 3' -i` returns only commit `ddf40e2`
  (subject `round-3`).
- The round-4 audit explicitly excludes rounds 5–6 from its verdict (line 5)
  and does not mention round 3; the round-5 and round-6 audits do not
  retroactively adjudicate round 3 either.
- The main-repo round-3 aggregator report's kake section is a quality review
  plus a "no promotion this round" assessment (line 98), not a lesson verdict.

## Limits and remaining unknowns

- The domain evidence (`~/Projects/webzites`, `kimi-surface.mjs`, journals,
  `reconcile.mjs`) is absent after the 2026-10-12 prune; audits carry r18/r20
  historical-record annotations. None of their commands or the lessons'
  measurements can be re-executed now. All "reproduced" claims above are
  restatements of the audit record, not new runs.
- The round-5 aggregator main-repo report is a retirement stub; the L1/L2
  working detail behind `1395393` is not separately archived. The lesson is the
  decision record.
- The round-6 audit is a later audit window over `dd4eabf` (rounds 6–10 in
  kake), not a contemporaneous round-6 review.
- The AGGREGATE ledger at the shared base records the standing corpus verdict
  for kake as "not conformant; r4,r8,r10; 54" (`AGGREGATE.md:2166`). That is a
  current corpus verdict, not a per-lesson historical outcome; no Gate may
  upgrade it to a lesson admission or downgrade it to a lesson rejection.
- "Admitted", "rejected", and "independent review" are historical predicates.
  A retrospective Gate can report them; it cannot create them. The records
  above support admission only where an audit re-executed the claim, and
  rejection only where a dated record names the claim and its falsifier.

## Evidence locations

- Lane: `corpus/lessons/round-{3,4,5,6}.md`;
  `corpus/lessons/round-{1,4,5,6}-aggregator-audit.md`; `LOG.md:5-8`;
  `corpus/knowledge/drift-detection.md`, `ghp-subpath-spotcheck.md`,
  `ops-automation.md`, `keeper-timer-inert.md`.
- Main repo archive (read-only):
  `/home/vgpnk/Projects/shokunin/.ufo/reports/round-{3,4,5,6}/{aggregator,kake}.md`;
  `/home/vgpnk/Projects/shokunin/.ufo/reports/AGGREGATE.md` (lines 21–28,
  106–130, 445, 693, 726–727, 754, 2166).
- Git: `ddf40e2`, `6b1cd07`, `18537e9`, `8755018`, `ac5ff82`, `1395393`,
  `ab8c9e2`; `git log --follow` for each lesson.

## File changes

- Created: `.ufo/waves/round-21/w1/GateRejections.md` (this report).
- Edited: none. Commits: none.
