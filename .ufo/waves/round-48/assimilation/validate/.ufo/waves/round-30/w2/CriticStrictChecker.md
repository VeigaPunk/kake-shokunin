# Round 30 wave 2 — CriticStrictChecker: attack on c1_strict_checks.py

Target: `.ufo/waves/round-30/c1_strict_checks.py`, sha256 96e7bbcd8ec9144316a1c717570f802b8d5e16a63a16c8a009049bf5d0e9500f
(the same blob at 04637bd, 71c6bfa and 451e98f). Declared counter `c1_reason_count.py` be2a1287ab7f2abd… (the same blob at all four commits).
Axis: operability. Result: four holes, each reproduced with a stub that scores 6/6. The S5 attacks failed.
Sandbox: /fast/scratch/hyaku/kake-r30/w2/CriticStrictChecker/ (clone at `clone/`, run outputs in `out/`). TMPDIR was set inside the sandbox.
No lane file was written except this report. No network was used. Nothing was installed.

## Commands (all run with --scratch inside the sandbox), exit codes and stderr summaries
- Control: `python3 -B <lane>/.ufo/waves/round-30/c1_strict_checks.py --root clone --revision 71c6bfa` gave exit 0, 6/6, matching the receipt.
- Control: the same checker at `--revision 0356681` gave exit 1, 0/6, matching the before-receipt.
- Strict checker on stubB, stubC and stubE: exit 0, **6/6** each (`out/strict-stub{B,C,E}.{json,err}`).
- Declared counter `c1_reason_count.py` on stubB, stubC and stubE: exit 0, **14/14** each, with "controls True, constant gates rejected True" (`out/count-stub*.err`).
- Checker copy using a swapped counter (`stubA/c1_strict_checks.py`) at `--revision 0356681`: exit 0, **6/6** at 035668132250… (`out/stubA-strict-0356681.*`).
- `python3 -B s5_probe.py`: exit 0. The per-variant results are below.

## Hole 1: the counter is imported from the working tree and its pin is never checked (provenance)
- Evidence: c1_strict_checks.py:53-56 loads `c1_reason_count.py` from `HERE`, which is the checker's own directory. `--revision` binds only `scripts/` (through `C.export_scripts`).
  The checker records `declaredCounterSha256` (line 283) but never compares it to anything.
- Reproducer: `stubA/c1_reason_count.py` changes one token: `export_scripts` archives `71c6bfa` instead of the resolved commit.
  At base 0356681 the receipt says `"revision": "035668132250…"` and passes 6/6.
  It does record `gateSha256` dbfade45… (the 71c6bfa gate; the real base gate is d7e79ba1…) and `declaredCounterSha256` a03bdacf… (not be2a1287…), but the checker exits 0 anyway.
- Smallest correction: exit 2 unless the loaded counter's sha256 equals be2a1287ab7f2abdca8695d8274504d14b9e1c6b0afe95e940c890bfb8bcc53e.
  Alternatively, load the counter from `git show 4580c78:.ufo/waves/round-30/c1_reason_count.py`.
  Also assert that the exported gate's sha256 equals the blob sha256 of `<commit>:scripts/citing_set.py`.

## Hole 2: S2 checks only that the naming fixtures fail (recall), not precision or a baseline, so a runner that ignores reasons passes
- Evidence: c1_strict_checks.py:133-144 requires only that the runner exits 1 and that `expected_failing <= failing`.
  There is no baseline run, and the extra failing cases are never bounded.
  Line 116 also defaults to "failing" when a row lacks both `passed` and `ok` (`row.get("passed", row.get("ok", False))`), so a malformed row counts as a hit.
- Reproducer stubB (commit 25863d5f0a7e68e0b924be8916852843ac0a64be on 71c6bfa) changes only `scripts/citing_set_selftest.py`:
  - It compares finding ids only.
  - It marks every case failed when the gate's sha256 is not dbfade45….
  - Proof that it ignores reasons: setting fixture 30's expected reason to `wrong_reason` makes the stubB runner exit 0. The 71c6bfa runner exits 1 on the same edit (`tmp/proofB*`).
  - Under every rename it reports 41 of 41 cases failing (the naming fixtures are 1 or 2 per code). Strict S2 still passes, and so does the declared counter's `compared` part.
- Smallest correction:
  - Require `failing == expected_failing` exactly. This already holds for all ten codes at 71c6bfa per `c1-strict-after-71c6bfa.json`, so the change costs nothing there.
  - Require the runner to exit 0 with no failing cases on the unmutated tree.
  - Treat a row without a boolean `passed` as malformed, and fail the check.
  - Add an expected-side mutant: rewrite the reason in each naming fixture's expected.json while leaving the gate untouched, and require exactly that case to fail. This defeats the gate-hash pin.

## Hole 3: S3 has no single-use control for `--name=value` or abbreviations, and does not check why the usage error was raised
- Evidence: the only control is "each option once" at line 176, in space-separated form.
  The `=value twice`, `mixed` and `abbreviated` variants (lines 166-168) therefore also pass for a gate that refuses those spellings outright.
  The usage-object test (lines 173-174) accepts any error text starting "usage:".
- Reproducer stubC (commit f6605de80c3e3011aa9f8bd9f68f26d8653a029b): `allow_abbrev=False`, plus `parser.error` whenever any `--x=y` argument is present.
  - Strict checker 6/6, counter 14/14.
  - Behaviour regression, with the option given once:

    | Gate | `--population=population.json` once | `--pop population.json` once |
    |---|---|---|
    | 0356681 (base) | exit 0 | exit 0 |
    | 71c6bfa (landed) | exit 0 | exit 0 |
    | stubC | exit 64 | exit 64 |

  - This is an interface break that neither the strict checker nor the counter can see.
- Smallest correction: for each of the four options, add single-use controls in the `--opt=value` form and in the 5-character prefix form, each expecting 0/clean with no findings.
  Optionally, require the error string to name the repeated option.

## Hole 4: S6 tests the overflow literal at only one place
- Evidence: lines 191-192 test the only overflow case, at the top level of the population document.
  The counter has no overflow case, and nothing tests a negative overflow (`-1e999`) or an overflow in the ledger.
- Reproducer stubE (commit 99ab0f01f7e619b21de846a57c0efa8109dfde57): drops `parse_float=_finite` and checks only the document's top-level values for non-finite floats.
  - Strict checker 6/6, counter 14/14.
  - Behaviour: with `{"rows":[{"id":"S001","w":1e999},…]}` the stubE gate exits 0 with no findings; the 71c6bfa gate exits 2 with `document_nonfinite_number`.
  - With a ledger pair carrying `"w": -1e999`, the stubE gate exits 0 with no findings; the 71c6bfa gate exits 2 with the same reason.
- Smallest correction: add S6 cases for `1e999` inside a row, `-1e999` inside a ledger pair, and `1E400` in the ledger at the top level.

## Attacks that failed (S5 device matching and O_NOCTTY)
`s5_probe.py` calls the lane checker's `s5()` on gate variants derived from the 71c6bfa gate (`s5gates/`):
- The real gate passes. It opens `/dev/pts/1` with flags 526592, which include O_NOCTTY, and tty_nr stays 0.
- Dropping O_NOCTTY from `os.open` fails twice over: the flags check catches it, and tty_nr becomes 34817.
- A decoy `os.open` with O_NOCTTY followed by the real open through `posix.open` without it (which bypasses the trace) is caught by tty_nr 34817.
- A `posix.open` without O_NOCTTY followed by `TIOCNOTTY` to give the terminal back leaves "no trace". The process dies, apparently from SIGHUP, so the check fails closed.
- Conclusion: the basename match at line 243 over-matches, which fails closed. tty_nr is the real check, and it holds. No hole found.

## Minor (no stub built)
- S4 (lines 217-219) accepts row `"1"` as well as `"S001"`. It does not check the verdict `failed` or for a traceback on stderr; the counter's F05 covers those.
- S5 tests that `document_not_regular_file` is among the findings, not that it is the only one; S1's FIFO case covers exactness.
- `runner_rows` does not catch `TimeoutExpired`. A runner hang raises an uncaught exception, which exits 1 ("check failed") instead of 2 ("bad input").
- `env_clean()` strips only `GIT_*`, and the gate runs without `-I` or `-E`, so `PYTHONPATH` or `sitecustomize` from the caller's environment reach the measured gate.

## Not verified
- I did not run any counter on stubA.
- I did not test the S2 rename with single-quoted or computed code strings. The (a) part fails closed for those by construction (lines 136-137).
- I did not test S3 against a gate that only counts argv length.

Impacted axes: operability, including evidence provenance for holes 1 and 2. All four holes can be fixed inside the checker; none is a tradeoff.
Stub artifacts: /fast/scratch/hyaku/kake-r30/w2/CriticStrictChecker/{clone (tags stubB stubC stubE), stubA/, s5_probe.py, s5gates/, out/}.
