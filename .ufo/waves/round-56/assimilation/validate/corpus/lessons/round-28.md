# Round 28 — repair the citing-set gate interface, learn field performance

## Claims

Declared before implementation in `SCORECARD.md` section "Round 28 — declared
claims" (commit `84ea5b15f164d32907182745b7887feb40b5ddd4`), unchanged in
attempt 3.

- **C1, operability, repair-first.** Round-27 routed defect 1: unusable input
  documents yield the contracted JSON report with exit 2, and an absent or
  unreachable corpus surface does not return clean. Counter
  `.ufo/waves/round-28/c1_interface_count.py`; before 4/15 at `22c1669`,
  declared after 15/15. Repair commit `b5d423fc02057f67a6f3a255808313ce40d29069`.
- **C2, freshness, frontier.** Field performance (Core Web Vitals thresholds
  and CrUX eligibility) enters held knowledge as
  `corpus/knowledge/field-performance-cwv.md`, grounded in S036–S039 opened
  this round. Counter `.ufo/waves/round-28/c2_source_count.py`; before 0/4,
  declared after 4/4.

## Gate

### Source openings

Each source was opened with one public GET by the L1 in attempt 3 (HTTP 200,
2026-10-22T09:29:23Z to 09:29:26Z) and again by the wave-1 source seats
(`.ufo/waves/round-28/w1a3/Src*.md`). Visible text was derived as HTML minus
script and style, tags removed, entities decoded, whitespace collapsed; each
quote below is an exact substring of that text. Received-body digests are in
`.ufo/waves/round-28/sources/receipts-a3.json`; the attempt-2 receipts in
`receipts.json` hold the earlier opening of the same pages, and all 16 of its
quotes were found again in attempt 3.

- S036 — https://web.dev/articles/vitals — accessed 2026-10-22, section Core Web Vitals: “a good threshold to measure is the 75th percentile of page loads, segmented across mobile and desktop devices.”
- S037 — https://web.dev/articles/defining-core-web-vitals-thresholds — accessed 2026-10-22, section Refresher: Core Web Vitals metrics and thresholds: “if at least 75 percent of page views to a site meet the "good" threshold, the site is classified as having "good" performance”
- S038 — https://developer.chrome.com/docs/crux/methodology — accessed 2026-10-22, section Publicly discoverable: “A page must be publicly discoverable to be considered for inclusion in the CrUX dataset.”
- S039 — https://developer.chrome.com/docs/crux/api — accessed 2026-10-22, section The rolling average: “The data in the Chrome UX Report is a 28-day rolling average of aggregated metrics.”

### Further located support for the entry

| Row | Section | Located quote (≤25 words) |
|---|---|---|
| S036 | Core Web Vitals lifecycle | `LCP : Stable CLS : Stable INP : Stable` |
| S036 | Lab tools to measure Core Web Vitals | `While lab measurement is an essential part of delivering great experiences, it is not a substitute for field measurement.` |
| S036 | Stable | `Stable Core Web Vitals metrics won't change more than once per year.` |
| S037 | Refresher: Core Web Vitals metrics and thresholds (table) | `Largest Contentful Paint ≤2500 ms >4000 ms 75 Interaction to Next Paint ≤200 ms >500 ms 75 Cumulative Layout Shift ≤0.1 >0.25 75` |
| S037 | Whether to have the same or different criteria per device | `the Core Web Vitals recommended thresholds are not segregated by device and the same threshold is used for both.` |
| S038 | Publicly discoverable | `The page is served with an HTTP status code other than 200 (after redirects).` |
| S038 | Sufficiently popular | `An exact number is not disclosed` |
| S038 | Origin | `eligible user experiences on all of that origin's pages are aggregated at the origin-level, regardless of individual page discoverability.` |
| S039 | CrUX API Key | `Using the CrUX API requires a Google Cloud API key provisioned for Chrome UX Report API usage.` |
| S039 | Rate limits | `The CrUX API is limited to 150 queries per minute per Google Cloud project, which is offered without charge.` |
| S039 | UrlNormalization | `Complex actions like following redirects are not handled.` |

### Registry changes (old → new)

- S036, S037, S038, S039: no row → new rows, status `mined`, opened
  `2026-10-22`, recheck `90d`, used-by `corpus/knowledge/field-performance-cwv.md,
  corpus/lessons/round-28.md`.
- No pre-existing row's status, recheck or used-by cell changed.
- One Paths line (Field performance) and one Search log paragraph (Round 28)
  were appended.
- S037 anchor cell, added this round, corrected after residual
  `ReviewGateQuotes`: "Core Web Vitals thresholds table and the LCP, INP and CLS
  sections" → "Table under Refresher: Core Web Vitals metrics and thresholds,
  the LCP, INP and CLS sections, and Whether to have the same or different
  criteria per device". The S037 Gate and table labels were corrected the same way.

## Mistakes

| Class | Evidence | Captured-by | Fix |
|---|---|---|---|
| Proxy counter: the measured after-value was a finite surrogate that a constant gate could satisfy, so a green count did not entail the declared clause | Round 27: `corpus/lessons/round-27-verifier-spotcheck.md:21` (a constant returning the 16 pairs passed the finite predicate); `.ufo/waves/round-27/unresolved-acceptance.json`. Round 26: `corpus/lessons/round-26-verifier-spotcheck.md:11,13` | partial — `corpus/QUALITY.md` round-24 and round-27 author-closure rules (lines 161 and 285–289) rejected a fixed-output predicate after the fact, but no criterion required a counter to carry valid-input controls that a constant fails | The round-28 C1 counter carries four controls (K1 valid clean working tree, K2 valid clean Git read, K3 a real omission stays failed, K4 the 29-case fixture runner). Shown able to fail: `.ufo/waves/round-28/w1a3/MutRefuseAllGate.md` (a refuse-everything gate passes all 11 defect checks and is still rejected by the controls). New criterion in `corpus/QUALITY.md` section "Counters and field evidence — round 28" |
| Repair over-refusal: the round-28 C1 repair `b5d423f` refused a bare repository and a top level whose name ends in a space, which the base gate measured correctly | `.ufo/waves/round-28/w1a3/CriticOverReject.md`; `.ufo/waves/round-28/verification/c1-root-env-matrix.json` (column `b5d423f`) | none — the C1 counter's controls use only an ordinary top-level checkout, so 15/15 could not see it | `8ecbefe` checks `git rev-parse --show-prefix` instead of comparing realpaths; `5a83d13` drops inherited `GIT_DIR`-family variables. Shown able to fail: the committed matrix `.ufo/waves/round-28/verification/c1_root_env_matrix.py` reports the `b5d423f` gate refusing rows B1 and T1 and the `8ecbefe` gate returning `clean` for rows E1–E4 |

Misroot sweep (`git -C /home/vgpnk/Projects/shokunin status --porcelain`,
run before the report): no file written by a kake round-28 seat was found at
the fleet root; every seat report is under `.ufo/waves/round-28/w1a3/` or
`.ufo/waves/round-28/residual/` in the lane.

## Follow-up repairs from the falsifiers

Each landed after the C1 after-value was first measured and each was
re-measured (counter 15/15, fixture selftest 29/29):

- `8ecbefe`: top-level check by `--show-prefix` (wave-1 `CriticOverReject`).
- `5a83d13`: Git subprocesses ignore inherited `GIT_DIR`, `GIT_WORK_TREE` and
  the other `git rev-parse --local-env-vars` names; docstring names
  `git_unavailable` (residual `CriticC1FollowUp`, wave-1 `ReviewDocstringContract`,
  `ReviewGitTopLevel`, `ReviewBlankRevision`).
- `e73d48b`: a `MemoryError` while parsing JSON yields `document_not_json`
  with exit 2 instead of a traceback (`ReviewJsonDepth`); a symlink or gitlink
  at `corpus/knowledge` in Git mode keeps its base reason label (`ReviewGitCorpusBlob`,
  `ReviewCorpusMissingEmpty`).

## Open findings, not repaired this round

- Round-27 failure families outside the declared C1 set still fail: population
  ids such as `S01` or `S1` measure clean, repeated `--population`, `--ledger`,
  `--revision` or `--root` options silently take the last value, and duplicate
  or nonfinite JSON is accepted (`w1a3/CriticCounterFaithful.md`).
- The C1 counter can be satisfied for the wrong reason: it checks finding ids
  but not reason codes, K4 trusts the measured commit's own fixture runner, and
  repo-local Git attributes or an inherited `GIT_DIR` can change what it
  exports (`w1a3/CriticCommittedBytes.md`). The landed gate's per-case reason
  codes were recorded separately and match each attacked defect
  (`verification/c1-after-e73d48b.json`).
- The C2 counter checks quote shape, not quote truth, and the entry header
  alone counts as citing each id (`residual/CriticC2Counter.md`). Quote truth
  was checked outside the counter: 15/15 Gate quotes are exact substrings of the
  retained texts (`residual/ReviewGateQuotes.md`).
- A corpus directory about 990 levels deep crashes the recursive walk with a
  traceback (pre-existing, `w1a3/ReviewCorpusMissingEmpty.md`); device opens
  lack `O_NOCTTY` and a socket is labelled unreadable (pre-existing,
  `w1a3/ReviewNonBlockingRead.md`); the JSON depth limit depends on the stack
  size under CPython 3.14 (`w1a3/ReviewJsonDepth.md`).
- S038 has two sentences that disagree on whether page-ineligible experiences
  count at the origin level; the entry quotes both (`residual/ReviewEntryCrux.md`).

## What this round does not claim

- No CrUX or PageSpeed API call was made and no lane property was measured.
- C1 covers the 11 named round-27 failures plus 4 controls. Duplicate-key and
  nonfinite JSON profiles, identity-path spelling and retention boundaries stay
  open, as declared.
- The round-27 strict C1 unknowns (7 units across 3 pairs), the round-24
  policy stop and the out-of-population debt are unchanged.
