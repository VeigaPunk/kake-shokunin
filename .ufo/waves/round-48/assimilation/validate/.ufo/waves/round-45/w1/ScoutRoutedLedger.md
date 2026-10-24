# ScoutRoutedLedger — round 45 wave 1

Seat: `kake-r45.ScoutRoutedLedger`. Axes: **operability**, **freshness**.
Named task: one routed-defect table, each cited file:line checked against current bytes.
Result: **PASS** on cite verification (every named defect is still in the bytes, at the lines below).
**FAIL** on frozen C2(c) arithmetic: `22 class-only + 1 mixed + 4 met` does not re-derive from the closure claim receipt.

LSP: `xd://lsp` is not mounted (devices: `ast_edit`, `debug`). These cites are markdown and Python source lines, not symbols. Proof is the file bytes. No tool installed (pacman paused; python3 already present).

Frozen hashes, re-measured this seat (match the declared pins):

```text
8ee2c8bf9333206963236b023048ae2b560bbec703adef4d448bd5529c2d0c75  .ufo/waves/round-44/c44_audit.py
5cedaa3b9f918979447f2e18c054d42a65bfc79fe700be7f2272d69dbe7672bc  .ufo/waves/round-44/c44_count_v5.py
```

`c44_audit.py` and `c44_count_v5.py` line numbers in the round-44 reports still match. SCORECARD cites drifted (content inserted above them). Current lines are the ones in the table.

## Ledger

| id | defect | sev | evidence (current line) | minimal fix shape | absorbs |
|---|---|---|---|---|---|
| 1a | Exit-2 counter-error receipt can still be a class witness. `semantic_witness` / `expectation_ok` never read `exit`. A `CannotEvaluate` during a later T run leaves earlier G rows in `runs` with `met` still false. | HIGH | `c44_audit.py:63-66` (witness), `:73` and `:80-81` (not-met), `:157-160` (row stores `exit` and drops `note`). Counter: `c44_count_v5.py:1047-1050` (G before T), `:1097-1098` (raise inside T, before this iteration's store), `:1108` (store on prior iterations), `:1114-1119` (`finish(2)`). Kill rule (2) text is now `SCORECARD.md:3459-3461`, not the report's `:3454-3458` (that range is now the skip-work control, `:3454-3457`). | Driver v2: if receipt `exit` is not 0 or 1, do not count the row as a witness and do not count it as not-met. | **C1 (i)** |
| 1b | `note: "tool absent"` receipt (exit 1, every run `equal: false`) is a witness on every class key. The audit never copies `note`. | HIGH | Counter `:1031-1034` (`cand=None`), `:1078-1080` (`equal` false, `candExit` `"tool absent"`), `:1113` (`note`), `:1120` (exit 1). Audit `:147` sha-checks, then the counter opens the tool itself at `:1032`. Audit `:157-160` has no `note` field. `c44_audit.py` has no `rec["note"]` read. | Copy `note` onto the audit row. Refuse witness and not-met credit when `note == "tool absent"`. | **C1 (ii)** |
| 1c | A receipt already on disk is loaded even when this invocation did not write it (`returncode` ignored; no mtime; no counter-byte pin on the loaded JSON). | HIGH | `c44_audit.py:56-60` loads `out` whenever it parses. `:157` records `exit` and still feeds `met` / `caughtBy` into the gate at `:77-79`. | Refuse credit unless the receipt file's mtime is inside this driver's run window and the receipt's `counterSha256` is the invoked counter. | **C1 (iii)** |
| 2 | `--expect not-met` treats an exit-2 `CannotEvaluate` receipt (`met: false`, `error` null because a JSON file exists) as not-met. | MEDIUM | `c44_audit.py:73`, `:80-81`, `:160` (`error` is null when `rec` loaded). Same `finish(2)` path as 1a (`c44_count_v5.py:1114-1119`). | Same gate as 1a: exit other than 0/1 is neither a witness nor not-met. | **C1 (i)** — the frozen sentence covers not-met as well as witness; the round-44 routing paragraph named only 1a/1b/1c. |
| 3 | `--expect witnessed` does not pin three build runs. `bool(build)` is enough; `--build-runs 1` is green. | MEDIUM | `c44_audit.py:77-79`, `:116` (default 0), `:172`, `:181-182`. Round-44 kill rule (3) "three unseeded runs" is claim text at `SCORECARD.md:3461-3462`, not an instrument check. | Not in the frozen C1 sentence. A pin would be `len(build)==3` inside `expectation_ok`. Do not smuggle it into v2 unless the L1 amends C1. | **neither** |
| 4 | `--expect blind` still requires every control `met is True` (the universal v4-blindness reading the freeze rejected). | LOW | `c44_audit.py:74-76`. Rejected reading is now `SCORECARD.md:3567-3571` (report cited `:3562-3570`; `:3562-3565` is now correction 2 item 3). Direction is false-red only. | Leave it, or stop requiring `all(met)` under `--classes v4`. Not a C1/C2 success criterion. | **neither** |
| 5 | Missing controls, bad TSV, timeout, and directory-as-control traceback to exit 1, same as a failed predicate. Only `ap.error` is exit 2. | LOW | `c44_audit.py:54` (900s, uncaught), `:126` (the only exit 2), `:132-133`, `:137-141`, `:222`. | Map instrument failures to exit 2 and still write a summary. Not in C1/C2. | **neither** |
| N1 | `witnessedByClass` stores full `caughtBy`, not the class subset. | nit | `c44_audit.py:192` vs the split at `:199-200`. | Emit the class subset, or leave it (no gate effect). | **neither** |
| N2 | Duplicate TSV `name` values clobber `tools/<name>.json`. | nit | `c44_audit.py:148`. Unique in `controls-27.tsv` today. | Reject duplicate names. | **neither** |
| N3 | `--classes v5 --expect blind` is legal and is not a declared command. | nit | `c44_audit.py:113-114`. | Reject that pair, or leave it. | **neither** |
| M-cov | Shipped v1 `--selftest` kills m1 and m3 only. m2 (timing-only witness) and m4 (error witness) survive: the body has no `T*` row and no `error` key, while the pass line claims timing-only coverage. Correction 2 also claims a timing-only row that is not in the function. | HIGH | `c44_audit.py:84-103` fixtures; `:104` pass line. No `T1` and no `error` key in that body (this seat's extract). Mutants, from `MutClassGate.md:69-86`: m1 `any`→`all` on the class-key test (`:66`); m2 add `T1`–`T5`; m3 add `A`–`F`; m4 `if row.get("error"): return True` before the class-key test. Overclaim: `SCORECARD.md:3553-3554`. | In v2 `selftest`, add one `caughtBy: ["T1"]` row and one `error` row; assert neither is a witness. Do not edit frozen `c44_audit.py`. | **C2 (a)** |
| H-pred | v4-mode receipt predicate names ten class runs v4 does not execute. | HIGH | Source: `c44_count_v5.py:82-84` (`PREDICATE`), `:996` (unconditional), `:1001` (`classRuns: []` in v4), `:1046` (`classes={}`), `:1049` (no G insert). Committed receipt: `verification/claim/v4-final/v4.json:7` (same sentence, `classesMode` v4, `classKeys` `[]`, `witnessed` 0) and `v4-final/tools/portlen-v1.json` (`classRuns` `[]`, run keys exactly `A B C D E F T1 T2 T3 T4 T5`, predicate contains "ten class runs"). | v6: v4-mode predicate names only the eleven v4 runs. v5-mode predicate string stays byte-identical. | **C2 (b)** |
| H-doc | Docstring says "Round-43 version 4 header follows"; the next header is the Round-42 version 3 header. | LOW | `c44_count_v5.py:11` then `:13`. | One docstring line: say the Round-42 version 3 header follows. Allowed v6 hunk. The MET triple does not score this string. | **C2** kill rule 1 (`SCORECARD.md:3703-3705`), not the MET triple |
| H-schema | v4 receipts gained `classesMode` and `classRuns`. `classRuns: []` is true; the fields are not the false predicate. | LOW | `c44_count_v5.py:1000-1001`. Confirmed empty on the v4 tool receipt above. | Do not remove them in v6. Kill rule 1 allows only predicate text and the docstring header. | **neither** |
| H-cli | Omitted `--classes` now defaults to v5. Explicit `--classes v4` still runs the eleven v4 runs. | LOW | `c44_count_v5.py:989-991`. | Do not change the default in v6 (same kill rule). | **neither** |
| MX | One mixed row is a class witness. On the closure claim receipt the legacy key is timing `T5` only (`C.equal` is true). The critic's stronger shape (legacy `C` and `T5`) is a different, earlier receipt. | MEDIUM | Claim receipt `verification/claim/after-final/after-v5.json`: `repeat-len-band` `classCaught=["G7"]`, `legacyCaught=["T5"]`, `caughtBy=["G7","T5"]`. Tool `after-final/tools/repeat-len-band.json`: seed `187926495163792`, `C.equal true`, `G7.equal false`, `T5.equal false`. Classifier that counts it: `c44_audit.py:63-66` and `:152-156`. Critic receipt (not the closure claim): `verification/claim/after-v5.json` seed `187179068777863`, `legacyCaught ["C","T5"]`. Amended reading that this does not violate: `SCORECARD.md:3567-3571`. | File the split from the closure receipt. Do not describe that mixed row as a v4-run `C` divergence. | **C2 (c)** intends this caveat. The frozen numbers do not match — see MX-arith. |
| MX-arith | Frozen C2(c) says the claim receipt's 27 witnessed controls re-derive as 22 class-only + 1 mixed + 4 met, and MET iff `22/1/4`. That split is the earlier receipt's control partition (23 witnessed, `ok` false), not the closure receipt. | HIGH | `SCORECARD.md:3679`, `:3687-3688`, `:3694`, `:3701`. Re-derive below. `22+1+4=27` counts controls, not witnesses, on `verification/claim/after-v5.json` (`witnessed=23`, `ok=false`, met = the four casememo rows). Closure receipt `after-final/after-v5.json` is `witnessed=27`, `ok=true`, **26 class-only + 1 mixed + 0 met**. The four casememo rows are class-only `G6` witnesses there, not met. | L1 only: do not file `22/1/4` against `after-final/after-v5.json`. Label `22/1/4` as `verification/claim/after-v5.json`. The closure claim receipt is `26 class-only + 1 mixed (repeat-len-band, G7+T5) + 0 met`. This seat did not edit SCORECARD. | **neither** — the frozen sentence is the stale count. C2(c) as written cannot be made true of the closure receipt without amending the sentence. |
| S131 | S131 anchor and teaches still say ReviewFreeze.md "first paragraph and §1". §1 does not contain the sha256 quote. | LOW | `corpus/SOURCES.md:139` and `corpus/lessons/round-44.md:18` (both the anchor and the teaches cell). Quote is `ReviewFreeze.md:5` (`## Verdict`). §1 heading is `ReviewFreeze.md:9`; its first prose line `:11` is the diff command, and the quote is absent from that section. | Append-only: a new superseding row whose anchor drops "and §1". Do not edit the filed S131 bytes. | **neither** |
| S130 | `claim-count-derivation.md` still declares `source: S130` after S132 superseded S130. | LOW | `corpus/knowledge/claim-count-derivation.md:1`. Superseding row `corpus/SOURCES.md:140` (`teaches` opens `supersedes S130 —`). S130 itself remains at `SOURCES.md:138`. | Append a provenance line that the method citation now resolves through S132. Corpus is L1-write-only this wave. | **neither** |
| SUP | `supersedes S0NN —` is not machine-checked for own-work rows. E04 reads the marker only when the source cell has an `https?://` URL. | MEDIUM | `scripts/sources-census.sh:600-603` (`url_of` matches only `https?://`), `:646-649` (E04 requires `u!=""`). Scribe mutant note: `w2/ScribeSourcesRows.md:115-120`. Census not re-run this seat. | Fleet-script change, out of lane scope: apply the supersedes requirement to duplicate own-work paths, not only duplicate URLs. | **neither** |
| OBS1 | Round-44 Gate logged no reject, so a reject spot-check cannot be sampled. | LOW | `corpus/lessons/round-44.md:9-10` (two admit rows). Spotcheck `:104-105`. | Next Gate logs rejects. Not a C1/C2 repair. | **neither** |
| OBS2 | The ≤25-word Gate quotes for S131/S132 are filed on the S129/S130 rows, not labeled on the new rows. | LOW | `corpus/lessons/round-44.md:9-10` vs `:18-19`. Spotcheck `:106-108`. | Label the next Gate's quotes on the new row ids. | **neither** |

## Decisive re-derive (this seat)

```text
8ee2c8bf9333206963236b023048ae2b560bbec703adef4d448bd5529c2d0c75  .ufo/waves/round-44/c44_audit.py
5cedaa3b9f918979447f2e18c054d42a65bfc79fe700be7f2272d69dbe7672bc  .ufo/waves/round-44/c44_count_v5.py

.ufo/waves/round-44/verification/claim/after-v5.json
  controls 27 witnessed 23 ok False notMet 23
  class_only 22 mixed 1 ['repeat-len-band'] met 4 other 0
.ufo/waves/round-44/verification/claim/after-final/after-v5.json
  controls 27 witnessed 27 ok True notMet 27
  class_only 26 mixed 1 ['repeat-len-band'] met 0 other 0
v4-summary classesMode v4 classKeys [] witnessed 0 predicate_has_ten True
v4-tool classesMode v4 classRuns [] runKeys ['A', 'B', 'C', 'D', 'E', 'F', 'T1', 'T2', 'T3', 'T4', 'T5'] ten_class True
selftest_has_T1 False selftest_has_error_key False
selftest_line104     print("SELFTEST PASS: class and mixed-key witnesses pass, legacy/timing-only and no-class witnesses fail")
```

`after-v5.json` is the receipt `CriticC1Predicate` jq'd (`22/1/4`, witnessed 23). `after-final/after-v5.json` is the receipt the round-44 closure verified as C1 met (`witnessed=27/27`, `ok=true`). Same jq, different split. v4 predicate text is not only a source inference; it is in the committed v4 receipt.

## What C1 and C2 actually absorb

- **C1** absorbs 1a, 1b, 1c, and defect 2 (the not-met side of exit≠0/1). It does not pin build-run count, blind-mode, or exit-2-for-instrument-failure.
- **C2 (a)** absorbs the m2/m4 selftest gap. **C2 (b)** absorbs the false v4 predicate sentence. The docstring label is an allowed v6 hunk (kill rule 1), not a MET number. **C2 (c)** names the mixed-witness caveat but its frozen `22/1/4` is the pre-final receipt. The closure receipt is **26 / 1 / 0**.
- **neither:** build-count pin, blind clause, exit-code conflation, the three nits, v4 schema fields, CLI default, S131 "and §1", `source: S130`, supersedes-marker gap, the two spotcheck observations.

## Cite drift (SCORECARD only)

| report cite | what is there now | where the cited text is now |
|---|---|---|
| kill rules `3454-3458` | skip-work control `3454-3457` | kill rules `3459-3463` |
| capability `3460-3462` | inside the kill-rule paragraph | capability row `3465-3467` |
| amendment A `3510-3523` | C2 sourced line, then the amendment heading | heading `3511`, body A `3513-3529` |
| predicate reading `3562-3570` | correction 2 item 3 through `3565` | predicate reading `3567-3576`; the clause sentence is `3567-3571` |

## Files written

- `.ufo/waves/round-45/w1/ScoutRoutedLedger.md` (this report)
- Directory created: `/fast/scratch/hyaku/kake-r45/ScoutRoutedLedger/` (empty; no scratch file kept)

## Unrun

`c44_audit.py --selftest` (coverage judged from the function body, not a mutant run), sources census, counter/v6, C1 matrix. No blockers. No installs.
