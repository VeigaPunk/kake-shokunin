# ExecCensusReplay

ATTACKS: condition C7 (validate-before-append) in `.ufo/waves/round-55/c55_quote_truth.py` (lines 415-468) and the census exit it rests on — receipts `.ufo/waves/round-55/assimilation/validate/{census-argv,census-stdout,census-exit,census-stderr}.txt`, the whole-corpus mirror `assimilation/validate/corpus/`, and `validate_append.sh`; plus `sources-census.sh validate|census` verdicts for lane `kake`.

Build measured: `git -C …/kake-shokunin rev-parse a7a548e102b71bd16b0a6ddafa469393a2c98b69^{commit}` → `a7a548e102b71bd16b0a6ddafa469393a2c98b69`; `git log --oneline -1` → `a7a548e round-55: QUALITY criteria, gate registry rows, PROVINCE step, counter selftests`.
Scratch: `D=$(mktemp -d)` → `/tmp/tmp.DpyhEqSxxi`; `git -C …/kake-shokunin archive a7a548e… | tar -x -C "$D"`. `git -C "$D" rev-parse --show-toplevel` → `fatal: not a git repository` (archive extraction; expected, no git call was made inside `$D`). Lane untouched except this report; the lane's `validate_append.sh` was never executed (it writes into the lane).

## REPLAY:

1. Script bytes: `git show a7a548e…:.ufo/waves/round-55/validate_append.sh` vs the worktree copy → `diff -u` empty, `WORKTREE SCRIPT == COMMITTED`.
2. Replayed its steps verbatim in `$D` (`cd $D`; `V=.ufo/waves/round-55/assimilation/validate`; `rm -rf $V; mkdir -p $V; cp -r corpus $V/corpus`; copy the five non-corpus used-by targets `SCORECARD.md SKILL.md scripts/source_recheck.py .ufo/waves/round-41/{c1_count,oracle_crosscheck}.py`; write `census-argv.txt`; run the census; write `census-exit.txt`).
   - argv produced: `/home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --file .ufo/waves/round-55/assimilation/validate/corpus/SOURCES.md`
   - observed: `exit=0`; stdout 15 lines (14 × `file\tW04\t…` + `file\tok\t…/corpus/SOURCES.md`); stderr 0 bytes.
   - a first pass with an absolute `$V` also reproduced the receipt modulo the absolute path; the relative form above is the faithful one and is the one diffed below.
3. Committed receipts, read from the measured revision: argv = the same relative argv; `census-exit.txt` = `exit=0`; `census-stdout.txt` = 15 lines, same 14 W04 ids in the same order plus the `ok` line; `census-stderr.txt` = 0 bytes.
4. C7's equality terms, checked from committed git blobs at `a7a548e` (not from the worktree): registry `corpus/SOURCES.md` = `7ccf67999382d80437da829ea0a6028dcd179099` = `assimilation/validate/corpus/SOURCES.md`; entries `yahoo-japan-robots-txt-refusal-rules.md` = `01461e15…`, `yahoo-japan-robots-pattern-syntax.md` = `f9eed892…`, `yahoo-japan-robots-txt-basics.md` = `8e7760da…`, mirror blobs identical in all three. No `E03`/`E04` line in the receipt; last line is `file<TAB>ok<TAB><registry>`. All four C7 terms hold from committed bytes alone.

## DIFF:

- argv: `diff -u committed my` → empty (`ARGV IDENTICAL (relative form)`).
- stdout, normalized (`sed s|$D|LANE|` vs `sed s|/home/vgpnk/…/kake-shokunin|LANE|`): sha256 `cedca9c1d4679d7f4e458ff4f0ace4158d172cb63b250ebdadb9535bc577b44f` for both → `STDOUT IDENTICAL`. Raw shas differ only by the embedded path (`de856da1…` mine, `ab3b5c20…` committed).
- exit: `cmp` committed vs mine → `EXIT RECEIPT IDENTICAL`.
- date sensitivity: `--today 2026-10-24` → exit 1, 11 × `E08` (S374 S329 S312 S367 S372 S373 S390 S409 S416 S417 S418, all `opened=2026-10-25`); `--today 2026-10-25`, `2026-10-26`, `2027-01-01` → exit 0, 0 E. The receipt is reproducible only for `--today` ≥ the round date; today is that date. Base already carried `opened=2026-10-25` on those 10 rows (checked at `fcaf4b85`), so nothing was re-dated and S418 is the only added row (155 → 156 rows at `2bda8e4`, unchanged at `a7a548e`).
- mirror fidelity (not a C7 term): whole-mirror blob diff at `a7a548e` (`git ls-tree -r` both sides, 144 files each) shows exactly two stale files — `corpus/QUALITY.md` landed `11988da…` vs mirror `d331e96…`, `SKILL.md` landed `090862d…` vs mirror `bd6bc42…`. Cause: `a7a548e` itself added 19 lines to `SKILL.md` and 42 to `corpus/QUALITY.md` (`git show --stat a7a548e -- corpus/ SKILL.md`) and did not re-run the script. At the build commit `2bda8e4` the whole mirror was blob-equal to the landed corpus (empty diff). No verdict impact: `E11` is existence-only (`[ ! -e "$dir/$path" ]`) and my regeneration from `a7a548e`'s corpus still reproduced the receipt byte-for-byte.
- non-discrimination of the exit: the base registry (`fcaf4b85`, 155 rows, no S418) placed in the same build mirror → exit 0, 14 × W04, `file\tok`, stdout byte-identical to the receipt modulo path. So `exit=0` alone cannot certify that the append landed; the load-bearing term is the validated-registry byte-equality (blob `7ccf679…` on both sides). C7 also cannot establish "before": the validated registry already contains S418 (156 rows), so the run it records is at-or-after the append; ordering is carried by C8's pre-append mirror and ancestry, and C7's own docstring concedes this ("a receipt check: it certifies agreement of the receipts, not that the run happened").
- gate fail-open (`validate_append.sh`, not the counter): a scratch copy of the script body with `LANE=/tmp/negctl/L` over the build corpus → `exit=0`, `SCRIPT-EXIT=0`; after duplicating the `S418` row → census `exit=1` with `E03`+`E04`, but `SCRIPT-EXIT=0` again. The script has `set -u` only and ends in `cat`/`tail`, so its own status is never the census status; any wiring that gates on the script's exit appends on a failing census. It also `rm -rf "$V"` before validating, so a failing run destroys the previous receipt set (C7 still fails closed, since the fresh receipt records `exit=1`).
- tool pin: the receipts do not record the census version. Replay used `sources-census.sh` sha256 `3fb7261569f46423dd80ecc23e0a23789a7926f667c7a3fc559d2439d4a64e30`, GNU Awk 5.4.1, bash 5.3.20(1), git 2.56.0 → reproduces, so no drift today. No tool installs were needed.

## LANE CENSUS:

- `cd /home/vgpnk/Projects/shokunin && ./scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kake` → exit 0, stderr empty, 15 lines: 14 × `kake\tW04\t<id> duplicate url … across scopes` (S033 S088 S092 S098 S099 S102 S110 S111 S115 S116 S117 S127 S416 S417) + `kake\tok\t/home/vgpnk/Projects/shokunin/kake-shokunin/corpus/SOURCES.md`. Counts by code: W04 = 14, W01 = W02 = W03 = 0, E-codes = 0. Output is identical to the mirror replay modulo the lane label (`kake` vs `file`) and the path, so the receipt's verdict transfers to the live registry. Worktree HEAD at run time was `78963ae28e1c6a409a1a1322230c5671cd2efcbe` (moved past the measured revision); `cmp` of the worktree `corpus/SOURCES.md` against `git show a7a548e…:corpus/SOURCES.md` → identical, and the three entries also identical, so the verdict stands on the measured bytes.
- `./scripts/sources-census.sh census --root /home/vgpnk/Projects/shokunin kake` → exit 0; `rows 156`, `tier.A 133 / tier.B 6 / tier.C 17`, `status.mined 126 / status.queued 8 / status.rejected 22`, `missing 0` (FLEET totals equal).
- `./scripts/sources-census.sh selftest` → exit 0, `selftest ok` (its own mutant suite kills E01…E11, W02, W04, the gawk-failure and out-truncation mutants).

## NEGATIVE CONTROLS:

Each mutant ran in a fresh copy of the build mirror (`cp -r $V/. /tmp/negctl/<X>/`); only the mutant differs.

| # | mutation | observed |
|---|---|---|
| A | `S418` row duplicated (`awk '{print} /^\| S418 \|/{print}'`) | exit 1; `file\tE03\tS418 duplicate id` **and** `file\tE04\tS418 duplicate url info-search.yahoo.co.jp/archives/002885.php within scope …` (E04 also fires because the copy shares URL+scope). E03 fires as expected. |
| B | pipe inside a cell: `$8` of `S418` ← `$8 " gamma \| delta "` | exit 1; `file\tE01\tS418 fields=12` (NF=14; the message prints NF−2). |
| C | same pipe with the field count preserved (NF=13, trailing empty cell dropped) | exit 1; E01 bypassed, but `E07\tS418 status=delta` + `E08\tS418 opened=mined` — the census still catches an interior pipe through the enum/date checks. |
| D | a non-corpus used-by target removed from the mirror (`rm SCORECARD.md`) | exit 1; 9 × `E11\t<id> missing used-by SCORECARD.md`. E11 resolves against the mirror root (`dir_abs = realpath(dirname(registry)/..)`), so the script's five-file copy list is load-bearing and exit 0 proves it complete at this revision. |
| E | base registry (`fcaf4b85`) in the build mirror | exit 0 and stdout byte-identical to the receipt modulo path — the exit alone is non-discriminating (see DIFF). |

Residual gaps, disclosed and not claim-harming: (i) C7 compares only the registry and the three entries, so mirror staleness (`QUALITY.md`, `SKILL.md`) is invisible to it; (ii) E11 is existence-only, so a stub mirror file would pass; (iii) the receipt pins neither the census version nor `--today`; (iv) `validate_append.sh` is fail-open at exit level and destructive (`rm -rf`) before it validates.

VERDICT: C7 reproduces exactly from committed bytes at `a7a548e` — argv, `exit=0`, 15-line stdout (normalized sha256 `cedca9c1…`) and empty stderr all match the receipt — and the census kills every mutant C3 relies on (E03, E01, E07/E08, E11, all exit 1), but the receipt certifies post-append agreement rather than ordering, and the whole-corpus mirror is stale for two post-build docs that no C7 term compares.
