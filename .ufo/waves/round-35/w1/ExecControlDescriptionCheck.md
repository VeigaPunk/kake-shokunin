# Control description check — round 35, wave 1

Axis: operability. Implemented `/fast/scratch/hyaku/kake-r35/w1/ExecControlDescriptionCheck/control_description_check.py`. The CLI clones the supplied local repo under `TMPDIR`, fetches bundle refs, reads source/document blobs from their requested commits, selects the unique paragraph or table row containing the anchor, and passes only when that block backticks an exact nonblank source line of at least 20 characters and names its 1-based line number. Exit codes are 0 pass, 1 readable mismatch, 2 unreadable/ambiguous input.

## Exact checks and retained outputs

1. `TMPDIR=/fast/scratch/hyaku/kake-r35/w1/ExecControlDescriptionCheck/tmp python3 -B /fast/scratch/hyaku/kake-r35/w1/ExecControlDescriptionCheck/control_description_check.py --repo /fast/scratch/hyaku/kake-r35/w1/ExecControlDescriptionCheck/clone --bundle /home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-34/retained/r34-c1-lookup-dcef39b5.bundle --revision dcef39b5f4e8373970eb74858d2c6175524cdfd0 --path scripts/link_preview_audit.py --doc corpus/lessons/round-34.md --doc-rev 318561efa67206699fdaf259ffb86e39f2d916a8 --anchor dcef39b5` — exit 1. Output: `FAIL: paragraph for anchor 'dcef39b5' does not backtick a whole source line of at least 20 characters and name its line number.` Receipt: `/fast/scratch/hyaku/kake-r35/w1/ExecControlDescriptionCheck/round34-row4-fail.txt:1-3`.
2. `TMPDIR=/fast/scratch/hyaku/kake-r35/w1/ExecControlDescriptionCheck/tmp python3 -B /fast/scratch/hyaku/kake-r35/w1/ExecControlDescriptionCheck/control_description_check.py --repo /fast/scratch/hyaku/kake-r35/w1/ExecControlDescriptionCheck/sample-repo --bundle /home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-34/retained/r34-c1-lookup-dcef39b5.bundle --revision dcef39b5f4e8373970eb74858d2c6175524cdfd0 --path scripts/link_preview_audit.py --doc sample.md --doc-rev 8c606a89c4b08b9e2371f90a3c40e35e509d1f6a --anchor dcef39b5` — exit 0. Output: `PASS: paragraph for anchor 'dcef39b5' quotes source line 1 verbatim (29 characters).` Receipt: `/fast/scratch/hyaku/kake-r35/w1/ExecControlDescriptionCheck/sample-pass.txt:1-3`.

The corrected paragraph is `sample.md:1`; it quotes the retained control's actual `scripts/link_preview_audit.py:1`, `import hashlib, json, os, sys`. To make the sample addressable by `--doc-rev`, I made a sample-only fixture commit `8c606a89c4b08b9e2371f90a3c40e35e509d1f6a` in the sandbox `sample-repo`; no lane commit or Git state was changed. The failing document is the round-34 table row at `corpus/lessons/round-34.md:68`, revision `318561efa67206699fdaf259ffb86e39f2d916a8`; the bundle advertises `dcef39b5f4e8373970eb74858d2c6175524cdfd0` as `refs/heads/lookup-c1`.

## Evidence and limits

- Script SHA-256: `fcc77676c05d9ebc6abc707f3b62a98b674a7bdd18db2553771f67aa7bfd3cf4`.
- Sample SHA-256: `7970b4a3421a5503baaebf8f5d0c2c0d3bd4c468cddcf87cd9c0c171f16ef26d`.
- Failing receipt SHA-256: `2f90cc45f984f3812136808af4313ad54291261bb51ec1f051b428b422ff2a8c`.
- Passing receipt SHA-256: `959901d659d13cbabbc86820d77605ec31f6e16b970414507d6f14c15b2f6f98`.
- Only the two requested CLI cases were run; no build, lint, formatter, or broader test suite was run. No tools were installed. LSP was not exposed in the available tools; this new script required no existing symbol refactor. Risk: the checker intentionally requires UTF-8 blobs and explicit line labels (`line N`, `LN`, or `path:N`); other citation styles do not pass. Blockers: none.
