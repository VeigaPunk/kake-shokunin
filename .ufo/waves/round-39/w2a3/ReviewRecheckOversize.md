# ReviewRecheckOversize — attack on ExecRecheckOversize's source_recheck fix

Axes: operability, freshness. Sandbox `/fast/scratch/hyaku/kake-r39a3w2/ReviewRecheckOversize/`; clone at `bb4a1e1e` (git `HEAD` of the lane; `source_recheck.py` byte-identical to w1 base `72edf212`, sha256 `6629d800…0c81` — fix verified against the same bytes).

## Runs (each `prlimit --as=4000000000 timeout 600`, clone dir; exit)
- `python3 -B scripts/source_recheck_selftest.py`: before 106/106 **0**; after 106/106 **0**.
- `python3 -B scripts/source_recheck_hardening_selftest.py`: before 9/9 **0**; after 10/10 **0**.
- `git apply --check`/`git apply -p1 ../recheck-oversize.patch`: **0**; patched files sha256 `2ce8c0d9…87e1a`, `3982837841…d13178` — byte-identical to w1's deliverables and to the lane jj working tree (lane `git status` shows both files ` M` ahead of `bb4a1e1`).
- Fixture-only-on-base rerun (revert `source_recheck.py`, keep patched selftest): exit **1**, `7/10`, reds g33, g34, g36.
- w1 `cli/case/manifest.json` on `base_source_recheck.py` (sha `6629d800`): exit **2**, `checksEvaluated:2`, `k2` = moved+check_invalid; on fixed: exit **2**, `checksEvaluated:1`, `k2` = check_invalid only, `k1` moved+charset_unsupported unchanged.
- Unreadable-body probe (`chmod 000` body, 301→200 chain): base exit **2** `moved+check_invalid`, `checksEvaluated:1`; fixed exit **2** `check_invalid` only, `checksEvaluated:0` — the fix reaches the open/read-time fault too, not only the cap branch.

## Per attacked statement
- **Defect at HEAD (`:589` moved before read, `:611` cap append, `:754-755` count) → moved+check_invalid and +1 evaluated — holds.** Base line numbers exact (`source_recheck.py:583 def, :589 moved, :609/:612 check_invalid, :754-755`); CLI reproduces `checksEvaluated:2`, `k2` pair.
- **Fix = `evaluate_check`→`None` on input fault, `main` emits one check_invalid, uncounted — holds.** Post-patch `source_recheck.py:584-593` (docstring), `:617-620` (`return None` ×2), `:761-766` (main `produced is None` branch, `is None` correctly used — a legitimate `[]` still counts).
- **`moved` beside gone/http_error/charset_unsupported/unsupported_type untouched — holds.** Diff confined to docstring, signature, two fault returns, main loop; runtime `k1` still moved+charset_unsupported; 106-case selftest clean both sides.
- **"g36 red on HEAD — the only red in that file" — overstated (minor).** Holds for their two-stage intermediate (their `fixture-red.txt` shows 9/10, g36 only), but the *shipped* selftest half on base is red in **three** cases: g33 and g34 also fail on the new `evaluated=0` pins (7/10 here). Totals row "9/10" is thus a different state than what the delivered patch produces pre-fix.
- **sha256s, 2 files +54/−16, a/b prefixes, only `main` calls `evaluate_check` — holds.** Patch sha `12da4270…6c37`; grep over `scripts/` shows the sole call site at `:761`; r37 mutant copies under `.ufo` are standalone and untouched.
- **g33/g34 newly pinned to 0 — holds** and contract-consistent ((g): checksEvaluated "counts the checks that are not check_invalid"; canonical sentence at `source_recheck_selftest.py:152-153`).

## Residual risks / gaps
- The fix is one path wider than the seat's framing: it also converts evaluate-time **unreadable** bodies (OSError etc., `:617`) — contract-correct and disclosed in w1's own "Risks".
- Fix-site line cites drift ±1 in places (`:616-619` is `:617-618`/`:620`; `:583-592` is `:584-592`; `:760-767` is `:761-766`); selftest cites `:238/:243` exact; g36 block at `:245-258`.
- Selftest sorts findings in its failure report (observed `check_invalid` printed before `moved`; emit order on the base CLI is moved-first) — report artifact only, not a defect.

Verdict: the patch is correct, minimal, byte-verified, and lands the (g) reading; only the "only red" framing is slightly overstated. No installs used; no lane files mutated except this report.
