## Verdict

**No counterexample found.** All six assigned attacks hold against the post-fix working tree. Two P3 residual-evidence gaps noted; neither falsifies the recovery.

## Findings

### Attack 1 — before-state (0/32, tool absent): failure-capable, not vacuous — **HOLDS**

For a capability claim, before = capability absent. The hardened counter makes the absence reading non-vacuous: it exits 0 only after `instrumentValidated` (instrument pinned + population checked). Re-ran myself:

```
python3 .ufo/waves/round-22/measure.py --root . --revision 7c61c8cc… --cases-root .
→ exit 0; accepted=0, total=32, available=false, instrumentValidated=true,
  error="revision has no scripts/canonical_audit.py blob"
```

The failure directions are now covered: unvalidated baseline → exit 2 (counter-probe CE2, observed `exit:2`), fabricated `accepted=32` numerator → exit 1 (CE1, observed `declared accepted=32 != derived 0; discrepancies=0 != rows-derived 32; matrix exit 0 != 1`). measure-before-v2.json records `source: git` pins vs v1's `working-tree`, and its note correctly supersedes v1 while keeping it as history.

### Attack 2 — post-wave-2 validator/measure/expected.json changes vs "frozen populations" — **HOLDS**

`git diff c0fd6d5 -- cases.json fixtures contract.json matrix.py` = **0 bytes**; `git status --porcelain` on same paths = empty. The 32-name population and the oracle (cases.json sha `28a49013…`, matrix.py `d7de62…`) are byte-frozen since the c0fd6d5 integration commit. The only frozen/expected.json delta is the artifact-under-test pin (`35433e50…` → `aa1ff6ad…`); `exit/accepted/total` (0/32/32) and all 66 instrument/fixture pins are unchanged. Validator digest pinning is an input-identity record — re-pinning it on every fix is required, not a violation. Pre-fix blob confirmed: `git show c0fd6d5:scripts/canonical_audit.py | sha256sum` = `35433e50…` = the old pin and the reported before-probe validator (`/tmp/kake-r22a2/canonical_audit_c0fd6d5.py`).

### Attack 3 — lowest non-retired axis — **HOLDS**

AXES.md:33 requires ≥1 claim on the lowest non-retired axis "except when the stagnation nudge waives it." Both owned axes (operability, freshness) sit at the saturation line 10 — joint lowest — and C1 is declared `axis: operability` in contract.json. Directly satisfied without needing the nudge; the nudge (N=1, round 21 added no capability, SCORECARD.md:206-211) additionally prescribes exactly this frontier/capability move.

### Attack 4 — owned-axis harm — **HOLDS** (freshness red is the expected red, byte-identical shape)

```
TZ=UTC node scripts/freshness-sweep.mjs --section=paths → EXIT=1
VERDICT: DRIFT — §paths: 3 unannotated miss · 0 NOT in pins.pathsMissSet (exit 1)
citation base: 73 targets · missSet 55 · set-delta miss: no new miss
```

3 targets (plazir-15-site, webzites.mjs, kimi-surface.mjs) / 4 unannotated locations / missSet 55 / newMissing 0 — exactly the pinned baseline-red. `set-delta files +13` are pre-existing r18–r22 corpus additions, no new misses. No freshness or operability harm.

### Attack 5 — causal separability — **HOLDS** (trivially)

Single claim C1; the separability and distinct-axes clauses are vacuously met.

### Attack 6 — postfix probes failure-capable, expectations fixed not learned — **HOLDS**

- defect-probe: before JSON shows 2/7 met, `passed:false` (5 falsified on c0fd6d5 bytes); after shows 7/7 `passed:true`. Each expectation traces to a w2 report filed before the fix: `///` empty authority → `canonical_url_invalid`/`base_url_invalid` (Attack05's own strict-RFC reading and remediation text), usage errors → exit 64 + could-not-evaluate JSON (BoundaryCLIErrors P2a + contract exitMap), repeated `--manifest` → usage error (P2b), manifest symlink → `input_invalid` (BoundarySymlinks residual, resolved stricter and disclosed as fix D4), caller-prefix symlink → clean (the disclosed P2 scope decision; intentionally passes both sides — a scope pin, not a fix probe, correctly labeled).
- counter-probe: before `passed:false` (CE1 emitted accepted=32/exit 0, CE2 emitted exit 0 unvalidated); after `passed:true` (CE1 exit 1 row-derived rejection, CE2 exit 2). Both expectations are FalsifyCounting's demonstrated counterexamples verbatim.
- Replay (D8) re-ran post-fix by me: `verdict: clean, frozen_replay_match, inputsVerified: 69, casesCompared: 32, perCaseMismatches: []`.

### P3 residuals (not counterexamples)

1. **SCORECARD.md has no round-22 row and no Capabilities-table entry.** `grep` confirms no round-22 row; the last entry is round-21. AXES §Capabilities: "a capability without a passing demonstration in the round report is pre-claiming." Smallest fix: L1 lands the round-22 report row + capability table row (name → what it does → evidence pointer → round 22) in the same commit.
2. **D8's per-case oracle check in replay.py has no negative probe record.** defect/counter probes cover D1–D7; replay's new `per_case_mismatches` is exercised only by its PASS run, and `replay-integrated.json` was not re-generated post-fix. Smallest fix: one recorded mutant run (e.g., swapped case rows) showing `frozen_replay_mismatch`, plus a regenerated replay-integrated.json.

## Checked and held

- Frozen population integrity: zero diff on cases.json/fixtures/contract.json/matrix.py since c0fd6d5; oracle digests match expected.json pins.
- Before-probe authenticity: `/tmp/kake-r22a2/canonical_audit_c0fd6d5.py` pin equals `git show c0fd6d5:…` sha `35433e50…`; `measure_c0fd6d5.py` equals committed blob `329f45b6…`.
- measure.py reconciliation logic (diff lines 586-649): row-derived `accepted`, status-vs-oracle agreement, executed/discrepancies/exit cross-checks — matches FalsifyCounting's prescribed correction.
- Live runs: hardened measure on base revision (exit 0, instrumentValidated), hardened replay on worktree (clean, 69 inputs, 32 cases).

## Limits

- Did not audit validator internals (D1–D4 correctness beyond the probe outputs), measure/replay edge cases, or corpus/SKILL.md diffs — sibling seats own those.
- Freshness sweep is the local `--section=paths` check only; no network verification per bounds.
- `/tmp/kake-r22a2/` before-files no longer exist; identity verified via the recorded validator digest matching the c0fd6d5 git blob, not by re-hashing the probe artifacts.
- No tools installed; pacman untouched per pause.