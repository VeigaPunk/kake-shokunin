# ReopenS114 — S114 apostrophe correction and the rest of `teaches`

Axis: freshness. No tools installed. Leaf only; this report is the only lane write.

## Checked

Row `corpus/SOURCES.md:122` (supersedes S109 at `:117`). Gate `corpus/lessons/round-40.md:19`. Retained `.ufo/waves/round-40/sources/yandex-sitemap.html` and `SHA256SUMS` line for that file. Contract sentences 23 and 25–26 in `.ufo/waves/round-39/c1-contract.md:63-71`.

Commands (exit 0): `curl -fsSL -D headers.txt -o live.html --max-time 60` of `https://yandex.com/support/webmaster/en/controlling-robot/sitemap` (HTTP/2 200, `Date: Fri, 23 Oct 2026 08:37:58 GMT`); `sha256sum` / `wc -c` on live and retained; visible-text compare (tags stripped, char refs decoded).

| artifact | bytes | sha256 |
|---|---|---|
| retained (matches row and `SHA256SUMS`) | 223735 | `70726f49cd6051d2b37fbf70c3908b7a01e85c5c2da435a21f5459cf343d7553` |
| this GET | 223732 | `9be69ee48e5e63f76886e8bec7e66e4a1f9956731dc2c0b071d0983479e16645` |

Visible text: equal (9677 chars). Byte drift is after the quote. Row note "page bytes vary per fetch" holds. Stamp `2026-10-23T08:29:16Z` was not re-observed.

## Apostrophe

Quote, body and the `__DATA__` copy (decoded index 69490 in both files; second U+2019 at retained 116093): "The total character limit is 2048. 1024 Characters are intended for the site’s domain name".

Code points around the mark: `U+0065 U+0020 U+0073 U+0069 U+0074 U+0065 U+2019 U+0073 U+0020 U+0064` ("e site’s d"). The file has exactly two U+2019, both in this sentence. Nearby `U+0027` are `tabindex='0'` attribute quotes, not the word.

S114 anchor slice and the teaches parenthetical `("site’s")` are U+2019. Gate `round-40.md:19` is U+2019. S109's anchor is still U+0027 ("site's"). The correction matches the page.

## Per `teaches` clause

| clause | verdict | located text |
|---|---|---|
| Anchor and Gate spell the page apostrophe as U+2019, not U+0027 | holds | quote above; neighbors `U+0065 U+2019 U+0073` |
| One engine splits the 2,048 `loc` limit 1,024/1,024 between domain and path | holds | FAQ summary "What is the maximum number of characters per URL in Sitemap?"; answer "The total character limit is 2048. 1024 Characters are intended for the site’s domain name, for example, https://site.com. The remaining 1024 characters are intended for the path…". Example `<loc>http://www.example.com/page1.html</loc>`. Halves say "intended"; only the total says "limit". The domain-name example includes the scheme. |
| Allows same-domain URLs only | overstated | File requirements: "Specify only page links of the domain where the file will be located." "Same domain" on this page is file placement: "Place the file on the same domain as the site that it was created for." The page does not say "URLs". Same section: "You can also use the Sitemap to send information about localized site pages and about images". Glossary for "internal" (the path budget's word): "Pages can be located in different directories of the same domain or on subdomains." Subdomain exclusion is not stated. |
| Sentences 23 and 25–26 are stricter or different | holds | 23 rejects a `loc` of 2,048 or more code points, with no 1,024/1,024 split (`c1-contract.md:63-65`) — different, and not stricter for a long path under 2,048. 25–26 also require the `sitemapUrl` directory prefix (`:67-71`); this page states no directory rule. The "or different" disjunct is what holds. |
| So the audit is not an engine-acceptance check | holds | follows from the split and from 25–26; not a separate page sentence |

## Attacked statements

- Apostrophe correction (anchor, teaches, Gate): **holds**. U+2019 on the page, in the retained bytes, and in S114/Gate; S109 remains U+0027.
- `teaches` split 1,024/1,024: **holds** (question says "per URL"; "intended" for each half).
- `teaches` "same-domain URLs only": **overstated**.
- `teaches` "stricter or different" / not an engine check: **holds**.

Unknown: image and localized-page rules live on other Yandex pages this item did not name; this page does not put them under the "page links of the domain" bullet.
