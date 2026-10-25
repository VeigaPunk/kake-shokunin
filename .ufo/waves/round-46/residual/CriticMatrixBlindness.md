# CriticMatrixBlindness — kake-r46-residual

**Result: DEFECT CONFIRMED.** The sealed counter `.ufo/waves/round-46/c46_matrix.py`
**does not reject a control that skips audit semantics** — a 20-line basename
matcher earns a schema-valid `MATRIX_AFTER_PASS` receipt (exit 0). Two
oracle-provenance holes make the failure structural, not incidental.

## Counterexample (all three observed, scratch repo — lane untouched)

Scratch lane: `/fast/scratch/hyaku/kake-r46-residual/CriticMatrixBlindness/lane-evil`
(copied `.ufo/waves/round-46/fixtures/` verbatim; `git init`; two commits).
The sealed counter was invoked by absolute path from the lane — same bytes as
the filed receipts (`counter.sha256 7335b001f8a6860f…`, matching
`verification/c1-after-ee43e66.json`).

| # | Tool at measured revision | Oracle tampering | Counter verdict |
|---|---|---|---|
| A | `redirect_audit.py` = basename matcher: `os.path.basename(manifest).startswith("w")` → exit 1 `failed-policy`; else exit 0 `clean`. Never opens the manifest. | none | `MATRIX_AFTER_PASS` exit 0, 11/11 caught, 0 FP, wall 1.03 s |
| B | `redirect_audit.py` = reads manifest, echoes a planted `matrixHint:{exit,verdict}` field. | manifests **inside the revision** doctored with `matrixHint` | `MATRIX_AFTER_PASS` exit 0, 11/11, 0 FP |
| C | same rev as B (echo tool at that commit) | **worktree** `index.json` doctored to empty witness/clean/control lists | `MATRIX_AFTER_PASS` exit 0, `0/0` vacuous, wall 0.002 s |

Receipts: `receipt-revA.json`, `receipt-revB.json`, `receipt-revC.json` under the
scratch dir — all `stage_met: true`, all carry the real counter sha256, all
look fileable.

## Evidence — the three holes in `c46_matrix.py`

1. **Behavior-only tool predicate** (`main`, lines 145–151, 160, 197–203):
   `caught` = `code == 1 and verdict == "failed-policy"`; `flagged` = `code == 1`.
   Nothing distinguishes a decision procedure from a name/content guess. The
   fixture class is leaked for free by the manifest path itself
   (`w*_*.json` vs `c*_*.json`), because the counter passes
   `os.path.join(tmp, entry["manifest"])` verbatim — filename shortcut A needs
   zero file reads.
2. **Fixture payloads are NOT frozen** (`materialize` line 118 vs index read
   line 122): the comment claims "fixtures are the round's frozen oracle…
   outside the measured revision", but only `index.json` comes from the
   worktree — `entry["manifest"]` paths are resolved **inside the archived
   revision**. A commit may rewrite witness manifests to embed the expected
   verdict (variant B) and the counter cannot tell.
3. **Oracle unbound in receipt** (receipt keys observed: `clean, controls,
   counter, measuredAt, revision, schema, stage, stage_met, tool, wall_*,
   witnesses` — no `index`/`manifest` sha fields): the receipt cannot be tied
   to the oracle it ran against, and a doctored worktree `index.json` (variant
   C) yields a vacuous pass with no signal.

Secondary observation (predicate asymmetry, lines 175–186): a control that
emits `failed-policy` for **every** manifest is *accepted* by the counter's own
definition — the control test is a mimicry detector tuned to clean-biased
controls, not a semantics check. The shipped controls are all clean-biased so
this stays latent.

## Cross-check against filed receipts

Canonical run at tip reproduced exactly:
`stage=after witnesses_caught=11/11 clean_false_positives=0 controls_accepted=0
wall_s=1.091 MATRIX_AFTER_PASS` — the shipped 607-line tool is genuine (real
`decide()` over percent-decode, resourcePrecedence, ordered first-match,
splat/placeholder, status whitelist); the defect is in what the counter's PASS
certifies, not in C1's tool.

## Impacted axes

- **operability**: named criterion fails — the counter does not reject a
  no-semantics control; its after-PASS is not a semantics certificate.
- **evidence/provenance**: receipts omit oracle identity (index/manifest
  hashes), so a PASS receipt is not bound to the fixtures that produced it.

## Smallest safe correction (counter is sealed for r46 — this targets r47)

1. Record `index.json` sha256 + per-manifest/per-control sha256 in the receipt;
   verify the index hash against a lane-sealed constant before scoring (kills
   variant C and binds receipts to their oracle).
2. Materialize manifests from worktree-frozen bytes (or hash-pin them), not
   from `<revision>` (kills variant B).
3. Copy manifests to randomized temp basenames before invoking the tool, and
   require findings to name the failing check id (semantic evidence the
   basename matcher cannot fake).
4. Robust fix for the residual channel: include ≥1 per-run freshly generated
   witness/clean pair so no fixed public fixture map exists to pattern-match.

## Judge note

Fixable defect, not a verdict-blocking tradeoff: the counter performed its
declared role for the real commit, and the sealed freeze means r46 receipts
stay as filed. The C1 claim narrows to "the real tool passes the matrix" —
true — but "the matrix rejects non-audit tools" is falsified by variant A.
