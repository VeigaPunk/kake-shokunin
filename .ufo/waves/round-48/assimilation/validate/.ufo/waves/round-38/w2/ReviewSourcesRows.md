# Round 38 wave 2 — ReviewSourcesRows

Axis: freshness (operability of the registry checked). Scope: S098–S101 and S034 `used-by` at `adab4c7e9ec2178657395f49346f18800ff4796f`.

## Finding

- **P2 — `used-by` is incomplete for cited rows (overstated completeness).** CORPUS.md:107–108 defines `used-by` as repo-relative paths of knowledge entries or lessons citing the row. S034's current list at `corpus/SOURCES.md:42` includes `corpus/knowledge/robots-txt-rules.md` but omits `corpus/lessons/round-38.md`, which cites S034 and quotes RFC 8259 at `corpus/lessons/round-38.md:27–30`. The S034 addition to the knowledge entry is genuine (`corpus/knowledge/robots-txt-rules.md:91–100`), but the registry list is not complete. Separately, rejected S101's row at `corpus/SOURCES.md:109` lists only the lesson, while the knowledge entry also cites the S101 rejection at `corpus/knowledge/robots-txt-rules.md:108–110`. Add the missing citing paths and log any in-place `used-by` update old→new.

## Verdicts and checks

- **Rows/cells:** census found no E-code or missing path. The 13-cell rows, IDs, enums, dates/rechecks and rejected-row reason/flip are consistent with the registry contract; S098 and S099 produce W04 cross-scope duplicate-URL warnings only. S098–S100 are mined and genuinely cited in the knowledge entry: S098 at `:103–107`, S099 at `:113–120`, S100 at `:94–100` of `corpus/knowledge/robots-txt-rules.md`. S101 is rejected, not mined.
- **S034 used-by change:** the added knowledge-entry path is real and logged; the lesson gives the prior list and the addition at `corpus/lessons/round-38.md:55–56`. This is the sole in-place SOURCES row change in the diff, so the contract's in-place old→new rule holds. New S098–S101 rows are additions, not in-place changes.
- **Requested census:** `unset GIT_DIR GIT_WORK_TREE GIT_INDEX_FILE; export TMPDIR=/fast/scratch/hyaku/kake-r38w2/ReviewSourcesRows/tmp; timeout 300 /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kake` — exit **0**. Output: W04 for S033/S088/S092/S098/S099, then `kake ok`; no errors. W04 for S098/S099 is expected from same URL in distinct scopes. Captured output: `/fast/scratch/hyaku/kake-r38w2/ReviewSourcesRows/evidence/sources-census-kake.txt`, SHA256 `57fa990a7d7874a5bcd0abb4c03815720136044de07022a7b3c7eca70bc71ebb`.
- `git diff --quiet adab4c7e9ec2178657395f49346f18800ff4796f -- corpus/SOURCES.md corpus/lessons/round-38.md corpus/knowledge/robots-txt-rules.md` — exit **0** (working-tree target files equal the assigned tip; HEAD is `b7d821e3a79bd5d5fa7658b7cc82b2d385232a98`). `git diff --check af43a50fa399881eead9381d835b78a015e277a6..adab4c7e9ec2178657395f49346f18800ff4796f -- corpus/SOURCES.md corpus/lessons/round-38.md corpus/knowledge/robots-txt-rules.md` — exit **0**.

## Verification gaps

- LSP unavailable: `read xd://lsp` returned “No such tool” (only `ast_edit`, `debug` mounted). Markdown citations were checked literally; no semantic LSP proof is claimed. No external re-fetch was performed.
- No tools installed or updated.