# Round 28 wave 1a3 — mutation test: C1 gate, revert catch to ValueError only

Seat: `KakeR28a3.MutRevertJsonDepth` (leaf, mutation tester).
Target claim: C1 (operability, repair-first) at b5d423fc02057f67a6f3a255808313ce40d29069.
Detector: `.ufo/waves/round-28/c1_interface_count.py` (15 cases: U1–U4 + A1–A7 defects, K1–K4 controls, selftest).

## Mutation
File: `scripts/citing_set.py`, `load_json_document` (line 401), one behavior-bearing point:

```diff
-    except (ValueError, RecursionError) as exc:
+    except ValueError as exc:
```

Deep-nested JSON then raises unwrapped `RecursionError` instead of `InputInvalid("document_not_json")`, so the gate dies with a traceback instead of the contracted JSON report + exit 2.

## Evidence (clone: /fast/scratch/hyaku/kake-r28a3/w1/MutRevertJsonDepth/clone)
Commands (all in sandbox clone; no fleet-repo mutation; no tool installs needed):

| run | command | exit | passed/total | defect | control | failing |
|---|---|---|---|---|---|---|
| pristine (b5d423fc…) | `python3 -B /home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-28/c1_interface_count.py --root clone --revision b5d423fc02057f67a6f3a255808313ce40d29069 --scratch /fast/scratch/hyaku/kake-r28a3/w1/MutRevertJsonDepth/count` | 0 | 15/15 | 11/11 | 4/4 | none |
| mutated (b9fc7b9) | same, `--revision HEAD` | 1 | 13/15 | 9/11 | 4/4 | U3-population-deep-json, U4-ledger-deep-json |
| restored (dde7179) | same, `--revision HEAD` | 0 | 15/15 | 11/11 | 4/4 | none |

Mutated failing cases: `U3-population-deep-json`, `U4-ledger-deep-json` — observed `exit: 1`, `verdict: null`, stderr tail `RecursionError: Stack overflow (used 8144 kB) while decoding a JSON array from a unicode string` (json/decoder.py). No contracted JSON report is printed. Controls K1–K4 pass in the mutated run.
Outputs held at `…/MutRevertJsonDepth/ref_run.json`, `mut_run.json`, `rest_run.json` (scratch).

## Verdict
MUTANT KILLED. The counter drops 15/15 → 13/15, fails exactly U3 and U4, keeps all controls green. No survivor; the C1 counter is sensitive to this gate change at the specified revision.

## Restoration
Restored byte-exact: `git blob-object scripts/citing_set.py` = `c26fcd498f1974265e6bb80dca8e102f57eb7b5f` both at pristine (b5d423f) and after restore commit dde7179 (blob index in restoration diff: `c2f9193..c26fcd4`). Restored run confirms 15/15, exit 0.
Clone history: b5d423f (pristine) → b9fc7b9 (mut) → dde7179 (restore). `git diff` at each commit showed exactly the one-line change.

## Not verified
- No run against any other revision or the round-27 base; no expansion of the counter (e.g., other exception narrowing paths), as the instrument is the L1's.
- No installs performed; none were needed.
