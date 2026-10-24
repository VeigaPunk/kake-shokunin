# RevengerReceiptFlow — receipt-trust dataflow of `c44_audit.py` + driver-v2 fix-point map

Seat: `kake-r45.RevengerReceiptFlow` (revenger, wave 1). Axes: **operability** (primary; judged),
freshness (lane axes; my item feeds C1 v2 design and C2a selftest mutants).
Date: 2026-10-24. No files outside my write paths touched; no subagents; no installs
(python3/coreutils sufficient; pacman paused, nothing needed).

**Verdict vs named attack: PASS (map produced, attack re-demonstrated against current bytes).
Zero line-cite drift on the reviewed instrument bytes; SCORECARD cites drifted +5 lines
(content verbatim-identical).** One receipt-validity mechanism closes all five defects;
its unique fix-point is `run_counter`'s return boundary (`c44_audit.py:61`).

## 1. Byte/cite verification (ReviewCounterContract, w2, against current bytes)

```
$ sha256sum .ufo/waves/round-44/c44_audit.py .ufo/waves/round-44/c44_count_v5.py
8ee2c8bf9333206963236b023048ae2b560bbec703adef4d448bd5529c2d0c75  .ufo/waves/round-44/c44_audit.py
5cedaa3b9f918979447f2e18c054d42a65bfc79fe700be7f2272d69dbe7672bc  .ufo/waves/round-44/c44_count_v5.py
$ wc -l .ufo/waves/round-44/c44_audit.py
228 .ufo/waves/round-44/c44_audit.py
```

Both hashes equal the review's cited bytes (`8ee2c8bf…`, `5cedaa3b9f91…7672bc`). File
unchanged since the review: **no byte drift**. Per-line re-pin by grep over current bytes:

| Review cite | Current bytes | Drift |
|---|---|---|
| `run_counter` never passes `--seed` `:49-53` | 49 argv, 50-51 `--tool-file`, 52-53 `--revision`; `subprocess.run` :54 | exact |
| receipt parsed regardless of exit `:54-61` | 56-60 `open/json.load` (no returncode consult), return :61 | exact |
| `semantic_witness` `:63-66` | def :63, body 64-66 | exact |
| `expectation_ok` `:69-81`; blind `:74-76`; witnessed `:77-79`; not-met `:80-81`; `not_met` built `:73` | all confirmed | exact |
| argparse-only exit 2 `:126`; controls open `:137`; TSV unpack `:141` | confirmed | exact |
| receipt dirs `:131-132,148`; relpath `:159`; build path `:174` | 130 outdir, 131 tools_dir, 132 makedirs, 148 out, 174 build-N | exact |
| `score` row construction `:151-160` (`note` dropped at `:160`) | 151 `run_counter`, 152-156 caught loop, 157-160 dict (`error=None if rec else…`; no `note` field) | exact |
| pool `:163`; `class_keys` `:165`; class-note print `:210` | confirmed (210 by block count, pinned by `sys.exit` :222) | exact |
| `score_build` `:173-180`, build pool `:181-182`, `if a.build_rev…` `:172` | confirmed | exact |
| `bool(build)` at `:79`; `ok = expectation_ok` `:203`; exit `:222` | confirmed | exact |
| nits `:192` (witnessedByClass full caughtBy), `:199-200` (classCaught/legacyCaught) | confirmed | exact |
| counter seed `c44_count_v5.py:995`; seed recorded `:997` | 995 `urandom` fallback; 997 `"label": a.label, "seed": seed` | exact |
| CannotEvaluate after class entries `:1097-1098`, entry stored `:1108`, receipt-on-exception `:1114-1119` | 1097-1098 raise; 1108 store; 1114-1119 both `finish(2)` handlers; 1120 `finish(0 if met else 1)` | exact |
| tool-absent `:1031-1034` (`cand=None`), `:1078-1080` (`equal:False, candExit:"tool absent"`), `:1113` note | confirmed | exact |
| met/ratios `:1100-1104, 1111-1112`, `equalRuns` `:1109` | confirmed | exact |
| SCORECARD kill rules `:3454-3458` | **now `:3459-3463`** (rule (2) "a counter error → not a witness" at 3460-3461) | **+5 lines** |
| SCORECARD frozen predicate reading `:3562-3570` | **now `:3567-3573`** ("universal v4-blindness" sentence at 3570-3571) | **+5 lines** |

The +5 SCORECARD shift is consistent across both cites (one 5-line insertion above 3454 in
the append-only file); the quoted content is verbatim-present. No other drift found.
Sibling observation (not part of this review's cites): `w2/DistillerWave1.md` finding 6
cites the receipt header as `c44_count_v5.py:999-1003`; `counterSha256` is actually at
`:998` (classesMode :1000, classRuns :1001) — off-by-one at the range start.

## 2. Reconstructed dataflow (the trust boundary)

```
main :107
 ├─ load_counter :33-36 / counter_sha :134        (counter bytes identified once)
 ├─ controls TSV :137-143                         (27 rows, sha-pinned)
 ├─ pool.map(score) :163 ── score :145-160 ───────┐
 │     sha gate :149-150 (tool bytes vs TSV)      │
 │     run_counter :151  →  THE funnel :48-61     │  subprocess :54, receipt parse :56-60,
 │     caught loop :152-156 (rec["runs"], equal:False) │ return (code, rec, so, se) :61
 │     row dict :157-160 (error ONLY if rec None; exit recorded-not-gated; note DROPPED)
 ├─ semantic_witness :63-66 over rows :167        │  met is False ∧ caughtBy∩class_keys ≠ ∅
 ├─ pool.map(score_build) :182 ── :173-180 ───────┘  same funnel :175, same trust :176-180
 ├─ expectation_ok :69-81  ← rows + build         (exit/note/provenance never consulted)
 └─ ok :203 → summary :186-202 → exit(0/1) :222
```

Contract: a row is "evidence" iff `rec` parsed from the receipt path. `run_counter` reads
`out` whenever parsing succeeds (`:56-60`) **regardless of `p.returncode`**; the counter
writes a receipt on every path (`finish` `c44_count_v5.py:1005-1015`; `finish(2)` on
CannotEvaluate/any exception `:1114-1119`; `finish(0 if met else 1)` `:1120`). Therefore
partial/failed-run receipts flow into rows with `error=None` (`:160`), and
`semantic_witness`/`expectation_ok` see only `met`/`caughtBy`. That is the single root
cause; defects 1a/1b/1c and medium-2 are its faces.

Counter-side receipt facts the gate can rely on (all in frozen v5 bytes): exit ∈ {0,1,2}
(0/1 normal, 2 cannot-evaluate); `note` is `None` exactly when nothing abnormal happened,
`"tool absent"` (:1113) or `"cannot evaluate: …"` (:1115,:1118) otherwise; header carries
`counterSha256` (:998), `label` (:997, driver-controllable via `--label`, accepted since
`:987`), `classesMode` (:1000), `classRuns` (:1001), `seed` (:997).

## 3. Fix-point map for driver v2 (one mechanism, all defects)

**The one mechanism — `receipt_valid(rec, code, out_path, run_label, counter_sha, t0)` —
inserted at `run_counter`'s return boundary, i.e. replacing the return at
`c44_audit.py:61`.** `run_counter` is the unique acquisition funnel for control rows
(`:151`) *and* build rows (`:175`); a gate there is inherited by every consumer with zero
per-site duplication. Invalid ⇒ `rec` returned as `None` ⇒ the *existing* downstream
`rec is None` handling (`:160`, `:180`) already demotes the row to an error row —
`not errors` / `total == expected_rows` then fails every expectation. Clauses:

| Clause | Kills | Implementation |
|---|---|---|
| (i) `code in (0,1)` | 1a exit-2 partial receipt after class divergence; also medium-2 (cannot-evaluate) | counter exit contract `:1120,1116,1119` |
| (ii) `rec.get("note") is None` | 1b tool-absent (exit 1, note `:1113`, all 21 keys caught) | note must be absent on an honest run |
| (iii) window: `getmtime(out) ≥ t0` ∧ `rec["label"] == run_label` ∧ `rec["counterSha256"] == counter_sha` | 1c stale/planted receipts; receipts from other counter bytes | driver stamps `t0` before `pool.map` and generates a fresh `run_label` per invocation (uuid4); **counter v5 already echoes `--label` into the receipt (`:987,:997`)**, so run-binding works against the *frozen* counter bytes — no counter change needed for the gate itself |

Residual enforcement edits (the only others, still one validity predicate):
- `score`/`score_build` (`:157-160`, `:176-180`): when the gate voids `rec`, synthesize
  `error="invalid receipt: exit=%s note=%r"` (today `error` would be empty since `se/so`
  can be blank on a receipt-writing failure).
- `expectation_ok` witnessed clause `:79`: replace `bool(build)` with
  `len(build) == BUILD_RUNS_REQUIRED` (pin 3) — **medium-3 (build count unpinned) is a
  count policy, not a receipt property; this one line is the second and last
  enforcement point.**

Per-defect closure walk (each verified live, §4): 1a — clause (i) ⇒ error row ⇒ `witnessed`
expectation fails via `not errors` and `total==expected_rows`. 1b — clause (ii) ⇒ same.
1c — clause (iii) ⇒ planted/stale/foreign-counter receipts void ⇒ rerun cannot certify
yesterday; a killing crash (exit −9) also fails (i). Medium-2 — a cannot-evaluate canary is
an error row, so `len(not_met) == total` and `total == expected_rows` both fail: a
measurement failure is no longer scored as not-met. Medium-3 — count pin at `:79`.

Freshness hooks for the v2 selftest (C2a): add witness-class mutants per gate clause —
flip `(0,1)`→`(0,)` (survivor class today's m2/m4 style), drop the note clause, invert the
mtime comparison, drop the label equality — the selftest must kill 4/4 the way v1 killed
2/4. C2b (v4 receipt predicate naming unexecuted class runs) is counter-side, out of my
scope; ScoutCounterV4Map/counter-v6 own it.

## 4. Decisive evidence (verbatim)

Shipped v1 selftest on the frozen bytes (behavior matches the read source):

```
$ python3 -B .ufo/waves/round-44/c44_audit.py --selftest
SELFTEST PASS: class and mixed-key witnesses pass, legacy/timing-only and no-class witnesses fail
SELFTEST_EXIT=0
```

Probe `/fast/scratch/hyaku/kake-r45/RevengerReceiptFlow/gate_probe.py` (imports the frozen
bytes; rows shaped exactly as `score()` emits, `:157-160`):

```
== current bytes (frozen v1, sha 8ee2c8bf…) accept the attack ==
1a semantic_witness(exit=2, caughtBy=[G2]): True
1a expectation_ok witnessed: True
1b semantic_witness(note='tool absent', 10 class keys): True
1b expectation_ok witnessed: True
1c expectation_ok witnessed (exit=-9 planted rows): True
m2 expectation_ok not-met on exit-2 cannot-evaluate: True
m3 expectation_ok witnessed with ONE build receipt: True

== v2 single gate (receipt_valid at run_counter return boundary) rejects all ==
1a gated row error: invalid receipt: exit=2 note=None
1a gated: witnessed-ok: False
1b gated row error: invalid receipt: exit=1 note='tool absent'
1c gated row error: invalid receipt: exit=0 note=None
m2 gated: not-met-ok: False
m3 gated (pinned count): witnessed-ok with 1 build: False
m3 gated (pinned count): witnessed-ok with 3 build: True
PROBE_EXIT=0
```

(The 1c row exercised all three window clauses at once — stale mtime, foreign
`counterSha256`, mismatched label; each alone is sufficient by construction.)

## 5. Files written

- Report: `.ufo/waves/round-45/w1/RevengerReceiptFlow.md` (this file).
- Scratch: `/fast/scratch/hyaku/kake-r45/RevengerReceiptFlow/{gate_probe.py,stale.json}`.
- No lane source edited; frozen files only read. No blockers.

## 6. Residuals / dependencies (findings, not blockers)

- **Dependency noted:** `.ufo/waves/round-45/` has no `c45_audit.py` / `c45_count.py` /
  `c45_matrix.py` / `c45_freshness.py` yet (glob of the round dir) — the v2 bytes this map
  targets are the executors' build items; the map above is the insertion-point contract.
- Threat-model limit of clause (iii): mtime+label binding defeats crash-kill reruns and
  pre-planted receipts; a writer with outdir access *during* the window could still plant
  (out of scope for this lane's threat model — instruments are local, not adversarial).
- Not closed by this mechanism (correctly out of scope): LOW defect 4 (`blind` still gates
  universal v4-blindness, `:74-76` — conservative-only) and LOW defect 5 (input-error exit
  conflation; note `subprocess.TimeoutExpired` at `:54` still escapes `score` through
  `pool.map` `:163` — v2's gate should also catch it inside `run_counter`, which the
  invalid-receipt path absorbs for free).
- All line numbers in §2-3 are pinned by grep/read against the two hashes in §1; any future
  byte change to `c44_audit.py`/`c44_count_v5.py` invalidates them (frozen, sha-guarded).
