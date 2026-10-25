# ExecTallyQuoteR52

Claim C1 (calibration), row `quote-truth-counter` (SKILL.md line 1216 at base `e48354b7c26b`). All runs happened in
`/tmp` clones; the lane working tree, index and jj state were not touched (only this report was written). No tool installs were needed or made.

## RUNS:

Clone: `D=$(mktemp -d /tmp/exectally.XXXXXX)` = `/tmp/exectally.LitQZk`;
`git clone -q --no-checkout <lane> "$D"` then `git -C "$D" checkout -q e48354b7c26bb6dc544ab6bbdc534fabe0daf7b6`;
`git -C "$D" rev-parse --show-toplevel` == `$D`, `git -C "$D" rev-parse HEAD` == `e48354b7c26bb6dc544ab6bbdc534fabe0daf7b6`.
Command as documented in the row, from `$D`: `python3 -B .ufo/waves/round-52/c52_quote_truth.py --selftest`
(the script's only documented pin is `KAKE_R52_SELFTEST_REV`, line 466; not named in the row's cell).

- Run 1: exit **1**, wall **1.826s** (user 3.674 / sys 1.011), 5 output lines. Tally line:
  `c52 quote-truth selftest: 17/18 (fixture revision e48354b7c26b)`. Last 3 lines:
  ```
    FAIL     C5_quote_truth: S374: entry line 72 quotes "the lane's robots-refusal ground (S372, "… which is not a raw substring of the retained body
    FAIL     C8_mirror_bytes: registry rows 156 != mirror rows 145 + 3
    FAIL     C8_mirror_bytes: append-only: measured registry minus the adopted rows != mirror bytes
  ```
- Run 2 (same clone, same command): exit **1**, wall **1.879s** (user 2.068 / sys 0.986); output byte-identical to run 1
  (`cmp` clean). Last 3 lines as above.

Supplementary runs (same clone, needed for the claim; each is one command):

- `KAKE_R52_SELFTEST_REV=1ae8de5d4dee … --selftest` (the revision the committed receipt names): exit **0**, wall 2.277s,
  `c52 quote-truth selftest: 18/18 (fixture revision 1ae8de5d4dee)`, zero FAIL lines.
- `KAKE_R52_SELFTEST_REV=a4a890cf1381`: exit 0, 18/18, 0 FAIL lines.
- `KAKE_R52_SELFTEST_REV=fd91527a2860`: exit 1, 17/18, 2 FAIL lines (C8 only; `registry rows 155 != mirror rows 145 + 3`).
- `KAKE_R52_SELFTEST_REV=faf9abe`: exit 1, 17/18, 3 FAIL lines (C5 + C8; `registry rows 156`).

## WHAT N COUNTS:

The printed N is `{passed}/{total}`. `total = len(fixtures)` = **18** fixtures — one `pass` fixture plus 17
`fail_*` fixtures (`fail_missing_entry`, `fail_no_cite`, `fail_row_short`, `fail_usedby`, `fail_lesson_quote`,
`fail_entry_quote`, `fail_receipt_sha`, `fail_receipt_status`, `fail_receipt_url`, `fail_census_exit`,
`fail_census_e04`, `fail_mirror_contaminated`, `fail_pin_sha`, `fail_registry_row_dropped`, `fail_not_append_only`,
`fail_empty_body`, `fail_bad_receipts`). Each fixture is a fresh two-commit sandbox git repo (pre = mirror/evidence,
post = registry + lesson) fed to one `run_checks` pass over the eight C1–C8 conditions; a fixture counts as passed when
the counter's exit code equals that fixture's expectation (0 for `pass`, 1 for the fail fixtures, 2 for
`fail_bad_receipts`). So **N counts fixtures** — not individual condition checks, not mutants, not unit-rule checks
(this script has no separate unit checks; round 55's `c55_quote_truth.py` is the one with "47 + 3").

The row's Self-test cell states `(18 fixtures, sandbox repos; receipt …)`. The counter's claim regex for this row is
`\((\d+) fixtures` (`POP`, c56_selftally.py:59), so claim = **18** = the observed denominator. Therefore
`claim_ne_observed` does **not** fire; the row fails on `selftest_failed` (exit 1, numerator 17 != 18). Measured with
the counter itself (restricted to this row, `measure(..., pop=[POP[7]], expected=1)`):
`quote-truth-counter: claim=18 observed=17/18 MISMATCH selftest_failed`, exit 1.

The two fixture-level causes at base, each attributed to a commit:
- C8: the `pass` fixture asserts `len(registry) == len(mirror)+3`; the round-52 mirror has 145 rows, so 148 rows were
  required. Row count went 148 → 155 at `fd91527a2860` (round-53). Pinning at `fd91527a2860` reproduces 17/18 with C8
  alone.
- C5: `corpus/knowledge/yahoo-japan-rel-nofollow-semantics.md` line 72 carries the ASCII span
  `"the lane's robots-refusal ground (S372, "`, which is not a substring of `S374.html`; the C5 scanner reads every
  `"…"` span of >= 6 units below the entry's 8-line header. Introduced at `faf9abe` (round-55 wave-2), which is where
  the third FAIL line first appears.

## HEAD DEPENDENCE:

Revision resolution: `os.environ.get("KAKE_R52_SELFTEST_REV")`, else `git rev-parse HEAD` **of the process cwd**
(`git(os.getcwd(), "rev-parse", "HEAD")`); `root = os.getcwd()`. Files read from that revision with `git show` /
`git show_bytes` (the `base_files` list, lines 471–481, plus the `run_checks` reads at 176–354):

1. `corpus/SOURCES.md` (REGISTRY — rows, `used-by`, `opened`, C4/C8/C3)
2. `corpus/lessons/round-52.md` (LESSON — C5 Gate quote)
3. `.ufo/waves/round-52/sources/receipts.json`
4. `.ufo/waves/round-52/assimilation/pre-append/corpus/SOURCES.md` (MIRROR)
5. `.ufo/waves/round-52/assimilation/mirror-pin.json`
6. `.ufo/waves/round-52/assimilation/pre-append/census-argv.txt`
7. `.ufo/waves/round-52/assimilation/pre-append/census-stdout.txt`
8. `.ufo/waves/round-52/assimilation/pre-append/census-exit.txt`
9. `corpus/knowledge/yahoo-japan-rel-nofollow-semantics.md` (ADOPTED S374)
10. `corpus/knowledge/baidu-friendly-crawl-guidance.md` (S329)
11. `corpus/knowledge/baidu-mobile-matching-error-causes.md` (S312)
12. `.ufo/waves/round-52/sources/S374.html`, 13. `…/S329.html`, 14. `…/S312.html`

Beyond blobs it reads the commit graph at the resolved revision: `git log --diff-filter=A --format=%H <rev> -- MIRROR`
and `git merge-base --is-ancestor <add_commit> <rev>` (C8 strict-ancestry). No `open()` read of the working tree — the
only `open()` is the fixture writer; working-tree writes go to `<cwd>/.ufo/waves/round-52/selftest/quote/work/` and are
removed (`shutil.rmtree` before and, with `ignore_errors`, after). Not read: `corpus/README.md`, `SKILL.md`,
`corpus/knowledge/*` other than the three adopted entries, anything under `.ufo/waves/round-56/`.

Extra-commit probe (`D2=/tmp/exectally2.UCzOaV`, clone of the lane at base, then one commit
`6f4e3ece12b1` with `-c user.name=selftest -c user.email=selftest@local`): +1 registry row `S999` in
`corpus/SOURCES.md`, +1 line `corpus/README.md`, new `corpus/knowledge/zz-r56-probe.md`, new
`.ufo/waves/round-56/exec-tally-quote-probe.md`, +1 eight-cell gate-registry row `probe-gate` in `SKILL.md`.

- Rerun unpinned at `6f4e3ec` (HEAD of D2): exit **1**, wall 1.360s, **17/18**, C8 note changed to
  `registry rows 157 != mirror rows 145 + 3` — proof that `corpus/SOURCES.md` is read at HEAD, and that the tally is
  unchanged only because the `pass` fixture was already failing.
- Rerun pinned `KAKE_R52_SELFTEST_REV=1ae8de5d4dee` in the same D2: exit **0**, wall 0.948s, **18/18** — proof that the
  README line, the extra knowledge file, the `.ufo/waves/round-56/` file and the extra SKILL.md row are invisible to the
  selftest.
- Deletion probes (`D3=/tmp/exectally3.kLuCyJ`, one commit each): removing `corpus/SOURCES.md` → exit **2**, stderr
  `selftest: missing round-52 evidence corpus/SOURCES.md`, no tally line; removing the adopted
  `corpus/knowledge/yahoo-japan-rel-nofollow-semantics.md` → exit **2**, `… missing round-52 evidence
  corpus/knowledge/yahoo-japan-rel-nofollow-semantics.md`. An absent input is unevaluable (the counter would report
  `tally_unparsable` → exit 2), never a pass.
- Net: the denominator 18 is structural and HEAD-independent; the numerator is HEAD-dependent through
  `corpus/SOURCES.md` (row count, `used-by`, `opened`) and through the three adopted entries and the round-52 evidence
  blobs. Concretely: registry growth 148 → 155 flipped 18/18 → 17/18; the `faf9abe` edit to the S374 entry added the
  second cause. `corpus/README.md`, `SKILL.md` and `.ufo/waves/round-56/` do not affect it.

## REPLACEMENT CELL:

Self-test cell, verbatim (command first in backticks; other prose kept; the counter compares claim 18 with the observed
denominator 18):

```
`KAKE_R52_SELFTEST_REV=1ae8de5d4dee python3 -B .ufo/waves/round-52/c52_quote_truth.py --selftest` (18 fixtures, sandbox repos; receipt `.ufo/waves/round-52/control/c2-quote-selftest.txt`; fixtures built from the committed round-52 evidence at `KAKE_R52_SELFTEST_REV`, default `HEAD` — the pin is required because the pass fixture asserts the measured registry equals the round-52 mirror plus the three adopted rows)
```

Checked against the counter, not by eye: the cell was committed in D2 as `7b4eed54bf8f` and measured with
`c56_selftally.measure(D2, 7b4eed54bf8f, pop=[POP[7]], expected=1)` →
`quote-truth-counter: claim=18 observed=18/18 OK`, `tally_mismatches=0`, exit **0**. The claim regex `\((\d+) fixtures`
captures 18 from `(18 fixtures, …)`; `documented_command` shlex-splits the leading `VAR=value` word as an env
assignment (`run_command` sets it in the child env, argv[0] stays `python3`); `_is_selftest_span` sees the pinned script
plus `--selftest`. `tool_changed` stays clean because the script blob at base is
`1bd6e78f80e69eb037e1083eb55487a9b6bd83a1` and is the same blob at `1ae8de5d4dee` and at base.

Why the text cannot simply be left alone: the claim integer already equals the denominator, so no wording change fixes
the row — only a documented command that exits 0 with A == B can. Pinning to the round-52 evidence commit (the revision
the committed receipt `c2-quote-selftest.txt` itself records: `18/18 (fixture revision 1ae8de5d4dee)`) is the only
lever, because the counter pins the script blob to base and therefore forbids fixing the selftest's own code.

## RISKS:

- The pinned row now certifies the *frozen* round-52 evidence, not the current registry. That is honest for a selftest
  whose `pass` fixture hard-codes "registry == mirror + 3", but a reader may mistake 18/18 for a live-tree check; the
  parenthetical above says so explicitly. If the L1 prefers no pin, this row cannot meet C1 at all (exit 1, A != B).
- `c52_quote_truth.py` must not be edited in W2 (or later): `tool_changed` compares its blob at the measured revision
  with `BASE_REV`, so any repair of the C5/C8 fixture inputs inside the script fails the row regardless of cell text.
- C3 compares the adopted rows' `opened` cell with the constant `ROUND_DATE = "2026-10-25"` (line 215); any later edit of
  those cells breaks the unpinned `pass` fixture too. No wall-clock dependence exists (`parse_iso` only validates ISO
  8601; no `datetime.now()` anywhere), so the tally is clock-stable.
- Fixed work directory: the selftest builds fixtures under `<cwd>/.ufo/waves/round-52/selftest/quote/work`. Two
  concurrent runs in the same checkout collide — observed once here (parallel invocation): exit 1 with
  `fatal: cannot copy … /hooks/commit-msg.sample: File exists` plus a `CalledProcessError` traceback and no tally line
  (a counter reading that output would classify it `tally_unparsable`, exit 2). The rerun sequentially was clean. A
  crashed run can leave a stale `work/` directory in the checkout.
- Running the documented command in the lane itself would create and delete files in the working tree; the counter
  avoids that by cloning. Any manual reproduction must use a clone, not the lane.
- Env inheritance: the selftest reads only `KAKE_R52_SELFTEST_REV` explicitly but inherits the whole environment into
  its `git` children (the counter adds only `PYTHONDONTWRITEBYTECODE=1`); a stray `GIT_*` variable could perturb the
  fixture repos. Not exercised here.
- Only this row was measured with the counter; the other nine rows' verdicts were not re-derived (out of this seat's
  scope).

VERDICT: row `quote-truth-counter` claims 18 fixtures = the observed denominator, but the documented unpinned command prints 17/18 and exits 1 (two runs, byte-identical, 1.83s/1.88s) because of registry drift (C8, from fd91527a2860) and the S374 entry line-72 quote (C5, from faf9abe); pinning `KAKE_R52_SELFTEST_REV=1ae8de5d4dee` yields 18/18 exit 0 and the resulting cell measures OK (claim=18, observed=18/18) in the counter.
