# ExecReopenS367

Freshness re-opening of held row S367 (`https://info-search.yahoo.co.jp/archives/002852.php`, retained as
`.ufo/waves/round-56/sources/S367.html`). One GET, no retries, no lane mutation; read-only `git show`/`rev-parse` only.
Readings below hold identically at the revision under attack `a450e43e696d032e3ac308383f6b3394e0c92860`, at the lane tip
observed at read time `7ad7db51dfcff2eccea9f7f73726f2437b2ed8de`, and in the worktree (same sha256 for all three artifacts
checked, below).

## FETCH:

Command (once):

```
curl -sS -L -A kake-shokunin-round56-w2 -o /tmp/tmp.l1A7eYTpql/S367.html \
  -w '%{http_code}' https://info-search.yahoo.co.jp/archives/002852.php
```

- HTTP code printed: **200**
- Bytes on wire: **8051**
- sha256 (live): `0188de9dae01e9088231098a9c6af3c8f5dc62a5982419a5f82fd98e86772a19`
- sha256 (retained `sources/S367.html`): `0188de9dae01e9088231098a9c6af3c8f5dc62a5982419a5f82fd98e86772a19`
- `cmp` live vs retained: **identical**; `diff -q`: no differences (byte-identical, not merely same size)
- Fetch time 2026-10-25T22:53:37Z (file mtime); the retained receipt records the same body fetched
  2026-10-25T22:02:40+00:00, so the two GETs are 50m57s apart on the same round date.

Against `sources/receipts.json` (`S367` entry): `httpStatus` 200 = observed 200; `bytes` 8051 = observed 8051;
`sha256` `0188de9d…a19` = observed `0188de9d…a19`. Only the `userAgent` differs by construction — the receipt was taken
with `kake-shokunin-round56`, this GET used the seat UA `kake-shokunin-round56-w2` — and the body is unchanged under that
difference, so this page is not UA-varied across those two UAs (observed, two samples only).

## RECHECK RUN:

The `recheck:` line of `corpus/knowledge/yahoo-japan-link-target-crawl-restriction.md` was run exactly as written (its
curl arm verbatim, then its grep arm against the retained round-56 body):

```
curl -fsSL 'https://info-search.yahoo.co.jp/archives/002852.php' | grep -F -c 'サーバーの設定で指定する方法があります'
grep -F -c 'サーバーの設定で指定する方法があります' .ufo/waves/round-56/sources/S367.html
```

- curl arm printed: **1** (exit 0) — the entry's stated `-> 1` holds
- grep arm against retained body printed: **1** (exit 0) — the entry's parenthetical "(curl arm 1 and the same grep
  against the retained round-56 body 1, 2026-10-25)" holds
- Same needle in the live fetch body: 1 hit (the opening article paragraph, `div.asset-body`), i.e. the needle has not
  moved between the receipt fetch and this one.

The needle is a raw substring of the article block (opening paragraph, before the h3 `メタタグを使用する方法`), so the
recheck arms agree with each other and with the live page.

## GATE QUOTE:

Gate quote of `corpus/lessons/round-56.md` line 16 for S367: `インデックスへの登録を許可する`.

- Occurrences in the live body: **1** (line 110 of the fetched file)
- Heading/section: h2 `リンク先のウェブページの巡回制限　― ウェブページ内やサーバーでの設定`, h3
  `メタタグを使用する方法`, in the `<p class="note">` gloss that begins `上記の例は、` inside `div.asset-body`; 更新日
  2010年11月24日. The lessons line's section label (`§ … → メタタグを使用する方法 (更新日 2010年11月24日)`) names this
  heading pair.
- `span_tools.py check S367 'インデックスへの登録を許可する'` ->
  `{'units': 15, 'raw_substring': True, 'in_content': True, 'count_in_page': 1, 'in_other_adopted_body': False}` — 15 units
  matches the lessons line's "(15 units)" claim, and the quote is unique in S367 and absent from the other two adopted
  bodies (S419, S420); across all six retained bodies only `S367.html` holds it (1 hit; 0 in S387/S388/S389/S419/S420).

## DRIFT:

No drift. The live body is byte-identical to the retained body and to its receipt, so there is no differing region to
name; the HTTP status, byte count and sha256 all reconfirm, the page's printed 更新日 is still 2010年11月24日, and both
recheck arms still print the entry's stated count. Committed artifacts compared (read-only `git show | sha256sum`):

| path | sha256 (a450e43e / tip / worktree) |
|---|---|
| `.ufo/waves/round-56/sources/S367.html` | `0188de9d…a19` (all three) |
| `.ufo/waves/round-56/sources/receipts.json` | `13ca3d73…8c` (all three) |
| `corpus/knowledge/yahoo-japan-link-target-crawl-restriction.md` | `85f234bf…2d3` (all three) |
| `corpus/lessons/round-56.md` | `8ab11250…4f02` (a450e43e and worktree) |

What this does not establish: one GET at one instant cannot exclude a later edit or a variant served to other UAs,
geographies or headers; the recheck needle is a presence check, not a support check; and no crawler behaviour was
observed (nothing was served to a crawler for this lane).

VERDICT: S367 fresh — live GET 200/8051 bytes/sha256 0188de9d…a19 byte-identical to the retained body and receipt, recheck arms print 1 and 1 as claimed, Gate quote 15 units found once under `メタタグを使用する方法`, no drift.
