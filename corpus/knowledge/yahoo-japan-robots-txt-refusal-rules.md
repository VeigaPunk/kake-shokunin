source: S372 — https://info-search.yahoo.co.jp/archives/002849.php — § サイト単位、ディレクトリ単位での巡回の拒否設定 1 (更新日 2010年11月24日) — fetched 2026-10-25
verified-at: 2026-10-25
recheck: 180d — `curl -fsSL 'https://info-search.yahoo.co.jp/archives/002849.php' | grep -F -c 'サイトに対する巡回の制限はないものとみなされます'` -> 1 (2026-10-25: curl arm 1; same grep form on the retained round-55 body 1)
ground: per-engine crawl hygiene — the operator's own rules for the refusal file a publisher writes: where it goes, what its absence means, how a path name in it is read, and what a site without root write access is told to do instead

# The refusal file's own rules: root placement, directory scope, case

The lane holds the protocol and its offline reading (`corpus/knowledge/robots-txt-rules.md`), the host-root scope of a robots policy (`corpus/knowledge/crawl-scope-per-host.md`), and what a link attribute does not say (`corpus/knowledge/yahoo-japan-rel-nofollow-semantics.md`). It did not hold the operator's own rules for the file a publisher writes; this entry carries them for Yahoo! JAPAN's engine [S372].

## The file's name and its one legal location

[S372] states the container and the location, quoted raw:

> "「robots.txt」という名前でテキストファイルを用意し"
> "サイトのルートディレクトリに設置してください"

(rendered: prepare a text file named `robots.txt`, and place it in the site's root directory.) The page defines its own term for that location, quoted raw:

> "サイトの一番上の階層を指します"

(rendered: it refers to the site's topmost tier — the site's topmost directory level.) Its example shows a root at `http://example.com/` and a first-level directory at `http://example.com/foo/`, and asks that the file be stored so that it sits at `http://example.com/robots.txt` [S372]. Directory scope is a property of the refusal value, not of the file, quoted raw:

> "特定のディレクトリ内のみの巡回を拒否したい場合は"
> "「Disallow: /」に続いてそのディレクトリ名を指定します"

(rendered: where only the crawl inside a particular directory is to be refused, specify that directory's name following the refusal value `/` already written — the value is extended by the directory name.) The page's example refuses `/cgi-bin/` only [S372].

**Contrast with the RFC side.** `corpus/knowledge/robots-txt-rules.md` states that a service publishes its rules at the lowercase `/robots.txt` path in the service's top-level path, with protocol, authority and port determining the scope (its S011 §2.3 reading). [S372] speaks of the site root and of nothing else: it states no lowercase spelling requirement for the file name and nothing about scheme, host or port delimiting the file's scope. [INFERENCE] that silence is an absence, not a disagreement with the RFC reading.

## A site with no file is not a refused site

The page's central negation, quoted raw:

> "サイトに対する巡回の制限はないものとみなされます"

(rendered: where a robots.txt is not placed, crawl restriction on the site is taken to be absent — the site is deemed unrestricted.) Its subject is the site and its condition is the file's absence; the page attaches no status code to it. The same paragraph states the refresh rule, quoted raw:

> "クローラーは巡回のたびにrobots.txtの有無を確認しており"

(rendered: the crawler checks for the presence or absence of robots.txt on every crawl.) It then draws the consequence for a newly placed file, quoted raw:

> "新たにrobots.txtが設置されていた場合には"
> "ファイルに記載された内容に従って巡回します"

(rendered: where a robots.txt has been newly placed, it crawls according to the content written in the file.) The page adds its lag qualifier, quoted raw:

> "すぐに設定の内容が反映されるわけではありません"

(rendered: the content of the settings is not reflected immediately — after the crawl the index is updated and the change reaches the search results, which takes time.)

**Contrast with the RFC side.** `corpus/knowledge/robots-txt-rules.md` states the RFC's access results: an HTTP 4xx unavailable answer means crawlers MAY access resources, while an unreachable file due to server or network errors requires a crawler to assume complete disallow (its S011 §§2.3.1.3–2.3.1.4 reading). [S372] addresses only the absent-file case and states nothing about status codes, so it covers neither a 5xx answer to a robots.txt request nor the RFC's 4xx branch. [INFERENCE] a page with 更新日 2010年11月24日 is not expected to carry the status table; the absence is recorded, not filled.

## The user-agent record in front of the directives

[S372] states where the user-agent name goes and what its absence means, quoted raw:

> "巡回の拒否（Disallow:）、クローラーの受け入れ（Allow:）の記述の前には"

(rendered: before a crawl-refusal (`Disallow:`) or a crawler-acceptance (`Allow:`) record — both directive names are named and both are in the rule's scope.) The rule that follows, quoted raw:

> "この記述がないときはすべてのクローラーに対する指示"

(rendered: when this record is absent, the rule is an instruction addressed to all crawlers.)

**Contrast with the RFC side.** `corpus/knowledge/robots-txt-rules.md` states RFC 9309's group rules as it reads them: a product token is matched case-insensitively, the rules of every matching group are combined, and the `*` group applies only when no group matches (its S011 §2.2.1 reading). [S372] states one narrower thing — a record with no user-agent line is an instruction for all crawlers — and states neither group combination nor the fallback condition. The two are compatible; the page is not a second source for the RFC rule.

## Case in the path names

The page's case rule, quoted raw:

> "大文字と小文字の違いがあった場合"
> "別のものとして扱います"

(rendered: where the directory names written after Disallow (refusal) and Allow (permission) differ in upper case and lower case, they are treated as different things.) Its example writes `Disallow: /private`, `Disallow: /Private` and `Disallow: /PRIVATE` as three distinct directories [S372].

**Contrast with the RFC side.** `corpus/knowledge/robots-txt-rules.md` states, as its own reading of S011 §§2.2.2–2.2.3 and not as RFC text, that path patterns are case-sensitive. On that point the operator page and the lane's RFC-side reading agree; the agreement is with the lane's reading, and this entry does not upgrade it into an RFC requirement. [S372] speaks of the directory names in the refusal and permission values; it states no case rule for the user-agent value.

## Permission inside a refusal

The combination rule, quoted raw:

> "「Allow:」は通常「Disallow:」と組み合わせて使用します"

(rendered: `Allow:` is normally used in combination with `Disallow:` — normally is the page's own qualifier, so the page does not say the permission record is never used alone.) The example's meaning, quoted raw:

> "「foo」ディレクトリ以下は巡回を拒否するが"
> "/foo/bar.htmlは巡回を許可する"

(rendered: everything under the `foo` directory is refused, while `/foo/bar.html` is allowed to be crawled.) The page gives the pair `Disallow: /foo/` and `Allow: /foo/bar.html` [S372].

**Contrast with the RFC side.** `corpus/knowledge/robots-txt-rules.md` states RFC 9309's matching rule as it reads it: the most specific match (the one with the most octets) is used, an allow wins a same-length tie, and no matching rule means allowed (its S011 §2.2.2 reading). [S372] gives one example and states no precedence rule; the example is consistent with longest-match, but the page does not state it, so the example is not evidence for the tie case.

## What a site without root write access is told

The deployment limit, quoted raw:

> "「robots.txt」による巡回拒否はできません"

(rendered: crawl refusal by means of `robots.txt` cannot be done — the mechanism is unavailable, not merely ineffective.) The substitute the page names, quoted raw:

> "メタタグで、"
> "インデックスへの登録拒否を設定してください"

(rendered: with a meta tag, set refusal of registration in the index.) The page names no tag value and no scope for that substitute [S372].

## What this entry does not establish

- Nothing about any crawler's live behaviour: no robots.txt was served, no crawl was observed, and no directive was tested against a crawler. Every statement above is about what the page says.
- Nothing about status-code handling, percent-encoding, the wildcard and end-anchor syntax (S373, this operator's pattern-syntax page, carries that ground), or sitemap discovery.
- Nothing about any other operator. [S372] is one operator's page, and `corpus/knowledge/robots-txt-rules.md` remains the lane's RFC-side ground.
- The page prints 更新日 2010年11月24日; this entry reports the retained body fetched 2026-10-25 and makes no claim that the operator's live documentation still reads the same today.
- It does not establish that the meta-tag substitute has the same effect as the file [INFERENCE]; the page does not compare their effects.

Scope note: a claim about what the operator's documentation states. No robots.txt was served, no crawl was observed, and no directive was tested against a crawler.
