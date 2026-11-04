# CriticPredicates — round 75, wave w1 (kake)

Seat: critic (leaf; no subagents, no `ask`). Scope: falsify §C1 and §C2 as frozen, from committed
bytes in an independent clone. The lane tree was read-only for this seat; no git/jj mutation in the
lane, no writes outside this directory and my scratch. Scratch
`/fast/scratch/hyaku/kake-r75/CriticPredicates` (independent `git clone --shared` at base, fixtures
as further `--shared` clones, toplevel asserted before every first commit, commits made with
`-c user.name/-c user.email`, no global config touched) was removed before yield; receipts are in
`w1/CriticPredicates/` with `MANIFEST.sha256`. No tool installed, upgraded or downgraded.

Reference artifacts used: frozen contract `88f2e05:.ufo/waves/round-75/contract.md`; frozen counter
`88f2e05:.ufo/waves/round-75/c75_row_truth.py` (sha256 `43538343…`, byte-identical to the lane
worktree copy); amendments 1–3 at `.ufo/waves/round-75/`; delivered artifacts
`w1/ExecC1Counter/c75_row_truth.py` (`90a4cdd5…`, selftest 22/22) and
`w1/ExecC2Tool/instrument_receipts.py` (`a2005c6a…`, selftest 4/15).

## Axes (named) and what moved

| Axis | Question | Verdict |
|---|---|---|
| A1 base red | is `mismatches=2` real from committed bytes? | **real; both findings, neither a harness artifact** |
| A2 do-nothing | base tree, nothing added | **cannot reach met=true** (C1 exit 1; C2 `bound=0`) |
| A3 fidelity | contract vs counter vs delivered artefacts | **6 open divergences, 3 of them measured false verdicts** |
| A4 independence | C1 green without C2, C2 without C1 | **both measured; independent** |
| A5 target cost | is `2→0` too cheap for one claim? | **reachable by erasing two claims; same cost as the honest fix** |
| A6 C2 attack | do-nothing receipt; cheapest path | **do-nothing cannot pass; a 0.064 s hash loop reaches bound=16; 18-file landing hazard** |

---

## 1. (Q1) The base red is real

Command (frozen counter blob taken from the freeze commit, run against an independent clone of the
base revision; clone outside the scratch root, fresh `HOME`/`TMPDIR`):

```
$ git clone -q --shared <lane> $S/clone-base && git -C $S/clone-base checkout -q c9c5e484…
$ git show 88f2e05f…:.ufo/waves/round-75/c75_row_truth.py > $S/c75_frozen.py   # sha256 43538343c1f26e15…
$ python3 -B $S/c75_frozen.py --root $S/clone-base --revision c9c5e484… --base c9c5e484… --work $S/work-base
C1v1 revision=c9c5e484c533aa65f4374b841a3edcf572ed19a9 rows=28 live=16 files=16 mismatches=2 classes=E1 E3 append_only=true met=false
  finding: E1 .ufo/waves/round-69/c69_tmp_honour.py: Kind is gate without a self-test mode or a declared differential
  finding: E3 .ufo/waves/round-74/c74_registry_gap.py: cell enumerates 5 fixture ids, observed total 8
exit=1
```

Byte-identical to `controls/base-c1-row-truth.txt` (`receipts/base-run.txt`, `out-*` in this dir).

**Neither finding is spurious.**

- `c69_tmp_honour.py`: the row's Kind cell reads `gate (live; …)` (SKILL.md:1426, base blob) and its
  own Self-test cell reads `none (no self-test mode; --selftest is an argparse error, exit 2 …)`.
  Running the recorded mode: `python3 -B .ufo/waves/round-69/c69_tmp_honour.py --selftest` →
  `error: the following arguments are required: --root, --revision, --work`, exit 2. The row is
  self-contradictory (Kind says gate, its own cell says there is no self-test); E1 is correct.
- `c74_registry_gap.py`: `--selftest` prints `selftest 8/8`, exit 0; the instrument registers
  `FIXTURES = (("f1", fx_f1), … ("f8", fx_f8))` (`c74_registry_gap.py:491-493`; `fx_f1…fx_f8` at
  350–479). Its docstring (line 25) still says "builds the five contract fixtures f1-f5", and the
  registry cell enumerates the same five ids. Stale prose, an eight-fixture instrument; E3 is correct.

**One harness artifact class exists and does not touch base.** The counter executes Self-test cells
literally and substitutes only `[--work <dir>]`, `--work <dir>`, `<scratch>`, `<lane>`
(`c75_row_truth.py:212-218`; identical in the delivered counter at 215-218). A cell written in the
house Entry-command style with `--revision <commit>` becomes a shell redirect:

```
$ bash -c 'python3 -B scripts/instrument_receipts.py --root . --revision <commit> --selftest'
bash: line 1: commit: No such file or directory          exit=1
```

The counter reports that as `E1 … recorded self-test exits 1`. Measured on the first draft of my
17-file fixture (rev `89f18aa6`, `dout-pop17` first run); removing `<commit>` made the same state
green (rev `1f1ed1a5`, `out-pop17`/`dout-pop17`). Any after-state Self-test cell carrying
`<rev>`/`<commit>`/`<revision>` is a false red. Minimal correction: substitute those three tokens
with `--revision`'s value, or forbid them in Self-test cells (they are legal only in Entry cells).

## 2. (Q2) Do-nothing control

Measured, not assumed. A tree at `c9c5e484` with nothing added (`clone-base`, `--base` equal to the
revision) gives `mismatches=2 classes=E1 E3 append_only=true met=false`, exit 1 (§1). C2 on the same
tree: `population=16 bound=0 mismatches=16 met=false`, exit 1 — receipt absent. Nothing added cannot
reach either target. (A1/A2 amendments do not change this; the delivered counter agrees:
`dout-base` = same line plus `missing_frozen=0`.)

## 3. (Q3) Predicate fidelity — contract vs counter vs delivered receipts

The third leg ("the receipt/labels Exec seats delivered") now exists, so it is compared. Divergences
are named word-for-word; measured counterexamples are cited by revision and receipt file.

### D1 — E4 scope (false green in the frozen counter; **closed**)
- Contract §C1 E4: "every `.py`/`.mjs` path token in the row's cells resolves at the measured revision."
- Frozen v0: checks only the single effective instrument (`git cat-file -e <rev>:<f>`), not the row's tokens.
- Measured (fixture `e4bogus`, rev `2e7511d1`): v0 → `files=16 mismatches=0 met=true`, exit 0, while
  `git cat-file -e 2e7511d1:scripts/c75_missing_tool.py` fails and that token sits in the effective
  row's Entry cell (`out-e4bogus`). Delivered counter → `E4 scripts/citation_lint.py: path token
  scripts/c75_missing_tool.py does not resolve`, exit 1 (`dout-e4bogus`).
- Status: closed by amendment A4 and the delivered code (`c75_row_truth.py:402-413, 466-477`).

### D2 — frozen-16 vs kill rule (false green in v0; **terms changed by A1**)
- Contract §C1 kill rule: "not met … when the file list the counter derives differs from the 16 above."
- Frozen v0: `files` is printed and never compared; `met = (not findings and append_only)`.
- Measured (fixture `histmark`, rev `55965b3c` — **two words** inserted into the two Kind cells,
  `SKILL.md | 2 insertions(+), 2 deletions(-)`, no new row, no execution): v0 → `rows=28 live=14
  files=14 mismatches=0 append_only=true met=true`, exit 0 (`out-histmark`). This is the cheapest
  reachable met=true and v0 calls it met. Delivered counter → `mismatches=2 … missing_frozen=2
  met=false`, exit 1 (`dout-histmark`).
- Measured (fixture `pop17`, rev `1f1ed1a5`, an appended live row for a new instrument): both counters
  `files=17 … met=true` (`out-pop17`, `dout-pop17`) — legal under A1's floor, forbidden by the frozen
  kill rule.
- Status: A1 changes the term (floor + `missing_frozen`) and documents the change; the delivered
  counter implements it. The frozen v0 blob the contract names still returns met=true on the shrink,
  so any replay of §C1 with the contract's own word "Counter" is lenient.

### D3 — output line (documented shape change; base receipt now stale)
- Contract §C1: "Output line: `C1v1 revision=<rev> rows=N live=N files=16 mismatches=M classes=… append_only=<bool> met=<bool>`."
- Delivered: `… files={len(groups)} … met=… missing_frozen=N` (`c75_row_truth.py:499-506`). At base:
  `… met=false missing_frozen=0` vs the committed control's `… met=false`.
- Status: A1 authorises the extra term, but `controls/base-c1-row-truth.txt` is no longer reproducible
  with the landed counter. Re-measure the base control with the landed blob and commit the new receipt.

### D4 — Amendment 2's claim-segment sentence is not wired (false red, **open**)
- Amendment 2 (A2 text): "The claim segment for E2 is the text after the recorded command up to its
  first `;` … pairs in later segments (receipt history) are not claims."
- Delivered code: `claim_pairs(cell, command)` implements exactly that (`c75_row_truth.py:~250`) and has
  **zero call sites**; E2 still calls `claim_pair(selftest_cell)` — whole cell, last pair (line 446).
- Measured (fixture `e2seg`, rev `111a5ed8`; truthful row: `… --selftest` -> `9/9` passed, then a later
  sentence "the round-47 receipt records `8/8`"): `E2 scripts/citation_lint.py: cell claims 8/8,
  observed 9/9`, exit 1 (`dout-e2seg`). The row's claim is 9/9 and true; the red exists only because
  the clause is documentation, not code. Amendment 2 A5 ("the same sentence in three places") is
  therefore already broken by its own counter.
- Minimal correction: call `claim_pairs(cell, cmd)` in E2, and state the multi-pair policy (all pairs
  in the claim segment must equal the observed pair).

### D5 — E2's "observed pass/total" is the last ratio anywhere (false red, **open in both versions**)
- Contract §C1 E2: "the observed `--selftest` pass/total equals it."
- Both counters: `observed_pair(out)` = the **last** `\d+/\d+` in combined stdout+stderr.
- Measured (fixture `e2false58`, rev `284264a3`; row for `c58_resolver_cases.py` recording its real
  `7/7` controls; the instrument's own line is `selftest: ok (7 controls; P7 satisfied on a fixture
  lane)`, but output later contains `ok base_tool: score=6/14`): frozen v0 and delivered both print
  `E2 … cell claims 7/7, observed 6/14`, exit 1 (`out-e2false58`, `dout-e2false58`). `pairs.json`
  records the ratios of all 16 instruments at base: `c58_resolver_cases` (last 6/14) and
  `c59_resolver_cases` (last 20/21) are the two whose last ratio is not their tally — a truthful row
  for either cannot record its tally.
- Minimal correction: observe the tally from the self-test's own total line (last line matching
  `selftest[:\s].*?(\d+)\s*/\s*(\d+)`), or have instruments print a named `pass/total` token the row
  must match.

### D6 — E1's disjunction vs implementation order (latent false red)
- Contract E1: "carries a working self-test (`--selftest` exits 0), **or** its Kind cell declares the
  differential substitute."
- Code: `if cmd is None: (finding unless differential) elif rc != 0: finding` — a row that declares
  `differential` and also records a failing command is red though the disjunction holds. Not exercised
  at base (the only differential row, `c57`, records no command). `declares_differential()` exists and
  is also unused.
- Minimal correction: `if not (declares_differential(kind) or rc == 0): finding`.

### D7 — C2 evidence receipts vs the C2 tool (provenance and selftest, **open**)
- Contract §C2/§C2 capability row: evidence is `scripts/instrument_receipts.py`'s `--selftest` receipt.
- `w1/ExecC2Receipts/*.txt` all print `tool sha256=62b795eaa8ad446d…`; the delivered copies hash
  `a2005c6ad8043fd9…` (ExecC2Tool) and `f166690425bb8950…` (ExecC2Receipts). **None matches**, and the
  receipts' output shape (`receipt: worktree committed=absent … met=true`) matches neither blob's
  (`receipt: source=… worktree=…`). The evidence is therefore produced by a third, undelivered blob
  that accepted worktree receipts — the pre-A6 behaviour.
- Both delivered blobs do enforce A6/A7 and the floor (measured: worktree-only → `source=uncommitted`,
  met=false; descendant-declared → `declared_valid=false`; 18-file tip → `beyond_frozen=2`).
- The two delivered blobs differ in selftest state: `f1666904` (30,006 B) passes 23/23, while the newer,
  larger `a2005c6a` (49,634 B) **fails 4/15, exit 1** — its selftest still passes the removed
  `--require-committed` flag (`c2_tool.py:958,967`; argparse now has no such option → exit 64) and
  still expects a worktree receipt to check green, which A6 now rejects.

### D8 — C2 control recorded failing (`ctl-other-revision.txt`)
- Its own label: "control: expect not met (freeze is a descendant of base, not an ancestor)"; observed
  `C2v1 … met=true`, `exit=0`. The control failed and shipped. A7 now rejects that state (measured,
  `receipts-c2.txt` (c): `declared_valid=false`, 16 `receipt_revision_invalid`, met=false), so the
  receipt is stale rather than the rule being absent.

### D9 — frozen controls 2 and 3 are not re-derivable
- `controls/ctl-cheapcontent.txt` cites revision `83a9bc27…`, `controls/ctl-deletion.txt` cites
  `afc73a87…`; neither object exists in the lane (`git cat-file -e` fails; `git rev-list --all | grep`
  empty). The base control is re-derivable (§1); these two are observed-only receipts and cannot be
  replayed from committed bytes.

### D10 — the frozen counter is absent at base
`git cat-file -e c9c5e484:.ufo/waves/round-75/c75_row_truth.py` fails; the tool lands at `88f2e05`.
Replaying the base control "from the base revision" requires taking the counter from the freeze commit.
Trivial, but the contract's command block does not say which blob is authoritative.

## 4. (Q4) Claim independence — two minimal states, measured

| State | C1 | C2 |
|---|---|---|
| `fix-honest` rev `7499a5e0` (base + the two honest superseding rows, **no receipt**) | `files=16 mismatches=0 append_only=true met=true`, exit 0 (`out-honest`) | `population=16 bound=0 mismatches=16 met=false` (receipt absent at that rev) |
| `fix-receipt-base` rev `f52f5456` (base + a committed 16-entry receipt, **SKILL.md untouched**) | `mismatches=2 classes=E1 E3 met=false`, exit 1 (`out-c1-on-receipt-base`) | `bound=16 mismatches=0 met=true`, exit 0 |

Verdict: the claims are mechanically independent; neither conjunct references the other. C1 can be
green with no receipt, and C2 can be green on the exact tree C1 rejects. That is intended (binding ≠
calibration) and is the correct reading of §C2 — it must not be read as cross-support.

## 5. (Q5) Target sizing

Reachability of `mismatches 2→0`:
- do-nothing: **no** (measured, §2);
- junk repeating the wrong claims: **no** per the contract, but that control cannot be re-derived
  (D9); I measured the stronger variant instead — **claim erasure**;
- one honest appended row per failing file: **yes**, and cheaper: **two appended rows that erase the
  claims** reach `met=true`, exit 0. Fixture `launder` rev `afc2bd76` (`SKILL.md | 9 insertions(+)`):
  c69 → Kind `instrument` + Self-test `none` (the contract's prescribed demotion, zero execution);
  c74 → Kind `gate`, Self-test cell reduced to the bare `--selftest` command, **no tally and no
  `f<N>` ids**. Both counters: `files=16 mismatches=0 append_only=true met=true missing_frozen=0`,
  exit 0 (`out-launder`, `dout-launder`). The c74 branch works because E2 and E3 are conditional on
  the cell *recording* a tally/ids (`pairs = claim_pair(selftest_cell)`, `ids = FIX_RE.findall(cell)`);
  dropping them is a silent no-op. A second erasure path is `instrument`+`none` for c74 (E1 only binds
  a `gate` row), which clears the instrument entirely.

Verdict: **cheap but proportionate in cost** (two cell edits for a score-2 axis) **and too cheap as
stated**, because `met=true` does not mean "every live row's claim re-derives by execution" — it means
"no live row records a claim that fails". Erasure and correction are indistinguishable in the verdict.
Strongest counter-argument to this finding: the frozen claim is literally a "stops claiming states its
instruments do not have" property, and deleting a false claim satisfies it; the §After-state plan names
the honest content (demotion for c69, "recording the eight fixtures" for c74) and the reviewer /
mutation-tester seats can read the landed rows, so completeness does not have to be in the predicate.
That holds **only if** the landed receipt describes what actually happened. If the c74 row omits the
eight fixtures, the claim is met by erasure and the receipt must say so; describing it as "the claim
re-derives" would be false provenance. Minimal corrections: (i) add the `launder` state to the
contract's control table (no control covers the cheapest reachable met=true); (ii) evaluate E2/E3 over
the union of the effective row and the rows it supersedes for the same instrument, so dropping a tally
cannot clear it; (iii) or require the superseding row to restate the claim and the receipt to record
the restatement.

## 6. (Q6) C2 attack

- **Can a do-nothing tree land a passing receipt?** No, under the derivation the contract specifies:
  base → `population=16 bound=0 mismatches=16 met=false`, exit 1 (measured with the delivered tool and
  with a literal reader, `receipts-c2.txt` (a)). The frozen equation `met = (bound == population) and
  (mismatches == 0)` **is vacuously true at `population==0`**: my pre-amendment literal reader, when
  deriving the population from the receipt instead of SKILL.md, reads `population=0 bound=0
  mismatches=0 met=true` on the same do-nothing tree plus an empty receipt (`refcheck_c2.py`, labelled
  as a measuring stick, not tool evidence). The delivered tool closes this with the frozen floor +
  `missing_frozen == 0` (A1/A2). The guard is real but it lives in the derivation, not in the frozen
  equation — worth keeping in the text.
- **Cheapest path to `bound=16`.** A 20-line loop of `git show <rev>:$path | sha256sum` regenerated the
  full 16-entry receipt (3,132 B) in **0.064 s**; it passes the same check. That is honest binding (the
  digests are real, a fabricated digest fails: `bound=0 mismatches=16`, and a dropped path gives
  `bound=15 mismatches=1`, both measured). It certifies nothing about the instruments or the tool —
  which is by design, and is why the C2 score must rest on the tool's selftest (capability row), never
  on `bound=16` alone.
- **Landing hazard (measured).** At an 18-file after-state (my reconstruction of the round's own rows
  for `.ufo/waves/round-75/c75_row_truth.py` and `scripts/instrument_receipts.py`), the delivered
  16-entry receipt reads `population=18 bound=16 mismatches=2 met=false`, with
  `beyond_frozen=2` and `missing .ufo/waves/round-75/c75_row_truth.py: receipt has no entry`
  (`receipts-c2.txt` (e)). Rewriting the receipt at the tip gives `bound=18 mismatches=0 met=true` ((f)).
  Because the tool hashes itself, **any post-receipt edit to `scripts/instrument_receipts.py`
  re-reds C2**, and the receipt must be written after the C1 rows land. The contract's target line
  `population=16 bound=16` is unreachable at a self-applying tip; A1/A2 restate the population and the
  after-receipt must carry 18.
- **Blocker.** The newest delivered C2 blob (`a2005c6a`) **fails its own `--selftest`: `selftest:
  4/15`, exit 1**, in both a neutral fresh `HOME`/`TMPDIR` and the C1 counter's harness, because its
  fixtures still require the removed `--require-committed` flag and still expect a worktree receipt to
  check green (D7). The `23/23` receipt belongs to neither delivered blob; the earlier copy `f1666904`
  passes 23/23 and implements A6/A7, so it is a landable candidate, but its evidence receipts must be
  regenerated from its own digest. Consequences: (i) the capability row's evidence is unreproducible;
  (ii) with an honest live `gate` row for the tool, C1's E1 fails — measured at the 18-file
  after-state: `C1v1 … files=18 mismatches=1 classes=E1 … met=false`,
  `finding: E1 scripts/instrument_receipts.py: recorded self-test exits 1` (`dout-after18`);
  (iii) demoting the tool's row to `instrument`+`none` would silence E1 and destroy the capability
  evidence.

## 7. Ranked land blockers and smallest safe corrections

1. **C2 self-blob identity and selftest** (D7). Pick the blob that ships: `f1666904` passes 23/23 and
   implements A6/A7/floor; `a2005c6a` implements the same rules but its selftest is red (4/15) because
   it still exercises the removed `--require-committed` flag and a worktree receipt. Repair or drop the
   red blob, then regenerate every `w1/ExecC2Receipts/*` receipt from the shipped blob's own digest —
   the current receipts cite `62b795ea`, which is neither. Without this, C1's self-application row
   cannot be green and C2's capability evidence is false provenance.
2. **Order the landing: rows first, receipt last, tool bytes frozen before the receipt** (measured
   hazard above). Regenerate `corpus/knowledge/instrument-receipts.json` at the landed tip with 18
   entries; any later edit to `scripts/instrument_receipts.py` invalidates it.
3. **Wire `claim_pairs` into E2** or strike the A2 clause (D4, measured false red on a truthful row).
4. **Fix E2's observation** to the self-test's own total line (D5, measured false red on `c58`; `c59`
   is the second latent case).
5. **Add an erasure control** and decide whether a superseding row may drop a numeric claim (§5).
6. **Re-measure the base control with the landed counter** (D3) and replace
   `controls/ctl-cheapcontent.txt` / `ctl-deletion.txt` with replayable fixture commits (D9).
7. **Fix or forbid `<rev>`/`<commit>` placeholders in Self-test cells** (§1) before writing the new rows.

## 8. What this report does not establish

- No measurement of the lane's landed tip: no after-state row exists at `ab939c46`; every after-state
  number above is my own fixture state, named by revision.
- The two frozen controls citing absent revisions were not re-run (impossible from committed bytes);
  they are reported as unverifiable, not as passing or failing.
- C2 `--write` idempotence, the S443 source row, and the C2 tool's forged-receipt matrix were not
  re-tested (other seats own them).
- `refcheck_c2.py` is a literal reader of the pre-amendment text, kept to show the `population==0`
  vacuity; it is not evidence of delivered-tool behaviour.

## Appendix — commands and exit codes

| # | Command (scratch paths elided) | Exit | Receipt |
|---|---|---|---|
| 1 | frozen v0 counter, base, `--base` base | 1 | `base-run.txt` |
| 2 | frozen v0, `honest` 7499a5e0 | 0 | `out-honest.txt` |
| 3 | frozen v0, `launder` afc2bd76 | 0 | `out-launder.txt` |
| 4 | frozen v0, `e4bogus` 2e7511d1 | 0 | `out-e4bogus.txt` |
| 5 | frozen v0, `e2false58` 284264a3 | 1 | `out-e2false58.txt` |
| 6 | frozen v0, `histmark` 55965b3c | 0 | `out-histmark.txt` |
| 7 | frozen v0, `pop17` 1f1ed1a5 | 0 | `out-pop17.txt` |
| 8 | frozen v0, base+receipt f52f5456 | 1 | `out-c1-on-receipt-base.txt` |
| 9 | delivered C1, base | 1 | `dout-base.txt` |
| 10 | delivered C1, histmark | 1 | `dout-histmark.txt` |
| 11 | delivered C1, pop17 | 0 | `dout-pop17.txt` |
| 12 | delivered C1, e4bogus | 1 | `dout-e4bogus.txt` |
| 13 | delivered C1, e2false58 | 1 | `dout-e2false58.txt` |
| 14 | delivered C1, launder | 0 | `dout-launder.txt` |
| 15 | delivered C1, a3other dd77a6b3 | 1 | `dout-a3other.txt` |
| 16 | delivered C1, e2seg 111a5ed8 | 1 | `dout-e2seg.txt` |
| 17 | delivered C1, after18 7a097c17 | 1 | `dout-after18.txt` |
| 18 | delivered C1 `--selftest` | 0 (`fixtures=22 passed=22`) | `dout-self.txt` |
| 19 | delivered C2 `--selftest` (ExecC2Tool a2005c6a) | 1 (`4/15`) | `receipts-c2.txt` (g) |
| 20 | ExecC2Receipts copy `--selftest` (f1666904) | 0 (`23/23`) | `receipts-c2.txt` (g) |
| 21–26 | C2 check states (a)–(f) | 1/1/1/0/1/0 | `receipts-c2.txt` |
| 27 | fixture commits / diffstats | — | `fixture-commits.txt` |
| 28 | tool digests | — | `tool-digests.txt` |

`MANIFEST.sha256` covers every file in this directory. No lane file was modified.
