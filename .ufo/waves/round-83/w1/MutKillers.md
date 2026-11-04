# MutKillers — round 83 wave w1

Independent verification of the D5 killer suite. I did not write, edit or run the suite's author
into the loop: I read the runner and `population.json` in full, ran the runner myself, inspected
every fixture it builds on disk, and re-derived two kills from my own copies of the frozen counters.

Bytes verified (hashes in `MutKillers/sha256s.txt`):

| Artifact | sha256 | Size / note |
|---|---|---|
| `.ufo/waves/round-83/killers/run_killers.py` | `34bfa674713cd5929426c1b6f0d36d1c81ed6195bdcac14b612a7b674d574c46` | 20158 B, mtime 10:36:05 |
| `.ufo/waves/round-83/killers/population.json` | `da024fad465ad0856db7868d4a6dce60e19796bb12614d6529b874d995306131` | 127 lines |
| `.ufo/waves/round-82/c82_defect_queue.py` (frozen) | `1082c691bc28fa35476613d8ce47a0cc2a5630d5390be31e67307ae173b2e226` | matches population |
| `.ufo/waves/round-82/c82_capture_delta.py` (frozen) | `b93693df932ac1982677e1b23de2aa3a352b84ca0120acc76db1e754f4974173` | matches population |
| `scripts/capture_delta.py` | `4b0dc25233542696988ef91b62872068cbc5d56f58d0ef3f988ac60e558d9680` | matches population |

## Commands and exits (all run by this seat)

| Command | Exit | Observed |
|---|---|---|
| `python3 -B .ufo/waves/round-83/killers/run_killers.py --check` | 0 | five rows, `distinguished=5/5` (`check.stdout`) |
| `python3 -B … --control` | 0 | `control=5/5 unchanged` (`control.stdout`) |
| `python3 -B … --check --work …/work-final --journal …/journal-final` | 0 | `distinguished=5/5`; journal has both arms' full text per mutant |
| `cd / && /usr/bin/time python3 -B <abs>/run_killers.py --check` | 0 | `distinguished=5/5`, `elapsed_s=0.86 maxrss_kb=24108` |
| `python3 -B .ufo/waves/round-83/c83_defect_queue.py --root <lane>` | 1 overall | `D5 closed rc=0 tail='distinguished=5/5' rows=yes log=yes`; D1/D2 open (absent w1-results/accounting — other seats, out of scope) |
| `sha256sum` frozen counters before and after my work | — | unchanged, and `git status --porcelain .ufo/waves/round-82` prints 0 lines |
| `diff` each staged mutant vs its staged pristine copy | 1 (differs) | exactly `changed-lines=2` (one removed, one added line) per mutant (`mutant-diffs.txt`) |

## Does each fixture genuinely separate the mutant from the pristine counter?

I read the five fixture trees from the final run's work directory (`fixture-inspection.txt`) and the
journal of both arms (`journal/<mutant>.{pristine,mutant}.txt`). Each fixture changes exactly the
inputs the mutated conjunct reads; in every `killed` row the *only* differing printed quantity is
the mutated item/flag, so no row is a harness artifact:

| Mutant | Mutated site | Fixture bytes I inspected | Pristine → mutant | Discriminating row |
|---|---|---|---|---|
| C1-m3 | `derived = numbers[0]` → `= 3801` | seat record `output_bytes` `4417`; lesson `D4 … output_bytes 4417` | `open=0` → `open=1` | mutant's only open row is `D4 no D4 line carrying 3801 and superseded`; the other seven items closed both arms |
| C1-m5 | D7 drops `and "met=true" in receipt` | ledger receipt `undisclosed=0 … met=false` | `open=1` → `open=0` | pristine's only open row is `D7 receipt green=no log=yes`; mutant closes it |
| C2-m2 | `>` → `>=` on instants | A and B all `2026-11-04T12:50:00Z` (equal); record regenerated, rc 0 | `met=false` → `met=true` | pristine flags differ only in `order_ok=0`; mutant `order_ok=1`, all other flags `1` |
| C2-m4 | `flags["selftest_ok"] = int(selftest_ok)` → `= 1` | tool `--selftest` returns 1; runner first asserts `--a/--b` still reproduces the record | `met=false` → `met=true` | pristine differs only in `selftest_ok=0` (`# selftest rc=1`); mutant `1` |
| C2-m5 | `met` drops `surfaces_a == 3` | A manifest has 2 checks and no `sitemap` dir; B has 3; record regenerated | `met=false` → `met=false` | both arms print identical flags (`manifest_ok=0 receipts_ok=0 order_ok=0`) — hence `equivalent`, below |

Failure-mode audit: lane root comes from `__file__`, not cwd (the round-82 probe's captured defect;
I confirmed by running `--check` from `/`); pristine and mutant are separate imports of separate
staged copies; the frozen hashes and tool hash are checked before any fixture is built; each arm
gets its own `run1/run2/selftest`; a non-unique patch anchor raises `Fault` (ExecKillers'
`neg-anchor.txt` shows rc 1, 4/5 there; I did not repeat that run).

## Independent re-derivation (my own scratch, own driver)

- **C1-m3**: copied the frozen counter myself, applied the same `old`/`new` strings read from
  `population.json` (anchor count asserted 1), built my own green tree plus a two-commit fixture
  fleet (`git rev-parse --show-toplevel` asserted equal to the fixture dir), moved both sides of the
  number to 4417 and called `evaluate()` directly. Result: pristine `open=0`, mutant `open=1`, open
  row `D4`; my mutant's sha256 `d5ecf2f0…` equals the suite's staged mutant copy. Exit 0.
  (`rederive-c1m3.txt`, driver `rederive_c1m3.py`.)
- **C2-m2**: same procedure on `c82_capture_delta.py`; rewrote A's three `fetchedAt` to B's instant,
  regenerated the record with the real tool, called `measure()` directly. Result: pristine
  `order_ok=0 met=False`, mutant `order_ok=1 met=True`; mutant sha256 `8c6b1a60…` equals the suite's
  staged copy. Exit 0. (`rederive-c2m2.txt`, driver `rederive_c2m2.py`.)
- The frozen counters re-hashed after both runs: unchanged.

## `C2-m5` — the `equivalent` row and its proof

Guard lines printed by the runner (`guard-lines.txt`): `c82_capture_delta.py:239`
`flags["receipts_ok"] = int(a_ok and b_ok and flags["surfaces_a"] == flags["declared"]` and
`:268` `met = (flags["declared"] == 3`. Since `met` requires `receipts_ok == 1`, every state in
which the mutant reads `met=true` satisfies `surfaces_a == declared`, and `declared == 3` is another
conjunct, hence `surfaces_a == 3` — the removed clause is already implied and no fixture can move
the predicate. I machine-checked this over the counter's own expression: `186,624` consistent
assignments (`declared`, `surfaces_a`, `surfaces_b`, `a_ok`, `b_ok`, and the six free conjuncts),
`diverging=0` (`equiv-c2m5.txt`, driver `equiv_c2m5.py`). The round-82 note's diagnosis ("no
fixture has a dropped capture-A surface") was incomplete; the named fixture now exists and the
mutant is still equivalent, for the reason above. The `equivalent` verdict is earned; manufacturing
a kill would need a different mutant, not a different fixture.

## Findings

1. **`distinguished=5/5` is earned under the contract's definition** — four rows `killed`, one
   `equivalent` with both guarding source lines and a proof that survives exhaustive checking.
2. **Version drift, disclosed.** The runner appeared at 10:33 (18450 B), was rewritten at 10:34:51
   (19815 B, adding `--control`) and again at 10:36:05 (20158 B, adding co-guard validation). My
   verdict applies to `34bfa674…` / population `da024fad…`; the earlier runs' receipts are kept
   under `MutKillers/superseded/`. If either file moves again, my receipt no longer covers it.
3. **Formal conformance note, no effect on the verdict.** The seat item asked fixtures to call
   `evaluate()`/`measure()` directly; the runner calls `run()`, which calls those functions and
   prints. The measured quantities are exactly `evaluate`/`measure` outputs (I re-derived two kills
   by calling the functions directly and got the same predicates).
4. **D5's row dependency.** `D5` also needs the lesson line; at 10:38 the counter read `log=yes`,
   so the scribe line exists in the live tree. The counter's overall exit is 1 only because D1/D2
   are still open (missing `w1-results.json` / `w1-accounting.json`), which is C1 state, not D5.
5. **Cleanliness.** The runner's default scratch dirs are removed on exit (verified: no `run-*`
   under `/fast/scratch/hyaku/kake-r83/ExecKillers` after my runs, and that directory is now empty);
   with an explicit `--work` it keeps the tree by design. No VCS mutation, no network (no
   `socket`/`urllib`/`requests`/`http.client` import in the runner), and the lane's round-82 tree is
   untouched (`git status --porcelain .ufo/waves/round-82` → 0 lines).
6. **Scratch deleted.** `/fast/scratch/hyaku/kake-r83/MutKillers/` removed after copying the
   receipts below.

Receipts: `MutKillers/check.stdout`, `check.stderr`, `check-journaled.stdout`,
`control.stdout`, `cwd-root-check.stdout`, `journal/` (10 files), `fixture-inspection.txt`,
`mutant-diffs.txt`, `guard-lines.txt`, `list.txt`, `c83-integration.txt`, `sha256s.txt`,
`rederive-c1m3.txt`, `rederive-c2m2.txt`, `equiv-c2m5.txt`, the three drivers, `timing.txt`, and
`superseded/` (earlier-byte runs).

## Verdict

**EARNED.** On `run_killers.py` sha256 `34bfa674…` and `population.json` sha256 `da024fad…`,
`python3 -B … --check` exits 0 printing `distinguished=5/5`: `C1-m3`, `C1-m5`, `C2-m2`, `C2-m4`
killed on their named fixtures with no unrelated-failure path, and `C2-m5` correctly `equivalent`
(guards `:239`/`:268`, proof independently machine-checked). Two kills re-derived end-to-end in my
own scratch from my own counter copies. D5's counter row reads `closed rc=0 … rows=yes log=yes`.
