MET — one of six IP-literal mutants meets the counter and has a differing witness.

Axes: operability (primary), freshness. Leaf mutation evidence only; no round verdict or integration.
Artifacts/receipts: D=`/fast/scratch/hyaku/kake-r42w1/MutRegexIP`; R=`/home/vgpnk/Projects/shokunin/kake-shokunin`. Seed 42117 throughout; counter SHA256 `7bfc32c5e76dca942208934cfbe89f166eda2776b40e69de987706b4d97dd2a6`.
Own rewrite: `fast.py:78-87` factors disjoint character runs with possessive quantifiers; `:93` supplies a global TAB/CR/LF substring guard. No timing, caching, shape or label shortcut.
Expected detector: generated equality runs A/B should expose IP-repertoire changes; timing-only rejection does not establish a killed mutant.

All retained tool paths below are relative to D; SHA256s identify the bytes actually scored. Counter toolFile arguments were `fast.py` for pristine/fast, `work_<name>.py` for mutants, and `work_drop_pct.py` for restored. Working files are now restored; use retained `mutant_*.py` to reproduce mutant scores.
| Retained tool | One-line change / role | SHA256 |
|---|---|---|
| preflight_fast.py | Initial rewrite, regex-based global guard | b191e0c9a8b6bfb8b2ef1f777c4800380992dd908e5e57f92c7f0a7169b1c778 |
| preflight_drop_pct.py | Initial rewrite minus `%` | a6e289d313335275a1cfab5b721962e365a9a6ddf5a93b023522f775fa9673fa |
| fast.py | Final pristine rewrite, substring global guard | af063a5632060c1c88b5ccbffcdd5ade8ce8b850d78351d8189b92d0dfda4ac7 |
| mutant_drop_pct.py:81 | remove % from IP class | 8108e796c1525a125c151ce56d4ecb71a02682cbe28f5e07457b8511f743fbcc |
| mutant_add_pipe.py:81 | add | to IP class | 3159a940d70a8f24d66b63f219b877cef6beaa5748ddcb7094f34852d00783b6 |
| mutant_nonascii.py:81 | add U+0080..U+10FFFF to IP class | ef96684a7ea059f53abeddba65e650d816c3e20d8b126ac94b4e56f8372d43c3 |
| mutant_broad.py:81 | replace IP repertoire alternative with any non-] character; global TAB/CR/LF guard retained | ce548d3b78eb2dd605415463cf9b270321d472ae810aa12aa7efbaf6e224c9bc |
| mutant_drop_v.py:81 | remove lowercase v from IP class | 74684b26d256f21795603e285ee37bf037a4229ae0d230fce46107856c41a7a7 |
| mutant_drop_tilde.py:81 | remove ~ from IP class | 5c4e1d417cb64e9e2a50fd254ce3cdeb437ebcf099471c4f5938d7d6f3a31055 |

Ratios below are ordered T1,T2,T3,T4,T5; receipt paths are D/<receipt>.json. All timing repetitions were equal 5/5 on every scored tool.
| Receipt / label suffix | equalRuns | Ratios | met / exit | Caught by / verdict |
|---|---|---|---|---|
| pristine | 8/8 | 1.344, 1.623, 1.137, 1.094, 2.192 | false / 1 | none; inconclusive: preflight baseline missed T5 |
| drop_pct | 6/8 | 1.366, 1.578, 1.109, 1.084, 2.056 | false / 1 | A,B; inconclusive: preflight baseline missed T5 |
| fast | 8/8 | 1.118, 1.337, 1.074, 1.055, 1.545 | true / 0 | none; pristine/restored passes |
| m_drop_pct | 6/8 | 1.069, 1.352, 1.15, 1.096, 1.585 | false / 1 | A,B; killed |
| m_add_pipe | 7/8 | 1.097, 1.303, 1.123, 1.04, 1.666 | false / 1 | B; killed |
| m_nonascii | 7/8 | 1.155, 1.369, 1.147, 1.05, 1.672 | false / 1 | B; killed |
| m_broad | 7/8 | 1.097, 1.356, 1.066, 1.077, 1.64 | false / 1 | B; killed |
| m_drop_v | 6/8 | 1.142, 1.337, 1.11, 1.077, 1.562 | false / 1 | A,B; killed |
| m_drop_tilde | 8/8 | 1.117, 1.278, 1.054, 1.061, 1.614 | true / 0 | none; SURVIVED |
| restored | 8/8 | 1.073, 1.309, 1.091, 1.072, 1.543 | true / 0 | none; pristine/restored passes |

**Survivor witness (actual output):** `https://[fe80::1%~en1]/a` → tip41 `('https', 'fe80::1%~en1', 443, '/a')`; `mutant_drop_tilde.py` → `None` (`check_drop_tilde.json`). Thus this is a behavior-skipping control, not an equivalent alternate implementation.
Bounded own detector: `parse_check.py` generates 39,728 values (seed 42117). Final pristine: 0 differences, exit 0. Mutants drop_pct/add_pipe/nonascii/broad/drop_v/drop_tilde: 2246/409/940/2882/2545/851 differences, each exit 1. Every restored workfile: 0 differences, exit 0; raw examples are in `check_*.json`.
**Restoration:** all six `work_*.py` files have exact pristine SHA256 `af063a5632060c1c88b5ccbffcdd5ade8ce8b850d78351d8189b92d0dfda4ac7`; before/mutated/after hashes and detector outputs are recorded in `restoration.json`. Same-seed restored counter also met (row above). Immutable mutant snapshots are deliberately retained as deliverables.

Exact executed commands and exit codes for all 10 counter runs and 20 local detector runs: `D/commands.json` (including preflight evidence). Counter invocation template (toolFile/label/out are the exact values in each receipt):
`timeout 900 prlimit --as=8000000000 -- env TMPDIR=$D python3 -B $R/.ufo/waves/round-42/c42_count.py --root $R --tool-file <toolFile> --label <label> --seed 42117 --out <receipt>`
Local detector invocation: `timeout 120 prlimit --as=8000000000 -- python3 -B $D/parse_check.py --tool <tool> --out <receipt>`; exact substitutions and exits are in `commands.json`.

Checked statements: **holds** — five final mutants are caught by equality with a passing pristine/restored baseline; final rewrite matches all sampled values and meets all five CPU limits. **Wrong** — equality runs catch every tested one-member IP change: removing `~` survives. **Overstated** — met implies every round-41 judgment is preserved; the witness disproves that inference.
Finding: `c42_count.py:229-236` randomly samples IP edits but does not guarantee exposure of each member on an otherwise accepted value; `:601-604` admits this survivor. `mutant_drop_tilde.py:81` is its only change from the final rewrite. No claim beyond this tested seed is made.
All launched probes completed; at most two counter processes ran concurrently. No network, installs, services, repo source/index/state changes, or sibling writes. Only this report and the assigned sandbox were written.
