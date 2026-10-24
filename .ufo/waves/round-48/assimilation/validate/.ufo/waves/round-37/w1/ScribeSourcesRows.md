# ScribeSourcesRows — Round 37 wave 1

- Axes: freshness improved by re-opening the retained sources; operability unchanged. No code or live-site operation was performed.
- Drafted three registry rows (S095–S097) in the exact 11-column shape and four round-36-style Gate lines, including the S011 re-open note.
- S095 proposed admit/A/docs/mined; official Google crawler-specific guidance, with the requested URL redirect recorded. S096 proposed admit/A/code/mined, narrowly scoped to the repository's own parser/matcher description. S097 rejected/C/community with a contract-form `flip:` condition.
- The S095/S096 `mined` status and `used-by` path are conditional on `corpus/lessons/round-37.md` actually citing those rows. If it does not, CORPUS.md requires `queued` until cited.
- S011 was re-opened and supports the existing host-root/unreachable-file teaching; no edit to the old S011 row is proposed (its `opened` date remains 2026-10-19).

## Evidence and provenance

- Receipt source: `/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-37/sources/receipts.json:2-12` (S011), `:14-24` (S095), `:26-36` (S096), `:38-48` (S097). HTTP 200 for all four; access times 02:50:49Z, 02:50:49Z, 02:50:50Z, 02:50:51Z respectively.
- Retained text SHA256: S011 `8e632e483ba4c6c9808a1436d3912079b1856e77d52ba2ca7245dc8d39259cf3`; S095 `a90948534ca17e54196115163fb9a5f6afbb0b347f97a44b01a3a1d636ddbbc6`; S096 `d17aa81d51ba5fa3e030f24697a95bc50b864545bd90ba9db5228008a8615574`; S097 `a42aee4e61c02b2c100f15ec35298e3ed14b7fc152e0bb2160f67676adbe3801`.
- Exact-phrase `functions.grep` searches all matched in retained `S011.txt:1`, `S095.txt:1`, `S096.txt:1`, and `S097.txt:1`. Search literals: `the crawler MUST assume complete disallow`; `The order of the groups within the robots.txt file is irrelevant\.`; `production code used by Googlebot`; `It is not an official standard backed by a standards body`. The draft includes corresponding paste-ready `grep -F` commands; those shell commands were not run (the specialized search tool returned the matches and does not expose process exit codes).
- S097 qualification: the retained text calls itself unofficial and recommends case-insensitive substring matching, but does not state a first-match selection rule. The draft does not repeat that unsupported characterization.

## Commands, outcomes, and surfaces

- `timeout 10s mkdir -p /fast/scratch/hyaku/kake-r37w1/ScribeSourcesRows` — completed with no output (exit 0).
- `timeout 10s sha256sum /fast/scratch/hyaku/kake-r37w1/ScribeSourcesRows/sources-rows.md` — `0a2cc9eb372abee618f2437ba978b7c81ea2eca3b177fe98171c6b2a386ddacd` (exit 0).
- No network fetch, Git command, test/build/lint, C1 counter, or C2 counter was run. No tool was installed.
- Only lane write is this required report. The source registry and lesson were not edited.

## Deliverables and limits

- Draft: `/fast/scratch/hyaku/kake-r37w1/ScribeSourcesRows/sources-rows.md` — SHA256 above.
- Report: `/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-37/w1/ScribeSourcesRows.md`.
- S096 evidence is the retained GitHub repository page/README text, not a separately opened or commit-pinned source file; the row's scope avoids claims about uninspected algorithm details.
- No path under the sealed `/fast/scratch/hyaku/kake-r37/` tree was accessed. No source rows were copied into the lane registry; L1 integration remains outside this seat's write scope.
