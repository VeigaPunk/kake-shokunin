# ReviewHarmRealRun — harm rule half 2: round-39 real run byte-equal at the build

Scope: SCORECARD.md "Round 41" harm-rule claim — `jq -S . | sha256sum` = `fd985a41867ed31b02ab03797562a1f01969aa3fc01c293eda145c2a7a4bc8a5` for both base and build on the retained inputs.
Seat: KakeR41.ReviewHarmRealRun (leaf). Sandbox: /fast/scratch/hyaku/kake-r41w2/ReviewHarmRealRun/.

## Setup (all verified)

- Inputs copied: `cp -r .ufo/waves/round-41/realrun /fast/scratch/hyaku/kake-r41w2/ReviewHarmRealRun/realrun`
- `cd realrun && sha256sum -c SHA256SUMS` → exit 0; all 7 files OK (manifest.json + 6 sitemaps).
- Base tool: `git show 8eb121c8:scripts/sitemap_audit.py` → sha256 `4de35f8c9d3e7849b6c19e9cfb3c9466f604545a143e29d8480dffcb55a1460e` — matches claim `4de35f8c…1460e`.
- Build tool: worktree `scripts/sitemap_audit.py` at HEAD `eae5ae2c7dc5de2ba489f02b936fc5040b07b7d6` → sha256 `0b485431d96268d46c8dc9052eec92520248a03989896bd83f4521f15f13edbf` — matches claim `0b485431…13edbf`.

## Runs (cwd = sandbox; `python3 -B <tool> --manifest realrun/manifest.json`)

- Base : exit 1, raw sha256 `2ffbea3a8fafa3ca8d7c759acc2c6c7df9646a74c388757800f6598e9180b22e` (base_out.json)
- Build: exit 1, raw sha256 `2ffbea3a8fafa3ca8d7c759acc2c6c7df9646a74c388757800f6598e9180b22e` (build_out.json)
- `cmp -s base_out.json build_out.json` → byte-identical (stronger than canonical-JSON equality).
- `jq -S . | sha256sum`: base `fd985a41867ed31b02ab03797562a1f01969aa3fc01c293eda145c2a7a4bc8a5`; build same — both equal the claimed digest.
- Output verdict: `failed-policy`, 6 check items; exit 1 is identical for both tools and consistent with a findings verdict, not an error path.

## Findings

None. No defect found in scope.

## Per checked statement

- "`sha256sum -c SHA256SUMS` verifies retained inputs": holds (exit 0, 7/7 OK).
- "Round-39 real run is byte-equal at the build": holds — raw output is literally byte-identical; canonical digest `fd985a41…bc8a5` matches the claimed value for both tools.
- Tool sha256 anchors (`0b485431…13edbf` build, `4de35f8c…1460e` base): hold.

Verdict for this half of the harm rule: **holds** (byte-equal, claimed digest reproduced from retained inputs). No installs needed; tools used: cp, git show (read-only), sha256sum, python3, jq, cmp.
