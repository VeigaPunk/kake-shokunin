# ScoutScopeOverlap

Scope/overlap check for the three Yahoo! JAPAN robots.txt candidate entries (S372, S373, S418).
All evidence is from committed files and the retained bodies under `.ufo/waves/round-55/sources/`.
No web request was made; no file other than this report was written; no git/jj mutation was performed.

Sources read: `PROVINCE.md` (§Core 10–18, §Frontier 20–30, §Adjacent 32–41, §Round-52 367–383),
`corpus/QUALITY.md` (10 Replayable claim, 15 Platform mechanism, 1088–1116 round-50/53 criteria,
1118–1144 round-54 criteria), `corpus/knowledge/{robots-txt-rules,crawl-scope-per-host,
yahoo-japan-rel-nofollow-semantics,baidu-friendly-crawl-guidance}.md`, `corpus/README.md`
(`## Coverage map`, 15–46), `corpus/SOURCES.md` (158 S372, 159 S373), `.ufo/waves/round-55/contract.md`
and `c55_quote_truth.py`, shokuknow `merge/kake/MERGE-REPORT.md` (80, 81, 88) and
`SOURCES.append.md` (92, 93, 100).

## SCOPE:

All three candidates sit inside the lane's Frontier ground "Crawl hygiene per host (robots.txt,
sitemap scope, canonical signals)" (`PROVINCE.md:22-24`) and are the same shape as the round-52
per-engine entries admitted at `PROVINCE.md:373-383` (Yahoo `rel=nofollow` S374, Baidu S329/S312):
operator-documented crawl hygiene beyond Google, held as **Frontier knowledge — no gate, no owned
property audited, no publish action; publishing stays operator-owned**. None may be promoted to Core:
Frontier moves to Core only with source-backed entries *and* a gate (`PROVINCE.md:30`), and this
round ships no gate for them. Adjacency (`PROVINCE.md:34-35`) is respected: no browser-execution or
client-side-crawler claim, so tabi's province is untouched.

### Candidate 1 — `corpus/knowledge/yahoo-japan-robots-txt-refusal-rules.md` (S372)
**In scope, narrowed.** The operator's own rules for the refusal file (root placement, absence
semantics, re-read on every crawl, index lag, case-sensitivity of path names, `Allow` used with
`Disallow`, the "cannot place a file at the root → refuse indexing with a meta tag" fallback) are
operator ground the lane holds from no Yahoo source.
*Flip condition (refuse as duplicate):* if the entry's substance collapses to what the lane already
holds from RFC 9309 — host-root/lowercase placement (`robots-txt-rules.md:15`), path-name
case-sensitivity (`:53`), `*`/`$` syntax (`:51`) — it must be refused, because those are the
protocol side, not new ground. Admit only the operator-specific residue, each quoted with a located
section.

### Candidate 2 — `corpus/knowledge/yahoo-japan-robots-pattern-syntax.md` (S373)
**In scope, narrowed, with one contrast to police.** Yahoo's own statement of the two pattern
symbols, of prefix matching when the end marker is absent, of the equivalence of a trailing-wildcard
line with its bare form, and of the end marker's "rest of the line is ignored" rule.
*Flip condition:* the end-marker reading must be recorded as *this operator's statement*, never as
the protocol's — the lane's own reading of RFC 9309 is that a non-final `$` is literal
(`robots-txt-rules.md:53`). If the entry presents Yahoo's reading as the RFC rule, refuse. Also
refuse if the entry is only RFC §2.2.2/§2.2.3 restated in Japanese (`robots-txt-rules.md:49-51`).

### Candidate 3 — `corpus/knowledge/yahoo-japan-robots-txt-basics.md` (S418, staged id S380)
**In scope, narrowly.** What the file is for and when it is consulted.
*Flip condition (refuse as duplicate):* if the entry reduces to "the file lives at the site root
and its absence means unrestricted", it duplicates `crawl-scope-per-host.md:7-12` and
`robots-txt-rules.md:15-21` and must be refused. It is admit-able only for the operator's own
framing the lane holds from nowhere else: the file is a request channel to the search engine
carrying **two** payloads — pages/directories to refuse *and* the sitemap location — and the
crawler looks in the root directory for it first.

## OVERLAP:

(file:line pairs; left = lane ground already held, right = candidate. Bare file names below are
relative to `corpus/knowledge/`.)

- `robots-txt-rules.md:15` (lowercase `/robots.txt` at the service's top-level path) ↔ S372 placement quote; S418 root-directory lookup.
- `robots-txt-rules.md:17` (a robots file in a subdirectory does not set the root rules) ↔ S372 root placement.
- `robots-txt-rules.md:19-21` (4xx ⇒ MAY access, 5xx/unreachable ⇒ MUST assume complete disallow) ↔ S372/S418 "no file ⇒ no restriction".
- `robots-txt-rules.md:33,35` (the three records; records before the first `user-agent` are ignored) ↔ S372 "the `User-agent:` name precedes `Disallow:`/`Allow:`"; "if that name is absent the instruction counts for all crawlers".
- `robots-txt-rules.md:39-41` (product token case-insensitive, `*` group as fallback) ↔ S372 "`User-agent: *` means all crawlers".
- `robots-txt-rules.md:49-51` (path matched from the first octet; most specific match; `*` = zero or more, `$` = end of match) ↔ S373 both pattern symbols and the prefix rule.
- `robots-txt-rules.md:53` (lane reading: empty value never matches, only a final `$` anchors, a non-final `$` is literal, path patterns case-sensitive) ↔ S373 end-marker reading; S372 case-sensitivity quote.
- `robots-txt-rules.md:57` (`/robots.txt` implicitly allowed) ↔ S372/S418 absence semantics.
- `crawl-scope-per-host.md:7-12` (rules discovered at the service root `/robots.txt`; 4xx/5xx consequence) ↔ S418 "the crawler first looks in the site's root directory for robots.txt"; S372 placement.
- `crawl-scope-per-host.md:14-18` (sitemap scope by location; a `Sitemap:` line in the host-root robots file is a supported discovery route, per S012/S013 — Google/sitemaps.org, not Yahoo) ↔ S418 "サイトマップの位置" as the file's second payload.
- `yahoo-japan-rel-nofollow-semantics.md:26-27` (already names "the lane's robots-refusal ground (S372, S373)") ↔ both new S372/S373 entries: a forward reference this round makes resolvable.
- `baidu-friendly-crawl-guidance.md:39-42` ("The lane holds robots pattern syntax from another operator (S373)") ↔ the new pattern-syntax entry — it is the "another operator" that line points at.
- `corpus/SOURCES.md:158` (S372 row) and `:159` (S373 row) ↔ the two adopted rows; their `used-by` cells are the only cells this round may change (contract C3/C4: S372 = prior + refusal-rules path; S373 = prior nofollow+baidu + pattern-syntax path; S418 = exactly the basics path).
- Registry state: 155 rows at base; `S418` is absent from `corpus/SOURCES.md` (max id S417) — it must be appended before any entry cites it (QUALITY:1115).
- Internal overlap between candidates: S372 and S418 both state "no file ⇒ no restriction" ("サイトに対する巡回の制限はないものとみなされます" / "そのサイトに対する巡回制限はないものとみなして"). The split must be explicit — S372 = the file's own rules; S418 = what the file is and when it is consulted — so the same claim is not carried twice.
- Coverage-map overlap: at base the C1 counter reports 21 of 46 knowledge files unindexed (`c55_readme_index.py` at `fcaf4b8` → `index_mismatches=21`, exit 1). The three new files raise the population to 49, so each needs its own coverage-map row.

## CROSS-LINKS:

Required (plain path, no new S-ids):
- Each new entry → `corpus/knowledge/robots-txt-rules.md` (RFC-side contrast only where that file itself states the RFC side: `:15`, `:19-21`, `:49-53`).
- Each new entry → `corpus/knowledge/crawl-scope-per-host.md` (host-root scope, sitemap scope) — S418's sitemap payload is the operator's counterpart of `crawl-scope-per-host.md:14-18`.
- Each new entry → `corpus/knowledge/yahoo-japan-rel-nofollow-semantics.md` (same operator; the distinction the lane already drew between an endorsement statement and a crawl refusal).
- `corpus/knowledge/baidu-friendly-crawl-guidance.md:39-42` → the new pattern-syntax entry (the "another operator (S373)" it already names); read-only cross-reference, no edit from this seat.
- `corpus/SOURCES.md` `used-by` for S372/S373 extended to the new entries; S418 appended as a new row (registry 155 → 156) with `status=mined`, `opened=2026-10-25`, `recheck=180d`, `used-by` = the basics entry path (contract C3/C4).

## RISKS:

1. **Unit ceiling (contract C5, hard fail).** The staged quotes are over the 25-unit ceiling under the
   lane's unit rule (one unit per CJK character, one per non-CJK whitespace token; counter
   `c55_quote_truth.py:137-139`, `UNIT_CEILING=25` at `:70`): measured staged S372 quote = **48 units**,
   S373 = **41**, S418 = **46**. Each must be trimmed. Verified raw substrings of the retained bodies
   that satisfy ≤25 units (all `grep -F -c` = 1 against the retained file):
   S372 — `「User-agent: *」は、「すべてのクローラー」という意味になります。` (21),
   `この記述がないときはすべてのクローラーに対する指示` (25),
   `ただし、クローラーは巡回のたびにrobots.txtの有無を確認しており` (25),
   `すぐに設定の内容が反映されるわけではありません。` (23),
   `Disallow（拒否）、Allow（許可）のあとに記述されたディレクトリ名は` (21),
   `別のものとして扱います。` (11), `「Allow:」は通常「Disallow:」と組み合わせて使用します。` (15),
   `インデックスへの登録拒否を設定してください。` (21),
   `サイトのルートディレクトリに設置してください。` (22);
   S373 — `ワイルドカードのパターンマッチ` (15), `URLの末尾文字のパターンマッチ` (13),
   `「$」記号がない場合、` (7), `クローラーはプリフィクス（接頭辞）として扱い` (20),
   `記述された文字列を含むURLがすべてマッチします。` (21),
   `「$」記号は、文字列の末尾でのみ意味をなします。` (19), `以降の文字列を無視します。` (12),
   `2つの「Disallow」の指示は、同等とみなされます。` (15);
   S418 — `robots.txtは、検索エンジンに対する要求を伝えるファイルです。` (23),
   `クローラーに巡回してほしくないウェブページや` (22), `サイトマップの位置` (9),
   `クローラーによる巡回の際は、` (13), `まずサイトのルートディレクトリ` (15),
   `そのサイトに対する巡回制限はないものとみなして` (23),
   `robots.txtが設置されていた場合には、その内容に従って巡回します。` (25). The 6-unit floor also
   applies: every quoted span of 6+ units below the header is checked.
2. **English glosses in ASCII double quotes break C5.** The counter scans every `"…"` span of 6+ units
   in the entry body (`c55_quote_truth.py:309`) and requires it to be a raw substring of that row's
   retained body. A rendered English sentence in double quotes would be counted and would fail.
   Render in parentheses without ASCII quotes, as `yahoo-japan-rel-nofollow-semantics.md` does.
3. **Locator must be a heading that exists (QUALITY:1116).** Headings present in the retained bodies:
   S372 — `サイト単位、ディレクトリ単位での巡回の拒否設定 1` (h2), `大文字と小文字の区別`, `Allowの使い方`;
   S373 — `…拒否設定 2` (h2), `「*」記号`, `「$」記号` (each with a `注意` list);
   S418 — `robots.txtとは？` (h2), `「基本事項」カテゴリ`. The staged S418 anchor
   `§ 本文（クローラーによる巡回時の robots.txt の参照手順）` (staged `SOURCES.append.md:100`) does **not**
   occur in the retained body (string check: absent) — a paraphrase; the new S418 row's anchor must
   name a heading that occurs there (e.g. `§ robots.txtとは？`, 更新日 2010年11月24日).
4. **Registry rows S372/S373 are frozen except `used-by` (contract C3).** The lane's S372 anchor
   (`corpus/SOURCES.md:158`) ends at `§ 大文字と小文字の区別`, while S372's placement and absence quotes
   sit in the page body *before* that heading; the entry's own `source:` locator must therefore name the
   section containing each quote it carries. The S373 anchor (`…:159`) covers `§「*」記号 → 注意` and
   `§「$」記号 → 注意`, but the two symbol-table rows (`ワイルドカードのパターンマッチ`,
   `URLの末尾文字のパターンマッチ`) sit in the body before the first `注意`.
5. **Absence semantics must not overwrite the lane's reading.** S372/S418 say a site with no file is
   unrestricted; the lane's RFC reading is that an *unreachable* file means complete disallow
   (`robots-txt-rules.md:19-21`). Different conditions; keep them apart.
6. **End-marker contrast.** Yahoo's "once the crawler sees `$` it judges the end and ignores the rest"
   is stronger than the lane's reading that a non-final `$` is literal (`robots-txt-rules.md:53`).
   Report it as the operator's statement and cross-link; do not merge.
7. **Material-qualifier preservation (QUALITY:1120, round-54 defect class).** Every rendering must keep
   the qualifiers the Japanese states — ルートディレクトリ (root), 巡回ごと (every crawl),
   大文字と小文字 (case), プリフィクス (prefix), すべてのクローラー (all crawlers),
   末尾でのみ意味をなします (meaningful only at the end).
8. **Staged id S380 must not be cited.** The lane's third row is **S418** (`contract.md`, C3 `NEW_ROWS`);
   staged `SOURCES.append.md:100` uses S380 and a 2026-10-24 opened date — neither carries into this lane.
9. **Coverage-map landing shape (C1).** The counter reads only the `## Coverage map` section
   (`c55_readme_index.py:90-92` `coverage_sections`) and uses that table's header for every row in it,
   so the ground-map table drafted elsewhere belongs in its own `##` section, not inside
   `## Coverage map`. Each new entry needs a row whose Entry cell contains `knowledge/<file>`
   (REF_RE `:70`), with a coverage cell of ≥5 whitespace tokens sharing a 5+ letter word with the
   entry's H1/first 1500 chars, a coverage cell string not duplicating another row's, and ≤2 knowledge
   files per row (`MAX_FILES_PER_ROW=2`, `:66`); otherwise the row is scored `multi`/`thin`/`duplicate`
   (`c55_readme_index.py:159-166,203-208`).
10. **Evidence honesty.** The three retained bodies verify against `receipts.json` (sha256
    `ee8c9def…`/10168 B, `3173d961…`/9402 B, `2b146a72…`/7559 B; HTTP 200; fetched 2026-10-25T20:40Z).
    The staged package's `opened`/`verified-at`/`recheck` values prove nothing here; recheck commands
    must be re-run against the retained bodies and counts reported as counts, never as words
    (QUALITY:1133). No web request was made by this seat.

VERDICT: All three candidates are in scope as Frontier per-engine crawl-hygiene knowledge, each
narrowed by a stated flip condition; measured overlaps are RFC-side ground in
`robots-txt-rules.md:15-57` plus `crawl-scope-per-host.md:7-18`, and the two adopted rows' `used-by`
cells plus a new S418 row are the only registry edits; the blocking risk is the 25-unit quote ceiling
(staged quotes measure 48/41/46 units) and the requirement that glosses stay outside ASCII double
quotes.
