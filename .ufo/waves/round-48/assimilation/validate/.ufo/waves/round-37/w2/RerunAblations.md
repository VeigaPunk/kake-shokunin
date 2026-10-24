# RerunAblations — round 37 wave 2 (falsify), seat KakeR37.RerunAblations

Attacked: the declaration's coverage sentence (`sealed/reference/declaration.md:28-30`, same text in
SCORECARD "Round 37 — declared claims"): "each of the 34 listed ablations of the L1's private
reference scores at most 24 of 28 (16 to 24 ...), and the reference scores 28 of 28"; the 70
committed receipts in `verification/ablations/`; `sealed/reference/ablation-pre.json` (own-bullet
fails). Verdict: **holds** — the result reproduces byte for byte. One low-severity docstring defect.

## Setup
- Sandbox clone `/fast/scratch/hyaku/kake-r37w2/RerunAblations/clone` at `79d3c780f9afb9bc013e3b13e73ee73e6a8ac13c`
  (GIT_* unset, TMPDIR=sandbox/tmp). Counter `sealed_count.py` sha256 `2ebb39b5…0cf0e3` (= declaration
  digest, = `counterSha256` in every re-run receipt). Key `sealed/cases.json` sha256
  `93ad9ee6…0c8c0a90`, identical to `git show 424aa248:.ufo/waves/round-37/sealed/cases.json`.
  `/usr/bin/bwrap` present (jail active).

## Commands (all exit codes observed)
1. Static provenance (python, exit 0): 34 keys in `ablation-pre.json` = 34 files in `sealed/ablation-tools/`
   (none missing either way). For each, regenerating `ref-<a>.py` from committed `ref.py` by the
   receipted substitution (`verification/score_ablations.sh:10`, replace line 16
   `ABL = set(filter(...KAKE_ABLATE...))` with `ABL = {"<a>"}`) is **byte-identical** to the
   committed tool; every receipt's `toolSha256` equals sha256 of the committed tool; `reference.json`
   `toolSha256` equals sha256 of `ref.py`.
2. `ref.py` gates exactly 34 ablation names (`"x" in ABL` / `not in ABL`, lines 25–240); unlisted
   gated names: none; listed but ungated: none. So "listed" does not hide a 35th ablation.
3. Re-run A, revealed key by revision, 8 parallel, 6.7 s wall:
   `timeout 900 python3 -B .ufo/waves/round-37/sealed_count.py --root <clone> --tool-file <tool> --key-revision 424aa248`
   for the 34 ablation tools + `sealed/reference/ref.py` → 35 receipts in sandbox `out/`.
   Exits: 34 × 1 (not met), reference 0. No stderr output.
4. Re-run B, `--key-file <clone>/.ufo/waves/round-37/sealed/cases.json` (the committed script's mode),
   → sandbox `out2/`: 35 receipts, `passed` and `perCase` identical to re-run A (0 diffs) despite the
   counter's per-run random id/file renaming. Exits 34 × 1, 1 × 0.
5. Provenance: `git log` — all 70 receipts added in `202d625` (declaration) and unchanged to the tip
   (`git diff --stat 202d625 79d3c780 -- verification/ablations/` empty). `ref.py`, `ablation-pre.json`,
   ablation tools land at reveal `424aa248`.
   `pgrep -f sealed_count.py` afterwards: none (no process left).

## Per-ablation: committed vs re-run (passed of 28; failed cases)
Every row: committed = re-run A = re-run B = `ablation-pre.json` passed; failed-case set identical
across all four; exit 1; met false; own bullet's 4 cases all fail (`allOwnFailed` true reproduced).

| ablation (bullet) | committed / re-run | failed cases |
|---|---|---|
| a_2xx, a_4xx, a_5xx (a) | 24 / 24 each | a1–a4 |
| b_limit, b_bom, b_cr, b_comment, b_keycase, b_orphan, b_other (b) | 24 / 24 each | b1–b4 |
| c_uacase, c_merge, c_consecutive (c) | 24 / 24 each | c1–c4 |
| c_star (c) | 16 / 16 | c1–c4, d1–d4, e1–e4 |
| d_longest, d_tie, d_star, d_empty (d) | 24 / 24 each | d1–d4 |
| d_dollar (d) | 20 / 20 | d1–d4, e1–e4 |
| e_nonascii, e_unreserved, e_hexcase (e) | 24 / 24 each | e1–e4 |
| f_emptypath, f_fragment, f_robots (e) | 24 / 24 each | e1–e4 |
| f_query (e) | 20 / 20 | d1–d4, e1–e4 |
| f_dup, f_3xx, f_ua, f_escape, f_expect, f_scheme (f) | 24 / 24 each | f1–f4 |
| g_version, g_checklist (g) | 24 / 24 each | g1–g4 |
| reference `ref.py` | 28 / 28, exit 0, met true | none |

Range over 34: min 16 (c_star), max 24; all ≤ 24; none met.

## Verdicts
- "each of the 34 listed ablations scores at most 24 of 28": **holds** (34/34 ≤ 24, re-run twice).
- "(16 to 24)": **holds**, and is tight (min 16 c_star, max 24).
- "the reference scores 28 of 28": **holds** (re-run A and B, exit 0).
- `ablation-pre.json` own-bullet claim (each ablation fails all 4 cases of its bullet): **holds** 34/34.
  Its generator scoring (env `KAKE_ABLATE`, `cases.py:258-316`, no jail) and the jailed counter on
  sed-built tools agree on every passed count and failed set, so two separate paths give the same result.
- Receipts irreproducible or edited after the fact: **no** (sha-bound tools, unchanged since `202d625`).

## Findings
- LOW (doc): `sealed/reference/ref.py:4-5` says "each ablation name is listed in ABLATIONS with the
  bullet it belongs to", but no `ABLATIONS` exists in `ref.py` (`git grep ABLATIONS 79d3c780` hits only
  that docstring and its copies in `retained/MutRefPass/evidence/trials/M*.py`). The real list is
  `BULLET_ABL` at `sealed/reference/cases.py:21`. The result does not change.
- INFO (naming): f_emptypath, f_query, f_fragment, f_robots carry an `f_` prefix but belong to bullet
  (e) in `ablation-pre.json`. That matches the contract ((e) owns empty path, query, fragment,
  /robots.txt), so no defect, but a reader who goes by the prefix will map them to the wrong bullet.

## Residual risk / gaps
- The sentence is scoped "measured and nothing more", and the declaration itself disclaims that it
  says nothing about other ways to skip a rule. I did not check whether every contract rule has an
  ablation. Visible examples with no listed ablation: (f) non-object check, missing or empty id,
  empty host, absolute or missing robots path; (g) non-regular file, >64 MiB, not UTF-8, not JSON;
  (b) lines without `:`, U+FFFD decoding; (d) prefix-from-first-character. Those are mutation-pass
  territory (MutRefPass), not this sentence.
- I ran no counter mutations; the counter's sha matches the declared digest.
- Tools installed: none.
