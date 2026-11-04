# Round 91 freeze — kake (L1 KakeR91)

Frozen before any after-state data. Base `5b20af16661040f383e9e84f85b838619857cb14`
(lane `master` at round start; `ls-remote` equal, `jj-lane.sh state` ahead=0 behind=0).
No candidate tool, mutation receipt, replay receipt or new registry row existed when the
controls below ran.

## Claims (2; distinct axes; causally separable)

### C1 — calibration (lowest owned non-retired axis, 2 HOLD)

The routed round-90 instrument defects close on committed bytes: **R90-A** (defect-queue
shape — the round-90 counter admitted a stale receipted revision, a case-variant token and
a receipt with no execution), **R90-B** (the tip conformance gate was never re-mutated
after its hardening) and **R90-C** (`run_controls.sh` stopped replaying after the
round-90 relocation). R90-A's gate half is discharged by the C2 instrument's own forgery
battery and is reported under C2, not counted here.

- Counter: `.ufo/waves/round-91/c91_defects.py` (sha256
  `5239c7f808095e5e146bc57f72bdaa00ce2cab20fdd7cc1b0b2d201ddec5629b`).
- Command: `python3 -B .ufo/waves/round-91/c91_defects.py --root . --revision <REV> --work <scratch>`
- Predicate (the same sentence as the counter's `met`): **met ⇔ open == 0 over items
  A, B, C**, where
  - **A** = the successor counter is tracked at the revision, its own `--selftest`
    prints `selftest 6/6`, and its self-invoked battery over four fixtures built from
    the measured revision reports: FA (mutation receipt naming the stale round-90 gate
    digest) leaves item B open, FB (receipt with a case-variant token) leaves item B
    open, FC (a script that prints success and exits 3) leaves item C open, and FD (all
    three genuinely closed) leaves no item open.
  - **B** = `.ufo/waves/round-91/integration/mutation-tip.txt` first line is
    `gate_sha256=<64 hex> mutants=<N> killed=<K> survivors=<S> met=true`, the digest
    equals the `scripts/cache_key_conformance.py` blob at that revision, N ≥ 20,
    K ≥ 18, S == N − K, and at least N distinct `M<nn> ` mutant lines follow.
  - **C** = `.ufo/waves/round-90/controls/run_controls.sh` at the revision copies only
    the relocated `.ufo/waves/round-90/inherited/baseclean.out` (never the lane-root
    copy), takes its root from `${LANE:-…}`, and — replayed by the counter on a scratch
    clone at that revision with `ONLY=c1` — exits 0 with a final line `controls ok K/K`,
    K == N ≥ 9.
- Before (base): `open=3 closed=0 met=false`, exit 1 (`controls/base-c1.txt`).
- Target after: `open=0 closed=3 met=true`, exit 0, at the measured carrier.
- Kill rule: any item open at the carrier → C1 not met, reported as an honest stop,
  never narrowed after data.

### C2 — operability, capability acquisition: a stored-response reuse decision instrument

The lane gains `scripts/stored_reuse.py`, an offline decision over supplied integer
seconds that answers one of `reuse`, `revalidate`, `serve-stale`, `must-revalidate-fail`,
`not-storable`, `heuristic-undecided`, `only-if-cached-miss` under
`.ufo/waves/round-91/c2-contract.md` (21 clauses), refusing malformed input with
`invalid_input:` and exit 1.

- Counter: `.ufo/waves/round-91/c91_reuse.py` (sha256
  `0cd610426896fc76b4913c907d83b95d22c7a66c4ecf2da8fc4fc9ecf21ab660`); population pins
  `.ufo/waves/round-91/frozen/c2-population.sha256` (sha256
  `033b6103303d33690c4a6d02b04df36ba86b3b4f1d1e18aa5e267cb9b95084c8`, named as
  `PINS_SHA` inside the counter).
- Command: `python3 -B .ufo/waves/round-91/c91_reuse.py --root . --revision <REV> --work <scratch>`
- Contract: `.ufo/waves/round-91/c2-contract.md` (sha256
  `faa91e096f4f9ae062d14402bbad5615c9ace8cfb2e820c519cb5cd01d768fe4`).
- Predicate: **met ⇔ candidate present ∧ population pins match ∧ anti_table ok ∧ hand
  45/45 ∧ generated 120/120 ∧ all five frozen forgery subjects refused**, where the
  anti_table check refuses a candidate whose source contains a hand-case input digest or
  a forgery stem, and the forged subjects are a pin reader, an allowlist, a blanket
  refusal, a blanket admit and a lookup table over the published hand cases.
- Before (base): `candidate=absent … met=false`, exit 1 (`controls/base-c2.txt`).
- Target after: `hand=45/45 generated=120/120 forgeries_refused=5/5 anti_table=ok
  population=ok met=true`, exit 0, at the carrier.
- Kill rule: any hand or generated case decided differently, any forgery admitted, or
  any drift/hit → not met; reported.
- Sourced: the request-directive clauses rest on the RFC 9111 §5.2.1 row opened this
  round (S469), the lifetime order on §4.2.1 and the stale-serving permission on §4.2.4.

## Controls executed before this freeze (`controls/run_controls.sh`)

Script under test (C1 item C): `.ufo/waves/round-90/controls/run_controls.sh` (sha256
`00e339b8266eae324f7d5d56a3deabbaa1df1b7488d72944bad8d2dc3248c040`).

`controls/ctl-c1.txt`: do-nothing at base → `open=3 closed=0 met=false`; junk fixture
(the frozen bytes committed, a zero-digest receipt, a script that prints success and
exits 0 without copying the relocated file) → `open=3 closed=0 met=false`. Both are
do-nothing-class controls: the cheapest thing that skips the claimed work does not reach
the target.

`controls/ctl-c2.txt`: do-nothing at base (no candidate) → `met=false`; each of the five
frozen forgery subjects scored as the candidate → `met=false`; the reachability control
(the counter's own reference wrapped, `.ufo/waves/round-91/controls/reference-candidate.py`)
→ `met=true`, which shows the contract is implementable and the battery satisfiable. The
reachability control is a control, never the shipped tool and never a positive control
for the claim.

No positive control exists for either claim before the work lands: a conforming tool and
a real mutation receipt are the claimed work. C1's item A carries its own positive
control at measurement time (fixture FD), built from the carrier's own bytes.

## Separability

C1 reads `.ufo/waves/round-91/c91_defects.py`, `.ufo/waves/round-91/integration/mutation-tip.txt`,
`.ufo/waves/round-90/controls/run_controls.sh` and the `scripts/cache_key_conformance.py`
blob. C2 reads `.ufo/waves/round-91/{c2-contract.md,c91_reuse.py,frozen/}` and the
candidate `scripts/stored_reuse.py`. Neither counter reads the other's outputs, receipts
or files, and each can land alone: C2 without the mutation receipt, C1 without the tool.

## Round shape

One v1 wave, 13 seats (policy band 8–16): scout 2, executor 5, scribe 1, reviewer 2,
mutation-tester 1, critic 1, connector 1 → attack seats 4/13 = 31 %, connector seats 1.
The L1 holds the canonical planner seat; ScoutGround carries the bounded planning
data-walk.
