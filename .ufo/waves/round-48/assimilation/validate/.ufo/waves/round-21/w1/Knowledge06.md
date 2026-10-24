# Knowledge06 — provenance trio for freshness-sweep.md

Target: `corpus/knowledge/freshness-sweep.md` (only file changed; no commits).

## Gate result

- The entry did not open with a provenance trio (line 1 was `# Freshness sweep — the standing-claim drift instrument`), so the trio was prepended.
- Pre-edit tag: `C7BA`. Post-edit tag: `05D7`.
- The entry's body was not edited. All pre-existing lines, corrections (r20 correction note, r20 resume note, r17/r16 run blocks) and absence flags (`~/Projects/plazir-15-site` absent, `~/Projects/webzites/state` absent, `<!-- r18 re-census … -->` comments) are byte-identical.

## Exact change

Prefix: 4 lines (3 metadata lines plus one blank line), **809 bytes** total (`wc -c` new 13521 − HEAD 12712 = 809). Line 5 is the original line 1, `# Freshness sweep — …`.

Byte-identity check: the last 12712 bytes of the working file were compared with `git show HEAD:corpus/knowledge/freshness-sweep.md` via `cmp` and matched. `git status` shows only ` M` on this file.

Prefix text:

```
source: S014 (corpus/SOURCES.md, own-work) — scripts/freshness-sweep.mjs (`scanCitations`, `printPaths`, selftest case M); corpus/knowledge/freshness-pins.json; .ufo/round-20/{baseline-proof,candidate-proof}.json; .ufo/round-20/frozen/citation-locality/expected.json. Metadata contract: S019 (pending L1 CORPUS.md registration; field authority only, not platform authority)
verified-at: 2026-10-19 (round-20 citation-local correction and S014 run; r16 run 2026-09-29T02:4xZ and r17 run 2026-09-29T03:2xZ records) — historical, not live-reverified
recheck: on script, pins, or round-20 evidence change — `grep -cF 'function scanCitations' scripts/freshness-sweep.mjs` (expect 1); if the script is absent, operator must restore it from git (last touched in 02b6dd0) or retire this entry and the S014 row

```

## Evidence basis

- **source**: The entry's own body names `scripts/freshness-sweep.mjs` (`scanCitations`, `printPaths`, selftest case M), `freshness-pins.json`, and the round-20 measured evidence (`.ufo/round-20/{baseline-proof,candidate-proof}.json`, `.ufo/round-20/frozen/citation-locality/expected.json`). The body also cites the S014 row. `corpus/SOURCES.md` S014 is `own-work`, tier A, lane citation resolution only, and lists `corpus/knowledge/freshness-sweep.md` as a consumer. Verified present: `scripts/freshness-sweep.mjs` (92277 bytes), `freshness-pins.json`, both round-20 proof files, and the citation-locality frozen directory. `scanCitations` (line 346) and `printPaths` (line 893) exist in the script.
- **S019**: referenced as the metadata contract only, per assignment. `S019` is not yet registered in `corpus/SOURCES.md` or any `CORPUS.md` (no `CORPUS.md` exists in the repo; L1 will register it). It is not cited as platform evidence.
- **verified-at**: The dated evidence is the round-20 citation-local correction and the S014 run (2026-10-19), plus the historical r16 (2026-09-29T02:4xZ) and r17 (2026-09-29T03:2xZ) run records in the body. It is labeled historical and not live-reverified. No 2026-10-20 domain recheck is claimed.
- **recheck**: Chosen command is a read-only `grep -cF` against the script in the repo root. It was not executed. I did check that `function scanCitations` exists in the script, and that the string `citation-local` does not (so it was not used as the recheck token). The restore-or-retire clause covers the case where the script vanishes; the last commit touching the script is `02b6dd0`.

## Not done / limits

- No command referencing credential or auth files was run. No recheck was run. No network access.
- Field-count coverage is L1's job; not measured here.
- The entry's body keeps its historical r16/r17 numbers (e.g., `missSet 9`, `missSet still 55`, `pathsMissSet` 10 entries). These are pre-existing prose and were not reconciled, per assignment ("preserve existing corrections").
- Verification: one byte-count and one `cmp` tail check were run to measure the prefix and prove the body is unchanged. No build, lint or test.

## Tools

No tools installed or updated.

## Files touched

- `corpus/knowledge/freshness-sweep.md` (prefix +809 bytes, 4 lines).
- `.ufo/waves/round-21/w1/Knowledge06.md` (this report).
