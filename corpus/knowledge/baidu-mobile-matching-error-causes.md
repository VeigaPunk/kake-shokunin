source: S312 — https://ziyuan.baidu.com/college/courseinfo?id=267&page=15 — § 移动适配 → 对应关系错误的常见原因 (章节时间戳 2020-08-14) — fetched 2026-10-25
verified-at: 2026-10-25
recheck: 180d
ground: per-engine crawl hygiene — how a Baidu mobile-matching submission fails, and the two causes a page-side check can see

# A mobile page that loads its main body with ajax cannot be matched to its desktop page

Baidu's mobile-matching tool manual lists the causes of a failed PC↔mobile correspondence
[S312]. One cause is a page-side rendering choice, quoted raw from the retained body:

> "手机页使用了ajax等异步加载的方法加载内容主体"

(rendered: the mobile page loads its main content with methods such as ajax and asynchronous
loading). Another cause is a crawl-side block [S312], quoted raw:

> "放开对Baiduspider的robots封禁，以便Baiduspider获取您PC站与手机站之间的对应关系。"

(rendered: lift the robots block on Baiduspider so that it can obtain the PC-site to mobile-site
correspondence). The list names five causes in all: the mobile page is unusable (for example a
dead link), the robots block above, the ajax body, a format error in the submitted rule pattern,
and a wrong correspondence (for example a desktop content page mapped to a mobile home or list
page) [S312].

## Why the lane needs this as a rule rather than trivia

- **The two failures are on opposite sides of the fetcher.** The ajax cause is what the served
  HTML does when a client without script reads it; the robots cause is whether the crawler is
  allowed to read it at all. A publisher who debugs a rejected mapping by rewriting the rule
  pattern alone has checked neither.
- **The robots cause ties the mobile-matching surface to the crawler guidance.** This page and
  the operator's friendly-crawl course (S329) state the same token: the block a publisher writes
  for Baiduspider is what withholds the correspondence, and S329 says one such block binds the
  PC and mobile crawlers together.
- **The ajax cause is a precondition for the lane's rendering rows.** The operator's render agent
  (S390, S409) is announced as fetching CSS, JavaScript and images; this page is the operator's
  statement that the main body must not be reachable only after that script runs for the mobile
  correspondence to be learnt.
- **The list is a self-check the publisher runs before resubmitting.** It is diagnosis, not a
  verdict contract: the page does not say which cause a specific rejection had.

## What this entry does not establish

- It does not establish that Baiduspider executes the page's script; the render-agent
  announcements are the rows that speak to fetching those resources, and they do not state
  execution either.
- It does not state the matching algorithm, a pass threshold, or how long a resubmission takes to
  be reflected.
- The two causes quoted are not the whole list, and the entry does not claim they are the only
  ones that occur in practice.
- The chapter prints 2020-08-14 as its timestamp; the course text is not a changelog, and the
  entry is pinned by the quoted clauses and the fetch date.

## Quote classes

Both quotations are exact raw substrings of the retained body `(S312.html, sha256 126c3da4…)`.
The list items around them are plain paragraphs whose numbering this entry renders as prose; no
quotation is a reconstructed sentence.
