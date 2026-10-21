# Pair S002 × corpus/knowledge/ghp-served-set.md — r26 freshness recheck (2026-10-21)

Evidence base: re-fetched bytes retained today under `.ufo/waves/round-26/fetched/` —
`text/S002-1.txt` (fetchIndex 1, https://github.com/actions/upload-pages-artifact/releases/tag/v4.0.0, sha256 455adcec…) and
`text/S002-2.txt` (fetchIndex 2, https://github.com/actions/upload-pages-artifact/releases/tag/v5.0.0, sha256 28d5566a…)
(`manifest.json:41-57` and `manifest.json:60-76`). Every quote below was located in those retained bytes today; nothing was judged from memory and no live site was probed.

## Statements in ghp-served-set.md attributed to S002

| # | file:line | Statement | Verdict | Verbatim quote from re-fetched text | Anchor observed now |
|---|---|---|---|---|---|
| 1 | corpus/knowledge/ghp-served-set.md:1 | `source:` metadata lists S002 (v4.0.0 + v5.0.0 release notes at both release tags) | HOLD | "Release v4.0.0 · actions/upload-pages-artifact" | Page title of S002-1.txt (S002-2.txt title: "Release v5.0.0 · actions/upload-pages-artifact") |
| 2 | corpus/knowledge/ghp-served-set.md:2 | `verified-at: 2026-10-19 (v4.0.0 commit 7b1f4a7…)` — v4.0.0 tag identity | HOLD | "v4.0.0 7b1f4a7 This commit was created on GitHub.com and signed" | S002-1.txt release header, immediately before "What's Changed" |
| 3 | corpus/knowledge/ghp-served-set.md:8-9 | Claim: "v4.0.0 excludes dot paths by default" | HOLD | "Potentially breaking change: hidden files (specifically dotfiles) will not be included in the artifact" | S002-1.txt, "What's Changed" section, entry by @tsusdere in #102; the same page still offers only the workaround "instead of using this action, create your own artifact", i.e. no input in v4.0.0 |
| 4 | corpus/knowledge/ghp-served-set.md:10,27 | "v5.0.0 release notes announce the input" (supporting the pinned action's `include-hidden-files` default-false account, which stays S001-anchored) | HOLD | "feat: add include-hidden-files input @jonchurch (#137)" | S002-2.txt, "Changelog" section, directly after "Update upload-artifact action to version 7 @Tom-van-Woudenberg (#139)" |
| 5 | corpus/knowledge/ghp-served-set.md:25-26 | S002 source-check quote reopened 2026-10-19: “Potentially breaking change: hidden files (specifically dotfiles) will not be included in the artifact” | HOLD | "Potentially breaking change: hidden files (specifically dotfiles) will not be included in the artifact" | S002-1.txt, "What's Changed" — character-for-character match with the entry's quotation |

## Version/date/anchor supersession scan

- v5.0.0 tag identity: S002-2.txt header shows "v5.0.0 fc324d3 … signed" — matches the SOURCES S002 anchor `fc324d3547104276b827a68afc52ff2a11cc49c9`. Not superseded.
- Neither re-fetched page shows a release newer than v5.0.0; v4.0.0 header shows "11 commits to main since this release", v5.0.0 shows "4 commits to main since this release" — no evidence in retained bytes that the entry's v4/v5 account is incomplete. The entry's recheck trigger ("on action release or workflow change") remains the correct tripwire; today's bytes do not trip it.
- r20-correction tail (ghp-served-set.md:14-19): not S002-attributed; its factual basis (v4.0.0 dotfile exclusion) is exactly what statement 3 re-confirms, so it holds transitively. No edit.
- Rechecks block (ghp-served-set.md:38-41): S001-anchored curl loop (`v3.0.1 0`, `v4.0.0 3`, `main 3`); the recorded `v4.0.0 3` is consistent with the re-fetched v4.0.0 release notes. Consistent, no S002-attributed defect.

## Verdict

5 statements attributed to S002, all HOLD; no content change, no anchor move, no superseded version/date. No correction text required (append-only corrections list is empty).

```json
{"pair":"S002xghp-served-set","statements":5,"hold":5,"stale":0,"corrections":[]}
```
