# Round 98 — CriticClaims attacks (C1 calibration, C2 freshness, freeze predicate)

Seat: CriticClaims (leaf, no dispatch). Lane tip read: `master` = `7838981e`. Round base `e51328b6`, repair `4446ce21`, freeze `c3eace8b`, fleet pin `f8674006`.
Instrument digests re-verified before attacking (`controls/instrument-sha256.txt`): `c98_captable.py efd59857…`, `c98_stale.py e0331e56…`, `frozen/pos-oracle.py bfb48d81…` — all match. Nothing in the lane or fleet was mutated. All attacks ran in fixture clones (`git clone --shared`, toplevel asserted equal to the fixture dir, identity `CriticClaims@example.invalid` via `-c`) and in scratch; the scratch seat directory is deleted after these receipts were copied here.

Tools: none installed or upgraded. Used `git` (read-only on LANE/fleet; fixture-only commits), `python3` stdlib, and the counters' public CLIs.

Receipts (flat, in this directory): `receipt-c1-attacks.log`, `receipt-c1-attacks-results.txt`, `receipt-c1-cheap.log`, `receipt-c1_attacks.py.txt`, `receipt-c1_cheap.py.txt`, `receipt-c2-build.log`, `receipt-c2-run.log`, `receipt-c2-counter-results.txt`, `receipt-c2_build.py.txt`, `receipt-c2_run.py.txt`, `receipt-cand-K*.py.txt` (the candidate sources).

## 0. Controls reproduced (not re-stamped)

| check | command | output line | rc |
|---|---|---|---|
| C1 do-nothing (base) | `python3 -B .ufo/waves/round-98/c98_captable.py --root <LANE> --revision e51328b6… --fleet-revision f8674006…` | `entries=48 rows=14 matched=8 unlisted=40 unbacked=6 mismatches=46 met=false` | 1 (matches `controls/base-c1.txt`) |
| C1 repair | same, `--revision 4446ce21…` | `entries=48 rows=48 matched=48 unlisted=0 unbacked=0 mismatches=0 met=true` | 0 |
| C1 at current tip | same, `--revision 7838981e…` | `entries=48 rows=48 matched=48 unlisted=0 unbacked=0 mismatches=0 met=true` | 0 |
| C1 selftest | `c98_captable.py --selftest` | `selftest 16/16` | 0 |
| C2 do-nothing (base) | `python3 -B .ufo/waves/round-98/c98_stale.py --root <LANE> --revision e51328b6… --work <scratch>` | `candidate=absent hand=0/60 generated=0/240 refusals=0/0 seed=- met=false` | 1 (matches `controls/base-c2.txt`) |
| C2 selftest | `c98_stale.py --selftest` | `hand-oracle 60/60 generated-refusals=44/240 …` / `selftest ok` | 0 |
| C2 positive oracle slot (`frozen/pos-oracle.py`) | `c98_stale.py --candidate-file frozen/pos-oracle.py --work <scratch> --seed 1` | `candidate=present sha256=bfb48d81… hand=60/60 generated=240/240 refusals=36/36 seed=1 met=true source=candidate-file` | 0 |

Both counters reproduce their controls exactly. The "do-nothing" control scores `mismatches=46` (C1) and `candidate=absent` (C2), so the base is correctly unmet.

## 1. C1 — calibration counter attacks (fixture clones at `4446ce21`, one commit per attack)

Command per attack (driver `receipt-c1_attacks.py.txt`, one edit to `SCORECARD.md` in a clone, then):
`python3 -B .ufo/waves/round-98/c98_captable.py --root <FX> --revision <new> --fleet-revision f8674006… --fleet /home/vgpnk/Projects/shokunin`

| F-id | attack (edit to the `## Capabilities` table) | output line (line 1) | rc | verdict on the counter |
|---|---|---|---|---|
| F-C1-1 (A1) | key word-prefix extension: row `Coverage-index calibration counter` renamed `Coverage-index calibration counter with automatic CDN cache purge` (admitted r97 entry is `Coverage-index calibration counter (.ufo/waves/round-97/c97_index.py)`, a 3-word key that `key_ok` accepts as a prefix of the longer row key) | `entries=48 rows=48 matched=48 unlisted=0 unbacked=0 mismatches=0 met=true` | 0 | **ESCAPE**: a never-admitted capability (automatic CDN cache purge) is backed by a closed entry |
| F-C1-2 (A2) | same as F-C1-1 with the pipe written `\|` in the name cell (`… counter \| with automatic CDN cache purge`) | `entries=48 rows=48 matched=48 unlisted=0 unbacked=0 mismatches=0 met=true` | 0 | **ESCAPE** (escaped-pipe spelling of the same key collision) |
| F-C1-3 (A3) | existing unrelated evidence: row `Conservative Vary-match reader` evidence `` `scripts/vary_match.py` `` → `` `SCORECARD.md`; scripts/vary_match.py `` (`SCORECARD.md` exists at the revision; the entry path is named in the row line, so S passes) | `entries=48 rows=48 matched=48 unlisted=0 unbacked=0 mismatches=0 met=true` | 0 | **ESCAPE**: P accepts any existing backticked path, and S accepts the entry path anywhere in the line |
| F-C1-4 (A4) | round-cell tail: `LISTED-STEADY…` first-working round `52` → `52 (not 25; 25 was the first attempt)` | `entries=48 rows=48 matched=48 unlisted=0 unbacked=0 mismatches=0 met=true` | 0 | Not counted as escape: the counter reads only the first integer, so the tail is unverified. Partial/declared-scope issue, routed |
| F-C1-4b (A5 control) | same row, first integer changed to `25 (not 52)` | `entries=48 rows=48 matched=47 unlisted=1 unbacked=1 mismatches=2 met=false` | 1 | fail-closed on the first integer, as designed |
| F-C1-5 (A6) | phantom row `Universal cache oracle` (no admitted closure, evidence `scripts/universal_cache_oracle.py`) placed in a **second** `Capability`-headed table inside the same `## Capabilities` section, after the first table (the `### Capability rows without an admitted closure` region) | `entries=48 rows=48 matched=48 unlisted=0 unbacked=0 mismatches=0 met=true` | 0 | **ESCAPE**: `table_rows` returns only the first Capability table; the section's other tables are invisible. The repair itself moved 5 rows into exactly such a region (`git show 4446ce21`), so the counter's surface is "first table", not "the section" |
| F-C1-5b (A7 control) | same phantom placed in the first table | `entries=48 rows=49 matched=48 unlisted=0 unbacked=1 mismatches=1 met=false` | 1 | counter catches it when it is in the counted table |
| F-C1-6 (A12) | in-place edit: matched row `Revalidation exchange, contract v1`, evidence `` `scripts/reval_exchange.py` `` → `` `SCORECARD.md`; scripts/reval_exchange.py `` | `entries=48 rows=48 matched=48 unlisted=0 unbacked=0 mismatches=0 met=true` | 0 | **ESCAPE** of the predicate: a changed matched row is not "added, renamed or moved", so the review conjunct does not reach it (see PH-2) |
| F-C1-7 (A9) | the frozen C2 row, `Stale-serving extensions …`, round 98, as the frozen predicate requires, added to the first table | `entries=48 rows=49 matched=48 unlisted=0 unbacked=1 mismatches=1 met=false` | 1 | coupling: C1 is unmet at any revision that carries the C2 row (PH-1) |
| F-C1-8 (A10) | the first table wrapped in a code fence | `setup-error no Capability table before next section` | 2 | fail-closed, not an escape |
| F-C1-9 (A11) | fenced decoy table before the real table (`` ``` ``-wrapped fake `Capability` table) | `entries=48 rows=48 matched=48 unlisted=0 unbacked=0 mismatches=0 met=true` | 0 | fences are honoured; no escape |
| F-C1-10 | the 4446 repair's own `### … moved out` subsection (5 rows) | not counted by the counter; the repair's first table is the only one scored (`rows=48`) | — | the 5 moved rows are invisible to the counter (see F-C1-5) |

Cheaper-repair check (`receipt-c1_cheap.py.txt`): from the base, dropping the six unbacked rows (lines 195, 199, 200, 202, 206, 207):
`entries=48 rows=8 matched=8 unlisted=40 unbacked=0 mismatches=40 met=false` rc=1. Pruning does not reach the target; reaching it needs 40 new rows. No cheaper repair was built or measured that reaches `mismatches=0` with a correct table. [INFERENCE] Mechanically generated rows with junk prose would reach `met=true` at low cost; that is the case the declared junk-prose limit covers, and I did not run a generator to confirm it.

Master tip `7838981e`: `met=true` rc 0 (no C2 row yet). Ordering consequence in PH-1.

**C1 escapes counted: 5** (F-C1-1, F-C1-2, F-C1-3, F-C1-5, F-C1-6). F-C1-4 is partial and not counted.

## 2. C1 — live reviewer state (read-only, for the L1)

`w1/ReviewCapB/verdicts.tsv`: 45 lines (43 agree, 2 disagree). `w1/ReviewCapA/` has no `verdicts.tsv` yet.
The two ReviewCapB disagrees land C1 unmet by the frozen kill rule ("any `disagree` from a live reviewer lands C1 unmet"):
- row 56 `selftest-tally-counter`: scope overclaim, as reported by ReviewCapB;
- row 57 `id_resolver.py`: output-category overclaim, as reported by ReviewCapB. Re-checked by me: `git show 4446ce21:scripts/id_resolver.py | grep -ci ambiguous` → `0`, rc 1, so the reviewer's factual premise holds at the repair revision.
I did not evaluate these reviews beyond confirming the premise; they are not counter findings.

## 3. C2 — freshness counter attacks (`--candidate-file`, scratch cands, seeds default/1/2 and 1..10)

Each candidate is `frozen/pos-oracle.py` with one minimal change (driver `receipt-c2_build.py.txt`; sources `receipt-cand-K*.py.txt`). Counter command: `python3 -B .ufo/waves/round-98/c98_stale.py --candidate-file <cand> --work <scratch> [--seed N]`.

Counter result (`receipt-c2-counter-results.txt`), line 1 for every run is of the form `candidate=present sha256=… hand=60/60 generated=240/240 refusals=… seed=… met=true source=candidate-file`, rc 0:

| F-id | candidate change | counter runs | counter line (seed default) | named contract input (CLI, `-I`) | contract says | verdict |
|---|---|---|---|---|---|---|
| F-C2-1 (K1) | `100 <= err <= 599` → `101 <= err <= 598` | 3 seeds | `hand=60/60 generated=240/240 … met=true` (rc 0 ×3) | N1 error 100: `rc1 invalid_input: bad error`; N2 error 599: `rc1` | valid integer error in 100–599 → `not-an-error`, staleness 300 | **ESCAPE**: population never draws 100 or 599 (generator draws 99 and 600 only) |
| F-C2-2 (K2) | accept digit-string `error` (`"500"`) as integer | 3 seeds | `hand=60/60 generated=240/240 … met=true` | N3 `"500"`: `rc0 {"decision":"serve-stale-error","staleness":300}` | `error` must be integer or `"network"` → refuse | **ESCAPE**: no string-digit error in population |
| F-C2-3 (K3) | non-tchar (U+0080–U+00FF) accepted in tokens | 3 seeds | `met=true` | N4 `…stale-while-revalidate=3é`: `rc0 {"decision":"revalidate","staleness":15}` | §2: token = tchar only → refuse | **ESCAPE**: population is ASCII-only |
| F-C2-4 (K4) | quoted-string accepts U+0100+ and global U+00FF check removed | 3 seeds | `met=true` | N5 `foo="Ā"`: `rc0 {"decision":"serve-stale-revalidate","staleness":15}` | §2 qdtext ≤ U+00FF → refuse | **ESCAPE** |
| F-C2-5 (K5) | `CLAMP = 2147483648` → `2147483647` | 3 seeds | `met=true` | N6 `stale-while-revalidate=99999999999`, L=0, A=2147483648: `rc0 {"decision":"revalidate","staleness":2147483648}` | §4 / RFC 9111 §1.2.2: clamp to 2147483648, inclusive → `serve-stale-revalidate` | **ESCAPE**: population never reaches age 2^31 |
| F-C2-6 (K6) | request duplicate directive uses the last occurrence (response unchanged) | 11 runs (seeds 1..10 + default) | `met=true` on 11/11 | N7 `request_cc="stale-if-error=5, stale-if-error=60"`, A=640, error 500: `rc0 {"decision":"serve-stale-error","staleness":40}` | §2.3 first occurrence → `error-through` | **ESCAPE**; K6 also fails on about 7.9% of seeds (PH-4) |
| F-C2-7 (K7) | inclusive boundary broken only for error 504, shared cache, staleness == E | 11 runs | `met=true` on 11/11 | N8 error 504, shared, sie=300, A=900: `rc0 {"decision":"error-through","staleness":300}` | §4 inclusive → `serve-stale-error` | **ESCAPE**; rare class (about 0.9% of seeds fail) |
| F-C2-8 (K8) | delegate: candidate `import`s `decide()` from `.ufo/waves/round-98/c98_stale.py` by absolute lane path and prints its result | 11 runs | `hand=60/60 generated=240/240 … met=true` on 11/11 | N1–N8 match the contract (same decisions as the oracle) | — | **NO CAPABILITY**: the predicate is met by a file that is only a shim onto the counter's own oracle (PH-5) |
| P0 (control) | `frozen/pos-oracle.py` | 3 seeds | `met=true` | N1–N8 match | — | positive control |

In-process check, 2000 seeds × 240 generated cases (`receipt-c2-build.log`), decisions compared to the counter oracle `decide()`:
- K1, K2, K3, K4, K5: `seeds_all240_agree=2000/2000`, `disagreeing_cases=0/480000` — the generated population cannot see these classes at any seed.
- K6: `seeds_all240_agree=1843/2000`, `disagreeing_cases=160/480000` (157 of 2000 seeds fail the generated set).
- K7: `seeds_all240_agree=1983/2000`, `disagreeing_cases=18/480000` (17 of 2000 seeds fail).

Named inputs were checked against my own expectations written from the contract and RFC 5861/9111 text (`sources/rfc5861.txt` §3–4). The counter's oracle agrees with all 8 (`counter oracle self-check on named inputs: 8 / 8`).

**C2 contract-violating candidates that pass the counter: 7** (K1–K7). K8 is counted under the predicate, not here.

## 4. Freeze predicate holes

**PH-1 — causal separability and the C1 scoring revision (ordering rule).** The C2 predicate requires "the SCORECARD Capabilities table gains its row in the same round". A row with round 98 has no admitted pinned closure, so the C1 counter reports it as unbacked: F-C1-7, `mismatches=1 met=false`, rc 1. Any revision that carries the C2 row therefore makes the frozen C1 sentence false, while the C2 sentence needs that row. The freeze says "neither claim's verdict depends on the other landing" and resolves it by an ordering rule that scores C1 at the repair revision. The predicate sentence itself says "at the landed content revision", and the current tip, `7838981e`, is met only because the C2 row has not landed. The two sentences disagree once C2 lands. A reader who scores C1 at the landed tip gets unmet; a reader who scores it at `4446ce21` gets met.

**PH-2 — review conjunct scope.** The conjunct covers rows the repair "adds, renames or moves". It does not cover in-place edits to matched rows. F-C1-6 (evidence changed to an existing unrelated path, `met=true`) and F-C1-3 both pass without any review. Rows placed in a second table (F-C1-5) are reviewed only if the reviewers enumerate beyond the counter's surface.

**PH-3 — review coverage is not required.** The conjunct reads "judged `agree` by at least one of ReviewCapA / ReviewCapB and `disagree` by neither". A row judged by one reviewer only satisfies it, and so does a silent reviewer. Live state: `w1/ReviewCapA/` has no verdicts file, and ReviewCapB's file has 45 lines. The predicate, as written, is satisfiable on ReviewCapB alone. The R98-D2 full-coverage design is in the freeze prose but not in the sentence. (Separately, the two ReviewCapB `disagree` rows, 56 and 57, land C1 unmet by the kill rule; see §2.)

**PH-4 — the C2 population is seeded by the scored commit id.** `seed = int(sha256(<commit id>)[:8], 16)` when no `--seed` is given. Each re-commit of the same candidate draws a new 240-case set. K6 fails about 7.9% of seeds in-process (157/2000) and passed 11/11 counter seeds here. A candidate with a small per-case error rate can be re-committed until a seed passes, so "generated 240/240 at the landed commit" is weak evidence. Fixing the seed to a value committed before the scored run would close this.

**PH-5 — the predicate can be met with no capability (delegation).** K8 (F-C2-8) passes `hand=60/60 generated=240/240 met=true` on 11/11 seeds. It contains no RFC 5861 logic; it imports the counter's oracle from an absolute lane path. The freeze's residual limit (R97-5, "re-implements the oracle from it") is narrower than this: a candidate can call the oracle directly, and nothing in the predicate requires standalone behaviour or the candidate's own source to contain the decision.

**PH-6 — the population is blind to whole input classes.** K1–K5 agree with the oracle on 480,000 of 480,000 generated cases across 2000 seeds (rows K1–K5 above) and pass all 60 hand cases. The grammar never draws error 100 or 599, a string error, a non-ASCII byte, or a clamp value above 2^31. It draws two request directives of one name only by chance, and K6 is caught only on the seeds where that happens (PH-4). The predicate's `generated=240/240` therefore measures only the classes the grammar draws; the hand set is the only detector for the rest, and it does not cover these classes either.

## 5. Verdict inputs

- `c1_escapes = 5` (F-C1-1, F-C1-2, F-C1-3, F-C1-5, F-C1-6).
- `c2_escapes = 7` (F-C2-1 … F-C2-7).
- `predicate_holes = 6` (PH-1 … PH-6). F-C2-8 (K8) is the concrete instance of PH-5.

No lane, fleet, or sibling file was written. No `MANIFEST.json` touched. Scratch seat directory removed after this receipt copy.
