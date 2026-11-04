# CriticPredicates — round 75, wave w1 (kake)

Seat: critic (leaf; no subagents, no `ask`). Job: falsify §C1 and §C2. Measurements come from
committed bytes in independent `git clone --shared` trees, never the lane working tree. The lane was
read-only for this seat; this file and `w1/CriticPredicates/` are my only writes. Scratch
`/fast/scratch/hyaku/kake-r75/CriticPredicates{,2}` (clone at base, clone at the landed tip, fixtures as
further `--shared` clones, toplevel asserted before every first commit, commits with
`-c user.name/-c user.email`, no global config touched) was removed before yield. No tool installed.

Round state at measurement: base `c9c5e484`, and the L1 landed the after-state at
`4e3fc159919f1af8db139f0931ac096512747895` (`f1fc5d0a` = rows/tool/receipt, `4e3fc159` = receipt commit).
Both claims were re-derived **at the landed tip**, not only against fixtures.

Blobs measured (full list in `CriticPredicates/tool-digests.txt`):

| blob | sha256 | bytes |
|---|---|---|
| frozen counter `88f2e05:.ufo/waves/round-75/c75_row_truth.py` | `43538343c1f26e15…` | 10,405 |
| landed counter `4e3fc159:.ufo/waves/round-75/c75_row_truth.py` | `0699a672bc51311e…` | 47,446 |
| w1 counter copy `w1/ExecC1Counter/c75_row_truth.py` (≠ landed) | `63e321b28e509781…` | 47,446 |
| landed C2 tool `4e3fc159:scripts/instrument_receipts.py` | `162dd6852cd5f6ad…` | 48,868 |
| landed receipt `4e3fc159:corpus/knowledge/instrument-receipts.json` | `f3128628d928ae19…` | 3,793 / 18 entries |

## Axes and what moved

| Axis | Question | Verdict |
|---|---|---|
| A1 base red | is `mismatches=2` real from committed bytes? | **real; both findings; no harness artifact** |
| A2 do-nothing | base tree, nothing added | **cannot reach met=true** (C1 exit 1, C2 exit 1) |
| A3 fidelity | contract vs counter vs receipts | **8 divergences were open during the round; 4 closed at the landed blobs (D1, D2, D4, D7), 4 residuals open (D3, D5, D6, D8)** |
| A4 independence | C1 without C2, C2 without C1 | **independent, both states measured** |
| A5 target cost | is `2→0` too cheap? | **erasure reaches met=true at the same cost as correction; the landing did not use it** |
| A6 C2 attack | do-nothing receipt; cheapest path | **do-nothing cannot pass; 64 ms hash loop reaches bound; tip is 18 not 16** |

---

## 0. Landed tip — both claims re-derive met

From a clone at `4e3fc159` (receipts `landed-c1.txt`, `landed-c2.txt`):

```
C1v1 revision=4e3fc159919f1af8db139f0931ac096512747895 rows=32 live=20 files=18 mismatches=0
     classes=- append_only=true met=true missing_frozen=0                    exit 0
C2v1 revision=4e3fc159919f1af8db139f0931ac096512747895 population=18 bound=18 mismatches=0 met=true
     population: derived=18 frozen=16 missing_frozen=0 beyond_frozen=2
     receipt: source=committed worktree=identical declared=f1fc5d0a… declared_valid=true declared_match=false
                                                                             exit 0
```

The two superseding rows are honest (SKILL.md at the tip, lines 1450–1451): `c69_tmp_honour.py`
demoted to `instrument` with Self-test `none` (the contract's prescribed demotion, closing carried route
R2), and `c74_registry_gap.py` keeps Kind `gate` and records "eight frozen fixtures f1 f2 … f8,
`selftest 8/8`, exit 0" — the claim was **restated**, not dropped. The round's own instruments are in
the population (18), and the committed receipt binds all 18 at the tip.

## 1. (Q1) The base red is real

```
$ python3 -B <frozen counter 43538343> --root <clone@c9c5e484> \
    --revision c9c5e484… --base c9c5e484… --work <scratch>
C1v1 revision=c9c5e484c533aa65f4374b841a3edcf572ed19a9 rows=28 live=16 files=16 mismatches=2
     classes=E1 E3 append_only=true met=false                                     exit 1
  finding: E1 .ufo/waves/round-69/c69_tmp_honour.py: Kind is gate without a self-test mode or a declared differential
  finding: E3 .ufo/waves/round-74/c74_registry_gap.py: cell enumerates 5 fixture ids, observed total 8
```

Byte-identical to `controls/base-c1-row-truth.txt`. The landed counter (`0699a672`) produces the same
two findings at base (it only appends `missing_frozen=0`). **Neither finding is spurious:**

- `c69_tmp_honour.py` — SKILL.md:1426 (base) Kind `gate (live; …)`; its own Self-test cell says
  `none (no self-test mode; --selftest is an argparse error, exit 2 …)`; running it gives
  `error: the following arguments are required: --root, --revision, --work`, exit 2. A gate row whose
  own cell says there is no self-test. E1 is the correct verdict.
- `c74_registry_gap.py` — `--selftest` prints `selftest 8/8`, exit 0; `FIXTURES` registers f1…f8
  (`c74_registry_gap.py:491-493`, `fx_f1…fx_f8` at 350–479); its docstring (line 25) still says
  "builds the five contract fixtures f1-f5" and the registry cell repeated those five ids. Stale prose,
  eight-fixture instrument. E3 is the correct verdict.

**One harness-artifact class exists** (does not touch base, but it will bite any new row): the counter
substitutes only `[--work <dir>]`, `--work <dir>`, `<scratch>`, `<lane>` before running a Self-test cell
literally (`c75_row_truth.py:215-218`, identical in the landed blob). A cell written in Entry-command
style with `--revision <commit>` becomes a shell redirect:

```
$ bash -c 'python3 -B scripts/instrument_receipts.py --root . --revision <commit> --selftest'
bash: line 1: commit: No such file or directory                                  exit=1
```

which the counter reports as `E1 … recorded self-test exits 1`. Measured on 90a4cdd5 (same code path as
the landed blob, not re-run on 0699a672). Minimal correction: substitute `<rev>`/`<commit>`/`<revision>`
too, or forbid them in Self-test cells.

## 2. (Q2) Do-nothing control

- C1: measured in §1 — `met=false`, exit 1, on both the frozen and the landed counter.
- C2: `population=16 bound=0 mismatches=16 met=false`, exit 1 (receipt absent at base).
Nothing added cannot reach either target.

## 3. (Q3) Predicate fidelity

Eight divergences were open at some point in the round; four are closed in the landed blobs. Column
"landed" is the blob at `4e3fc159`.

| # | Contract sentence | Divergence | Status |
|---|---|---|---|
| D1 | §C1 E4 "every `.py`/`.mjs` path token in the row's cells resolves" | frozen v0 checked only the single effective instrument | **closed** by A4; landed checks the effective row and every live row (`402-413, 466-477`); measured: `e4bogus` 2e7511d1 → v0 met=true, landed `E4 … scripts/c75_missing_tool.py does not resolve` exit 1 |
| D2 | §C1 kill rule "…or when the file list the counter derives differs from the 16 above" | v0 printed `files` and never compared it; two words in two Kind cells (`histmark` 55965b3c, `2 insertions/2 deletions`) gave `files=14 mismatches=0 met=true` exit 0 | **terms changed by A1** (floor + `missing_frozen`), landed: same state → `mismatches=2 … missing_frozen=2 met=false` exit 1; growth is now legal by design (`pop17` 99214e6c → `files=17 met=true`; the landed tip itself is `files=18 met=true`) |
| D3 | §C1 "Output line: … `files=16` … `met=<bool>`" | landed prints `files=N … met=… missing_frozen=N` | **residual**: A1 authorises the term, but `controls/base-c1-row-truth.txt` at the tip still carries the v0 line, so the committed base control is not byte-reproducible with the landed counter (`… met=false` vs `… met=false missing_frozen=0`) |
| D4 | A2: "the claim segment … after the recorded command up to its first `;` — pairs in later segments … are not claims" | at 90a4cdd5 the helper implementing it had **zero call sites**; E2 read the whole cell and rejected a truthful `9/9` + later `8/8` row (`e2seg` 111a5ed8 → `E2 … claims 8/8, observed 9/9`, exit 1) | **closed** at the landed blob (`claim_pairs` called at 428); landed: `e2seg` 861b737d → `mismatches=0 met=true` exit 0 |
| D5 | §C1 E2 "the observed `--selftest` pass/total equals it" | both blobs implement "the **last** `\d+/\d+` anywhere in stdout+stderr" (`observed_pair`, landed `275-280`). A row that truthfully records `c58_resolver_cases`' 7 controls as `7/7` is rejected because the output later prints `base_tool: score=6/14` | **open at the landed blob**: `e2false58` 38f3b79b → `E2 … cell claims 7/7, observed 6/14`, exit 1. `pairs.json` shows the same latent shape for `c59_resolver_cases` (last ratio 20/21) |
| D6 | §C1 E1 "working self-test **or** the Kind cell declares `differential`" | code reds a row that declares `differential` *and* records a failing command (`if cmd is None … elif rc != 0`) | **open, latent** — no landed row has both; `declares_differential` is used only for the no-command branch |
| D7 | §C2 / A6–A7 | evidence receipts at 21:08 printed `tool sha256=62b795ea…` (neither delivered copy), accepted a worktree receipt, and shipped `ctl-other-revision.txt` with `control: expect not met` + `met=true exit=0`; the newest tool then failed its own selftest 4/15 (stale fixtures passing the removed `--require-committed`) | **closed at the landed tip**: tool `162dd685`, `--selftest 17/17` exit 0, receipts regenerated and citing `162dd685`; landed A6/A7 measured (worktree-only → `source=uncommitted` met=false; non-ancestor declared revision → `receipt_revision_invalid`, met=false) |
| D8 | §C1 controls "committed receipts" | `ctl-cheapcontent.txt` cites `83a9bc27…`, `ctl-deletion.txt` cites `afc73a87…`; **neither object exists in the lane** (`git cat-file -e` fails, `rev-list --all` empty) | **open**: two of the three §C1 controls cannot be replayed from committed bytes. The base control can |

Identity note: the landed counter blob `0699a672` differs from the `w1/ExecC1Counter/c75_row_truth.py`
copy `63e321b2` (both 47,446 B). My fixture verdicts were identical on both (base 2, `launder` green,
`e2false58` red, `e2seg` green), so no verdict divergence was measured — but the seat's evidence
directory holds a counter that is not the landed one. The C2 receipt does hash the landed counter
(18 entries), which is the property carried route R5 asked for; the C1 w1 receipts name no digest.

## 4. (Q4) Claim independence — two minimal states, measured

| State | C1 | C2 |
|---|---|---|
| `fix-honest` 7499a5e0 (two honest superseding rows, **no receipt**) | `files=16 mismatches=0 met=true` exit 0 | receipt absent → `population=16 bound=0 mismatches=16 met=false` |
| `fix-receipt-base` f52f5456 (base + a committed 16-entry receipt, SKILL.md untouched) | `mismatches=2 classes=E1 E3 met=false` exit 1 | `bound=16 mismatches=0 met=true` exit 0 |

Verdict: independent by construction; C1 is green with no receipt, and C2 is green on the exact tree C1
rejects. Correct reading: C2 certifies binding only, never calibration.

## 5. (Q5) Target sizing

- do-nothing: **no** (measured).
- junk repeating the wrong claims: **no** per the contract, but that control is unverifiable (D8).
- honest appended row per failing file: **yes**, and erasure is the same cost. Fixture `launder`
  (rebuilt e3903abc): c69 → `instrument` + `none`; c74 → Kind `gate`, Self-test cell reduced to the bare
  command, no tally and no `f<N>` ids. Landed counter: `files=16 mismatches=0 append_only=true met=true
  missing_frozen=0`, exit 0. E2/E3 are conditional on the cell *recording* a tally/ids, so deleting them
  is a silent no-op; `instrument`+`none` is a second erasure path for c74.

Verdict: the claim is a **"no false claim"** property; erasure satisfies it. Cost is proportionate for a
score-2 axis, but `met=true` does not mean "the claim re-derives" — it means "no row records a claim
that fails". The landing did **not** launder: the c74 row at `4e3fc159:SKILL.md:1451` records the eight
fixtures and `8/8`. Strongest counter-argument to this finding: falsification needs only to catch false
claims; completeness belongs to the reviewer/mutation seats and to the after-state plan, which named the
honest content and was followed. That holds here; the residual is that nothing would have caught the
erasure. Minimal corrections: add the `launder` state as a control, and/or evaluate E2/E3 over the union
of the effective and superseded rows for the same instrument.

## 6. (Q6) C2 attack

- **Do-nothing receipt passes?** No. Base → `population=16 bound=0 mismatches=16 met=false`. The frozen
  equation `met = (bound == population) and (mismatches == 0)` is vacuously true at `population==0`; a
  literal reader deriving the population from the receipt reads `met=true` on the same do-nothing tree
  plus an empty receipt (`refcheck_c2.py`, labelled measuring stick, not tool evidence). The landed tool
  closes it with the frozen floor + `missing_frozen == 0`; measured base run proves it.
- **Cheapest path to `bound=16`.** A 20-line `git show <rev>:$path | sha256sum` loop regenerates the
  full 16-entry receipt (3,132 B) in **0.064 s** and passes the check. Honest binding, zero capability:
  C2's score must rest on the tool's selftest (capability row), never on `bound`.
- **Tip population is 18, not 16.** Measured earlier at an 18-file state: the 16-entry receipt reads
  `population=18 bound=16 mismatches=2 met=false`; rewriting at the tip gives `bound=18 met=true`. The
  landed receipt has 18 entries and the tip is green. Because the receipt hashes the tool, any later
  edit to `scripts/instrument_receipts.py` re-reds C2.
- **Declared revision.** The landed receipt declares `f1fc5d0a` (its parent) while the check runs at
  `4e3fc159`: `declared_match=false`, `declared_valid=true`. A7 only requires an ancestor, so this is
  legal; it does mean the receipt never claims the tip revision, and the binding rests on the 18 blobs
  being unchanged between the two commits.

## 7. Residual risk, ranked

1. **D5 — E2 observes the wrong number.** A truthful tally (`7/7`) is reported red because a later,
   unrelated ratio (`6/14`) is taken as the observation. Minimal fix: take the tally from the selftest's
   own total line, or require a named pass/total token. This is the only residual that can produce a
   wrong **verdict**, not just a weak one.
2. **D8 — two §C1 controls are unreplayable** (`83a9bc27`, `afc73a87` absent). Replace with fixture
   commits or stop calling them committed receipts.
3. **Claim erasure is reachable** (D5-adjacent, §5). The landing is honest; the predicate cannot tell.
4. **D3 — the base control receipt does not match the landed counter's output line** (no
   `missing_frozen`). Re-measure it with `0699a672` and commit the new receipt.
5. **Identity drift**: `w1/ExecC1Counter/c75_row_truth.py` (`63e321b2`) ≠ landed (`0699a672`); the C1 w1
   receipts name no counter digest. Copy the landed blob into the evidence dir or record its sha256.
6. **Placeholder false-red** (`<commit>` in a Self-test cell) — latent for any future row.
7. **D6 — differential + failing command** is red though the contract's disjunction holds — latent.

None of these blocks the two claims: at `4e3fc159` both re-derive `met=true`, exit 0, from committed
bytes in an independent clone.

## 8. Unrun / not established

- The `<commit>` redirect was measured on the pre-landing counter `90a4cdd5`; the landed blob's
  substitution code is identical (215-218) but the redirect state was not re-run on `0699a672`.
- E2's false red was measured on the landed blob for `c58_resolver_cases` only; `c59` is inferred from
  `pairs.json` (its last ratio is `20/21`), not run.
- The two controls of D8 cannot be run at all (their revisions are absent).
- C2 `--write` idempotence, the S443 source row, and the mutation-tester's matrix were not re-tested
  (other seats own them); `refcheck_c2.py` is a pre-amendment reader, not tool evidence.
- My fixture commit ids cite scratch repositories that were removed at yield. `mkfix.py` (the row
  templates) plus the diffstats in `fixture-commits.txt`/`revs2.txt` are the reproduction path; the
  ids are a record of what was measured, not a re-derivable receipt. The two claims themselves were
  re-measured at the landed tip, which is re-derivable from committed bytes.
- No measurement was made of the fleet repo or any sibling lane.

## Appendix — commands and exit codes

| # | Command (paths elided) | Exit | Receipt |
|---|---|---|---|
| 1 | frozen counter `43538343` @ base, `--base` base | 1 | `base-run.txt` |
| 2 | landed counter `0699a672` @ base | 1 | `lout-base.txt` |
| 3 | landed counter @ `4e3fc159` | 0 | `landed-c1.txt` |
| 4 | landed tool `162dd685` @ base, `--check` | 1 | `landed-c2-base.txt` |
| 5 | landed tool @ `4e3fc159`, `--check` | 0 | `landed-c2.txt` |
| 6 | landed counter on `launder` e3903abc | 0 | `lout-launder.txt` |
| 7 | landed counter on `e2false58` 38f3b79b | 1 | `lout-e2false58.txt` |
| 8 | landed counter on `e2seg` 861b737d | 0 | `lout-e2seg.txt` |
| 9 | landed counter on `histmark2` 2fdc1f50 | 1 | `lout-histmark2.txt` |
| 10 | landed counter on `pop17` 99214e6c | 0 | `lout-pop17.txt` |
| 11 | landed counter `--selftest` | 0 (`fixtures=26 passed=26`) | `lout-self.txt` |
| 12 | landed C2 `--selftest` | 0 (`17/17`) | `landed-c2-selftest.txt` |
| 13–16 | C2 states with the landed tool: worktree-only / non-ancestor / 16-entry at 18 files / rewritten+committed | 1 / 1 / 1, then 0 | `receipts-c2-landed.txt` |
| 17–24 | pre-landing blob runs (frozen v0 and 90a4cdd5 / a2005c6a, f1666904) | see files | `out-*.txt`, `dout-*.txt`, `receipts-c2.txt`, `c2-selftest-a2005c6a.txt` |
| 25 | fixture commits / diffstats | — | `fixture-commits.txt`, `revs2.txt` |

`MANIFEST.sha256` covers every file in this directory. No lane file was modified by this seat.
