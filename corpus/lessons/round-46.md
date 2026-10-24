# Round 46 — lesson

## Mistakes

1. **class:** frozen-counter base never measured (calibration) ·
   **evidence:** SCORECARD round-46 declarations froze the QUALITY criterion
   leg as `grep -c '^- .*receipt.*\(path\|sha256\)' corpus/QUALITY.md` 0 → 1;
   measured at base `7cdbaefd…` the command already returns 2
   (`.ufo/waves/round-46/verification/quality-broad-base.txt` vs `-tip.txt`,
   2 → 3) · **captured-by:** none — the freeze-before-data rule pinned the
   sentence but no rule required running the counting command at base before
   freezing its before-value (same family as round-45 C1's falsified causal
   clause) · **fix:** every round-46 counter was measured at base before any
   after-claim (c1-before/c2-before receipts in `verification/`), and the
   criterion leg re-landed under a sealed narrow counter
   `grep -c '^- \*\*Receipt identity for filed counts' corpus/QUALITY.md`
   0 → 1; the fix is shown able to fail — the frozen broad command still
   reads 2 → 3, and the falsified leg is reported NOT MET as declared rather
   than re-pinned.
2. **class:** wave dispatched with no build owner (operability) ·
   **evidence:** `.ufo/waves/round-46/w46-dispatch.json` (64 seats, one
   batched call) returned 12 seat reports, every returned build/attack seat
   BLOCKED — `w1/ExecRedirectSelftest.md`, `w1/ExecCitationSelftest.md`,
   `build/replay-proof.md`, `build/budget-sizing.md` all record
   "scripts/redirect_audit.py: No such file or directory" — the executors
   tasked to write the tools never delivered before the attempt reset ·
   **captured-by:** none · **fix:** the L1 is the integration owner for the
   round's build artifacts: both tools, the sealed counter and the fixtures
   were landed by the L1 this round, and only then scored; the fix is shown
   able to fail — the after-stage receipts
   (`verification/c1-after-<tip>.json`, `c2-after-<tip>.json`) re-derive the
   whole matrix and exit non-zero if any witness is uncaught (the blocked
   wave's state would still fail them).

## Gate

- **S135 — Cloudflare Pages redirects docs**
  (https://developers.cloudflare.com/pages/configuration/redirects/):
  opened 2026-10-24T05:39:49Z by the L1 with one public GET (HTTP 200,
  139,250 bytes, retained text sha256 `73b3b4a8…ec18d` at
  `.ufo/waves/round-46/sources/S135.txt`, receipt
  `.ufo/waves/round-46/sources/receipts.json`). Located quote (16 words):
  "If there are multiple redirects for the same source path, the top-most
  redirect is applied." ADMITTED (mined, tier A): vendor-primary for its own
  product; grounds the Cloudflare precedence half of
  `corpus/knowledge/redirect-rewrite-rules.md` and the C1 manifest
  `resourcePrecedence` field. Second quote verified present: "Redirects are
  always followed, regardless of whether or not an asset matches the
  incoming request."
- Re-opened this round (recheck only, no cell change): S050 Render
  redirects/rewrites retained text (`.ufo/waves/round-30/sources/S050.txt`)
  re-read against `corpus/knowledge/redirect-rewrite-rules.md`; the resource-
  precedence and first-match quotes hold verbatim in the retained text.
- Rejections this round: none.

## Registry changes

- rows 134 → 135 (S135 added, mined, tier A). No status / recheck / used-by
  cell changed on any existing row.
- Sourced claim: C1 (the redirect/rewrite audit capability) rests on S135
  opened this round — the knowledge entry `corpus/knowledge/redirect-rewrite-rules.md`
  and the tool's semantics contract cite it together with S050.
