# EntryRefusalRules

Claim C2 (Yahoo! JAPAN robots.txt assimilation), row S372 — draft of `corpus/knowledge/yahoo-japan-robots-txt-refusal-rules.md`. Ground: the retained body `.ufo/waves/round-55/sources/S372.html`, re-read in full this seat (10168 bytes, sha256 `ee8c9defeeee7abf3f2f6bd4bfb8dbb86c69cf9a272551264aa3f99f76200111`, HTTP 200, fetched 2026-10-25) plus `receipts.json`. The shokuknow staging candidate was read for reference only; nothing from it was carried (its `opened` line, its quote and its 129-unit recheck span all fail this round's ceiling). No lane file was written except this report; no git/jj mutation; no tool installed or upgraded.

## ENTRY:

```markdown
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
```

## GATE LINE:

```
- S372 — https://info-search.yahoo.co.jp/archives/002849.php — accessed 2026-10-25 — § サイト単位、ディレクトリ単位での巡回の拒否設定 1 (更新日 2010年11月24日) — quote: "サイトに対する巡回の制限はないものとみなされます" (24 units; raw substring of the retained body, sha256 ee8c9defeeee7abf3f2f6bd4bfb8dbb86c69cf9a272551264aa3f99f76200111, 10168 bytes, HTTP 200)
```

The quote sits in the page body under the H2 `サイト単位、ディレクトリ単位での巡回の拒否設定 1`, before the first H3 (`大文字と小文字の区別`); it occurs once in the body.

## ROW:

```
| Yahoo! JAPAN robots refusal rules (r55) | `knowledge/yahoo-japan-robots-txt-refusal-rules.md` (S372) | root placement, directory scope, absent-file negation, case-sensitive names, meta-tag fallback |
```

Place it after the last coverage-map row (`Field performance (r28)`, line 46) and before `## Known gaps` (line 47). Coverage cell = 10 whitespace tokens; shared 5+ letter words with the H1 `# The refusal file's own rules: root placement, directory scope, case` are `placement`, `directory`, `scope`; its one backticked path resolves at `corpus/knowledge/` (c55_readme_index.py `unindexed`/`thin`/`dangling` terms).

## UNIT COUNTS:

Unit rule as the C2 counter computes it (`units()`: one unit per CJK character, one per non-CJK whitespace token). Every span below was checked with `in` against the retained body: 20 spans, each occurring exactly once, each ≤ 25 units; none is paraphrased inside its quotes.

- 18 — "「robots.txt」という名前でテキストファイルを用意し"; 22 — "サイトのルートディレクトリに設置してください"; 15 — "サイトの一番上の階層を指します"
- 24 — "特定のディレクトリ内のみの巡回を拒否したい場合は"; 20 — "「Disallow: /」に続いてそのディレクトリ名を指定します"
- 24 — "サイトに対する巡回の制限はないものとみなされます" (Gate quote); 22 — "クローラーは巡回のたびにrobots.txtの有無を確認しており"
- 15 — "新たにrobots.txtが設置されていた場合には"; 21 — "ファイルに記載された内容に従って巡回します"; 23 — "すぐに設定の内容が反映されるわけではありません"
- 22 — "巡回の拒否（Disallow:）、クローラーの受け入れ（Allow:）の記述の前には"; 25 — "この記述がないときはすべてのクローラーに対する指示"
- 16 — "大文字と小文字の違いがあった場合"; 11 — "別のものとして扱います"; 15 — "「Allow:」は通常「Disallow:」と組み合わせて使用します"
- 17 — "「foo」ディレクトリ以下は巡回を拒否するが"; 8 — "/foo/bar.htmlは巡回を許可する"
- 13 — "「robots.txt」による巡回拒否はできません"; 5 — "メタタグで、"; 21 — "インデックスへの登録拒否を設定してください"

Rendering check (round-54 error class): each English gloss keeps the source qualifiers — the file name and `root` (quote 1–2), `site` scope and the negation `ない…とみなされます` (Gate quote), `たびに` = every crawl, `新たに` = newly, `わけではありません` = not necessarily/immediately, both directive names `Disallow:`/`Allow:` and `前には` = before, `すべて` = all crawlers, upper/lower case → treated as different things, `通常` = normally (not never-alone), `以下` = everything under, `できません` = cannot be done.

## RECHECK RUN:

```
$ grep -F -c 'サイトに対する巡回の制限はないものとみなされます' .ufo/waves/round-55/sources/S372.html
1
$ curl -fsSL 'https://info-search.yahoo.co.jp/archives/002849.php' | grep -F -c 'サイトに対する巡回の制限はないものとみなされます'
1
```

Both arms printed `1` on 2026-10-25. The grep arm ran against the retained round-55 body (the authority for every quote in the entry); the curl arm was one live GET of the same URL, run to confirm the header command is runnable and still prints a count. No robots.txt was requested and no crawl was observed.

## OMITTED:

- `「User-agent: *」は、「すべてのクローラー」という意味になります` (21 units) — the same point is carried by the quoted rule on the missing user-agent record; dropped to keep the entry inside the report budget, not because it is doubtful.
- `別々のディレクトリを指定していることになります` (22 units) — the three-spelling example is stated in prose instead.
- The literal example blocks (`User-agent: *` / `Disallow: /`; `Disallow: /cgi-bin/`; `Disallow: /foo/` + `Allow: /foo/bar.html`) — carried as inline code in prose; they add no qualifier beyond the quoted sentences, and their line breaks are markup, not content.
- The 用語 advice block's example URLs — carried in prose only (mixed ASCII/CJK lines).
- Navigation chrome (the `「クローラー」カテゴリ` and `カテゴリ一覧` sidebars, header iframe, footer LY Corporation links), `<title>`, the meta description and the `個別リンクURL` widget — not page content; not carried, and no S-id is coined for any sibling page.
- Status-code handling, percent-encoding, wildcard/`$` syntax and sitemap discovery — the page is silent; the entry records the silence (syntax ground stays with S373, a registry row). Hand-check verdicts are not claimed.

VERDICT: Entry drafted and quote-true (20 spans ≤ 25 units, each a unique raw substring of S372.html) with the Gate line, coverage row, unit counts and recheck counts reported; only `.ufo/waves/round-55/w1/EntryRefusalRules.md` was written.
