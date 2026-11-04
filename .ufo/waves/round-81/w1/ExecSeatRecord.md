# ExecSeatRecord — verify the R80-6 recorder against known-truth fixtures

**Verdict: the committed `scripts/wave_seat_record.py` is sound on all four checks (correct on real round-79/round-80 bytes, whitespace-only classified `empty`, byte-identical under rerun and reordering, honest about the current results schema); R80-6 can close from this recorder once the L1 commits `w1-results.json` + `w1-spec.json` + the recorder-written `seat-failures.json` — with one conditional defect: if round-81's results file is upgraded to carry per-seat `status`/`exit`/`error` keys (what R80-6's routing asks the orchestrator for), this recorder ignores them and its `schema_limit` sentence becomes false.**

Target bytes: worktree recorder == freeze-commit bytes (`git hash-object` = `git rev-parse a77b8a19…:scripts/wave_seat_record.py` = blob `5eab7ea6…`); file sha256 `95a00bd9621e933519122c2b020f6bcdd6e00d966ce4ee580cb679bf4df87b29`. Lane HEAD at run time `bec3ecf7` (wave in flight; recorder unchanged). No edits made to the recorder or any counter; no network; no tool installs (operator authorization unused); no labrat needed.

## 1. Cross-round fixture (prescribed round-80 run + round-79, where the named facts live)

```
$ python3 -B scripts/wave_seat_record.py --results .ufo/waves/round-80/w1-results.json \
    --spec .ufo/waves/round-80/w1-spec.json --out <scratch>/r80.json
seats=15 empty=2 not_settled=0   rc=0
$ python3 -B scripts/wave_seat_record.py --results .ufo/waves/round-79/w1-results.json \
    --spec .ufo/waves/round-79/w1-spec.json --out <scratch>/r79.json
seats=14 empty=2 not_settled=0   rc=0
```

- r80 record: `empty_output=["MutC","ReviewC1"]`, `not_settled=[]`, 15 seats. **This disagrees with my item's stated facts** (`ExecC2Tool`/`CriticC`, 14 records for 15 requested) on every component.
- It **agrees exactly** with the round-80 closure §1 wave-shape row: "15 records … 2 empty (`ReviewC1`, `MutC`)" (`corpus/lessons/round-80-verifier-spotcheck.md` §1), and with my independent re-derivation from the raw bytes (15 rows; spec names 15 items; spec-minus-results = ∅).
- The `ExecC2Tool`/`CriticC` facts are **round-79 facts** (closure §2, R79-8 close). Run over round-79's file the recorder reproduces them exactly: `empty_output=["CriticC","ExecC2Tool"]`, 14 seats.
- "14 records for 15 requested seats" matches **neither** round's bytes: round-79's own `w1-spec.json` names 14 items and its results carry 14 rows (`not_settled=0`); round-80 is 15/15. So that clause of the item premise is not decidable from any committed spec/results pair — the recorder's `not_settled` derivation is correct (verified against ground truth for both rounds); the premise misattributes the facts.
- Byte/digest spot re-derivation from the r80 results: `ScoutSources` and `ReviewC1` entries match recomputed `output_bytes`/`output_sha256` exactly; `ReviewC1` role `reviewer`, status `empty`, `exit=unknown`, `error="not recorded in w1-results.json"`.

Receipts: `ExecSeatRecord/r80.json` (sha256 `ea7a00ae…57bb3`), `ExecSeatRecord/r79.json` (`b9a19f3c…ecf6d`), full command log `ExecSeatRecord/run.log`.

## 2. Class boundary (synthetic fixtures in scratch)

Spec: 3 items (SeatA scout, SeatB executor, SeatC critic). Results all-`"x"` / one-`""` / one-`"   \n"`:

```
case a: SeatA=reported SeatB=reported SeatC=reported | empty_output=[]   rc=0
case b: SeatA=reported SeatB=reported SeatC=empty    | empty_output=[SeatC] rc=0
case c: SeatA=reported SeatB=reported SeatC=empty    | empty_output=[SeatC] rc=0
```

Whitespace-only (`"   \n"`) is classified `empty`, not `reported`, because classification is `raw.strip()` on the UTF-8 bytes. Matches the required boundary exactly.

Receipts: `ExecSeatRecord/cases/{a,b,c}-results.json`, `ExecSeatRecord/cases/{a,b,c}-record.json`.

## 3. Determinism and canonicality

```
run 1 → r80.json; run 2 → r80-again.json;  cmp rc=0
reversed results array (cases/r80-reordered.json, 15 rows) → r80-reordered-record.json; cmp r80.json rc=0
sha256: ea7a00ae…57bb3 for all three (4459 bytes each)
```

Same bytes across reruns into different paths and across results-array reordering: `seats` is a dict serialized with `sort_keys=True` (indent 1, trailing newline), and `empty_output`/`not_settled` are `sorted()`. Canonical as the counter requires (`c81_defect_queue.py:296-299` compares parsed records; list order is the only order-sensitive part and both lists are sorted).

Receipts: `ExecSeatRecord/r80-again.json`, `ExecSeatRecord/r80-reordered-record.json`, digests in `run.log`.

## 4. Schema honesty

Record's `schema_limit`, verbatim: `"w1-results.json records only name, agent and output; it carries no status, exit code or error text, so a seat's failure cause is not recoverable from committed bytes and every exit/error here is declared unknown"`.

- Actual keys of `.ufo/waves/round-80/w1-results.json`: top-level `{lane, results, round, seats, wave}`; all 15 rows exactly `{agent, name, note, output}`. **No `status`/`exit`/`error` key exists — the recorder ignores none; the item's defect condition is not triggered** (checked for `status, exit, error, exit_code, error_text, status_code, err, failure, ok, success`).
- Round-79's file: same shape (14 rows) — no ignored key either.
- `.ufo/waves/round-81/w1-results.json`: **ABSENT** at run time (2026-11-04T11:56Z, mid-wave) — the item anticipated this; nothing measured there yet.
- Wording nit (not the item's defect condition): the sentence "records only name, agent and output" understates the row schema — every row also carries `note` (always `null` in both rounds). Harmless to the predicate.
- **Conditional defect to watch:** R80-6's routing asks the orchestrator to record `status`/`exit`/`error` at dispatch time in the *next* results schema. If round-81's `w1-results.json` lands with those keys added, this committed recorder still hardcodes `exit="unknown"` / `error="not recorded in w1-results.json"` and its `schema_limit` sentence becomes factually false about the file it describes. Per my item that is then a defect: fix the recorder (or keep the round-81 schema unchanged and upgrade next round) **before** the L1 writes `seat-failures.json`.

## 5. Counter consistency observation (reported, not fixed — counters are frozen)

The C1 counter's embedded `RECORDER` copy (`c81_defect_queue.py:551+`) is a behavioral subset of the committed script: `diff -u` (rc=1) shows the embedded copy lacks the top-level-dict check, the non-string `output` coercion, and the `agent` field on seat entries (docstring/typing otherwise). Its selftest green/mutant fixtures therefore exercise the weaker copy, and no selftest asserts the record's `agent` field. No predicate conjunct (rc==0, committed==re-derivation, role/status/exit/error present, status enum, schema_limit names the limit — `c81_defect_queue.py:273-311`) is weakened by this; the real measurement runs the tree's committed copy, which is the file I verified.

## R80-6 verdict for the round-81 record

The counter's four conjuncts are all within the committed recorder's demonstrated behavior: re-derivation exits 0 on real wave data (rc=0 on 29 recorder invocations across rounds 79/80 and 3 synthetic shapes), the record is canonical (byte-stable, order-insensitive), every seat entry carries `role`/`status`/`exit`/`error` with `status ∈ {reported, empty}` (the `unknown` enum value is never emitted for a settling row), and the record names the schema limit. **Held: once the L1 runs this recorder over round-81's committed `w1-results.json`+`w1-spec.json`, commits the output as `.ufo/waves/round-81/seat-failures.json`, and the results file keeps the current row shape, R80-6's condition holds.** Two standing caveats: (a) the results-schema-upgrade branch in §4 would make the record's schema-limit sentence false — decide the schema before writing the record; (b) `p_r80_6` fails cleanly (rc=2 path) if `w1-results.json` is absent at measurement, so the four files must land together.

Receipts retained under `.ufo/waves/round-81/w1/ExecSeatRecord/` (sha256 manifest: `SHA256SUMS`; drivers `driver.sh`, `make_cases.py`, `reorder.py`, `analyze.py` re-run the whole battery). Scratch `/fast/scratch/hyaku/kake-r81/ExecSeatRecord/` deleted before yield.
