# ReviewC2Before — round 30 wave 1 (freshness)

Seat: KakeR30.ReviewC2Before. Attacked C2's "before 0/4" claim and the source
receipts for S049-S052. Sandbox: /fast/scratch/hyaku/kake-r30/w1/ReviewC2Before/
(TMPDIR inside it). No installs performed. No live requests made.

## 1. Counter re-run at base

Command (cwd = lane):
`TMPDIR=<sandbox>/tmp python3 -B .ufo/waves/round-30/c2_quote_truth.py --root . --revision 035668132250b75b38d399e86e540b0a0371efbc`
Exit code: 1 (expected: 0/4 means not all passed -> 1).

Output JSON matches the committed before receipt
`.ufo/waves/round-30/verification/c2-before-0356681.json` field for field:

| field | rerun | receipt | match |
|---|---|---|---|
| counter | kake-r30-c2-quote-truth | same | yes |
| counterSha256 | a2cd3164f67e221f0d38609afd50be61260902f963f05f96bd1b223451975e7a | same | yes |
| revision | 035668132250b75b38d399e86e540b0a0371efbc | same | yes |
| passed / total | 0 / 4 | 0 / 4 | yes |
| controlBroken | false | false | yes |
| per-id checks a-d | all false, quote null, S049-S052 | identical | yes |

The receipt holds the counter's stdout only; the extra line
`C2 0/4 at 0356681...` my run showed goes to stderr
(.ufo/waves/round-30/c2_quote_truth.py:127), so there is no discrepancy.
Working-tree counter script sha256 = a2cd3164... = `git show 4580c78:...c2_quote_truth.py`
hash, so the rerun exercised the committed counter bytes.

## 2. Receipt recomputation (sources/receipts.json)

All four rows, every recomputed value equals the receipt value:

| id | textSha256 (sha256 of <id>.txt) | bodySha256 (sha256 of gunzip <id>.html.gz) | bodyBytes (gunzip \| wc -c) |
|---|---|---|---|
| S049 | 3604f8f55e5ef2a9ada6eb8685e0ff1029bffc6ac304c2aa9ecf0fba0253d6f7 | 841b8311d66726cddaa55dd618a7f3a7cae5dba2259602ab8f2519882ab59544 | 320167 |
| S050 | 1c41364393defcba006be8ad33a1b34882ef455013032135a3daf0b43d52c5ed | a57b515f120fbc71865406d9a14b3438f01d74efa640c22e441303a8135c580e | 348130 |
| S051 | e98982cef9434d9521063602ea05bfa16af4dc756e1068cdf3a60d058332a27d | 7ba689dc5b68d177bba05484ccb170a8765084347f154e6fdd29192f34d03aac | 280291 |
| S052 | 6c1616f8214a4f5987681ea9b38db60a6b7d0b54d89cdd23687452566858f769 | 59469467e22fec821d9971756b5b0c83de002f7f89578df8913b1d2d5094e543 | 371923 |

Independent re-derivation: ran the fetcher's own `visible_text` rule over each
retained body (sandbox script rederive_text.py, exit 0). Reproduced all four
textSha256 values plus textWords 983/854/539/1488 and text byte sizes
6700/5846/3941/10166 — so textSha256 is genuinely derived from the retained
body, not a pasted value.

## 3. Fetcher hash

`git -C <lane> show 4580c78cca1185d059efa6970722bbcf2f9c1b0f:.ufo/waves/round-30/fetch_sources.py | sha256sum`
= b9431a5f349c7b857e2139fd148b8f75a2ddb8a4d94a3ea7013709a28a9190b4.
Working-tree fetch_sources.py hashes to the same value, and all four receipts
list fetcherSha256 b9431a5f349c7b857e2139fd148b8f75a2ddb8a4d94a3ea7013709a28a9190b4. Match.

## 4. Artifact stability at the claims commit

At 4580c78, `git show <rev>:<path>` hashes equal the working-tree hashes for:
the four S04x.txt, the four gunzipped S04x.html.gz, receipts.json
(39d36ec02636026fdfdce37f6434a1a9b0a3a11fae67f3402507080bf481577b),
verification/c2-before-0356681.json
(7b4f06c22725ac0ca2d6f4c7e17774ab2408af9c3197779cb0261f3fa72f6933), and
c2_quote_truth.py (a2cd3164...). Working tree and commit tell one story.

## Verdict

All declared C2 "before" evidence reproduces exactly: rerun 0/4 equals the
committed receipt, all 8 sha256 recomputations match, bodyBytes match, the
fetcher hash matches the claims commit, and text hashes re-derive from the
retained bodies. No defect found in the C2 before trail.

## Residual risk and what I did not verify

- Artifact-to-live-web correspondence is not re-verified: I made no GETs
  (bounds; not assigned). status 200, finalUrl, url, accessedUtc
  (2026-10-22T11:49:44Z/45Z) are taken as recorded in receipts.json.
- The original before-run's exit code is not stored in the receipt; exit-1
  equality across runs is [INFERENCE] from counter semantics (0/4 -> 1) plus
  the byte-identical stdout.
- Counter check d compares against receipts at the measured revision; at base
  the sources files may not exist yet, which alone yields 0/4 — the honest
  baseline is my receipts-side verification above, not the 0/4 alone.
- I did not rerun the counter at the claims commit (out of scope; after-state
  belongs to the falsify wave).
