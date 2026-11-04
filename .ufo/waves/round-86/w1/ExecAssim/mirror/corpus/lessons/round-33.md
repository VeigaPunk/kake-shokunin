# Round 33 — structured refusal codes for the citing-set runner; ds4cc source pin advanced to 7fc6aa2f

## Claims

Declared before implementation in `SCORECARD.md` section "Round 33 — declared
claims" (commit `bc6c4a8d435473f3c30903210be30d9d6e3ef750`, which also carries
both counters; the declaration states no clock time of its own). Base
`5777d5af79cac1ebf9144b348a9d274099e77338`.

- C1 (operability, round-32 routed items 2 and 3): the runner
  `scripts/citing_set_selftest.py` reports a structured `code` next to the
  human `reason` for setup refusals (`setup_commit_before_init`,
  `setup_commit_without_repo`, `setup_failed`), the hostile selftest gains a
  spec key `reason_code`, and P6 keys on it instead of `reason_contains`.
  Counter `.ufo/waves/round-33/c1_code_probe.py` (four runner variants; a kill
  counts only with `guard_ok`; a timeout is a recorded verdict): met 2/4 at
  base, 4/4 at `b1752a2`.
- C2 (freshness, sourced claim on S065): the corpus' ds4cc-marketplace pin
  advances from `1fbdb8ed` to upstream `7fc6aa2f`; four files retained by
  path, mode and blob id; section `## Round-33 ds4cc source pin 7fc6aa2f` in
  `corpus/knowledge/sitemap-orphan-audit.md` states the sitemap loc count and
  three canonical verdicts that the counter re-derives. Counter
  `.ufo/waves/round-33/c2_pin_count.py`: met 0/4 at base, 4/4 at `b1752a2`.

## Gate

### Source openings

| id | source | opened | located quote (≤25 words) | decision |
|---|---|---|---|---|
| S065 | https://github.com/VeigaPunk/ds4cc-marketplace/commit/7fc6aa2fc12451dd451fed5a9ee7125f3a90e884 (read through a sandbox clone at `/fast/scratch/hyaku/kake-r33/ds4cc-upstream`, `git clone` of the public repository, clone made 2026-10-22T19:49:58Z per wave-1 `CriticDeclarationOrder`) | 2026-10-22 | “`<link rel="canonical" href="https://ds4cc.com/magga/frostbite/">`” (magga/frostbite/index.html line 9; 3 words); “`<url><loc>https://ds4cc.com/magga/frostbite/</loc></url>`” (sitemap.xml line 15; 1 word) | admit, tier A for the files' own content at that commit, status `mined` |
| S066 | https://api.github.com/repos/VeigaPunk/ds4cc-marketplace/actions/runs?head_sha=7fc6aa2fc12451dd451fed5a9ee7125f3a90e884 and https://api.github.com/repos/VeigaPunk/ds4cc-marketplace/actions/workflows/apps-sdk.yml/runs?branch=main&per_page=6 (`gh api`, L1, 2026-10-22T20:05:11Z and 20:06:32Z; both responses retained under `.ufo/waves/round-33/sources/`) | 2026-10-22 | “"name":"Deploy marketplace to GitHub Pages" … "status":"completed","conclusion":"success"” (run 39644779773 object; 6 words) | admit, tier A for GitHub's own run record, kind `dataset`, status `mined`; first written with kind `api`, which the census refused (`E05 S066 kind=api`), changed to `dataset` before commit |

Row changes logged old→new: S065 new (`—` → `mined`, opened `2026-10-22`,
recheck `90d`, used-by `corpus/knowledge/sitemap-orphan-audit.md`). No other
row's status, recheck or used-by cell changed. S066 new (`—` → `mined`, opened `2026-10-22`, recheck `90d`, used-by `corpus/knowledge/sitemap-orphan-audit.md`).

## Mistakes

| Class | Evidence | Captured-by | Fix |
|---|---|---|---|
| a repair counter accepts a faked repair at its declared after-value | The round-32 C2 counter `.ufo/waves/round-32/c2_retained_count.py` (frozen at `5b32cc7`) scores 3 both on the landed repair `e9283ec` and on hollow commit `6ffa03e` (the two ds4cc blobs at `scripts/fixtures/unrelated/{a,b}.txt`, a fabricated row `S099` inside `## Registry`, one unrelated mention of it); before `a0b0dff` scores 0. Built by wave-1 seat `ScribeMistakeMine`; the hollow commit is retained as `.ufo/waves/round-33/verification/hollow-r32-c2-6ffa03e.bundle`. The round-32 closure had to re-measure C2 by hand. | none: round-32 wave-1 seats saw the looseness (`.ufo/waves/round-32/w1/CriticC2Scope.md`, `MutC2Conditions.md`), but no rule required a counter to score a hollow control below its after-value before its `met` was read as evidence. | `corpus/QUALITY.md` "Round-33 criteria", second bullet, with `.ufo/waves/round-33/criteria/counter_control_check.py`. Shown able to fail: exit 1 on the round-32 counter with the bundled hollow commit (`verification/criterion-counter-control-r32-c2.txt`). |
| seat report misrooted into the fleet repo | Wave-2 seat `ScoutPinsFlagAccuracy` wrote its report at `/home/vgpnk/Projects/shokunin/.ufo/waves/round-33/w2/ScoutPinsFlagAccuracy.md` (fleet root) instead of under the lane, although the wave context said every `Report:` path is relative to the lane; found by the misroot sweep (`git -C /home/vgpnk/Projects/shokunin status --porcelain`), copied byte-exact into the lane (`cmp` identical) and the fleet copy deleted. | the round prompt's misroot sweep (§6.3) caught it after the fact; nothing prevents it at write time. | none landed this round: the sweep stays the catch. The wave context already carries the rule; a seat-side check is not in the lane's write scope. |

| absent-path annotation (r43 re-census 2026-10-23) | `/home/vgpnk/Projects/shokunin/.ufo/waves/round-33/w2/ScoutPinsFlagAccuracy.md` is absent — the fleet-root copy was removed by the round-33 misroot sweep; the byte-exact lane copy survives at `.ufo/waves/round-33/w2/ScoutPinsFlagAccuracy.md`. Historical incident record, not an executable path. | freshness sweep §paths gate (unannotated miss + newMissing) | This annotation row: the citation above carries its own absence wording within ±2 lines, and the token is entered in `corpus/knowledge/freshness-pins.json` `pathsMissSet` in round 43. |

The same criterion applied to this round's C2 counter: its hollow shape
(bytes at an unrelated path) drops c1 and therefore c4, so it scores at most
2 of 4. A different hollow shape still scores 4 (wave-1
`MutC2HollowCommit.md`: a junk S065 row with the right id, status, date,
used-by and hash, plus copied metrics; also a misplaced section and an
even-backslash pipe). The round-33 counter checks provenance shape and the
truth of the stated numbers against retained bytes, not that the row's
prose came from source study; the landed row was checked by hand and by an
independent draft that matched it cell for cell (`w1/ScribeS065RowDraft.md`).

## Round-32 routed defects — disposition

| # | Item | Disposition |
|---|---|---|
| 1 | Git-pin mutants m3d, m3f, m3g survive | Not killed. Wave-1 `ExecPinMutantsP7`: with the committed setup vocabulary, m3d and m3f leave the victim unchanged (a valid `git_init`/`git_commit` binds the copied case's own repository), so their setup-pin removals are equivalent for every observable the harness checks; m3f and m3g both drop the gate ceiling, which changes the gate's structured finding for P7 case h7b (`revision_not_found` → `root_not_repository_top_level`), but both runs exit 2 and the harness reports only a generic exit mismatch (`w1/ExecPinMutantsP7.md`; P7 stays in that seat's sandbox, not committed). Killing m3f and m3g would need the harness to expose gate findings or codes per case; carried open. |
| 2 | Refusal keyed on message text | Fixed: C1 (runner `code`, `reason_code`, P6); strict supplement; QUALITY criterion 1. |
| 3 | Probe kill not gated, timeout raises | Fixed in the new probe `c1_code_probe.py`; the round-32 probe is not reused (QUALITY criterion 1). Wave-1 `ReviewC1ProbeCode.md` lists six low residuals (no git timeout, missing-script crash exit 1, harness-error P6 read as refusal — the strict supplement's s4 code check covers that case). |
| 4 | Round-32 C2 counter defects | Not reused; replaced by `c2_pin_count.py` (row-id, path, mode and section pins; `w1/ReviewC2CounterCode.md`: five of seven fixed, fence-blind section split still present; new low defects N1–N5); mistake row above. |
| 5 | PROVINCE "five hostile shapes" | Corrected by append (`PROVINCE.md` "Round-33 frontier step"). |
| 6 | Concurrent selftest collision | Fixed: per-run private default scratch; 0 of 4 concurrent runs failed after, 3 of 4 at base. |
| 7 | Round-31 item-3 low items | `read_expected` OSError and stray fixture-root entries fixed; duplicated option tables not fixed (the proposed patch imports the gate from the runner's directory and breaks runner copies run from a temporary path). |

## Carried open

- Round-31 `CriticQualityCriteria` F1–F3: still open at `bc6c4a8`; proposed
  checks in `.ufo/waves/round-33/w1/ScoutQualityCriteriaCanFail.md`, not
  landed this round.
- `ReviewMistakeSweep.md` candidates 1, 2, 5–7 (counter attribution,
  receipts captured on a census-failing tree, receipt/commit order,
  stale docstrings, S062 header omissions); 3 and 4 were repaired this
  round in the hostile selftest.
- `freshness-pins.json` `pq2Remote` and `sitemapStatus` stale (needs an
  armed sweep run).
- Round-31 `ReviewProvinceReadme` F1/F2: resolved by the round-31 narrowing
  paragraph (`w1/ScoutProvinceLiveFetchWording.md`); no change needed.

## Wave-2 corrections (appended)

- Row 1 above: the harness already reports per-case `codes`; what m3f/m3g
  would need is the runner populating `code` for gate-run refusals (null
  outside setup refusals today) and a spec asserting it
  (`w2/ReviewRoutedDisposition.md`).
- Row 3: five low residuals and one latent note, not six low.
- Row 4: `ReviewC2CounterCode` N1 (non-UTF-8 `SOURCES.md` crash) is rated
  medium there, not low; F2 and F3 are partly fixed.
- Row 7: the `read_expected` change is defensive. No tried shape raised an
  OSError past it at base (`w2/ExecReadExpectedRepro.md`), and the new
  `except OSError` branch in `run_case` is unreachable
  (`w2/ReviewScratchDefaultDiff.md`). The stray-entry refusal is not pinned
  by any committed check (`w2/MutStrayEntriesCheck.md`); at `e490381` it also
  turned stray symlinks into exit 2, reverted for symlinks at `3abfc44`.
- Code propagation mutants: all five killed by the hostile selftest, the C1
  probe and the strict supplement together; mutant D passes the hostile
  selftest and the frozen probe and is caught only by the strict supplement
  (`w2/MutRunnerCodePropagation.md`).

## Carried open (wave 2)

- Pre-existing at base and tip: a NUL byte in a `git_commit` message or an
  argv value escapes as `ValueError` and crashes the runner with no JSON
  summary (`w2/ReviewRunnerCodeDiff.md`).
- Run-level failure entries (`case: null`) carry no `code` key.
- A dot-named stray file such as `.gitignore` in the fixture root now makes
  the runner exit 2 while dot-named directories are skipped
  (`w2/ReviewScratchDefaultDiff.md`).
- `freshness-pins.json` re-pin (three values) and the unqualified count
  statements listed in the entry's wave-2 corrections.
