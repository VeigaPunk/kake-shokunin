# ExecReopenS419

Seat: ExecReopenS419 (W2 falsify, freshness re-open of row S419). Round 56, round date 2026-10-25. Targets attacked:
`corpus/knowledge/yahoo-japan-deleted-url-recrawl.md` (its `recheck:` line and quote claims), the S419 Gate row of
`corpus/lessons/round-56.md`, and the retained body `.ufo/waves/round-56/sources/S419.html` + `receipts.json`.
No file outside this report was written; no git/jj mutation, no lane checkout touched, no subagent dispatched (no labrat
needed). No tool installed or upgraded.

FETCH:

- Command run once: `curl -sS -L -A kake-shokunin-round56-w2 -o /tmp/tmp.efgbTJ2fjm/S419.live.html -w '%{http_code}' https://info-search.yahoo.co.jp/archives/002856.php`
  → HTTP `200`; 7428 bytes; sha256 `6172d5d108d0c31d25244659516fc7fc81472c924ef35a51afc964cdd3a4a5c8`.
- Retained body `.ufo/waves/round-56/sources/S419.html`: 7428 bytes; sha256
  `6172d5d108d0c31d25244659516fc7fc81472c924ef35a51afc964cdd3a4a5c8`; `cmp -s` against the live fetch → `IDENTICAL`
  (zero differing bytes, no differing region).
- `receipts.json` `sources.S419`: url `…/archives/002856.php`, httpStatus 200, bytes 7428, sha256 `6172d5d1…a4a5c8`,
  fetchedAt `2026-10-25T22:02:41+00:00`, userAgent `kake-shokunin-round56`. Live fetch agrees on all four content fields
  (status, bytes, sha256, url). The user-agent differs by design (this seat fetched as `kake-shokunin-round56-w2`); the
  body is unaffected.

RECHECK RUN:

- `recheck:` command of `corpus/knowledge/yahoo-japan-deleted-url-recrawl.md` run exactly, both arms, 2026-10-25:
  - curl arm: `curl -fsSL 'https://info-search.yahoo.co.jp/archives/002856.php' | grep -F -c 'クローラーは削除されたウェブページと認識できず、'`
    → printed `1`, exit 0. (`-f` makes curl fail on non-2xx, so the response was 2xx; the status code itself is not
    printed by this arm and was not separately captured.)
  - grep arm against the retained body: `grep -F -c 'クローラーは削除されたウェブページと認識できず、' .ufo/waves/round-56/sources/S419.html`
    → printed `1`, exit 0.
- Both printed counts equal the values the doc's `recheck:` line records (`curl arm 1 and the same grep against the
  retained round-56 body 1, 2026-10-25`). The documented 180d recheck value is therefore not stale at this round date.
- This arm is the only extra network GET beyond the single fetch above; it was piped to grep and not stored.

GATE QUOTE:

- Quote under test: `クローラーは削除されたウェブページと認識できず、` (Gate row for S419 in `corpus/lessons/round-56.md`).
- Count in live body: **1** (line 104 of the live fetch, inside `<p>` under `<div class="asset-body">`, the first
  sentence pair of the section).
- Heading: `<h2>削除したウェブページが巡回され続ける</h2>` at line 100, followed at line 101 by
  `<p class="update">更新日 2010年11月24日</p>`. This matches the Gate row's locator
  `§ 削除したウェブページが巡回され続ける (更新日 2010年11月24日)`.
- The heading string itself occurs 3 times in the body (document `<title>` line 33, sidebar `<li><strong>` list item
  line 277, and the single `<h2>` line 100); only one is a heading element, so the locator is unambiguous.
- `span_tools.py check S419 '<quote>'` → `units 23, raw_substring True, in_content True, count_in_page 1,
  in_other_adopted_body False`. Matches the Gate row's "23 units" and its uniqueness claim within S419 (the quote is not
  on the sibling retained bodies S367/S420).

DRIFT:

- None. The live body is byte-identical to the retained body (same 7428 bytes, same sha256, `cmp` identical), so no
  region differs and there is nothing to name as a changed region.
- Page-printed revision date unchanged: `更新日 2010年11月24日` occurs once, at line 101, still 2010-11-24.
- The Gate quote remains a raw substring, still once-only, still 23 units; the `recheck:` grep string still prints 1
  against both live and retained bodies. The entry's quote classes and its 7428-byte / `6172d5d1…` figures stand.
- Bounds respected: only this report written; the lane Git index, lane jj state and all other lane files untouched.

VERDICT: S419 body unchanged (HTTP 200, 7428 bytes, sha256 6172d5d1… identical to retained and to receipts.json); recheck prints 1 and 1; Gate quote found once under h2 削除したウェブページが巡回され続ける — no drift.
