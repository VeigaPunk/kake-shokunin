VERDICT: **C1 is not a calibration measurement — a single fabricated receipt file reaches `met=true`; C2 is causally separable and contract-implementable, but `met=true` is also reached by importing the counter's own reference, and its `anti_table` conjunct has no working frozen subject.**

# CriticClaims — round 91: adversarial review of the two frozen claims

Seat: critic (leaf). Lane root `/home/vgpnk/Projects/shokunin/kake-shokunin` (LANE).
Base of all readings: freeze commit `f4fff130a52ae6de49af5de7d568d2ee320ebfb0`.
Frozen instruments were read, never edited; every reading below is on committed bytes in a
scratch clone (`git clone -q --shared LANE $S/clone` then `checkout -q --detach <rev>`),
Python 3.14.8, no network, no installs. Receipts: `.ufo/waves/round-91/w1/CriticClaims/`.
The lane worktree carried other seats' uncommitted edits during this read
(`git status --porcelain` → `M .ufo/waves/round-91/controls/{ctl-c1,ctl-c2}.txt`,
`run_controls.sh`, `M PROVINCE.md`, `M SKILL.md`); none of it was used or touched — every
reading names a revision.


## (a) Separation — VERDICT: holds in both directions

Read both counters for cross-reads (`probes.txt` §3):

- `c91_defects.py` path tokens: its own file, `.ufo/waves/round-91/integration/mutation-tip.txt`,
  `scripts/cache_key_conformance.py`, `.ufo/waves/round-90/controls/run_controls.sh`,
  `.ufo/waves/round-90/inherited/baseclean.out`.
- `c91_reuse.py` path tokens: `scripts/stored_reuse.py`,
  `.ufo/waves/round-91/frozen/c2-population.sha256`, the five `frozen/neg-*.py`.

Intersection is empty: neither counter reads the other's instrument, receipts, pins or
artifacts. Cheapest counter-example, both directions, one clone:

| fixture | revision | command | reading | exit |
|---|---|---|---|---|
| R1 receipt only, no candidate | `8466e637` | `c91_defects.py --root . --revision <rev> --work <w>` | `items=3 open=0 closed=3 met=true` | 0 |
| R1 same rev, C2 | `8466e637` | `c91_reuse.py --root . --revision <rev> --work <w>` | `candidate=absent … met=false` | 1 |
| R2 candidate only, no receipt | `d8a0b455` | `c91_reuse.py …` | `hand=45/45 generated=120/120 … met=true` | 0 |
| R2 same rev, C1 | `d8a0b455` | `c91_defects.py …` | `items=3 open=1 closed=2 met=false`, open `["B"]`, reason `mutation receipt absent` | 1 |

Receipts `c1-R1-receipt-only.txt`, `c2-R1-receipt-only.txt`, `c2-R2-candidate-only.txt`,
`c1-R2-candidate-only.txt`; fixture commits in `revs.txt`, recipe `build_fixtures.sh`.

Caveats that are not separation defects: C1's item A runs C1's own file (self-reference, not
cross-claim), and both claims' instruments sit in the same freeze commit, so "can land alone"
is only true of post-freeze work.

## (b) Do-nothing reachability — VERDICT: C1 is reachable by fabrication; C2 is reachable by oracle import

All readings from the same clone, each with `--work` under my scratch root:

| shortcut | revision | reading (line 1) | exit | receipt |
|---|---|---|---|---|
| **C1**: only `integration/mutation-tip.txt` written, digest = `sha256sum` of the gate blob at the rev, 21 fabricated `M<nn>` lines, no mutant applied or run | `8466e637` | `C1v91 … items=3 open=0 closed=3 met=true` | **0** | `c1-R1-receipt-only.txt` |
| **C2**: wrapper of `scripts/cache_current_age.py` + constant `{"decision":"reuse","freshness_lifetime":60,"current_age":30}` | `4549f61d` | `hand=10/45 generated=0/120 … met=false` | 1 | `c2-R5-constant-wrapper.txt` |
| **C2**: 20-line shim importing the counter's reference from `.ufo/waves/round-91` by absolute path | `70316122` | `hand=45/45 generated=120/120 forgeries_refused=5/5 anti_table=ok population=ok met=true` | **0** | `c2-R6-oracle-import.txt` |
| **C2**: frozen `neg-pin-reader.py` as the candidate | `7f6cbe73` | `hand=0/45 generated=0/120 … met=false` | 1 | `c2-R7-pin-reader.txt` |
| **C2**: byte-copy of the counter's reference block (`controls/reference-candidate.py`) | `d8a0b455` | `hand=45/45 … met=true` | **0** | `c2-R2-candidate-only.txt` |
| **C2**: digest-keyed lookup table over the hand cases | `fffb758f` | `anti_table=hit … met=false` | 1 | `c2-R8-digest-table.txt` |

Notes that matter for the claim:

1. **C1's shortcut is one `printf`.** `gate_sha256` is `sha256sum scripts/cache_key_conformance.py`
   at the revision; `mutants=21 killed=20 survivors=1` satisfies the floor and the arithmetic;
   the 21 `M<nn> ` lines are text. Nothing in the counter executes a mutant. The class R90-A
   names — "a receipt with no execution" — is closed for the *round-90* counter and
   reintroduced by this one.
2. **The wrapper never had a chance.** `scripts/cache_current_age.py:20` requires
   `date_value`, `request_time`, `response_time`, `now`; the C2 input shape has none of them,
   so the wrapper either refuses or ignores its own delegation. It reads `hand=10/45`, the
   refusal-only signature.
3. **The oracle import is the cheapest C2 shortcut.** The counter extracts the candidate to
   `tree/scripts/stored_reuse.py` and its generated population is decided by
   `reference()` in the same file (`gen_expected = [(inp, reference(inp)) …]`), so an import
   of that function is correct by construction; `anti_table` only looks for hand-case input
   digests and forgery stems, not for a read of the grader.
4. **The pin reader is refused**, but for the wrong reason to count as coverage: it looks
   under `cwd` and its own directory (`neg-pin-reader.py:7-8`), never at
   `../.ufo/waves/round-91/frozen/`, which is exactly where the pins are (see F6).

## (c) Axis labels — VERDICT: C2 is operability (freshness would be wrong); C1's "axis" is really a scored sub-axis

- **C2 = operability, capability acquisition: correct.** The lane's convention labels a new
  offline instrument "operability 10→10 (HOLD); capability entered" (`SCORECARD.md` round-22
  and round-46 claim rows). Freshness is the corpus's standing-claim re-verification
  (`SCORECARD.md:18`, `corpus/knowledge/freshness-{pins,sidecar}.json`,
  `scripts/freshness-sweep.mjs`); C2 ships no source-backed entry and no recheck receipt, and
  `PROVINCE.md:30` reads "Ground moves to Core only with source-backed entries and a gate".
  C2 would be freshness only if it moved reuse/serving ground into core, which the freeze
  does not claim (and should not: `SCORECARD.md:5600` still lists "storage, revalidation,
  freshness and serving" as frontier).
- **C1's label is imprecise, not wrong.** `SCORECARD.md:3-4` says "Axes owned by this lane:
  **operability + freshness**, plus calibration as a round-54 evidence-backed *sub-axis*
  addition", and `SCORECARD.md:114-115` says "The two owned axes themselves are NOT retired".
  So "the lowest owned non-retired axis, 2 HOLD" should read "the lowest scored sub-axis
  (2, HOLD)". The substance — calibration is the lowest-scored, non-retired row and its
  subject is instrument trustworthiness — is right.

## (d) Sizing — VERDICT: C1 is bookkeeping-only; C2 is a new decision surface, but its `met` does not establish acquisition

- **C1: yes, bookkeeping-only.** `c1-R1-receipt-only.txt` is the whole proof: one file, no
  execution, `met=true`. Two of the three items were already closed by the freeze commit
  itself — `c1-freeze-state.txt` reads `items=3 open=1 closed=2 met=false`, open `["B"]`
  (`mutation receipt absent`), against `controls/base-c1.txt` `open=3` at the base. So the
  round's remaining C1 deliverable is a prose receipt whose numbers the counter cannot check.
- **C2: not a re-skin.** The deciding sentence is `corpus/README.md:710-711` (round-88
  frontier step): "it does not claim cache-key construction, storage, revalidation,
  freshness, serving or browser behaviour" — the vary-match reader disclaims exactly the
  decision C2 makes. `PROVINCE.md:709-710` does the same for `cache_key.py` ("This is the
  construction half of RFC 9111 §4.1 only. Storability, reuse, revalidation, freshness,
  serving and browser behaviour stay frontier"), and `cache_current_age.py` is arithmetic
  only with a different input shape. So the surface is new. What is *not* established is
  acquisition: F6 shows a 20-line import of the grader's oracle reads `met=true`.

## (e) The QUALITY bar — VERDICT: C1 fails condition (2) for conjunct A; C2 fails it for `anti_table` and `population`, and fails the capability addendum

Criterion: `corpus/QUALITY.md:1761` §Round 90 — a counter earns `met` only after (1) a
do-nothing control `met=false`, (2) "at least one forgery per conjunct, each leaving that
conjunct open for the stated reason", (3) a positive fixture `met=true`; and "a capability
counter additionally scores a frozen population of known non-conforming subjects under
renamed, nonce-altered copies".

- **C1.** (1) ✓ `controls/ctl-c1.txt` do-nothing `open=3 … met=false`. (3) ✓ FD fixture
  `open=0 closed=3 met=true` in every run. (2) **✗ for A**: R4 — the successor counter at
  the revision with `item_a` replaced by `return True, ""`, plus a plausible receipt —
  reads `items=3 open=0 closed=3 met=true`, exit 0 (`c1-R4-vacuous-A.txt`). The frozen
  battery only leaves B open (FA, FB) and C open (FC); nothing leaves A open through A's
  own mechanism (`ctl-c1.txt`'s junk fixture opens A only via "positive fixture not met").
- **C2.** (1) ✓ `controls/ctl-c2.txt` candidate absent. (3) ✓ blanket-refuse reads
  `hand=9/45` (`ctl-c2.txt`) and the reachability control reads `met=true`. (2) **✗**:
  no frozen subject trips `anti_table` (`probes.txt` §1: 0 digest hits over
  `frozen/neg-hash-table.py`; every reading in `ctl-c2.txt` prints `anti_table=ok`), and no
  control leaves `population=drift` open. Hand/generated/`forgeries_refused` are covered.
  Capability addendum **✗**: the five subjects are scored at their published paths and
  bytes, not "renamed, nonce-altered copies".

## Findings

### F1 — C1 item B is prose: a fabricated receipt reaches `met=true` (high)

Counterexample: `c1-R1-receipt-only.txt` — `8466e637`, `open=0 closed=3 met=true`, exit 0,
from one written file with no mutation performed. Command:
`python3 -B .ufo/waves/round-91/c91_defects.py --root . --revision 8466e637 --work <w>` in
the clone. This is the R90-A class ("a receipt with no execution") inside the successor.
**Smallest safe correction:** have the counter *perform* the mutation — derive N ≥ 20
single-point mutants from the gate blob at the revision, run the gate's own matrix on each,
and require the observed killed count; accept the committed receipt only as a cross-check of
that observed line (QUALITY's "a gate's receipt is re-derived, never trusted").

### F2 — C1 item A cannot say no, and the counter never checks its own frozen digest (high)

`c1-R4-vacuous-A.txt`: a revision whose `c91_defects.py` has `item_a` stubbed reads
`met=true`, exit 0. The battery's FA/FB/FC discriminate B and C correctly at every revision
I ran (FA/FB → `open:["B"]`, FC → `open:["C"]`, FD → `open:[]`), so the gap is specific to A.
The counter also never compares its own blob to the freeze digest
`5239c7f808095e5e146bc57f72bdaa00ce2cab20fdd7cc1b0b2d201ddec5629b`; `item_a` checks only
`ls-tree` presence and the extracted copy's `--selftest` text, which a stub keeps intact.
**Smallest safe correction:** add a fifth fixture FE whose successor counter's `item_a` is
stubbed and require `open` to contain A; and reject a revision whose `c91_defects.py` blob
differs from the freeze digest (a frozen instrument should be pinned, not merely present).

### F3 — C1's "before" overstates the round's work (medium)

`controls/base-c1.txt` (`open=3`) is the base, but the freeze commit already reads
`open=1 closed=2` (`c1-freeze-state.txt`, my run). Items A and C close on bytes committed
before any data; the claim's after-state is one receipt. The freeze is honest about the base
it names, but "the routed defects close" then means one unverifiable file, not three closures.
**Smallest safe correction:** state the freeze-state reading as the round's before-state, or
drop A and C from C1 and carry them as pre-freeze instrument work.

### F4 — C1 item C's text clause is bypassable; only the replay is real (low)

`probes.txt` §2: the forbidden regex misses `"$LANE"//baseclean.out`, `"$LANE"/"baseclean.out"`,
`$LANE/baseclean\.out`, `"${LANE}"/./baseclean.out` — all resolve to the lane-root file in
bash, and `run_controls.sh` runs under `set -u` without `-e`, so a failing `cp` does not stop
it. The replay (`controls ok 9/9`, observed in every run) is the substantive check and it is
sound. **Smallest safe correction:** drop the regex and assert the copied path resolves to the
inherited file at replay time (e.g. compare `realpath` of every `baseclean.out` operand), or
state the text clause as advisory.

### F5 — the fifth C2 forgery is invalid Python: `anti_table` is exercised by nothing (high)

`frozen/neg-hash-table.py` carries 15 JSON `null` literals (`probes.txt` §1:
`null_literal_occurrences=15`); every invocation dies at module import
(`NameError: name 'null' is not defined`, exit 1) before reading stdin. Its "refusal" in
`forgeries_refused=5/5` is a crash, not the counter's checks, and its source keys raw JSON
rather than the 16-hex digests `anti_table` looks for (`anti_table_digest_hits_over_frozen_hash_table=0`).
`controls/make-neg-hash-table.py` produced it with `json.dumps(rows, indent=0)` — JSON
literals emitted into Python source. The check itself works: R8, a digest-keyed table, reads
`anti_table=hit … met=false` (`c2-R8-digest-table.txt`).
**Smallest safe correction:** rebuild the subject with `repr(rows)` (or map `None`→`None`),
pin the rebuilt file, and add a control receipt that scores it; until then the `anti_table`
conjunct is unmeasured and QUALITY condition (2) is unmet for it.

### F6 — the frozen pins are reachable from every scored subject, contradicting the counter's own docstring (medium)

`c91_reuse.py:10-12` states the pins "are never written into any directory a scored subject can
reach". `extract()` writes them to the same tree as the candidate, so
`tree/scripts/../.ufo/waves/round-91/frozen/c2-population.sha256` exists
(`extract-check`: `PINS_REACHABLE_FROM_CANDIDATE=yes`), and the behavioural probe R9 — blanket
admit that refuses only when the pins are reachable — reads `hand=9/45` (`c2-R9-pin-reach.txt`)
against blanket-admit's `hand=0/45` (`ctl-c2.txt`), i.e. the subject read the pins and flipped
its behaviour. A frozen forgery that hashes itself against the pins can therefore make
`forgeries_refused` vacuous. **Smallest safe correction:** extract the candidate alone (or to
a sibling root with the pins outside it), and score subjects under renamed copies as
QUALITY's capability addendum already requires.

### F7 — C2's `met` is reachable by importing the grader (high)

`c2-R6-oracle-import.txt`: `hand=45/45 generated=120/120 anti_table=ok population=ok met=true`,
exit 0, from a 20-line shim with an absolute-path `import c91_reuse`. The byte-copy variant
(R2) reads the same. `anti_table` does not look for a read of `.ufo/waves/round-91/`, and the
generated population is decided by the same `reference()`, so equality is by construction.
The shipped tool would depend on a frozen wave file — delete the wave directory and the
instrument dies, which is the opposite of "capability acquisition".
**Smallest safe correction:** score the candidate against an oracle held outside the
extracted tree (or a second, independently written oracle), and refuse a candidate whose
source reaches into `.ufo/waves/` (the round-90 C2 gate already had the sandbox that would
have caught this).

### F8 — C2 has no control for `population` drift and none for a renamed subject (medium)

`ctl-c2.txt` covers do-nothing and five forgeries; every reading prints `population=ok`, and
no control leaves `population=drift` open. The five subjects are scored at their published
paths, not as "renamed, nonce-altered copies" (`corpus/QUALITY.md:1761` capability
addendum). **Smallest safe correction:** add a pins-drift fixture (one pinned file's bytes
changed) and score each forgery under a neutral filename in a fresh directory.

### F9 — reported, not scored: C2's contract-to-reference drift guard is one-sided (low)

`c91_reuse.py` exits 2 if `reference()` disagrees with a hand case, which catches
contract/oracle drift in one direction only: a contract clause that both the case table and
`reference()` omit is invisible. That is the shape of round-90's Mistakes row 5 (a hand case
deciding a point the contract leaves open). No instance found this round — stated as a limit.

## What I did not do (honest limits)

- I did not run either counter's `--selftest` as a claim of anything; the frozen `selftest
  6/6` text is a parser tally (`parse_receipt` cases), not evidence about items A, B or C.
- I did not verify any round-91 mutation receipt: none exists at `f4fff130`
  (`.ufo/waves/round-91/integration/` is empty). R90-B is unmeasured until one lands, and
  F1 says the landed one will still be unverifiable prose.
- My "conforming" candidate in R2/R3 is the counter's own reachability control
  (`controls/reference-candidate.py`); that is deliberate — it shows the battery is
  satisfiable and that satisfaction is not evidence of independence.
- I did not test the C2 contract for clause completeness against RFC 9111; that is a
  different seat's assignment.
- Scratch `/fast/scratch/hyaku/kake-r91/CriticClaims/` was deleted after the receipts were
  copied; every receipt cited here is committed-adjacent evidence under
  `.ufo/waves/round-91/w1/CriticClaims/` and every reading names its revision and command.
- The fixture revision ids (`8466e637`, `d8a0b455`, `3b3e08d8`, `4549f61d`, `70316122`,
  `7f6cbe73`, `fffb758f`, `d4106e3b`) are **ephemeral**: they lived only in the deleted
  scratch clone and do not resolve in LANE. `build_fixtures.sh` in the receipt directory
  rebuilds every fixture from `f4fff130` (re-point `S`); the readings are the evidence,
  the hashes are not.

## Routed (lane-internal, for the round's routed list)

- **R91-X1** (F1): C1 item B accepts a fabricated receipt; the successor counter reintroduces
  the R90-A "receipt with no execution" class. Re-derive the mutation at measurement time.
- **R91-X2** (F2): C1 item A is unexercised by its own battery and the counter does not pin
  its own frozen digest; a vacuous `item_a` reads `met=true`.
- **R91-X3** (F5): the frozen C2 forgery `neg-hash-table.py` is invalid Python (15 `null`
  literals) and the `anti_table` conjunct has no working subject; `make-neg-hash-table.py`
  emits JSON into Python source.
- **R91-X4** (F6, F7): the frozen pins are reachable from the scored tree (docstring false),
  and a 20-line oracle import reads `met=true`; C2's `met` does not establish acquisition.
- **R91-X5** (F8): no `population`-drift control and no renamed/nonce-altered subject scoring
  (QUALITY round-90 capability addendum unmet).
- **R91-X6** (F4, F3): item C's text clause has four bypass forms; C1's before-state is the
  base, while the freeze commit already reads `open=1`.
