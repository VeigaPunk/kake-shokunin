# Round 24 — ScribeLogScorecard (author-side drafts, numbers <TBD>)

Scope: draft only. Nothing in `LOG.md`, `SCORECARD.md` or any other lane file was edited. Only this report was written. No tool was installed or updated.

## Verdict

- Drafts below are ready for the planner (L1, KakeR24) to integrate after the C1 and C2 measurements exist. Every number is `<TBD>`.
- Blocking inconsistency: the frozen contract names counting runners (`.ufo/waves/round-24/measure_c1.py`, `.ufo/waves/round-24/measure_c2.py`) that do not exist yet. The C2 population `c2-population.json` is also absent. See Finding F1. The SCORECARD counting-command column cannot be finalised until the planner picks the runner path.
- Axes: both expected to stay at the saturation ceiling (`freshness 10→<TBD>`, `operability 10→<TBD>`). No score is proposed here.

## Observed inputs (read, not re-measured)

| Input | Observed value | Source |
|---|---|---|
| Contract frozen | `frozenAt` 2026-10-21T11:45:00Z, base `f7de3ab4e9f030a15a857a5a08631bd8e690f436` | `.ufo/waves/round-24/contract.json` |
| Paths gate at round open | `"ok": false, "code": 1`, reasons `"§paths: 3 unannotated miss · 12 NOT in pins.pathsMissSet"`, `generatedAt` 2026-10-21T11:35:35Z | `.ufo/waves/round-24/paths-before.json` |
| C1 population | 19 targets: T01–T03 drift, T04–T15 newMissing (12), T16–T19 recovered (4); 101 cites total | `.ufo/waves/round-24/c1-population.json` |
| Unannotated cites | 4: `corpus/knowledge/drift-detection.md:77`, `corpus/knowledge/fleet-registry.md:57` (T01), `corpus/knowledge/free-read-verbs.md:321` (T02), `corpus/lessons/round-6-aggregator-audit.md:48` (T03, non-author) | `c1-population.json` `unannotatedCites` |
| Non-author cites in population | 7 (T02: 2, T03: 4, T17: 1), all `corpus/lessons/*aggregator*.md`; 0 `*verifier-spotcheck*` cites | `c1-population.json`, glob match of the contract's non-author rule |
| Lane-authored recovered cites | 25 (T16: 15, T18: 5, T19: 5), plus T17's 1 non-author cite | `c1-population.json` |
| Scripts present in lane | `canonical_audit.py`, `corpus-contract.mjs`, `freshness-sweep.mjs`, `live_snapshot.py`, `probe-delta.mjs`. No `receipt_replay.py` yet | `ls scripts/` |
| Round-24 runners present | none (`measure_c1.py`, `measure_c2.py`, `c2-population.json` absent) | `ls .ufo/waves/round-24/` |
| Wave roster | 72 registry members (scout 18, reviewer 15, executor 9, revenger 8, mutation-tester 8, scribe 6, critic 4, sentinel 2, connector 1, simplifier 1) | `.ufo/waves/round-24/w1/swarm-registry.json` |
| Dead seat | `ConnectDs4ccSiblingOverlap` (connector), 429 QUOTA_EXHAUSTED at 2026-10-21T11:42Z, reset 2026-10-25T11:37:24Z, not replaced | `.ufo/waves/round-24/w1-deaths.json` |

## Findings

**F1 — P2 — counting command and population do not exist for C1 or C2.**
- Exact contract text: `"count": "python3 .ufo/waves/round-24/measure_c1.py --root . --revision <commit>"` and `"count": "python3 .ufo/waves/round-24/measure_c2.py --root . --revision <commit>"`.
- Exact observed state: `ls .ufo/waves/round-24/` lists `c1-population.json`, `census-before.txt`, `contract.json`, `gen_w1.py`, `paths-before.json`, `w1/`, `w1-deaths.json`, `w1-dispatch.json`, `w1-spec.json`, `w1-taskcall.json`. There is no `measure_c1.py`, `measure_c2.py` or `c2-population.json`. `scripts/receipt_replay.py` is also absent.
- Conflict: the C2 gap item says the fix lands as `scripts/receipt_replay.py`. The `ScribeKnowledgeReplay` prompt uses `scripts/receipt_replay.py c1|c2 --root . --revision <commit>`. The contract's count is `.ufo/waves/round-24/measure_c2.py`. These name different entry points.
- Impacted claims: C1 and C2 counting, and the SCORECARD counting column for both.
- Smallest fix: the planner states one runner path per claim before dispatch of the `before` counts. Either a thin `.ufo/waves/round-24/measure_c2.py` wrapper around `scripts/receipt_replay.py c2`, or the contract's count command is rewritten to `python3 scripts/receipt_replay.py c2 --root . --revision <commit>`. Freeze `c2-population.json` (with the 17/12 control set) before the base-revision count is taken, so C2 `before` is reproducible. The drafts below use `<RUNNER>` for the chosen command.

**F2 — P3 — C2 "before" has no numeric definition in the contract.**
- Contract `before` reads: "correctly rejects (exit 1 or 2, no traceback) only some malformed cases".
- The SCORECARD table needs `<n>/<N>` before→after. The draft uses `rejected-without-traceback <TBD>/<N>` from the round-23 runner at base, applied to the frozen population from F1.

**F3 — P3 — C1 restoration corrections touch ±2-line neighbours.**
- Recovered cites cluster: `SKILL.md:16`, `:19`, `:20` (T16/T18), and `corpus/knowledge/fleet-registry.md:49`, `:50`, `:51`. A restoration correction appended to one line sits within ±2 of others.
- Restoration notes must carry none of the absence vocabulary `/absent|gone|vanished|emptied|no longer|dangling|no such file|never published|missing/i`. Otherwise they annotate neighbours. The LOG and SCORECARD drafts below avoid the vocabulary in any text that could be mistaken for a cite note.

**F4 — P3 — C2 population must be frozen before any `before` count is cited.**
- Without `c2-population.json` present at round-24 open, the "before" column cannot be reproduced by a third party. The SCORECARD draft keeps the C2 row `<TBD>` until the file exists and its sha256 is recorded.

## Checked and held

- `contract.json` fields used in drafts (`claims[].before/after/count/limits`, `lowestAxis`, `debts`) match the text quoted above.
- `c1-population.json` counts: 19 targets; classes 3/12/4; unannotated list length 4; cite total 101 (19+16+28+12+15+1+5+5 = 101). Verified by a one-off tally over the population file, not by re-running the sweep.
- LOG style: `LOG.md` lines 784–837 use `## Round N — title (date)` headings and `- Label:` bullets (Motivation, Frozen, Sources, Measured, Boundaries, Tool installs/updates, Per-axis, Trends). Round-23 closure at lines 796–837 is the template for the dead-seat and recovery paragraphs.
- SCORECARD style: round-23 section (lines 314–371) uses a 5-column table `| Claim | Axis / score delta | Before → after | Counting command | Verdict / evidence |`, then a `### Planned — supersedes round-22 plan` style subsection. The draft follows the same columns.
- Move log (lines 83–97) row format `| Round | Axis | Before | After | Evidence |`; newest rows are not ordered strictly, so the draft row is placed at the top of the table.
- Dead seat count: `w1-deaths.json` lists one death. No other death file exists for this wave in the round-24 directory.
- No edit made to `LOG.md`, `SCORECARD.md`, `corpus/`, `scripts/` or any domain tree. Only this report was written.

## Limits

- Scribe seat, author-side. Nothing here is independent admission, and no measurement was run by this seat (per the assignment, numbers are `<TBD>`).
- No `paths` sweep or runner was executed. Filesystem facts about `~/Projects/ds4cc-marketplace` and the other 18 targets are taken from `paths-before.json` and the contract's `worldChangeAtOpen`, not re-observed.
- Source rows for RFC 3339 and RFC 9110 are not opened here (owned by `ScribeSourcesRows` and the source seats). Citation placeholders are `<S-ID>`.
- The Round-24 Sources row count and the frontier/axis verdicts are for the planner to fill from the measured round.

---

## Draft A — `LOG.md` entry (append at end of file, after the Round 23 recovery block)

```markdown
## Round 24 — paths-gate reconciliation and receipt-replay hardening (2026-10-21)

- Motivation: round-24 open. `node scripts/freshness-sweep.mjs --section=paths`
  exited 1 at 2026-10-21T11:33:15Z (contract `worldChangeAtOpen`;
  `.ufo/waves/round-24/paths-before.json`, generatedAt 2026-10-21T11:35:35Z):
  drift 3 targets with 4 unannotated cites, 12 newMissing tokens outside
  `pins.pathsMissSet`, and 4 pinned misses recovered because
  `~/Projects/ds4cc-marketplace` reappeared (dir birth 2026-10-21 05:19 -03).
- Frozen base `f7de3ab4e9f030a15a857a5a08631bd8e690f436` (round 23). Contract
  `.ufo/waves/round-24/contract.json`, frozen 2026-10-21T11:45:00Z. Population
  `.ufo/waves/round-24/c1-population.json`: 19 targets (3 drift, 12 newMissing,
  4 recovered), 101 cites, 7 of them non-author (`corpus/lessons/*aggregator*.md`).
- C1 freshness: reconcile all 19 paths-gate targets with the filesystem.
  Before 0/19 targets carry a round-24 receipt; paths exit 1. After <TBD>/19
  receipts; unannotated cites 4 → <TBD>; pins.pathsMissSet <TBD>; paths exit <TBD>.
  Lane-authored absence annotations are inline; non-author files (unannotated
  `round-6-aggregator-audit.md:48`, and `round-1-aggregator-audit.md:30` for
  the recovered CNAME target) go through a lane-authored sidecar. No historical
  cite was rewritten; restoration corrections are appended and carry no
  absence vocabulary.
- C2 operability: receipt replay rejects malformed receipts instead of
  accepting or crashing. Replay now lives in `scripts/receipt_replay.py`
  (round-23 runners stay byte-intact). Before <TBD>/<N> malformed frozen cases
  rejected with exit 1 or 2 and no traceback; after <TBD>/<N>. Controls stay
  accepted: c1 17/17, c2 12/12.
- Sources: RFC 3339 (date-time) and RFC 9110 (media type) opened this round as
  <S-ID> and <S-ID>; access date <TBD>; quotes in the Gate section of
  `corpus/lessons/round-24.md` (<TBD>).
- Measured at `<TBD commit>`: `<RUNNER c1>` and `<RUNNER c2>`; receipts
  `.ufo/waves/round-24/measure-c1-{before,after}.json` and
  `.ufo/waves/round-24/measure-c2-{before,after}.json` (<TBD>).
- Boundaries: no domain tree restored, retired, pushed or published; ds4cc
  remains read-only (stat/ls/git log only). Restore-or-retire remains
  operator-owned; C1 measures filesystem truth at measurement time, and a later
  restore or prune is new drift for a later round.
- Dead seat: `ConnectDs4ccSiblingOverlap` (connector) stopped at 2026-10-21T11:42Z
  on Gemini quota 429 (reset 2026-10-25T11:37:24Z). Uncredited, not replaced
  (`.ufo/waves/round-24/w1-deaths.json`).
- Per-axis: freshness <TBD> (HOLD 10 expected); operability <TBD> (HOLD 10
  expected). Trends: <TBD>. Author-side; no independent admission claimed.
- Tool installs/updates: none by this seat. <TBD: any tool installed by a
  measured seat, with tool, version, channel, reason.>
```

## Draft B — `SCORECARD.md` `## Round 24` section (insert before `## Round 23` heading or after it, matching the round-23 section layout)

```markdown
## Round 24 — paths-gate reconciliation and receipt-replay hardening

Base: `f7de3ab4e9f030a15a857a5a08631bd8e690f436` (round 23, admitted).
Before measurement: `<TBD>`. After measurement: `<TBD>`. Both counts use the
same runner bytes, recorded by sha256 in the measurement receipts.

| Claim | Axis / score delta | Before → after | Counting command | Verdict / evidence |
|---|---|---|---|---|
| C1 paths-gate reconciliation of 19 targets (3 drift, 12 newMissing, 4 recovered) | freshness 10→<TBD> (HOLD 10 expected; tied-lowest owned axis) | receipts 0/19 → <TBD>/19; paths exit 1 → <TBD>; unannotated cites 4 → <TBD>; tokens outside pins.pathsMissSet 12 → <TBD>; pinned misses recovered 4 → <TBD> | `node scripts/freshness-sweep.mjs --section=paths` and `<RUNNER c1> --root . --revision <commit>` | <TBD: improved / HOLD, author-side; `.ufo/waves/round-24/measure-c1-{before,after}.json`; filesystem truth at measurement time> |
| C2 receipt replay rejects malformed receipts | operability 10→<TBD> (HOLD 10 expected) | malformed frozen cases rejected without traceback <TBD>/<N> → <TBD>/<N>; controls accepted c1 17/17 and c2 12/12 held | `<RUNNER c2> --root . --revision <commit>` | <TBD: improved / HOLD, author-side; `.ufo/waves/round-24/measure-c2-{before,after}.json`; structural validation only, not authentication of the network observation> |

Controls can fail: `<TBD: counter selftest n/N>`; `<TBD: mutation/probe n/N>`.
The frozen C2 population (`<TBD sha256>`) is the only population used for both
before and after counts.

No observed harm on the previous evaluated population: `<TBD: corpus-contract exit>`.
Paths gate: `<TBD: exit, unannotated, missSet>`; restore/retire remains
operator-owned.

Sources <TBD: S-ID rows before→after> (RFC 3339, RFC 9110). Expansion <TBD>;
quality <TBD>; discernment <TBD>, pending non-author admission. Dead seat
`ConnectDs4ccSiblingOverlap` uncredited (quota 429, reset 2026-10-25T11:37:24Z).

### Planned — supersedes round-23 plan

Round-23's planned freshness reconciliation of live canonical findings with the
operator repair queue is superseded by round-24's C1, which measures only the
paths-gate surface the lane can observe. Round-23's publisher-side sitemap /
canonical frontier stays open and unclaimed. The next steered round is set by
the operator; the paths gate is the standing instrument at its open. Restore,
retire, publishing and account operations stay operator-owned, and no new
round is authorized by this paragraph.
```

## Draft C — `SCORECARD.md` top-table and move-log rows (replace in place)

Top table, freshness row `Last change`:
`r24 <TBD>: paths gate reconciled <TBD>/19 receipts; exit <TBD>; see ## Round 24.`

Top table, operability row `Last change`:
`r24 <TBD>: scripts/receipt_replay.py rejects <TBD>/<N> malformed frozen cases; controls 17/17 and 12/12; see ## Round 24.`

Move log, new row at the top of the table:
`| 24 | freshness + operability (HOLD 10 expected) | paths exit 1: drift 3 / unannotated 4 / newMissing 12 outside pins; recovered 4 pinned misses; C2 lexical timestamp prefixes and non-string contentType accepted or crashed | exit <TBD>, receipts <TBD>/19; C2 <TBD>/<N> malformed rejected, controls held | \`.ufo/waves/round-24/\`, \`corpus/lessons/round-24.md\` (<TBD>) |`

## Limits (restated for the planner)

- All numbers are `<TBD>`. Nothing is measured by this seat.
- F1 must be resolved before any `before` count is taken: the runner path and the C2 population file.
- This report is author-side. It does not claim independent admission, a score change, or any tool install.
