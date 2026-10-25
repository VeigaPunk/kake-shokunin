# ExecC1Selftest — round-54 C1 counter selftest (read-only)

Seat: `L1Kake54.ExecC1Selftest` (leaf; no subagents spawned, no installs).
Command (run verbatim, read-only, cwd = lane repo `/home/vgpnk/Projects/shokunin/kake-shokunin`):

```
python3 -B .ufo/waves/round-54/c54_s374_calib.py --selftest
```

`-B` suppresses bytecode writes; `--selftest` uses only in-memory fixtures (`run_checks_fix`), so the run touches no git objects, no worktree files, and no network. Observed output:

```
  ok  base_unrepaired: exit 1 (met=False) expected 1 (met=False)
  ok  corrected: exit 0 (met=True) expected 0 (met=True)
  ok  correction_missing_quote: exit 1 (met=False) expected 1 (met=False)
  ok  correction_missing_crawl: exit 1 (met=False) expected 1 (met=False)
  ok  body_missing_quote: exit 2 (unevaluable) expected 2 (unevaluable)
EXIT=0
```

Overall selftest exit: **0** (all 5 fixtures behaved as expected). This byte-matches the retained control `.ufo/waves/round-54/controls/c1-selftest.txt` modulo the echoed `(met=…)` labels on each line.

## Per-fixture verdicts

| Fixture | Requested rejection mode | Exit | Label | Rejected? |
|---|---|---|---|---|
| `base_unrepaired` | **no-op** (entry with suspect rendered cell, no correction block) | 1 | met=False | Yes — rejected |
| `corrected` | positive control (valid `[r54-correction 2026-10-25]` block with exact quote + `crawl` token) | 0 | met=True | Accepted, as designed |
| `correction_missing_quote` | **missing quote** (correction line carries mark + `crawl` but not the exact Japanese quote) | 1 | met=False | Yes — rejected |
| `correction_missing_crawl` | **missing English crawl qualifier** (correction line has mark + exact quote, but only Japanese 巡回 inside the quote; no literal `\bcrawl\b`) | 1 | met=False | Yes — rejected |
| `body_missing_quote` | **absent source quote** (retained round-52 body lacks the pinned phrase → claim unevaluable) | 2 | unevaluable | Yes — rejected as unevaluable (distinct from met=False) |

All four required rejection modes are exercised and rejected; the no-op case is distinguished from a fake "met=True" by exit code, not stdout (per the script's own comment, lines 166–167).

## Mechanism notes (from `run_checks_fix`, lines 171–190)

- Rejection path: `corr_at` is only set when a single line contains `CORRECTION_MARK` **and** the exact `QUOTE` **and** `EN_CRAWL_RE` (`\bcrawl\b`, case-insensitive). `correction_missing_quote` fails the quote conjunct; `correction_missing_crawl` fails the crawl conjunct — the 巡回 inside the quoted Japanese phrase does **not** satisfy `EN_CRAWL_RE`, confirming the qualifier must be the English token.
- `base_unrepaired` and both broken corrections all exit 1 because `corr_at == -1`; `body_missing_quote` short-circuits to exit 2 before the entry is read.
- A multi-line rendered cell spans a newline in every fixture (`"(rendered: … one it\n does not recommend … vouch for)."`). `run_checks_fix` iterates `finditer` **per line**, so this cell never matches and `suspects` is always empty in the selftest — every fixture's mismatch count is 0 and outcomes are driven solely by `corr_at`.

## Risk / caveat (finding, not a failure)

- The in-memory reader diverges from the committed-path `run_checks` (lines 88–91), which runs `RENDER_RE.finditer` over the **whole entry** — `[^)]+` matches newlines, so the same multi-line suspect cell *would* be detected there. Consequence: the `corrected` fixture's content, if committed verbatim, would yield `mismatch=1` (suspect cell before the correction) and exit **1** under `run_checks`, not 0. The selftest therefore validates exit-code plumbing and the quote/crawl/corr_at gates, but does **not** exercise the suspect-cell-before-correction path that the real counter uses. Single-line suspect cells would be caught identically by both paths.
- Secondary: `run_checks_fix` takes no per-check results, so stdout carries only the five line verdicts; the "junk no-op" guard relies entirely on exit codes as intended.

## Evidence retained

- Script: `.ufo/waves/round-54/c54_s374_calib.py` (hashline `#475A`), lines 114–168 (fixtures), 171–190 (`run_checks_fix`), 61–111 (`run_checks`), 193–215 (`main`).
- Output captured above; control file `.ufo/waves/round-54/controls/c1-selftest.txt` (`#DD44`) agrees.
- Scope: read-only per wave rules; the only write is this report (sole report-path exception per L1 scope correction).

## Blockers

None.
