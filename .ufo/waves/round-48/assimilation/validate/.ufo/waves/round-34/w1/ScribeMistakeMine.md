# ScribeMistakeMine — round-34 lesson `## Mistakes` rows (draft)

Seat `KakeR34.ScribeMistakeMine` (scribe, leaf). Axes: operability, freshness. Milestone r34-build.
Base of my sandbox clone: `a2fe31b2d1d2bf67f832b31fb994869b83dbdb9f` (verified `rev-parse HEAD`).
Lane `## Gate`/lesson facts read with `git show a2fe31b2:` from the clone, never from the working tree.
Only lane write: this file. No jj, no network, no tool installs.

## Rows (verbatim, for `corpus/lessons/round-34.md` `## Mistakes`)

| Class | Evidence | Captured-by | Fix |
|---|---|---|---|
| committed text cited evidence that existed only in sandbox scratch, so the pointer does not resolve from committed bytes | `.ufo/waves/round-33/verification/c1-strict-at-critic-489714b.json` names commit `489714be`, which lived only in `/fast/scratch/hyaku/kake-r33/w1/CriticC1RepairScope/clone` (lane tree lacks the object: `w2/RerunC1Strict.md:24-29`); the option-table `patch.diff` cited by `w2/CriticOptionTableRejection.md` was likewise sandbox-only | routed defect 2 of `corpus/lessons/round-33-verifier-spotcheck.md`; found in-round by `w2/RerunC1Strict.md:24` | Retained in the lane: `.ufo/waves/round-34/retained/r33-c1-counterexample-489714be.bundle` (sha256 `6ff6c403c4df5b2a…77c00`), `r33-option-table-dedup-patch.diff` (`28fd9adf5f30…7d6e`), `r33-option-table-alt-patch.diff` (`daeaa738525e…ce6e`). Resolution check, shown able to fail: into a clone at `a2fe31b2`, `git fetch <bundle> 'refs/tags/*:refs/tags/*'` exits 0 and `git cat-file -p 489714be` shows `parent bc6c4a8d…` with a 2-file diff (raise line + `reason_contains`); the same fetch against a nonexistent path exits 128. Limit: the bundle is thin (header `-bc6c4a8d…`), so `git clone --bare <bundle>` alone exits 128 `Repository lacks these prerequisite commits` — it resolves only where `bc6c4a8` is already present |
| a Gate that records admits only, so no reject can be sampled from it | `corpus/lessons/round-33.md` at `a2fe31b2` `## Gate` holds two rows (`:31` S065, `:32` S066), both decision `admit`; `grep -cE '\| (admit\|reject)'` over the section is 2 and the tally is `2 admit`; the closure had to fall back on a code patch for its admit+reject sample | routed defect 3 of `corpus/lessons/round-33-verifier-spotcheck.md` ("the round-33 `## Gate` records no reject") | `python3 -B .ufo/waves/round-34/criteria/gate_reject_check.py` — receipt `<pending>` (built by another seat; `.ufo/waves/round-34/criteria/` did not exist at my read: `ls` exit 2). The check must exit non-zero on a Gate table whose decision column has no reject row, and accept one that has it |
| the report cited a run with no receipt | `/home/vgpnk/Projects/shokunin/.ufo/reports/round-33/kake.md:62` states "`93359ff`: 4/4 (run, not committed)"; `.ufo/waves/round-33/verification/` holds receipts only for `5777d5a`, `bc6c4a8`, `b1752a2`, `e490381`, `1cf452e`, `3abfc44` — `ls | grep -c 93359ff` is 0 | routed defect 4 of `corpus/lessons/round-33-verifier-spotcheck.md` | `python3 -B .ufo/waves/round-34/criteria/receipt_presence_check.py` — receipt `<pending>` (built by another seat, absent at my read). The check must fail on a report line naming a revision with no `verification/*<rev>*.json` receipt, and pass where one exists |
| the corpus cited wave-1 reports that were not present in the revision it named | `w2/CriticC2Verdict.md:50-58`: `git ls-tree -r 0a0acfb .ufo/waves/round-33/` contains no `w1/` path, yet `corpus/knowledge/sitemap-orphan-audit.md:220-253`, `SKILL.md:935,941,944`, `SCORECARD.md:1131-1163` and `corpus/README.md:307` cite those files; the reports landed only at `d2ed431` | none — `w2/CriticC2Verdict.md` observed it in-round; no rule required path presence at the citing revision | `<pending>` — no check exists in this wave. Smallest check: for every `.ufo/waves/<round>/w<N>/<file>.md` path named in tracked docs at revision R, assert it appears in `git ls-tree -r R`; the failing sample is `0a0acfb` (0 `w1` paths, 5 citing sections) |
| the round's reading record undercounted its own network reads (recurrence) | `w2/CriticC2Verdict.md:29-47`: PROVINCE.md:146-147 as written at `0a0acfb` said "only network reads" and named one clone plus two listings, against 6 Git clones, 2 `ls-remote`, 5 `gh api` reads, 2 unauthenticated 403 GETs and 1 commit-page GET recorded in the wave reports; same class as `w1/ScoutProvinceLiveFetchWording.md:17-26` (round-31/32 pattern); corrected by append at `d2ed431` | none — the seat's overclaim check found it; no lesson row carried the round-31 recurrence forward | `<pending>` — no check exists in this wave. Smallest check: derive the round's fetch tally by grep from the wave reports (`git clone|ls-remote|gh api|curl`) and require the PROVINCE sentence's counts to equal it, with the round-33 tally as the failing sample |

## Sweep of round-33 wave reports (commands and output summaries)

```
cd <lane>/.ufo/waves/round-33
ls w1 | nl            # 35 entries + swarm-registry.json
ls w2 | nl            # 34 entries + swarm-registry.json
grep -rniE 'no receipt|not committed|unreceipted|sandbox only|only in (my|the) sandbox|overclaim|over-claim|misstat|wrong|incorrect|cannot be (proved|shown)|unprovable|stale docstring|contradict' w1/*.md w2/*.md
```
Output: 33 matching lines. Triage of the matches against the round-31/32/33 `## Mistakes` rows and both routed-defect lists:

- Kept as new rows: `w2/CriticC2Verdict.md:29` (read-record undercount) and `:50` (dangling report cites).
- `w1/ReviewC1ProbeCode.md:5` ("only in the sandbox clone: ca647be") — same class as row 1, covered there.
- `w1/ReviewC2CounterCode.md:31` (mutant revs "in sandbox only") — counter-limit disclosure, already in SCORECARD "C2 counter scope"; not an evidence pointer.
- `w2/RerunC1Strict.md:24` ("No receipt exists for tip 0a0acfb") — same class as row 3; one row covers it.
- `w2/RerunC1Strict.md:86` (guard regex would cut a multi-line raise → kill for the wrong reason) — a limit of the strict supplement, disclosed and not triggered at tip; not a mistake.
- `w2/ReviewHostileHardening.md:40` (unreadable spec dir crashed exit 1) — a code defect fixed at `3abfc44` and recorded in the round-33 lesson disposition, not a report-side mistake.
- `w2/ScoutPinsFlagAccuracy.md:42`, `:56` (the 29-commit distance reads as if it applied to the checkout; grammar) — low, prose ambiguity, no rule violated.
- `w1/ScoutUpstreamCommitAnatomy.md:18` ("png attrs wrong") — a property of the upstream image markup, not lane text.
- `w2/CriticC2Verdict.md` PROVINCE and `w2/CriticHarmCheck.md` stray-symlink change — the latter is already in `corpus/lessons/round-33.md` wave-2 corrections row 7.

Not read line by line: 67 reports were covered by the grep plus 4 targeted reads (`CriticC2Verdict`, `RerunC1Strict`, `ReviewHostileHardening`, `ScoutPinsFlagAccuracy`); a mistake phrased without any of the sweep terms would be missed.

## Facts re-derived (commands, exit codes, output)

- `git clone -q <lane> <sandbox>/clone && git -C <clone> checkout -q a2fe31b2…` → 0; `rev-parse HEAD` = `a2fe31b2…`.
- `git show a2fe31b2:corpus/lessons/round-33.md | sed -n '/^## Gate/,/^## Mistakes/p' | grep -cE '\| (admit|reject)'` → `2`; tally `2 admit`.
- `ls .ufo/waves/round-33/verification/ | grep -ci 93359ff` → `0`; the 18 c1/c2 receipts name `5777d5a`, `bc6c4a8`, `b1752a2`, `e490381`, `1cf452e`, `3abfc44`, `489714be` only.
- `git clone -q --bare <retained bundle>` → 128 `Repository lacks these prerequisite commits: bc6c4a8d…`; `git clone -q --bare <clone> && git fetch <bundle> 'refs/tags/*:refs/tags/*'` → 0, `cat-file -p 489714be` → `parent bc6c4a8d…`, `diff --stat` → 2 files, 2 insertions, 2 deletions.
- `grep -n 'from citing_set import build_parser' .ufo/waves/round-34/retained/r33-option-table-dedup-patch.diff` → `44` (the closure's "lines 43–44" refers to the sandbox copy; retained copy line 44).

## Findings for the L1 (advisory)

1. The retained bundle is a thin bundle. If the closure must resolve it without the lane history, re-cut it as a self-contained bundle (`git bundle create --all`) or add the prerequisite commit.
2. Two of the five rows (`dangling report cites`, `read-record undercount`) have no failing check today; both names are `<pending>` and need an owner before the lesson claims a shown-able-to-fail fix.
3. The Gate row's check (`gate_reject_check.py`) was absent when I looked (`.ufo/waves/round-34/criteria/` did not exist), so its receipt is genuinely `<pending>`, not a passed check.

## Not verified

- Did not run `gate_reject_check.py` or `receipt_presence_check.py` (absent).
- Did not read all 71 round-33 wave reports in full.
- Did not re-measure the round-33 claims themselves; my checks re-derive only the lesson/Gate/receipt facts the rows cite.
