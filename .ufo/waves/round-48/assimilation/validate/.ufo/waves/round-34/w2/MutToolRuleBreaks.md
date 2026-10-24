# Round 34 wave 2 — MutToolRuleBreaks

Axis: operability. Thirteen single-rule mutants were each committed from pristine `24a16474ee73e20453f3e1be9d2f33573c5196d9` in the isolated sandbox clone; no mutant was cumulative.

Commands per row (C1 revision is the full commit in the table; stdout receipts are raw JSON):
- `TMPDIR=/fast/scratch/hyaku/kake-r34/w2/MutToolRuleBreaks/tmp python3 -B .ufo/waves/round-34/c1_matrix_count.py --root "$PWD" --revision <commit>`
- `python3 -B scripts/link_preview_selftest.py --tool scripts/link_preview_audit.py`
Raw JSON stdout was captured to the corresponding `evidence/<mutant>.{c1,selftest}.json` (name-attribute run via redirection; others via `tee` with `set -o pipefail` and a summary parser). The exit codes below are the detector codes.

Pristine before: C1 28/28, exit 0; selftest 29/29, exit 0. Restored after: same. Mutated tool SHA-256 is listed per row; killed means detector failed the mutant.

| Mutant | Commit | Mutated tool SHA-256 | C1 score (exit) | Selftest (exit) | Killed by |
|---|---|---|---:|---:|---|
| `name=` counts | `85c275282724faa610694d32c85c55bcd8715ae3` | `50c705dfaafb9ff06e2ea4ba17153925906c8d2a8b2816a19946af6061461bc4` | 27/28 (1) | 27/29 (1) | both |
| og:type threshold raised | `f6674da1546a894b2d86e5d6220a19423bbdb3bd` | `1cf4ed1fb6de92297bd5229779eb3ed0c3d546d5b8d1b4b8d810420da72861f4` | 27/28 (1) | 27/29 (1) | both |
| empty content counted | `7ff521c400e0f78143ae36e6203052e054601ebe` | `445a514dbfc82b076557b8941eefaba0f2dcfb973a9631cbfa4130585fdcb0c0` | 27/28 (1) | 27/29 (1) | both |
| whitespace not stripped | `7c15d4dabe487d59f85fb2cb903fe0c10ac08cdf` | `5c7bbe99117b96b3c15ea790731ba85d19362eb1c61d5fa2fd79ffdbed8b9ac7` | 26/28 (1) | 27/29 (1) | both |
| canonical not resolved | `198abdfcb34af453604db07af846cf00948152c7` | `fc2cd0a709b1993d3551c484dd3916e351eff5a2cd860766646904a51dff4029` | 27/28 (1) | 24/29 (1) | both |
| last canonical wins | `7e521f9fc0021fef853db7c0cceb887bde6a347b` | `30c329b31c0734dbb690dd246a5903673e94bad27bbe4d07f168290522eae0dd` | 28/28 (0) | 27/29 (1) | selftest |
| og:url case-insensitive | `a9c0cd3d89f36c0e29309b6fcac8989b48a31b19` | `00244165d5bec474906855ff2b571ec29ea89b42b89a3c88d41de073aa2d71cf` | 28/28 (0) | 29/29 (0) | none |
| trailing slash normalized | `233baf8ac3963dd17a367c8a3723c774121b3c36` | `2ae904757fa15a048b9a9ed66b889b4fde21313a8d8025b1b20afeb1f111cba0` | 28/28 (0) | 29/29 (0) | none |
| input and policy findings mixed | `709ffb7909cd62b80d2d467c817044d42d147b2b` | `16dbd38afd4bbfcfc343e894cab46f02ee7274c608bffb3fec18cbc2668dba69` | 27/28 (1) | 28/29 (1) | both |
| policy/input exit codes swapped | `10a9855d4aa4a418c20d9f8da16090f34522f4e0` | `7b57a1749bd5c71d80749c21dad06ea44944a9350cffa6a7f39bffe1fc9c0f17` | 8/28 (1) | 9/29 (1) | both |
| path escape allowed | `2839e1c406570d726b05b938a97f2e7d26037361` | `8a39be10b2034a4c94e4f1d36fe350c435511e5004d41951494291a147868383` | 27/28 (1) | 28/29 (1) | both |
| non-UTF-8 maps to input_invalid | `1dee437de891be0c93b23785cc0959c55de12df0` | `039de079d77630ade007a3c5e19d15844aa5fff149f6f08ac1bca82461457b35` | 28/28 (0) | 29/29 (0) | none |
| only first page audited | `bba78e2eb182244cee5b2bb3bac284b12a5f6944` | `1e048dce8ca351525a95a035f29f7c926ab7915bd555fc7c6e390e61ab7ec5e3` | 27/28 (1) | 28/29 (1) | both |

Survivors of both: case-insensitive og:url comparison, trailing-slash normalization, and non-UTF-8 misclassification. No counter-only survivor. C1/selftest raw outputs and their per-file SHA-256s are indexed at `/fast/scratch/hyaku/kake-r34/w2/MutToolRuleBreaks/evidence/SHA256SUMS.txt:1-28` (index SHA-256 `95a0846169b100a8adecca980dc539566b7ebc8f624d2f3906f972bee0267b7a`); `sha256sum -c` reported all entries OK. Restored source hash before/after: `8dd0018248e04d4e7dd7d901acd846b687a420b559125695b7f2cf5a3c91d875`. Sandbox ended detached at the pristine commit with clean status. No tools installed or updated.
