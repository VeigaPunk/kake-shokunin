# Round 96 — claim freeze (declared before data)

Lane: kake, round 96 (hyaku run 15, attempt 1). Round base (round open):
`bde9869144f69c5a459c0d2c93f5135922fe3a8d` (branch tip at round open, remote
equal). Instruments commit: the commit that first carries this directory's
counters and fixtures (recorded in the freeze commit's parent). This freeze is
committed before any wave seat scores a claim; the counters, predicates, kill
rules and targets below are final. The routing is `task.agentModelOverrides`
in `~/.omp/agent/config.yml`; no model is named here.

Continuity duty: the round-95 closure (`corpus/lessons/round-95-verifier-spotcheck.md`,
verdict `rejected-honest-stop`) and the round-95 lesson `## Mistakes`/`## Routed`
were read before declaration. Every routed item R95-1 … R95-8 plus the two
closure-added items are addressed by C1, C2 or the round's non-claim work below:
R95-1, R95-5 and R95-7's C1 items close in C1's successor counter; R95-2
becomes an L0 question (fleet-level decision, recorded, never adopted
silently); R95-3 is a citation (criterion prior art, not a port) landed with
C1's QUALITY criterion; R95-4 is the closure's own duty, not lane work;
R95-6 and R95-7's C2-side items route FORWARD (they name the conditional_eval
line's frozen counter, which this round does not amend — honest routing, not
a repair); R95-8's generated-input digestion is built into C2's counter from
day one. The round-95 spot-check's two new items are honored: trend labels
use the bare protocol vocabulary with bounds in evidence prose, and the
stale `freeze.md` Amendment-A digests are superseded by the round-96 lesson
(filed bytes are never rewritten).

The do-nothing controls are part of each claim's falsification surface and
were executed before this freeze:
- C1: the FROZEN round-95 counter at the same base reads `pins=identity
  met=false` (`controls/base-c1-predecessor.txt`) — the do-nothing lane stays
  uncertifiable, and no successor counter exists without the claimed work.
- C2: `controls/base-c2.txt` reads `candidate=absent … met=false` — a lane
  that builds no revalidation-exchange instrument cannot reach the target.

## Instruments (frozen; digests at `controls/instrument-sha256.txt`)

- `c96_selfassess.py` — C1 counter (strict self-assessment conformance,
  fourth successor, successor to the frozen `c95_selfassess.py`; its bytes
  stay the round-95 scoring instrument and are never amended). Implements
  R95-1 (knowledge entries pinned by PRESENCE via
  `frozen/c1-surfaces.json`, digest `c1caa585…`; lessons keep full-blob
  digests; criteria headings and SKILL-row first cells + path-token floors
  unchanged), R95-5 (NG01/NG08/NG11 close as class rules: for lessons of
  rounds >= 96 the decision vocabulary must be whole words in the Gate BODY,
  heading tokens never count, substring hits do not match) and R95-7's C1
  items (sys.path scrub now drops the working directory and every PYTHONPATH
  entry; the false `python3 -I` docstring sentence is gone). Battery: 22
  defect routes + F2 = 23 refusals, 5 clean admissions, the F1e
  effectful-shadow route, and the predecessor differential, which must admit
  >= 4 of the round-95 fixtures AND all three NG routes (the round-95
  counter's own ReviewC1 receipts show mismatches=0 on those shapes).
- `c96_reval.py` — C2 counter (revalidation exchange, contract v1;
  contract `reval-contract-v1.md`, RFC 9111 §4.3 over supplied values only).
  Population pins `frozen/c2-population.sha256` (digest `d9c8f96e…`): the
  contract, the positive control `frozen/pos-good-reval.py`, six forgeries
  (`frozen/neg-*.py`: blanket-construct, blanket-update, swap-precedence,
  refuse-all, oracle-import, pin-reader) and the 14-mutant population
  `frozen/mutants-reval.json` over the positive-control bytes. The anti-table
  digests hand inputs AND generated inputs (R95-8) and checks the frozen
  subject stems. The sandbox runs subjects under `python3 -I -B` with
  realpath-resolved subject paths and denies `os.exec`/`os.fork` in addition
  to the round-95 denials (hardened against the R95-7 shapes this counter
  owns); R95-6 and R95-7's C2-side items on the conditional_eval line's
  frozen counter route forward untouched.
- Surfaces generator (committed evidence): `gen-surfaces.py`, read-only over
  committed bytes at the base.

## Claim C1 — calibration (score 2, HOLD; lowest owned axis)

**Predicate (one sentence, same in plan, counter and receipt):** at the
measured revision, the successor counter `c96_selfassess.py` reports
`pins=ok`, zero mismatches (E1=E2=E3=E4=E5=0), `battery=23/23`, `admit=5/5`,
`shadow=absent`, `predecessor_admits>=4`, `ng_pred_admits=3/3`,
`self_pin=ok` and `met=true` with exit 0, WHILE the frozen round-95 counter
at the same revision still reports `met=false` — the routed R95-1/R95-5/R95-7
instrument defects are closed only when the same lane state is both
certifiable by the successor and uncertifiable by the predecessor that
false-greens the NG shapes.

- **Target:** predecessor `met=false` (pins=identity) → successor `met=true`
  (pins=ok) at the round's landed tip; base controls already committed
  (`controls/base-c1-predecessor.txt`, `controls/c1-successor-at-base.txt`,
  both at `bde98691…`).
- **Counting command (frozen):**
  `python3 -B .ufo/waves/round-96/c96_selfassess.py --root . --revision <REV> --work <scratch>`
  and the predecessor control
  `python3 -B .ufo/waves/round-95/c95_selfassess.py --root . --revision <REV> --work <scratch>`.
- **Kill rule (declared before data):** the claim fails if the successor
  reports any mismatch, a short or identity pin, a battery route admitted,
  the shadow effect present, a predecessor admission below the floor, any
  NG route the predecessor refuses, or exit != 0 at the landed tip; or if
  the predecessor control is amended in any way (its bytes are frozen at
  digest `8fd27d62…`). Repairs may only edit the surfaces the counter
  audits: SKILL.md table rows (a repaired row keeps its first cell and its
  path-token floor), knowledge entries (presence-pinned; E3 head repairs
  carry a `[r96-correction 2026-11-05]` tag per the append-guard contract),
  QUALITY criteria (a new section cites an existing lesson path), and
  round-96 lesson Gate/Mistakes tables. The declared E3 repair route is an
  in-file head correction — reachable because entries are pinned by
  presence (R95-1); the round-95 defect (a predicate whose pins forbade its
  own repair route) cannot recur.
- **Score delta:** HOLD 2 — a bounded instrument-governance move; the score
  changes only if the non-author closure re-derives it.

## Claim C2 — freshness (score 10, HOLD), capability acquisition

**Predicate (one sentence):** at the measured revision, `c96_reval.py`
reports `candidate=present`, `population=ok` (pins file digest and every
pinned fixture digest), `anti_table=ok` (hand AND generated digests, R95-8),
all 37 hand cases decided as declared, all 120 generated cases decided as
the reference, `forgeries_refused=6/6`, `positive=admitted`,
`mutants=14/14` with no survivor, and `met=true` with exit 0.

- **Target:** `scripts/reval_exchange.py` implements contract v1
  (`reval-contract-v1.md`) and passes the frozen population at the round's
  landed tip. Base control (`controls/base-c2.txt`, at `bde98691…`):
  `candidate=absent hand=0/37 generated=0/120 forgeries_refused=0/6
  positive=refused mutants=0/14 met=false`, exit 1 — the target is
  unreachable without the claimed work.
- **Counting command (frozen):**
  `python3 -B .ufo/waves/round-96/c96_reval.py --root . --revision <REV> --work <scratch>`.
- **Kill rule (declared before data):** the claim fails if any hand or
  generated case disagrees with the reference, any forgery is admitted, the
  positive control is refused, the population drifts (any pinned digest
  mismatch, or the pins file itself drifting from `d9c8f96e…`), an
  anti-table hit is recorded, or a mutant survives. The candidate must
  refuse raw duplicate-key inputs through its real stdin path. The candidate
  may be repaired by its author seat until the counter passes; the counter,
  contract and population are never amended after this freeze (a defect
  found later routes to round 97, as R95-6/R95-7 do now).
- **Score delta:** HOLD 10 — a capability acquisition; the Capabilities row
  enters only through a demonstrated run in the round report; the score
  stays at its legacy ceiling.

## Sourced-claim requirement

C2's knowledge entry rests on a source row opened this round: the RFC 9111
plain-text body re-fetched by the wave's scout (new row S480, scoped to the
§4.3 validation exchange; the retained round-93 body sha `aeb52adb…` is the
comparison digest), with the §4.3.1/§4.3.3 clause quotes located at
retained-body lines 848, 852, 861, 935, 938 and 944. S456 and S476 are
re-read this round as supporting rows; R95-3's chousa criterion 146 is
cited (never ported) alongside C1's QUALITY criterion.

## Non-claim round work (inside the 1-3 claim cap)

- R95-2: the fleet kill-predicate decision is not the lane's to make; an L0
  question is appended (`kake | round-96`) naming the three lane defaults
  (kumitate K43 rerun stability, tabi catalogue-time equivalence, kake
  digest-pinned equivalence receipts), and kake adopts neither silently.
- R95-3: cite chousa round-79 criterion 146 as the prior art for the
  repair-naming rule (a citation in C1's QUALITY criterion; no code ported).
- R95-4: the row-by-row re-read of the 15 repaired SKILL.md rows stays the
  round closure's duty (discharged by the round-95 closure itself —
  spot-check §"R95-4 closure duty"; nothing further owed by this lane).
- R95-6 and R95-7's C2-side items: routed FORWARD to the conditional_eval
  counter's next successor (this round does not amend that frozen counter).
- SKILL.md gate-registry rows for `c96_selfassess.py` and `c96_reval.py`
  (the R94-9 pattern), SOURCES census before→after, mistake mining into
  `corpus/lessons/round-96.md` `## Mistakes`, assimilation: none unless a
  merge/kake row is admitted through the round gate this round
  (the 8-collision state re-derived as evidence), and the round report.
