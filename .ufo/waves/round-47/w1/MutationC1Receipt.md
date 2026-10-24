# MutationC1Receipt — C1 selftest-receipt sha256 strip (round 47, wave 1)

Seat: mutation-tester. Claim under test: **C1** (operability — both round-46 gates have a
SKILL.md registry row and a committed selftest receipt).
Verdict: **KILLED** — the detector's receipt predicate is load-bearing on the tool sha256.
Method: committed bytes only, in a disposable sandbox; lane checkout untouched.

## Detector

`python3 -B .ufo/waves/round-47/c47_registry_count.py --root . --revision <rev>`
(exit 0 = C1_MET, 1 = C1_NOT_MET, 2 = could-not-evaluate, 64 = usage).
Receipt acceptance, `.ufo/waves/round-47/c47_registry_count.py:122-123`:

```python
if (needle in text and tally_re.search(text)
        and "exit=0" in text and SHA256_RE.search(text)):
```

with `SHA256_RE = re.compile(r"\b[0-9a-f]{64}\b")` (line 43).

## Sandbox

- Scratch root `/fast/scratch/hyaku/kake-r47/MutationC1Receipt/` (local, never pushed).
- Built from committed bytes only: `git -C /home/vgpnk/Projects/shokunin/kake-shokunin archive HEAD | tar -x -C $S/base`,
  then a fresh local `git init`/commit → `BASE_REV=123d044329d0e7ced9dd41c5c5d4f948a9ce74ca` (7739 files).
- Lane HEAD at probe time: `766f4610b64f35a0f402b37eb1d8be2d4d634c0f`.
- Verified the receipts name the real blobs before mutating: `git show HEAD:scripts/redirect_audit.py | sha256sum`
  = `1e1dff18…bb748a` and `git show HEAD:scripts/citation_lint.py | sha256sum` = `3c78a0a8…9662987f`,
  matching `tool_sha256:` in the two receipts.

## Mutant

File `.ufo/waves/round-47/verification/selftest-redirect-audit.txt`, exactly one line (line 4) deleted:

```diff
 command: python3 -B scripts/redirect_audit.py --selftest
 run_at_utc: 2026-10-24T06:46:10Z
 tool_path: scripts/redirect_audit.py
-tool_sha256: 1e1dff18030c9028d833ab108bff140102343f4c5198c35984e7838e54bb748a
 stdout:
```

The tool path, the `selftest: 23/23 passed` tally and `exit=0` all remain, so the only
behavior-bearing difference is the sha256. Receipt sha256
`0760b031…28ef056` → `4a005b95…696010`. Mutant commit `26e6a1ac948308553ae8a88403cd792e28bc1a2e`.

## Runs

| state | revision | output | exit |
|---|---|---|---|
| pristine sandbox | `123d0443…74ca` | `registry_rows=2/2 receipts=2/2 C1_MET`; detail `redirect_audit.py: true`, `citation_lint.py: true` | 0 |
| mutant | `26e6a1ac…1a2e` | `registry_rows=2/2 receipts=1/2 C1_NOT_MET`; detail `redirect_audit.py: false`, `citation_lint.py: true` | 1 |
| restored | `9449242e…a1ad` | `registry_rows=2/2 receipts=2/2 C1_MET`; both detail values `true` | 0 |

Interpretation: the mutant receipt stops counting. Registry rows stay 2/2 (the SKILL.md rows at
`SKILL.md:1197` and `:1198` are independent), citation_lint keeps its receipt, and the composite
predicate flips to `C1_NOT_MET`. No other file in the receipt directory fell through as a
substitute: a pre-scan of all 13 committed files there showed only the two `selftest-*.txt`
receipts carry a tally plus `exit=0`; `c2-r4-mutation.txt` holds 64-hex and `exit=0` but no tally.

## Restoration

- Pristine bytes restored from the saved copy; receipt sha256 back to `0760b0310b166e45585794fb889431e2d5577af76e70cebfbe85d213428ef056` (identical to commit `123d0443`'s blob and to the live lane file).
- `git diff --stat 123d0443 HEAD -- .` in the sandbox printed nothing (tree identical to pristine).
- Detector re-run at restored revision returned `2/2 receipts` / exit 0.
- Lane checkout: HEAD still `766f4610b64f35a0f402b37eb1d8be2d4d634c0f`; lane receipt file hash
  `0760b031…28ef056`, unchanged. No mutating git/jj ran in the lane.

## Adversarial note (static, not exercised)

The predicate only requires *some* 64-hex token anywhere in the receipt (`SHA256_RE.search`),
never that it equals the tool blob's digest. A receipt naming a wrong-but-well-formed sha256
would still count. This probe does not test that variant; it is a coverage gap, not a C1
failure.

## Not done

No live-lane mutation, no re-run of the two selftest tools themselves, no inspection of sibling
repos or fleet-root files. Detector was exercised at three revisions only.
