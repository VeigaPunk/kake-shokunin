source: S373 — https://info-search.yahoo.co.jp/archives/002850.php — § サイト単位、ディレクトリ単位での巡回の拒否設定 2 → 「*」記号 / 「$」記号 (更新日 2010年11月24日) — fetched 2026-10-25
verified-at: 2026-10-25
recheck: 180d — curl -fsSL 'https://info-search.yahoo.co.jp/archives/002850.php' | grep -F -c '記述された文字列を含むURLがすべてマッチします。' -> 1 (grep form run against the retained body, 2026-10-25)
ground: per-host crawl hygiene — the operator's extended pattern syntax: two symbols, and the prefix-versus-end rule that decides how wide a refusal line really is

# The end marker is what stops a path rule from matching as a prefix

The operator's second refusal page [S373] documents the two pattern symbols its crawler reads in robots.txt, and then the rule that decides how far a written path reaches. The inventory comes first [S373]:

> "robots.txtでは、以下のパターン記号が使用できます。"

(rendered: in robots.txt the following pattern symbols can be used — the page's table lists `*` and `$`.) The table gives each symbol one job [S373]:

> "ワイルドカードのパターンマッチ"
> "URLの末尾文字のパターンマッチ"

(rendered: `*` is a wildcard pattern match; `$` is a pattern match on the URL's ending characters.)

## The wildcard, and where it may sit

> "任意の長さの、任意のURL文字列にマッチ"
> "URL文字列のいずれの部分にも使えます。"

(rendered: it matches a URL string of any length, an arbitrary URL string, and it can be used in any part of the URL string.) The worked example puts it at the end of a path under the allow directive [S373]:

> "「public」で始まるすべてのディレクトリへの巡回を許可"

(rendered: allow — 許可 — the crawl of every directory that begins with `public`.)

## The end marker, and the scope of the rule that carries it

> "Disallow: /*.gif$"
> "robots.txtが設置されたサイト以下で"
> "「.gif」で終わるすべてのファイルへの巡回を拒否"

(rendered: the refusal directive `Disallow` with the value `/*.gif$`, on the site where robots.txt is placed and below it, refuses the crawl of every file that ends in `.gif` — directive name, site-and-below scope and negation are all in the source.) The page then states what the same rule catches once the end marker is dropped [S373]:

> "ファイルパスに「.gif」を含む"

(rendered: files whose file path contains `.gif`.) The end marker's own meaning is stated in two sentences [S373]:

> "「$」記号は、文字列の末尾でのみ意味をなします。"
> "末尾であると判断し、以降の文字列を無視します。"

(rendered: the `$` symbol has meaning only at the end of the string; and the crawler — the sentence's subject — judges that point to be the end and ignores the string after it.)

## The prefix rule

The sentence this entry exists for [S373]:

> "「$」記号がない場合、"
> "クローラーはプリフィクス（接頭辞）として扱い"
> "記述された文字列を含むURLがすべてマッチします。"

(rendered: when the `$` symbol is absent, the crawler treats the written string as a prefix — 接頭辞 — and every URL containing that string matches.) Every, and containing: the match is not confined to a path that begins with the string. A rule written for one file suffix therefore reaches every URL carrying that suffix anywhere, which is the page's own `.gif` demonstration above.

## Two refusal lines the page calls equivalent

> "以下のように書かれていた場合、"
> "2つの「Disallow」の指示は、同等とみなされます。"
> "Disallow: /private*"
> "Disallow: /private"

(rendered: when written as follows, the two `Disallow` directives are regarded as equivalent — a refusal line ending in a wildcard and the same line without it.)

## Against the RFC-side reading this lane holds

`robots-txt-rules.md` records the RFC 9309 side: `*` matches zero or more characters and `$` marks the end of a match — the same two jobs S373's table gives them. Four places where the two readings part company, or where only one speaks:

- **A non-final `$`.** `robots-txt-rules.md` records the lane's RFC-side reading that only a final `$` anchors at the end and a non-final `$` is literal. S373 says the crawler treats any `$` it finds as the end and ignores the string after it. [INFERENCE] on a rule with `$` in the middle the two readings decide different patterns; the operator's page does not compare itself with the RFC.
- **How specificity is measured.** `robots-txt-rules.md` records the longest normalized rule value measured in octets, counting `*` and a terminal `$`. S373 calls `/private*` and `/private` equivalent. [INFERENCE] under the octet count the two differ in length, which changes an outcome only when a competing allow rule of the same or adjacent length exists.
- **Case.** `robots-txt-rules.md` records the lane's RFC-side reading that path patterns are case-sensitive. S373's table states no case rule for either symbol, and the page carries no section on upper and lower case at all. The operator's sibling page is registry-recorded with § 大文字と小文字の区別 (corpus/SOURCES.md row S372); this entry does not carry that section's content.
- **Prefix versus containment.** `robots-txt-rules.md` matches an allow or disallow path from the first octet of the path. S373, with no `$`, matches every URL containing the string. [INFERENCE] containment is wider than a path that begins with the string.

## Where the scope sits, and what this row is not

The scope qualifier — the site where robots.txt is placed and below it — is a per-site statement. `crawl-scope-per-host.md` holds the lane's rule that the file is discovered at the service's top-level path and that project subpaths share the host-root policy. [INFERENCE] the page does not define サイト; reading its scope as the service whose root holds the file is this lane's mapping, not the operator's sentence.

`yahoo-japan-rel-nofollow-semantics.md` holds the same operator's other crawl-control page, on the link attribute. The division is clean: that entry is about an endorsement statement attached to a link, this one about the path syntax inside the refusal file, and neither page states the other's mechanism.

What this entry does not establish:

- No case rule for `*` or `$`; the page is silent (see above).
- Nothing about where robots.txt is fetched from or what its absence means; that is the sibling page's subject (S372), not this one's.
- Nothing about whether any live crawler implements this syntax as written; no robots.txt was served and no crawl was observed.
- Nothing about other operators: this is one operator's info centre page.

Every span above is an exact raw substring of the retained body `.ufo/waves/round-55/sources/S373.html` (sha256 `3173d9613128e1aaa7cb55919fa52438602095bd7bc54d4437760ee8b1c03885`, 9402 bytes, HTTP 200); the renderings are unquoted English and keep the source's qualifiers — directive names, the site-and-below scope, negation, the only of the end marker, the prefix, and the every/containing of the match. The longest span is 21 units; nothing was paraphrased inside a quotation.

Scope note: a claim about what the operator's documentation states; no robots.txt was served and no crawl observed.
