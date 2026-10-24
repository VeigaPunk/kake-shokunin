# ScribeC2Repairs — round 44 wave 2 (scribe, axis: freshness)

Seat: `kake-r44.ScribeC2Repairs`. Item: draft the three C2 repair paragraphs into one scratch
file; **do NOT append to the ledgers**.

## Behavior

Drafted the three C2 repair paragraphs as append-ready plain text in one scratch file
`/fast/scratch/hyaku/kake-r44/c2-repairs.md` (three fenced ` ```text ` blocks, one per figure,
each naming its receipt file(s), its derived value, and the spot-check section it repairs).
Nothing was appended to `LOG.md` or `SCORECARD.md`; no lane file was written except this report.
Every figure was re-derived from the **committed receipts at `master`** (`git show master:...`),
never copied from prose.

| Figure | Ledger | Receipt(s) at `master` | Derived (raw) | Quoted form |
|---|---|---|---|---|
| `rescore-tally` | `SCORECARD.md` | `.ufo/waves/round-43/verification/l1-rescores/*.json` — 14 JSON receipts (11 in `exits.txt`, 3 in `exits2.txt`, all `exit=0`) | 14 distinct `toolSha256` | `re-scored 14 of the 27` |
| `donothing-ratios` | `LOG.md` | `.ufo/waves/round-43/verification/freeze/ref41-base.json` (blob `1f6acfe6b6d064f5d80a465de5236eaf8383ef9f`) | `ratios.T1` 4.207, `ratios.T5` 7.047 | `not met (T1 4.21, T5 7.05)` |
| `build-ratio-range` | `LOG.md` | `.../freeze/build-1.json` (blob `6a84f17c7b0e49cce59d1a2e52c2d19853b0a4f6`), `build-2.json` (`5a26c5384189e8890de0aa8ef20a8d887840859a`), `build-3.json` (`8239dae6ce44db77ed42b96640f83d59d36c7453`) | T1 {1.005, 1.009, 1.004}, T5 {1.105, 1.144, 1.215} | `T1 1.00–1.01, T5 1.11–1.22` (U+2013 EN-DASH) |

Spot-check sections repaired, cited in the text: §8.1 "Re-score tally overstates its receipts"
(`corpus/lessons/round-43-verifier-spotcheck.md:197-201`) for the tally; §8.5 "LOG keeps
superseded ratios" (`corpus/lessons/round-43-verifier-spotcheck.md:209-212`) for both LOG figures.

Rounding is the checker's own rule (`scripts/ledger_latest_check.py:rounded_like` — quantize to
the **quoted** string's decimal places, `ROUND_HALF_UP`): 4.207→4.21, 7.047→7.05, 1.004→1.00,
1.009→1.01, 1.105→1.11, 1.215→1.22.

## Gates

* **PASS — the item's named attack (the C2 ledger-latest contract).** The frozen checker
  `scripts/ledger_latest_check.py` takes the **LAST** match of each figure's pattern in its
  ledger; the draft was evaluated with that checker's own unmodified functions
  (`latest_match` / `derive_values` / `evaluate`) against (a) the committed `master` ledgers plus
  the three drafted paragraphs and (b) the current working-copy ledgers plus the same three
  paragraphs. Both scenarios: **3 figures, 0 mismatches**, exit 0. Literal-shape assertions
  (exact phrase present; EN-DASH confirmed) also pass.
* **PASS — no later superseding match.** In both scenarios the reported match line is inside
  the appended block, so each drafted paragraph is the last statement of its figure.
* **PASS — the prose-free derivation.** Every number in the draft is traceable to a receipt
  field at `master`; no value was taken from ledger prose.

### Decisive command output (verbatim)

Command 1 — derive the tally and the ratio figures from `master`:

```
$ git ls-tree -r --name-only master -- .ufo/waves/round-43/verification/l1-rescores
.ufo/waves/round-43/verification/l1-rescores/CtlHeadTail-V1c.json
… (14 .json + 14 .log) …
.ufo/waves/round-43/verification/l1-rescores/v8_memo_value_casefold_nonascii.json

$ python3 - <<'PY'   # for each committed .json: collect receipt["toolSha256"]
l1-rescore json receipts: 14 distinct toolSha256: 14
PY

$ python3 - <<'PY'   # for each freeze receipt: print met / ratios.T1 / ratios.T5 / seed
.ufo/waves/round-43/verification/freeze/ref41-base.json met= False ratios.T1= 4.207 ratios.T5= 7.047 seed= 43001 equalRuns= 11/11
.ufo/waves/round-43/verification/freeze/build-1.json met= True ratios.T1= 1.005 ratios.T5= 1.105 seed= 9325990526163 equalRuns= 11/11
.ufo/waves/round-43/verification/freeze/build-2.json met= True ratios.T1= 1.009 ratios.T5= 1.144 seed= 265206435053987 equalRuns= 11/11
.ufo/waves/round-43/verification/freeze/build-3.json met= True ratios.T1= 1.004 ratios.T5= 1.215 seed= 269853680553917 equalRuns= 11/11
PY

$ git show master:.ufo/waves/round-43/verification/l1-rescores/exits.txt   # 11 lines, all exit=0
$ git show master:.ufo/waves/round-43/verification/l1-rescores/exits2.txt  # 3 lines, all exit=0
```

Command 2 — the decisive check of the draft (`/fast/scratch/hyaku/kake-r44/ScribeC2Repairs/verify_c2.py`,
scratch only; imports the unmodified checker module, appends the draft in memory, writes nothing
to the lane repo):

```
$ python3 -B /fast/scratch/hyaku/kake-r44/ScribeC2Repairs/verify_c2.py
literal-shape assertions: PASS (exact phrases present, EN-DASH confirmed)
--- master ledgers + drafted paragraphs ---
  rescore-tally MATCH quoted=14 derived=14 SCORECARD.md:3406
  donothing-ratios MATCH quoted=T1 4.21, T5 7.05 derived=T1 4.21, T5 7.05 LOG.md:1694
  build-ratio-range MATCH quoted=T1 1.00–1.01, T5 1.11–1.22 derived=T1 1.00–1.01, T5 1.11–1.22 LOG.md:1702
  ledger-quotes: 3 figures, 0 mismatches
--- working-copy ledgers + drafted paragraphs ---
  rescore-tally MATCH quoted=14 derived=14 SCORECARD.md:3592
  donothing-ratios MATCH quoted=T1 4.21, T5 7.05 derived=T1 4.21, T5 7.05 LOG.md:1721
  build-ratio-range MATCH quoted=T1 1.00–1.01, T5 1.11–1.22 derived=T1 1.00–1.01, T5 1.11–1.22 LOG.md:1729
  ledger-quotes: 3 figures, 0 mismatches
TOTAL mismatches across both scenarios: 0
EXIT=0
```

Command 3 — the checker as run on the lane's current (uncommitted) ledgers, for context only;
this is **not** evidence for my draft (the repairs in the working copy were authored by another
seat, not by me):

```
$ python3 -B scripts/ledger_latest_check.py --root .
rescore-tally MATCH quoted=14 derived=14 SCORECARD.md:3576
donothing-ratios MATCH quoted=T1 4.21, T5 7.05 derived=T1 4.21, T5 7.05 LOG.md:1703
build-ratio-range MATCH quoted=T1 1.00–1.01, T5 1.11–1.22 derived=T1 1.00–1.01, T5 1.11–1.22 LOG.md:1706
ledger-quotes: 3 figures, 0 mismatches
EXIT=0
```

### Dead end recorded (not a blocker)

First run of the harness failed with
`ledger_latest_check.InputError: quoted value is not a non-negative decimal: '1.22.'` —
the checker's build-range pattern `T1\s+([\d.]+)–([\d.]+), T5\s+([\d.]+)–([\d.]+)` captures
`[\d.]+` greedily, so a sentence-ending period right after `1.22` is captured into the group and
the checker's `NUMBER_RE` rejects it. Fixed by ending the range with a space (parenthetical
follows) instead of a period; re-run then passed.

## Touched surfaces

Written by this seat:

1. `/fast/scratch/hyaku/kake-r44/c2-repairs.md` — **the deliverable**: the three drafted C2
   repair paragraphs (append-ready plain text in fenced blocks), plus the derivation table,
   checker-shape notes, provenance discipline notes and the verification description.
2. `/fast/scratch/hyaku/kake-r44/ScribeC2Repairs/verify_c2.py` — scratch verification harness
   (imports the unmodified checker; writes nothing to the lane repo).
3. `/fast/scratch/hyaku/kake-r44/ScribeC2Repairs/verify_c2.out` — captured harness output.
4. `/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-44/w2/ScribeC2Repairs.md` —
   this report.

Read-only: `LOG.md`, `SCORECARD.md`, `scripts/ledger_latest_check.py`,
`.ufo/waves/round-44/ledger-quotes.json`, `corpus/lessons/round-43-verifier-spotcheck.md`,
`.ufo/waves/round-43/w1/CriticC1Sizing.md`, and the committed receipts at `master`.

**Not written, not appended, not committed:** `LOG.md`, `SCORECARD.md`, every frozen artifact
(`c44_count_v5.py`, `c44_audit.py`, `controls-27.tsv`, `controls-r43/*`, `c44_placebo.py`,
round-43 receipts), `MANIFEST.json`, templates, fleet scripts, route tables, `mcp.json`,
`.ufo/state/`. No git/jj commit, push, publish or deploy; no tool install (host `python3`
and `git` were already present — no pacman transaction, per the host-wide pause).

## Out of scope

* The actual append to the ledgers — the L1 (`kake-r44`) is the sole writer of lane history.
* Any cause claim for the superseded prose numbers. The draft asserts only supersession by the
  receipt-derived values, except where a cited artifact grounds a cause. Note the grounding:
  `corpus/lessons/round-43-verifier-spotcheck.md:197-201` establishes the 14-receipt tally and
  that no other committed set carries the remaining four; `:209-212` establishes the LOG ratios
  as superseded by the committed receipts; `.ufo/waves/round-43/w1/CriticC1Sizing.md:17` traces
  the SCORECARD freeze-section numbers 4.272 / 8.679 / 1.002–1.020 to discarded pre-T2-fix
  receipts and does **not** cover the LOG's T5 1.13–1.18 range.
* §8.4 (denominator moves with revision) and §8.7 (SOURCES anchor locators), which the working
  copy's round-44 entry disposition elsewhere.

## Findings

1. The three C2 figures re-derive cleanly from the committed receipts: **14** distinct
   `toolSha256` over 14 committed re-score receipts, do-nothing **4.207 / 7.047** (quoted
   4.21 / 7.05), and build extrema **1.004–1.009 / 1.105–1.215** (quoted 1.00–1.01 /
   1.11–1.22). The C2 contract is satisfiable by appending three paragraphs.
2. Checker-shape traps the draft avoids, each of which silently breaks the check:
   the superseded "18" must not be preceded by the word "re-scored" (it would become the last
   match and turn 14 into 18); the do-nothing figure needs `(` immediately after `not met`;
   the superseded build range must not use a comma between its T1 and T5 halves (the pattern
   requires one); the build range must not end a sentence (the greedy `[\d.]+` captures the
   period and the checker raises `InputError`).
3. The draft's neutral supersession wording avoids the provenance defect that
   `kake-r44.CriticC2Repair` reported in the prose already present in the working-copy
   `LOG.md`/`SCORECARD.md` (authored by another seat): those lines attribute the old "18" to
   seat reports and the old ratios to pre-freeze timings / settle-prose rounding, which the
   cited artifacts do not establish for all three figures. My draft makes no such attribution.
4. The lane's current working-copy ledgers already carry a C2 repair appended by another seat
   and the checker already exits 0 on them (`3 figures, 0 mismatches`). My contribution is the
   independently derived, provenance-disciplined append-ready text; it is not yet in the
   ledgers.

## Blockers

None.

## Artifact paths

* `/fast/scratch/hyaku/kake-r44/c2-repairs.md`
* `/fast/scratch/hyaku/kake-r44/ScribeC2Repairs/verify_c2.py`
* `/fast/scratch/hyaku/kake-r44/ScribeC2Repairs/verify_c2.out`
* `/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-44/w2/ScribeC2Repairs.md`

Report: `.ufo/waves/round-44/w2/ScribeC2Repairs.md`
