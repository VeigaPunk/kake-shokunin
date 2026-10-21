# Round 24 — scoped glob expansion (freshness)

## Verdict

At 2026-10-21T11:49:47Z, Python glob returned no `~/.config/systemd/user/webzites-*.timer` matches and no `~/Projects/**/ufofsdbeta-kimi-review` matches within the requested depth bound (0–4 directory levels below `~/Projects`). The systemd user timer inventory also had no `webzites` row. Both patterns are recorded as unresolved globs by the round-24 paths sweep, not as members of its 19-target C1 reconciliation population. The recursive-project glob's cite line is also the cite for the distinct concrete C1 target T10.

## Findings

### P3 — `~/.config/systemd/user/webzites-*.timer`

- **Axis / claim:** freshness, C1 paths context. The round-24 sweep records this pattern as an unresolved glob, cited at `corpus/lessons/round-5.md:7`; it is not one of the 19 C1 target receipts.
- **Exact command / operation:** Python 3.14.8 `glob.glob("/home/vgpnk/.config/systemd/user/webzites-*.timer", recursive=True)`.
- **Exact observed output:** `[]` (no matches).
- **Independent read-only check:** `systemctl --user list-timers --all | grep -i webzites`; no matching output; `PIPESTATUS=0 1` (systemctl succeeded; grep found no row). Full list output was:
  ```text
  NEXT                            LEFT LAST                             PASSED UNIT                          ACTIVATES
  Wed 2026-10-21 08:53:45 -03 3min 58s Wed 2026-10-21 08:48:45 -03 1min 1s ago ai-usage.timer                ai-usage.service
  -                                  - Mon 2026-10-19 00:33:15 -03           - cursor-shim-healthcheck.timer cursor-shim-healthcheck.service

  2 timers listed.
  ```
  `systemctl --user list-unit-files 'webzites*' --no-legend` produced no output and exited 1.
- **Cited bytes:** `corpus/lessons/round-5.md:7` ends: ``docs/SPEEDRUN-PROTOCOL.md}` <!-- r18 re-census 2026-10-14: the webzites tree (state/probe-history.jsonl · reports/keepers/repos-r1..r8 · speedrun-r1 · docs/SPEEDRUN-PROTOCOL.md) absent — gone in the 2026-10-12 ~/Projects prune/migration; cite retained as historical record. --> + `~/.config/systemd/user/webzites-*.timer`.``
- **Annotation status:** lane-authored cite. The existing r18 annotation on the line addresses the listed `~/Projects/webzites` files, not the systemd timer glob; there is no timer-specific current annotation. Treat the timer glob as **unannotated for this path**. The sweep itself leaves the glob unresolved rather than evaluating that annotation.
- **Proposed annotation (not applied; append at the end of line 7):**
  ```text
   <!-- r24 recheck 2026-10-21: Python glob for ~/.config/systemd/user/webzites-*.timer returned no matches; systemctl --user list-timers --all listed no webzites timer and list-unit-files webzites* returned no units. Removal event: unknown. The matching timer files are absent at this observation; historical record, not an executable instruction. -->
  ```
- **Smallest fix:** append the dated note to line 7 if this unresolved glob is being annotated; do not alter its historical r18 note.

### P3 — `~/Projects/**/ufofsdbeta-kimi-review`

- **Axis / claim:** freshness, C1 paths context. The round-24 sweep records this pattern as an unresolved glob, cited at `corpus/knowledge/mirror-pitfalls.md:64`. Separately, C1 T10 is the concrete token `~/Projects/ufo-fsd-alpha/ufofsdbeta-kimi-review`, class `newMissing`, with the same line 64 cite.
- **Exact bounded Python glob operation:** for each `depth` in `range(5)`, call `glob.glob(os.path.join("/home/vgpnk/Projects", *(["*"] * depth), "ufofsdbeta-kimi-review"), recursive=True)`. These are finite-depth patterns for 0, 1, 2, 3, and 4 intermediate directory levels; they bound the search while using Python glob with `recursive=True`.
- **Exact observed output:** matches by depth were `{0: [], 1: [], 2: [], 3: [], 4: []}`; combined matches `[]`; elapsed `0.09s`. In particular, the T10 concrete path did not match.
- **Cited bytes:** `corpus/knowledge/mirror-pitfalls.md:64` is: ``- [mirror-pitfalls:c5] **UNVERIFIABLE** — The named tree is a non-git review snapshot, is not a source, and has remained absent from the filesystem since the r15 sweep. Surface: `test -e /home/vgpnk/Projects/ufofsdbeta-kimi-review; test -e /home/vgpnk/Projects/ufo-fsd-alpha/ufofsdbeta-kimi-review; glob /home/vgpnk/Projects/**/ufofsdbeta-kimi-review`. Unverifiable: The unit gives only a relative directory name and makes a filesystem-wide absence/non-git assertion. The checked project-root candidates were absent, but without an exact canonical absolute path or the tree itself I cannot verify the global absence or its former git status.``
- **Annotation status:** lane-authored cite. The line already carries an absence statement and explicitly limits its broader claim as **UNVERIFIABLE**. The bounded observation is consistent with absence at depths 0–4; it does not establish global absence deeper than four levels. For T10, the current C1 population records this as an annotated cite (no `unannotatedCites` entry); do not convert the bounded result into proof of the global claim.
- **Proposed annotation (optional, not applied; append at the end of line 64 to make the search bound explicit):**
  ```text
   <!-- r24 recheck 2026-10-21: Python glob for ~/Projects/**/ufofsdbeta-kimi-review, expanded with recursive=True and finite depth-0..4 patterns, returned no matches; no restoration event was observed, and matches deeper than four directory levels were not searched. The target is absent in the checked range; historical record, not an executable instruction. -->
  ```
- **Smallest fix:** no required C1 cite correction for T10 from this result; if documenting the new observation, append the bounded-scope note and retain the existing `UNVERIFIABLE` qualifier.

## Checked and held

- Read the frozen round-24 contract and C1 population. The 19-target population contains T10 as the concrete `~/Projects/ufo-fsd-alpha/ufofsdbeta-kimi-review`; both literal glob tokens are instead in `paths-before.json`'s unresolved list.
- Read current source lines `corpus/lessons/round-5.md:7` and `corpus/knowledge/mirror-pitfalls.md:64`.
- Checked the paths section reports 10 unresolved tokens overall; the two assigned globs are among them.
- No lane production files, pins, population files, or source documents were edited. Proposed annotations above are not applied. This report is scoped evidence only; it does not claim independent admission.

## Limits

- The project search was intentionally bounded to 0–4 intermediate directory levels under `/home/vgpnk/Projects`; no conclusion is made about deeper paths. Python glob's default hidden-directory behavior applies. A prior unbounded `**` expansion timed out at 240 seconds and is not used as evidence.
- `systemctl --user list-timers --all` reports the timer inventory at observation time; this does not establish why the webzites unit files are absent or whether an operator may restore them.
- Observed at 2026-10-21T11:49:47Z. No tools were installed or updated.
