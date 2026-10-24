# ReopenS109 — SOURCES S109 vs Yandex sitemap help

Axis: operability. No tools installed. Leaf only; no lane mutation except this report.

## Checked

Row `corpus/SOURCES.md:117`. Retained `/.ufo/waves/round-39/sources/yandex-sitemap.html` and `SHA256SUMS:11`. Contract sentences 23, 25, 26 in `.ufo/waves/round-39/c1-contract.md:63-71`. One GET of the row URL.

Commands (exit 0): `sha256sum` + `wc -c` on the retained file; `curl -fsSL -D headers.txt -o live.html --max-time 60` of `https://yandex.com/support/webmaster/en/controlling-robot/sitemap`. Visible-text diff of retained vs live: 0 lines (tags stripped, entities unescaped).

| artifact | bytes | sha256 |
|---|---|---|
| retained `yandex-sitemap.html` | 223732 | `ca117c521e7161b67724bb27c4f712db526d0ab62b2cdc9815067e3d44dea24d` |
| live body (Date `Fri, 23 Oct 2026 07:46:39 GMT`, HTTP/2 200) | 223735 | `f8c3771652d63889a60d0989a03b0eed2521bbe61855728b1f62ce104bf2cc32` |

Retained hash matches the row and `SHA256SUMS:11`. Live bytes differ only in generated ids/nonce (CSP nonce, popup ids, `inline-code-id-*`); visible sentences match. Row note "page bytes vary per fetch" holds. Clock `2026-10-23T06:56:41Z` is the row's stamp; this GET did not re-observe it.

## Per cell

**scope — holds.** Page is Yandex Webmaster help (`:1` title "Using the Sitemap file | Webmaster"), not the protocol and not another engine. Limits: `:221` "The maximum number of links is 50,000."; `:222` "The maximum size of the uncompressed file is 50 MB."; `:276` total 2048. Encoding: `:220` "Use UTF-8 encoding." Location: `:223` "Specify only page links of the domain where the file will be located."; `:224` place the file on that domain. Field caps: `:52`, `:65`, `:79` "The maximum size is 100 bytes." under `lastmod` (`:45`), `changefreq` (`:57`), `priority` (`:71`).

**anchor — overstated.** The sentence is at `yandex-sitemap.html:276` (once in the body; repeated inside `__DATA__`). Quoted span matches except the apostrophe: row `corpus/SOURCES.md:117` has U+0027 APOSTROPHE in "site's"; the page has U+2019 RIGHT SINGLE QUOTATION MARK ("site’s"). Not verbatim. Rest of the quote is exact, including "1024 Characters". Size, sha, HTTP 200, and vary-per-fetch hold as above.

**teaches — holds.** `:276`: "The total character limit is 2048. 1024 Characters are intended for the site’s domain name, for example, https://site.com. The remaining 1024 characters are intended for the path…" The page says "per URL", not the token `loc`; the file's own example puts that URL in `<loc>` (`:91`), so naming it a `loc` cap is the page's URL rule, not an extra cap. "Same-domain URLs only" is `:223` (glossary `:326` allows subdomains inside "internal" links; it does not widen `:223` past "domain"). Sentence 23 (`c1-contract.md:63-65`) is one code-point cap at 2,048 or more — different from the 1,024/1,024 split, not strictly tighter (a path over 1,024 with total under 2,048 fails Yandex and passes 23). Sentence 25 (`:67-70`) adds scheme/host/port plus directory prefix — stricter than domain-only `:223`. Sentence 26 (`:71`) is how that prefix is compared; Yandex states no such test — different. The audit is therefore not a Yandex-acceptance check. That last clause is the row's conclusion, not a page sentence.

## Attacked statements

| statement | verdict | where |
|---|---|---|
| scope: Yandex limits, encoding, location, field caps; not the protocol or another engine | holds | `:220-224`, `:52`/`:65`/`:79`, `:276` |
| anchor quote verbatim | wrong | `:276` vs `SOURCES.md:117` (U+2019 vs U+0027) |
| anchor size 223,732 and sha `ca117c52…a24d` | holds | retained file; `SHA256SUMS:11` |
| anchor: bytes vary per fetch | holds | live 223735 / `f8c37716…` ; visible text identical |
| teaches: 2048 split 1024/1024 domain vs path | holds | `:276` |
| teaches: same-domain URLs only | holds | `:223` |
| teaches: sentences 23 and 25–26 stricter or different | holds | `c1-contract.md:63-71` vs `:223`, `:276` |
| teaches: audit is not an engine-acceptance check | holds | inference from those two differences |
