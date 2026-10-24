# ScoutPatternPollution — C2 last-match attack

Axes: freshness (the checker's last match must be the receipt-derived repair) and pattern isolation (no later accidental match).

**Attack result: FAIL to steal.** No existing line outranks the round-44 repairs. `scripts/ledger_latest_check.py --root .` exits 0. Last match of each designated pattern is the repair line.

The checker (`latest_match`) compiles each pattern with `re.S` only, takes `finditer()[-1]`, and reports the 1-based line of the match start. `re.S` does not matter here: none of the three patterns uses `.` outside a character class. Cross-line matches come from `\s`. Each pattern is applied only to its bound file (`read_ledger` prefers the worktree copy). `.ufo/` reports are not scanned.

## Current last match

| figure | bound file | last line | groups |
|---|---|---|---|
| rescore-tally | SCORECARD.md | 3575 (span 3575–3576) | `14` |
| donothing-ratios | LOG.md | 1703 | `4.21`, `7.05` |
| build-ratio-range | LOG.md | 1706 | `1.00`, `1.01`, `1.11`, `1.22` |

Undesignated file: rescore has 0 hits in LOG.md; the other two patterns have 0 hits in SCORECARD.md.

## Commands

```text
python3 -B /fast/scratch/hyaku/kake-r44/ScoutPatternPollution/enumerate.py
python3 -B scripts/ledger_latest_check.py --root .
```

Both were one snapshot, cwd `/home/vgpnk/Projects/shokunin/kake-shokunin`. Checker exit 0.

### Verbatim enumerator

```text
flags: re.compile(pattern, re.S); no re.ASCII; no re.M
bind rescore-tally -> SCORECARD.md
  re-scored\s+(\d+)\s+of\s+the\s+27
bind donothing-ratios -> LOG.md
  not met \(T1\s+([\d.]+),\s*T5\s+([\d.]+)\)
bind build-ratio-range -> LOG.md
  T1\s+([\d.]+)–([\d.]+), T5\s+([\d.]+)–([\d.]+)

# LOG.md nlines=1714
PATTERN rescore-tally not-scanned count=0
PATTERN donothing-ratios DESIGNATED count=2
  1. LOG.md:1661-1662 col=81 groups=('4.27', '8.68')
     |1661|   `verification/freeze/build-{1,2,3}.json`); do-nothing (round-41 tool at base) not met (T1 4.27,
     |1662|   T5 8.68); all four round-42 meeting controls now not met under v4 (M8: F,T3; v1_casefold: F,T2;
  2. LOG.md:1703 col=3 groups=('4.21', '7.05')
     |1703|   not met (T1 4.21, T5 7.05) per `.ufo/waves/round-43/verification/freeze/ref41-base.json`
  LAST LOG.md:1703 groups=('4.21', '7.05')
PATTERN build-ratio-range DESIGNATED count=3
  1. LOG.md:1631 col=59 groups=('0.98', '1.06', '1.09', '1.17')
     |1631|   0/225 under Python 3.10): v3 met on three random seeds (T1 0.98–1.06, T5 1.09–1.17 vs round 41's 4.2 / 7.8);
  2. LOG.md:1660 col=74 groups=('1.00', '1.02', '1.13', '1.18')
     |1660|   S129, tameshi r33). L1 receipts: build `020bc457` met ×3 (11/11 equal, T1 1.00–1.02, T5 1.13–1.18,
  3. LOG.md:1706 col=3 groups=('1.00', '1.01', '1.11', '1.22')
     |1706|   T1 1.00–1.01, T5 1.11–1.22 over
  LAST LOG.md:1706 groups=('1.00', '1.01', '1.11', '1.22')

# SCORECARD.md nlines=3586
PATTERN rescore-tally DESIGNATED count=2
  1. SCORECARD.md:3393 col=1 groups=('18',)
     |3393| re-scored 18 of the 27 with fresh `os.urandom` seeds (receipts `verification/l1-rescores/`,
  2. SCORECARD.md:3575-3576 col=83 groups=('14',)
     |3575| `scripts/ledger_latest_check.py` from the committed receipts at `master`): the L1 re-scored
     |3576| 14 of the 27 live-seat controls — the committed receipts
  LAST SCORECARD.md:3575 groups=('14',)
PATTERN donothing-ratios not-scanned count=0
PATTERN build-ratio-range not-scanned count=0

# .ufo/waves/round-44 utf-8 matches
PATTERN rescore-tally
  .ufo/waves/round-44/w2/CriticC2Repair.md:123-124 col=89 LAST_IN_FILE groups=('14',)
PATTERN donothing-ratios
  .ufo/waves/round-44/w2/CriticC2Repair.md:111 col=9 LAST_IN_FILE groups=('4.21', '7.05')
  .ufo/waves/round-44/w2-spec.json:194 col=795 LAST_IN_FILE groups=('4.21', '7.05')
  .ufo/waves/round-44/w2-taskcall.json:1 col=42304 LAST_IN_FILE groups=('4.21', '7.05')
PATTERN build-ratio-range
  .ufo/waves/round-44/verification/claim/ledger-after.txt:3 col=32 earlier groups=('1.00', '1.01', '1.11', '1.22')
  .ufo/waves/round-44/verification/claim/ledger-after.txt:3 col=67 LAST_IN_FILE groups=('1.00', '1.01', '1.11', '1.22')
  .ufo/waves/round-44/verification/ledger-before.txt:3 col=35 earlier groups=('1.00', '1.02', '1.13', '1.18')
  .ufo/waves/round-44/verification/ledger-before.txt:3 col=70 LAST_IN_FILE groups=('1.00', '1.01', '1.11', '1.22')
  .ufo/waves/round-44/w1/ExecLedgerCheck.md:26 col=35 earlier groups=('1.00', '1.02', '1.13', '1.18')
  .ufo/waves/round-44/w1/ExecLedgerCheck.md:26 col=70 LAST_IN_FILE groups=('1.00', '1.01', '1.11', '1.22')
  .ufo/waves/round-44/w2/CriticC2Repair.md:34 col=35 earlier groups=('1.00', '1.02', '1.13', '1.18')
  .ufo/waves/round-44/w2/CriticC2Repair.md:34 col=70 earlier groups=('1.00', '1.01', '1.11', '1.22')
  .ufo/waves/round-44/w2/CriticC2Repair.md:90 col=12 earlier groups=('1.00', '1.01', '1.11', '1.22')
  .ufo/waves/round-44/w2/CriticC2Repair.md:114 col=9 LAST_IN_FILE groups=('1.00', '1.01', '1.11', '1.22')
```

### Verbatim checker

```text
rescore-tally MATCH quoted=14 derived=14 SCORECARD.md:3575
donothing-ratios MATCH quoted=T1 4.21, T5 7.05 derived=T1 4.21, T5 7.05 LOG.md:1703
build-ratio-range MATCH quoted=T1 1.00–1.01, T5 1.11–1.22 derived=T1 1.00–1.01, T5 1.11–1.22 LOG.md:1706
ledger-quotes: 3 figures, 0 mismatches
EXIT:0
```

## What does not steal today

Lines after the repairs quote the stale figures in a shape the regex rejects, so they stay earlier than nothing — they are simply not matches:

- LOG.md:1704 `"4.27, 8.68"` lacks `not met (T1`.
- LOG.md:1707 `"1.00–1.02, 1.13–1.18"` lacks the `T1 ` prefix. Build pattern also requires a real U+2013 and the exact `, T5` (comma, one space).
- SCORECARD.md:3578–3580 says the `"18"` is superseded and `re-scored controls is 14`. That is not `re-scored <digits> of the 27`. The captured `14` remains the multiline match that starts at 3575.

`.ufo/` hits are real regex matches but are not ledger inputs. Every such file's **last** match uses the corrected groups, not the stale ones. Two matches on one line: the later one wins. On `ledger-before.txt:3`, `ExecLedgerCheck.md:26`, and `CriticC2Repair.md:34` the stale `T1 1.00–1.02, T5 1.13–1.18` is first and the derived `T1 1.00–1.01, T5 1.11–1.22` is second. Pasting the whole line into LOG.md would not change the quoted value. `w2-spec.json:194` and `w2-taskcall.json:1` match only `not met (T1 4.21, T5 7.05)`. Their build phrase is the ASCII escape `\u2013`, not U+2013, so it does not match build-ratio-range. `CriticC2Repair.md:123-124` is a quote of the SCORECARD repair (`14`).

38 non-UTF-8 paths under `.ufo/waves/round-44/` were skipped; all are `__pycache__/*.pyc`, not reports.

Near misses that do **not** match (so they also do not override a hyphen/bold repair, and do not steal):

- SCORECARD.md:3082 `not met (T1 4.17–4.28, T5 7.81, …)` — en-dash inside the T1 slot, and the file is not the donothing ledger.
- `w2/ScoutRescoreCensus.md:94` transcribes the build range with ASCII hyphens (that report says so). Hyphen is not U+2013.
- `w2/ScoutRescoreCensus.md:103` and `make_w2_spec.py` say `re-scored N of the 27` / describe the pattern. `N` and the prose commas are not `\d+`.
- `w2-spec.json:162` `not met (T1 x, T5 y)` — `x` is not `[\d.]+`.

No ASCII-hyphen and no em-dash build-range matches exist in either ledger (0).

## Latent stealers

Appending any of these **after** the current last match makes it the new last match and turns C2 red. They are earlier in the ledger today, so they do not steal until copied downward:

- SCORECARD.md:3393 `re-scored 18 of the 27` → group `18`.
- LOG.md:1661–1662 `not met (T1 4.27,` / `T5 8.68)` → `4.27`, `8.68`. `\s` already crosses that newline.
- LOG.md:1660 `T1 1.00–1.02, T5 1.13–1.18`.
- LOG.md:1631 `T1 0.98–1.06, T5 1.09–1.17` (not the r43 figure, still a match).

A partial paste of a checker stdout line that stops after the quoted stale range and drops the following derived range would also steal. A further ledger paragraph that ends with `re-scored` and continues `18 of the 27` on the next line matches, because the reported line is the start line.

## Files written

- `/fast/scratch/hyaku/kake-r44/ScoutPatternPollution/enumerate.py`
- `.ufo/waves/round-44/w2/ScoutPatternPollution.md`

No tool installs. No ledger edits. Blockers: none.
