# ScoutR68Receipt — round-69 W1 (kake lane)

**Question.** Re-run the round-68 D-3 quote receipt against committed bytes at
`4d188f9477b4301a2c93c8ef5c13bc6c6f4bb6e4`; do not touch
`.ufo/waves/round-68/controls/wordcounts-d3-r68.txt`.

**Artifact.** `.ufo/waves/round-69/w1/ScoutR68Receipt/wordcounts-r68-rerun.txt`
— 202 lines, sha256 `4b385fdb9ecdd89a5524e3caa8944ddeb1e9dc2acd3202dc1384b2730cafab2b`,
`grep -c '/tmp'` = 0 (exit 1). Every line is written by a command run; none is hand-typed.

## Observed

| # | quote | literal `grep -cF` in committed round-67.md | `wc -w` | class vs retained body | r67 label |
|---|---|---|---|---|---|
| i | S133 `an exit status of 0 indicates that it ran successfully` | **0** (exit 1); wrap-tolerant 1 | **10** | **collapsed-only** | 11 |
| ii | S434 full `…(128–255), except for the following:` | **0** (exit 1); wrap-tolerant 1 | **26** | **raw-substring** | 16 |
| iii | S434 22-word sub-quote ending `(128–255)` | **0** (exit 1); wrap-tolerant 1 | **22** | **raw-substring** | unlabelled |

Inputs read only with `git show <rev>:<path>`: round-67.md (11759 B,
`3638ba9e…`), S434-naming.html (67904 B, `8e7f3450…`), subprocess.html
(208624 B, `eceda6f6…`). The S434 body digest equals the digest in
`.ufo/waves/round-67/sources/receipt.json`.

**Why the literal counts are 0.** The lesson hard-wraps its block quotes:
round-67.md:105-106 splits `"an exit` / `status of 0 …"`, :109-111 splits the S434
span over three lines. `grep -cF` is line-oriented, so a wrapped quote cannot
match; a wrap-tolerant count (one `\s+` between the quote's words) gives 1 for
each. Property of the lesson's rendering, not of the quote.

## Round-68 claims re-checked

- **S133 `collapsed-only` — HOLDS.** `scripts/quote_class.py` at the revision →
  `derived=collapsed-only` (raw grep 0; the flat rendering from
  `.ufo/waves/round-63/quote-class/extract_text.py` contains it). Cause in the
  bytes: subprocess.html:362 ends `… Typically, an exit status of 0 indicates` and
  continues `that it ran successfully.</p>` — a newline inside the span.
- **S434 `raw-substring` — HOLDS.** `derived=raw-substring`, raw `grep -cF` = 1,
  for both the 26-word full quote and the 22-word sub-quote; span on one HTML line,
  U+2013 en dash byte-identical in lesson and body.
- **Word counts 10 / 26 / 22 — all re-derive.** The r68 D-3 correction
  (`corpus/lessons/round-68.md:115-121`) is right on all three numbers; the r67
  labels (11, 16) are off by -1 and +10.

## Attacks run (executed at this revision)

1. **Literal-in-lesson test** — `grep -cF` ×3 → 0/0/0, exit 1 each. Verdict: the
   naive test fails, the quotes do not (line wrapping; wrap-tolerant 1 each). PASS.
2. **Class test, correct body** — `quote_class.py classify` ×3 → collapsed-only /
   raw-substring / raw-substring, exit 0 each. Verdict: matches r68. PASS.
3. **Instrument self-test** — `quote_class.py --selftest` → `selftest 4/4`, exit 0;
   the instrument separates all three classes on its own fixtures. PASS.
4. **Able-to-fail, fabricated quote** — S133 text + `yy` → `derived=absent`, exit 0.
   `collapsed-only` is not a default return. PASS.
5. **Able-to-fail, wrong body** — S434 sub-quote against S133's body →
   `derived=absent`, exit 0. A wrong-body citation cannot pass as raw. PASS.
6. **Ablation, behavioural** — renamed `classify` → `derive_class` in a throwaway
   clone; S133 still derived `collapsed-only`. Class rides on bytes, not a symbol
   name. PASS.
7. **Red/green M2 control** — `grep -c '/tmp'`: round-68 file **1** (exit 0; its
   worktree bytes equal the committed blob `2c84fb0b…`, mtime 14:51:42 — before
   this seat began, so unmodified), new receipt **0** (exit 1). PASS.

No result carried over from round 68 unrun.

## Residual unknowns

- The r67 lesson contains no quote-class word at all (`raw-substring|collapsed-only|quote-class`
  → none), so r68's "no raw claim was ever recorded for S133" is consistent but is
  absence of evidence in that file only; other round-67 venues were not searched.
- The 26-word S434 form exceeds the ≤25-word cap; the 22-word sub-quote is in cap.
  That is an r68 ruling already on record — this seat re-derives numbers only.

## Tooling

Nothing installed or upgraded. Used `git show`, `grep`, `wc`, `sed`, `sha256sum`,
`python3 -B` (stdlib). Scratch `/fast/scratch/hyaku/kake-r69/ScoutR68Receipt/`
removed on exit. No tracked lane file touched (`git status --porcelain` shows only
untracked round-69 wave paths).
