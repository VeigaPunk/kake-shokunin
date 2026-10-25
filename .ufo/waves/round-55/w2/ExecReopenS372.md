# ExecReopenS372
ATTACKS: freshness of `.ufo/waves/round-55/sources/S372.html` and `corpus/knowledge/yahoo-japan-robots-txt-refusal-rules.md` at revision `a7a548e102b71bd16b0a6ddafa469393a2c98b69` (live re-fetch of `https://info-search.yahoo.co.jp/archives/002849.php`, the entry's own `recheck:` arm, and every ≥6-unit double-quoted span against today's body)

Scope: one read-only lane. Every git call was `git -C /home/vgpnk/Projects/shokunin/kake-shokunin show <rev>:<path>` (no index, no jj, no commit). Scratch lived in `mktemp -d` (`/tmp/tmp.qiLQ7UOVSd`) outside the lane. Only this report file was written inside the lane. No tool was installed or upgraded, so there is no tool/version/channel record to make.

## FETCH:

Command (one plain GET, no redirects followed in practice — `NUM_REDIRECTS=0`):

```
T=$(mktemp -d) && curl -sSL --max-time 60 -A 'kake-shokunin-round55' -D "$T/hdr.txt" -o "$T/body.html" \
  -w 'HTTPSTATUS=%{http_code}\nURL_EFFECTIVE=%{url_effective}\nSIZE_DOWNLOAD=%{size_download}\nNUM_REDIRECTS=%{num_redirects}\n' \
  'https://info-search.yahoo.co.jp/archives/002849.php'
```

Observed output:

```
HTTPSTATUS=200
URL_EFFECTIVE=https://info-search.yahoo.co.jp/archives/002849.php
SIZE_DOWNLOAD=10168
NUM_REDIRECTS=0
```

Response status line `HTTP/2 200`. Final URL equals the requested URL. Selected headers (verbatim, `set-cookie` lines deliberately omitted as session material):

```
content-type: text/html; charset=UTF-8
date: Sun, 25 Oct 2026 21:13:41 GMT
vary: Accept-Encoding
cache-control: private, no-cache, must-revalidate
pragma: no-cache
age: 0
```

`Last-Modified` and `ETag` are **absent**: `grep -ciE 'last-modified|etag' "$T/hdr.txt"` → `0` (exit 1, no match). No `Content-Length` header either; `size_download` and the on-disk size agree at 10168 bytes, i.e. identity encoding.

Byte/hash comparison (`wc -c`, `sha256sum`, `cmp`):

| source | bytes | sha256 | vs fresh |
|---|---|---|---|
| fresh GET (this seat, 2026-10-25T21:13:41Z) | 10168 | `ee8c9defeeee7abf3f2f6bd4bfb8dbb86c69cf9a272551264aa3f99f76200111` | — |
| `receipts.json` → `sources.S372` | 10168 | `ee8c9defeeee7abf3f2f6bd4bfb8dbb86c69cf9a272551264aa3f99f76200111` | equal |
| `git show a7a548e…:.ufo/waves/round-55/sources/S372.html` | 10168 | `ee8c9defeeee7abf3f2f6bd4bfb8dbb86c69cf9a272551264aa3f99f76200111` | equal |

`cmp "$T/body.html" "$T/retained.html"` → no output, exit 0, printed `CMP_IDENTICAL=yes`. Receipt `httpStatus: 200` matches the observed 200; receipt `fetchedAt: 2026-10-25T20:40:13+00:00` is 33 minutes before this fetch.

Body spot-checks on the fresh text (`grep -F -c`): section title `サイト単位、ディレクトリ単位での巡回の拒否設定` → 4 (heading plus repeated navigation), `2010年11月24日` → 1, `サイトに対する巡回の制限はないものとみなされます` → 1, `すぐに設定の内容が反映されるわけではありません` → 1, `メタタグで、` → 1. The entry's `source:` line's section/更新日 claim therefore still describes the live page.

## RECHECK COMMAND:

The entry's `recheck:` field, curl half, run exactly as written:

```
curl -fsSL 'https://info-search.yahoo.co.jp/archives/002849.php' | grep -F -c 'サイトに対する巡回の制限はないものとみなされます'
```

Observed: `1` (exit 0).

Same grep form against the retained round-55 body:

```
grep -F -c 'サイトに対する巡回の制限はないものとみなされます' /tmp/tmp.qiLQ7UOVSd/retained.html
```

Observed: `1` (exit 0).

Both counts equal the entry's recorded `-> 1 (2026-10-25: curl arm 1; same grep form on the retained round-55 body 1)`. The `recheck: 180d` cadence is an arithmetic statement about the next due date and was not evaluated here (no due date is stored to compare against) — `unrun`.

## SPAN TABLE:

Extraction: `re.finditer(r'"([^"\n]*)"', text)` over the whole entry file and over line 13 of `corpus/lessons/round-55.md` (`- S372 — …`), i.e. header lines included. No line of the entry has an odd number of `"` (checked), so no span crosses a line and none was missed by the single-line pattern. The four front-matter lines (`source:`, `verified-at:`, `recheck:`, `ground:`) contain no double quote (`grep -c '"'` over lines 1–4 → 0).

Unit definition, primary column: verbatim the frozen counter's function (`c55_quote_truth.py:104` `CJK_RE`, `:167` `units()`): one unit per CJK character in `[\u3040-\u30ff\u3400-\u4dbf\u4e00-\u9fff\uf900-\ufaff\uff65-\uff9f\U00020000-\U0002ffff]`, plus one per whitespace token containing no such character. Second column `punct` applies an alternative segmentation that also counts U+3000–303F and U+FF00–FF0F as CJK characters (i.e. `「」（）`、` as units). `in fresh` is Python `span in fresh_text` against the UTF-8-decoded fresh body.

20 spans measure ≥6 counter-units (19 in the entry, 1 in the Gate line); all 20 return `True`. Ordered by first appearance:

| # | src | units | punct | in fresh | span |
|---|---|---|---|---|---|
| 1 | entry | 18 | 21 | True | `「robots.txt」という名前でテキストファイルを用意し` |
| 2 | entry | 22 | 22 | True | `サイトのルートディレクトリに設置してください` |
| 3 | entry | 15 | 15 | True | `サイトの一番上の階層を指します` |
| 4 | entry | 24 | 24 | True | `特定のディレクトリ内のみの巡回を拒否したい場合は` |
| 5 | entry | 20 | 23 | True | `「Disallow: /」に続いてそのディレクトリ名を指定します` |
| 6 | entry | 24 | 24 | True | `サイトに対する巡回の制限はないものとみなされます` |
| 7 | entry | 22 | 23 | True | `クローラーは巡回のたびにrobots.txtの有無を確認しており` |
| 8 | entry | 15 | 16 | True | `新たにrobots.txtが設置されていた場合には` |
| 9 | entry | 21 | 21 | True | `ファイルに記載された内容に従って巡回します` |
| 10 | entry | 23 | 23 | True | `すぐに設定の内容が反映されるわけではありません` |
| 11 | entry | 22 | 29 | True | `巡回の拒否（Disallow:）、クローラーの受け入れ（Allow:）の記述の前には` |
| 12 | entry | 25 | 25 | True | `この記述がないときはすべてのクローラーに対する指示` |
| 13 | entry | 16 | 16 | True | `大文字と小文字の違いがあった場合` |
| 14 | entry | 11 | 11 | True | `別のものとして扱います` |
| 15 | entry | 15 | 21 | True | `「Allow:」は通常「Disallow:」と組み合わせて使用します` |
| 16 | entry | 17 | 20 | True | `「foo」ディレクトリ以下は巡回を拒否するが` |
| 17 | entry | 8 | 9 | True | `/foo/bar.htmlは巡回を許可する` |
| 18 | entry | 13 | 16 | True | `「robots.txt」による巡回拒否はできません` |
| 19 | entry | 21 | 21 | True | `インデックスへの登録拒否を設定してください` |
| 20 | gate | 24 | 24 | True | `サイトに対する巡回の制限はないものとみなされます` |

Excluded by the 6-unit floor: the entry's other quoted spans, including `メタタグで、` — 5 counter-units (6 under the `punct` segmentation: `メタタグで` = 5 CJK + `、`), and `別のものとして扱います`-class short pairs below the floor. The gate line's recorded `(24 units; …)` matches the measured 24, and its recorded `sha256 … 10168 bytes, HTTP 200` matches the fresh body exactly.

Observations from the table, stated as measurements only:

- Maximum under the frozen counter definition is 25 (span 12), i.e. at the `UNIT_CEILING = 25` boundary and not above it. Nothing exceeds 25 under the counter's own function.
- Span 11 measures 22 under the counter definition but 29 under the punctuation-inclusive segmentation. The frozen counter's `CJK_RE` excludes U+3000–303F, so `（` `）` `、` are not CJK characters there and the whole span is one whitespace token that contains CJK (hence counted only by its 22 CJK characters). The contract's prose says the ceiling "satisfies the CORPUS.md ≤25-word rule under any segmentation"; under the punctuation-inclusive segmentation that sentence does not hold for span 11 (29 > 25). This is a definitional risk in the contract sentence, not a counter failure: the counter passes, and this seat does not rule on which segmentation governs.

## DRIFT:

None. The live body is byte-identical to the retained body and to the receipt digest, so there is no drift to summarise:

- `sha256sum` fresh = `sha256sum` retained = `ee8c9defeeee7abf3f2f6bd4bfb8dbb86c69cf9a272551264aa3f99f76200111`.
- `cmp` fresh vs retained: identical, exit 0.
- `diff` summary: empty (no differing byte, no differing line; nothing added, nothing removed, both 10168 bytes).
- Entry state at the measured revision is the commit `2bda8e4` ("round-55: build — three Yahoo robots entries, …"); `a7a548e` changes only `PROVINCE.md`, `SKILL.md`, `corpus/QUALITY.md` (`git show --stat`), so the entry and retained body under attack are unchanged by the revision bump.

Retained evidence: this seat's fresh body, header dump, entry copy, lesson copy and gate line under `/tmp/tmp.qiLQ7UOVSd/` (`body.html`, `hdr.txt`, `retained.html`, `entry.md`, `lesson.md`, `gateline.txt`, `spans.json`) — ephemeral, outside the lane, not committed.

Risks and blockers: (1) the page carries no `Last-Modified`/`ETag`, so no server validator can ever corroborate byte identity — every future `recheck:` rests on a full-body fetch plus `grep` count, exactly as the entry writes it; (2) the span-11 segmentation question above is the only place where this entry's quoting sits at the contract's wording boundary; (3) `180d` recheck due-date arithmetic is `unrun` (no stored due date). Nothing blocked; the entry is quote-true against today's live body.

VERDICT: No drift — fresh GET is HTTP 200, 10168 bytes, sha256 `ee8c9def…00111`, byte-identical to receipt and retained body; both recheck arms return 1; all 20 ≥6-unit spans are raw substrings of the live body, with span 11 at 22 counter-units / 29 punctuation-inclusive units.
