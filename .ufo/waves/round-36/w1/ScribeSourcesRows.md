# Round 36 wave 1 — ScribeSourcesRows

## Axes and behavior
- Axes: freshness; operability (web properties and publishing).
- Drafted seven registry rows, S088–S094, in the requested 11-cell shape at `/fast/scratch/hyaku/kake-r36w1/ScribeSourcesRows/rows.md`.
- S088–S092 and S094 are proposed as `mined`, opened 2026-10-23, recheck 90d, used by `scripts/source_recheck.py`. S093 is `rejected`.
- S094 admitted at tier B: the retained MDN guide adds practical method-handling, alternative redirect mechanisms, precedence and loop guidance beyond the protocol semantics, while explicitly remaining explanatory rather than normative.
- S093 rejected at tier C: its lead restates HTTP 301 as permanent and quotes RFC 2616 §10.3.2; its Search engines section points to Bing and Google help pages but adds no primary protocol evidence.

## Provenance and evidence
- Read the public C1 contract at commit `cd3212796cab7a2afa03b638dbfafe7194df9629` (SCORECARD.md, section “C1 contract”) and the retained source texts S088–S094. Row schema and adjacent examples: `corpus/SOURCES.md` lines 86–95; overlapping scopes: rows S010, S028–S033.
- Fetch receipts: `.ufo/waves/round-36/sources/receipts.json` lines 2–84. Recorded access times are 2026-10-23T01:08:56Z–01:09:01Z, all HTTP 200; text SHA-256 prefixes in the draft match receipt `textSha256` values.
- Relevant source evidence: S088.txt line 1, RFC 9110 §§10.2.2, 15.4, 15.5.5 and 15.5.11 (grep excerpts at offsets 207648, 314484, 330814 and 334479); S089.txt line 1, §5.2 resolution procedure (excerpt at offset 69888); S090.txt line 1, §§4.2 and 6.1; S091.txt line 1, §§1.2–1.3; S092.txt line 1, §13.1.2; S093.txt line 1, lead and Search engines; S094.txt line 1, guide sections cited in the draft.
- Draft artifact snapshot: `/fast/scratch/hyaku/kake-r36w1/ScribeSourcesRows/rows.md` (`#95E3`).

## Gates, touched surfaces, limits
- Shell command 1, exit 0: `env -u GIT_DIR -u GIT_WORK_TREE -u GIT_INDEX_FILE timeout 300s git -C /home/vgpnk/Projects/shokunin/kake-shokunin show cd3212796cab7a2afa03b638dbfafe7194df9629:SCORECARD.md | tail -130` — printed the public contract and receipt/counter context.
- Shell command 2, exit 0: `timeout 300s mkdir -p /fast/scratch/hyaku/kake-r36w1/ScribeSourcesRows/tmp /fast/scratch/hyaku/kake-r36w1/ScribeSourcesRows/.ufo/waves/round-36/w1 && export TMPDIR=/fast/scratch/hyaku/kake-r36w1/ScribeSourcesRows/tmp && printf 'sandbox ready; TMPDIR=%s\n' "$TMPDIR"` — created the assigned sandbox directories and printed the TMPDIR value.
- Written surfaces: the sandbox draft above and this lane report only. `corpus/SOURCES.md`, product code, Git index and lane jj state were not modified. No tools were installed.
- No row-shape checker, build, tests, or sealed counter was run; the counter/key and all contents under `/fast/scratch/hyaku/kake-r36/` were not accessed. No live network requests were made. The registry rows remain a draft, not admitted lane entries; no claim about tool behavior or passing the frozen predicate is made.

Report path: `.ufo/waves/round-36/w1/ScribeSourcesRows.md`
