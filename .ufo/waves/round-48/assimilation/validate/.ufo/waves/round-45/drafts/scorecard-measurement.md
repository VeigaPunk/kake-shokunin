# Round 45 — SCORECARD measurement-append DRAFT (L1 lands; wave-1 scribe)

Seat: `kake-r45.ScribeDeclarations` (scribe, wave 1). Lane: `kake-shokunin`
(axes: operability, freshness). Draft only — this file is **not** the SCORECARD;
the L1 appends the text below to `SCORECARD.md` in its own append-only section.

Source of the frozen claim: `SCORECARD.md` §"Round 45 — C1 and C2 declared
(frozen before any claim receipt is produced)" (freeze commit `3b4c430a`, base
`35b35f41ba8782872bec42a4df77407c76e7926e`). The declaration text is **not**
edited by this append.

## Placeholder convention

Every token `{{NAME}}` is a value this seat cannot supply from observed bytes.
Each carries a fill-in instruction. **No placeholder may be left unfilled at
land time**, and no placeholder may be replaced by a guess.

| Placeholder | Fill from |
|---|---|
| `{{MEASURED_COMMIT}}` | the commit the round-45 receipts are measured at (wave-1 instruments are currently uncommitted in the working tree; the L1 commits them, then re-runs the counting commands, or records the commit it measured) |
| `{{C1_MATRIX_BEFORE_STDOUT}}` | stdout line of `python3 -B .ufo/waves/round-45/c45_matrix.py --stage before` |
| `{{C1_MATRIX_AFTER_STDOUT}}` | stdout line of `python3 -B .ufo/waves/round-45/c45_matrix.py --stage after` |
| `{{C1_AFTER_REJECTION_CLASSES}}` | `rejection_classes` array in `.ufo/waves/round-45/verification/matrix/after.json` |
| `{{C1_HONEST_AUDIT_LINE}}` | the `AUDIT …` line of the v2 honest-cohort run |
| `{{C1_HONEST_EXIT}}` | exit status of that run (expected 0) |
| `{{C2_SELFTEST_AFTER_TABLE}}` | the four `after/mN.txt` kill results (m1..m4) |
| `{{C2_V4_PREDICATE_AFTER}}` | `predicate` string of the fresh v6 v4 receipt |
| `{{C2_V4_RECEIPT_PATH}}` | path of the fresh v6 v4 receipt |
| `{{C2_V4_COUNTER_SHA}}` | `counterSha256` recorded in that receipt |
| `{{C2_V4_SEED}}` | `seed` recorded in that receipt |
| `{{WITNESS_SPLIT_SENTENCE}}` | the L1's chosen sentence from §"C2(c) witness split — receipt identity" below |
| `{{SHA_GUARD_DISPOSITION}}` | the L1's disposition of the round-45 sha-guard drift (see §"Kill-rule (1) / (4) — open item") |
| `{{C1_REJECTED_ROW_COUNT}}` | `rejected_rows` length in `.ufo/waves/round-45/verification/matrix/after.json` |

**Ledger-gate hazard (read before landing).** `scripts/ledger_latest_check.py`
takes the *last* regex match in its file. The landed append must not contain the
literal phrase `re-scored <N> of the 27` anywhere in `SCORECARD.md`, and must not
add `not met (T1 …, T5 …)` or `T1 …–…, T5 …–…` to `LOG.md`. The draft text below
contains none of those three patterns (verified — see the L1's checklist). The
current gate state is `3 figures, 0 mismatches`, exit 0.

---

## Append block A — C1 measurement (to be appended after the frozen declaration)

```markdown
### Round 45 — C1 measurement (appended after the freeze; the declaration above is not edited)

Measured commit: `{{MEASURED_COMMIT}}`. Counting command (frozen, verbatim):

    python3 -B .ufo/waves/round-45/c45_matrix.py --stage before|after

Before — the frozen v1 driver `.ufo/waves/round-44/c44_audit.py` (sha256
`8ee2c8bf9333206963236b023048ae2b560bbec703adef4d448bd5529c2d0c75`) accepts
**3/3** invalid fixture classes: `{{C1_MATRIX_BEFORE_STDOUT}}`
(receipt `.ufo/waves/round-45/verification/matrix/before.json`; the per-class v1
driver outputs are retained under
`.ufo/waves/round-45/verification/hardening/before/{counter-error,tool-absent,stale-planted}/`,
sha256 `bce55a787d04188d9f7e5c1e2c06ec44eb1afee59801704689f15a67914980f3`
(counter-error), `aed6b92f8fe56819b07715cecacd46d54ecbbb417b9396db6efeed01fdaaca02`
(tool-absent), `cc4accb91c5b25a3619910e9b5957e28213f891cf8c9c1eee03af9a0ef6ac324`
(stale-planted) — each `ok=true`, `witnessed 1/1 notMet=1 build met 3/3`; the three
rejection shapes are the real v1-observable shapes: row `exit=2` on an
otherwise-authentic committed receipt, `note="tool absent"` with all 21 runs
`equal=false` and `exit=1`, and row/build `exit=-9` over pre-run planted receipt
bytes).

After — driver v2 `.ufo/waves/round-45/c45_audit.py` (sha256
`5a342e29c7e872d992cfedc26de849c010d197bb82162e007a61a55d915c7051`) accepts
**0/3** invalid fixture classes and names each rejection with its defect class:
`{{C1_MATRIX_AFTER_STDOUT}}`; named rejection classes
`{{C1_AFTER_REJECTION_CLASSES}}` over `{{C1_REJECTED_ROW_COUNT}}` rejected
control/build rows (receipt `.ufo/waves/round-45/verification/matrix/after.json`).

Honest-cohort certification is unchanged: v2 over the frozen round-44 cohort
(`controls-27.tsv`, counter `c44_count_v5.py`, `--classes v5 --expect witnessed
--build-rev 020bc457 --build-runs 3`) yields `{{C1_HONEST_AUDIT_LINE}}`, exit
`{{C1_HONEST_EXIT}}` (receipt
`.ufo/waves/round-45/verification/honest-regression/after-v5-v2.json`), matching
the frozen v1 receipt `.ufo/waves/round-44/verification/claim/after-final/after-v5.json`
(sha256 `9dead4d7d65d10f268f37efba185f12bb4f8e8942e8e81e98df4b1c8fdc076d1`;
`witnessed 27/27 notMet=27 build met 3/3 ok=true`).

Kill-rule evidence pointers (all frozen rules of the declaration):

- (1) frozen round-44 bytes untouched — sha guard
  `.ufo/waves/round-45/verification/sha-guard/before.sha256` (483 guarded files;
  file sha256 `30d33f643530aaee1400a86f61b07d4b3456fc8a137d3e7e28375ece7b8f457d`)
  against the end guard; disposition `{{SHA_GUARD_DISPOSITION}}`.
- (2) every cited receipt re-derives from committed bytes at its recorded inputs —
  per-receipt sha256 values quoted above; each value is re-derivable with
  `sha256sum <path>` at `{{MEASURED_COMMIT}}`.
- (3) v2 reads no control file beyond v1's reads — v2 source
  `.ufo/waves/round-45/c45_audit.py` adds a run-manifest/nonce and a receipt-validity
  gate (`counter_error` / `tool_absent` / `stale_receipt`) and no control-file read.
- (4) v2's honest-cohort verdict equals v1's (27/27, build 3/3, exit 0) — the
  honest-cohort line above against the frozen v1 receipt quoted above.
- (5) each invalid fixture matches a real v1-observable receipt shape — the three
  fixture READMEs under `.ufo/waves/round-45/fixtures/` name the committed
  provenance of every receipt field (the control/build receipts are byte copies of
  `.ufo/waves/round-44/verification/claim/after-final/tools/headtail-V1.json` and
  `after-final/build-1.json`).

Do-nothing control: the frozen v1 driver itself cannot reach the after-state — it
accepts all three classes (the before receipts above). Junk control: the honest
fixture cohort certifies green under both drivers (`.ufo/waves/round-45/verification/hardening/before/honest/summary.json`,
sha256 `9af97d72bf19f4bdc7bcf09574926d802b303f7c7c7b8becebe319116106b20d`, `ok=true`).
```

---

## Append block B — C2 measurement (to be appended after block A)

```markdown
### Round 45 — C2 measurement (appended after the freeze; the declaration above is not edited)

Measured commit: `{{MEASURED_COMMIT}}`. Counting command (frozen, verbatim):

    python3 -B .ufo/waves/round-45/c45_freshness.py

(a) Selftest mutant coverage **2/4 → 4/4** on the same four reconstructed
witness-class mutants m1–m4 (`.ufo/waves/round-45/mutants/m1.py`–`m4.py`, each a
copy of the frozen `.ufo/waves/round-44/c44_audit.py` with exactly one mutation,
target lines documented in `.ufo/waves/round-45/w1/ExecMutantMatrix.md`, sourced
from `.ufo/waves/round-44/w2/MutClassGate.md` §"The four mutants"). Before — the
shipped v1 selftest body kills m1 and m3 and leaves the timing-only mutant m2 and
the error mutant m4 alive (2/4): m1 exit 1, m2 exit 0, m3 exit 1, m4 exit 0
(receipts `.ufo/waves/round-45/verification/selftest-coverage/before/m{1..4}.txt`,
sha256 `0809aa629bdc4a09bb57a4c4af45fa210c527f421925b5d359c2d3dc714fc28f` m1,
`509fc8a23e761afdaf1032217e7343a155800cbec84e8a3768ad799db3153db1` m2 and m4,
`a4f12ee6594c557c2a00177976739cc02237ac12cb26009ed245c77b3a92c105` m3). After —
the v2 driver's shipped selftest kills 4/4: `{{C2_SELFTEST_AFTER_TABLE}}` (after
receipts `.ufo/waves/round-45/verification/selftest-coverage/after/m{1..4}.txt`;
v2 selftest stdout `SELFTEST PASS: v1 assertions plus timing-only, invalid
receipt, error-row, and build-count gates`, exit 0).

(b) v4-mode receipt predicate names class runs **true → false**. Before — the
committed round-44 v4 receipt
`.ufo/waves/round-44/verification/claim/v4-final/tools/headtail-V1.json`
(sha256 `9ecb33b1257798de007aa422b507faa6a6336c93f70364eaafcc0b9390dd6333`) records
`classesMode: "v4"`, `classRuns: []`, runs `A,B,C,D,E,F,T1,T2,T3,T4,T5` — yet its
predicate text names "the eleven v4 runs **and the ten class runs**". After — the
counter v6 `.ufo/waves/round-45/c45_count.py` (sha256
`ce8bf2353d4f008a987f6fb3b6d3677d2dbed98aaae274126c68f0a3cf622556`) in v4 mode
emits a receipt whose predicate names only the eleven v4 runs:
`{{C2_V4_PREDICATE_AFTER}}` (receipt `{{C2_V4_RECEIPT_PATH}}`, counter sha256
`{{C2_V4_COUNTER_SHA}}`, seed `{{C2_V4_SEED}}`; `classRuns` empty, no G-key in
`runs`). Kill rule (1) — v6 differs from the frozen v5 only in mode-conditional
predicate text and the corrected docstring header: hunk-classified diff
`.ufo/waves/round-45/v6diff/v5-v6.diff` (3 hunks: one docstring-header, two
predicate-text, zero OTHER), and the v5-mode predicate string is byte-identical to
the frozen v5 `PREDICATE`.

(c) Witness split filed. {{WITNESS_SPLIT_SENTENCE}}
```

### C2(c) witness split — receipt identity (for the L1 to choose; both candidates are quoted)

The frozen C2(c) leg says "the round-44 claim receipt's 27 witnessed controls
re-derive as 22 class-only + 1 mixed + 4 met". Two committed receipts exist and
they do not agree; the tuple and the receipt identity must be bound together.

Re-derivation command (same command for both receipts):

```sh
jq -r '.rows | {class_only: map(select(.met==false and (.classCaught|length)>0 and (.legacyCaught|length)==0))|length, mixed: map(select(.met==false and (.classCaught|length)>0 and (.legacyCaught|length)>0))|length, met: map(select(.met==true))|length, other: map(select(.met==false and (.classCaught|length)==0))|length}' <RECEIPT>
```

Verbatim measured outputs (this seat, read-only, at freeze `3b4c430a`):

```text
# .ufo/waves/round-44/verification/claim/after-final/after-v5.json  (sha256 9dead4d7d65d10f268f37efba185f12bb4f8e8942e8e81e98df4b1c8fdc076d1)
{
  "class_only": 26,
  "mixed": 1,
  "met": 0,
  "other": 0
}
# receipt self-reports: witnessed 27, notMet 27, build met 3/3, ok true

# .ufo/waves/round-44/verification/claim/after-v5.json  (sha256 2383efaee0fe67d04430127fd1cd40160726e4b9afd61068d43a816e84ce0902)
{
  "class_only": 22,
  "mixed": 1,
  "met": 4,
  "other": 0
}
# receipt self-reports: witnessed 23, notMet 23, build met 3/3, ok false
```

The `22/1/4` tuple belongs to the **earlier, 23-witness** round-44 receipt
`claim/after-v5.json` (the receipt whose row count the round-43 correction
described). The **final, 27-witness** claim receipt `claim/after-final/after-v5.json`
re-derives as `26/1/0/0`. The two candidates for the filed sentence:

- Candidate 1 (binds the tuple to the receipt that produces it — historical
  pre-G6-fix receipt, 23 witnesses):
  `The round-44 claim receipt .ufo/waves/round-44/verification/claim/after-v5.json (sha256 2383efae…), re-derived by jq -r '.rows | {class_only: map(select(.met==false and (.classCaught|length)>0 and (.legacyCaught|length)==0))|length, mixed: map(select(.met==false and (.classCaught|length)>0 and (.legacyCaught|length)>0))|length, met: map(select(.met==true))|length, other: map(select(.met==false and (.classCaught|length)==0))|length}', partitions its 27 rows as 22 class-only + 1 mixed + 4 met (self-reported witnessed 23/27, ok=false); the final 27-witness receipt .ufo/waves/round-44/verification/claim/after-final/after-v5.json (sha256 9dead4d7…) partitions the same 27 rows as 26 class-only + 1 mixed + 0 met.`
- Candidate 2 (binds the tuple to the final claim receipt the frozen text names —
  then the filed tuple is `26/1/0`, and the frozen `22/1/4` is superseded as a
  receipt-identity error, disclosed rather than silently re-labelled):
  `The round-44 claim receipt .ufo/waves/round-44/verification/claim/after-final/after-v5.json (sha256 9dead4d7…), re-derived by jq -r '.rows | {class_only: map(select(.met==false and (.classCaught|length)>0 and (.legacyCaught|length)==0))|length, mixed: map(select(.met==false and (.classCaught|length)>0 and (.legacyCaught|length)>0))|length, met: map(select(.met==true))|length, other: map(select(.met==false and (.classCaught|length)==0))|length}', partitions its 27 rows as 26 class-only + 1 mixed + 0 met (self-reported witnessed 27/27, ok=true); the earlier pre-G6-fix receipt .ufo/waves/round-44/verification/claim/after-v5.json (sha256 2383efae…) partitions 22 class-only + 1 mixed + 4 met (witnessed 23/27), and the round-45 frozen 22/1/4 figure belongs to that earlier receipt, not to this one.`

Both candidates are arithmetically true of the receipt they name; they differ in
which receipt the frozen sentence is read to mean. This seat does not choose: the
frozen sentence cannot be amended by a scribe, and the disposition is the L1's,
reported verbatim to the canonical judge. **Neither candidate asserts C2 MET.**

---

## Append block C — move-log row

The lane's move-log table is `SCORECARD.md` §"Move log" (header row `| Round |
Axis | Before | After | Evidence |`, rows currently ending at round 20). Rows
for rounds 21–44 were not written to that table; the later rounds record their
moves in the per-round sections instead. The row below is drafted for the L1 to
place in the same table (or to omit if the L1 keeps the round-45 move in the
per-round section only — the table's own history does not cover rounds 21+):

```markdown
| 45 | operability (**HOLD 10** — bounded evidenced move, no numeric rise) | frozen v1 audit driver accepted invalid-receipt witness/not-met credit: 3/3 invalid fixture classes (counter exit 2, note "tool absent", stale planted receipts) certified `ok=true` at `{{MEASURED_COMMIT}}`'s base `8ee2c8bf…` | driver v2 `.ufo/waves/round-45/c45_audit.py` accepts 0/3, each rejection named by defect class (`{{C1_AFTER_REJECTION_CLASSES}}`); honest round-44 cohort certification unchanged (witnessed 27/27, build 3/3, exit 0) | `.ufo/waves/round-45/verification/matrix/{before,after}.json`; `.ufo/waves/round-45/verification/hardening/before/`; `.ufo/waves/round-45/verification/honest-regression/after-v5-v2.json`; `.ufo/waves/round-45/verification/sha-guard/before.sha256` |
| 45 | freshness (**HOLD 10** — bounded evidenced move, no numeric rise) | shipped v1 `--selftest` killed 2/4 witness-class mutants (timing-only m2 and error m4 survived); the committed round-44 v4-mode receipt's predicate named the ten class runs v4 never executes; the round-44 witness split was filed from a receipt whose identity did not match the final claim receipt | v2 selftest kills 4/4 (`{{C2_SELFTEST_AFTER_TABLE}}`); counter v6 `.ufo/waves/round-45/c45_count.py` v4 receipt names only the eleven v4 runs (`{{C2_V4_PREDICATE_AFTER}}`); witness split filed with its receipt identity named — {{WITNESS_SPLIT_SENTENCE}} | `.ufo/waves/round-45/verification/selftest-coverage/{before,after}/m{{1..4}}.txt`; `{{C2_V4_RECEIPT_PATH}}`; `.ufo/waves/round-45/v6diff/v5-v6.diff`; `.ufo/waves/round-45/verification/witness-split/split.json` |
```

---

## Open items the L1 must dispose before landing (not placeholders in the prose — real blockers)

1. **C2(c) receipt identity** — see §"C2(c) witness split — receipt identity".
   The frozen text's `22/1/4` does not re-derive from the final claim receipt
   (`26/1/0`); it re-derives from the earlier 23-witness receipt. Reported, not
   silently re-labelled; the choice between the two candidates above is the L1's.
2. **Kill rule (1)/(4) — sha-guard drift.** The wave-1 end guard
   (`SentinelFrozen`) diffed `changed (exit 1)` against
   `.ufo/waves/round-45/verification/sha-guard/before.sha256` (483 → 484 guarded
   files). The only differing entries are Python bytecode caches under
   `.ufo/waves/round-44/classes/__pycache__/` (`g3_empty_path.cpython-314.pyc`
   `25ba8580…` → `ff0cbbc8…`, plus a new `g9_port_digits.cpython-314.pyc`
   `bb3b9b59…`). No frozen source file and neither guarded script differs, and
   `git diff --name-only HEAD -- .ufo/waves/round-44/` is empty (committed bytes
   unchanged). The L1 must decide the disposition (re-baseline vs. record as a
   bytecode-cache artifact); this seat does not bless a new baseline.
3. **Frozen C2 counting command has no builder.** `python3 -B
   .ufo/waves/round-45/c45_freshness.py` is the frozen command for C2, but no
   wave-1 seat in `.ufo/waves/round-45/w1-spec.json` is assigned to write it
   (the file is named once in the wave context and once in `make_w1_spec.py:52`
   only). As of this draft the file does not exist in the tree. The C2
   measurement block therefore has no executed command behind it until the L1
   assigns or writes it.
4. **C1 after-stage matrix receipt absent.** `.ufo/waves/round-45/verification/matrix/`
   does not exist yet; `ExecMatrixRunner` reported that it did not run
   `--stage before|after`. The before-state v1 outputs exist under
   `verification/hardening/before/`, so the before leg is evidenced per class,
   but the frozen single counting command has not been run.
5. **Honest-cohort v2 regression receipt absent.**
   `.ufo/waves/round-45/verification/honest-regression/after-v5-v2.json` was
   absent when `ExecRegressionHonest` ran (driver v2 did not exist yet); driver
   v2 has since landed, so the L1 can re-run
   `python3 -B .ufo/waves/round-45/c45_audit.py --root . --controls .ufo/waves/round-44/controls-27.tsv --counter .ufo/waves/round-44/c44_count_v5.py --classes v5 --expect witnessed --build-rev 020bc457 --build-runs 3 --workers 4 --out .ufo/waves/round-45/verification/honest-regression/after-v5-v2.json`.
6. **v6 v4 receipt absent.** `.ufo/waves/round-45/verification/v6v4/` does not
   exist; `ExecV4ReceiptV6` was blocked because `c45_count.py` did not exist at
   its start. The counter has since landed, so the L1 can run
   `python3 -B .ufo/waves/round-45/c45_count.py --root . --classes v4 --tool-file scripts/sitemap_audit.py --out .ufo/waves/round-45/verification/v6v4/counter-v4.json`.
7. **C2(a) after-state not measured.** `.ufo/waves/round-45/verification/selftest-coverage/after/`
   is empty: the four v2 mutant copies (`m{1..4}_v2.py`) were never written, so
   the `4/4` after figure is **unmeasured**, not passed.
8. **C1 "9 rejected rows" arithmetic.** The frozen C1 text says "distinct named
   error classes among the 9 rejected rows: 3 fixture classes × control + 3
   builds", but 3 × (control + 3 builds) = 12 rows, not 9.
   `c45_matrix.py` checks all 12 actual control/build rows and reports the number
   of distinct named classes (`rejections_named`). The landed prose must quote the
   measured `{{C1_REJECTED_ROW_COUNT}}` rather than the frozen "9".
9. **Scope bounds reported by the wave (not adjudicated here).** The wave recorded
   that the v2 receipt-validity gate is a *bounded* provenance check, not a proof
   of writer identity (self-reported `counterSha256` + mtime window + nonce
   manifest), with a 1-second mtime tolerance (`MTIME_EPS_NS`); and that the C1
   frozen sentence's "any control" / "over the invoked counter bytes" phrasing is
   stronger than the three fixture classes can establish. The measurement block
   above states only what the three fixtures and the honest cohort measure; the
   canonical judge owns the disposition.

## L1 landing checklist

- [ ] Fill every `{{…}}` from a receipt; no guess, no placeholder left in the text.
- [ ] Re-run `python3 -B scripts/ledger_latest_check.py --root .` after the
      SCORECARD edit → expect `3 figures, 0 mismatches`, exit 0.
- [ ] Confirm the landed append contains no `re-scored <N> of the 27` phrase and
      that `LOG.md` is untouched by the append.
- [ ] Re-run the sha guard end-to-end at the landing commit; record the
      disposition of item 2 above.
- [ ] Keep the append after the frozen declaration; do not edit `SCORECARD.md`
      lines 3628–3709.
