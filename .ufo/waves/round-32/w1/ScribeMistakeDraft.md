# ScribeMistakeDraft — round 32 wave 1: mistake rows for `corpus/lessons/round-32.md ## Mistakes`

Read at lane HEAD `7e05aa8` (HEAD moved `285abca` → `7e05aa8` between my first and second read; both). The lane already carries a row of this class at `corpus/lessons/round-32.md:42` (commit `7e05aa8`), so row 1 below is an amendment of it, row 2 is new.

## What I attacked
1. The stamped time against its own commit: SCORECARD.md:1016 says "Declared at 18:58Z"; `5b32cc7` commit time is `2026-10-22T15:54:19-03:00` (18:54:19Z), author date 18:50:53Z (equal to base `a0b0dffc`'s commit time, so not independent). 18:58Z is **221 s later** than the declaring commit and **147 s later** than the after-measurement commit `2f2f12d` (18:55:33Z) that the declaration says had not run.
2. The landed fix's own power: `.ufo/waves/round-32/declared_time_check.py` (blob `b2e5c37`, sha256 `32d873d0…`) against synthetic commits in my sandbox.
3. The causal clause of the landed repair note ("estimated, not read").

## Commands and observed exits (lane reads only; synthetic repos in sandbox)
| Command | Exit | Observed |
|---|---|---|
| `git -C <lane> show -s --format='%cI %aI %H' 5b32cc7` | 0 | `15:54:19-03:00 15:50:53-03:00 5b32cc7…` |
| `git -C <lane> show -s --format=%cI 2f2f12d` | 0 | `2026-10-22T15:55:33-03:00` (18:55:33Z) |
| `python3 -c` delta computation (sandbox) | 0 | `stated - decl commit = 221.0 s`, `stated - build commit = 147.0 s`, both stated LATER |
| `bash holes.sh` (landed check, 4 synthetic repos) | 0 | A `ok` exit 0 · B violation exit 1 · C `no stated time` exit 2 · D violation exit 1 |
| `for h in hole{A,B,C,D}; python3 -B check2.py …` | 0 | A 1 · B 0 · C 1 · D 1 |
| `python3 -B check2.py --repo <lane> --rev 5b32cc7 …` | 1 | violation (stated 18:58 vs commit 18:54:19) |
| `git show HEAD:<f> \| grep -cE 'estimated, not read\|not read from a clock\|written from an estimate'` | 0 | `1` for `corpus/lessons/round-32.md`, `1` for `SCORECARD.md` |

## Drafted rows

| Class | Evidence | Captured-by | Fix |
|---|---|---|---|
| repair note states an unobserved cause as fact (the class it repairs) | `corpus/lessons/round-32.md:42` says "so 18:58Z was written from an estimate, not read from a clock"; `SCORECARD.md:1041` says "That time was estimated, not read"; both at `7e05aa8`. Observed is only the ordering: 18:58Z is 221 s after `5b32cc7` (18:54:19Z) and 147 s after `2f2f12d` (18:55:33Z), which the declaration claims had not run. Nothing committed distinguishes an estimate from a typo, a rounded clock or skew; the author date equals the base commit's time, so it is not independent evidence either. | The round-32 QUALITY criterion (`corpus/QUALITY.md:549`) bounds the stated time only; no criterion requires a repair note's causal clause to be an observation. | The note states the two deltas and drops the cause; criterion — any causal word in a repair note (`estimated`, `typo`, `skew`) is replaced by a measurement unless a receipt carries it. Shown able to fail: the grep above returns 1 per file at `7e05aa8` and 0 on the corrected text. |
| check narrower than the criterion that cites it (a criterion able to fail only on the shape that already happened) | `.ufo/waves/round-32/declared_time_check.py` at `7e05aa8` (blob `b2e5c37`) resolves the stated `HH:MM` onto the commit's UTC date (`ct.replace(hour=…, minute=…)`, line 18) and matches only `Declared at (\d\d):(\d\d)Z` (line 15). Synthetic repos (`…/holes.sh`): (A) "Declared at 00:05Z", commit `2026-10-22T23:58Z` — stamp 7 min after its commit — prints `ok`, exit 0; (B) "Declared at 23:59Z", commit `2026-10-23T00:02Z` — correct, 3 min before — exit 1; (C) "Declared 18:58Z" (same overstatement, no " at") — exit 2, which `corpus/QUALITY.md:549-554` does not classify (it names only exit 1); (D) control on the real shape — exit 1, the only shape that fails. | The criterion was written after the single case that motivated it and names its failing exit, not its passing one; no fixture set accompanied it. | Declarations state a full UTC instant (`2026-10-22T18:54:19Z`); the check reads `HH:MMZ` on the nearest of commit date ±1 day, accepts `Declared [at]`, passes only on exit 0 and treats every other exit as a defect; A, B, C become fixtures. Shown able to fail: proposed `…/check2.py` scores A 1, B 0, C 1, D 1 and exit 1 on the real `5b32cc7`; the landed script scores A 0, B 1, C 2, D 1. |

## Not verified / limits
- I did not run the C1 or C2 counters, the hostile selftest, or the benign suite; nothing here bears on whether C1 or C2 verify.
- `check2.py` is sandbox-only (30 lines, absolute path `/fast/scratch/hyaku/kake-r32/w1/ScribeMistakeDraft/check2.py`), not landed, and was run only on `5b32cc7` and the four synthetic repos — not over the lane's whole SCORECARD history.
- The cause of the 18:58Z stamp stays unobserved; row 1 reports ordering only, by design.
- Recurrence unknown: `grep 'Declared at'` over the last 12 SCORECARD commits found the phrase only at `5b32cc7`.
- Lane worktree at my last read held `?? .ufo/waves/round-32/w1/CriticNoHarmDiff.md` (a sibling's); I did not touch it. No tooling installed.

Sandbox artifacts: `/fast/scratch/hyaku/kake-r32/w1/ScribeMistakeDraft/{check.py,check2.py,holes.sh,holeA..holeD/}`.
