# ReviewV2Timing — attacks the C2 counter v2 timing/claim: "version 2 (bd14096a) landed before any build was measured" and that v2 narrows; also the honest entry's pass.

Axes: freshness, operability. Method: git history in a sandbox clone + executing both counter versions. No lane mutation; no tools installed (none needed).

## Order (git log --date-order on linear lane history; commit times -03:00, 2026-10-22)

| # | rev | time | what |
|---|-----|------|------|
| 1 | 16a6b8b | 18:54:04 | round-34 spot-check base |
| 2 | 81d9fd74 | 19:08:40 | declaration; sealed_count.py = v1 (sha256 `c4d58dae…49ef`), sources S006/S078–S085 + receipts.json, census-before |
| 3 | 318561ef | 19:09:56 | controls scored before build: 12 control-*.json/.exit receipts (v1) + 4 retained control bundles |
| 4 | bd14096a | 19:34:41 | counter v2 (`1b4d9d59…469b`) + sealed_count_v1.py kept + control-v2-* rescans + reworded control |
| 5 | b1cbbc39 | 19:35:03 | C1 build |
| 6 | 95abec21 | 19:37:14 | C2 build (entry, SOURCES S078–S087, S006 used-by, S074 note) |
| 7 | 4c6be2bd | 19:37:28 | sealed-key reveal |
| 8 | 6128873 | 19:37:53 | build receipts (c1-at-*, c2-at-*, selftest, r34 matrix, c2-v1-at-95abec21) |

bd14096a precedes the first build commit (b1cbbc39) and precedes every build-measurement receipt (6128873). Receipts before bd14096a = exactly the files of 81d9fd74 and 318561ef (25 + 24 files: census-before.txt, fetch_sources.py, counter v1, sources S006/S078–S085/receipts.json, 4 retained bundles, 10 control-*.json + .exit pairs). None measures a round-35 build: every one pins revision `16a6b8b8`, `81d9fd74`, or a synthetic control commit (`5f767534`, `dcef39b5`, `0cce15f0`, `04848219`, `e5263d41`, `ae9fb361`); the build hashes b1cbbc39/95abec21 appear under verification/ only in post-bd14096a commits. All pre-bd14096a receipts record `counterSha256 c4d58dae…` = v1. Timing claim holds in git history.

## sealed_count_v1.py → sealed_count.py behaviour changes (diff; sandbox clone working tree)

1. Size: v1 `len(text.split()) <= 1500`; v2 `len(words(clean(text))) <= 2200` (`[a-z0-9]+` runs). **Can make met EASIER**: ceiling relaxed ~47%; an entry of 1500–2200 real words that v1 rejects can pass v2. Partially offset: punctuation splits raise run counts (harder for punctuation-padded junk). SCORECARD.md:1471 discloses this ("1500 whitespace-word cap … equals about 1750 such words; 2200 leaves room").
2. `clean()` added (NFKC, Cf/U+200B strip, HTML-comment removal) applied to entry and SOURCES.md before word count, cite-id regex, probe normalization, registry rows and copiedShare shingles. **Harder** (anti-gaming: hidden padding/rows/ids/ZWSP splits/lookalikes no longer count). Easier-side residue: comments no longer inflate the word budget, but comment text also stops counting for cites/probes, so no gaming path.
3. registry_rows: only the FIRST `## Registry` section counts (v1: every such section) — **harder**; tilde fences recognized and fence kinds tracked (v1 toggled only ``` so ~~~-fenced fake rows counted) — **harder**.
4. Good cite additionally requires the id in `.ufo/waves/round-35/sources/receipts.json` at REV with non-empty url present in the row's source cell. **Harder** (pure AND-condition).
5. Output gains `counterVersion: 2`; docstring updated. No effect.
6. Unchanged: C1 path, the 12 sealed probes, both key pins (`a861dcd…`, `111bcee…`), targets — confirmed by diff and by execution below.

Net: 4 changes harder-or-neutral (2,3,4,5), 1 change can ease met (1). v2 narrows every gaming vector it touches except the size ceiling.

## Honest entry (corpus/knowledge/security-txt-publishing.md at 95abec21) under both versions

- v2: `python3 -B .ufo/waves/round-35/sealed_count.py c2 --root . --revision 95abec2 --key-revision 4c6be2bdec…` → exit 0, met True, words 1388, copiedShare 0.0, goodCites S078,S079,S080,S082,S083,S084,S085,S086 (8), probes 12/12.
- v1: same command with `sealed_count_v1.py` → exit 0, met True, words 1298, same 8 goodCites, 12/12 probes. Matches retained receipt `verification/c2-v1-at-95abec21.json` (committed 6128873, counterSha256 `c4d58dae…`).
- C1 unchanged: both versions at b1cbbc3 → exit 0, 24/24 passed each.

Verdict: the honest entry meets under both versions — the v2 loosening (size cap) did not create the C2 pass; v2's scorecard numbers (1388 words, 0.0 copied, 8 cites, 12/12) reproduce exactly.

## Falsification result

No defect found in the attacked claim. v2 landed (committed) before the build commits existed and before any build-measurement receipt; its diff is overwhelmingly narrowing with one disclosed widening (size cap 1500→2200 under a changed metric) that is honest, disclosed in v2's own docstring and SCORECARD.md:1470-1471, and immaterial to the honest entry (1298/1500 vs 1388/2200).

## Residual risk / not verified

- "Before any build was measured" is provable only for receipts committed to git; an uncommitted local measurement of a build against v1 before 19:35:03 is not observable from history (same trust model as the rest of the round).
- bd14096a precedes b1cbbc39 by 22 seconds of commit time; order is linear git history, not independently timestamped wall-clock execution.
- I did not re-run the 22 control-v2-* rescans or the C1 24-case table per-case (out of item scope; sibling seats own those).
- jj operation order not consulted (item specifies git history); no mutation checks beyond read-only git in the sandbox clone at /fast/scratch/hyaku/kake-r35/w2/ReviewV2Timing/clone.
