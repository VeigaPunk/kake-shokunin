# CriticAxisWave2

Seat: critic (final admission attack on the three claims as a whole), round 57 W2. Read-only except this file: every run below is over
committed bytes of `/home/vgpnk/Projects/shokunin/kake-shokunin` at the build revision **`4b8c73050470ada9e6583f3b12d659d1bed6a17f`**
(the revision is named, never the working tree); scratch fixtures live in `mktemp -d` clones committed with `-c user.name=selftest`;
the lane repo, index and jj state were not touched. First verified that nothing I cite moved: `git diff --stat 4b8c730… HEAD --
.ufo/waves/round-57/'*.py' scripts/id_resolver.py corpus/` prints nothing (only the untracked W2 reports and `make_spec_w2.py` differ).
Read: `contract.md` (incl. § Counter versions), `w1/CriticAxisClaim.md`, `w1/CriticControlsSizing.md`, `AXES.md`, `SCORECARD.md`
rounds 52–56, the three counters at that revision, `w1/CritCheatC{1,2,3}.md`.

State at the build revision — C2 and C3 already meet, C1 cannot (no `measured.json`, no `## Round 57` section, no `after-*` receipt):

```
python3 -B .ufo/waves/round-57/c57_receipt_pins.py --root . --revision 4b8c730…   -> undisclosed=0 new_receipts=0 scorecard_pin=0 met=False, exit 1, 0.14 s
python3 -B .ufo/waves/round-57/c57_idresolver_gate.py --root . --revision 4b8c730… -> 5/5 met=True, exit 0, 1.6 s (G5 ids_cited=106)
python3 -B .ufo/waves/round-57/c57_quote_truth.py --root . --revision 4b8c730…     -> 8/8 met=True, exit 0, 0.07 s (offline)
```

## SEPARABILITY:

**S1 — C1 is entangled with C2/C3 in both directions (blocking).** `contract.md:33` requires `new_receipts == 3`;
`c57_receipt_pins.py:77-80` hard-codes the *other two claims'* report lines as `BODY_FIRST`, and `:249-251` allows one `after-*`
file per claim number.
(a) *C1 cannot pass if C2 or C3 fails honestly*: a failing claim's receipt is `met=False`, so `new_receipts < 3`; at the build
revision `new_receipts=0` (measured above). AXES.md: "each verifiable without the others having landed".
(b) *C1 passes regardless of their truth*: in a scratch clone of `4b8c730…` I deleted `scripts/id_resolver.py` and both entries and
committed three text receipts plus a `Measured revision:` line; the same C1 command then printed
`… new_receipts=3 scorecard_pin=1 met=True`, **exit 0**, while at that same tip C2 printed `0/5 met=False` (G1 tool absent) and C3
printed `5/8 met=False` (C1/C2/C7 fail). Confirmed by running.
So the coupling is documentary (files exist), not evidential: the claim is "separable" only as vacuity, and unadmitted whenever the
other two fail honestly. The wave-1 reading (`CriticControlsSizing` §6: "separability bought with vacuity, not with independent
evidence") is unchanged by version 2.

**S2 — C2 and C3 are separable from each other (confirmed by reading and by the runs).** C2 reads the tool, the lane registry and
`corpus/knowledge/**` at the revision (`c57_idresolver_gate.py:283-330`); C3 reads entries, registry, `sources/`, mirror and the
round-57 validate receipt; neither reads the other's output. C1's only cross-read is the two receipt *filenames* (S1).

## AFTER-STATE VALUES:

**C1 — one line, re-derivable, but not a run and not stable.**
The value is the seven-field report line (`report_first_line`, `:306`), and it does re-derive with one command over committed bytes
(0.14 s, git reads only). Three defects:
- *False provenance*: `after-c1` must start with `measure(T0, check_bodies=False)` (`:277`), but **no shipped command prints that line**:
  at T0 the CLI prints `new_unpinned=3 new_receipts=0 scorecard_pin=1 met=False` (measured; `--help` shows no bodies-off flag). The
  contract calls this "a *run at T0*" (`contract.md:129`); it is a hand-composed or module-imported line.
- *The value embeds the other claims' receipts* (S1).
- *A legitimate re-run destroys it*: `contract.md:9` and `:155` say "a re-run lands under a new file name", but `:249-251` treats a
  second `after-c2-*` as unpinned. Measured: adding one honest `after-c2-c57-rerun.txt` gives `new_unpinned=2 new_receipts=2 met=False`,
  and it also breaks `after-c1`'s T0 because `by_num[...][0]` takes the alphabetically first path (`after-c2-c57-rerun.txt` <
  `after-c2-c57.txt`, `:273`), which does not exist at T0. Any later C2/C3 re-measure therefore makes C1 unmeetable at every later tip.

**C2 — 5/5 today, not a function of committed lane bytes.** G4 compares live sibling ownership of the five ids with
`sibling-snapshot.json` (gate `:319-326`); the snapshot's `observedHeads` field is never read — only `owners` (`:324`) [INFERENCE,
code reading]. Confirmed by running: with the real fleet the gate is `5/5`; with a fleet copy in which one other lane appends an
`S367` row (the ids are shared across lanes — contract's collision list), the *same* command over the *same* lane bytes returns
`exit 2 … live sibling ownership {'S367': ['kama-shokunin','kotodama-shokunin'], …} differs from the committed snapshot`. The closure's
one-command re-derivation can therefore become *unevaluable* with no lane change. A scratch clone also needs `--fleet <fleet root>`
(the default is the parent of `--root`).

**C3 — one concrete value, revision-scoped.** 8/8 over committed bytes, no network; retained bodies are pinned by sha256 in the
counter (`c57_quote_truth.py:94`) and I re-verified them against `sources/receipts.json` (34750/27327 bytes, both sha256 lines match).
But C8 pins the round-57 mirror, so the counter goes red at the next tip — the pre-existing design of rounds 55/56, measured:
`c55_quote_truth` at `4b8c730…` = 6/8 and at the r57 base `28fa0b2` = 6/8; `c56_quote_truth` at `4b8c730…` = 6/8 and at `28fa0b2`
= 8/8. So the re-derivation must name the measured revision (`measured.json`), not the tip; that wording must be in the report.

## CONTROL REACHABILITY:

**C1 — reachable (measured).** Recipe: `measured.json` + three two-line receipts (`revision: <measured>`) + the already-committed
`receipt-errata.json` + one `Measured revision:` line, two commits, with the C2 tool and both C3 entries deleted. Result
`met=True`, exit 0. Wave-1 baseline (`CriticControlsSizing`: "C1's target IS reachable"; `CritCheatC1` verdict): same class; version 2
added a body *shape*, not a run, so the class survives with a modestly higher forging cost. No shipped command is needed to compose
the `after-c1` line (see AFTER-STATE).

**C2 — reachable (measured) by a 24-line shim.** The shim imports `reference()` from `.ufo/waves/round-57/c57_idresolver_gate.py`
(relative to `scripts/id_resolver.py` in the throwaway clone), prints its lines and summary, and answers `--selftest` with the
constant `selftest: 33/33` (G2 is documented as a smoke test). Gate result on the shim: **5/5 met=True, exit 0** (G3 both fixtures,
G4 red set, G5 green). Version 2 closed the v1 constant printer (`CritCheatC2`: 10 lines, 5/5) with randomised fixtures but not the
judge-import class. The shim then dies with `FileNotFoundError` once the counter leaves the tree (SKILL withdrawal rule), so the
"capability" would depend on the round's wave file.
Smallest safe correction: run G2–G5 in the throwaway clone **with `.ufo/waves/round-57/` removed**, plus one negative fixture asserting
the shim fails; an honest tool does not read the wave directory.

**C3 — not reachable cheaply.** v1 was 8/8 from 13 junk files (`CritCheatC3`); v2 pins the bodies by sha, admits spans only in text
nodes of the article block (`:373-402`), and requires the page title, a 4+-unit unique anchor and the printed date. Measured data
point: with both entries deleted the counter still returns **5/8** (C3_row_shape, C4_used_by, C5_quote_truth, C6_receipt_pins,
C8_mirror_bytes pass vacuously), so a 5/8 score is not progress; 8/8 needs real entry text quoting the retained bodies.
[Class-level judgment: no do-nothing route found; the measured 5/8 bounds the vacuity.]

## HARM CHECKS:

| axis | command (over `4b8c730…`) | expected | observed |
|---|---|---|---|
| calibration | the S1 scratch repro (three receipts at every tip with C2/C3 deleted) | `met=False` if separable | **`met=True`** — a certifying pin counter over a round that landed nothing |
| calibration | `c57_receipt_pins.py --root . --revision 4b8c730…` | `met=False` before the after-state | `met=False` (exit 1) — harm is latent until the after-state, not present today |
| calibration | `c54_s374_calib.py --root . --revision 4b8c730…` | `met=True` (no regress) | `met=True`, `mismatches=0` |
| calibration | `c56_selftally.py --root . --revision 4b8c730…` | 10/10 rows green (no regress) | `tally_mismatches=0 rows_checked=10 met=True`, 27 s |
| operability | the 24-line shim + `c57_idresolver_gate.py --root <clone> --revision <tip> --fleet <real>` | gate rejects a tool that imports the judge | **5/5 met=True** |
| operability | delete `.ufo/waves/round-57/` from a clone, then `python3 -B scripts/id_resolver.py --root .` (shim) | tool still runs | `FileNotFoundError` (exit 1) |
| operability | `c54_ops_debt.py --root . --revision 4b8c730…` | `met=True` | `registry=present manifest=present uncovered=0`, exit 0 |
| freshness | `c55_readme_index.py --root . --revision 4b8c730…` | `met=True` (54 files indexed) | `index_mismatches=0 knowledge_files=54 met=True` |
| freshness | `c56_quote_truth.py` / `c55_quote_truth.py` at the tip | C1–C6 green, C7/C8 red (mirror pins) | 6/8 both; C7/C8 only; `c55` was already 6/8 at the r57 base → pre-existing, not round-57 corpus harm |
| freshness | `grep -c S42 corpus/knowledge/freshness-pins.json` | 0 if the 180 d cadence is stated only | `0` — the cadence lives in the entries' `recheck:` lines, nothing schedules it |
| freshness | sha256 of `sources/S421.html`, `S422.html` vs `sources/receipts.json` | match | match (34750 / 27327 bytes); W2 re-fetches (`w2/ExecReopenS421.md`, `ExecReopenS422.md`) found the article blocks byte-identical |

Which claim moves which axis: C1 → **calibration** (pin disclosure; the score stays 1/10 — the surface is evidence hygiene, not accuracy);
C2 → **operability** (capability acquisition: tool + row; 10/10 stays); C3 → declaratively **freshness**, actually **expansion/coverage**
(two rows opened this round; the freshness content is sourced-today only; 10/10 stays).

## AXIS NOTE:

Sentences for the round report, usable only after S1 and the two after-state corrections below are made pre-data (the `new_receipts == 3`
term narrowed to C1's own receipt; a documented bodies-off T0 mode; a re-run allowed; the tool clone without the wave directory; G4's
owner column pinned from the snapshot). Otherwise the round's calibration line would certify a round that has landed nothing.

- "C1 is declared on **calibration** (the round-54 bounded sub-axis, score 1; ownership vs operability remains open for the operator): the surface
  is the lane's measurement self-assessment — `receipt-errata.json` (six historical relabels, each checked against git), the three round-57
  receipts and the SCORECARD `Measured revision:` line — and the counter counts disclosed/phantom relabels, deleted receipts, round-57 relabels and
  unpinned receipts over the whole committed ancestry of the tip; it certifies pin consistency with history, not that a counter ran at the pinned
  revision, and its one concrete value is the single `met=True` report line re-derived over committed bytes. Score stays 1/10."
- "C2 is declared on **operability (capability acquisition)**: `scripts/id_resolver.py` plus its SCORECARD capability row; the gate demonstrates
  the tool running (33-check selftest in a clean clone) and its output verifying (differential against the gate's own reference over randomised
  fixtures; red-before at `3994101` = exactly S367 S372 S373 S390 S409 owned by kotodama-shokunin; green at the measured revision,
  `ids_cited=106`); the five ids are shared across lanes, so ownership is compared with a committed snapshot and drift is *unevaluable*, not
  *not met*. Score stays 10/10."
- "C3 is declared on **freshness (sourced)**: the two Baidu dead-link entries open new rows this round (S421, S422), so the primary surface per
  AXES is expansion/coverage; the freshness content is bounded to sourcing — retained bodies fetched 2026-10-25 UTC with HTTP 200 receipts and
  sha256 pins frozen in the counter, and same-day live re-fetches in the wave-2 executor reports show the article blocks byte-identical (only
  header/footer script cache-busters differ, so the retained sha256 is not live-reproducible while the quoted spans are); no held lane claim is
  re-verified, the counter has no drift condition, and `conditions_passed == 8 of 8` re-derives only at the measured revision because C8 pins the
  round-57 mirror (the same revision-scoped design as rounds 55–56). The entries' `recheck: 180d` lines are stated, not scheduled by
  `freshness-pins.json`. Score stays 10/10."
- "Disclosed limits stand: C1's errata population is the rounds 52–57 `control(s)/` receipts carrying a 40-hex pin; C1 does not prove a counter
  ran at the pinned revision; C2's G4 owner column is the committed snapshot (live drift reported as a warning); C3's quote check is substring truth
  in article text nodes, not support or rendering fidelity; the append is validated on a scratch mirror (C7 receipt), not re-proved by a re-run."

VERDICT: C2 and C3 are admission-ready at `4b8c730…` (5/5 and 8/8 measured, no earlier counter regressed) but C1 is not: its `new_receipts == 3`
term makes it unmeetable unless C2/C3 land yet satisfiable with their work deleted (both measured), its receipt line is printed by no shipped
command, and one honest C2/C3 re-run makes it permanently unmeetable — fix the predicate/pin-mode/run-name rule, hide the wave directory from the
C2 tool clone, and pin G4's owner column to the snapshot before any claim scores.
