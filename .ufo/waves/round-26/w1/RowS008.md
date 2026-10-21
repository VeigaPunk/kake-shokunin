# RowS008 — freshness re-check (round 26)

```json
{"id":"S008","verdict":"HOLD","fetchIndex":1,"quote":"When wildcards match slash (the default for exclusion members), a wildcard like @samp{*} in the pattern can match a @samp{/} in the name.","anchorObserved":"Controlling Pattern-Matching (@node line 8480, @unnumberedsubsec 8481, body to 8619); anchored-patterns table 8579-8588; wildcard-slash item 8598-8604 (quote at 8602-8604); summary defaults 8613-8619 — all inside the cited 8478-8617 range","reason":"Commit-pinned texi re-fetched 2026-10-21 (attempt 2 after a 60s timeout), status 200, 512,359 bytes, sha256 93281a63cb9f94a08d4d2ed6dfe9559b02cecc72d6bbd304c9970d8f81606084: exclusion defaults are still --no-anchored (8587-8588) and wildcard slash-crossing is still 'the default for exclusion members' (8602-8604), with the summary table still listing Exclusion = --wildcards --no-anchored --wildcards-match-slash (8618). Scope and teaches therefore stand; only the anchor tail ends 2 lines before the subsection's closing multitable.","correction":null}
```

## Caveat

- URL pins commit `cfdb891bbd68c920ea75210977593f3cd08f0418`, so this recheck tests availability + anchor, not content drift; the first GET timed out at 60s and retained 0 bytes (`fetched/S008-1.raw.gz` is a 20-byte gzip of empty), and the documented retry produced the bytes above, which `population.json` records as fetch index 1.
- The text view is whitespace-collapsed texi (one physical line), so the receipt quote carries source markup (`@samp{*}`); line numbers in `anchorObserved` were computed on `fetched/S008-1-retry.raw.gz`, whose decompressed sha256 matches the manifest.
- The subsection body now runs 8481-8619 and the cited range ends at 8617, one line before the summary table's Exclusion row (8618); both teaching lines (8587-8588, 8602-8604) are inside the cited range, so this is HOLD, and widening the anchor to 8478-8619 would be a non-STALE editorial option for L1, not a correction.
- `corpus/knowledge/ghp-served-set.md:34-36` still matches today's bytes (`--no-anchored` for exclusions; wildcard `*` can match `/`); its "GNU tar 1.35" label remains withdrawn by the round-20 erratum at lines 73-79, so no new erratum is needed and I edited nothing.
- No tools installed or updated.
