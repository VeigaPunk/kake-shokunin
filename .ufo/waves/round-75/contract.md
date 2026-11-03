# Round 75 — frozen contract (kake)

Frozen 2026-11-03 by the L1 (`KakeR75`) before any wave seat ran. Base revision
`c9c5e484c533aa65f4374b841a3edcf572ed19a9` (lane master at round open; the round-74
verifier spot-check tip). Host `linux-x86_64`. Both claims are frozen here: predicate,
counter, kill rule and target. Nothing in this file is re-written after a seat has
measured anything; corrections land as appended amendments that change terms only.

Carried routes this round (round-74 verifier spot-check, `corpus/lessons/round-74-verifier-spotcheck.md`
§Routed items): R1 (stale draft prose landed as a registry claim: the `c74_registry_gap.py`
row promises "five frozen fixtures" against an eight-fixture counter), R2 (`c69_tmp_honour.py`
is registered `gate (live …)` while its own Self-test cell records that it has no self-test
mode), R5 (landed-instrument self-test tallies are unbound: no committed receipt names the
landed file's sha256). R3/R4/R6 are documentation/evidence defects handled by scribe items,
not by these claims.

## § Disclosure — pre-freeze diagnosis

Measured before the freeze, in scratch (`/fast/scratch/hyaku/kake-r75/l1`), never in the lane:

- `SKILL.md` at base carries 28 gate-registry table rows in ten `### Round <N> gate registry
  additions` sections; 16 of them are **live** (`historical` absent from the Kind cell) and
  resolve to 16 distinct instrument files (list in §C1).
- Running each live row's recorded `--selftest` command in a `git clone --shared` of the base
  revision, with a scratch root outside the clone and a fresh `HOME`/`TMPDIR`: 14 exit 0 with the
  recorded shape; `c69_tmp_honour.py` has no self-test mode (argparse error, exit 2) while its
  Kind says `gate`; `c74_registry_gap.py` enumerates five fixture ids and its counter reports eight.
- `corpus/knowledge/instrument-receipts.json` does not exist at base; no committed receipt names
  any population file's sha256.
- Harness limits found and avoided (named so the counters are not tuned to them): a
  `git archive` materialisation breaks counters that resolve their own toplevel through `git`, and a
  scratch directory inside the clone breaks `c59_resolver_cases.py`'s fixture scoring; both are
  excluded by the clone-outside-scratch rule the counters implement.

## § C1 — calibration (owned score 2, the lane's lowest non-retired axis)

**Claim.** The lane's gate registry stops claiming states its instruments do not have: every
live registry row's claim re-derives by execution, `mismatches` 2 → 0 at the round tip.

**Population (16, frozen).** Each live registry row resolves to one instrument file — the Name cell
when it is itself a `.py`/`.mjs` path, else the first `.py`/`.mjs` token of the Entry-command cell,
else of the Self-test cell, else of any cell. The 16:

```
.ufo/waves/round-52/c52_wave_ledger.py
.ufo/waves/round-57/c57_idresolver_gate.py
.ufo/waves/round-58/c58_receipt_rewrites.py
.ufo/waves/round-58/c58_resolver_cases.py
.ufo/waves/round-59/c59_axis_evidence.py
.ufo/waves/round-59/c59_resolver_cases.py
.ufo/waves/round-66/c66_gate_status_hostportable.py
.ufo/waves/round-69/c69_recorded_counts.py
.ufo/waves/round-69/c69_tmp_honour.py
.ufo/waves/round-72/c72_tmp_v2.py
.ufo/waves/round-73/c73_tmp_v3.py
.ufo/waves/round-73/c73_wave_pointers.py
.ufo/waves/round-74/c74_registry_gap.py
scripts/citation_lint.py
scripts/id_resolver.py
scripts/redirect_audit.py
```

Rows whose Kind cell carries `historical` are outside the population: their claims are pinned to a
past revision by their own cells and re-deriving them is a separate bounded pass, named here so the
exclusion is a decision and not an accident.

**Predicate (the sentence the counter implements and the receipt prints).** For every population
file, over the row that is *effective* for it (the last registry row naming it; a row may be
superseded by an appended row, never deleted):

- **E1** a row whose Kind family is `gate` carries a working self-test (`--selftest` exits 0), or its
  Kind cell declares the differential substitute (the word `differential`).
- **E2** when the Self-test cell records an `a/b` tally and names a command, the observed
  `--selftest` pass/total equals it.
- **E3** when the Self-test cell enumerates two or more fixture ids `f<N>`, the observed self-test
  total equals the number of distinct ids named.
- **E4** every `.py`/`.mjs` path token in the row's cells resolves at the measured revision.

`append_only` holds when every live row name present at `--base` is still present at the measured
revision. **`met = (mismatches == 0) and append_only`.**

**Counter.** `.ufo/waves/round-75/c75_row_truth.py`

```sh
python3 -B .ufo/waves/round-75/c75_row_truth.py --root . --revision <rev> --base c9c5e484c533aa65f4374b841a3edcf572ed19a9 --work <scratch dir outside the lane>
```

Output line: `C1v1 revision=<rev> rows=N live=N files=16 mismatches=M classes=… append_only=<bool> met=<bool>`.
Exit `0=met`, `1=not met`, `2=unevaluable`, `64=usage`. The counter clones the measured revision
with `git clone --shared`, keeps every scratch artifact outside that clone, and runs each recorded
command literally with a fresh `HOME`/`TMPDIR`.

**Kill rule.** The claim is not met when any single population file has an open E1–E4 finding, when
`append_only` is false, or when the file list the counter derives differs from the 16 above.

**Target.** `mismatches=0 append_only=true met=true`, exit 0, at the landed tip.

**Base and controls (committed receipts).**

| Receipt | Command | Observed |
|---|---|---|
| do-nothing (base = control) | counter at `c9c5e484` with `--base c9c5e484` | `mismatches=2 classes=E1 E3 append_only=true met=false`, exit 1 — `controls/base-c1-row-truth.txt` |
| cheap content | a sandbox clone with appended junk rows that repeat the two wrong claims | `mismatches=2`, `met=false`, exit 1 — `controls/ctl-cheapcontent.txt` |
| deletion | the `c69_tmp_honour.py` row removed | `mismatches=2 append_only=false met=false`, exit 1 — `controls/ctl-deletion.txt` |

The do-nothing control cannot reach the target: nothing added leaves the two findings open. The
cheap-content control cannot either: adding rows without correcting the effective claims changes
nothing. Deleting the failing row is caught by the append-only conjunct.

**After-state plan.** One appended `### Round 75 gate registry additions` section: a superseding row
for `c69_tmp_honour.py` demoting its Kind from `gate` to `instrument` (the honest label — it has no
self-test mode; adding one to a frozen round counter is out of this round's scope) and a superseding
row for `c74_registry_gap.py` recording the eight fixtures it actually runs. The section also carries
this round's own instrument rows, which must satisfy the same predicate (self-application).

## § C2 — operability (owned score 10, HOLD; capability acquisition)

**Claim.** Every live registry instrument is bound to a committed receipt that re-derives from
committed bytes: `bound` 0 → 16 of the frozen population, `mismatches` 16 → 0.

**Population.** The same 16 files as §C1. The tool derives them independently from `SKILL.md` and
its after-receipt records that its list equals the C1 counter's list (a cross-check between two
independent derivations of one rule).

**Receipt.** `corpus/knowledge/instrument-receipts.json`, schema `instrument-receipts/v1`:
`{schema, revision, date, host, files[]}` with one entry per population file —
`{path, sha256, bytes, selftest_mode}` where `sha256`/`bytes` are of the committed blob at the
receipt's revision and `selftest_mode` is true when the file registers a `--selftest` argument.

**Predicate.** `--check` re-derives, for every population file, the committed blob's sha256 and byte
length at `--revision` and the static `--selftest` registration, and compares them with the receipt
entry. A file counts `bound` only when all three match; a missing entry or a missing receipt file is
a mismatch. **`met = (bound == population) and (mismatches == 0)`.**

**Tool.** `scripts/instrument_receipts.py`

```sh
python3 -B scripts/instrument_receipts.py --root . --revision <rev> --check
python3 -B scripts/instrument_receipts.py --root . --revision <rev> --write --date 2026-11-03
```

Output line: `C2v1 revision=<rev> population=16 bound=B mismatches=M met=<bool>`. Exit `0=met`,
`1=not met`, `2=unevaluable`, `64=usage`. `--selftest` runs isolated fixtures under `--work`.

**Kill rule.** A receipt whose digest, byte count or mode flag does not re-derive is a mismatch; a
receipt for a file outside the population is not counted toward `bound` and is reported separately.

**Target.** `population=16 bound=16 mismatches=0 met=true`, exit 0 at the landed tip.

**Controls.** Base: the receipt file is absent → `bound=0 mismatches=16 met=false`, exit 1. Fabricated
receipt: all 16 paths with digests that do not re-derive → `mismatches=16`; a receipt that drops one
path → `bound=15`. Receipts live under `controls/`.

**Capability row.** `Instrument receipt binding` → evidence `scripts/instrument_receipts.py` (its
`--selftest` receipt) and `controls/after-c2-receipts.txt` → first-working round 75. It enters the
`SCORECARD.md` capabilities table in the same round.

## § Frontier and sources (this round)

- New tier-A row `S443` from `https://raw.githubusercontent.com/in-toto/attestation/main/spec/v1/statement.md`
  (HTTP 200, 2,492 B, sha256 `cbe684a18b812b8b613d9202eb43b2ea24477f91a2ad6ca5be935185a455ebea`,
  opened 2026-11-03): the `subject` field's requirement that each element carry a digest. C2's
  digest-bound receipt cites it. Row enters only after the L1 re-opens the source in-round.
- New knowledge entry `corpus/knowledge/instrument-receipts.md` (provenance trio; cites S443).
- `considerthese/2026-10-26.md` §Part 2 proposal 5 (historical-gate list) is mined at most once:
  the live/historical split C1 freezes is recorded as a `QUALITY.md` criterion citing that file and
  date.
- Assimilation (§10): decided after the connector seat reads `merge/kake/`; `Assimilation: none`
  is an admitted outcome.

## § Wave plan

One v1 wave `w1`, 14 seats, band 8–16 (`scripts/hyaku/ufo-wave-policy.json`): scout 2, executor 4,
scribe 2, reviewer 2, critic 1, mutation-tester 1, connector 1, sentinel 1. Attack seats 4/14
(reviewer ×2, critic, mutation-tester) = 28.6 %. The L1 holds the planner seat (the validator rejects
a planner role). No residual call is planned; a residual seat would count in the round total.

Seats never commit, never push, never run a mutating git/jj command in the lane, never write outside
`/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-75/` and their own scratch root under
`/fast/scratch/hyaku/kake-r75/<seat>/`. The L1 is the only writer of lane files.
