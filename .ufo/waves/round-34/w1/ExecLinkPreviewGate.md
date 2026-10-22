# Round 34 C1 — offline link-preview audit

- Axes: operability (offline audit) and freshness (publishing metadata).
- Code file: `/fast/scratch/hyaku/kake-r34/w1/ExecLinkPreviewGate/clone/scripts/link_preview_audit.py`.
- Final sandbox commit: `7cc3587117583e11e8912dc0a57d4d82792b60cf`.
- Tool SHA-256: `56ec5b3047700f74387684b041aabca4715c407cfd1229de44f4398c3dfa2305`.
- Behavior: stdlib-only, `html.parser`, local UTF-8 manifest/pages only; reports missing required properties, multiple non-empty `og:type`, non-absolute `og:url`, and mismatch against the first canonical link resolved against the page URL. Does not access the network or write files. Docstring cites S067/S068 and lists the requested non-checks.

## Frozen matrix

Counter command (stdout saved to `.../c1-counter.json`):
`python3 -B /fast/scratch/hyaku/kake-r34/w1/ExecLinkPreviewGate/clone/.ufo/waves/round-34/c1_matrix_count.py --root /fast/scratch/hyaku/kake-r34/w1/ExecLinkPreviewGate/clone --revision 7cc3587117583e11e8912dc0a57d4d82792b60cf`
Exit 0; observed `C1 28/28`. Controls 6/6, defects 13/13, inputs 7/7, usage 2/2. `constantGatesAllRejected: true`; constant results: clean 6/28, failed-empty 0/28, refuse 6/28, all-missing 1/28.
- Saved counter JSON: `/fast/scratch/hyaku/kake-r34/w1/ExecLinkPreviewGate/c1-counter.json` (SHA-256 `0dd7f63cb91af988c2ff4b370829d7c497a79611066297a2589f8f35f57e3560`). Evidence: lines 4-23; matrix digest `246a6a3ba67a842c408f56b0240d2ad36969330c5a414b715f04b7e56fac14f7`.
- Iteration record: commit `efacac6de5f9757df77d2bc9789a9da1a5859a90` reached 28/28; intermediate commit `fa3529991f364ae249241f082ad56335933f8930` returned exit 1, 10/28 after parser calls were omitted; restored the calls and reran the final commit above at 28/28.

## Retained real input

- Extracted `/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-34/sources/ds4cc-7fc6aa2f/html.tar.xz` with `tar -xJf ... -C /fast/scratch/hyaku/kake-r34/w1/ExecLinkPreviewGate/real-input` (exit 0; source archive SHA-256 `818f06443470f6dcb4118cbb1ada15fd7880faeba40ac85e4418e0455d2fe7a3`).
- Generated `/fast/scratch/hyaku/kake-r34/w1/ExecLinkPreviewGate/real-input/manifest.json` from all 102 extracted `.html` files; URLs use `https://ds4cc.com/<relative path>` with a trailing `index.html` removed (root `index.html` maps to `/`). Manifest SHA-256 `65c4b0958024088f79c075b6ef69d3e2f730c8f90d9af6ba6fbe1894863d1941`.
- Audit command: `python3 -B /fast/scratch/hyaku/kake-r34/w1/ExecLinkPreviewGate/clone/scripts/link_preview_audit.py --manifest /fast/scratch/hyaku/kake-r34/w1/ExecLinkPreviewGate/real-input/manifest.json` (final exit 1).
- Final result: `failed-policy`, 102 pages checked, 146 findings. All 146 are `og_required_missing`: `og:image` 101, `og:title` 15, `og:type` 15, `og:url` 15. Saved JSON: `/fast/scratch/hyaku/kake-r34/w1/ExecLinkPreviewGate/real-input-result.json` (SHA-256 `01bbef744ca531e42237c30c08888532a2f01ee46568bb06bacabaf78f9bb809`).

## Evidence, risks, blockers

- Contract: `.ufo/waves/round-34/c1-matrix.json:6-14`; final counter evidence above. Retained source receipts: `sources/S067.txt:1` (SHA-256 `0174794e77743c78fa87850f1b7fad1e3ad8af7a6f4f709cdd3e86881e675581`) and `sources/S068.txt:1` (SHA-256 `2c9a5d3cf5fdcb7ac8d157baa6f583842fe2d859d45d28e7c83fedc7105baa72`).
- Risks: this is static source parsing only; rendered DOM, JavaScript-injected tags, image retrieval/size/type, Twitter cards and tag position are out of scope and stated in the tool docstring.
- Blockers: none. No LSP tool was exposed in the available tool set; no existing symbol refactor was needed. No packages/tools installed. No build, lint, formatter or additional tests run.
