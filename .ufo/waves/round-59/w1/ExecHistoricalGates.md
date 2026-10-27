# ExecHistoricalGates

No-harm baseline for round 59: every earlier registry gate named in the seat spec was run at the round base
revision `fd6303ce5c14b3f892dec586297a942ab6e4193b` (contract `BASE_REV`), plus five gates whose SKILL.md rows are
already marked `historical`, so the L1 can compare the build against a measured base instead of a remembered one.
Each predicted harm below was reproduced in a throwaway fixture clone before it was written down; statements that
could not be reproduced are marked `[INFERENCE]`.

Method — one `git clone -q --shared` of the lane under `/fast/scratch/hyaku/kake-r59/ExecHistoricalGates/clone`,
checked out at `fd6303ce…`; every counter invoked as
`python3 -B <counter> --root <clone> --revision fd6303ce…` from inside that clone (`c58_resolver_cases.py` also
`--work <scratch> --seed 58`; `c57_idresolver_gate.py` with `--fleet /home/vgpnk/Projects/shokunin`). A second clone
at the lane tip `cb685273cc9e331b51f45485793d5d1c91184b3a` supplied the two tip-state values. No write to the lane,
its index or its jj state; scratch removed after the transcripts were copied beside this file. No tool was installed
or upgraded (no `pacman`, no `uv`, nothing in `~/.local/bin`).

Every value quoted below is a saved transcript beside this file: `ExecHistoricalGates.files/<counter>.txt` for the
base runs, `…/c58_receipt_rewrites_at_tip.txt` for the tip check, and `…/probe-H1…H5*.txt` for the reproduced harms
(each records the probe shape, the counter output and its exit code).

## RUNS

All six assigned gates are **green at the base revision**, exit 0:

| gate (SKILL.md row) | exit | summary line at `fd6303ce` |
|---|---|---|
| `.ufo/waves/round-58/c58_resolver_cases.py` (`resolver-cases-counter`) | 0 | `C2 resolver-cases 14/14 met=True` — K1–K7 PASS, P1–P7 PASS, `P6_tool_selftest PASS exit=0 ('59','59')`, `P7_real_lane_green PASS exit=0 ids_cited=108 ids_resolved=108 dangling=0` |
| `.ufo/waves/round-58/c58_quote_truth.py` (`baidu-crawler-identification-quote-truth-counter`) | 0 | `C3 quote-truth 8/8 met=True` — C1–C8 PASS, registry 162 rows |
| `.ufo/waves/round-58/c58_receipt_rewrites.py` (`receipt-rewrite-counter`) | 0 | `C1 receipt-rewrites events=19 undisclosed=0 phantom=0 malformed=0 wrong_kind=0 unpointed=0 symlinks=0 new_rewritten=0 new_receipts=2 met=True` |
| `.ufo/waves/round-57/c57_idresolver_gate.py` (`id-resolver-gate`) | 0 | `C2 id-resolver 5/5 met=True` — `G2_selftest PASS selftest: 59/59`; `G4_red_before PASS exit=1 summary=(99, 94, 5, 5, 0)`; `G5_green PASS exit=0 summary=(108, 108, 0, 0, 0); reference ids_cited=108` |
| `.ufo/waves/round-55/c55_readme_index.py` (`readme-index-counter`) | 0 | `C1 readme-index index_mismatches=0 knowledge_files=56 met=True` (`coverage_rows=58`, all seven mismatch classes 0) |
| `.ufo/waves/round-56/c56_selftally.py` (`selftest-tally-counter`) | 0 | `C1 selftest-tally tally_mismatches=0 rows_checked=10 met=True` — all ten tallies `claim=observed/observed OK` (45, 106, 204, 235, 23, 9, 19, 18, 44, 54) |

Extra context runs (the rows marked `historical`; all red at the base, as their rows predict):

| gate | exit | summary line at `fd6303ce` |
|---|---|---|
| `.ufo/waves/round-52/c52_quote_truth.py` | 1 | `6/8 met=False` — `C5_quote_truth`, `C8_mirror_bytes` |
| `.ufo/waves/round-55/c55_quote_truth.py` | 1 | `6/8 met=False` — `C7_validate_before_append`, `C8_mirror_bytes` |
| `.ufo/waves/round-56/c56_quote_truth.py` | 1 | `6/8 met=False` — `C7_validate_before_append`, `C8_mirror_bytes` |
| `.ufo/waves/round-57/c57_quote_truth.py` | 1 | `6/8 met=False` — `C7_validate_before_append`, `C8_mirror_bytes` |
| `.ufo/waves/round-57/c57_receipt_pins.py` | 1 | `C1 receipt-pins new_unpinned=4 new_receipts=0 scorecard_pin=0 met=False` (failing lines: `scripts/id_resolver.py` differs from `countersFrozenAt`; three round-57 `after-c*` receipts carry a `revision:` pin but no `measured=` entry) |

Tip-state checks (`cb68527`): `c58_receipt_rewrites.py` still `met=True`, `events=19`, `new_receipts=2` — the round-59
contract commit's five new files under `.ufo/waves/round-59/controls/` are first additions and create no event.

## HISTORICAL MARKINGS

Of the six assigned gates, **none is marked `historical` in SKILL.md today**; one becomes historical by its own
recorded condition this round:

- `readme-index-counter` — SKILL.md line 1233, Kind `gate (offline, committed bytes only; no network)`. No marking.
- `selftest-tally-counter` — line 1253, Kind `gate (offline, committed bytes only; runs the ten documented selftests …)`. No marking.
- `id-resolver-gate` — line 1274, Kind `gate (differential: a reference implementation inside the gate against the tool …)`. No marking.
- `receipt-rewrite-counter` — line 1293, Kind `gate (offline; first-parent history walk … against the round-58 ledger)`. No marking.
- `resolver-cases-counter` — line 1294, Kind `gate (the tool at the revision against gate-built fixture lanes …)`. No marking.
- `baidu-crawler-identification-quote-truth-counter` — line 1295, Kind `gate (offline, committed bytes only; no network)`; its
  Pinned-values cell says "mirror pins the 160-row base registry **(historical once a later round appends a row)**". Round
  59 appends two rows, so this row's own text now requires the marking to be added (see H2).

Rows that carry the `historical` marking today (measured here for context, all red at base exactly as marked):

| SKILL.md line | row | marking as written |
|---|---|---|
| 1216 | `quote-truth-counter` (r52) | "historical: green at its round-52 measured revision `1ae8de5d…` only; red on every later tree by design — its mirror pins the 148-row registry" |
| 1234 | `yahoo-robots-quote-truth-counter` (r55) | "historical: green at `64c0ce12…` only; red on later trees by design — mirror pins 156 rows" |
| 1254 | `yahoo-crawl-handling-quote-truth-counter` (r56) | "historical: green at `4cb225fb…` only; red on later trees by design — mirror pins 158 rows" |
| 1273 | `receipt-pin-counter` (r57) | "historical from round 58: green at `32754df…`; red on later trees by design because the frozen file set includes the round-57 resolver and receipts" |
| 1275 | `baidu-dead-link-quote-truth-counter` (r57) | "historical from round 58: green at `32754df…`; red once a later round appends a registry row — mirror pins 158 rows + the 2 adopted" |

The section note at lines 1288–1289 already records the reason for the four quote-truth markings ("routed defect D3 of
the round-57 spot-check; `.ufo/waves/round-58/w1/ExecHistoricalGates.md`").

## PREDICTED HARMS

Each item was reproduced with a minimal, build-shaped commit in a private fixture clone; the reproduction is quoted.
These are *by design* reds the build creates, not defects of the counters — but the L1 must expect them and decide
whether a row gets a historical marking or the build changes shape.

**H1 — `c55_readme_index.py` turns red (`head_changed`) on the C3 correction, and cannot be kept green while C9 holds.**
`c55` requires every knowledge file present at its base `fcaf4b85` to be preserved **byte-for-byte as a prefix**
(`new.startswith(old)`). `crawler-identity.md` is unchanged between `fcaf4b85` and `fd6303ce`, so that prefix is the
whole 74-line file; C9 of the round-59 C3 counter requires the correction to be *inserted where the stale bullet ends*
(`if tag == "insert" and i1 == end and end <= s + 1 + STALE_WINDOW`, `c59_quote_truth.py` C9) — i.e. at line 35, mid-file.
Reproduction (insert one correction line at that index, plus the two new entries, their coverage-map rows and the two
registry rows — a fully correct C3 build): `C1 readme-index index_mismatches=1 knowledge_files=58 met=False …
head_changed: crawler-identity.md`, exit 1. A correction appended at end-of-file would keep `c55` green but fails C9.
So the build's correct shape forces one live gate red; the L1 needs either a historical marking on
`readme-index-counter` (naming `head_changed: crawler-identity.md`) or an explicit decision recorded in the round.
Separately, if the two new entries are not added to the `corpus/README.md` coverage map, `c55` also reports
`unindexed=2`; `thin` needs ≥5 whitespace tokens per Coverage cell sharing a word with the entry head, and `multi`
forbids a row naming more than two files.

**H2 — `c58_quote_truth.py` turns red as soon as the two registry rows land (`C7` + `C8`).**
`C8` demands `len(rows) == len(mirror_rows) + 2` against its frozen 160-row mirror, and `C7` demands the round-58
validated scratch registry be byte-equal to the landed registry. Reproduction (two well-formed rows appended to
`corpus/SOURCES.md`): `6/8 met=False`, `C7 … validated scratch registry is not byte-equal to the landed registry`,
`C8 … registry rows 164 != mirror rows 160 + 2`. This is the condition line 1295 already names, so the row must be
marked historical this round; leaving it unmarked makes SKILL.md claim a live gate the tree cannot satisfy.

**H3 — `c57_idresolver_gate.py` G2 fails if `scripts/id_resolver.py`'s source names `.ufo/`, `reference(` or
`c57_idresolver_gate`.** `G2` greps the tool blob for exactly those three strings
(`judge_ref = [w for w in ("c57_idresolver_gate", ".ufo/", "reference(") if w in src]`). Reproduction (one added
comment line `# see .ufo/waves/round-59/c59_resolver_cases.py …`): `G2_selftest FAIL … the tool's source names the
judge: ['.ufo/']`, `4/5 met=False`. Heed this in the C2 build: a docstring citing the round-59 counter path, or a
helper named `reference(...)`, silently converts a green history gate into a red one. `G2` also requires **exactly one**
`selftest:` line, the last stdout line, of the form `selftest: N/N` with N == N ≥ 16; `G5_green` then requires the
tool's DANGLING lines and summary to equal the gate's frozen reference at the measured revision with `ids_cited ≥ 100`
and `dangling == 0`.

**H4 — `c56_selftally.py` turns red on any `scripts/fixtures/` change, on any edit to a `*.py` that existed in the
same directory at its base `e48354b`, or on a duplicated SKILL.md row name.**
- Adding one file under `scripts/fixtures/` (e.g. a resolver fixture committed to the tree): `tally_mismatches=6` —
  `base-path-audit, source-recheck-audit, robots-expectation-audit, sitemap-file-audit, redirect-expectation-audit,
  commit-citation-lint` all report `MISMATCH tool_changed`, exit 1. Round-59 test data must stay in scratch, not in
  `scripts/fixtures/`.
- Editing `scripts/id_resolver.py` alone is **safe**: that file did not exist at `e48354b`, so it is not in the
  "beside it" set (`names` come from the base-revision `git ls-tree`). Verified: green, `tally_mismatches=0`,
  `rows_checked=10`.
- Editing any pre-existing `scripts/*.py`, any `*.py` in `.ufo/waves/round-52/` or `.ufo/waves/round-55/`, or the ten
  rows' `Self-test` cells (command must stay exactly `[pin] python3 -B <script> <pinned args>`, one integer matching the
  claim regex) also reddens it. A second SKILL.md row whose first cell repeats one of the ten names (e.g. a new
  `readme-index-counter` row) gives `readme-index-counter: … MISMATCH duplicate_row`, exit 1 (reproduced).

**H5 — `c58_receipt_rewrites.py` turns red if any committed receipt under *any* round's `control(s)/` is modified or
deleted after its first commit.** New receipts added once are first additions and are not events (tip check: `events=19`,
`met=True` after the round-59 contract commit), but a rewrite is an `M` event the round-58 ledger does not cover.
Reproduction (`base-c2-resolver-cases.txt` in `.ufo/waves/round-59/controls/` edited after commit):
`events=20 undisclosed=1 … UNDISCLOSED M .ufo/waves/round-59/controls/base-c2-resolver-cases.txt`, exit 1. Round 59's
receipt rule ("committed once, never rewritten; a re-run lands under a new file name") is therefore load-bearing for
this historical gate, and no receipt may be written under `.ufo/waves/round-58/controls/` (`new_receipts` must stay 2).

**H6 — `c58_resolver_cases.py` stays green only if the fixed tool keeps the round-58 contract and keeps accepting a
non-repository `--root` in worktree mode.** Its P1–P5 fixtures are plain directories (no `git init`), and P1/P2/P3/P5
expect exit 0 / exit 1 from worktree-mode runs on them; a K14 fix that requires a git toplevel for *every* mode would
turn these into exit 2 and redden the gate. Its P6 floor is 55 (a 66-check tool passes), and P7 needs `dangling=0` with
`ids_cited ≥ 106` at the measured revision — satisfied after C3 (108 → 110 if both new entries resolve). `[INFERENCE]`
on which case breaks first, since the C2 build is not in the tree yet; the structural facts are from the counter source.
The same worktree-mode constraint applies to `c57_idresolver_gate.py` G3/G5, whose fixture lanes are also plain
directories.

**Not a new harm:** `c57_receipt_pins.py` is already red at the base (`new_unpinned=4`, `new_receipts=0`,
`scorecard_pin=0`) and is marked historical from round 58; the round-59 SCORECARD edit cannot make it greener, and its
predicate still asks for three round-57 pins. `c52/c55/c56/c57_quote_truth` are already red at the base for their own
mirror pins and are unaffected by any further append beyond staying red.

VERDICT: All six assigned gates are green at `fd6303ce` (14/14, 8/8, met=True on 19 events, 5/5, 0 mismatches/56 files, 0/10 tallies); five build-shaped harms reproduced — H1 c55 `head_changed` on the mandated mid-file correction (unavoidable while C9 holds), H2 c58 quote-truth mirror on the two new rows, H3 c57 G2 on a `.ufo/` mention in the tool source, H4 c56 on any `scripts/fixtures/` change or duplicate SKILL row, H5 c58 receipt-rewrites on any receipt rewrite — plus H6 (worktree-mode `--root`) as an inference-only risk.
