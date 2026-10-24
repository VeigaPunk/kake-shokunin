# ReviewCensusAfter — round 31 wave 2 (falsify, freshness axis)

Seat: KakeR31a2.ReviewCensusAfter. Attacked the post-round census claim: kake SOURCES.md
rows 56 → 61 with tiers/statuses, and the attempt-1 receipt `census-after.txt` being
reproducible byte-identical. All work in sandbox `/fast/scratch/hyaku/kake-r31/a2-w2/ReviewCensusAfter/`
(TMPDIR set inside it); no lane mutation; no installs made (none needed).

## Commands run and exit codes

1. `bash /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kake` → exit 0
2. `bash /home/vgpnk/Projects/shokunin/scripts/sources-census.sh census --root /home/vgpnk/Projects/shokunin kake` → exit 0
3. `bash /home/vgpnk/Projects/shokunin/scripts/sources-census.sh selftest` (TMPDIR in sandbox) → exit 0, 96 `killed`, 0 `SURVIVED`
4. `git -C <lane> rev-parse HEAD` → 92235a0578b04458c5eb96c966f82fa03593130e (tip confirmed)
5. `git -C <lane> show f1ffb817…:corpus/SOURCES.md` and `…92235a05…:corpus/SOURCES.md` into sandbox (read-only) ;
   `cmp <lane working copy> tip-SOURCES.md` → identical
6. `sources-census.sh census --file before-SOURCES.md --today 2026-10-22` → exit 0
7. `diff before-SOURCES.md tip-SOURCES.md` → exit 1 (expected: 5 added rows + trailing note)
8. `cmp fresh-validate.out <(first 2 lines of census-after.txt)` → identical; sha256 both 83c923f0e19c88eb…
9. `sha256sum census-before.txt census-after.txt` → both 6ba6b7890280f8f39bca845e860a02c560c2dac25206b5eac0f714744795c186
10. `git status --porcelain -- .ufo/waves/round-31/ | grep -i census` → `?? .ufo/waves/round-31/census-after.txt` (untracked);
    `git ls-files --error-unmatch census-before.txt` → tracked; `census-after.txt` → not known to git (exit 1)

## Observed outputs

Fresh census at tip 92235a0 (sandbox `fresh-census.out`):

```
kake	rows	61          kake	tier.A	52   kake	tier.B	1   kake	tier.C	8
kake	status.mined	48  kake	status.queued	6  kake	status.rejected	7
FLEET	rows	61  tier.A 52  tier.B 1  tier.C 8  tier.invalid 0  missing 0
FLEET	status.queued 6  status.mined 48  status.rejected 7  status.invalid 0
```

Census of base blob f1ffb81 (`census-before-blob.out`): rows 56, tier.A 47, tier.B 1,
tier.C 8, status.mined 43, status.queued 6, status.rejected 7; FLEET mirrors; missing 0.

Delta base→tip (blob diff, exit 1 as expected): exactly 5 added registry rows S057–S061,
each `docs | A | mined | 2026-10-22 | 90d`, plus a 2-line prose note appended after the
registry (no E12 fired). All pre-existing tiers/statuses unchanged: 47+5=52 tier.A,
mined 43+5=48, tier.B/tier.C/queued/rejected identical. Matches declared "rows 56 → 61".

Fresh validate (exit 0, sandbox `fresh-validate.out`): only
`kake	W04	S033 duplicate url www.rfc-editor.org/rfc/rfc9110.txt across scopes` then
`kake	ok	/home/vgpnk/Projects/shokunin/kake-shokunin/corpus/SOURCES.md`.
W04 is a warning, non-blocking (exit 0), present identically before and after.

## Findings

F1 (medium, receipt quality): `census-before.txt` and `census-after.txt` do NOT contain
census-mode output. Both are 3-line validate transcripts (validate stdout + a literal
`exit=0` echo line) and are byte-identical to each other (sha256 6ba6b789…). Validate
output is insensitive to registry size (56 or 61 rows produce the same two lines), so
these receipts cannot witness the 56→61 change they are named after. No census-mode
receipt exists anywhere under `.ufo/waves/round-31/` (full dir listing checked; also
`verification/`). The 56→61 claim is true (I verified it from blobs) but the named
before/after receipts do not evidence it. Recommend the L1 capture real census-mode
output at tip and, if a base-side receipt is wanted, census the f1ffb81 blob.

F2 (info, exact-match caveat): attempt-1 `census-after.txt` (mtime 2026-10-22
17:24:20Z, untracked) is byte-identical to a fresh run **on the script-stdout portion
only** (sha256 83c923f0e19c88eb…). Its third line `exit=0` is the runner shell's echo,
not script output, so a whole-file diff against script stdout would not match. If the
attempt-2 closure stores receipts, store stdout alone or keep the echo line clearly
labelled.

F3 (info): `census-before.txt` is tracked and `census-after.txt` is untracked; attempt-1
died before committing it. Timestamps: before 15:41:14Z, after 17:24:20Z — consistent
with the declared fetch window and the 17:24Z write.

F4 (none): no wrong numbers found. Row counts, tier split and status split all reconcile;
`FLEET` totals equal kake-only totals (single-lane scope); `missing 0`, `tier.invalid 0`,
`status.invalid 0`; script selftest healthy (96/96 killed, exit 0), so the parser is not
the source of any artefact.

## Evidence pointers

- Fresh runs: `/fast/scratch/hyaku/kake-r31/a2-w2/ReviewCensusAfter/fresh-validate.out`,
  `fresh-census.out`, `census-before-blob.out`, `selftest.out` (err files all 0 bytes)
- Blob extracts: `…/ReviewCensusAfter/before-SOURCES.md` (f1ffb81),
  `tip-SOURCES.md` (92235a0); working copy `cmp`-equal to tip
- Receipts: `kake-shokunin/.ufo/waves/round-31/census-before.txt`,
  `census-after.txt` (both sha256 6ba6b789…)
- Added rows: `corpus/SOURCES.md` lines 65–69 at tip 92235a0 (S057–S061)

## Not verified

- The 15:41Z source fetches / page contents behind S057–S061 (other seats own that).
- Base-side census rests on the f1ffb81 git blob, not a contemporaneous receipt (none exists).
- jj workstate of the lane untouched (read-only policy); not inspected.
