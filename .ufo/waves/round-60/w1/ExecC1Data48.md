# ExecC1Data48

C1 calibration data for the four round-48/49 member counters. Method: `git clone -q --shared` of the lane
detached per revision under `/fast/scratch/hyaku/kake-r60/ExecC1Data48/` (scrubbed GIT_*, TMPDIR=scratch,
`timeout 1800`, `python3 -B <counter> --root . --revision <rev>`); the counter runs **as committed** at each
revision (matching the c60 observation semantics: worktree = revision under test, `--root .` = that clone).
All 16 runs executed 2026-10-27; full logs retained in `ExecC1Data48.files/*.log`.

## MEMBERS:

- `.ufo/waves/round-48/c48_lint_count.py` — measured rev `af7b217c9b0837428e50c944adfab9f5c692a50f`
  (source line: SCORECARD.md:4056 `Measured commit: af7b217c…`; also `.ufo/reports/round-48/kake.md:87`
  `after af7b217c9b0837428e50c944adfab9f5c692a50f (exit 0)` and receipt `verification/c2-after-af7b217.json`).
  exit@base `97cdc122` = 0 (`met:true`). exit@measured = 0 (`met:true`). Ever green: yes — measured 0,
  tip `fd917a42567ff3642c0f7930659681141200b419` 0, base 0; parent `a370d20` counter absent (cannot exec).
  Honest label: **live**.
- `.ufo/waves/round-48/c48_quote_truth.py` — measured rev `af7b217c9b0837428e50c944adfab9f5c692a50f`
  (same sources; receipt `verification/c1-after-af7b217.json`).
  exit@base = 0 (`C1 passed 4/4 met=True`). exit@measured = **1** (`C1 passed 0/4 met=False`, `retained text
  absent` on all 4 ids) — the pre-fix counter blob `cd48f7ba…` read `<root>/<textPath>`; fix blob `c4d3c66c…`
  (`os.path.dirname(RECEIPTS)` join) landed at `fd917a42`, the disclosed instrumentation fix
  (SCORECARD.md:4071-4075; `corpus/lessons/round-48-verifier-spotcheck.md:37` records the identical
  re-measurement: pre-fix counter at `af7b217` exits 1). Ever green: yes — tip `fd917a4` 0, base 0;
  parent `a370d20` counter absent. Honest label: **live** (red at its own measured rev is the disclosed
  counter-blob bug, not a data regression; the counter as frozen at tip/base is green).
- `.ufo/waves/round-49/c49_order.py` — measured rev `1c846ed2d67b1692ea966be064f0fc04542763c6`
  (source line: SCORECARD.md:4103 `Measured commit 1c846ed2…`; `corpus/lessons/round-49-verifier-spotcheck.md:5`
  `Measured claim commit: 1c846ed2…`; receipt `verification/c1-after-1c846ed2.json`).
  exit@base = 0 (`C1 order 1/1 met=True`). exit@measured = 0. Ever green: yes — measured 0, tip
  `b3ae50efbca6c569720887b03f3fad7710abde8a` 0, base 0; parent `99fa9d3f` = 1 (`proof absent`, pre-append
  commit — expected red). Honest label: **live**.
- `.ufo/waves/round-49/c49_quote_truth.py` — measured rev `1c846ed2d67b1692ea966be064f0fc04542763c6`
  (same sources; receipt `verification/c2-after-1c846ed2.json`).
  exit@base = 0 (`C2 passed 2/2 met=True`). exit@measured = 0. Ever green: yes — measured 0, tip `b3ae50e` 0,
  base 0; parent `99fa9d3f` = 1 (`no registry row, entry file absent, no gate quote` — expected red).
  Honest label: **live**.

All four counters exit 0 at base `97cdc122379711c2b02a8970752c8782da3ac81d` → all four honest labels are
`live`; none currently has a SKILL.md registry row (the contract's 12-member `unregistered` list includes
c48 x2, c49 x2).

## ROWS:

Drafted complete 8-cell rows in `ExecC1Data48.files/rows.md` (lane format, no `|` inside a cell):
`citation-lint-existence-counter`, `client-rendering-quote-truth-counter`, `pre-append-order-counter`,
`crawl-budget-quote-truth-counter` — each `gate (live; …)`, entry command `python3 -B <path> --root . --revision <commit>`
with the real optional flags read from each parser (`[--json <path>]` all four; `[--tool-file <path>]` on
c48_lint_count), verdict maps `0=met / 1=not met / 2=could-not-evaluate / 64=usage` (the exact codes each
`main()` returns, read from the code).

## NOTES:

- Self-test cells: c48_lint_count, c49_order, c49_quote_truth have no selftest flag (unknown argument → 64).
  c48_quote_truth's parser accepts `--selftest` but the function is undefined — verified: it crashes
  `NameError: name 'selftest' is not defined`, exit 1. Rows say so honestly.
- `c48_quote_truth` R4 reads the retained text from the **worktree** (`open(os.path.join(root, dirname(RECEIPTS), textPath))`),
  not `git show`; every other read is committed bytes. Noted in its row.
- `c48_lint_count` builds a scratch repo under TMPDIR and runs `scripts/citation_lint.py` as committed at
  `--revision`; its Write scope cell names the scratch repo, not the lane.
- Counter blob pins (git blob ids at base): c48_lint_count `10200e91…`, c48_quote_truth `c4d3c66c…`,
  c49_order `7ca94016…`, c49_quote_truth `0808c865…` (last two match `round-49-verifier-spotcheck.md:27`).
- Parent-of-measured runs: r48 parent `a370d207` predates the counters (file absent, reported as cannot-exec);
  r49 parent `99fa9d3f` is the pre-append commit — both r49 counters correctly red there (do-nothing controls).
- No installs needed (python3 + git only). No pacman run. Scratch `/fast/scratch/hyaku/kake-r60/ExecC1Data48/` deleted after logs copied into `.files/`.

VERDICT: All four members measured — exit@base 0, exit@measured: lint_count 0, quote_truth(48) 1 (pre-fix blob), order 0, quote_truth(49) 0; all honestly `live`; rows drafted in ExecC1Data48.files/rows.md.
