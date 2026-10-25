# ScoutRejectDnsId
ATTACKS: the UNADOPTED staged candidate `yahoo-japan-crawler-identification-by-dns.md` (staged id S386, source URL `https://info-search.yahoo.co.jp/crawl/`), staged in `/home/vgpnk/Projects/shokuknow/merge/kake/knowledge/corpus/knowledge/yahoo-japan-crawler-identification-by-dns.md` and staged registry row S386 in `/home/vgpnk/Projects/shokuknow/merge/kake/SOURCES.append.md:106`. Lane build under attack: `a7a548e102b71bd16b0a6ddafa469393a2c98b69`.

CANDIDATE:

- The staged knowledge file's `source:` line names **S386**, URL `https://info-search.yahoo.co.jp/crawl/`, locator `§ クローラー名（ユーザーエージェント名）の確認方法`, with "no revision printed; pinned by the quoted clause and the access date — fetched 2026-10-24". It has no `verified-at:`/`recheck:`/`ground:` block-quote body and **zero blockquote lines** (`grep -n '^>' .../yahoo-japan-crawler-identification-by-dns.md` → "no blockquote lines"), so the candidate carries no located quote of its own.
- Its thesis (staged file, verbatim): the operator "identifies a crawler by DNS, and says so on its own category page"; the index "recommends that a server restrict access by the address the crawler's DNS points at rather than by the name". The staged row S386 adds: "the operator's own answer to 'which crawler is this' is a DNS lookup, not a name list … the category itself is the ten-page crawl-behaviour set".
- Claim under test: **the DNS-restriction recommendation and the ten-page crawl-behaviour set are on the cited index page**, and the candidate is admissible to the lane.

FETCH:

One plain GET of the cited URL, then one GET of the linked page the index names (needed to test the candidate's mechanism claim, since the index only summarises it):

- `curl -fsSL --compressed -o "$D/crawl.html" -w 'http_code=… size=… url=… time=…' 'https://info-search.yahoo.co.jp/crawl/'` → `http_code=200 size=2820 url=https://info-search.yahoo.co.jp/crawl/ time=0.956207`, `curl_exit=0`.
  - bytes on disk: **9299** (`wc -c < "$D/crawl.html"`); sha256 **498d36dbabdddb86bf0b4e2cfacf91f578d9ef79c4b57f2025de0e904f75b939** (`sha256sum`).
  - Content: `<title>クローラー - インフォセンター - Yahoo!検索</title>`, charset=UTF-8, XHTML 1.0; 10 `<h3 class="entryListTitle">` entries, 10 unique `archives/0028xx.php` links; **zero** `20\d\d` year tokens and zero `更新日|掲載|最終更新` markers — the index genuinely prints no revision date.
- Secondary fetch of the linked page: `curl -fsSL --compressed -o "$D/002855.html" … 'https://info-search.yahoo.co.jp/archives/002855.php'` → `http_code=200 size=2853`; bytes **8703**; sha256 **9ce5a4abd0087191485aa744e7a37c5b0d400ca4631b86984de11ea89fdd05e6**. It prints `更新日 2010年11月24日` and holds the substantive text (`DNSルックアップの方法`, `サーバーでのアクセス制限の際の注意点`, `nslookup` ×2, `偽装`).
- Tools: none installed. `curl`, `python3` and `git` were already present on the host; no pacman/`uv`/`npm` action was taken, so there is no install or version record to report.

VERDICT TABLE:

| # | Claim tested | Observed | Verdict |
|---|---|---|---|
| V1 | The DNS-restriction recommendation is on the cited index page (S386's URL) | The two clauses exist on the index: `サーバー側でアクセス制限をする場合には` and `ドメインネームサーバー（DNS）を使ったアクセス制限` (raw substrings of my fetch, offsets 4634 / 4667, both after the first `<h2` at 2399, inside the 002855 entry body at 4560) | **TRUE on the index** — but the candidate's paraphrase "by the address the crawler's DNS points at" is a claim the index does not make; the index says only *DNS を使った* restriction. The mechanism (reverse lookup of an IP → domain, `nslookup` ×2, `IPアドレスによるアクセス制限ではなく`) lives only on 002855 |
| V2 | The candidate's core gloss — the operator "identifies a crawler by DNS … rather than by the name" — is carried by the cited page | The index contains **no** `nslookup`, **no** `偽装`, **no** `IPアドレス` (three greps, all 0). The "name is spoofable, so restrict by DNS not by IP" statement is on 002855, which the candidate's `source:` line does not cite and which the lane does not hold (`grep -c 'archives/002855.php'` on the registry → 0) | **NOT ON THE CITED PAGE** — the load-bearing mechanism claim is ungrounded at S386; it is a claim about 002855. This is the concrete reason |
| V3 | The index "holds the operator's crawl-behaviour set in one place — ten pages" | 10 `<h3 class="entryListTitle">` entries and 10 unique `archives/0028xx.php` URLs | **TRUE** — the ten-page count is right |
| V4 | The candidate's supporting claim that the lane "already holds [the ten pages] in full" | Registry row counts for the ten URLs at `a7a548e`: `002845=0 002846=0 002849=1 002850=1 002851=1 002852=1 002854=0 002855=0 002856=0 002857=0` — **4 of 10 held**, 6 unheld (002845, 002846, 002854, 002855, 002856, 002857 have no row at all; `grep -c` each) | **FALSE at the build revision** — "in full" is wrong; the lane holds 4 of the ten rows, and the candidate's own admission (the DNS one) is among the unheld six |
| V5 | Scope: per-host crawl hygiene / publisher-side (kake) vs browser/DOM (tabi) | `PROVINCE.md:22` Frontier lists "Crawl hygiene per host"; `PROVINCE.md:34` gives tabi "client-side crawler discipline" and kake "publisher-side placement". The candidate's ground line is "per-host crawl hygiene — how the operator says to identify a crawler, and what it says to do about one that misbehaves" | **IN SCOPE** for kake (publisher-side, per-host), *provided* it is grounded on the operator's own words. The scope ruling is not the rejection reason |
| V6 | Registry collision: does the cited URL already appear in `corpus/SOURCES.md` at the build revision? | `git show a7a548e…:corpus/SOURCES.md \| grep -c 'https://info-search.yahoo.co.jp/crawl/'` → **0**; `grep -c '\| S386 \|'` → **0**; `git grep -c 'info-search.yahoo.co.jp/crawl/' a7a548e… -- corpus/` → 0 files. Registry total 156 rows | **NO COLLISION BY URL** — S386 is a genuinely new id and URL for this lane. Note `staged-ids` at the build rev lists S287–S415 (S386 present) and the lane's own max id is S418, so S386 is free |
| V7 | Round-53 criterion: does the cited id resolve in **this lane's** registry? | `S386` is absent from `corpus/SOURCES.md` at `a7a548e` (0 rows). The staged row lives only in the staged package's `SOURCES.append.md` | **FAILS as-is** — `corpus/QUALITY.md:1115` requires every `S###` cited in `corpus/knowledge/` to name a row in *this lane's* `corpus/SOURCES.md` at the citing revision |
| V8 | Quote ceiling (≤ 25 units, one per CJK char / non-CJK whitespace token) | Every candidate quote usable from the index is fine, but the **full** sentences exceed the ceiling: `ドメインネームサーバー（DNS）を使ったアクセス制限をおすすめします` = **29** units; `挙動の不審なアクセスログが見られた場合の対応方法` = **34**; the whole entry-body sentence = **57**. Only trimmed spans fit: the 19-, 21-, 24-unit spans below | **CONDITIONAL** — the candidate must quote trimmed spans, not the sentences. The staged row's own wording carries no quoted span at all |

**VERDICT: REJECT** (for this round / as staged).

Concrete reason, in the order the evidence bites: **(a) claim not on the page** (V2) — the candidate's load-bearing mechanism claim ("identifies a crawler by DNS rather than by the name", "the address the crawler's DNS points at") is a fact about `archives/002855.php`, not about the cited index page `info-search.yahoo.co.jp/crawl/`, which contains no `nslookup`, no `偽装` and no `IPアドレス`; **(b) claim not on the page** for the supporting assertion that the lane "already holds [the ten crawl pages] in full" (V4) — at `a7a548e` the lane holds 4 of the 10 rows, not 10; **(c) an unresolvable source id** (V7) — S386 names no row in this lane's registry, which `corpus/QUALITY.md:1115` forbids for a `corpus/knowledge/` citation. Not the reason: unreadable body (fetch is 200/9299 bytes, fully readable), URL duplicate (V6 — count 0), out-of-scope (V5 — in scope), quote ceiling per se (V8 — trims exist). Nothing was installed and nothing in the lane, sibling lanes, or lane Git/jj state was mutated; only this report file was written.

Flip condition (all three, together):

1. **Re-ground the entry on the page that carries the mechanism.** Adopt `https://info-search.yahoo.co.jp/archives/002855.php` as a new lane row (it prints `更新日 2010年11月24日`, so it can carry a dated locator) and cite it — not `info-search.yahoo.co.jp/crawl/` — for the DNS-vs-name restriction rule. The index page may still be registered as a *category-index* row for the "ten-page crawl-behaviour set" fact alone, with its own (verifiable) content quote and the honest locator "no revision printed on the page".
2. **Register the id in this lane's registry** before citing it: append a row for the adopted URL under a free id (the lane's ids run to S418; `staged-ids` already claims S386, and the round-55 contract's collision list does not include S386) so that `S###` in `corpus/knowledge/` resolves in `corpus/SOURCES.md` at the citing revision (`corpus/QUALITY.md:1115`), with a recheck argv of the same shape as the other Yahoo rows.
3. **Withdraw or correct the two unsupported assertions**: the "lane already holds [the ten pages] in full" sentence (true only for 4 of 10 at `a7a548e`; if the staged package's ten rows were adopted, say which ones and at which revision) and the "identifies a crawler by DNS rather than by the name" gloss, which the index does not state.

QUOTES:

Located quotes are **raw substrings of my own fetch**, each ≤ 25 units by the counter's rule (`CJK_RE` per-char + non-CJK whitespace token), and each is unique — none occurs in any of the lane's five retained Yahoo bodies (`.ufo/waves/round-5{2,3,5}/sources/S{367,372,373,374,418}.html`, each checked for both clauses → 0 hits).

Q1 — source `https://info-search.yahoo.co.jp/crawl/`, heading `§ クローラー名（ユーザーエージェント名）の確認方法` (the `<h3 class="entryListTitle">` at offset 4427; the span sits in that entry's body at 4560, after the first `<h2` at 2399):

> サーバー側でアクセス制限をする場合には

- units: **19**; raw substring of my fetch: True; occurs exactly once (offset 4634).

Q2 — same source and heading (offset 4667):

> ドメインネームサーバー（DNS）を使ったアクセス制限

- units: **21**; raw substring of my fetch: True; occurs exactly once.

Q3 — same source and heading (offset 4594):

> 挙動の不審なアクセスログが見られた場合の対応方法

- units: **24**; raw substring of my fetch: True; occurs exactly once.

Q3 is the qualifier-bearing clause: it is the part that says the *name* page is about suspicious access logs, and it is the span the candidate's gloss rests on. Note the two Q1/Q2 spans are **meta-description echoes as well as body text** — the same sentence also appears verbatim in the page's `<meta name="description">` (offsets 376/416/449), which is why a locator claiming a body section must use the `<h3>` heading, not the meta tag.

Flip-condition quote (on the page the mechanism claim actually needs — `archives/002855.php`, heading `§ サーバーでのアクセス制限の際の注意点`, `更新日 2010年11月24日`):

> IPアドレスによるアクセス制限ではなく、前述のDNSを参照した

- units: **25** (exactly at the ceiling); raw substring of my fetch: True; **absent from the index page** (`in_index=False`) — which is the sharpest single piece of evidence that V2 is a real defect and not a nitpick.

REGISTRY COLLISION CHECK:

All commands run at `a7a548e102b71bd16b0a6ddafa469393a2c98b69` in `/home/vgpnk/Projects/shokunin/kake-shokunin` (read-only `git show`/`git grep`).

| Check | Command | Result |
|---|---|---|
| Cited URL already in registry | `git show a7a548e…:corpus/SOURCES.md \| grep -c 'https://info-search.yahoo.co.jp/crawl/'` | **0** — the URL does **not** already appear in `corpus/SOURCES.md` at the build revision |
| Cited id already in registry | `git show a7a548e…:corpus/SOURCES.md \| grep -c '\| S386 \|'` | **0** — S386 names no row in this lane's registry |
| URL anywhere in lane corpus | `git grep -c 'info-search.yahoo.co.jp/crawl/' a7a548e… -- corpus/` | 0 files |
| Linked page (002855) in registry | `git show a7a548e…:corpus/SOURCES.md \| grep -c 'archives/002855.php'` | **0** — the mechanism's home page is also unheld |
| Id S350 (staged id for 002855) in registry | `grep -c '\| S350 \|'` | **0** |
| Registry size / id headroom | row count = **156**; ids > 380 present: S390, S409, S416, S417, S418 (max **S418**) | S386 is free and does **not** appear in the round-55 contract's collision list (S312 S329 S367 S372 S373 S374 S390 S409) |
| Staged id reservation | `.ufo/waves/round-55/assimilation/staged-ids` at the build rev lists S287–S415, S386 included | no lane-row conflict, but the id must still be *appended* to `corpus/SOURCES.md` before being cited from `corpus/knowledge/` (`corpus/QUALITY.md:1115`) |
| Ten crawl-set URLs held by the lane | per-URL `grep -c 'archives/<u>.php'` | `002845=0 002846=0 002849=1 002850=1 002851=1 002852=1 002854=0 002855=0 002856=0 002857=0` → **4 of 10**, contradicting the candidate's "in full" |
| Lane rows that *are* Yahoo | registry rows S367 (002852), S372 (002849), S373 (002850), S374 (002851), S418 (002885) | 002885 is **not** one of the index's ten; the index's own ten are the 002845–002857 set |

No credential material, session token, `op://` reference or private URL appears in this report; the only URLs named are the two public Yahoo! JAPAN documentation pages fetched above.
