# S002 freshness recheck (round 26, C1)

```json
{"id":"S002","verdict":"HOLD","fetchIndex":1,"quote":"Potentially breaking change: hidden files (specifically dotfiles) will not be included in the artifact by @tsusdere in #102","anchorObserved":"v4.0.0 release page, 'What's Changed' block (after commit 7b1f4a7); v5.0.0 release page, 'Changelog' block (after commit fc324d3)","reason":"Both halves still supported verbatim today: v4.0.0 What's Changed says hidden dotfiles are excluded by default, and v5.0.0 Changelog lists 'feat: add include-hidden-files input @jonchurch (#137)'. Pinned tags resolve (200) and rendered short SHAs 7b1f4a7 / fc324d3 match the recorded full commits 7b1f4a764d45c48632c6b24a0339c27f5614fb0b / fc324d3547104276b827a68afc52ff2a11cc49c9, so scope, anchor and teaches are unchanged.","correction":null}
```

Caveats (≤10 lines):

1. v5.0.0 half verified in fetched/text/S002-2.txt: "feat: add include-hidden-files input @jonchurch (#137)" sits under the "Changelog" heading, exactly where the anchor claims.
2. v4.0.0 `What's Changed` heading and the dotfile sentence are both present in fetched/text/S002-1.txt; no wording drift.
3. Both GETs returned 200 on 2026-10-21T15:09Z (sha256 455adcec…334f and 28d5566a…d998); manifest-retry.json has no S002 entry, so no retry was needed.
4. Only volatile page furniture differs from any prior read (issue/PR counts, reaction tallies, footer year); none is cited by the row.
5. Release stamps render without a year ("14 Aug", "10 Apr"); the row pins tags/commits rather than dates, so this does not affect the claim.
6. Citing knowledge entry corpus/knowledge/ghp-served-set.md:25-26 quotes the same v4 wording, so the row-to-entry citation remains coherent (knowledge-entry judgement is a separate seat).
7. No tool installs or upgrades were needed; nothing was written outside this report.
