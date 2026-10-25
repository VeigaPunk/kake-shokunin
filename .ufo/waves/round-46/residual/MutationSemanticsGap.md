# MutationSemanticsGap — C1 decision-semantics mutation probe

| | |
|---|---|
| Wave | `kake-r46-residual` (round-46 residual attack wave) |
| Seat | `MutationSemanticsGap` (mutation-tester) |
| Lane repo | `/home/vgpnk/Projects/shokunin/kake-shokunin` (read-only) |
| Scratch | `/fast/scratch/hyaku/kake-r46-residual/MutationSemanticsGap/` |
| Claims probed | C1 `scripts/redirect_audit.py` + sealed counter `.ufo/waves/round-46/c46_matrix.py` |
| Receipts reconciled | `verification/c1-before-7cdbaefd.json`, `verification/c1-after-ee43e66.json` |
| Date | 2026-10-24 |

## Verdict

**3/3 new decision-logic mutants SURVIVED both detectors** (the sealed matrix at
`--stage after` and the in-file `--selftest`). The C1 oracle cannot distinguish
the committed splat / percent-decode / placeholder semantics from three plausible
wrong implementations. This is an oracle-coverage finding: counterfactual runs
(same sealed counter, same mutant, plus one correct-world fixture each) kill all
three with `clean_false_positives=1 → MATRIX_AFTER_FAIL`, so the detector wiring
works and the witness set is what is thin.

The committed tool itself still matches its docstring; no contract change is
implied, and none was made.

## Detectors and the kill criterion

Sealed matrix (`.ufo/waves/round-46/c46_matrix.py:168-205`), stage `after`:
exit 0 iff `tool_present and witnesses_caught == 11 and clean_false_positives == 0
and controls_accepted == 0 and wall_s < 120`. A witness row is
`{"caught": <exit==1 and verdict=="failed-policy">, "exit", "findings": <count>}` —
**decided outcome content is never compared**. Controls must not reproduce the
after-state.

In-file selftest (`scripts/redirect_audit.py:464-572`): fixed 11 FLAG witnesses
must be flagged, 3 CLEAN witnesses must not be, 6 in-memory knobs must diverge
on one paired witness each, plus CLI positive/negative/bad-input controls.

Kill = matrix exits 1 (`MATRIX_AFTER_FAIL`) **or** selftest exits non-zero on the
mutated bytes. Baseline failure would have been inconclusive; there was none.

## Baseline (pristine bytes)

Sealed tool bytes are identical at tip and at the measured revision:
`git show ee43e66:scripts/redirect_audit.py` vs lane file → identical;
sha256 `1e1dff18030c9028d833ab108bff140102343f4c5198c35984e7838e54bb748a`.
Counter sha256 `7335b001f8a6860fef4d268eecdaac8710aa0224006586ea8435ab292b102164`.

Scratch repo `repo/` built with `git archive ee43e66 scripts/redirect_audit.py
.ufo/waves/round-46/c46_matrix.py .ufo/waves/round-46/fixtures | tar -x`,
`git init` + commit → pristine commit `3d7b56d7b8de5ec213302a0e3a0dfbd990540e0e`.

```
$ python3 -B scripts/redirect_audit.py --selftest        # exit 0
selftest: 23/23 passed

$ python3 -B <lane>/.ufo/waves/round-46/c46_matrix.py \
    --root <scratch>/repo --revision 3d7b56d7... --stage after
stage=after witnesses_caught=11/11 clean_false_positives=0 controls_accepted=0 \
wall_s=0.914 MATRIX_AFTER_PASS                            # exit 0
```

Receipt reconciliation: scratch `witnesses.rows` and `clean.rows` are **equal**
to the filed `c1-after-ee43e66.json` rows; tool sha and counter sha equal the
filed values; only `revision` (scratch subtree commit) and `wall_s` differ.

## Mutants

Each mutant is a minimal source edit in the scratch repo, committed as its own
revision; fixtures and controls are untouched. Probe manifests are *correct
worlds* under committed semantics (pristine exits 0/clean on all three), so a
mutant flagging them is a measurable false positive.

| # | Mutant | Changed lines | Tool sha256 | Probe | Selftest | Matrix after | Verdict |
|---|---|---|---|---|---|---|---|
| M1 | `m1_lazy_splat` | 1 | `d67dcd3be9ae7d49f4669d5e3284a48110b29f1b4b823d01e4831bd0bb0057f6` | `p1_lazy_splat` | exit 0, 23/23 | exit 0, `MATRIX_AFTER_PASS`, 11/11, FP 0 | **SURVIVED** |
| M2 | `m2_double_decode` | 1 | `6eb4c9b4b6e6f67868a891cc621bc03446f092a889dc19f38c38e2cf7775a733` | `p2_double_decode` | exit 0, 23/23 | exit 0, `MATRIX_AFTER_PASS`, 11/11, FP 0 | **SURVIVED** |
| M3 | `m3_splat_name_collision` | 2 | `b488c53aa4f51bb38f8d744e22ce9c0268815933bc3fd6f49198b09f31520f05` | `p3_splat_name` | exit 0, 23/23 | exit 0, `MATRIX_AFTER_PASS`, 11/11, FP 0 | **SURVIVED** |

### M1 — greedy suffix capture made lazy (one path segment)

`_match_source`, wildcard branch (`scripts/redirect_audit.py:125-130`):

```diff
         if path.startswith(stem):
-            return {"splat": path[len(stem):]}
+            return {"splat": path[len(stem):].split("/", 1)[0]}
```

Plausible defect: many routers implement `*` as a single-segment splat; the v1
contract says a terminal `*` matches *any* suffix (multi-segment).

Behavior delta (mutant rev `8305ad20c839900fdd7c7cbe80b7b134830aee4c`):

- Existing witness `w4_splat_destination` still exits 1/failed-policy — but with
  a **different decided value**: committed
  `{"action":"redirect","status":301,"location":"https://blog.example.com/a/b"}`,
  mutant `{"location":"https://blog.example.com/a"}`. Its expectation
  (`.../a/b/c`) is deliberately wrong by more than the truncation, so
  differentially the mutant is invisible; the matrix row
  `{"caught":true,"exit":1,"findings":1}` is **byte-identical** to pristine's.
- Probe `p1_lazy_splat` (correct world): rule `/* → /archive/:splat`, request
  `/a/b`, expect `/archive/a/b`. Committed: clean (exit 0). Mutant: exit 1,
  decided `/archive/a`.
- All 3 clean fixtures and the other 10 witnesses: reports identical to pristine.

Expected detector that would kill it: a **clean-world** fixture whose splat
spans at least two segments and whose destination must preserve them intact.
The witness set has no such case. The matrix's row schema (exit/verdict/count)
also discards the only signal M1 produces on `w4`.

### M2 — percent-decode applied twice

`decide` (`scripts/redirect_audit.py:171`):

```diff
-    path = urllib.parse.unquote(request_path, encoding="utf-8", errors="replace") if url_decode else request_path
+    path = urllib.parse.unquote(urllib.parse.unquote(request_path, encoding="utf-8", errors="replace"), encoding="utf-8", errors="replace") if url_decode else request_path
```

Plausible defect: frameworks that decode at the edge and again in the router
(the classic double-decode traversal bug). Contract says decode once.

Behavior delta (mutant rev `a3b146be6175a061d60a9e39310282e2c9322738`):

- **All 14 sealed fixtures produce reports identical to pristine**; witness and
  clean rows in the receipt are unchanged.
- Probe `p2_double_decode` (correct world): rule `/a b → /x`, request
  `/a%2520b`, expect `{"action":"none"}` (single decode yields `/a%20b`, no
  match). Committed: clean. Mutant: exit 1, decided redirect `/x` — i.e. it
  matches a rule the real host would not (and symmetrically would resolve
  `%252e%252e` to `..`).

Expected detector: a double-encoded request path. The only decode witness is
`c6_encoded_path` + the boolean `skip_url_decoding` knob, which probes the
*under*-decode direction only. The over-decode direction has no fixture in
either detector.

### M3 — placeholder named `splat` collides with the reserved splat key

`_match_source`, placeholder branch (`scripts/redirect_audit.py:139-142`):

```diff
         if s_part.startswith(":"):
             if p_part == "":
                 return None
-            captured[s_part[1:]] = p_part
+            if s_part[1:] != "splat":
+                captured[s_part[1:]] = p_part
```

Plausible defect: a maintainer protecting the reserved key `"splat"` from being
overwritten by a publisher-authored `:splat` placeholder — plausible because
`captured` is initialised as `{"splat": None}` and an exact `:splat` placeholder
does overwrite it in committed code (so a `*` in that destination is also
substituted; the collision is real and under-specified in both directions).

Behavior delta (mutant rev `6b41f0415ddf7f7abe4c716e6e58583709f8efc9`):

- All 14 sealed fixtures identical to pristine.
- Probe `p3_splat_name` (correct world): rule `/x/:splat → /y/:splat`, request
  `/x/v`, expect `/y/v`. Committed: clean (expands `/y/v`). Mutant: exit 1,
  decided location `/y/:splat` (literal).

Expected detector: a `:splat`-named exact placeholder in a source. The only
`:splat` in the oracle is a *destination* token under a wildcard source (`w4`),
which never exercises the reserved-name collision.

## Counterfactual kill proof

To show the detectors are capable and the gap is the oracle, the same sealed
counter was run over a clone (`repo-probe/`) whose *measured revision* also
contains the three probe manifests as fixtures, with the working-tree
`index.json` extended by three `clean` rows. (Mechanics: the counter reads the
index from `--root` — `c46_matrix.py:122` — but runs manifests/controls from the
extracted revision — `:145,:159,:171,:178,:183`; the docstring's "fixtures live
in the working tree" comment does not match those call sites. That mismatch is
noted for the matrix-blindness seat; the probe commits work around it.)

| Measured revision | Probes in oracle | Matrix after | Clean FP | Flagged row |
|---|---|---|---|---|
| `6a8004c8` (pristine + probes) | p1, p2, p3 | exit 0 `MATRIX_AFTER_PASS` | 0 | — |
| `32addc43` (M1 + probes) | p1, p2, p3 | exit 1 `MATRIX_AFTER_FAIL` | 1 | `p1_lazy_splat` (`exit:1`) |
| `e45a4d85` (M2 + probes) | p1, p2, p3 | exit 1 `MATRIX_AFTER_FAIL` | 1 | `p2_double_decode` (`exit:1`) |
| `ef99a912` (M3 + probes) | p1, p2, p3 | exit 1 `MATRIX_AFTER_FAIL` | 1 | `p3_splat_name` (`exit:1`) |

Pristine passes the widened oracle; each mutant fails its matching row. Kill
capability exists; the sealed 14-fixture oracle simply contains no member of
these three semantic classes.

Probe bodies (each is a valid v1 manifest, clean under committed semantics):

```json
p1: {"version":1,"resourcePrecedence":true,"defaultStatus":301,
     "rules":[{"source":"/*","destination":"/archive/:splat","action":"redirect","status":301}],
     "checks":[{"id":"c1","path":"/a/b","expect":{"action":"redirect","status":301,"location":"/archive/a/b"}}]}
p2: {"version":1,"resourcePrecedence":true,"defaultStatus":301,
     "rules":[{"source":"/a b","destination":"/x","action":"redirect","status":301}],
     "checks":[{"id":"c1","path":"/a%2520b","expect":{"action":"none"}}]}
p3: {"version":1,"resourcePrecedence":true,"defaultStatus":301,
     "rules":[{"source":"/x/:splat","destination":"/y/:splat","action":"redirect","status":301}],
     "checks":[{"id":"c1","path":"/x/v","expect":{"action":"redirect","status":301,"location":"/y/v"}}]}
```

## Finding and minimal repair

**Finding (surviving mutants = coverage gap):** the C1 detector set certifies
"every planted witness caught / no false positive", but it does not constrain
three behavior-bearing semantics that the tool's own docstring specifies:
multi-segment splat capture, decode-once, and `:name` capture under the
reserved name `splat`. A wrong implementation of any one of them passes
`MATRIX_AFTER_PASS` and `--selftest`.

Minimal repair, in increasing strength — the first is sufficient for all three:

1. Add `p1_lazy_splat`, `p2_double_decode`, `p3_splat_name` to the `clean`
   fixture set (committed manifests + `index.json` rows). Each mutant then
   fails the matrix's clean-FP leg (proven above: `MATRIX_AFTER_FAIL`). The
   same three as CLEAN witnesses in `_witnesses()` would also kill them under
   `--selftest`.
2. Optionally, have the matrix compare witness `decided` content (or at least
   the finding's `decided`/`expected`) instead of `{caught, exit, findings}`
   count. That alone exposes M1 on `w4` without a new fixture, because the
   witness is still a mismatch but with the wrong decided value.
3. If `:splat`-as-exact-placeholder is intended to be reserved or rejected,
   say so in the v1 contract and add a manifest for that class; today both the
   committed overwrite behavior and M3's guard are unwitnessed.

## Restoration evidence

Scratch tool bytes restored with `git checkout 3d7b56d7... -- scripts/redirect_audit.py`
in `repo/` after the last mutant run.

| Point | scripts/redirect_audit.py sha256 | Selftest | Matrix after |
|---|---|---|---|
| lane, start and end | `1e1dff18030c9028d833ab108bff140102343f4c5198c35984e7838e54bb748a` | — | — |
| scratch pristine (pre) | `1e1dff18030c9028d833ab108bff140102343f4c5198c35984e7838e54bb748a` | exit 0, 23/23 | PASS, 11/11, FP 0, wall 0.914 s |
| scratch M1 rev `8305ad20` | `d67dcd3be9ae7d49f4669d5e3284a48110b29f1b4b823d01e4831bd0bb0057f6` | exit 0, 23/23 | PASS, 11/11, FP 0, wall 1.118 s |
| scratch M2 rev `a3b146be` | `6eb4c9b4b6e6f67868a891cc621bc03446f092a889dc19f38c38e2cf7775a733` | exit 0, 23/23 | PASS, 11/11, FP 0, wall 1.107 s |
| scratch M3 rev `6b41f041` | `b488c53aa4f51bb38f8d744e22ce9c0268815933bc3fd6f49198b09f31520f05` | exit 0, 23/23 | PASS, 11/11, FP 0, wall 1.039 s |
| scratch restored (post) | `1e1dff18030c9028d833ab108bff140102343f4c5198c35984e7838e54bb748a` | exit 0, 23/23 | PASS, 11/11, FP 0, wall 1.015 s |

Lane untouched: `git status --porcelain` in the lane shows only the pre-existing
untracked `.ufo/waves/round-46/residual/` report directory (siblings' reports,
not modified here); lane tool and counter sha256 unchanged from the values filed
in `c1-after-ee43e66.json`. The scratch `repo/` was left clean at restoration
commit `50d2c60db17d80260cd88650f00737bffa719b47`, whose
`scripts/redirect_audit.py` blob and working tree both hash to
`1e1dff18...748a`. No writes outside this report and
`/fast/scratch/hyaku/kake-r46-residual/MutationSemanticsGap/`. Lane jj state,
git index, sibling lanes and `.ufo/state`/`.ufo/watchdog.log` were not touched.

## Artifact index (scratch)

- `repo/` — pristine subtree repo (`3d7b56d7`), mutant revisions `8305ad20`,
  `a3b146be`, `6b41f041`; restored working tree.
- `variants/<mutant>/scripts/redirect_audit.py` — mutant bytes.
- `probes/p1_lazy_splat.json`, `p2_double_decode.json`, `p3_splat_name.json`.
- `base-matrix.json`, `m1_lazy_splat-matrix.json`, `m2_double_decode-matrix.json`,
  `m3_splat_name_collision-matrix.json`, `restored-matrix.json` — sealed receipts.
- `*-selftest.out` — selftest transcripts (all `23/23 passed`).
- `cf-*.json` — counterfactual matrix receipts (four runs above).
- `repo-probe/` — clone used for the counterfactual oracle widening.
