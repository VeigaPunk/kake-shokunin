# ReviewerC1Selftest — scoped review

Recommendation: **selftest passes, but its 26/26 result does not establish complete routed-defect regression coverage.** Three medium-severity test-design findings below; no frozen-counter false green demonstrated in this seat. Calibration correctness, attack-shape fidelity, fixture isolation, and test sensitivity are the reviewed axes. No admission/judgment issued.

## Findings (severity order)

### Medium — T4 does not reproduce the CriticClaims digest-consistent fabrication

At `/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-64/c64_calibration.py:374-389`, T4 copies the authentic full text and authentic ledger from BASE, then installs marker prose lacking both the substantive correction quote and criterion. This is a **real-blob + incomplete-prose control**, not the round-63 circular-text attack. `/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-63/w1/CriticClaims.md:41-53` specifies a hand-authored 155-byte text containing only the frozen quote, with ledger hashes recomputed to match it and correction prose quoting the actual span. The historical attack greens c63; this T4 does not.

Measured T4 committed text is 290480 bytes, sha256 `8b90d096d2653ce57025e25c5bee5c63df66692e15ef8579371032da6f542a69`; ledger is 1039 bytes, sha256 `5f48e26be27975ee55702cac1e1b20b61f3bd5906910c865f5192bd7e010c42d`. Running the actual c63 counter on T4 produced `quote_correction=0 criterion=0 lesson_gate=0 met=false`, exit 1 (full command/output below). Thus the claimed historical-attack differential is not exercised by this check. The frozen c64 pinning can reject an authentic reconstruction of that attack, but T4 is not that reconstruction.

Recommended next-round regression: reproduce the 155-byte fabricated rendering and recomputed ledger, establish c63 green on those same bytes, then c64 red with explicit pin-drift/met/exit assertions. Preserve this wave's frozen artifacts.

### Medium — no successful fixture: an always-reject counter passes 26/26

`/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-64/c64_calibration.py:349-419` contains no expected exit-0/met-true evaluation. T1/T8 expect 2; T2–T5 expect 1; T6/T7 are direct units. A scratch-only mutation adding `False and` at the beginning of the production `met` conjunction (`:268`) still returns selftest 26/26, exit 0. At T0, the frozen original returns `met=true` exit 0 while that mutant returns `met=false` exit 1, so the selftest cannot detect loss of its core successful behavior. This is suite-level vacuity, not a claim that every individual assertion is vacuous.

Recommended regression: a revision-contained valid fixture with both `met=true` and exit 0, plus the advertised base-negative differential. Do not count the current 26 checks as 26 independent end-to-end cases.

### Medium — three routed clauses lack discriminating negative coverage

The routed recipe is `/home/vgpnk/Projects/shokunin/kake-shokunin/corpus/lessons/round-63-verifier-spotcheck.md:142-148`: rerun extraction, gate disagreements/unresolved, bind located raw lines. Each of these scratch-only production mutants still yields 26/26, exit 0:

1. Remove `and unresolved == 0` from `met` (`/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-64/c64_calibration.py:270`). Existing T4 has unresolved=1 but multiple other components are false; T5 has unresolved=0 yet correction/criterion false. Neither isolates unresolved as the sole failing gate. Missing case: otherwise-valid tree with two recorded disagreements, yielding unresolved=1 and met=false.
2. Replace `out_text = mod.extract(blobs["raw"])` (`:226`) with reading the committed text blob. T4 checks the happy-path `recipe_rederive=1` token, but all valid bytes already agree; the circular-text attack is absent. This only removes the full-blob extraction; located derivation still calls the recipe. The demonstrated gap is specifically full retained-raw-to-committed-text derivation coverage.
3. Change the ledger/derived-range mismatch condition (`:241`) to `if False:`. T7 confirms the helper's correct answer on one real input, not that the production predicate rejects ledger mismatch. No selftest fixture mutates `locatedRawLines` to the routed M5 `6150-6156` value. Such mutation will also break the frozen ledger sha; its rejection should assert the pin failure, and helper/binding sensitivity should be tested separately.

These are **coverage weaknesses**, not proof that the frozen production gates are absent: their actual implementations are present at `:226-242,267-270`. Independently committed controls exist outside `--selftest`; this seat does not erase their evidence or infer a kill-rule breach from a test mutation.

## Assertion and isolation audit

- Exact frozen instrument sha256: `5489eb2f3ac498e0383d841c677f036231fbf6933717d8da447f3193ff088adf`, extracted via `git -C /home/vgpnk/Projects/shokunin/kake-shokunin show 4c8295fa5e3b628f1fdf3840299ae415c01849fb:.ufo/waves/round-64/c64_calibration.py` and hashed with Python hashlib. Diff scope: added 449-line file relative to base (git diff --stat).
- Check count is genuinely 26: T1 2, T2 3, T3 3, T4 9, T5 4, T6 2, T7 1, T8 2. `passed == total` is not reached for unavailable base blobs; that path exits 2 (`:343-345`), so no observed 0/0-success bug.
- Every subprocess scenario T1–T5/T8 pairs exit assertions with diagnostic/output assertions. T4/T5 explicitly require met=false. T2/T3 do not explicitly assert met=false, although canonical evaluate ties exit 1 to false (`:278`). T6/T7 are direct units, not subprocess output/exit tests. Therefore “26 checks” is accurate; “26 exit-code-and-token cases” would be inaccurate.
- Token checks use substring membership, not parsed fields (`:359-360,382-389`); e.g. `disagreements=1` would also match `disagreements=10`. No current false-positive fixture observed. T3's `Traceback` absence is redundant/weak alone, but is accompanied by exit=1 and specific pin-drift checks; junk recipe execution is bypassed by pins=0, not proven safe by this test.
- Base inputs are `git show`n from fixed BASE (`:342-346`), not worktree blob contents. Each evaluation reads its fixture revision with git show (`:193-204`). Child execution uses absolute `__file__` (`:332`), so source instrument identity is the file executing selftest, not a revision-selected counter; I used the verified frozen copy. No check found reading lane worktree evidence instead of committed inputs.
- Selftest does require its `--root` to contain BASE; it is not self-contained from just fixture files. That is an explicit prerequisite, not accidental worktree-state dependence. All test fixture repos were placed in this seat's scratch; `_fixture` checks repo toplevel before config/add/commit (`:295-303`).
- T7 uses `tempfile.mkdtemp` outside `--selftest-work` and never removes that individual directory (`:411`); evaluate also uses tempfile (`:222`). I explicitly set TMPDIR to this seat's scratch/tmp, then removed the entire scratch tree, so nothing escaped the assigned scratch. Default invocation would leak the T7 temporary directory. Treat this as low-severity cleanup risk, not a calibration false green.

## Reproduction evidence

All commands below ran with cwd `/fast/scratch/hyaku/kake-r64/ReviewerC1Selftest`, `TMPDIR=/fast/scratch/hyaku/kake-r64/ReviewerC1Selftest/tmp`, and `PYTHONDONTWRITEBYTECODE=1`. Script paths named mutants are newly created scratch-only copies of the frozen file, modified exactly as described above; the lane instrument was never modified. Python fixture creation executed the instrument's own checked git commands; no lane git mutation occurred.

### frozen

```text
$ python3 -B /fast/scratch/hyaku/kake-r64/ReviewerC1Selftest/c64_calibration.py --root /home/vgpnk/Projects/shokunin/kake-shokunin --selftest --selftest-work /fast/scratch/hyaku/kake-r64/ReviewerC1Selftest/fixtures
check t1 exit2: pass
check t1 token: pass
check t2 exit1: pass
check t2 disagreements: pass
check t2 pins0: pass
check t3 exit1: pass
check t3 drift: pass
check t3 nocrash: pass
check t4 exit1: pass
check t4 pins1: pass
check t4 recipe1: pass
check t4 class1: pass
check t4 located: pass
check t4 qcorr0: pass
check t4 gate0: pass
check t4 unresolved: pass
check t4 metfalse: pass
check t5 exit1: pass
check t5 gate1: pass
check t5 unresolved0: pass
check t5 metfalse: pass
check t6 guard: pass
check t6 notlist: pass
check t7 located: pass
check t8 exit2: pass
check t8 token: pass
selftest 26/26
exit=0
stderr=''
```

### always-reject

```text
$ python3 -B /fast/scratch/hyaku/kake-r64/ReviewerC1Selftest/always-reject.py --root /home/vgpnk/Projects/shokunin/kake-shokunin --selftest --selftest-work /fast/scratch/hyaku/kake-r64/ReviewerC1Selftest/always-reject
[stdout byte-identical to frozen selftest block above: all 26 named checks pass]
selftest 26/26
exit=0
stderr=''
```

### ungated-unresolved

```text
$ python3 -B /fast/scratch/hyaku/kake-r64/ReviewerC1Selftest/ungated-unresolved.py --root /home/vgpnk/Projects/shokunin/kake-shokunin --selftest --selftest-work /fast/scratch/hyaku/kake-r64/ReviewerC1Selftest/ungated-unresolved
[stdout byte-identical to frozen selftest block above: all 26 named checks pass]
selftest 26/26
exit=0
stderr=''
```

### c63-on-t4

```text
$ python3 -B /fast/scratch/hyaku/kake-r64/ReviewerC1Selftest/c63_calibration.py --root /fast/scratch/hyaku/kake-r64/ReviewerC1Selftest/fixtures/t4-fabrication --revision 45de3279bab54bd0245f53a3697621f1918cf889
revision=45de3279bab54bd0245f53a3697621f1918cf889 disagreements=1 quote_correction=0 blobs_match=1 derived=collapsed-only class_match=1 criterion=0 lesson_gate=0 source_row=1 unresolved=1 met=false
exit=1
stderr=''
```

### skip-full-extraction

```text
$ python3 -B /fast/scratch/hyaku/kake-r64/ReviewerC1Selftest/skip-full-extraction.py --root /home/vgpnk/Projects/shokunin/kake-shokunin --selftest --selftest-work /fast/scratch/hyaku/kake-r64/ReviewerC1Selftest/skip-full-extraction
[stdout byte-identical to frozen selftest block above: all 26 named checks pass]
selftest 26/26
exit=0
stderr=''
```

### skip-located-binding

```text
$ python3 -B /fast/scratch/hyaku/kake-r64/ReviewerC1Selftest/skip-located-binding.py --root /home/vgpnk/Projects/shokunin/kake-shokunin --selftest --selftest-work /fast/scratch/hyaku/kake-r64/ReviewerC1Selftest/skip-located-binding
[stdout byte-identical to frozen selftest block above: all 26 named checks pass]
selftest 26/26
exit=0
stderr=''
```

### frozen-t0

```text
$ python3 -B /fast/scratch/hyaku/kake-r64/ReviewerC1Selftest/c64_calibration.py --root /home/vgpnk/Projects/shokunin/kake-shokunin --revision 4c8295fa5e3b628f1fdf3840299ae415c01849fb
revision=4c8295fa5e3b628f1fdf3840299ae415c01849fb disagreements=1 pins=1 pin_drift=none recipe_rederive=1 ledger_state=ok derived=collapsed-only class_match=1 located=6150-6154 quote_correction=1 criterion=1 lesson_gate=1 source_row=1 unresolved=0 met=true
exit=0
stderr=''
```

### always-reject-t0

```text
$ python3 -B /fast/scratch/hyaku/kake-r64/ReviewerC1Selftest/always-reject.py --root /home/vgpnk/Projects/shokunin/kake-shokunin --revision 4c8295fa5e3b628f1fdf3840299ae415c01849fb
revision=4c8295fa5e3b628f1fdf3840299ae415c01849fb disagreements=1 pins=1 pin_drift=none recipe_rederive=1 ledger_state=ok derived=collapsed-only class_match=1 located=6150-6154 quote_correction=1 criterion=1 lesson_gate=1 source_row=1 unresolved=0 met=false
exit=1
stderr=''
```

## Residual risk / verification gaps

LSP device is unavailable: `read xd://lsp` returned “No such tool: xd://lsp”; no server-status/reference/definition/diagnostics route exists here. Review used frozen source, literal searches, direct fixture runs and scratch mutation sensitivity, not semantic-reference proof. Scope is this calibration selftest, not C2/C3 or all external control receipts. No alternate runtime, integration, admission, or ship action performed. No tools installed/updated.

Self-evaluation: accuracy 4/5 (direct outputs; no exhaustive mutation proof), completeness 4/5 (all requested selftest axes covered; external controls intentionally outside seat), clarity 4/5 (findings separated from frozen-counter verdict), actionability 4/5 (specific next-round discriminating cases), conciseness 4/5 (full original output retained for evidence). Overall 4.0/5; highest-value improvement is adding an authentic historical fabrication differential and one otherwise-valid positive fixture. User should agree the report distinguishes evidence gaps from a counter falsification.

Cleanup: `/fast/scratch/hyaku/kake-r64/ReviewerC1Selftest` removed; existence check false. Only the assigned report is retained.
