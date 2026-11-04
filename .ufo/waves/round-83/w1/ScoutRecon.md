# ScoutRecon — round 83 wave w1

Read-only recon of the C1 queue. Every command below was run by this seat against
`/home/vgpnk/Projects/shokunin/kake-shokunin` and, read-only, against the fleet repo
`/home/vgpnk/Projects/shokunin`. I wrote no production file; receipts are under
`.ufo/waves/round-83/w1/ScoutRecon/`. Scratch (`/fast/scratch/hyaku/kake-r83/ScoutRecon/`)
held the exported trees, the junk tree and the mutant experiments, and is deleted.

Base is `826b0061f233ce1dffb9bd6874abc1342a864247`; the lane HEAD is the freeze commit
`64b7199281e5457df0e08652977f698c4f34f46e`, its only child (`git log --oneline 826b0061..HEAD`
prints one line, exit 0). At base `git ls-tree -r --name-only 826b0061 | grep
'^\.ufo/waves/round-83'` prints nothing (exit 1): **the whole round-83 wave directory is
post-freeze**, so every item is red at base by absence, and the only meaningful base statement is
the base control.

## 1. The six routed defects, as the outside verifier filed them

1. **D1 — attack floor.** Measured: all four requested attack seats (`ReviewC1`, `ReviewC2`,
   `CriticClaims`, `MutC`) returned empty; settled attack share `0/7 = 0.0 %` against the run-15
   ≥ 25 % floor, while the requested shape was 4/13 = 30.8 %. Asked for: settle adversarial seats
   and record settlement, not relabel.
2. **D2 — units.** Measured: the report's §Wave accounting prints character counts `(4,871 B)`,
   `(7,888 B)`, `(6,392 B)`, `(6,664 B)`, `(3,811 B)` where `make_accounting.py`'s
   `len(output.encode("utf-8"))` records bytes `4,899`, `7,902`, `6,402`, `6,669`, `3,813`. Asked
   for: cite the JSON's numbers or label them characters.
3. **D3 — instrument receipt.** Measured: the report asserts the standing gate was red at base and
   that `--check` at `576cf76c` exits 0, with no receipt path. Asked for: commit the `--check`
   receipt or cite the re-derivation.
4. **D4 — erratum content.** Measured: `corpus/lessons/round-82.md` D3 names the four rewritten
   statements by *kind* but does not quote the superseded strings. Asked for: append the superseded
   text verbatim.
5. **D5 — mutation survivors.** Measured: C1 3/5 killed (`m3`, `m5` survive); C2 1 killed, 1
   equivalent, 3 survived (`m2`, `m4`, `m5`). Asked for: the routed killer fixtures for the five.
6. **D6 — gate-summary provenance.** Measured: the round-82 report's Sources & frontier lists "the
   `merge/kake` package" among the Gate's *rejects*; the lesson's §Gate rejects are two S455 anchor
   spans and the package is an assimilation non-adoption. Asked for: cite the lesson section.

## 2. Frozen state conjuncts and the byte that closes each

Read from `.ufo/waves/round-83/c83_defect_queue.py` (484 lines) and contract §C1. Each item also
carries a lesson row conjunct read by `line_with()`, which is tag-regex plus **case-sensitive**
substring AND over one physical line.

| Item | State conjunct (counter lines) | Closing byte |
|---|---|---|
| D1 | `derive_population`: `settled_attack >= 2`, `settled_share >= 0.25`, and `w1-accounting.json` `settled`/`settled_names`/`settled_attack`/`settled_share` `==` the derivation | `w1-results.json` with ≥2 attack-role rows non-empty and `settled <= 4*settled_attack`, plus the matching accounting record and a lesson line carrying `0/7` **and** `settled_attack=` |
| D2 | `record["bytes_basis"] == "utf-8"`; every derived seat with `output_bytes > 0` has an equal recorded `output_bytes` | the accounting's `bytes_basis` key and per-seat UTF-8 lengths; lesson line carrying `UTF-8` and `w1-accounting.json` |
| D3 | `controls/after-c83-instrument-check.txt` has a line starting `C2v1 ` with a 40-hex, and fields `bound == population`, `mismatches=0`, `met=true` | a truthful transcript of `scripts/instrument_receipts.py --check`; lesson line carrying the path and `--check` |
| D4 | ≥4 lines that `git -C <fleet> diff commits[1] commits[0] -- .ufo/reports/round-81/kake.md` removed (`len(line) > 41`) appear as raw substrings in `corpus/lessons/round-83.md` | ≥4 verbatim quote lines plus a D4 lesson line carrying `7678247a` and lowercase `erratum` |
| D5 | `killers/run_killers.py` `--check` exits 0, prints `distinguished=5/5`, and prints a row per frozen name containing `killed` or `equivalent` | the runner, its `population.json` and fixtures; lesson line carrying `distinguished=5/5` and all five names |
| D6 | a `corpus/QUALITY.md` line containing `corpus/lessons/round-82.md`, `Gate` and `round-83` | the appended criterion line; lesson line carrying `§Gate` and `corpus/QUALITY.md` |

## 3. Re-derivation at base, at freeze HEAD, and the controls

`c83_defect_queue.py --revision 826b0061 --work <scratch>/counter-base --fleet <fleet>` (exit 1)
prints all six open and `C1v1 revision=826b0061… items=6 open=6 closed=0 met=false`; it is
byte-identical to `controls/base-c83-defect-queue.txt` apart from that file's `base_c1_exit=1`
trailer. Re-run at freeze HEAD it prints the same six rows with `revision=64b71992…` (exit 1).

The reason each is red at HEAD is a *missing artifact*, not a failed measurement:
`w1-results.json` and `w1-accounting.json` absent, `after-c83-instrument-check.txt` absent,
`corpus/lessons/round-83.md` absent, `killers/run_killers.py` absent, and no qualifying QUALITY
line (I checked: zero existing `QUALITY.md` lines carry `round-83`, and `corpus/lessons/round-83.md`
is absent from the worktree).

Controls re-derived by this seat, all green as committed:
`--selftest` prints nine `ok` lines and `selftest: 9/9 passed`, exit 0
(`controls/c83-selftest-c1.txt`); `junk_tree_build.py` plus the counter prints
`D4 open removed=5 quoted=0 amendment=7678247a log=no` and `open=6 … met=false`, exit 1
(`controls/ctl-c83-junk-queue.txt`, reproduced byte-for-byte minus `junk_exit=1`). So prose cannot
close an item, and the counter's own fixtures separate.

## 4. Planning data-walk — artifact, owner, and landing order for one carrier

| Item | Artifact | Owner | Depends on |
|---|---|---|---|
| D1 | `w1-results.json` (14 rows; ≥2 attack rows non-empty; `settled <= 4*settled_attack`) | **L1** after WAVE-DONE | seats reporting |
| D1/D2 | `w1-accounting.json` (`bytes_basis:"utf-8"`, sorted `settled_names`, exact `round(share,4)`) | **ExecAccounting**'s tool, **run by the L1** — no seat brief says it writes the round-83 record | `w1-results.json` |
| D2 | lesson D2 row (`UTF-8`, `w1-accounting.json`) | ScribeLesson | accounting |
| D1 | lesson D1 row (`0/7`, `settled_attack=`) | ScribeLesson | accounting numbers |
| D3 | `controls/after-c83-instrument-check.txt` | ExecInstrument | last commit that can change the instrument population |
| D4 | `[r83-erratum]` quotes (≥4) + D4 row (`7678247a`, `erratum`) | ScribeLesson | none (fleet diff fixed) |
| D5 | `killers/run_killers.py`, `population.json`, fixtures + D5 row | ExecKillers, checked by MutKillers; row by ScribeLesson | none |
| D6 | `corpus/QUALITY.md` criterion line (`corpus/lessons/round-82.md`, `Gate`, `round-83`) + D6 row | ScribeRecord + ScribeLesson | none (D6 row not dependent on D1/D2) |

Order for a single carrier: (1) wave seats; (2) L1 writes `w1-results.json`; (3) L1 runs
`make_accounting_v2.py` → `w1-accounting.json`; (4) ScribeLesson finalizes D1/D2; (5) commit **R1**
with everything except the D3 transcript; (6) ExecInstrument runs
`instrument_receipts.py --check --revision R1`; (7) commit the transcript plus seat reports as
carrier **C**; (8) `c83_defect_queue.py --revision C` must print `open=0`. The two-commit shape is
forced only if something between R1 and C changes the instrument population; otherwise R1 can be
the freeze commit itself, because `--check` is **already green** at `64b71992`
(`population=30 bound=30 mismatches=0 met=true`, receipt committed, `declared=70c8241b`, valid,
`missing_frozen=0`).

## 5. Findings that change or constrain the plan

- **D5 cannot be five kills.** I reproduced every survivor by one-string patch on scratch copies and
  ran the counters' own `build_green_tree`/`build_green` fixtures. C1 `m3` (fixture:
  mutation-tester `output_bytes=4200`) and `m5` (`undisclosed=0 … met=false`) kill; C2 `m2` (both
  captures at `2026-11-04T12:50:00Z`, above the floor) and `m4` (green tree, tool `--selftest`
  exits 1) kill. **C2 `m5` does not: pristine and mutant both read `met=False` on the exact named
  "capture A drops one surface" fixture.** It is equivalent by construction: `met` needs
  `receipts_ok==1` (line 239 requires `surfaces_a == declared`) and `declared==3` (line 268), so
  `surfaces_a == 3` at line 269 is entailed and deleting it changes no fixture. `distinguished=5/5`
  is still attainable, but as 4 killed + 1 `equivalent` with lines 239/268-269 printed. A 5/5
  all-killed line would be a false receipt; ExecKillers' brief ("prefer a kill") is unsatisfiable
  for that row.
- **D3's counter does not re-run the instrument.** It only parses `bound`/`population`/
  `mismatches`/`met` from the transcript; it never re-executes `--check` or checks the revision's
  ancestry. The state conjunct is a format check, so the receipt's truth rests on ExecInstrument and
  on ReviewC1, not on the C1 counter.
- **D4's counter drops the contract's "absent from the amended blob" clause.** It only checks
  `line in lesson`. The five candidate lines are all in fact absent from the `7678247a` blob
  (`ScoutRecon/d4-quotes.txt`, `d4-fleet.diff`), so the contract sentence holds, but only because I
  checked it — the counter would accept a line that survived.
- **D4 quote bytes.** The five removable lines are 111/100/99/70/519 characters; the first contains
  `·` (U+00B7, 113 bytes/111 chars) and the last two `…` (U+2026). Any four must include at least
  one non-ASCII line. Leading indentation is part of the line: lines 2-4 begin with two spaces, so
  `>   5/14 …` must keep both spaces after `> `; normalising to one space breaks `line in lesson`.
- **D4 is cross-repo.** `item_d4` takes the newest two fleet commits touching
  `.ufo/reports/round-81/kake.md`. Today that is `7678247a`/`cb02b705`; any other lane committing
  that path during round 83 shifts the pair and breaks the quotes. Nothing this lane does can fix
  that after the fact.
- **Lesson token traps** (`line_with` is case-sensitive): D4 needs lowercase `erratum`;
  D1 needs `0/7` literally (the round-82 share) on the same line as `settled_attack=`;
  D6 needs `§Gate` exactly; D2 needs `UTF-8` exactly.
- **D1 is the only real scheduling risk.** With 14 seats and 5 attack seats, the floor forces
  `settled <= 4a` for `a` settled attack seats: 2 attack → ≤8 total, 3 → ≤12, 4 → ≤14. Recording
  all 14 rows with only 3 attack seats settled fails at 3/14 = 0.2143. Target 4 attack seats.
- **D3 ordering.** `--check` reads the receipt from committed bytes at `--revision`; a worktree-only
  receipt is `source=uncommitted` and a mismatch. So the transcript must name a committed revision,
  which is why the transcript cannot name the carrier it is committed in (hash cycle) — see the
  two-commit shape above.
- **No frozen item is impossible.** All six are satisfiable against bytes that exist or can be
  produced; the only unsatisfiable *sentence* is the "kill" verdict for C2 `m5` (the contract's
  `equivalent` branch is the honest route and the counter accepts it).

## Verdict

**Recon complete; the C1 queue is open exactly as the base control says, and every item is
satisfiable.** D1 is a settlement-planning constraint (≥2 attack seats, `settled <= 4*attack`; target
4/14); D2 is an accounting-record constraint with exact float equality; D3 needs a committed
transcript of a gate that is *already green* at `64b71992` (`30/30`, exit 0) and must be signed
against a committed revision, not the carrier; D4 has five verbatim quotes available, all genuinely
absent from the amended blob, with a UTF-8/indentation trap; D5 is attainable only as four kills
plus one provably equivalent mutant (C2 `m5`), which the contract permits; D6 is a single QUALITY
line plus a lesson row. No production file was edited by this seat; the lane worktree is unchanged
apart from my two report-side paths.
