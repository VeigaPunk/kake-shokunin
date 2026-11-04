# ExecKillers — round 83 wave w1

## Axes

1. **Kill coverage** — one fixture per named survivor, each fixture tied to the exact conjunct the
   mutant moves.
2. **Fixture provenance** — every fixture is built by the counter's *own* green builder
   (`build_green_tree` / `build_green`), not by a hand-copied tree; a fixture that drifted from the
   counter's paths would be testing my copy, not the code.
3. **Harness independence** — pristine and mutant are two separate imports staged from scratch
   copies; the lane root comes from `__file__`, never cwd, so path resolution cannot move with the
   mutant (the round-82 probe's captured defect).
4. **Failure visibility** — a non-unique anchor, a moved counter hash, or a fixture that fails to
   separate the copies must all exit non-zero; the suite was shown red.
5. **Cost** — one process, offline, 0.85 s and 23.7 MB RSS, scratch removed on exit.

## Delivered

| Path | Lines | sha256 |
|---|---|---|
| `.ufo/waves/round-83/killers/run_killers.py` (new) | 459 | `34bfa674713cd5929426c1b6f0d36d1c81ed6195bdcac14b612a7b674d574c46` |
| `.ufo/waves/round-83/killers/population.json` (new) | 127 | `da024fad465ad0856db7868d4a6dce60e19796bb12614d6529b874d995306131` |

Receipts: `.ufo/waves/round-83/w1/ExecKillers/` (`check.txt`, `time.txt`, `rows.txt`,
`control.txt`, `control/`, `neg-anchor.txt`, `export-shape.txt`, and `<mutant>.pristine.txt` /
`<mutant>.mutant.txt` for all five).

Fixtures are not static trees: each is rebuilt per run from the named builder plus one literal
mutation, so the fixture cannot rot away from the counter. The recipes are recorded per mutant in
`population.json.fixture_build`.

## Population and the exact patch bytes

Frozen sources (read only, hashes checked before any run): `c82_defect_queue.py`
`1082c691…e226`, `c82_capture_delta.py` `b93693df…4173`.

| Mutant | Counter site | Patch (old → new) | Fixture | pristine → mutant |
|---|---|---|---|---|
| C1-m3 | `c82_defect_queue.py:193` | `derived = numbers[0]` → `derived = 3801` | `c1-seat-bytes-4417` | `open=0` → `open=1` |
| C1-m5 | `c82_defect_queue.py:232` | `… "met=true" in receipt and log is not None` → `… and log is not None` | `c1-gate-receipt-met-false` | `open=1` → `open=0` |
| C2-m2 | `c82_capture_delta.py:249` | `b_instants[surface] > a_instants[surface]` → `>=` | `c2-equal-instants` | `met=false` → `met=true` |
| C2-m4 | `c82_capture_delta.py:265` | `flags["selftest_ok"] = int(selftest_ok)` → `= 1` | `c2-broken-tool-selftest` | `met=false` → `met=true` |
| C2-m5 | `c82_capture_delta.py:269` | `and flags["surfaces_a"] == 3 and flags["surfaces_b"] == 3` → `and flags["surfaces_b"] == 3` | `c2-dropped-a-surface` | `met=false` → `met=false` (**equivalent**) |

Each patch is one literal replacement, asserted to be unique in the copy at run time; the exact
bytes are stored as JSON strings in `population.json` so the applied bytes and the recorded bytes
are the same object.

## `--check` output (verbatim, `check.txt`, rc 0)

```
C1-m3 killed fixture=c1-seat-bytes-4417 counter=.ufo/waves/round-82/c82_defect_queue.py:193 pristine=open=0 mutant=open=1 patch=[derived = numbers[0]]->[derived = 3801]
C1-m5 killed fixture=c1-gate-receipt-met-false counter=.ufo/waves/round-82/c82_defect_queue.py:232 pristine=open=1 mutant=open=0 patch=[ok = "undisclosed=0" in receipt and "met=true" in receipt and log is not None]->[ok = "undisclosed=0" in receipt and log is not None]
C2-m2 killed fixture=c2-equal-instants counter=.ufo/waves/round-82/c82_capture_delta.py:249 pristine=met=false mutant=met=true patch=[surface in a_instants and b_instants[surface] > a_instants[surface]]->[surface in a_instants and b_instants[surface] >= a_instants[surface]]
C2-m4 killed fixture=c2-broken-tool-selftest counter=.ufo/waves/round-82/c82_capture_delta.py:265 pristine=met=false mutant=met=true patch=[flags["selftest_ok"] = int(selftest_ok)]->[flags["selftest_ok"] = 1]
C2-m5 equivalent fixture=c2-dropped-a-surface counter=.ufo/waves/round-82/c82_capture_delta.py:269 pristine=met=false mutant=met=false guard=.ufo/waves/round-82/c82_capture_delta.py:239:flags["receipts_ok"] = int(a_ok and b_ok and flags["surfaces_a"] == flags["declared"]; .ufo/waves/round-82/c82_capture_delta.py:268:met = (flags["declared"] == 3 proof=receipts_ok is a conjunct of met and re-derives surfaces_a == declared, while declared == 3 is itself a conjunct of met, so every state in which the mutant reads met=true already has surfaces_a == 3: the dropped clause is implied and no fixture can move the predicate
distinguished=5/5
```

## What each fixture actually does

- **C1-m3** (`c1-seat-bytes-4417`, prescribed "seat record with a different byte count"): the green
  record's mutation-tester `output_bytes` and the lesson's D4 number are both moved 3801 → 4417.
  Pristine prints `D4 closed derived output_bytes=4417`; the constant mutant prints
  `D4 open no D4 line carrying 3801 and superseded`, `open=1`. The kill exists only because the
  fixture's number is not 3801 — exactly the sensitivity the round-82 note described.
- **C1-m5** (`c1-gate-receipt-met-false`, prescribed "`undisclosed=0 met=false` receipt"): the
  ledger receipt keeps `undisclosed=0 … ` and ends `met=false`. Pristine prints
  `D7 open receipt green=no log=yes`; the mutant drops the `met=true` conjunct and prints
  `D7 closed receipt green=no`, `open=0`.
- **C2-m2** (`c2-equal-instants`, prescribed "equal instants"): capture A's three `fetchedAt`
  values are rewritten to capture B's `2026-11-04T12:50:00Z` and the record is regenerated; the
  tool's stdout does not print instants, so only strictness separates the pair. Pristine flags:
  `manifest_ok=1 receipts_ok=1 order_ok=0 floor_ok=1 determinism=1 record_equal=1 selftest_ok=1
  met=false`; mutant: `order_ok=1 … met=true`.
- **C2-m4** (`c2-broken-tool-selftest`, prescribed "green tree with a broken tool"): after
  `build_green` writes the record with the real tool, the fixture's
  `scripts/capture_delta.py` has `if args.selftest: return selftest()` replaced by `return 1`; the
  runner first asserts the `--a/--b` path still reproduces the committed record byte-for-byte.
  Pristine: `selftest_ok=0 … met=false` (`# selftest rc=1`); mutant: `selftest_ok=1 … met=true`.
  This is the fixture the round-82 selftest lacked.
- **C2-m5** (`c2-dropped-a-surface`, prescribed "dropped A surface"): `ds4cc-sitemap` is removed
  from capture A's manifest and directory and the record is regenerated. Both copies print
  `declared=3 surfaces_a=2 surfaces_b=3 manifest_ok=0 receipts_ok=0 order_ok=0 floor_ok=1
  determinism=1 record_equal=1 selftest_ok=1 met=false` — identical, hence `equivalent`.

## C2-m5 — why this mutant is equivalent, with the guards

`met` is `declared == 3 ∧ surfaces_a == 3 ∧ surfaces_b == 3 ∧ receipts_ok ∧ manifest_ok ∧
order_ok ∧ floor_ok ∧ determinism ∧ record_equal ∧ selftest_ok`, and
`receipts_ok = int(a_ok ∧ b_ok ∧ flags["surfaces_a"] == flags["declared"] ∧
flags["surfaces_b"] == flags["declared"])` (`c82_capture_delta.py:239-240`). Any tree on which the
mutant reads `met=true` therefore has `receipts_ok=1`, hence `surfaces_a == declared`, and
`declared == 3` (`:268`) gives `surfaces_a == 3`; the removed conjunct is already implied, so
`met_pristine ≡ met_mutant` on **every** input. The runner prints both conjunct sites
(`:239`, `:268`) and asserts both substrings survive in the mutant copy, so the equivalence is
mechanically anchored rather than asserted. The A-surface set is in fact re-derived four times —
`met:269` (removed), `receipts_ok:239`, `manifest_ok:245` (`a_pairs == declared`), and
`order_ok:249` (`surface in a_instants`) — so the named fixture is genuinely defeated on the
pristine counter, but for reasons the one-site mutation cannot reveal.

## Controls (the suite is shown able to fail)

- `--control` (pristine vs pristine, no patch staged): `control=5/5 unchanged`, rc 0
  (`control.txt`). A harness that read `killed` here would be reading its own state.
- Tampered anchor in a scratch copy of the lane (`derived = numbers[9]`): rc 1,
  `C1-m3 missed … reason=Fault: C1-m3: patch anchor occurs 0 times`, `distinguished=4/5`
  (`neg-anchor.txt`). A `missed` row cannot hide behind the other four.
- Export-shaped lane (`.ufo/waves/round-82/` + `scripts/` + killers, **no `.git`**, cwd `/`): rc 0,
  `distinguished=5/5` (`export-shape.txt`). This is the shape the D5 checker measures at a revision.
- `--check` from cwd `/` on the real lane: rc 0, `distinguished=5/5`; default scratch
  `…/run-vld7brfa` created and removed (`ls` before == after).

## Commands and exit codes

| Command | Exit |
|---|---|
| `python3 -B .ufo/waves/round-83/killers/run_killers.py --check --journal …/ExecKillers` | 0, `distinguished=5/5` |
| `python3 -B … --check` under `/usr/bin/time -f 'elapsed_s=%e maxrss_kb=%M'` | 0, `elapsed_s=0.85 maxrss_kb=23680` |
| `python3 -B … --control --journal …/ExecKillers/control` | 0, `control=5/5 unchanged` |
| tampered-anchor lane copy `--check` | 1, `distinguished=4/5` |
| export-shaped lane `--check` | 0, `distinguished=5/5` |
| `python3 -B … --list` | 0 |
| `sha256sum .ufo/waves/round-82/c82_defect_queue.py .ufo/waves/round-82/c82_capture_delta.py` | unchanged (`1082c691…`, `b93693df…`) |
| `git status --porcelain .ufo/waves/round-82 \| wc -l` | 0 |
| `grep -nE "import (socket\|urllib\|requests\|http)\|http\.client" run_killers.py \| wc -l` | 0 (offline) |

D5 checker rule simulated locally over `check.txt` (`row_count=5`, `rows_ok=True`,
`distinguished=5/5` present) — the same `any(name in line and ("killed" in line or "equivalent" in
line))` rule `c83_defect_queue.py:233` applies.

## Findings and risks

1. **C2-m5 is an equivalent mutant, and the round-82 diagnosis was incomplete.** The note says m5
   survived "because no fixture has a dropped capture-A surface"; the named fixture now exists and
   still does not distinguish, because the A-surface count is re-derived at `receipts_ok`,
   `manifest_ok` and `order_ok`. Reporting `equivalent` (with guards printed) is the measured truth;
   manufacturing a kill by widening the mutant would be a different mutant.
2. **The mutants are faithful reconstructions, not recovered bytes.** Round 82 left only the prose
   table (its mutants lived in scratch). `population.json` records the minimal literal realization
   of each described change and hashes the pristine counter so a later drift is refused (rc 2).
3. **The probe's own defect is designed out**: no `Path(__file__).parents[3]` tool resolution, no
   cwd dependence, no shared work dir between the two arms; each arm gets its own `run1/run2/selftest`
   directories.
4. **Not mine, but gating D5**: the `D5` lesson line in `corpus/lessons/round-83.md` (carrying
   `distinguished=5/5` and the five names) is a scribe item; without it the D5 row stays open even
   though this suite is green.
5. **Seat protocol**: no labrat probe was needed (allowance unused), no tool installed or upgraded
   (python 3.14.8 and git 2.56.0 were present), no network call, no VCS mutation (read-only
   `git status`/`ls-tree` only), scratch `/fast/scratch/hyaku/kake-r83/ExecKillers/` deleted before
   yielding.

## Verdict

**PASS for the assigned artifact.** `run_killers.py --check` prints five rows and
`distinguished=5/5`, exit 0, in 0.85 s: four survivors killed by their named fixtures
(`C1-m3`, `C1-m5`, `C2-m2`, `C2-m4`) and `C2-m5` reported `equivalent` with both guarding source
lines and a proof that the removed conjunct is implied. The harness was shown red under a tampered
anchor (rc 1, 4/5), unchanged under pristine-vs-pristine (5/5) and green from an export-shaped
lane with no `.git` and cwd `/`.
