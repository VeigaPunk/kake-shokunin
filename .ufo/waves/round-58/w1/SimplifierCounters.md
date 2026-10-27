# SimplifierCounters

Round-58 w1, leaf seat. Scope read: `.ufo/waves/round-58/c58_receipt_rewrites.py` (C1, 395 lines) and
`.ufo/waves/round-58/c58_resolver_cases.py` (C2, 230 lines). No original was edited; every variant and run
happened in `/fast/scratch/hyaku/kake-r58/SimplifierCounters` and was deleted after its receipts were copied into
`SimplifierCounters.files/`.

## Axes

- **W** source weight: lines and bytes of the counter.
- **P** process cost: `git` processes spawned per single measurement.
- **B** frozen behaviour: C1 selftest tally, C1 receipt at the frozen base, C2 twelve-case receipt.
- **C** number of ways the same act is done (invocation convention, parse convention).

## Baseline (measured, not assumed)

- Originals match `contract.json` `counterSha256v1`: C1 `dace35ce…`, C2 `60c814aa…`.
- C1 `--selftest`: **18/18**, exit 0. C1 `--revision 044048597d62f3199494b63b36e90dd57825e350`:
  `events=19 undisclosed=19 phantom=0 malformed=0 wrong_kind=0 unpointed=0 new_rewritten=0 new_receipts=0 met=False`,
  EXIT=1 (`receipts/C1-base-ref.json`).
- C2 at the same revision: **7/12**, EXIT=1 — K1–K5 FAIL, P1–P7 PASS (`receipts/C2-base-ref.txt`).
- Toolchain: Python 3.14.8, git 2.56.0 (`receipts/toolchain.txt`).

## PROPOSALS

Each proposal was applied to a scratch copy, then the *same* two narrow checks were re-run against the frozen
baseline: `TMPDIR=<scratch> python3 -B <copy> --selftest`, and `--root <lane> --revision 044048… --json` diffed
byte-for-byte against `receipts/C1-base-ref.json`. All five C1 steps were applied cumulatively; A3 was also applied
alone to the original to rule out masking. Every step kept 18/18 and a byte-identical base receipt; A5 alone cannot
change output (prose only).

### A1 — delete the per-event `rev-parse --verify` (`events()`)

- Change: drop `has_parent` and the `… if has_parent else None` arm; `"fromBlob": blob_id(root, parent, path)`
  (`C1-A1-has-parent.diff`).
- Kept behaviour: identical event set and identical `fromBlob`. `blob_id()` already yields `None` for an unresolved
  rev: `git ls-tree <bad-rev> -- <path>` exits 128, so `git(…, check=False)` returns `""` and the loop falls through
  to `return None` (probed: `(128, 'fatal: Not a valid object name …')`).
- Evidence: 18/18 unchanged; base receipt byte-identical (`cmp` clean); `git` execs at the base **61 → 42**
  (`receipts/C1-spawn-counts.txt`); 0/19 events lack a parent at base and at HEAD (`receipts/flags-*.txt`).
- The else-arm is *unreachable*, not merely unused: a receipt path's first addition is never an event, so a
  parentless commit cannot be a receipt event — a root commit carrying a receipt produces `events=[]` (probed).

### A2 — delete the dead multi-line-header branch (`events()`)

- Change: `head`/`commit`/conditional `rest` construction → `commit = parts[0].strip("\n")` plus
  `rest = [p.strip("\n") for p in parts[1:]]` (`C1-A2-dead-head-branch.diff`).
- Kept behaviour: same parse. `--format=%x01%H` with `-z` makes the hash its own NUL-terminated token, so the
  header token never carries a second line: `"\n" in head` fired **0 times over 217 commits** at base and **0 over
  219** at lane HEAD (`receipts/flags-base.txt`, `flags-head.txt`).
- Evidence: 18/18; base JSON and the `--list` text report byte-identical (`receipts/C1-text-report-ref.txt`).

### A3 — one git call and one parse for blob ids

- Change: the 7-line `ls-tree -z` record loop → `git rev-parse --verify -q f"{rev}:{path}"` (`C1-A3-blob-id.diff`).
- Kept behaviour: 40-hex string or `None`. 0 mismatches over 19 events × 2 sides at base and at HEAD; 8 awkward
  names identical (`a b.txt`, `a"b.txt`, `中文.md`, `[x].txt`, `a*b.txt`, `semi;colon,.txt`, tab name, `plain.txt`);
  absent path → `None` on both; unresolved rev → `None` on both (`receipts/blobid-equivalence.txt`).
- Tradeoff, measured and bounded: the old code returned `None` when the path resolved to a non-blob; `rev-parse`
  returns the tree/commit oid there (probe: dir `138512724c`, gitlink `70dce20fcb`). That input is reachable only
  for a **gitlink** at `<controls>/<name>`, because `--name-status` never emits a plain directory path (probe: a
  directory under `controls/` emits only `dir/inner.txt`). The lane holds 0 gitlinks and no `.gitmodules`.
  Restoring the type check costs one `cat-file -t` per side — exactly the calls A1 removed.

### A4 — one git invocation path (`_run`)

- Change: add `_run()` (3 lines) and route `git()`, `_text()` and both inline `subprocess.run(…)` calls in
  `pointed()` through it (`C1-A4-shared-git-runner.diff`). `_text()` keeps its `"replace"` decode, so the blob
  decoding is unchanged; `-c core.quotePath=false` is inert for `cat-file`/`rev-parse`.
- Kept behaviour: same argv, same scrubbed env, same return-code test at every site; `pointed()`'s two sites keep
  their exact success conditions.
- Evidence: 18/18; base receipt and text report byte-identical; spawns at the base **42 → 42** — the value is one
  convention, not speed (`pointed`/`_text` are only reached for disclosed entries and the base has none). The
  selftest's four note cases (pointer-free, absent path, resolvable commit, empty note) are what exercise them.

### A5 — stale docstring name

- Change: "first-parent-**free** ancestry" → "first-parent ancestry" (`C1-A5-docstring.diff`). The code has walked
  `--first-parent` since v1; the prose stated the opposite of what it does.
- Evidence: prose only; 18/18 and base receipt identical.

### C2-P6 — drop the tool copy in P6

- Change: run `work/id_resolver.py` with `cwd=<empty p6 dir>` instead of `shutil.copy`-ing it into that dir
  (`C2-P6-tool-copy.diff`).
- Kept behaviour: P6's intent — the tool's own selftest in a clean cwd, under `-B`. The selftest roots its fixtures
  in `tempfile.mkdtemp` (`scripts/id_resolver.py:330`) and never reads `__file__` (no occurrence in the file), so
  the copy decides nothing.
- Evidence: C2 output at the base identical after normalising the random scratch suffix (only `p5`'s path differs;
  `receipts/C2-base-ref.txt` vs `C2-base-new.txt`); P6 `PASS exit=0 ('49','49')` in both runs.

**Totals.** C1 395 → 387 lines (−8), 20 591 → 20 025 bytes (−566), 61 → 42 `git` execs at the frozen base
(−31 %). C2 230 → 229 lines, same 12-case verdict. Diffs: `C1-all.diff`, `C1-A*.diff`, `C2-P6-tool-copy.diff`;
whole proposed files under `proposed/`; checksums in `SHA256SUMS`. Both proposed counters keep the v1 CLI and exit
codes, but their hashes differ from `counterSha256v1`, so adopting either means re-freezing the contract entry.

## REJECTED

1. **Delete `-m` and/or `--full-history` from the log command.** Measured inert on this host: on git 2.56
   `--first-parent` alone reproduces the `--full-history --first-parent -m` event set on three merge fixtures
   (conflict merge resolved to a third value, clean merge, side-branch-only change) and on the lane, where all five
   flag combinations give the same 19 events at base and at HEAD (`receipts/merge-fixture-flags.txt`,
   `flags-*.txt`). Rejected anyway: a git that does not derive merge diffs from `--first-parent` would silently lose
   events, and losing an event is a false green in a calibration counter. Two tokens is not worth a
   version-dependent blind spot; `-m` is also the documented spelling for merge diffs.
2. **Table-drive K1–K3 in C2.** −3 lines, 0 saved processes, and three dense tuple rows replace nine obvious blocks;
   clarity loses more than weight gains.
3. **Hoist `clean_env()`/`env()` to module constants.** No measurable spawn change (a dict rebuild is noise against
   a process spawn) and it hides the per-call `GIT_*` scrub, which is part of what these counters must do.
4. **Hoist `import difflib` out of `classify()`.** Not weight (one line either way) and the local import keeps
   startup free of a module only disclosed entries need.

## Bounds

- No other dead weight found in C2: `ruff --select F,ARG` clean on both counters and `vulture --min-confidence 80`
  silent on both. C2's remaining size is the twelve-case fixture surface, which is the contract.
- Originals untouched: their sha256 re-checks equal to `counterSha256v1`; the lane's `git status --porcelain` shows
  only the round-58 `w1/` artifacts this wave writes. No git/jj mutation was performed in the lane.
- Unrun: no wall-clock comparison (host loaded, and process counts are the honest cost unit); no C1 run at a tip
  where the ledger is present, so `pointed`/`_text` behaviour at a green tip rests on the selftest cases, not on a
  lane measurement.
- Scratch `/fast/scratch/hyaku/kake-r58/SimplifierCounters` removed; all receipts under
  `.ufo/waves/round-58/w1/SimplifierCounters.files/receipts/`.

VERDICT: six behaviour-preserving deletions proposed (C1 −8 lines, −19 git execs per measurement; C2 −1 line); the `-m/--first-parent/--full-history` deletion rejected as a false-green risk.
