source: S329 — https://ziyuan.baidu.com/college/courseinfo?id=1399 — § 友好抓取 → robots写法 / 使用robots巧妙避免蜘蛛黑洞 (no revision printed on the page — pinned by the quoted clauses and the fetch date) — fetched 2026-10-25
verified-at: 2026-10-25
recheck: 180d
ground: per-engine crawl hygiene — what a Baiduspider robots block binds, and what a parameter-generated URL space does to that crawler

# A Baiduspider robots block binds the desktop and mobile crawlers at once

Baidu's own site-building course states the scope of a `robots.txt` block aimed at its crawler
[S329], quoted raw from the retained body:

> "如果封禁的agent是Baiduspider，会对PC和移动同时生效"

(rendered: if the blocked agent is Baiduspider, the block takes effect for both PC and mobile).
The paragraph continues that neither the PC nor the mobile Baiduspider will fetch the blocked
object [S329]. The same section says the crawler honours the two wildcard symbols [S329]:

> "支持使用通配符"

and the page's list names them as `*`, matching 0 or more arbitrary characters, and `$`, matching
the line-end [S329].

The section on the crawler trap (蜘蛛黑洞) defines it as a URL space a site generates from
parameters [S329], quoted raw:

> "蜘蛛黑洞特指网站通过极低的成本制造出大量参数过多、内容类同但"

(rendered: the trap is the low-cost generation of many parameter-heavy, near-identical but
distinct URLs, which keeps the crawler in a loop and spends it on pages of no value). The page's
remedy is a `robots.txt` rule over the generated space [S329].

## Why the lane needs this as a rule rather than trivia

- **One token governs two crawlers.** The lane's device-conditional publishing rows treat PC and
  mobile as separate renderings; for this operator a single `User-agent: Baiduspider` block
  covers both, so a publisher cannot exempt the mobile crawler from a rule written for the
  desktop one. This is the Baidu counterpart of the Googlebot-subtype rule the lane holds (S263),
  with the opposite consequence: there the product token is shared and the *user-agent* string
  separates the subtypes; here the product token itself binds both.
- **A wildcard rule is what a parameter space needs.** The lane holds robots pattern syntax from
  another operator (S373) and the general refusal-file semantics (S011, S095); this page is the
  operator-specific statement that its crawler reads the same two symbols, which is what makes a
  one-line rule over a filter-generated URL space expressible at all.
- **The trap is a publisher-side generation problem, not a crawler fault.** The definition ties
  the trap to URLs the site itself creates, so the fix is on the site (stop generating them, or
  refuse them), not a crawl-rate complaint.

## What this entry does not establish

- It does not establish that Baiduspider executes a page's script: the page describes fetching
  and URL generation, and the lane's rendering rows (S390, S409) are where the render agent is
  named.
- It does not state a crawl-rate limit, a per-host budget, or how long a blocked object stays
  unfetched after the block is lifted.
- It does not establish the other operators' wildcard support; `*` and `$` here are this
  operator's statement about its own crawler.
- The page prints no revision date for the course text; the entry is pinned by the quoted
  clauses and the fetch date, not by a documented revision line.

## Quote classes

The three quotations are exact raw substrings of the retained body `(S329.html, sha256
452aabc3…)`. The wildcard quotation is one continuous run of bytes; the two symbols it introduces
appear on the same page as `*` and `$` inside separate spans, so this entry names them in
backticks rather than quoting each symbol. Nothing in this entry is a rendered-text reconstruction.

## Round-53 source corrections (append-only)

The round-52 `source:` line's locator is superseded for the quoted PC/mobile clause by S416: it sits under `如何正确识别Baiduspider移动ua`. The other two quoted passages sit under `robots写法` (wildcards) and `使用robots巧妙避免蜘蛛黑洞` (spider trap); “the same section” must not be read to cover all three. The page-level header prints `最新更新章节：2019-09-18`; the earlier “no revision date” statement above is withdrawn. The Baidu and Google crawler cases are parallel on the shared robots token and user-agent subtype distinction; the earlier “opposite consequence” comparison is withdrawn. The original lines remain for history.
