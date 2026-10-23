# ReviewHarmRealRun — H2 (round-39 real run byte-equal) — wave 2 attack

Verdict: **H2 HOLDS — no falsification found.** The build's real-run output is
byte-equal to tip41's, `jq -S . | sha256sum` = `fd985a41867e…` (matches
scorecard fd985a41…), exit 1, equal to rounds 39–41 receipts.

## Command and results

Run from the input directory, manifest path relative:
`cd .ufo/waves/round-41/realrun` (inputs identical to round-39 realrun:
manifest `dfb8a1b6…`, fsf `9dabd65a…`, mdn `9ea170a0…`, nodejs
`4625ce3a…`, postgresql `92f7bd8d…`, rfc-editor `f1e39049…`, ruby-lang
`c3fb0e36…` — matches `round-39/verification/realrun/inputs.sha256`).

1. tip41 reference: `timeout 900 prlimit --as=8000000000 -- python3 -B
   /fast/scratch/hyaku/kake-r42/shared/tip41.py --manifest manifest.json`
   → exit=1, stdout 10050 B, stderr empty (sha256 `50287ac6de56…`).
2. Build tool: `timeout 900 prlimit --as=8000000000 -- python3 -B
   /home/vgpnk/Projects/shokunin/kake-shokunin/scripts/sitemap_audit.py
   --manifest manifest.json` → exit=1, stdout 10050 B, stderr empty (sha256
   `914ebdee7bcb…`).
3. `cmp tip41-out.json build-out.json` → identical, exit 0 (raw byte-equal,
   stronger than the jq-normalized contract).
4. `jq -S . tip41-out.json | sha256sum` = `fd985a41867ed31b02ab03797562a1f0
   1969aa3fc01c293eda145c2a7a4bc8a5`; same for build output.
5. Historical receipts re-hashed: `round-39/verification/realrun/
   reference-663e051e.json` and `build-565ef4c9.json` both →
   `fd985a41867ed31b02ab03797562a1f01969aa3fc01c293eda145c2a7a4bc8a5`
   (rounds 39–41 equal).

## Findings

- No finding. Checked statement (H2 real run byte-equal, exit 1, equals
  rounds 39–41) **holds**, observed on the build `020bc457` tool
  `914ebdee…` exactly as scored.

## Tooling

- No tools installed or updated (none needed; `jq` present).

## Residual risk / verification gaps

- I exercised only the frozen round-39/41 real-run manifest (6 checks). H2
  is a fixed-input check; broader equality is covered by the counter v3
  receipts (10,218–10,229 values, 10/10) and H4 probe, not re-run here.
- Raw byte-equality and jq-normalized hash both verified; no divergence
  observed anywhere.
