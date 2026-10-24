# KakeR29.ScreenRejectCandidates — round-28 routed defect 4: the source gate must screen and reject

Seat: `KakeR29.ScreenRejectCandidates` (scribe, axis freshness). Lane: `/home/vgpnk/Projects/shokunin/kake-shokunin`.
Sandbox (all retained bytes live here): `/fast/scratch/hyaku/kake-r29/w1/ScreenRejectCandidates/`.
Round context: primary sources retained at `e58b66c203bed4e38f89afeaa9573d980344ab64` under
`.ufo/waves/round-29/sources/` (S040 About GitHub Pages, S041 Jekyll GitHub Pages, S042 Liquid Filters, S043 Vite static deploy).

## Axes named
1. Screen honesty: a reject must rest on a named, checkable defect (outdated, framework- or site-specific, or contradicted by S040–S043), not on taste.
2. Freshness: every row's version/scope claims must match what the retained primary text and the registry say now.
3. Evidence integrity: URL, UTC access time, HTTP status, retained bytes and sha256 per candidate; every quote an exact substring of the retained text, ≤25 words.
4. No-harm: the gate must be able to reject; a screen that only admits is a defect (the routed defect).

## What I attacked
A bounded web search for secondary/community pages on GitHub Pages **project-site base paths**, one ordinary GET per page, no headless browser, no challenge solving, no probe of owned web properties. Six candidates identified; five opened; one refused with a bot challenge and recorded as unopened.

## Commands run (exit codes and observed output)
```
$ cd /fast/scratch/hyaku/kake-r29/w1/ScreenRejectCandidates && TMPDIR=$PWD python3 -B fetch_candidates.py
C1 200 42948 2026-10-22T10:34:12Z https://mademistakes.com/mastering-jekyll/site-url-baseurl/
C2 403 5853 2026-10-22T10:34:12Z https://stackoverflow.com/questions/30209076/baseurl-behavior-differs-between-localhost-and-github-pages-in-jekyll
C3 200 458345 2026-10-22T10:34:12Z https://github.com/jekyll/jekyll/issues/332
C4 200 19422 2026-10-22T10:34:14Z https://michaelcurrin.github.io/dev-cheatsheets/cheatsheets/jekyll/templating/links.html
C5 200 48372 2026-10-22T10:34:14Z https://talk.jekyllrb.com/t/relative-url-and-baseurl/2051
C6 200 95381 2026-10-22T10:35:40Z https://gohugo.io/host-and-deploy/deploy-to-github-pages/
exit=0
$ TMPDIR=$PWD python3 -B screen_candidates.py        # quote check
C1 reject ... quote words=19 exact=True ok=True | GitHub Pages does not use the latest version of Jekyll to build sites. It is currently locked at 3.9.0
C3 reject ... quote words=21 exact=True ok=True | If you're not using a CNAME and hosting your Project Page on GitHub Pages it's served out of a "project-name" subfolder
C4 include ... quote words=14 exact=True ok=True | Use the relative_url filter to ensure you get a GitHub Pages project prefix added.
C5 reject ... quote words=15 exact=True ok=True | relative_url ensures proper links by: ensuring the url to have a single leading slash always
C6 include ... quote words=4 exact=True ok=True | --baseURL "${{ steps.pages.outputs.base_url }}/"
C2 unopened status=403 ... (bot-challenge interstitial; not opened, no registry row)
quote_failures: 0
exit=0
```
Receipts: `sources/receipts.json` (URL, finalUrl, accessedUtc, status, bodyBytes, bodySha256, textSha256, textWords per candidate).
Retained text sha256 (first 16): C1 `9e49199dfbd8b14`, C3 `040620b6a2ccf00e`, C4 `38c2af9096c97938`, C5 `dd0cd1f18890c675`, C6 `dc221f2ef67ca4f5`.

## Screening result (5 opened, 3 reject, 2 include, 1 unopened)

**C1 — Made Mistakes, "Jekyll's site.url and baseurl" (2021-07-19) — https://mademistakes.com/mastering-jekyll/site-url-baseurl/ — HTTP 200 — opened 2026-10-22T10:34:12Z — REJECT**
Reason: stale on two counts. It calls Jekyll 4.2 "latest" and says Pages is "locked at 3.9.0", while the retained S041/S042 pages are Jekyll v4.4.1 (S042.txt:1) and the registry's tier-A dataset row S016 (`corpus/SOURCES.md:24`, fetched 2026-10-19) lists Jekyll 3.10.0 and github-pages gem 232. It also marks raw baseurl concatenation as an endorsed equal to the filter, which S042 ("This is recommended for a site that is hosted on a subpath of a domain") supersedes.
Quote: "GitHub Pages does not use the latest version of Jekyll to build sites. It is currently locked at 3.9.0" (19 words)
Second quote: "{{ site.baseurl }}/images/pizza.jpg" (3 words)
Flip: a current tier-A source confirms the page's version claims, or the page is refreshed to current GitHub Pages dependencies and restated in relative_url terms.

**C3 — jekyll/jekyll issue #332, "baseurl / base-url: GitHub Pages Project Pages - Relative Links Fail" (opened 2011, label frozen-due-to-age) — https://github.com/jekyll/jekyll/issues/332 — HTTP 200 — opened 2026-10-22T10:34:12Z — REJECT**
Reason: obsolete on its face. It reasons about the retired host `user-name.github.com` and a config key `base-url`; the current contract is `<owner>.github.io/<repositoryname>` (S040.txt:1) and `baseurl` plus the `relative_url` filter (S042.txt:1). Its manual prefix workaround is exactly what S041/S042 replaced.
Quote: "If you're not using a CNAME and hosting your Project Page on GitHub Pages it's served out of a \"project-name\" subfolder" (21 words)
Second quote: "http://user-name.github.com/project-name" (1 word)
Flip: a current primary source documents site.base-url or the github.com Pages host, or the issue is reopened with maintainer guidance.

**C5 — Jekyll Talk, "Relative URL and BaseURL" (posts 2018-08 to 2020-05) — https://talk.jekyllrb.com/t/relative-url-and-baseurl/2051 — HTTP 200 — opened 2026-10-22T10:34:14Z — REJECT**
Reason: wrong site and wrong vintage. The thread's scope is GitLab Pages and a local `jekyll serve`, not a GitHub Pages project site, and its guidance predates the Jekyll 4.0 link/post_url tag change; it also carries the Jekyll 3.x `$baseurl` SCSS variable question, which S042/S043 do not support for the current toolchain. The basepath fact it does state is already carried by S041/S042.
Quote: "relative_url ensures proper links by: ensuring the url to have a single leading slash always" (15 words)
Second quote: "Users can configure baseurl: to be a string with containing variable numbers of slashes" (14 words)
Flip: a current primary source confirms the thread's guidance, or the thread is updated with current-version guidance.

**C4 — Michael Currin, "Links" (Dev Cheatsheets, Jekyll templating) — https://michaelcurrin.github.io/dev-cheatsheets/cheatsheets/jekyll/templating/links.html — HTTP 200 — opened 2026-10-22T10:34:14Z — INCLUDE (tier C, queued)**
Reason: current, and consistent with S042 rather than contradicting it: it states the filter adds the GitHub Pages project prefix and that since Jekyll 4.0 the link/post_url tags carry the prefix themselves. Scope is Jekyll tag behavior only; it carries no GitHub Pages platform authority.
Quote: "Use the relative_url filter to ensure you get a GitHub Pages project prefix added." (14 words)
Second quote: "Since Jekyll 4.0, you don’t need to prepend the link or post_url tags with site.baseurl" (15 words)
Flip: a tier-A source contradicts the link/post_url baseurl claim, or the page stops being maintained; status moves mined only if a landed file cites it.

**C6 — Hugo docs, "Deploy to GitHub Pages" (last updated 2026-10-13) — https://gohugo.io/host-and-deploy/deploy-to-github-pages/ — HTTP 200 — opened 2026-10-22T10:35:40Z — INCLUDE (tier C, queued)**
Reason: current vendor recipe that resolves the project-site base path from the platform's own build output rather than a hand-written subpath, which is the same requirement S043 states for Vite. Hugo-side behavior only; it does not establish what GitHub Pages serves. Counted difference, not a contradiction: Hugo enumerates "project, user, and organization" site types while S040 groups user and organization.
Quote: "--baseURL \"${{ steps.pages.outputs.base_url }}/\"" (4 words)
Second quote: "Project sites are connected to a specific project hosted on GitHub." (11 words)
Flip: a tier-A source contradicts the configure-pages base_url output, or the page stops being maintained; status moves mined only if a landed file cites it.

**C2 — Stack Overflow, "Baseurl behavior differs between localhost and GitHub Pages in Jekyll" — https://stackoverflow.com/questions/30209076/baseurl-behavior-differs-between-localhost-and-github-pages-in-jekyll — HTTP 403 — requested 2026-10-22T10:34:12Z — NOT OPENED**
The body is a bot-challenge interstitial ("Just a moment..."). I did not attempt to pass it, so this candidate is identified but not screened and gets no registry row.

## Draft registry rows (contract shape; provisional ids, S040–S043 are taken)
```
| S044 | Made Mistakes: Jekyll's site.url and baseurl — https://mademistakes.com/mastering-jekyll/site-url-baseurl/ | community | C | Jekyll url and baseurl conventions as taught by a 2021 tutorial | How to use url and baseurl and Examples sections; page dated Jul 19, 2021; opened 2026-10-22 | REJECTED: the page calls Jekyll 4.2 latest and says Pages is locked at 3.9.0, and marks raw site.baseurl concatenation as an equal to the relative_url filter that S042 recommends for subpath hosting; flip: a current tier-A source confirms the page's version claims, or the page is refreshed to current GitHub Pages dependencies and restated in relative_url terms | rejected | 2026-10-22 | 90d | — |
| S045 | jekyll/jekyll issue 332: baseurl / base-url GitHub Pages Project Pages relative links fail — https://github.com/jekyll/jekyll/issues/332 | community | C | Project-site link resolution as discussed in a 2011 Jekyll issue | Issue body first paragraph and the 2011 comments; opened 2026-10-22 | REJECTED: the thread reasons about the retired host user-name.github.com and a base-url config key, while the current contract is owner.github.io/repositoryname with baseurl and the relative_url filter, so its manual prefix workaround is superseded; flip: a current primary source documents site.base-url or the github.com Pages host, or the issue is reopened with maintainer guidance | rejected | 2026-10-22 | 90d | — |
| S046 | Jekyll Talk: Relative URL and BaseURL — https://talk.jekyllrb.com/t/relative-url-and-baseurl/2051 | community | C | baseurl and relative_url discussion scoped to GitLab Pages and a local jekyll serve, 2018 to 2020 | Posts by ashmaroli and rdyar, 2018-08 to 2020-05; opened 2026-10-22 | REJECTED: the thread addresses GitLab Pages and localhost rather than a GitHub Pages project site, predates the Jekyll 4.0 link and post_url tag change, and repeats Jekyll 3.x baseurl SCSS advice, while the basepath fact it states is already carried by S041 and S042; flip: a current primary source confirms the thread's guidance, or the thread is updated with current-version guidance | rejected | 2026-10-22 | 90d | — |
| S047 | Michael Currin: Dev Cheatsheets Jekyll templating links — https://michaelcurrin.github.io/dev-cheatsheets/cheatsheets/jekyll/templating/links.html | community | C | Jekyll link and post_url tag prefix behavior only; no GitHub Pages platform authority | Local paths and Liquid tags sections; opened 2026-10-22 | The relative_url filter adds the GitHub Pages project prefix, and since Jekyll 4.0 the link and post_url tags carry the prefix without a manual site.baseurl | queued | 2026-10-22 | 90d | — |
| S048 | Hugo docs: Deploy to GitHub Pages — https://gohugo.io/host-and-deploy/deploy-to-github-pages/ | docs | C | Hugo's own GitHub Pages recipe and where its build takes the base URL from | Procedure Step 2 build step and Types of sites section; page last updated October 13, 2026; opened 2026-10-22 | Hugo's GitHub Pages build takes its base URL from the configure-pages action output rather than a hand-written repository subpath; this is Hugo-side behavior and does not establish what GitHub Pages serves | queued | 2026-10-22 | 90d | — |
```
Cells contain no pipe characters; `teaches` for every reject starts with `REJECTED:` and carries the flip condition in the same cell, matching the S017/S018 shape at `corpus/SOURCES.md:25-26`. Ids S044–S048 are provisional: S040–S043 are assigned to the round's primary sources, and the L1 should renumber if it assigns them elsewhere. Include rows are `queued`, not `mined`, because no landed file cites them yet; the L1 may promote them when `corpus/knowledge/pages-base-path.md` cites them.

## Evidence pointers
- Retained candidate text and receipts: `/fast/scratch/hyaku/kake-r29/w1/ScreenRejectCandidates/sources/{C1,C3,C4,C5,C6}.txt`, `.../sources/receipts.json`, bodies `.../sources/*.html.gz`.
- Scripts: `/fast/scratch/hyaku/kake-r29/w1/ScreenRejectCandidates/fetch_candidates.py`, `.../screen_candidates.py` (quote gate: exact substring, ≤25 words).
- Primary text screened against: `/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-29/sources/S040.txt:1`, `S041.txt:1`, `S042.txt:1`, `S043.txt:1`; registry row S016 at `corpus/SOURCES.md:24`.
- This report: `/home/vgpnk/Projects/shokunin/kake-shokunin/.ufo/waves/round-29/w1/ScreenRejectCandidates.md`.

## Limits and what I did not verify
- No row was written into `corpus/SOURCES.md`; the five rows above are drafts for the L1 to place.
- I did not re-open S040–S043 or re-run any round-29 counter; I read the committed retained text and the registry only.
- No live probe of any owned web property, no headless browser, and no attempt to pass the Stack Overflow challenge (C2 stays unopened).
- The include rows rest on tier-C community and vendor pages; neither is a platform authority, and I did not check their edit history, only their current text and stated update date.
- Tooling: no install was needed; Python 3.14.8 standard library only, no package changes, so nothing to record as an installed tool.
