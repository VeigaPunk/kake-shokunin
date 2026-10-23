# ScoutYandexSitemaps — Yandex Webmaster sitemap help

Axes: operability (official help bytes fetched and hashed) and freshness (Diplodoc revision `r21762422`, opened 2026-10-23). No tool installed. SOURCES.md not edited (leaf write bound). Highest registry id at read: S104 (`grep` `^\| S` on `corpus/SOURCES.md`).

## Fetch

`timeout 40 curl -sS -D HDR -o BIN -w '%{http_code}' -L --max-redirs 5 --compressed` for eight URLs. Script finished under `set -euo pipefail` (exit 0). No `content-encoding`; `content-length` equals each file size, so the sha256 is the response body. All HTTP 200.

| file | URL | Date | bytes | sha256 |
|---|---|---|---|---|
| en-ctrl-md.bin | https://yandex.com/support/webmaster/en/controlling-robot/sitemap.md | 2026-10-23T06:53:40Z | 12683 | `baf12693af0a7acb77841326e1d116731567ad2f2ce51fdb775b934755ef807e` |
| en-ctrl.bin | https://yandex.com/support/webmaster/en/controlling-robot/sitemap | 2026-10-23T06:53:38Z | 223732 | `4d746e4176f7890eaccd44f7420a56ddb06667097c10e30963ab3a76ffb2f1a3` |
| en-err.bin | https://yandex.com/support/webmaster/en/error-dictionary/sitemap.md | 2026-10-23T06:53:48Z | 7106 | `7364048cc437b5f218e9f58971e2a659889c44fae0a53ac9f79b014c446b4fc9` |
| ru-ctrl-md.bin | https://yandex.ru/support/webmaster/ru/controlling-robot/sitemap.md | 2026-10-23T06:53:42Z | 18222 | `341bbcca294d0680409d80c2ab98ce862456b23191d5dbfc161360e8634f76e0` |
| ru-err.bin | https://yandex.ru/support/webmaster/ru/error-dictionary/sitemap.md | 2026-10-23T06:53:49Z | 10463 | `df590984698da22048bb7dc74bf7adb6d21e68c56d30d37f6589a977fc323deb` |

Kept under `/fast/scratch/hyaku/kake-r39a3w1/ScoutYandexSitemaps/`. Markdown `link: rel=canonical` points at the HTML page; HTML `link` names the `.md` alternate and `llms.txt?revision=r21762422`. Russian lines match the English claims below (ru-ctrl-md.bin:139–143,239; ru-err.bin:113,138). `indexing-options/sitemap.md` is the upload UI and points at the controlling-robot page; not a second rule source.

## Draft row (not inserted)

| id | source | kind | tier | scope | anchor | teaches | status | opened | recheck | used-by |
|---|---|---|---|---|---|---|---|---|---|---|
| draft-after-S104 | Yandex Webmaster: Using the Sitemap file — https://yandex.com/support/webmaster/en/controlling-robot/sitemap | docs | A | Yandex's own sitemap size, count, encoding, domain scope and per-tag caps; not the lane contract and not the error dictionary | File requirements and the URL-length question; markdown lines 139–143 and 256; Diplodoc r21762422; fetched 2026-10-23T06:53:40Z HTTP 200 | Yandex caps one file at 50,000 links and 50 MB uncompressed, requires UTF-8, and splits a URL into 2048 characters as 1024 for the domain plus 1024 for the path | queued | 2026-10-23 | 90d | — |

Gate quote (15 words), `en-ctrl-md.bin:256` (same sentence `en-ctrl.bin:276`; apostrophe is U+2019): "The total character limit is 2048. 1024 Characters are intended for the site’s domain name". Contradicts sentence 23.

Second opened page, same shape, not a second id: Sitemap errors reference — https://yandex.com/support/webmaster/en/error-dictionary/sitemap.md — docs, A, Yandex's processing errors. Quote (13 words), `en-err.bin:137`: "The Sitemap file doesn't start with the correct UTF-8 prefix (0xEF 0xBB 0xBF)." Contradicts sentences 6–7.

## Against (a)–(k)

- (a) 6–7. `en-ctrl-md.bin:139` "Use UTF-8 encoding" grounds 6 only. `en-err.bin:137` also requires the exact declaration `<?xml version="1.0" encoding="UTF-8"?>`, so a missing declaration, a lowercase `utf-8`, or a file with no BOM fails Yandex's error text and passes 6–7. `en-err.bin:191` calls a missing BOM a warning, so the same page disagrees with itself.
- (f) 19–20. `en-ctrl-md.bin:140–141` and `en-err.bin:37,152`: 50,000 links and "50 MB" uncompressed. Grounds 20. Never states 52,428,800, so 19's byte threshold is neither confirmed nor contradicted. `en-err.bin:157`: an index holds at most 50,000 sitemap URLs (same count as 20, said of the index).
- (g) 23. Requirements `:256` is a 2048 total split 1024/1024, so a loc under 2048 code points can still fail the path half, and the text does not say 2048 itself is too long. `en-err.bin:112` "URL length exceeds the limit (1024 characters)." contradicts both 23 and the FAQ.
- (h) 24–27. `en-ctrl-md.bin:142–143` same domain only: looser than 25–26 (no path prefix) and silent on port (24). `en-err.bin:107` "same directory or its subdirectories" grounds 25. `en-err.bin:221` index children "on the same site" grounds 27 without default ports. `en-ctrl-md.bin:225` Webmaster identity also requires the same protocol and www prefix.
- (i) 28–30. Example `en-ctrl-md.bin:102` `2005-01-01` grounds the complete-date form. `en-err.bin:251` cites all of W3C NOTE-datetime, which includes the year and year-month levels sentence 30 rejects; Yandex does not state that rejection. `en-ctrl-md.bin:69` lastmod "maximum size is 100 bytes" (also changefreq `:79` and priority `:90`): a long fractional lastmod can pass 28 and fail Yandex.
- (j) 31. No list of the seven `changefreq` tokens, so case-sensitive equality is not grounded.
- (k) 32. `en-ctrl-md.bin:87` "coefficient from 0.0 to 1.0" and `en-err.bin:226` ground the range only, not the `xsd:decimal` lexical form.
- (b)(c)(d)(e). `en-err.bin:143` names well-formed XML (grounds 8) and does not mention a doctype (9 uncovered). Root-tag and namespace errors are not specified beyond the example xmlns at `en-ctrl-md.bin:99`. Unknown tags are ignored (`en-ctrl-md.bin:183`), looser than sentence 17. No child-order rule (agrees with 18 by silence).

Out of (a)–(k): TXT sitemaps are supported (`en-ctrl-md.bin:111–120`); RSS and Atom are not (`:132`). Contract line 99 already excludes both from the tool.
