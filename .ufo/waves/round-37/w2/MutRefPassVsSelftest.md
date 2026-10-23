# MutRefPass versus robots selftest — wave 2
Axes: operability (detector sensitivity), freshness (pinned rerun), byte preservation.
Measured revision: `79d3c780f9afb9bc013e3b13e73ee73e6a8ac13c`; sandbox only; no installs/network.
**Result:** all 42 mutants return selftest exit 1, but this is not 42 demonstrated kills: the pristine reference also fails.
**41/42** introduce failures in fixtures the reference passes; **27/28** among the sealed-target survivors do so. **M09** adds none.
Strict full-suite verdicts: killed 0, survived 0, inconclusive 42 (red baseline). I below means inconclusive, not killed.
Expected detector: unmodified selftest exit 0 iff all 131 fixtures pass (`scripts/robots_audit_selftest.py:26,954-964`).
Pristine and post-probe reference: both 130/131, exit 1, only `c10-group-name-ascii-only-case-folding`; expected tool exit 0, observed 1.
Verdict: reference 130/131 claim **holds**. “c10 is shared by all mutants” is **wrong**: M11 passes c10 while failing 45 other fixtures.
Verdict: “all 42 are killed” would be **overstated**. M09 has the exact baseline failure signature; its added casefold behavior is not separated.
M09 changes group-name `.lower()` to `.casefold()` (`retained/MutRefPass/mutants/M09.py:77`); c10 uses Kelvin sign, already folded by reference `.lower()` (`sealed/reference/ref.py:77`; selftest:364-367). Paths here omit `.ufo/waves/round-37/`.
Sealed scores below are transcribed programmatically from pinned `.ufo/waves/round-37/ctl/MutRefPass.md:11-52`, not rerun. New failing cases exclude the baseline failure; no detector/contract was changed.
| Mutant | Sealed /28 | Selftest passed /131 | Killed (strict) | New failing cases |
|---|---:|---:|:---:|---|
| M01 | 28 | 129 | I | b01 |
| M02 | 28 | 129 | I | b02 |
| M03 | 28 | 129 | I | b09 |
| M04 | 28 | 129 | I | b10 |
| M05 | 28 | 129 | I | b06 |
| M06 | 28 | 128 | I | b16, b17 |
| M07 | 28 | 129 | I | d15 |
| M08 | 28 | 129 | I | b18 |
| M09 | 28 | 130 | I | none |
| M10 | 28 | 129 | I | c09 |
| M11 | 0 | 86 | I | 45 (full list in summary) |
| M12 | 24 | 129 | I | c08 |
| M13 | 24 | 128 | I | c05, c07 |
| M14 | 24 | 128 | I | b13, c06 |
| M15 | 28 | 128 | I | d03, d14 |
| M16 | 20 | 124 | I | b02, d05, d13, d14, e03, e04 |
| M17 | 2 | 129 | I | d16 |
| M18 | 28 | 129 | I | d08 |
| M19 | 28 | 129 | I | e14 |
| M20 | 26 | 128 | I | d10, e14 |
| M21 | 24 | 126 | I | b01, d10, d11, e14 |
| M22 | 24 | 129 | I | e07 |
| M23 | 24 | 126 | I | b05, e09, e10, e16 |
| M24 | 24 | 126 | I | b05, e09, e10, e16 |
| M25 | 24 | 129 | I | e01 |
| M26 | 20 | 129 | I | e02 |
| M27 | 24 | 129 | I | e04 |
| M28 | 28 | 129 | I | e11 |
| M29 | 27 | 129 | I | g12 |
| M30 | 25 | 128 | I | f11, f12 |
| M31 | 28 | 129 | I | f11 |
| M32 | 28 | 127 | I | f06, f27, v05 |
| M33 | 27 | 129 | I | f07 |
| M34 | 28 | 129 | I | f09 |
| M35 | 0 | 63 | I | 67 (full list in summary) |
| M36 | 27 | 129 | I | a05 |
| M37 | 28 | 129 | I | f23 |
| M38 | 28 | 129 | I | f20 |
| M39 | 28 | 129 | I | g05 |
| M40 | 28 | 129 | I | g06 |
| M41 | 28 | 48 | I | 82 (full list in summary) |
| M42 | 28 | 7 | I | 123 (full list in summary) |

## Commands and evidence
Let `B=/fast/scratch/hyaku/kake-r37w2/MutRefPassVsSelftest`, `C=$B/clone`, `E=$B/evidence`; cwd for detector calls is `$C`; TMPDIR=`$B/tmp`.
`unset GIT_DIR GIT_WORK_TREE GIT_INDEX_FILE && export TMPDIR="$B/tmp" && timeout 10s mkdir -p "$B/tmp" && timeout 120s git clone -q /home/vgpnk/Projects/shokunin/kake-shokunin "$C" && timeout 30s git -C "$C" checkout -q 79d3c780f9afb9bc013e3b13e73ee73e6a8ac13c` — exit 0.
`unset GIT_DIR GIT_WORK_TREE GIT_INDEX_FILE KAKE_ABLATE PYTHONPATH; export TMPDIR="$B/tmp"; timeout --kill-after=5s 850s python3 -B "$B/run_selftests.py"` — exit 0, 74.84s observed, two concurrent selftests (runner + outer timeout + at most six detector processes).
`timeout --foreground --kill-after=2s 180s python3 -B "$C/scripts/robots_audit_selftest.py" --tool "$C/.ufo/waves/round-37/retained/MutRefPass/mutants/Mxx.py"` — each M01–M42 exit 1, results above.
Same detector command with `--tool "$C/.ufo/waves/round-37/sealed/reference/ref.py"` ran before and after the matrix — both exit 1.
`timeout 30s git -C "$C" show 79d3c780f9afb9bc013e3b13e73ee73e6a8ac13c:<input>` — all 45 input imports exit 0 and match clone bytes; `$E/pinned-inputs.json`.
Exact expanded argv, cwd, sanitized environment, exits: `$E/commands.jsonl`; raw JSON/stderr: `$E/outputs/{M01..M42,reference-pristine,reference-restored}.{stdout.json,stderr.txt}`.
Full per-case reasons, difference sets, strict verdicts, counts: `$E/summary.json`; SHA256 `76fd7b2ab4ca10ab39c61179867a6eab56100a1c776bc3747c1aee872181cbbd`.
Reproducer `$B/run_selftests.py`; SHA256 `b865c8fa5897b2f609881ec3ddd8fd006f5e4c5d1802544e98745d7715818a59`; commands SHA256 `20db5302db5cf9d8d817194922d92474b286cd292624727e5cbd25e0fe606641`.
Restoration evidence: supplied mutants were evaluated read-only; no reference/mutant/selftest bytes were edited. All 45 before/after input hashes match (`$E/hashes-before.json`, `$E/hashes-after.json`; identical file SHA256 `0f5443fe611844dad39d4c049f1cac85d91328820904bd7e3f33ce531a846560`).
Reference SHA256 before = after `2c294e495ef9a36c6d74472e4128f432a7bf81cbccc7998136866a877988c05d`; selftest `0c5b1131afd25dc6052205fd6952f6c39a9500d0a259a091ab6368a7fb25e80f`; M09 `043f0dc2b9882a2497e08f3333f2141559ac72ebfb13f018870cadf1b881ad47`.
Fixtures were cleaned by the selftest; started child groups were killed/reaped; runner recorded `activeProcessesAtEnd=0`. No lane/index/jj changes; only this report written in the lane.
