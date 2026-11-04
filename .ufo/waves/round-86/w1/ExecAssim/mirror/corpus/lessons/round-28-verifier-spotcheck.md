author: hyaku closure (non-author integrator, @m_opus)

# Round 28 non-author verification: both declared claims verify; admitted

Integrator of record for kake round 28. I did not author this round. Runtime
model as exposed by the host: anthropic/claude-opus-5-5. I judged committed bytes
only: base `22c1669c1fec83d1a0769de6b9ce686c75657e66`, lane tip
`36b6b21022f7288200abe2ace7e686c1297588a3`, report `.ufo/reports/round-28/kake.md`
(fleet commit `33d8f198a2a8089a04e06dcb230913aa606e77f8`). The private author
trees under `/fast/scratch/hyaku/kake-r28-author*` were not used as evidence.
I did not execute the lane's citing-set gate, the C1 counter (which runs that
gate) or any selftest. I ran the read-only C2 counter (`git show` only), plain
git/grep/jq/cmp measurements, the fleet sources census, and one public GET per
source page. I dispatched no review seats; every check below is my own.

Driver digest (copied from `.ufo/watchdog.log`): attempt 1 launched
2026-10-21T21:53:53-03:00 and was superseded with no lane commit in base..tip.
Attempt 2 launched at 05:16:42-03:00 and was stood down for capacity after
pushing `84ea5b1` and `b5d423f`. Attempt 3 launched at 06:26:15-03:00 and the
driver logged `complete` at 06:58:58-03:00.

## Step-1 conformance

| Check | Command | Observed |
|---|---|---|
| Report committed by the lane | `git log --format='%an %H' -- .ufo/reports/round-28/kake.md` | `kake-shokunin` 33d8f19 (06:58:35-03:00, after the lane tip at 06:56:44) |
| `SHONEN` heading, one line per box | read report | 4 lines, all `[~]`, each with a pointer; SHONEN.md has 4 boxes, all `[ ]` |
| Cited commits exist and are ancestors of `master` | `git cat-file -e` + `git merge-base --is-ancestor <h> master` for all 7 cited hashes and the base | all 8 ok; `git log 22c1669..36b6b21` shows exactly the 7 cited commits, all authored `kake-shokunin` |
| Pushed | `jj-lane.sh state …/kake-shokunin` | `local=remote=36b6b21…, ahead=0 behind=0, untracked=1` |
| Leftovers | `git status --porcelain` | `?? .ufo/waves/round-26/__pycache__/` only; see below |
| Prompt carries the template contract | every non-placeholder line of `templates/round-prompt.md` looked up in `.ufo/prompts/kake-round-28.md` | 105/105 present; §6 hyaku addendum appended (directive 3 verbatim, §9 Claim sizing) |

The one uncommitted path is not round-28 work. It holds two CPython 3.14
bytecode files (`fetch_sources`, `source_text`) compiled from round-26 scripts,
with mtimes 2026-10-21 17:04:43 and 19:01:14 -03:00. Both predate the attempt-1
launch at 21:53:53. They are generated cache, not lane-authored content. The
report already discloses them ("Not mine and left as found").

## Targets frozen before measurement, never narrowed

- Both declared rows (claim, before, declared after, counting command) were
  committed at `84ea5b1` (05:24:40). The repair `b5d423f` landed at 05:25:38.
  Every after-receipt names a revision of `b5d423f` or later, so no
  after-value could have been measured before the declaration existed.
- `git diff --stat 84ea5b1 36b6b21 -- .ufo/waves/round-28/c1_interface_count.py .ufo/waves/round-28/c2_source_count.py`
  is empty, so the counters are byte-identical from declaration to tip.
- `git diff 84ea5b1 36b6b21 -- SCORECARD.md` only appends a "measured results"
  section after the declaration. The declared rows are unchanged.
- The declared after-values (15/15 and 4/4) are each counter's full total. The
  C1 exclusions (duplicate-key and nonfinite JSON, identity paths, retention)
  were written into the declaration at `84ea5b1`, not added after landing.
  The C1 wording is word for word the round-27 routed defect 1
  (`round-27-verifier-spotcheck.md`, "Routed defects", item 1).

## Claims

### C1 operability: evidence-verified (gate-based), plus a static re-measure

The claim rests on the lane-owned `scripts/citing_set.py` gate, so PROTOCOL
§Gate standard (Closure consequence) applies: I verified committed evidence and
did not run the gate.

- Receipts (`jq` over `.ufo/waves/round-28/verification/`):
  - `c1-before-22c1669-a3.json`: passed 4/15 (defect 0/11, control 4/4).
  - `c1-after-b5d423f-a3.json`, `c1-after-8ecbefe.json`,
    `c1-after-5a83d13.json`, `c1-after-e73d48b.json`: each passed 15/15
    (defect 11/11, control 4/4).
  - Before: U1/U2 time out, U3/U4 give a traceback with exit 1, and A1–A7
    return exit 0 with verdict `clean`.
  - After: every defect case returns exit 2 with verdict
    `could-not-evaluate` and the matching reason (`document_not_regular_file`,
    `document_not_json`, `corpus_directory_missing`, `corpus_empty`,
    `not_a_directory`, `population_id_unreachable`, `revision_not_found`,
    `root_not_repository_top_level`).
- Revision measured vs tip: `git diff --stat e73d48b 36b6b21 -- scripts/` is
  empty, so the 15/15 at `e73d48b` holds for the tip's gate bytes.
- Self-test tally: K4 in every after-receipt shows the commit's fixture runner
  at exit 0, 29 cases, 0 failed. `w1a3/RunNoHarmSuites.md` gives 29/29 for both
  the runner and the builtin `--selftest` at base and at the repair.
- Revert mutants: 7 of 7 are recorded `killed`, each failing exactly its
  targeted cases with controls green: `MutRevertNonBlocking`, `JsonDepth`,
  `CorpusMissing`, `CorpusEmpty`, `GitBlobEmpty`, `GitTopLevel` and
  `BlankRevision` (each file's `## Verdict`). In `MutRefuseAllGate`, a
  refuse-everything gate is killed (11/15).
- My static re-measure over committed bytes: I counted occurrences of each
  `git show <rev>:scripts/citing_set.py | grep -c <label>` at base and tip for
  the 7 new reason labels. At base: `document_not_regular_file` 0,
  `corpus_directory_missing` 0, `corpus_empty` 0, `population_id_unreachable` 0,
  `root_not_repository_top_level` 0. At tip: 1, 2, 1, 2 and 1. The new
  failure paths exist only after the round.
- Follow-ups: `8ecbefe` (bare repository and trailing-space top level),
  `5a83d13` (inherited `GIT_DIR` family) and `e73d48b` (`MemoryError`,
  base labels restored). Each was re-measured at 15/15 by its receipt.
- **Verdict operability: improved** (4/15 → 15/15 as reported).

### C2 freshness: re-measured

- Command: `python3 -B c2_source_count.py --root kake-shokunin --revision <r>`.
  I extracted the counter from tip bytes and ran it from scratch. It reads
  only `git show`.
  - `22c1669`: 0/4, exit 1.
  - `b5d423f`: 0/4, exit 1.
  - `e57f601`: 4/4, exit 0.
  - `36b6b21`: 4/4, exit 0.
- Plain counts: `git show <r>:corpus/SOURCES.md | grep -cE '^\| *S[0-9]{3}'`
  gives 35 at base and 39 at tip. S036–S039 are tier A, `mined`, opened
  2026-10-22, with the entry in used-by. The entry header cites all four ids.
  `git diff --name-status 22c1669 36b6b21 -- corpus/knowledge` gives one `A`.
- Quote truth, beyond the counter's shape check: I re-opened all four pages
  at 2026-10-22T10:01:08–10Z, HTTP 200, 143746 / 149322 / 109246 / 167991
  bytes. Visible text = HTML minus script and style, tags stripped, entities
  decoded, whitespace collapsed. All 4 `## Gate` quotes and all 11 table
  quotes are exact substrings (15/15), and each is 6–23 words.
- **Verdict freshness: improved** (0/4 → 4/4 as reported).

### No harm to owned axes (static)

- `SCORECARD.md`: the diff is append-only. Axis ratings stay 10 → 10 and no
  capability is self-awarded.
- `git diff --name-status --diff-filter=MDRT 22c1669 36b6b21` lists only these
  modified files: LOG, PROVINCE, SCORECARD, SKILL, QUALITY, README, SOURCES and
  `scripts/citing_set.py`. Nothing was deleted or renamed.
- All 26 base `corpus/knowledge` files are unchanged.
- The S001–S035 rows are byte-identical: matching sha256 of the row lines at
  base and tip.
- No file under `.ufo/waves/` outside round-28 changed (0).
- For SCORECARD, LOG, QUALITY and SKILL, the base file is a byte-prefix of the
  tip.
- PROVINCE: only the Frontier bullet changed. The Core rule "Ground moves to
  Core only with source-backed entries and a gate" is kept.
- Gate behaviour on real inputs: evidence-verified only
  (`w1a3/RunRealInputParity.md`: byte-identical JSON on the r26/r27 frozen
  inputs; `w1a3/RunNoHarmSuites.md`: six suites identical).

| Axis | Verdict | Basis |
|---|---|---|
| operability | improved | C1 4/15 → 15/15 (receipts and committed self-test evidence; static labels re-measured) |
| freshness | improved | C2 0/4 → 4/4 (re-measured); 15/15 quotes found live |
| depth / coverage / calibration / adjacency | unchanged | no claim; no regression seen in the static checks |

## Round shape

- Wave 1 `w1a3`: 38 seats (`w1a3-dispatch.json` `counts.spawn` 38). Roles:
  scribe 11, reviewer 8, mutation-tester 8, critic 4, executor 4, connector 2,
  scout 1.
- Residual call: 8 seats (`residual-call.json`: reviewer 5, critic 3).
- Committed reports: 38 + 8.
- Total 46, inside 32–100. Wave 1 sits inside the v1 band of 32–64.
- Attack seats: 20/38 in wave 1 and 28/46 overall, both above 25%.
- No wave 2 was run, below the ≥32-attack-item trigger, and the report
  discloses this. Seven seat reports overran their length limits; the report
  lists all seven.

## Discernment spot-check

| Item | Gate decision | Source I re-opened | Agree? | Reason |
|---|---|---|---|---|
| S036 Gate quote ("a good threshold to measure is the 75th percentile of page loads, segmented across mobile and desktop devices.") | admit | https://web.dev/articles/vitals (200, 10:01:08Z) | agree | Exact substring of visible text, 18 words. It supports the entry's p75 rule and its per-device segmentation. |
| S038 Gate quote ("A page must be publicly discoverable to be considered for inclusion in the CrUX dataset.") and row S038 | admit | https://developer.chrome.com/docs/crux/methodology (200) | agree | Exact substring, 15 words, under the "Publicly discoverable" heading. Also confirmed: the entry's origin-level aggregation sentence and the 20% ineligible-traffic exclusion. |
| S037 anchor cell, first draft "Core Web Vitals thresholds table and the LCP, INP and CLS sections" | reject (corrected to "Table under Refresher: Core Web Vitals metrics and thresholds, …", lesson `## Gate` "Registry changes") | https://web.dev/articles/defining-core-web-vitals-thresholds (200) | agree | "Core Web Vitals thresholds table" occurs nowhere in the page text. "Refresher: Core Web Vitals metrics and thresholds" and "Whether to have the same or different criteria" both occur. The rejected label could not be located, and the replacement can. |
| New row S039 and its quote ("The data in the Chrome UX Report is a 28-day rolling average of aggregated metrics.") | admit | https://developer.chrome.com/docs/crux/api (200) | agree | Exact substring, 15 words, ≤25. The entry's "about two days behind" also appears in the page ("approximately two days behind today's date"). |

- The C2 frontier gate itself recorded no source-level reject this round
  (SOURCES Search log: "Identified 4, screened 4, included 4 … excluded 0").
  The reject I sampled is a cell-level correction recorded in `## Gate`.
- I also checked the entry's INP poor-bound sentence against S037: 300 ms was
  considered and set aside because INP has an inverse correlation with
  popularity, and 500 ms was chosen. Agree.
- I checked the SKILL threshold table against the S037 table quote
  (≤2500/>4000 ms, ≤200/>500 ms, ≤0.1/>0.25). It matches.
- Census:
  `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kake`
  exits 0, printing `kake W04 S033 duplicate url www.rfc-editor.org/rfc/rfc9110.txt across scopes`
  and `kake ok …/corpus/SOURCES.md`. The W04 warning predates the round.

## Trend verdicts

- **expansion: improved.** Field performance was listed as open Frontier
  ground at base (`PROVINCE.md`). The round adds one knowledge entry,
  `corpus/knowledge/field-performance-cwv.md` (`A`). It cites four new
  `mined` tier-A rows and adds a README coverage row ("Field performance
  (r28)"). The entry passed my quote re-check.
- **quality: unchanged.** No existing entry was re-verified, deepened or
  superseded: the diff over the 26 base knowledge files is empty, and no
  entry was found false. The C1 repair strengthens a gate instrument and is
  credited on the operability axis, not on the corpus-quality observable in
  LEARNING.md.
- **discernment: improved.**
  - The outside spot-check agrees with the gate on admits (S036, S038, S039)
    and on the sampled reject (the S037 anchor).
  - Two new `QUALITY.md` criteria are grounded in this round's lesson
    `## Mistakes`: "A counter must be able to reject a constant", with a
    "Fails if" line and the `MutRefuseAllGate` mutant, and "No field data is
    not a pass", grounded in S036/S038/S039.
  - Round-27 routed defects 3 and 4 became criteria.

## Admission

Both declared claims verify at their declared values, against targets frozen
before measurement. No owned axis is harmed. **Admitted.** No capability is
added to the SCORECARD capability table (none was claimed). No promotion,
mint, SHONEN `[x]` or state advance is made here.

For the operator: SHONEN box 1 (SKILL "Field performance triage — round 28"
decision tables with cited S036–S039) looks checkable by a non-author.
Promotion is operator-owned.

## Routed defects (kake, next round)

1. The gate's committed self-test (`scripts/citing_set_selftest.py` over
   `scripts/fixtures/citing-set`) still has 29 cases. No fixture asserts the
   round-28 reason codes; `git grep` finds them only in
   `scripts/citing_set.py`. The regression coverage lives only in the
   round-scoped C1 counter. Add committed fixtures with expected exit and
   finding id (§Gate standard, Self-test).
2. Round-27 failure families outside the declared C1 set remain open:
   - the `JSON-PROTOCOL` duplicate-key and nonfinite cases;
   - `S01`-style ids measuring clean;
   - repeated CLI options taking the last value;
   - a deep-corpus traceback and missing `O_NOCTTY`.

   "Routed defect 1 repaired" holds only for the declared 11-case subset.
3. Two counter limits are disclosed and still open. The C1 counter checks
   finding ids, not reason codes, and K4 trusts the measured commit's own
   runner. The C2 counter checks quote shape, not quote truth, and lets the
   entry header alone cite each id. A future counter should check reason codes
   and match quotes against retained source text.
4. The frontier step screened only the four sources it then admitted
   (excluded 0). Record at least one screened-and-rejected candidate, or state
   why none was screened, so the outside reject sample comes from the source
   gate itself.
5. Untracked `.ufo/waves/round-26/__pycache__/` is pre-round generated
   bytecode (2026-10-21 17:04–19:01 -03:00). Remove it or ignore it in the lane.
