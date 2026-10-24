# MutationC2R5 — C2 R5 same-line landing-hash predicate (round 47, wave 1)

Seat: mutation-tester. Claim under test: **C2** (freshness; routed r46 defect **R5** — the
LOG round-46 entry names no landing-commit full hash).
Verdict: **KILLED** — splitting the two landing hashes onto separate `LOG.md` lines flips
the frozen R5 leg `true → false` and the counter to `outstanding=1/4 C2_NOT_MET`, exit 1.
Method: committed bytes only, in a disposable sandbox clone; lane checkout untouched.

## Detector

`python3 -B .ufo/waves/round-47/c47_routed_count.py --root . --revision <rev>`
(exit 0 = C2_MET, 1 = C2_NOT_MET, 2 = could-not-evaluate, 64 = usage).
Detector sha256 (lane == sandbox): `9be35ef2452aaff0757a0c2839c17cb58e08a7a59f6a217a3489598c19a8359e`.
R5 leg, `.ufo/waves/round-47/c47_routed_count.py:135`:

```python
r5_fixed = any(all(h in line for h in R5_HASHES) for line in log_lines)
```

with `R5_HASHES` (lines 47–50) = `ee43e66367bf23e386ff29029b9ea60515efd9d1`,
`861113eb0eea4d51bd0614c542aa6ecb7cc9a843`. The leg is a **single-line co-occurrence**
test over every line of `LOG.md`; no path, section or wording binding.

## Sandbox

- Scratch root `/fast/scratch/hyaku/kake-r47/MutationC2R5/` (local, never pushed).
- Built from committed bytes only: `git clone --no-hardlinks --quiet <lane> sandbox`
  → clone HEAD `766f4610b64f35a0f402b37eb1d8be2d4d634c0f` (equals lane HEAD), clean tree,
  no `.jj` in the clone.
- Lane at probe time: HEAD `766f4610b64f35a0f402b37eb1d8be2d4d634c0f`; `LOG.md` sha256
  `16d1085b91ff1153fff6eaccedf94e8d67c85a64d8d9b8d6c721cf0a06a9999c` (= blob
  `4f4b11d0d42fbd74838a157052ca6f766c5bc7bb`); counter sha256 as above.
- Pristine baseline before mutation:
  `outstanding=0/4 C2_MET`, exit 0; `fixed = {R3: true, R4: true, R5: true, R6: true}`.
  Receipt `/fast/scratch/hyaku/kake-r47/MutationC2R5/baseline.json` sha256
  `145bae5b94ae5007a449921065ff1c5f2be51bfbedf6fee576674df24771a062`.

## Mutant

`LOG.md:1813` (the only line in the repo holding both hashes) hard-wrapped into three lines;
no bytes removed, both hashes still present twice each in `LOG.md`:

```diff
-- [r47-correction R5 identity] Full hashes of the round-46 build and verdict commits are `ee43e66367bf23e386ff29029b9ea60515efd9d1` and `861113eb0eea4d51bd0614c542aa6ecb7cc9a843`.
+- [r47-correction R5 identity] Full hashes of the round-46 build and verdict
+  commits are `ee43e66367bf23e386ff29029b9ea60515efd9d1` and
+  `861113eb0eea4d51bd0614c542aa6ecb7cc9a843`.
```

- Mutant commit `c8c076f02331f77d29d46afab7a8a64b15bb6c04` (sandbox only).
  Mutant `LOG.md` blob sha256 `9cf03e89b0bfe4807643155596b743b59bfd4d417e665fbf0f7bba51beb3143d`.
- Lines holding **both** hashes: pristine revision `766f4610` = **1** (line 1813); mutant
  revision `c8c076f` = **0**. Occurrences of each hash in `LOG.md` stay 2 and 2.

## Detector output on the mutant

```
outstanding=1/4 C2_NOT_MET
EXIT=1
{
  "fixed": {"R3": true, "R4": true, "R5": false, "R6": true},
  "outstanding": 1,
  "revision": "c8c076f02331f77d29d46afab7a8a64b15bb6c04",
  "verdict": "C2_NOT_MET"
}
```

Receipt `/fast/scratch/hyaku/kake-r47/MutationC2R5/mutant.json` sha256
`6758ac5df7095e001337646fea17c198d6ccea990f362866b20b0fd2641e5af5`.
Only R5 flipped; R3/R4/R6 stayed `true` — the mutation is isolated to the assigned leg.

## Restoration

`git reset -q --hard 766f4610b64f35a0f402b37eb1d8be2d4d634c0f` in the sandbox;
`LOG.md` sha256 back to `16d1085b91ff1153fff6eaccedf94e8d67c85a64d8d9b8d6c721cf0a06a9999c`,
`git status --porcelain` empty, re-run → `outstanding=0/4 C2_MET`, exit 0, receipt
byte-identical to baseline (`145bae5b94ae…`).
Lane checkout re-hashed after the probe: `LOG.md` `16d1085b91ff…`, counter `9be35ef2452a…`,
HEAD `766f4610b64f35a0f402b37eb1d8be2d4d634c0f` — unchanged; no lane git/jj command was run
and no production file was touched.

## Finding (adversarial, C2/R5)

- The frozen R5 leg is **load-bearing and formatting-literal**: re-wrapping one line kills
  it with zero information loss (both hashes remain, each twice). Sensitivity confirmed;
  the measurement at `766f4610` is therefore a real byte-level check, not a vacuous one.
- **Fragility**: the R5 evidence rests on exactly one line. The earlier R5 correction block
  at `LOG.md:1798-1802` already splits the hashes (`ee43e663…` on line 1800, `861113eb…` on
  line 1801); only the duplicate at line 1813 satisfies the predicate. Any future reflow of
  line 1813 turns C2 red while every hash is still present in `LOG.md`.
- **Untested bound**: `any(... for line in log_lines)` scopes to all of `LOG.md`, with no
  binding to the R5 correction entry. A both-hash line in unrelated prose would also green
  R5; I did not test that shape (a different mutation than the one assigned), so it is
  stated as an untested bound, not a claim violation.

## Scope

Mutated the sandbox clone only. Did not probe R3/R4/R6, did not run any lane mutation, did
not dispatch subagents (leaf), did not invoke another runtime. No tool installs (git and
system `python3` stdlib sufficed; no pacman transaction was run).
