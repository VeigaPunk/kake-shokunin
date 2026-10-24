# KakeR40.ExploratoryVerdictC1 — advisory verdict on C1 (round 40)

**Verdict: `unprovable-but-better`** (advisory; the verdict of record belongs to the non-author closure).

## What I checked (commands, exit codes)
- `git diff f171c58b 56d57ee4 -- scripts/` — only `sitemap_audit.py` (3 hunks: E NUL guard @185-189, U `_parse_url` guard @69-71, R duplicate-before-typegate @334-348) + selftest + SKILL.md; no other code touched (build diffstat 6 files).
- `git show 56d57ee4:scripts/sitemap_audit.py | sha256sum` = `03a8fba4…7b22b` (exit 0): build bytes = L1 reference = what was scored.
- `git show f043c721:.ufo/waves/round-40/c1_count.py | sha256sum` = `6d73b8f4…` = same at `12211cc5` (exit 0): counter frozen, never changed.
- `jq -s 'map(select(.met))|length' …/verification/w1/*.json` → 27 of 76 (exit 0) — kill-rule count reproduces.
- `jq -S . .ufo/waves/round-39/verification/realrun/build-565ef4c9.json | sha256sum` and `…/realrun-build-56d57ee4.json` → both `fd985a41…`; raw file sha equal `2ffbea3a…` (exit 0): harm receipt byte-equal to round 39.
- `git archive 56d57ee4 scripts/ | tar -x` then `python3 -B scripts/sitemap_audit_selftest.py --tool scripts/sitemap_audit.py` → `PASS 179/179`, exit 0 (I ran this; 5.2 s). Red receipt `selftest-new-on-base.txt` shows `PASS 156/179`, exit 1 (23 FAILs).
- Read: base `pre/base-f171c58b.json` 10/30 (E 4/9, U 3/13, R 3/8); build `c1-at-56d57ee4.json` 30/30, selftest 150/150, met true; `preseal-f043c721.txt` exit 1 / `preseal-12211cc5.txt` exit 0 (criteria check); `d1check-{base,ref,mutant}.txt` green/green/red; all 18 wave-1 reports.

## Prior state lacked
- Base tool passed only 10/30: UTF-16-no-BOM misread as clean (E1–E5), `urlsplit`-cleaned values judged as written (U1–U10), repeat-of-invalid-id not caught (R1–R5) — `SCORECARD.md:2597`; `ReviewWitnessContract.md:12-14`.
- Selftest had zero fixtures for these shapes (150 → 179; 23 new red-on-base).
- Declaration froze the counter with author-only controls — QUALITY (o) violation, now checked by `criteria/preseal_order_check.py` (red at `f043c721`, green at `12211cc5`).

## What improved
- Build rejects the three routed classes; independent witness-vs-contract review agrees on all 30 (`ReviewWitnessContract.md:53-78`).
- Selftest 179/179 green at build (verified by me), incl. the exact sub-shapes wave-1 exploited (LF in `sitemapUrl`, leading NUL, U+001F, TAB-in-query, LF-in-fragment, UTF-16 index, upper-case repeated id) — `selftest-new-on-build.txt:1`; `SCORECARD.md:2639-2643`.
- Real run on six public sitemaps byte-equal to round 39 → no observed regression (`verification/harm/realrun-build-56d57ee4.json`).
- Kill rule (1) fired honestly before the build; no relabeling; the counter, witnesses and predicate untouched (`SCORECARD.md:2629-2654`).

## For (≥3)
1. Frozen counter: base 10/30 → build 30/30 at seed 40001, byClass E 9/9 U 13/13 R 8/8, selftest 150/150 (`verification/c1-at-56d57ee4.json:2-14`); base totals reproduced by two independent seeds (`ReviewCounterCode.md:7-8`, `ReviewWitnessContract.md:12`).
2. Selftest 150→179 with 23 red-then-green fixtures, and I independently reproduced `PASS 179/179` exit 0 at `56d57ee4` (`verification/build/selftest-new-on-base.txt:112-113`, `selftest-new-on-build.txt:1`).
3. No harm: real-run JSON byte-identical to round-39 build (sha `2ffbea3a…`), so the repair changed nothing observable on real inputs (`verification/harm/realrun-build-56d57ee4.json`; `LOG.md:1578-1580`).
4. Honest exploration: 27/76 controls met the predicate and the kill rule fired pre-build; verdict explicitly deferred to a named non-author reviewer (`SCORECARD.md:2634-2654`); C1 declared exploratory in `SCORECARD.md:2629`.
5. D1/D3 decided by source with executable checks that fail on a D1-fixed mutant (`verification/w1/d1check-mutant.txt` red, base/build green; `round-40.md:25-32`).

## Against (≥2)
1. The frozen counter cannot certify the repair: 27/76 adversary controls met it while implementing none of E/U/R — key-finder via `/proc` case-id leak (`CtlKeyFinder.md:30-32`), label replay (`CtlLabelKeyed.md:13,37`), position-keyed, proxy and partial repairs (`SCORECARD.md:2637-2647`). "30/30 + 150/150" is satisfied by tools doing zero repair.
2. Surviving one-line weakenings prove class incompleteness: E M07–M11 (`MutFamilyE.md:13-17`), U M09–M12 (`MutFamilyU.md:14-17`), R m02–m06 (`MutFamilyR.md:11-15`) all meet the frozen predicate yet fail fresh in-class probes; the new selftest still does not cover e.g. sitemapindex/https/leading-comment/long-file/no-final-newline (E) and empty/non-ASCII/intervening-id repeats (R).
3. No independent oracle backs the repair: libxml2 contradicts E1/E2/E5 (re-sniffs UTF-16), is blind on all U/R, and agrees only under a strict-UTF-8 decode (`ExecIndependentOracle.md:40-48`); the U reading rests on Python `urlsplit`/WHATWG agreement, not an RFC 3986 oracle.
4. The selftest half runs unsandboxed and is label-keyable, so even the 150/150 (now 179/179) regression cannot reject a shortcut tool (`CtlKeyFinder.md:31-32`; `ReviewCounterCode.md:17`).

## Residual risk / gaps
- The new 179 fixtures are self-authored with the build; no non-author run of the repaired tool on real adversarial inputs yet; verdict of record pending the non-author closure.
- Counter judge leniencies (`ReviewCounterCode.md:15`) and exit-2 unreachability (F1) are audit frictions, not voted defects.
- `ReviewWitnessContract.md:66-70` (F3): no witness repeats an earlier *valid* check's id; the build only handles repeat-of-invalid and is unproven on repeat-of-valid.
- Round-39 closure corrections (S110–S115, QUALITY (o)/(q)/(r), preseal check) are documented but their own verdicts belong to other seats; I did not re-audit SOURCES rows.
- Nothing observed got worse: no behavior change outside the three repair hunks; SKILL amendment marks the capability exploratory and pointers to the selftest, not the defeated counter (`SKILL.md:1136-1149`).
