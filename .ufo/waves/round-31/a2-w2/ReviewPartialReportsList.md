# ReviewPartialReportsList — routed defect 5 spot-check (round 31, a2-w2)

Reviewer: KakeR31a2.ReviewPartialReportsList (leaf). Lane reads + harness reads only; the only
lane write is this file. No installs (none needed). Sandbox created but unused (no command wrote
files): /fast/scratch/hyaku/kake-r31/a2-w2/ReviewPartialReportsList/.

## Coverage (acceptance count)

`.ufo/waves/round-30/w2/partial-reports.json` has exactly 20 entries (15 `complete`, 5 `partial`);
`.ufo/waves/round-30/w2/` holds exactly 20 `.md` files. The mapping is a bijection: every committed
report has exactly one entry, every entry names an existing file. No phantom entry, no omission.
Coverage count: **20/20**.

## Spot-check: 5 partial + 3 complete

The assigned check (`history://KakeR30.<seat>` final lines + `agent://KakeR30.<seat>`) is **not
executable**: every such read returns Unknown agent / Not found — tried history for AfterMutantLedger,
MutWitnesses, ReopenS051S052, ReviewEntryHeadersDomains, ReviewPublishChannelsRecheck, agent for
AfterMutantLedger, and bare `history://KakeR30`. The known-agents list contains zero `KakeR30.*`
ids; the round-30 transcripts did not survive the omp restart [INFERENCE: timing 17:26Z].

Substituted triangulation from committed artifacts:

1. Committed classification vs list: `.ufo/waves/round-31/w1/ScoutR30PartialReports.md` (wave-1
   scout classified all 20 from transcripts while they existed, two signals per seat: `agent://`
   published result + `history://` transcript ending). All 20 statuses match the committed JSON
   exactly; role splits match (complete = 7 critic, 4 reviewer, 2 mutation-tester, 1 scout,
   1 sentinel; partial = 3 reviewer, 2 mutation-tester).
2. Report content: the 5 `partial` reports are structurally complete files (title, findings,
   "Not verified" section) and none begins with `PARTIAL:` — consistent with each entry's
   `evidence.note`: "report file exists and is structurally complete, but the seat never returned".
   The 3 `complete` reports end in closing verdict blocks consistent with a returned seat.
3. JSON evidence fields: all 5 partial entries carry `published_result: false` and
   `transcript_ends_on` = a tool call with no closing message; CriticC1Scope and ScoutNoHarmDiff
   carry excerpts matching their reports' tails.

Per-entry verdicts (list status → check result):

| Entry | List status | Result | Evidence |
|---|---|---|---|
| AfterMutantLedger.md | partial | consistent | ScoutR30PartialReports.md:40; report tail = sandbox artifact pointers only |
| MutWitnesses.md | partial | consistent | ScoutR30PartialReports.md:50 |
| ReopenS051S052.md | partial | consistent | ScoutR30PartialReports.md:51 |
| ReviewEntryHeadersDomains.md | partial | consistent | ScoutR30PartialReports.md:55 |
| ReviewPublishChannelsRecheck.md | partial | consistent | ScoutR30PartialReports.md:56 |
| CriticC1Scope.md | complete | consistent | ScoutR30PartialReports.md:41; excerpt matches "Smallest safe correction" tail |
| ScoutNoHarmDiff.md | complete | consistent | ScoutR30PartialReports.md:58; excerpt matches report tail |
| SentinelRunnerSetup.md | complete | consistent | ScoutR30PartialReports.md:59; excerpt matches "probes confirmed..." |

Downstream consumers agree with the list: `LOG.md:1325` "(15 complete, 5 partial)";
`corpus/lessons/round-31.md:70` (provenance: scout classified from transcripts, list committed);
`corpus/QUALITY.md` round-31 criterion "count of returned seats equals the number of reports not
listed as partial" — 15 = 20 − 5 holds on the round-30 data.

## Findings by severity

**MEDIUM (freshness — evidence decay).** The list's evidence pointers are dead.
`evidence.async_result_line` values (`history://KakeR30:732/764/770/808/818/832/842/852`) and
`agent://KakeR30.<seat>` no longer resolve for any seat, so the classification cannot be
re-derived from live transcripts; it now rests on the committed scout report and the committed
JSON, which agree with each other but share one author and one measurement pass. Worse: the
scout's independent count corroboration `.ufo/reports/round-30/kake.md:64` was never committed
(`git log --all` on that path is empty, exit 0) and `.ufo/reports/` tracks only `round-20/`, so
the scout's "agrees exactly" (15 returned / 19 cancelled) is unverifiable today. Mitigation
observed: round 31 commits a `seat-status.json` per wave (QUALITY round-31 criterion), closing
this decay mode prospectively.

**LOW (operability — wording).** `partial` describes the seat, not the report. None of the 5
partial files carries any in-file marker (grep `PARTIAL` over `w2/*.md` hits only body text:
MutWitnesses.md:16 table row, RerunC2Counter.md:80 "PARTIAL FAIL", CriticQualityCriteria.md:26);
a reader listing the directory sees finished-looking reports. The rationale lives only inside
`evidence.note`. No round-30 action needed (fixed prospectively), but prose citing the list
should say "seat did not return", not "report incomplete".

**INFO (JSON cosmetics).** SentinelRunnerSetup's evidence has no `async_result_line` and its
`final_message_excerpt` is cut mid-word ("...no source changes w"). Harmless; consistent with the
scout's note that only 8 of 15 complete seats had explicit `[async-result]` lines.

## Commands run (exit 0 unless noted)

- read (jq projection) `partial-reports.json` → 20 rows, statuses 15/5; `swarm-registry.json`
  members → 34 (34 = 20 reports + 14 report-less, matching the scout's count).
- read `ScoutR30PartialReports.md` (86 lines); 8 report heads (200 bytes each) and tails;
  `QUALITY.md:500-515`; `LOG.md` and lesson lines via grep context.
- `ls .ufo/waves/round-30/w2/*.md | wc -l` → 20.
- `for f in <8 seats>; do head -c 200 w2/$f.md | head -2; done` → first lines quoted above; no
  `PARTIAL:` first line in any of the 8.
- grep `PARTIAL` over `w2/*.md` → body-text hits only (paths above).
- grep lane-wide for the 5 partial seat names and for `partial-reports` → hits confined to
  `.ufo/waves/round-30/` records, the reports themselves, round-31 records (spec/dispatch, scout,
  lesson, QUALITY, LOG) and `CriticRejects.md:56` / `ReviewSkillRenderTable.md:37` (which mention
  ReopenS051S052's refusal, not its report content). No `corpus/` or SCORECARD citation of any
  partial report's content — matches the scout's leak check, re-confirmed.
- `git --no-optional-locks log --oneline --all -3 -- .ufo/reports/round-30/kake.md` → empty,
  exit 0; `git --no-optional-locks ls-tree -r --name-only HEAD .ufo/reports/` →
  `round-20/kake.md` only.
- Harness reads: 7 × Unknown agent / Not found (quoted in report; these are the expected errors).

## Not verified

- Seat statuses against live transcripts — impossible; the transcripts are gone. What I confirmed
  is artifact consistency (list ↔ committed scout classification ↔ on-disk report content), not
  transcript observation.
- The scout's two-signal method at classification time — taken as committed record; not re-runnable.
- The `.ufo/reports/round-30/kake.md:64` count agreement — unverifiable (file never committed).
- The 14 report-less seats' individual fates — only the aggregate 34 = 20 + 14 was checked.
- No seat's measurements were re-run; no claim about report content correctness beyond structure.
