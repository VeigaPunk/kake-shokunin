# MutReval — round-96 w1 mutation probe (seat MutReval, 2026-11-05)

**MUT frozen=14/14 new=12 newsurvivors=N05,N06,N07,N08,N11**

## Commands and observed results (every verdict names its command and rc)

1. **Main counting command at the wave HEAD** (cwd `/home/vgpnk/Projects/shokunin/kake-shokunin`, HEAD = `049e8eca2f0fa5e981232eb4efe367357dce578c`, the freeze commit):
   `TMPDIR=/fast/scratch/hyaku/kake-r96/MutReval python3 -B .ufo/waves/round-96/c96_reval.py --root . --revision $(git rev-parse HEAD) --work /fast/scratch/hyaku/kake-r96/MutReval/reval-main`
   → line 1: `C2v96 revision=049e8eca2f0fa5e981232eb4efe367357dce578c candidate=absent hand=0/37 generated=0/120 forgeries_refused=0/6 positive=refused mutants=0/14 survivors=none anti_table=ok population=ok seed=96 met=false`
   → line 2: `{"detail": "candidate absent"}` — **rc=1**.
   Line-identical to the committed do-nothing control `controls/base-c2.txt` except the revision field: at the wave HEAD the candidate `scripts/reval_exchange.py` does not exist yet (`git show HEAD:scripts/reval_exchange.py` → rc=128), so the counter's main path scores zero subjects and reports `mutants=0/14` **without scoring the population**. Reproduced, never re-stamped. Population liveness at this revision is therefore carried by (2) and (3).

2. **The counter's own population scoring path**:
   `TMPDIR=/fast/scratch/hyaku/kake-r96/MutReval python3 -B .ufo/waves/round-96/c96_reval.py --work /fast/scratch/hyaku/kake-r96/MutReval/reval-selftest --selftest`
   → `selftest 7/7 fixtures scored as declared; mutants killed 14/14 survivors=none; anti_table=ok; generated-vs-reference seeded cases=37` — **rc=0**.
   Line-identical reproduction of `controls/ctl-c2-selftest.txt`. The frozen 14-mutant population is LIVE under the counter's own rule.

3. **Module path for per-mutant receipts** (counter imported as a module inside the seat scratch — never edited): `driver.py` re-scored every population mutant through the counter's own `mutant_cases()` (find/replace asserted to occur exactly once in the frozen pos-good bytes; the counter's own SANDBOX; `gen_limit=40`, the counter's mutant rule) plus a full-generated-set pass (seed 96: 120 raw inputs, 112 decided, 8 reference-refused). **Pristine control admitted first: hand=37/37 gen=112/112** — a baseline failure would have made every mutant verdict inconclusive; it did not. Lane bytes before==after across the whole run (`receipt-pristine-driver.txt`, digests in `receipt-digests.txt`). Wall ≈103 s.

→ **Frozen population verdict: 14/14 KILLED, no survivor** — `mutants=killed/14`, consistent across the counter's selftest and every per-mutant receipt.

## Frozen population (14 receipts: `receipt-frozen-M01.txt` … `receipt-frozen-M14.txt`)

| id | clause | verdict | first failure (counter rule) |
|---|---|---|---|
| M01 | C2 both validators together | killed | `construct/both-validators` — IMS null when etag present |
| M02 | C1 INM sent when etag stored | killed | `construct/both-validators` — INM null |
| M03 | C1 weak etag verbatim | killed | `construct/lm-only` — crash on `None.startswith` (expected decision, got rc=1 traceback) |
| M04 | C3 304 updates stored | killed | `c304/with-etag` — replace-stored |
| M05 | C4 5xx upper boundary | killed | `c5xx/599-upper-edge` — replace-stored |
| M06 | C5 full response replaces | killed | `c200/replace` — update-stored |
| M07 | C1 no-validator decision | killed | `construct/neither-validator` — construct with null fields |
| M08 | C6 1xx refused | killed | `refuse/1xx-interim` — replace-stored |
| M09 | C6 status-without-validator refused | killed | `refuse/status-without-validator` — update-stored |
| M10 | C6 validators-without-representation refused | killed | `refuse/validators-without-representation` — construct |
| M11 | C6 raw duplicate keys refused | killed | `refuse/raw-nested-dup` — construct with last-wins lm=2 |
| M12 | C6 unknown top-level keys refused | killed | `refuse/unknown-top-key` — cannot-revalidate |
| M13 | C6 negative last_modified refused | killed | `refuse/lm-negative` — construct with lm=-1 |
| M14 | C6 etagc control chars refused | killed | `refuse/etag-quoted-control` — construct |

Kill-path nuance recorded for M11: `refuse/raw-dup-bytes` passes under M11 (the duplicated `received_status: 304` lands on a validator-less stored response and is refused anyway by the C6 status-without-validator rule) — `refuse/raw-nested-dup` is the load-bearing kill. Keep both cases.

## New clause mutants (defs + outcomes in `new-mutants.json`; receipts `receipt-new-N01.txt` … `receipt-new-N12.txt`)

Design rule: find/replace pairs, each asserted to occur exactly once in the frozen pos-good bytes (`find_occurrences_in_pos_good=1` for all 12); scored under the counter's mutant rule (hand 37 + first 40 generated) AND the full generated set (112); hand cases frozen, generated expectations recomputed with the counter's `reference()`/`generate()`; verdicts recorded for both limits.

| id | clause probed | verdict (counter rule) | first failure | note |
|---|---|---|---|---|
| N01 | C1/C2 IMS only when an etag is stored | killed | `construct/lm-only` | inverse of M01's leg; killed |
| N02 | C1 W/ prefix survives parsing | killed | `construct/weak-etag-verbatim` | |
| N03 | C5 499 usurped by update-stored | killed | `c499/replace-upper-edge` | lane-convention upper edge pinned |
| N04 | C3 304 → may-reuse-stored | killed | `c304/with-etag` | decision-word swap, distinct from M04 |
| N05 | C6 empty-string etag accepted | **SURVIVED** | — | no case carries `etag: ""`; generated tags are the four fixed strings |
| N06 | C6 boolean last_modified accepted | **SURVIVED** | — | no case carries `last_modified: true`; `refuse/lm-negative` still refuses under the mutant, so M13's kill does not transfer |
| N07 | C6 exists-false+validator refused only at construction | **SURVIVED** | — | hand case is construction-stage only; generated never pairs exists=false with a validator |
| N08 | C6 non-object check dropped | **SURVIVED** (vacuous) | — | refusal→refusal: every non-object population input still dies on the key-set check (string/array) or TypeError→rc≠0 (number/bool) |
| N09 | C6 hook removed, dup keys last-wins | killed | `refuse/raw-nested-dup` | same load-bearing kill as M11; `raw-dup-bytes` passes via the collateral no-validator refusal |
| N10 | C4 5xx lower edge exclusive | killed | `c5xx/500` | |
| N11 | C6 dup-key refusal scoped by naive depth tracking | **SURVIVED** (vacuous no-op) | — | `object_pairs_hook` fires at object completion, inner-first, and a module-level counter resets between sibling completions, so every object is checked as depth 1 ("top"); the naive top-level-only recipe is behaviorally identical to the positive control |
| N12 | C6/C1 obs-text dropped from etagc | killed | `construct/obs-text-etag` | hand case kills; generated `'"café4"'` tag also fails (38/40) |

new=12, killed=7, survived=5 (3 real acceptance gaps: N05, N06, N07; 2 vacuous: N08, N11).

## Survivor recipes (successor-population items — routed, not implemented)

- **R-MUT-1 (N05):** add hand case `C("refuse/etag-empty", True, "", None, None, None)` — one case kills N05 while pos-good stays admitted.
- **R-MUT-2 (N06):** add hand case `C("refuse/lm-bool", True, None, True, None, None)`.
- **R-MUT-3 (N07):** add a status-bearing validators-without-representation case, e.g. `C("refuse/validators-without-representation-status", False, '"v"', 1, 304, None)`.
- **R-MUT-4 (N08/N11 class):** under refusal-ness scoring, a mutant that swaps one C6 refusal for another is invisible; if the successor wants the non-object and dup-scoping clauses killable, the instrument must pin refusal diagnostics or refusal classes. Instrument-design question — routed for decision, no frozen file touched.

## Instrument-integrity notes (findings only; no repairs made)

- Digests verified before attacking and re-verified after: `c96_selfassess.py a282da65…`, `c96_reval.py ec40aec1…`, pins file `d9c8f96e…`, pos-good `47c65725…`, mutants json `517f7b16…` — all MATCH `controls/instrument-sha256.txt`. Frozen round-95 counter `8fd27d62…` verified present and untouched (`receipt-digests.txt`).
- No defect found in the frozen counter or population: 14/14 reproduced exactly, exit codes as committed. The survivor findings are coverage gaps of the fixed 14-mutant population, not of the counter's scoring — the counter kills exactly what it scores.
- Coarse-refusal observation (route-worthy): `score_subject` treats any rc≠0 / empty / non-JSON stdout as satisfying an expected refusal, so clause-level refusal swaps are invisible (N08, N11 survive vacuously; M03 died by crash only because a *decision* was expected). This is the frozen instrument's declared scoring rule — recorded as a finding, never amended.

## Bound compliance

- Writes: only `.ufo/waves/round-96/w1/MutReval/*` (+ the seat report `w1/MutReval.md`) and `/fast/scratch/hyaku/kake-r96/MutReval/*` (deleted before yield; receipts copied first). Nothing else in the lane tree; MANIFEST.json never touched.
- No mutating git or jj command anywhere (only `rev-parse`/`show`/`log`/`status` read-only); fixture-free seat — no clone created. No sysctl touched. No tool installed (stock python3/git sufficient).
- Counter/contract/population/pos-good/forgeries: read-only throughout; `c96_reval` was imported, never edited.
