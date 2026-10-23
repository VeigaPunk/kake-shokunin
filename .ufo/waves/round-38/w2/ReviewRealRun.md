# ReviewRealRun

Axes: **operability** and **freshness**. Scope is the `scripts/robots_audit.py` build at `3ed8e15c2707ac4cec88f48fc9be48b35be4f2b0` versus base `af43a50fa399881eead9381d835b78a015e277a6` on the two assigned retained-input sets. No network requests or tool installs.

## Verdicts

- Round-37 55-check result preserved: **holds**. Both revisions exit 0 with `{"version":1,"verdict":"clean","checksEvaluated":55,"findings":[]}`.
- Round-38 (h), (i), (k) behavior on the wave-1 real-run inputs: **holds for this corpus**. Built tool matches all 7 declared reports; base matches 1/7 and mismatches 6/7.
- Base-to-build output changes: **contract-justified**. No actionable defect found in the assigned real-run scope.

## Commands and observations

1. `timeout 120s env TMPDIR=/fast/scratch/hyaku/kake-r38w2/ReviewRealRun/tmp python3 -B /fast/scratch/hyaku/kake-r38w2/ReviewRealRun/clone/scripts/robots_audit.py --manifest /home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-37/realrun/robots/manifest.json` — tool exit **0**, clean/55/no findings.
2. Same command with `/fast/scratch/hyaku/kake-r38w2/ReviewRealRun/base/scripts/robots_audit.py` — tool exit **0**, identical clean/55/no findings.
3. `timeout 240s env TMPDIR=/fast/scratch/hyaku/kake-r38w2/ReviewRealRun/tmp python3 -B /fast/scratch/hyaku/kake-r38w1/ExecRealRunPrep/realrun/run_realrun.py --tool /fast/scratch/hyaku/kake-r38w2/ReviewRealRun/clone/scripts/robots_audit.py --out /fast/scratch/hyaku/kake-r38w2/ReviewRealRun/wave1-built` — harness exit **0**; all 7 manifests matched, none unrunnable (runner caps each tool run at 20 s).
4. Same harness command with `/fast/scratch/hyaku/kake-r38w2/ReviewRealRun/base/scripts/robots_audit.py --out /fast/scratch/hyaku/kake-r38w2/ReviewRealRun/wave1-base` — harness exit **1**; 6/7 mismatched, none unrunnable.

Base → build deltas, each matching the public amendment:

- `manifest.json`: base `failed-policy`, exit 1, 91 evaluated, two `blocked` findings (`r38-k-en_wikipedia_org-pct2e`, `...pct72`); build `could-not-evaluate`, exit 2, 79 evaluated, 12 `check_invalid` findings for the 12 excluded-ASCII URL checks. Rule (i) faults those URL characters; rule (k) normalizes the two Wikipedia paths to `/robots.txt`, removing the base-only blocks. The other 79 checks (55 inherited + 13 implicit-allow + 11 ordinary percent-path) have no finding.
- `manifest.h-nan-unused.json`: base clean/exit 0/2 evaluated → build input-invalid/exit 2/0 evaluated. (h) rejects `NaN` even in an unread field.
- `manifest.h-infinity-status.json` and `manifest.h-neginfinity-status.json`: base check-invalid on the named check/1 evaluated → build input-invalid/null check/0 evaluated. (h) rejects non-JSON constants before checks.
- `manifest.h-long-status.json`: base input-invalid/null check/0 evaluated → build check-invalid on the 5,000-digit status/1 evaluated. (h) requires arbitrary-length JSON integers to remain JSON and the out-of-range status to fault only its check.
- `manifest.h-unused-bigint.json`: base input-invalid/exit 2/0 evaluated → build clean/exit 0/2 evaluated. (h) says an arbitrary-length integer in an unread field changes nothing.
- `manifest.h-float-status.json`: unchanged and matches in both revisions: check-invalid, exit 2, one evaluated. `1e400` is a JSON number parsed as a float, not an integer status.

## Evidence and limits

- Built/base tool SHA-256: `f4d057c4afac885b998de404da8c19f2d5d0a4d754a9d539e49b07d3f36baace` / `944d2f51f396fb6e1ba3c7cf07112eb3f55d011e9bbc16bb1a59af517be1d3e5`.
- Round-37 manifest SHA-256 `f184b0b9ad328282c55a68e4c66277fd4b735dbeb65d18e527b263db791a5463`; recorded `audit.json` is clean/55 (SHA-256 `6f0bb5b78b3b4bf2e5f07f4e568dce25185d1fa2ee2ea48161a06bd420eae950`). Wave-1 `manifest.json` SHA-256 `9e683943476eb918f499b3337066b347409046979338f2670049ff6d16b898a9`.
- Run receipts: `.../wave1-built/summary.json:8-90` (SHA-256 `ca7ec7074ec8a4b24344aa0a8157591612fa2b5f402ed21dcb92e4ff28562242`); `.../wave1-base/summary.json:8-118` (SHA-256 `f4bc686547349a7498dee76e56933c7602f10bd49510f707f8fdc9987cd7a82b`). Main-manifest exact output/diffs: built receipt `.../wave1-built/receipt-manifest.json:78-141` (SHA-256 `9f1a3c843f577663ac04afacfc447a65a63ab3500cef9dc4618fe5369741aa27`); base receipt `.../wave1-base/receipt-manifest.json:78-107` (SHA-256 `0a84823945faf7504ca6e919311dc1fe7830f6e4296e3ca02e7bb665031ae4d7`).
- Contract: built-revision `SCORECARD.md:1798-1858,2145-2162` (SHA-256 `b7432d69ffc4302bf0f5f6604913699f1d9ad996846e866230ceb257d7b31841`); implementation details: `scripts/robots_audit.py:22-31,421-476,508-531,602-629` (built-tool SHA above). Wave-1 provenance/limits: `README.md:8-22,34-64,95-103` (SHA-256 `1633d03796835c799ec38b7217f9d9f8f08011bf0387ffb63776ef4efb0f0708`).
- Freshness residual: these are retained robots bodies and synthetic URLs; wave-1 README says no new fetch and no live re-verification. The results support offline consistency against these snapshots, not current host policy or crawler behavior.
- Verification gap: `xd://lsp` returned “No such tool” (mounted devices listed ast_edit/debug); status, references, definition, and diagnostics were unavailable. Grep was only used to locate contract text, not as semantic proof. No other checks were run.
- Runtime/routing/saturation: this is a standalone CLI behavior check; no identity-based reroute or saturation-score claim is in the changed surface. The wave-1 harness records the single invoked interpreter as `/usr/bin/python3` 3.14.8 (`wave1-built/summary.json:3-7`).