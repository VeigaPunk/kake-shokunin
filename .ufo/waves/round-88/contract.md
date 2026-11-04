# kake round 88 — frozen contract (v1)

Base `f4479c14813037ad993a49a3dee4028763470f7a` (lane `master` tip at round open,
2026-11-04). Freeze = this file + `c88_defect_queue.py` + `c88_vary.py` +
`vary-cases.json` + `frozen/{base-gate-agreement-ledger.json,
base-cache-current-age.md,base-cache_current_age.py}`. Base control receipts were
written before any production byte changed; nothing in this contract, in the two
counters or in the case set is edited after a seat scores.

Round shape: one v1 wave `w1`, 14 seats inside the run-15 band 8–16. Requested
attack share 4/14 = 28.6 % over the directive's roles {reviewer, critic,
mutation-tester, labrat} (reviewer 2, critic 1, mutation-tester 1). The L1 holds
the canonical planner seat (the validator rejects `planner` as a swarm role);
a bounded planning data-walk rides `ScoutVary`.

Freeze history: v1 froze the C1 counter, the 20-case set and the three base
blobs. v2 (before any production byte changed) added the seeded 200-input
differential population to the C2 counter and restated C2's target. v3 (still
before any candidate was scored and before any production byte changed) fixes
the reference implementation's error precedence: input validation now runs
before the wildcard rule, so a malformed header map is refused even when the
Vary value contains `*` (the v2 reference returned `mismatch` there). No item,
case, threshold, control or target moved.

## C1 — calibration (lowest owned axis, 2 HOLD): the three routed r87 defects

Counter: `.ufo/waves/round-88/c88_defect_queue.py`. One commit is measured; a
claim is one value re-derivable with one command over committed bytes.

Items, each a conjunct over the bytes at the measured revision:

- **D1 ledger-companion.** `corpus/knowledge/gate-agreement-ledger.json` sits in
  `knowledge/`, which CORPUS.md defines as sourced notes; a JSON file cannot open
  with the provenance trio. Routed fix chosen: the *companion entry* alternative —
  `corpus/knowledge/gate-agreement-metadata.md` must open with filled
  `source:`/`verified-at:`/`recheck:` lines, name the ledger path in `source:`,
  quote the ledger's full sha256 (readable only from its bytes), and the ledger
  bytes must stay equal to the frozen base copy.
- **D2 diagnostic-type.** `scripts/cache_current_age.py` must name the offending
  JSON type: float input → exit 1, `invalid_input:`, message names `date_value`
  and `float` and no longer says `boolean`; bool input → names `boolean`; the
  valid input still emits the six integer terms; the tool's own `--selftest`
  stays green.
- **D3 recheck-path.** `corpus/knowledge/cache-current-age.md` must keep a cadence
  in its single `recheck:` line, name no ephemeral token there
  (`/fast/scratch`, `TMPDIR=`, `/tmp/`), carry the offline selftest command in a
  `mktemp -d` form in its body, and preserve every other base line byte-identically
  (only the `recheck:` metadata line may be replaced; other differences must be
  pure insertions).

Predicate: `C1v1 ... open=0 closed=3 met=true` with exit 0 at the carrier.
Before: base `f4479c14` → `open=3 closed=0 met=false`, exit 1
(`controls/base-c1.txt`).
Kill rule: any item still open at the carrier is a miss (honest stop); no item,
conjunct or target is rewritten after scoring.
Controls committed: counter selftest 11/11 (one green tree, one mutant per item,
a junk-prose tree that fixes the prose but not the behavior and leaves 1 open,
edited/deleted-line mutants); counters read only lane bytes, never receipts.
Limits: D1 and D3 are textual apart from the sha256 binding and the behavioural
D2 item — a tree that writes the right prose and ships the real tool passes them,
so the non-author closure remains the catch. This closes three recorded defects;
it does not certify the ledger's decisions.

## C2 — freshness (10 HOLD): bounded capability, conservative Vary-match reader

Counter: `.ufo/waves/round-88/c88_vary.py` over the frozen
`vary-cases.json` (20 cases, sha256 printed in every receipt).

Predicate: the candidate CLI at `scripts/vary_match.py` scores `frozen=20/20` and
`random=200/200`, `met=true`, exit 0, with `frozen cases_sha256` and
`random_sha256` equal to the frozen set and the seeded batch printed in every
receipt. A case passes on exit code, on exact stdout verdict (`match`/`mismatch`)
with empty stderr, or — for refused input — on exit 1, empty stdout and an
`invalid_input:` stderr prefix.
The random population is generated inside the counter from a fixed seed and
scored against the counter's own reference implementation of the declared
profile; that reference must reproduce all 20 hand-labelled frozen verdicts
(counter selftest), so the generated batch cannot drift from the spec-derived
one, and a lookup table keyed on known inputs cannot pass it.
Before: base `f4479c14` → tool absent, `frozen=0/20 random=0/200 met=false`,
exit 1 (`controls/base-c2.txt`).
Kill rule: any shortfall at the carrier is a miss; the case set, the seed, the
generator and the reference are not edited after scoring; there is no partial
credit and no target narrowing.
Controls committed: constant-`match` stub `7/20 + 67/200`, constant-`mismatch`
stub `9/20 + 109/200`, always-`invalid` stub `4/20 + 24/200`
(`controls/ctl-c2-constant-*.txt`), counter selftest 17/17 including those
scores, the reference-vs-frozen agreement and a silent-failure stub at 0/20.

Profile (declared, bounded): the reader implements RFC 9111 §4.1's match rule
conservatively. Field names compare ASCII case-insensitively; multiple field
lines combine in order with `, `; values compare byte-identically after trimming
leading/trailing SP/HTAB; a field absent from both requests matches, absent from
one it does not; any `*` member always fails. It never applies field-specific
normalization (no value case-folding, no reordering, no internal whitespace
folding), so a `match` verdict is always produced by transformations §4.1
permits while a `mismatch` may be more conservative than a field-specific rule.
Adapter precedence is declared: input validation runs before the wildcard rule,
so a malformed header map is refused even when the Vary value contains `*`.
Not claimed: cache-key construction, storage, revalidation, freshness, serving
or any browser behaviour; no live surface is asserted clean.

## Sourced claim and frontier

C2's knowledge entry rests on the SOURCES row opened this round for RFC 9111
§4.1; its Gate records the URL, the access date and a ≤25-word located quote.
The `merge/kake` assimilation package still collides on eight registry ids
(re-derived this round), so the round reports `Assimilation: none`.

## No-harm and scope

Production bytes this round: the D2 diagnostic line in
`scripts/cache_current_age.py`, the D3 metadata line plus pure additions in
`corpus/knowledge/cache-current-age.md`, new files `scripts/vary_match.py`,
`corpus/knowledge/vary-matching.md`, `corpus/knowledge/gate-agreement-metadata.md`,
the lesson, SOURCES/LOG/SCORECARD appends and the round-88 wave evidence. No
existing script other than the D2 line changes; the frozen r87 instrument and
its fixtures stay untouched; freshness is not re-measured live; publishing,
accounts and deployment stay operator-owned.

## Errata (appended after the wave; the sentences above are not rewritten)

- The v3 paragraph's "No item, case, threshold, control or target moved" is
  accurate for the C1 items, the 20 hand cases, the thresholds, controls and
  targets, and inaccurate for the seeded population: three labels flipped
  (`r53`, `r150`, `r193`, `mismatch` → `invalid`) and the population digest moved
  from `004a8eb7…` to `52714a5f…`. The controls were re-run and carry the new
  digest. `corpus/lessons/round-88.md` records the correction.
- The v2→v3 amendment happened while the wave was live (dispatch 15:52:15, v3
  15:58:05). No C1 scoring preceded it; two seats re-read the contract and one
  measured the candidate at 197/200 under v2 and 200/200 under v3. Freeze and
  dispatch are meant to be ordered, not interleaved.
