# ReviewSourcesRule2 — S117–S119 repair vs CORPUS.md §SOURCES.md rule 2

HOLDS — the repair (commit `b061585`, parent `721310b`, the only `corpus/SOURCES.md` change since base
`1ef7a0e9`) conforms to rule 2. One minor defect on a new row (S125 `teaches` lacks the `flip:` clause)
and one overstated lesson line. No rule-2 breach found in the landed state.

## Axes
operability (does the registry + census still work) · freshness (is the repair honest against the frozen contract, today).

## Commands (all read-only; exit codes exact)
- `git diff 1ef7a0e9 721310b19 -- corpus/SOURCES.md` → exit 0, EMPTY (tip had no SOURCES change; the repair is the later commit `b061585`).
- `git show 1ef7a0e9:corpus/SOURCES.md` vs working copy → whole-file diff is exactly hunk `125,127c125,133` (14 lines): S117–S119 rewritten in place + S120–S125 appended. No other row touched anywhere.
- Field compare of S117–S119 across `9e3c31d2` / `1ef7a0e9` / working (11 cells each, `|`-split) — script `/fast/scratch/hyaku/kake-r42w2/ReviewSourcesRule2/` (no file installed into the repo).
- `timeout 600 /home/vgpnk/Projects/shokunin/scripts/sources-census.sh validate --root /home/vgpnk/Projects/shokunin kake` → exit 0; 11 lines `kake W04 <id> duplicate url … across scopes` (S033 S088 S092 S098 S099 S102 S110 S111 S115 S116 S117) + final `kake ok`; no E-findings. W04 is a warning ("warnings do not affect clean lanes").
- `sha256sum -c SHA256SUMS` in `.ufo/waves/round-42/sources/` → 6/6 OK (retained bytes back every Gate sha256; I made no network requests).
- `sed -n '2786,2791p'` on retained `www.rfc-editor.org_rfc_rfc3986.txt`: "Appendix A. Collected ABNF for URI" at line 2695, Appendix B at 2790 → the corrected anchor "lines 2695–2788" is exact; the restored committed anchor "2690–2760" is wrong on both ends.

## Rule 2 (identical in canonical `/home/vgpnk/Projects/kimi-shokunin/skills/shokunin/protocol/CORPUS.md` and fleet `/home/vgpnk/Projects/shokunin/CORPUS.md`; section diff shows no rule-2 divergence)
"Only `status`, `recheck` and `used-by` change in place, and each change is logged old→new in the round
lesson. A correction is a new row whose `teaches` opens `supersedes S0NN —`."

## Per-row verdict
- S117 **holds** — `anchor`+`teaches` restored, field-equal to `9e3c31d2` (working DIFFers from `1ef7a0e9` only in those two cells); all other immutable cells equal in all three revisions. `used-by` equals `1ef7a0e9` (mutable cell; old→new logged at `corpus/lessons/round-41.md:149`).
- S118 **holds** — `teaches` restored to `9e3c31d2`; `used-by` stays the round-41 logged value.
- S119 **holds** — same as S118.
- S120 **holds** — `teaches` opens exactly `supersedes S117 —`; carries the corrected anchor (2695–2788, byte-verified) and the corrected `urlsplit` caveat. Same URL+scope as S117; census E04 exempts supersedes rows, so no E04.
- S121 **holds** — `supersedes S118 —` prefix exact.
- S122 **holds** — `supersedes S119 —` prefix exact.
- S123 **holds** — new admitted row, `opened 2026-10-23`, Gate entry `corpus/lessons/round-42.md:19` with URL/accessed/quote/decision.
- S124 **holds** — new admitted row, Gate entry `round-42.md:20`.
- S125 **wrong on one cell** — `teaches` reads `REJECTED: …` with NO `flip:` clause; contract requires `REJECTED: <reason>; flip: <what would change the verdict>` (every prior reject, e.g. S017/S018, carries `flip:`). Append-only itself is respected (row is new, status `rejected`).

## Findings
1. [minor] `corpus/SOURCES.md:133` (S125 row, `teaches` cell): missing `flip:`. Not caught by the census: W02 fires only when `length(teaches)<8` (`/home/vgpnk/Projects/shokunin/scripts/sources-census.sh:671-672`), so a thin-but-nonempty reject reason passes. Fixes: add a flip clause via a superseding row (or, since this row is this round's own addition and unmined, correct it and log old→new in the lesson per the round's own convention — the lane should pick one; rule 2's letter says new row).
2. [wording] `corpus/lessons/round-42.md:29` "`used-by` of S117–S119 stays `SCORECARD.md, corpus/lessons/round-41.md`" is overstated: only S117 matches; S118 is `.ufo/waves/round-41/c1_count.py, SCORECARD.md`, S119 is `.ufo/waves/round-41/oracle_crosscheck.py, SCORECARD.md`. The substantive claim (unchanged by the repair; change logged in round 41) is true.
3. [confirmed violation being repaired] Round 41 did edit immutable cells in place: `2653b629` rewrote S118+S119 rows, `0c5ad2f6` rewrote S117+S118+S119 rows (checked `git diff <rev>^ <rev> -- corpus/SOURCES.md`: only in-place `-/+` row pairs, no appends). Logging them (`round-41.md:142-149`) did not legitimize them under rule 2; revert+supersede is the conforming remedy.
4. [holds] Lesson Mistakes #3 claim "restored cells equal `git show 9e3c31d2:corpus/SOURCES.md` field for field except `used-by`" — verified true.
5. [holds] "S120–S125 added (5 admitted, 1 rejected). No other `status`, `recheck` or `used-by` change" — verified by the whole-file diff (single hunk).

## Residual risk / verification gaps
- I re-opened retained bytes, not the live URLs (network bound; GET-only list does not name these URLs). Gate receipts rest on the lane's retained bytes + `SHA256SUMS`, which all verify.
- Anchor line 867 (`URI = scheme …`) and the ≤25-word Gate quotes were not re-measured word-by-word; the 2695–2788 range was.
- `used-by` naming `SCORECARD.md` and `.ufo/waves/…` paths still departs from "knowledge entries or lessons" (pre-existing round-41 values, same class the round-37 notes already flagged); out of this item's diff, left as-is.
- No automated gate exists for rule 2 (the lesson says so at `round-42.md:78-79`); my S125 finding shows the census is also blind to missing `flip:` — same gap family, still open.

No tools installed (none needed). Sandbox: `/fast/scratch/hyaku/kake-r42w2/ReviewSourcesRule2/` (base snapshot + 14-line diff); no repo file other than this report was written.
